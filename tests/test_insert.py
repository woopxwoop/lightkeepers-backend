import asyncio
import httpx
import json
import pytest
from app.insert import insert_abyss_team
from app.wrapper import YSHelperWrapper

URL = "https://api.yshelper.com/ys/getAbyssRank.php"

params = {
    "star": "all",
    "role": "all",
    "lang": "en",
    "version": ""
}

# Minimal but safe headers
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Origin": "https://app.yshelper.com",
    "Referer": "https://app.yshelper.com/"
}

def fetch_abyss_rank():
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(URL, params=params, headers=HEADERS)
            response.raise_for_status()
            data = response.json()

            # Pretty-print to inspect structure
            print(json.dumps(data, indent=2, ensure_ascii=False))

            return data

    except httpx.RequestError as e:
        print(f"Request failed: {e}")
    except httpx.HTTPStatusError as e:
        print(f"Bad status code: {e.response.status_code} - {e.response.text}")

@pytest.mark.asyncio
async def insert_characters_abyss():
    wrapper = YSHelperWrapper()
    characters = ["Ambor", "Kaeya"]
    for character in characters:
        teams = await wrapper.get_teams(role = character)
        for team in teams:
            insert_abyss_team(team)


