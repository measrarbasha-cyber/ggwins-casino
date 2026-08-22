with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

idx = s.find("['hero-claim-btn'")
print(s[idx:idx+300].encode('ascii', errors='replace').decode('ascii'))