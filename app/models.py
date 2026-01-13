from pydantic import BaseModel
from typing import List


class Character(BaseModel):
    name: str
    rarity: int | None = None
    icon: str | None = None


class AbyssTeam(BaseModel):
    version_number: int
    members: List[Character]
    usage_rate_top: float | None = None
    usage_rate_bottom: float | None = None
    usage_total: float | None = None
    team_key: str | None = None


class AbyssSetRequest(BaseModel):
    character_names: list[str] = []
    version: int = 53
    num_teams: int = 100


class AbyssIncludesRequest(BaseModel):
    character_name: str = ""
    version: int = 53
    num_teams: int = 100
