"""
LLM Generation Service — GPT-4o RAG Synthesis
Retrieves relevant legal chunks from Supabase (pgvector) and synthesizes
a professional answer using OpenAI GPT-4o via LangChain.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from services.vector_store import get_supabase_client

load_dotenv()

# ---------------------------------------------------------------------------
# System prompt — enforces Zero Hallucination rules
# ---------------------------------------------------------------------------
LEGAL_SYSTEM_PROMPT = """You are a senior legal assistant AI. Your role is to
provide clear, professional, and accurate answers to legal queries based ONLY
on the context provided below.

RULES — follow these strictly:
1. Use ONLY the information present in the provided context paragraphs.
2. If the context does not contain enough information to answer the question,
   respond with: "I don't have enough information in the available documents
   to answer this question."
3. Never fabricate statutes, case names, penalties, or legal definitions.
4. Cite the source document and page number when available.
5. Structure your response in clear, readable paragraphs suitable for a
   legal professional.

CONTEXT:
{context}
"""


def _get_llm() -> ChatOpenAI:
    """Return a ChatOpenAI instance configured for GPT-4o."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")
    return ChatOpenAI(
        model="gpt-4o",
        temperature=0,          # deterministic for legal accuracy
        api_key=api_key,
    )


def _get_embedding_model() -> OpenAIEmbeddings:
    """Return an OpenAIEmbeddings instance for query vectorisation."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")
    return OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)


# ---------------------------------------------------------------------------
# Step 1: Retrieve relevant chunks from Supabase / pgvector
# ---------------------------------------------------------------------------
def retrieve_relevant_chunks(query: str, match_count: int = 5) -> list[Document]:
    """
    Embed the user query and perform a similarity search against the
    Supabase `document_chunks` table using pgvector.

    Returns a list of LangChain Document objects with page_content and
    metadata (source_filename, page_number).
    """
    embedding_model = _get_embedding_model()
    query_vector = embedding_model.embed_query(query)

    supabase = get_supabase_client()

    # Call the Supabase RPC function for similarity search
    result = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_vector,
            "match_count": match_count,
        },
    ).execute()

    documents: list[Document] = []
    for row in result.data or []:
        documents.append(
            Document(
                page_content=row.get("content", ""),
                metadata={
                    "source_filename": row.get("source_filename", "unknown"),
                    "page_number": row.get("page_number"),
                },
            )
        )

    return documents


# ---------------------------------------------------------------------------
# Step 2: Synthesise answer via GPT-4o
# ---------------------------------------------------------------------------
def generate_response(query: str) -> dict:
    """
    Full RAG pipeline:
      1. Retrieve the most relevant legal chunks from Supabase.
      2. Send them alongside the user query to GPT-4o.
      3. Return the synthesised answer plus source citations.
    """
    # --- Retrieval (Supabase / pgvector) ---
    chunks = retrieve_relevant_chunks(query)

    if not chunks:
        return {
            "answer": (
                "I don't have enough information in the available documents "
                "to answer this question."
            ),
            "sources": [],
        }

    # Build context string from retrieved chunks
    context_parts: list[str] = []
    sources: list[dict] = []
    for i, doc in enumerate(chunks, 1):
        source_info = doc.metadata.get("source_filename", "unknown")
        page = doc.metadata.get("page_number", "N/A")
        context_parts.append(
            f"[Chunk {i} | Source: {source_info}, Page: {page}]\n{doc.page_content}"
        )
        sources.append({"source_filename": source_info, "page_number": page})

    context = "\n\n".join(context_parts)

    # --- Synthesis (GPT-4o) ---
    llm = _get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", LEGAL_SYSTEM_PROMPT),
            ("human", "{question}"),
        ]
    )
    chain = prompt | llm
    ai_message = chain.invoke({"context": context, "question": query})

    return {
        "answer": ai_message.content,
        "sources": sources,
    }
