from app.db import supabase
from app.models import AbyssTeam

def insert_abyss_team(team: AbyssTeam):
  payload = team.model_dump()
  
  response = (
    supabase.table("abyss_teams").upsert(payload, on_conflict="team_key").execute()
  )
  
  return response

