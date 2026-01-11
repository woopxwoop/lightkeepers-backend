from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.cron import (
    update_character_mapping,
    update_versions,
    update_teams,
)
from app.models import Character, AbyssTeam, TeamRequest
from app.wrapper import YSHelperWrapper
from app.get import (
    get_teams_from_character,
    get_teams_from_character_set,
)

app = FastAPI(
    title="Genshin Team Recommender Wrapper",
    version="0.1.0",
    description="Backend wrapper normalizing YSHelper data",
)

origins = [
    "https://woopxwoop.github.io",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be included in cross-origin requests
    allow_methods=["*"],  # Allow all standard methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/characters", response_model=list[Character])
def get_characters():
    data = []
    return data


@app.get("/teams", response_model=list[AbyssTeam])
async def get_teams():
    wrapper = YSHelperWrapper()
    data = await wrapper.get_teams()
    return data


@app.get("/db-test-2")
def get_teams_including_character(
    character_name: str = "", version: int = 53, num_teams: int = 100
):
    data = get_teams_from_character(
        character_name,
        version,
        num_teams,
    )
    return data


@app.get("/db-test-3")
async def get_teams_only_including_characters(req: TeamRequest = TeamRequest()):
    wrapper = YSHelperWrapper()

    character_names = req.character_names
    version = req.version
    num_teams = req.num_teams

    all_characters = list(await wrapper.get_character_list())

    if not character_names:
        character_names = all_characters

    data = get_teams_from_character_set(character_names, version, num_teams)
    return data


@app.get("/cron/daily")
async def cron_jobs():
    await update_versions()
    await update_character_mapping()
    await update_teams()
    return {"status": "ok"}


@app.get("/cron/new")
async def cron_test():
    await update_teams()
    return {"status": "ok"}
