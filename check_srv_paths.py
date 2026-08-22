srv_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py"
with open(srv_path, "r", encoding="utf-8") as f:
    s = f.read()

import re
matches = re.findall(r'self\.path\s*==\s*[\'"][^\'"]+[\'"]', s)
print("POST/GET path checks in server.py:")
for m in set(matches):
    print(" ", m)