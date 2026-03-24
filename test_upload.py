import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    print("Health:", response.status_code, response.json())

def test_upload():
    print("Testing upload with unsupported file...")
    with open("dummy.txt", "w") as f:
        f.write("This is a dummy file.")
    
    with open("dummy.txt", "rb") as f:
        response = client.post("/upload", files={"file": ("dummy.txt", f, "text/plain")})
        
    print("Upload Response:", response.status_code, response.json())
    os.remove("dummy.txt")

if __name__ == "__main__":
    test_health()
    test_upload()
