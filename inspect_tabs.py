with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

start = idx.find('<div class="section-tabs"')
end = idx.find('</div>', start)
print(idx[start:end+6].encode('ascii', errors='replace').decode('ascii'))