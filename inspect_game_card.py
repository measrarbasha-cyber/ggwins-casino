with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

import re
card_fn = re.search(r'function createGameCard\(.*?\n\}', s, re.DOTALL)
if card_fn:
    print(card_fn.group(0)[:1200].encode('ascii', errors='replace').decode('ascii'))