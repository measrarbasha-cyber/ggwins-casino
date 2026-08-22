with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

import re
games_sec = re.search(r'<section[^>]*id="games-section"[^>]*>.*?</section>', idx, re.DOTALL)
if games_sec:
    print(games_sec.group(0)[:1200].encode('ascii', errors='replace').decode('ascii'))
else:
    print("games-section not found directly by regex")