from db import supabase

def test_connection():
  result = supabase.table("abyss_teams").select("*").limit(1).execute()
  print(result)
  
if __name__ == "__main__":
  test_connection()