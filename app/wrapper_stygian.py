import httpx
import hashlib
from app.models import StygianTeam, Character
from app.get import get_character_mapping_dict
from typing import List


class YSHelperWrapperStygian:
    BASE_URL = "https://api.lelaer.com/ys/getAbyssRank2.php"

    character_mapping: dict[str, str] = None

    def __init__(self, lang="en"):
        self.lang = lang
        self.version_number = 0

    async def fetch_data(self, star="all", role="all"):
        params = {"star": star, "role": role, "lang": self.lang, "version": ""}

        headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "origin": "https://app.yshelper.com",
            "referer": "https://app.yshelper.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }

        async with httpx.AsyncClient(
            timeout=httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=10.0)
        ) as client:
            response = await client.get(self.BASE_URL, params=params, headers=headers)
            response.raise_for_status()
            return response.json()

    def normalize_team(self, team):
        """Normalize a single team object"""
        normalized_roles = []
        for char in team.get("role", []):
            name = self.character_mapping.get(char["avatar"], "Unknown")
            normalized_roles.append(
                {"name": name, "star": char["star"], "avatar": char["avatar"]}
            )
        return {
            "roles": normalized_roles,
            "use": team.get("use"),
            "use_rate": team.get("use_rate"),
            "has": team.get("has"),
            "has_rate": team.get("has_rate"),
            "attend_rate": team.get("attend_rate"),
            "up_use": team.get("up_use"),
            "mid_use": team.get("mid_use"),
            "down_use": team.get("down_use"),
            "up_use_num": team.get("up_use_num"),
            "mid_use_num": team.get("mid_use_num"),
            "down_use_num": team.get("down_use_num"),
        }

    def generate_team_key(self, members: List[Character]) -> str:
        member_names = [member.name for member in members]
        team_str = "-".join(sorted(member_names))

        return hashlib.sha256(team_str.encode("utf-8")).hexdigest()

    def map_team_to_model(self, team) -> StygianTeam:
        members = [
            Character(
                name=self.character_mapping.get(char["avatar"], "Unknown"),
                rarity=char["star"],
                icon=char["avatar"],
            )
            for char in team.get("role", [])
        ]

        return StygianTeam(
            version_number=self.version_number,
            members=members,
            usage_rate_top=team.get("up_use"),
            usage_rate_middle=team.get("mid_use"),
            usage_rate_bottom=team.get("down_use"),
            usage_total=team.get("use_rate"),
            team_key=self.generate_team_key(members),
        )

    def get_abyss_teams(self, raw_teams) -> List[StygianTeam]:
        return [self.map_team_to_model(team) for team in raw_teams]

    def extract_teams(self, data):
        """
        Given the raw JSON from the API, return only the objects that represent teams.
        We identify them by the presence of the 'role' key.
        """
        teams = []
        for v in data.values():
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, list):
                        for t in item:
                            if "role" in t:
                                teams.append(t)
        return teams

    def get_current_version(self, data) -> int:
        history = data["history_list"]
        recent = history[0]
        return recent["value"]

    async def extract_dict(self) -> dict[str, str]:
        data = await self.fetch_data()

        return dict((c["avatar"], c["name"]) for c in data["has_list"])

    async def extract_versions(self) -> dict[str, int]:
        data = await self.fetch_data()

        return dict((c["title"], int(c["value"])) for c in data["history_list"])

    def normalize_response(self, data) -> List[StygianTeam]:
        """Normalize the full API response"""

        teams = []
        teams_data = self.extract_teams(data)

        for team in teams_data:  # Adjust key if needed
            teams.append(self.normalize_team(team))

        return self.get_abyss_teams(teams_data)

    async def get_teams(self, role="all"):
        """Fetch and normalize in one call"""
        await self.get_mapping_cached()
        raw_data = await self.fetch_data(role=role)

        # self.extract_dict(raw_data)
        self.version_number = self.get_current_version(raw_data)
        return self.normalize_response(raw_data)

    async def get_mapping_cached(self):
        if self.character_mapping is None:
            self.character_mapping = get_character_mapping_dict()

    async def get_character_list(self):
        await self.get_mapping_cached()
        return self.character_mapping.values()

    async def get_characters_object_list(self):
        data = await self.fetch_data()

        return [
            {"name": c["name"], "rarity": c["star"], "icon": c["avatar"]}
            for c in data["has_list"]
        ]
