from os import getenv
from dotenv import load_dotenv

load_dotenv()

STABLE_TOKEN = getenv("TOKEN")
BETA_TOKEN = getenv("BETA_TOKEN")

SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_KEY = getenv("SUPABASE_KEY")
