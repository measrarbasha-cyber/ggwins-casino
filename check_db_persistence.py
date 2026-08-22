# Verify database.json and server.py backend persistence handlers
import json, os

db_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\data\database.json"
if os.path.exists(db_path):
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    print("Database Keys:", list(db.keys()))
    print("Total Users in DB:", len(db.get("users", [])))
    print("Sample Users:", [u.get("username") for u in db.get("users", [])])
else:
    print("DB file does not exist yet at", db_path)