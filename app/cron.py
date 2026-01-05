from fastapi import FastAPI
from app.insert import insert_abyss_team, insert_character_mapping, insert_version
from app.wrapper import YSHelperWrapper

app = FastAPI()

@app.get("/api/cron/abyss")
async def update_abyss_teams():
  print("Updating Abyss Teams!")
  
  wrapper = YSHelperWrapper()
  characters = wrapper.get_character_list()
  for character in characters:
      teams = await wrapper.get_teams(role = character)
      for team in teams:
          insert_abyss_team(team)

  return {"message": "Cron job executed successfully"}

@app.get("/api/cron/version")
async def update_versions():
  print("Updating Versions Table")
  
  wrapper = YSHelperWrapper()
  mapping = await wrapper.extract_versions()
  
  for version, version_number in mapping.items():
    insert_version(version, version_number)
  return {"message": "Cron job executed successfully"}

  
@app.get("/api/cron/map")
async def update_character_mapping():
  print("Updating Character Mapping!")
  
  wrapper = YSHelperWrapper()
  mapping = await wrapper.extract_dict()
    
  for url, character_name in mapping.items():
    insert_character_mapping(url, character_name)
  
  return {"message": "Cron job executed successfully"}
