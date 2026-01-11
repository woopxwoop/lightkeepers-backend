from app.db import supabase


def get_teams_from_character(character_name: str, version: int, num_teams: int):
    response = (
        supabase.rpc(
            "get_teams_by_character",
            {"p_character_name": character_name, "p_version_number": version},
        )
        .limit(num_teams)
        .execute()
    )

    return response


def get_teams_from_character_set(
    character_names: list[str], version: int, num_teams: int
):
    response = (
        supabase.rpc(
            "get_teams_with_characters_subset",
            {"p_character_names": character_names, "p_version_number": version},
        )
        .limit(num_teams)
        .execute()
    )

    return response


def get_abyss_teams(version: str = None):
    query = supabase.table("abyss_teams").select("*")

    if version:
        query = query.eq("version", version)

    response = query.execute()

    if not response.data:
        return "Error fetching data or empty"

    return response.data


async def get_character_mapping() -> dict[str, str]:
    response = supabase.table("url_to_character_mapping").select("*").execute()

    mapping = {}
    for row in response.data:
        mapping[row["url"]] = row["character_name"]

    return mapping
