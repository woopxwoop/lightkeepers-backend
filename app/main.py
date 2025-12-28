from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Character, AbyssTeam
from app.wrapper import YSHelperWrapper
from app.get import get_abyss_teams

app = FastAPI(
  title="Genshin Team Recommender Wrapper",
  version="0.1.0",
  description="Backend wrapper normalizing YSHelper data"
)

origins = [
  "https://woopxwoop.github.io/portfolio/",
  "http://localhost",
  "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # List of allowed origins
    allow_credentials=True,         # Allow cookies to be included in cross-origin requests
    allow_methods=["*"],            # Allow all standard methods (GET, POST, PUT, etc.)
    allow_headers=["*"],            # Allow all headers
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

