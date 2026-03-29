# ⚖️ Legal Team Assistant (AI-Powered RAG)

**Intelligent Document Analysis & Semantic Search for Legal Professionals**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C?logo=langchain&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-pgvector-3ECF8E?logo=supabase&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?logo=openai&logoColor=white)

---

## 📖 Overview

The **Legal Team Assistant** is a production-ready **Retrieval-Augmented Generation (RAG)** pipeline designed to ingest complex legal documents (PDFs / Word) and provide highly accurate, context-aware answers. Built with scalability and security in mind, it features custom chunking logic to preserve legal clauses and guarantees **source attribution for every AI response**.

---

## ✨ Core Features

- 📄 **Multi-Format Ingestion:** Specialized parsers for `.pdf` and `.docx` legal contracts with automatic metadata enrichment (`source_filename`, `page_number`).
- 🧠 **Context-Aware Chunking:** Recursive character splitting (1000 chars / 200 overlap) optimized for legal statutes, preserving complete clauses without cutting off crucial meaning.
- ⚡ **Vector Search:** Integrated with **Supabase (pgvector)** for lightning-fast semantic retrieval via a custom `match_documents` RPC function.
- 🤖 **GPT-4o Synthesis:** Retrieved chunks are sent to OpenAI GPT-4o (`temperature=0`) which generates clean, professional legal summaries with full source citations.
- 🎯 **Zero Hallucination Guardrails:** Strict system prompts force the AI to rely **only** on retrieved context. Every answer includes exact metadata tracking (Filename & Page Number). If the answer isn't in the database, the system safely replies *"I don't have enough information."*
- 🛡️ **Production Security:** Rate limiting (5 req/min via SlowAPI), strict Pydantic input validation (max 1000 chars), and secure environment variable isolation for all API keys.

---

## 🏗️ Project Structure

```
Legal-Team-Assistant/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Dependency management
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── Prd.md                     # Product Requirements Document
├── progress.txt               # Development progress log
│
├── services/                  # Core business logic modules
│   ├── __init__.py            # Package marker
│   ├── pdf_loader.py          # PDF ingestion (PyMuPDFLoader)
│   ├── docx_loader.py         # DOCX ingestion (Docx2txtLoader)
│   ├── router.py              # File-type routing dispatcher
│   ├── splitter.py            # Legal-text chunking logic
│   ├── chunking.py            # Ingestion pipeline orchestrator
│   ├── embeddings.py          # OpenAI embedding model setup
│   ├── vector_store.py        # Supabase client initialisation
│   └── llm.py                 # RAG pipeline (retrieval + GPT-4o synthesis)
│
├── frontend/                  # HTML/CSS dashboard
│   ├── main_dashboard.html    # Landing page
│   ├── case_details.html      # Case detail view
│   ├── documents_list.html    # Document management
│   ├── research_dashboard.html# Legal research interface
│   └── settings_page.html     # Application settings
│
└── tests/
    ├── test_query.py           # /query endpoint validation
    ├── test_upload.py          # /upload endpoint validation
    ├── test_embedding.py       # Embedding vector dimension check
    ├── test_vector_store.py    # Supabase connectivity check
    ├── test_rate_limit.py      # Rate limiting & input validation
    └── check_env.py            # Environment diagnostic utility
```

---

## 🧠 System Architecture: How It Works

This is the exact sequence of operations for the Legal Assistant's RAG system.

### Step 1: Cloud Retrieval (Supabase)

The system performs a **real similarity search** using pgvector and the `text-embedding-3-small` model.

- When a legal query is submitted (e.g., *"What is the penalty for early contract termination?"*), it is converted into a mathematical vector via OpenAI's `text-embedding-3-small` model.
- The system calls a custom Supabase RPC function (`match_documents`) to find the most relevant legal context in milliseconds.
- Supabase (pgvector) performs a rapid similarity search across all embedded legal document chunks and returns the top matches with their `source_filename` and `page_number` metadata.

### Step 2: Expert Synthesis (GPT-4o)

The "Brain" (GPT-4o) receives the real retrieved chunks and generates a structured `{answer, sources}` response.

- **Reading Comprehension:** GPT-4o reads the dense, complex legal paragraphs that Supabase found.
- **Contextual Reasoning:** It determines how each specific paragraph addresses the user's question.
- **Structured Response:** Instead of returning raw text, GPT-4o generates a clean, professional, human-readable summary.
- **Source Attribution:** It includes precise `source_filename` and `page_number` metadata for every claim, ensuring full accountability.

### Step 3: Zero Hallucination Guardrails

By setting the model temperature to `0`, the system ensures the most **deterministic and reliable** answers possible.

- The system prompt strictly enforces that if the answer isn't in the Supabase chunks, the agent **will not guess**.
- GPT-4o responds with *"I don't have enough information in the available documents to answer this question"* rather than fabricating statutes, case names, or legal definitions.
- Every answer is grounded exclusively in the retrieved context — **no external knowledge is used**.

---

## 🔌 API Endpoints

| Method | Path | Description | Rate Limit |
|--------|------|-------------|------------|
| `GET` | `/` | API information | — |
| `GET` | `/health` | Health check | — |
| `POST` | `/upload` | Ingest a legal document (PDF/DOCX) | 5/min |
| `POST` | `/query` | Ask a legal question (RAG pipeline) | 5/min |
| `GET` | `/docs` | Interactive Swagger UI | — |

### Example Response (`POST /query`)

```json
{
  "status": "success",
  "query": "What is the penalty for early contract termination?",
  "answer": "According to Section 73 of the Indian Contract Act, 1872...",
  "sources": [
    { "source_filename": "contract_act.pdf", "page_number": 42 },
    { "source_filename": "contract_act.pdf", "page_number": 43 }
  ]
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.11+ |
| **Framework** | FastAPI |
| **Orchestration** | LangChain |
| **Vector Database** | Supabase (pgvector) |
| **Embeddings** | OpenAI `text-embedding-3-small` (1536 dimensions) |
| **LLM** | OpenAI GPT-4o (`temperature=0`) |
| **Rate Limiting** | SlowAPI |
| **Document Parsing** | PyMuPDF, docx2txt |

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/your-username/legal-team-assistant.git
cd legal-team-assistant

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env          # Windows
# cp .env.example .env          # macOS / Linux
# Then edit .env with your real API keys

# 5. Start the server
uvicorn main:app --reload

# 6. Open the interactive docs
# http://127.0.0.1:8000/docs
```

### Environment Variables

```env
OPENAI_API_KEY=sk-proj-...             # OpenAI API key (GPT-4o + embeddings)
SUPABASE_URL=https://xxx.supabase.co   # Your Supabase project URL
SUPABASE_KEY=your-service-key-here     # Supabase service role key
```

---

## 📄 License

This project is for educational and portfolio purposes.
