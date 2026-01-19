from itertools import islice

from app.insert import (
    insert_character_mapping,
    insert_version,
    upsert_multiple_teams,
)

from app.db import supabase
from app.dependencies import yswrapper
import asyncio
import httpx


async def update_characters():
    print("Updating characters!")

    characters = await yswrapper.get_characters_object_list()
    supabase.rpc(
        "upsert_characters",
        {"p_characters": characters},
    ).execute()


async def update_top_100_abyss_teams():
    print("Updating Top 100 Teams!")

    supabase.rpc("refresh_top_100_abyss_teams").execute()


async def update_versions():
    print("Updating Versions Table!")

    mapping = await yswrapper.extract_versions()

    for version, version_number in mapping.items():
        insert_version(version, version_number)


async def update_character_mapping():
    print("Updating Character Mapping!")

    mapping = await yswrapper.extract_dict()

    for url, character_name in mapping.items():
        insert_character_mapping(url, character_name)


def chunked(iterable, size):
    it = iter(iterable)
    while chunk := list(islice(it, size)):
        yield chunk


BATCH_SIZE = 10


async def generate_team_batches():
    seen_team_keys = set()
    batch = []

    characters = await yswrapper.get_character_list()

    for character in characters:
        teams = await yswrapper.get_teams(role=character)
        await asyncio.sleep(0.3)  # 3–4 req/sec max

        for team in teams:
            if team.team_key in seen_team_keys:
                continue  # skip duplicate team
            seen_team_keys.add(team.team_key)
            batch.append(team)

            if len(batch) >= BATCH_SIZE:
                yield batch
                batch = []

    if batch:  # yield remaining teams
        yield batch


async def async_enumerate(aiterable, start=0):
    idx = start
    async for item in aiterable:
        yield idx, item
        idx += 1


async def update_teams():
    print("Updating teams!")
    total_processed = 0

    async for i, batch in async_enumerate(generate_team_batches(), start=1):
        upsert_multiple_teams(batch)
        total_processed += len(batch)
        print(f"Processed batch {i}, total teams: {total_processed}")

    print(f"All teams processed: {total_processed}")
