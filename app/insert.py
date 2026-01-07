from app.db import supabase
from app.models import AbyssTeam

def insert_abyss_team(team: AbyssTeam):
  payload = team.model_dump()
  
  response = (
    supabase.table("abyss_teams").upsert(payload, on_conflict="team_key").execute()
  )
  
  return response

def insert_character_mapping(url: str, character_name: str):
  response = (
    supabase.table("url_to_character_mapping").upsert({"url": url, "character_name": character_name}).execute()
  )
  
  return response

def insert_version(version: str, version_number: str):
  response = (
    supabase.table("versions").upsert({"version": version, "version_number": version_number}).execute()
  )
  
  return response