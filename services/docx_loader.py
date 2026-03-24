"""
DOCX Loader Service
Extracts text content from Microsoft Word (.docx) files using LangChain's Docx2txtLoader.
"""

from pathlib import Path
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document


def load_docx(file_path: str) -> list[Document]:
    """
    Load a DOCX file and return a list of LangChain Document objects.

    Each Document contains:
      - page_content: the extracted text from the entire document
      - metadata: source path and enriched source_filename

    Args:
        file_path: Absolute or relative path to the DOCX file.

    Returns:
        A list of Document objects (typically one for the whole document).

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a .docx file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"DOCX file not found: {file_path}")

    if path.suffix.lower() != ".docx":
        raise ValueError(f"Expected a .docx file, got: {path.suffix}")

    loader = Docx2txtLoader(str(path))
    documents = loader.load()

    # Enrich metadata with the original filename
    for doc in documents:
        doc.metadata["source_filename"] = path.name
        doc.metadata["page_number"] = 1  # DOCX usually parsed as one big chunk originally
        if "source" not in doc.metadata:
            doc.metadata["source"] = path.name

    return documents
