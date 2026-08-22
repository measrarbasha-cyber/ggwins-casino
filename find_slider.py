with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

import re
matches = [m.start() for m in re.finditer(r'slider|carousel|slide', idx, re.I)]
for m in matches[:5]:
    print(idx[m-50:m+150].encode('ascii', errors='replace').decode('ascii'))
    print("="*40)