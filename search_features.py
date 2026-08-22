with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

import re
matches = [m.start() for m in re.finditer(r'carousel|chat|modal', s, re.I)]
for m in matches[:6]:
    print(s[m-30:m+120].encode('ascii', errors='replace').decode('ascii'))
    print("="*40)