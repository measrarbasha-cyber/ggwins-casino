with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

import re
matches = [m.start() for m in re.finditer(r'login|register|auth|session|signup', s, re.I)]
for m in matches[:10]:
    print(s[m-30:m+120].encode('ascii', errors='replace').decode('ascii'))
    print("="*40)