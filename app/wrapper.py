import httpx
import asyncio
import hashlib
from models import AbyssTeam, Character
from typing import List

class YSHelperWrapper:
    BASE_URL = "https://api.yshelper.com/ys/getAbyssRank.php"
    
    AVATAR_MAP = {
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Lisa.png": "Lisa",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Kaeya.png": "Kaeya",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Ambor.png": "Ambor",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Collei.png": "Collei",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Bennett.png": "Bennett",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Barbara.png": "Barbara",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Xingqiu.png": "Xingqiu",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Noel.png": "Noelle",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Xiangling.png": "Xiangling",        
      "https://inews.gtimg.com/om_bt/Ovpvyje229FxFlHfL7PmR9p5u1Hmgxsietat2EtDr4tpYAA/0": "Kachina",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Candace.png": "Candace",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Faruzan.png": "Faruzan",
      "https://shp.qpic.cn/cfwebcap/0/5810a890003501fe544c51080c85ec17/0": "Lynette",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Yaoyao.png": "Yaoyao",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Sucrose.png": "Sucrose",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Fischl.png": "Fischl",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Diona.png": "Diona",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Rosaria.png": "Rosaria",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Feiyan.png": "Yanfei",
      "https://inews.gtimg.com/om_bt/ODUFcnfghVFbDRCFOk67FwGRkJBF1peCzFANQRczGECZ4AA/0": "Aino",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Shinobu.png": "Kuki Shinobu",       
      "https://inews.gtimg.com/om_bt/OUac2bNDmaSzn9wyh-lMP1q5MF9uatt6yxn7Hu4T9QihcAA/0": "Sethos",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Beidou.png": "Beidou",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Dori.png": "Dori",
      "https://inews.gtimg.com/om_bt/Oo-JfOcJOVzrDl0QGzIecgeEiFQLnxBSucZXfOqxFsAfkAA/0": "Ororon",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Sara.png": "Kujou Sara",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Tohma.png": "Thoma",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Layla.png": "Layla",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Chongyun.png": "Chongyun",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Gorou.png": "Gorou",
      "https://inews.gtimg.com/om_bt/OMvF07baGvTcaC75ckHf8EXx5OvTHOt0T4NXzwrTHR-_sAA/0": "Gaming",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Razor.png": "Razor",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Heizo.png": "Shikanoin Heizou",     
      "https://act-webstatic.mihoyo.com/hk4e/e20200928calculate/item_icon_u82ase/09f16853b42c95407e2071af70953556.png": "Kirara",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Ningguang.png": "Ningguang",        
      "https://shp.qpic.cn/cfwebcap/0/33c5bacac6c8686178ef0340f931f989/0": "Chevreuse",
      "https://shp.qpic.cn/cfwebcap/0/1962102b8cc6f48c6b5038eea2c83712/0": "Furina",
      "https://shp.qpic.cn/cfwebcap/0/309409f8c929405a09137fa5c4cb4817/0": "Charlotte",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Tighnari.png": "Tighnari",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Xinyan.png": "Xinyan",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Yunjin.png": "Yun Jin",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Mona.png": "Mona",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Sayu.png": "Sayu",
      "https://inews.gtimg.com/om_bt/OpHMvM_1jlWwxql6zy6ogxZmHxudyxoPcLDB2B0i3RHEoAA/0": "Lan Yan",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Mika.png": "Mika",
      "https://shp.qpic.cn/cfwebcap/0/132e6b32aa5a1a8fd2b40d3dc39d126b/0": "Freminet",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Qin.png": "Jean",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Keqing.png": "Keqing",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Kaveh.png": "Kaveh",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Diluc.png": "Diluc",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Qiqi.png": "Qiqi",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Kazuha.png": "Kaedehara Kazuha",    
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Dehya.png": "Dehya",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Nahida.png": "Nahida",
      "https://inews.gtimg.com/om_bt/OeFYov5btGCz4bWU6OnUjJ_ljINGTS1M6Mzf4zS5SNqvMAA/0": "Iansan",
      "https://inews.gtimg.com/om_bt/O54G_cOnCYOATmTdmY7QXm3KaVQCTGMLEba0ZjTvwpZ5kAA/0": "Ifa",
      "https://inews.gtimg.com/om_bt/O0xvyovTLdAZItFU05s46ZJPMs59oPP-qLjiRaUbhUIs8AA/0": "Xilonen",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Zhongli.png": "Zhongli",
      "https://inews.gtimg.com/om_bt/OUqLJ9qw6zNXkdmllEoXQHAsCiuELytbSHWjANDJgZohcAA/0": "Dahlia",
      "https://inews.gtimg.com/om_bt/OaLzqQy89YeG64YptvdxJq1JjacCICjF0IUloiadJsXYgAA/0": "Yumemizuki Mizuki",
      "https://inews.gtimg.com/om_bt/Om32feaSpkBDl7_cbtSwaUn1BQZMaXrd4PmZFJiaepD2EAA/0": "Citlali",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Shougun.png": "Raiden Shogun",      
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Yelan.png": "Yelan",
      "https://shp.qpic.cn/cfwebcap/0/05ed42b3eaca863eddc188f76cf47549/0": "Neuvillette",
      "https://inews.gtimg.com/om_bt/Oqp4fgRseMUZ93xE-RoEUZBh-Z1lmg-sHby9q2wwuHY44AA/0": "Mavuika",
      "https://inews.gtimg.com/om_bt/OQYIX8ioLWvHu6LRn2EMhDxJ9UxSPtD76lGBjenxNSPZoAA/0": "Skirk",
      "https://inews.gtimg.com/om_bt/Opsi8112vmUVw1fW-s-fxJFEGLHoUBlJ9z0W1TNCG1spwAA/0": "Jahoda",
      "https://inews.gtimg.com/om_bt/OPy-ASsY4HwfFbTHSpwfZDDPy6TBBhAWW6JDKgjTEmKdgAA/0": "Arlecchino",
      "https://inews.gtimg.com/om_bt/OiRpjcVFlBJYQKzvWaSG3ZIklzSgpAnuAb9E3ZwhJJxw8AA/0": "Escoffier",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Ayaka.png": "Ayaka",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Venti.png": "Venti",
      "https://inews.gtimg.com/om_bt/OLzL0pLGyTkCxTuBol3XDQrWwKb1VwxRtAqKfhF2ysMpcAA/0": "Xianyun",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Hutao.png": "Hu Tao",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Kokomi.png": "Sangonomiya Kokomi",  
      "https://inews.gtimg.com/om_bt/O6LtewowU5-iYHLllWIwB_RfuFzQ_S9BdxaPyOAKuzBEcAA/0": "Durin",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Yae.png": "Yae Miko",
      "https://shp.qpic.cn/cfwebcap/0/aa806650373512969e333f11baf26fd9/0": "Navia",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Wanderer.png": "Wanderer",
      "https://inews.gtimg.com/om_bt/OO9Q_noY7yM9fZeDboXX5rcd46ukhOz7_Vm2769M-d2KgAA/0": "Lauma",
      "https://inews.gtimg.com/om_bt/OBn-YEIwxlQ1-v1UDv4ANlQcRKqrq1B8LmkP7_bjA1tdsAA/0": "Flins",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Alhatham.png": "Alhaitham",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Ganyu.png": "Ganyu",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Xiao.png": "Xiao",
      "https://inews.gtimg.com/om_bt/OMig7VJyrmCsh_yOGj5-x8ZpGze8LKqMf6kzvmBngzmIcAA/0": "Chasca",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Shenhe.png": "Shenhe",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Yoimiya.png": "Yoimiya",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Nilou.png": "Nilou",
      "https://inews.gtimg.com/om_bt/OZBabi2uXPQ10bwzQ6OP9abQ0YQvcyaSmMYn4UWERmFooAA/0": "Nefer",
      "https://inews.gtimg.com/om_bt/O8IKvb-_pmcbS38PnbE6lwE6ni1nWSDiBgGCuvTFweqYQAA/0": "Ineffa",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Tartaglia.png": "Tartaglia",        
      "https://inews.gtimg.com/om_bt/OTaCuAiOHfU1pQ_P-aoupanHzSI6jRblBy7WgLtrrZm5oAA/0": "Kinich",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Baizhuer.png": "Baizhu",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Aloy.png": "Aloy",
      "https://inews.gtimg.com/om_bt/Oo2txeBxQJAgE6ppkASf0SVWkgwUgmkDxIWmFFBHxjKzEAA/0": "Clorinde",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Ayato.png": "Kamisato Ayato",       
      "https://inews.gtimg.com/om_bt/O1lOQWrxFgrmK2PY-xRlCdrg_17q1L9tZ49UIVH3v4zxoAA/0": "Mualani",
      "https://inews.gtimg.com/om_bt/OsOlZq27XIAFpw27OonFsrQGCKptezUAZjX_LKJHXxTjsAA/0": "Varesa",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Klee.png": "Klee",
      "https://shp.qpic.cn/cfwebcap/0/f7096c524a2dccebae05034b6e53c95c/0": "Wriothesley",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Cyno.png": "Cyno",
      "https://inews.gtimg.com/om_bt/O4brjwyf7EhF8vtbHE7SkMsd_iNSclIfSA3bVBM0sMHMQAA/0": "Emilie",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Eula.png": "Eula",
      "https://shp.qpic.cn/cfwebcap/0/1fbb825b87056ef0f5b6e88d810bbbde/0": "Lyney",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Itto.png": "Arataki Itto",
      "https://inews.gtimg.com/om_bt/OnZ-ukxBnAOFHN0JIgi3JgOIela3BuBhIFUYZ655b5isAAA/0": "Sigewinne",
      "https://upload-bbs.mihoyo.com/game_record/genshin/character_icon/UI_AvatarIcon_Albedo.png": "Albedo",
      "https://inews.gtimg.com/om_bt/OWLdJcMIIecD4D86Uy5s96yjjduxk1tjOIqjJxTsv7WjUAA/0": "Chiori"
    }

    def __init__(self, lang="en"):
        self.lang = lang
        self.version = ""

    async def fetch_data(self, star="all", role="all"):
        params = {
            "star": star,
            "role": role,
            "lang": self.lang,
            "version": ""
        }

        headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "origin": "https://app.yshelper.com",
            "referer": "https://app.yshelper.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
          
    def normalize_team(self, team) -> AbyssTeam:
        """Normalize a single team object"""
        normalized_roles = []
        for char in team.get("role", []):
            name = self.AVATAR_MAP.get(char["avatar"], "Unknown")
            normalized_roles.append({
                "name": name,
                "star": char["star"],
                "avatar": char["avatar"]
            })
        return {
            "roles": normalized_roles,
            "use": team.get("use"),
            "use_rate": team.get("use_rate"),
            "has": team.get("has"),
            "has_rate": team.get("has_rate"),
            "attend_rate": team.get("attend_rate"),
            "up_use": team.get("up_use"),
            "down_use": team.get("down_use"),
            "up_use_num": team.get("up_use_num"),
            "down_use_num": team.get("down_use_num")
        }
        
    def generate_team_key(self, members: List[Character], version: str) -> str:
        member_names = [member.name for member in members]
        team_str = "-".join(sorted(member_names)) + f"-{version}"
        
        return hashlib.sha256(team_str.encode("utf-8")).hexdigest()
        
        
    def map_team_to_model(self, team) -> AbyssTeam:
        members = [Character(name = self.AVATAR_MAP.get(char["avatar"], "Unknown"), rarity = char["star"], icon = char["avatar"]) for char in team.get("role", [])]
        
        return AbyssTeam (
            version=self.version,
            members=members,
            usage_rate_top = team.get("up_use"),
            usage_rate_bottom = team.get("down_use"),
            usage_total = team.get("use_rate"),
            team_key = self.generate_team_key(members, self.version)
        )

    def get_abyss_teams(self, raw_teams) -> List[AbyssTeam]:
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

    def get_current_version(self, data):
        history = data["history_list"]
        recent = history[0]
        return recent["title"]
    
    def extract_dict(self, data):
        for c in data["has_list"]:

          print("\"" + c["avatar"] + "\"" + ": " + "\"" +c["name"] + "\"," )

        
    
    def normalize_response(self, data) -> List[AbyssTeam]:
        """Normalize the full API response"""
        
        teams = []
        teams_data = self.extract_teams(data)
        
        for team in teams_data:  # Adjust key if needed
            teams.append(self.normalize_team(team))
            
        return self.get_abyss_teams(teams_data)
    
    async def get_teams(self):
        """Fetch and normalize in one call"""
        raw_data = await self.fetch_data()
        
        #self.extract_dict(raw_data)
        self.version = self.get_current_version(raw_data)
        return self.normalize_response(raw_data)
      
