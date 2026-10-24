import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    # Helpful error for developers if .env is missing
    print("WARNING: SUPABASE_URL or SUPABASE_KEY is missing from environment variables!")

supabase: Client = create_client(
    supabase_url or "https://placeholder.supabase.co",
    supabase_key or "placeholder_key"
)
