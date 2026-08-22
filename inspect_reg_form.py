with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

start = idx.find('id="form-register"')
print(idx[start:start+2000].encode('ascii', errors='replace').decode('ascii'))