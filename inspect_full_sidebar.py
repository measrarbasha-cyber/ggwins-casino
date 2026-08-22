with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

start = idx.find('<aside')
end = idx.find('</aside>')
print(idx[start:end+8].encode('ascii', errors='replace').decode('ascii'))