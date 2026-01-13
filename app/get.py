from app.db import supabase


def get_teams_from_character(character_name: str, version: int, num_teams: int):
    res = (
        supabase.rpc(
            "get_teams_by_character",
            {"p_character_name": character_name, "p_version_number": version},
        )
        .limit(num_teams)
        .execute()
    )

    return res.data


def get_teams_from_character_set(
    character_names: list[str], version: int, num_teams: int
):
    res = (
        supabase.rpc(
            "get_teams_with_characters_subset",
            {"p_character_names": character_names, "p_version_number": version},
        )
        .limit(num_teams)
        .execute()
    )

    return res.data


def get_abyss_teams():
    res = supabase.table("top_100_abyss_teams").select("*").execute()

    return res.data


def get_character_mapping_dict() -> dict[str, str]:
    mapping = {}
    for row in get_character_mapping():
        mapping[row["url"]] = row["character_name"]

    return mapping


def get_character_mapping():
    res = supabase.table("url_to_character_mapping").select("*").execute()
    return res.data


def get_all_versions(desc=True):
    res = (
        supabase.table("versions")
        .select("*")
        .order("version_number", desc=desc)
        .execute()
    )

    return res.data
