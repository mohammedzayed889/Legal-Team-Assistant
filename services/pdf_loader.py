"""
PDF Loader Service
Extracts text content and metadata from PDF files using LangChain's PyMuPDFLoader.
"""

from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document


def load_pdf(file_path: str) -> list[Document]:
    """
    Load a PDF file and return a list of LangChain Document objects.

    Each Document contains:
      - page_content: the extracted text from a single page
      - metadata: source filename, page number, and any PDF-level metadata

    Args:
        file_path: Absolute or relative path to the PDF file.

    Returns:
        A list of Document objects, one per page.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a PDF.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {path.suffix}")

    loader = PyMuPDFLoader(str(path))
    documents = loader.load()

    # Enrich metadata with the original filename and standardized page number
    for doc in documents:
        doc.metadata["source_filename"] = path.name
        # PyMuPDF uses 0-indexed 'page' by default
        page = doc.metadata.get("page", 0)
        doc.metadata["page_number"] = page + 1
        # ensure 'source' exists as a fallback
        if "source" not in doc.metadata:
            doc.metadata["source"] = path.name

    return documents
