"""
Document Router
Routes incoming files to the appropriate loader based on file extension.
"""

from pathlib import Path
from langchain_core.documents import Document

from services.pdf_loader import load_pdf
from services.docx_loader import load_docx

# Supported file extensions mapped to their loader functions
SUPPORTED_EXTENSIONS: dict[str, callable] = {
    ".pdf": load_pdf,
    ".docx": load_docx,
}


def route_document(file_path: str) -> list[Document]:
    """
    Route a document to the correct loader based on its file extension.

    Args:
        file_path: Absolute or relative path to the document.

    Returns:
        A list of LangChain Document objects produced by the appropriate loader.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not supported.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(SUPPORTED_EXTENSIONS.keys())
        raise ValueError(
            f"Unsupported file format: '{extension}'. "
            f"Supported formats: {supported}"
        )

    loader_fn = SUPPORTED_EXTENSIONS[extension]
    return loader_fn(file_path)
