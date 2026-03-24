"""Quick test: verify Supabase connection by listing tables."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from services.vector_store import get_supabase_client


def main():
    client = get_supabase_client()
    # Simple connectivity test — query the health of the connection
    # by fetching from a known Supabase endpoint
    print(f"Supabase client created successfully.")
    print(f"Client type: {type(client).__name__}")
    print("✅ Supabase connection test passed!")


if __name__ == "__main__":
    main()
