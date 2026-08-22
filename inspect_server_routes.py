srv_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py"
with open(srv_path, "r", encoding="utf-8") as f:
    srv = f.read()

import re
matches = [m.start() for m in re.finditer(r'/api/register|/api/login', srv, re.I)]
for m in matches:
    print(srv[m-50:m+1200].encode('ascii', errors='replace').decode('ascii'))
    print("="*40)