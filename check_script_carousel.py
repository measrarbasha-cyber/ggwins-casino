with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

import re
matches = [m.start() for m in re.finditer(r'race-join-btn|tournaments|slide-2', s, re.I)]
for m in matches:
    print(s[m-50:m+150].encode('ascii', errors='replace').decode('ascii'))
    print("="*40)