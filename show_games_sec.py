with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

start = idx.find('<section class="section games-section"')
end = idx.find('</section>', start)
print(idx[start:end+10].encode('ascii', errors='replace').decode('ascii'))