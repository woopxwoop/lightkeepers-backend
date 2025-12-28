from fastapi import FastAPI, HTTPException
from app.models import Character, AbyssTeam
from app.wrapper import YSHelperWrapper
from app.get import get_abyss_teams

app = FastAPI(
  title="Genshin Team Recommender Wrapper",
  version="0.1.0",
  description="Backend wrapper normalizing YSHelper data"
)
  
@app.get("/")
def health_check():
  return {"status":"ok"}

@app.get("/characters", response_model=list[Character])
def get_characters():
  data =[]
  return data


@app.get("/teams", response_model=list[AbyssTeam])
async def get_teams():
  wrapper = YSHelperWrapper()
  data = await wrapper.get_teams()
  return data

@app.get("/db-test")
def get_teams_by_version(version: str = None):
  data = get_abyss_teams(version)
  return data

