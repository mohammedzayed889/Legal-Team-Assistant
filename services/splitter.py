"""
Text Splitter Service
Provides a pre-configured RecursiveCharacterTextSplitter tuned for legal documents.

Split hierarchy: paragraphs (\n\n) → newlines (\n) → sentences (. ) → spaces → characters.
This preserves clause and paragraph boundaries in dense legal texts.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Defaults optimised for Indian legal texts (dense case-law, statutes, rule books)
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200


def get_legal_text_splitter(
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> RecursiveCharacterTextSplitter:
    """
    Return a RecursiveCharacterTextSplitter configured for legal documents.

    The splitter tries to keep paragraphs, sentences, and clauses intact
    by splitting on natural boundaries first, falling back to character-level
    splitting only as a last resort.

    Args:
        chunk_size:    Maximum number of characters per chunk (default 1000).
        chunk_overlap: Overlap between consecutive chunks (default 200).

    Returns:
        A configured RecursiveCharacterTextSplitter instance.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
