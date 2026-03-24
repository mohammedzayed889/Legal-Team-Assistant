import os
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_rate_limit_and_validation():
    print("Testing Rate Limiting (/query)...")
    # Send 6 requests rapidly
    for i in range(6):
        response = client.post("/query", json={"query": f"Test query {i}"})
        print(f"Request {i+1}: {response.status_code}")
    
    assert response.status_code == 429, "The 6th request should be rate limited"
    print("✅ Rate Limiting test passed!")

    print("\nTesting Strict Validation (> 1000 chars)...")
    long_query = "A" * 1001
    response = client.post("/query", json={"query": long_query})
    print(f"Long Query Response: {response.status_code}")
    assert response.status_code == 422, "Query > 1000 chars should be rejected"
    
    print("\nTesting Strict Validation (empty query)...")
    response = client.post("/query", json={"query": "   "})
    print(f"Empty Query Response: {response.status_code}")
    assert response.status_code == 422, "Empty query should be rejected"
    
    print("✅ Strict Validation test passed!")

if __name__ == "__main__":
    test_rate_limit_and_validation()
