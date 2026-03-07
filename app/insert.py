from app.db import supabase
from app.models import AbyssTeam, StygianTeam, Character


def insert_character_mapping(url: str, character_name: str):
    response = (
        supabase.table("url_to_character_mapping")
        .upsert({"url": url, "character_name": character_name})
        .execute()
    )

    return response


def insert_version(version: str, version_number: str):
    response = (
        supabase.table("versions")
        .upsert({"version": version, "version_number": version_number})
        .execute()
    )

    return response


def insert_stygian_version(version: str, version_number: str):
    response = (
        supabase.table("stygian_versions")
        .upsert({"version": version, "version_number": version_number})
        .execute()
    )

    return response


def get_or_create_character(char: Character):
    result = supabase.table("characters").select("id").eq("name", char.name).execute()

    if result.data:
        return result.data[0]["id"]

    payload = char.model_dump()

    insert_res = supabase.table("characters").insert(payload).execute()

    return insert_res.data[0]["id"]


def insert_team_members(team_id, members):
    rows = []
    for member in members:
        char_id = get_or_create_character(member)

        rows.append({"team_id": team_id, "character_id": char_id})

    supabase.table("abyss_team_members").upsert(
        rows, on_conflict="team_id,character_id"
    ).execute()


def insert_team(team_key: str) -> tuple[str, bool]:
    # Check if team already exists
    existing = (
        supabase.table("abyss_teams").select("id").eq("team_key", team_key).execute()
    )

    if existing.data:
        team_id = existing.data[0]["id"]
        is_new = False
    else:
        # Insert new team
        res = supabase.table("abyss_teams").insert({"team_key": team_key}).execute()
        team_id = res.data[0]["id"]
        is_new = True

    return team_id, is_new


def insert_team_stats(
    team_id: str,
    version_number: int,
    usage_top: float,
    usage_bottom: float,
    usage_total: float,
):
    payload = {
        "team_id": team_id,
        "version_number": version_number,
        "usage_rate_top": usage_top,
        "usage_rate_bottom": usage_bottom,
        "usage_total": usage_total,
    }

    supabase.table("team_stats").upsert(
        payload, on_conflict=["team_id", "version_number"]
    ).execute()


def store_abyss_team(team: AbyssTeam):
    team_id, is_new = insert_team(team.team_key)

    if is_new:
        insert_team_members(team_id, team.members)

    insert_team_stats(
        team_id,
        team.version_number,
        team.usage_rate_top,
        team.usage_rate_bottom,
        team.usage_total,
    )


async def upsert_abyss_team(team: AbyssTeam):
    await supabase.rpc(
        "upsert_abyss_team",
        {
            "p_team_key": team.team_key,
            "p_character_names": [c.name for c in team.members],
            "p_version_number": team.version_number,
            "p_usage_rate_top": team.usage_rate_top,
            "p_usage_rate_bottom": team.usage_rate_bottom,
            "p_usage_total": team.usage_total,
        },
    ).execute()


def upsert_multiple_teams(teams: list[AbyssTeam]):
    # Convert teams to JSON array for PostgreSQL
    payload = []
    for team in teams:
        payload.append(
            {
                "team_key": team.team_key,
                "members": [member.name for member in team.members],
                "version_number": team.version_number,
                "usage_rate_top": team.usage_rate_top,
                "usage_rate_bottom": team.usage_rate_bottom,
                "usage_total": team.usage_total,
            }
        )

    supabase.rpc("upsert_abyss_teams_batch", {"p_teams": payload}).execute()


def upsert_multiple_teams_stygian(teams: list[StygianTeam]):
    # Convert teams to JSON array for PostgreSQL
    payload = []
    for team in teams:
        payload.append(
            {
                "team_key": team.team_key,
                "members": [member.name for member in team.members],
                "version_number": team.version_number,
                "usage_rate_top": team.usage_rate_top,
                "usage_rate_middle": team.usage_rate_middle,
                "usage_rate_bottom": team.usage_rate_bottom,
                "usage_total": team.usage_total,
            }
        )

    supabase.rpc("upsert_stygian_teams_batch", {"p_teams": payload}).execute()
