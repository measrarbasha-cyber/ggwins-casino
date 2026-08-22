with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

start = idx.find('<div class="hero-slider"')
end = idx.find('</section>', start)
print(idx[start:end].encode('ascii', errors='replace').decode('ascii'))