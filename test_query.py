"""Quick test: verify the /query endpoint returns a structured RAG response."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_query():
    print("Testing /query endpoint...")
    response = client.post(
        "/query", json={"query": "What is the penalty for contract breach?"}
    )
    print("Query Response:", response.status_code, response.json())

    data = response.json()
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert data["status"] == "success"
    assert "answer" in data, "Response must contain an 'answer' field"
    assert "sources" in data, "Response must contain a 'sources' field"
    print("✅ Query test passed!")


if __name__ == "__main__":
    test_query()
