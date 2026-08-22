import json
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\data\database.json", "r", encoding="utf-8") as f:
    db = json.load(f)
users = [u["username"] for u in db.get("users", [])]
print("Verified Users in DB:", users)