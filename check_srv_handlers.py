srv_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py"
with open(srv_path, "r", encoding="utf-8") as f:
    s = f.read()

import re
endpoints = re.findall(r'def handle_[a-zA-Z0-9_]+', s)
print("Server API Handlers:", endpoints)