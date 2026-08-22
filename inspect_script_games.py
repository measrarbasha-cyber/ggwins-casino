with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

import re
games_arr = re.search(r'const GAMES\s*=\s*\[(.*?)\];', s, re.DOTALL)
if games_arr:
    print(games_arr.group(0)[:1500].encode('ascii', errors='replace').decode('ascii'))

render_games = re.search(r'function renderGames\(.*?\n\}', s, re.DOTALL)
if render_games:
    print("RENDER GAMES FUNCTION:")
    print(render_games.group(0)[:1500].encode('ascii', errors='replace').decode('ascii'))