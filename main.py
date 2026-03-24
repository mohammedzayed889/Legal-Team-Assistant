"""
Legal AI Assistant — Main Application Entry Point
FastAPI server for the Knowledge Base Ingestion Pipeline.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import shutil
from dotenv import load_dotenv

from services.chunking import process_and_chunk_document
from services.llm import generate_response

# Load environment variables from .env file
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Legal AI Assistant",
    description="Knowledge Base Ingestion Pipeline for legal document processing",
    version="0.1.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint to verify the server is running."""
    return {"status": "healthy", "service": "Legal AI Assistant", "version": "0.1.0"}


@app.get("/", tags=["System"])
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": "Legal AI Assistant API",
        "docs": "/docs",
        "health": "/health",
    }


@app.post("/upload", tags=["Ingestion"])
@limiter.limit("5/minute")
async def upload_document(request: Request, file: UploadFile = File(...)):
    """Upload a document, process it, chunk it, and return ingestion status."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")
        
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Check if file is empty
        if os.path.getsize(temp_file_path) == 0:
            raise ValueError("The uploaded file is empty or corrupted.")
            
        # Process and chunk
        chunks = process_and_chunk_document(temp_file_path)
        
        # Clean up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_created": len(chunks)
        }
    except ValueError as e:
        # Clean up on error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        # Catch unexpected document parsing failures from loaders like PyMuPDF
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=422, detail=f"Unprocessable Document: {str(e)}")
    except Exception as e:
        # Clean up on error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

class QueryModel(BaseModel):
    query: str = Field(..., max_length=1000, description="The user's legal query.")

    @field_validator("query")
    @classmethod
    def check_query_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace only.")
        return v

@app.post("/query", tags=["Querying"])
@limiter.limit("5/minute")
async def query_endpoint(request: Request, query_request: QueryModel):
    """Answers a user's legal query using the mock LLM generation service."""
    response = generate_response(query_request.query)
    
    return {
        "status": "success",
        "query": query_request.query,
        "response": response
    }
