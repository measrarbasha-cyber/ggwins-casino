with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# Let's inspect sidebar in index.html
start = idx.find('<aside class="sidebar"')
end = idx.find('</aside>')
print(idx[start:end+8].encode('ascii', errors='replace').decode('ascii'))