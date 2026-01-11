from itertools import islice

from app.insert import (
    insert_character_mapping,
    insert_version,
    upsert_multiple_teams,
)

from app.wrapper import YSHelperWrapper


async def update_versions():
    print("Updating Versions Table")

    wrapper = YSHelperWrapper()
    mapping = await wrapper.extract_versions()

    for version, version_number in mapping.items():
        insert_version(version, version_number)
    return {"message": "Cron job executed successfully"}


async def update_character_mapping():
    print("Updating Character Mapping!")

    wrapper = YSHelperWrapper()
    mapping = await wrapper.extract_dict()

    for url, character_name in mapping.items():
        insert_character_mapping(url, character_name)

    return {"message": "Cron job executed successfully"}


def chunked(iterable, size):
    it = iter(iterable)
    while chunk := list(islice(it, size)):
        yield chunk


BATCH_SIZE = 10


async def generate_team_batches(wrapper: YSHelperWrapper):
    seen_team_keys = set()
    batch = []

    characters = await wrapper.get_character_list()

    for character in characters:
        teams = await wrapper.get_teams(role=character)
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
    wrapper = YSHelperWrapper()
    total_processed = 0

    async for i, batch in async_enumerate(generate_team_batches(wrapper), start=1):
        upsert_multiple_teams(batch)
        total_processed += len(batch)
        # print(f"Processed batch {i}, total teams: {total_processed}")

    # print(f"All teams processed: {total_processed}")
