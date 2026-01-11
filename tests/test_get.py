from app.db import supabase


def connection():
    result = supabase.table("abyss_teams").select("*").limit(1).execute()
    print(result)
