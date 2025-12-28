from app.db import supabase

def get_abyss_teams(version: str = None):
  query = supabase.table("abyss_teams").select("*")
  
  if version:
    print(version)
    query = query.eq("version", version)
  
  response = query.execute()
  
  if not response.data:
    return "Error fetching data or empty"
  
  return response.data