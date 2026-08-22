with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

# Let's inspect the GAMES array in script.js
idx_start = s.find("const GAMES = [")
idx_end = s.find("];", idx_start)
print(s[idx_start:idx_end+2].encode('ascii', errors='replace').decode('ascii'))