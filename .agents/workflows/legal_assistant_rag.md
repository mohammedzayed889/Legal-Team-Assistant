---
description: Legal Assistant RAG Pipeline Workflow
---
# Legal Assistant RAG Pipeline

This workflow outlines the exact sequence of operations for the Legal Assistant's Retrieval-Augmented Generation (RAG) system.

## Step 1: Cloud Retrieval (Supabase)
The system performs a real similarity search using pgvector and the `text-embedding-3-small` model.

- When a legal query is submitted, it is embedded into a vector via OpenAI's `text-embedding-3-small` model.
- It calls a custom Supabase RPC function (`match_documents`) to find the most relevant legal context in milliseconds.
- Supabase (pgvector) performs a rapid similarity search across all embedded legal document chunks and returns the top matches with their `source_filename` and `page_number` metadata.

## Step 2: Expert Synthesis (GPT-4o)
The "Brain" (GPT-4o) now receives the real retrieved chunks and generates a structured `{answer, sources}` response.

- **Reading Comprehension:** GPT-4o reads the dense, complex legal paragraphs that Supabase found.
- **Contextual Reasoning:** It determines how each specific paragraph addresses the user's question.
- **Structured Response:** Instead of returning raw text, GPT-4o generates a clean, professional, human-readable summary.
- **Source Attribution:** It includes precise `source_filename` and `page_number` metadata for every claim, ensuring full accountability.

## Step 3: Zero Hallucination Guardrails
By setting the model temperature to `0`, the system ensures the most deterministic and reliable answers possible.

- The system prompt strictly enforces that if the answer isn't in the Supabase chunks, the agent will not guess.
- GPT-4o is instructed to respond with "I don't have enough information in the available documents to answer this question" rather than fabricating statutes, case names, penalties, or legal definitions.
- Every answer is grounded exclusively in the retrieved context — no external knowledge is used.
