from fastapi import FastAPI, HTTPException
from models import Character, AbyssTeam
import asyncio
import httpx
import json
from wrapper import YSHelperWrapper

app = FastAPI(
  title="Genshin Team Recommender Wrapper",
  version="0.1.0",
  description="Backend wrapper normalizing YSHelper data"
)
  
@app.get("/health")
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

@app.get("/teams/by-boss/{boss_id}", response_model=list[AbyssTeam])
def get_teams_by_boss(boss_id: str):
  data = []
  filtered = [team for team in data if team.get("boss_id") == boss_id]
  return filtered

