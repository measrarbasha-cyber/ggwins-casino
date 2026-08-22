with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# Let's find search elements in index.html
import re
searches = [m.start() for m in re.finditer(r'search|filter', idx, re.I)]
for m in searches:
    print(idx[m-40:m+120].encode('ascii', errors='replace').decode('ascii'))
    print("="*40)