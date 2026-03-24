import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Ensure environment variables are loaded
load_dotenv()


def get_supabase_client() -> Client:
    """Initialize and return a Supabase client for vector store operations."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")

    if not url:
        raise ValueError("SUPABASE_URL is not set in the environment.")
    if not key:
        raise ValueError(
            "SUPABASE_SERVICE_KEY (or SUPABASE_KEY) is not set in the environment."
        )

    return create_client(url, key)
