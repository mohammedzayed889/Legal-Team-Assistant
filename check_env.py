from dotenv import load_dotenv
import os
load_dotenv()
url = os.getenv("SUPABASE_URL", "NOT_SET")
key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY", "NOT_SET")
print(f"URL set: {url != 'NOT_SET'}")
print(f"Key set: {key != 'NOT_SET'}")
if url and len(url) > 20:
    print(f"URL starts with: {url[:25]}...")
else:
    print(f"URL: {url}")
