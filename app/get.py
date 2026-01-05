from app.db import supabase

def get_abyss_teams(version: str = None):
  query = supabase.table("abyss_teams").select("*")
  
  if version:
    query = query.eq("version", version)
  
  response = query.execute()
  
  if not response.data:
    return "Error fetching data or empty"
  
  return response.data

async def get_character_mapping() -> dict[str, str]:
  response = supabase.table("url_to_character_mapping").select("*").execute()
  
  mapping = {}
  print(response.data)
  for row in response.data:
    mapping[row["url"]] = row["character_name"]
  
  return mapping
  