with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

idx = s.find("tabLogin")
if idx != -1:
    print(s[idx:idx+2500].encode('ascii', errors='replace').decode('ascii'))