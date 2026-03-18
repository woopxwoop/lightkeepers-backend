from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.cron import (
    update_versions,
    update_teams,
    update_teams_stygian,
    update_abyss_views,
    update_stygian_views,
    update_characters_abyss,
    update_characters_stygian,
)
from app.models import AbyssSetRequest, AbyssIncludesRequest
from app.dependencies import yswrapper
from app.get import (
    get_teams_from_character,
    get_teams_from_character_set,
    get_character_mapping,
    get_all_versions,
    get_abyss_teams,
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


@app.get("/api/versions")
async def get_versions():
    return get_all_versions()


@app.get("/api/characters")
async def get_characters():
    return get_character_mapping()


@app.get("/api/abyss/top")
async def get_teams():
    return get_abyss_teams()


@app.post("/api/abyss/including")
def get_teams_including_character(req: AbyssIncludesRequest = AbyssIncludesRequest()):
    """Gets the most used teams given a character name where all teams includes the given character name.

    Args:
        req (AbyssSetRequest, optional): A model including a character name, a version number, and an upper bound on the number of teams returned.

    Returns:
        data: a JSON object of the list of teams
    """
    teams = get_teams_from_character(
        req.character_name,
        req.version,
        req.num_teams,
    )

    return teams


@app.post("/api/abyss/set")
async def get_teams_only_including_characters(req: AbyssSetRequest = AbyssSetRequest()):
    """Gets the most used teams given a set of characters where all team compositions are a subset of the set of characters.

    Args:
        req (AbyssSetRequest, optional): A model including a list representing the set  of character names, a version number, and an upper bound on the number of teams returned.

    Returns:
        data: a JSON object of the list of teams
    """

    character_names = req.character_names
    version = req.version
    num_teams = req.num_teams

    # if character_names is empty then use all characters
    if not character_names:
        character_names = list(await yswrapper.get_character_list())

    teams = get_teams_from_character_set(character_names, version, num_teams)
    return teams


@app.get("/cron/abyss")
async def cron_jobs_abyss():
    update_versions()
    await update_characters_abyss()
    await update_teams()
    await update_abyss_views()
    return {"status": "ok"}


@app.get("/cron/stygian")
async def cron_jobs_stygian():
    update_versions()
    await update_characters_stygian()
    await update_teams_stygian_job()
    await update_stygian_views()
    return {"status": "ok"}


@app.get("/cron/stygian-version")
async def jobs_stygian():
    await update_versions()
    return {"status": "ok"}


@app.get("/update-teams")
async def update_teams_job():
    await update_teams()


@app.get("/update-teams-stygian")
async def update_teams_stygian_job():
    await update_teams_stygian()


@app.get("/update-abyss-views")
async def update_abyss_views_job():
    await update_abyss_views()


@app.get("/update-stygian-views")
async def update_stygian_views_job():
    await update_stygian_views()


@app.get("/test")
async def test_job():
    await update_characters_stygian()
