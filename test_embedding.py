"""Quick test: embed a single dummy string and print the vector length."""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.embeddings import get_embedding_model

def main():
    model = get_embedding_model()
    vector = model.embed_query("This is a dummy legal document for testing embeddings.")
    print(f"Vector length: {len(vector)}")
    assert len(vector) == 1536, f"Expected 1536, got {len(vector)}"
    print("✅ Embedding test passed!")

if __name__ == "__main__":
    main()
