"""
Chunking Service
Wires together the document router and the text splitter so that any
supported file is loaded, split into semantically coherent chunks, and
each chunk inherits the original source metadata.
"""

from langchain_core.documents import Document

from services.router import route_document
from services.splitter import get_legal_text_splitter


def process_and_chunk_document(file_path: str) -> list[Document]:
    """
    Load a document and split it into metadata-enriched chunks.

    Pipeline:
      1. route_document(file_path)  → raw Document list (via PDF / DOCX loader)
      2. get_legal_text_splitter()  → configured splitter
      3. splitter.split_documents() → chunked Document list with metadata intact

    Args:
        file_path: Path to a supported document (.pdf or .docx).

    Returns:
        A list of chunked Document objects.  Every chunk carries the
        original metadata (source, source_filename, page number, etc.).

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is unsupported.
    """
    # Step 1 — load raw documents via the appropriate loader
    raw_documents = route_document(file_path)

    # Step 2 — get the pre-configured legal text splitter
    splitter = get_legal_text_splitter()

    # Step 3 — split while preserving metadata on every chunk
    chunks = splitter.split_documents(raw_documents)

    return chunks
