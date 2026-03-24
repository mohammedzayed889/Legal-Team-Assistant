import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# Ensure environment variables are loaded
load_dotenv()

def get_embedding_model() -> OpenAIEmbeddings:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")
    return OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
