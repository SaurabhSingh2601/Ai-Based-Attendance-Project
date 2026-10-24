import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase_url = (os.getenv("SUPABASE_URL") or "").strip().strip('"').strip("'")
supabase_key = (os.getenv("SUPABASE_KEY") or "").strip().strip('"').strip("'")

is_configured = bool(supabase_url and supabase_key and "placeholder" not in supabase_url)

if not is_configured:
    print("WARNING: SUPABASE_URL or SUPABASE_KEY is missing from environment variables!")

supabase: Client = create_client(
    supabase_url if is_configured else "https://placeholder.supabase.co",
    supabase_key if is_configured else "placeholder_key"
)
