import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_query():
    print("Testing /query endpoint...")
    response = client.post("/query", json={"query": "What is the penalty for contract breach?"})
    print("Query Response:", response.status_code, response.json())
    
    assert response.status_code == 200
    assert "penalty for contract breach" in response.json()["response"]
    print("✅ Query test passed!")

if __name__ == "__main__":
    test_query()
