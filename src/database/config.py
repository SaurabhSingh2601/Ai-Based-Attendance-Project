import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Real project credentials as built-in fallback so Render works even if env vars were not set
DEFAULT_SUPABASE_URL = "https://gxgqmyxuwjsmyaleboba.supabase.co"
DEFAULT_SUPABASE_KEY = "sb_publishable_NiEiBkGJYlH5IWtGm3BaKg_8YXvyQ_h"

env_url = (os.getenv("SUPABASE_URL") or "").strip().strip('"').strip("'")
env_key = (os.getenv("SUPABASE_KEY") or "").strip().strip('"').strip("'")

supabase_url = env_url if (env_url and "placeholder" not in env_url) else DEFAULT_SUPABASE_URL
supabase_key = env_key if (env_key and "placeholder" not in env_key) else DEFAULT_SUPABASE_KEY

supabase: Client = create_client(supabase_url, supabase_key)
is_configured = True
