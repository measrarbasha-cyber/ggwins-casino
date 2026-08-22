with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# Let's inspect sidebar and navigation in index.html
start = idx.find('<aside')
end = idx.find('</aside>')
if start != -1 and end != -1:
    print("SIDEBAR:")
    print(idx[start:end+8][:1500].encode('ascii', errors='replace').decode('ascii'))

# Let's inspect topbar
start = idx.find('<header')
end = idx.find('</header>')
if start != -1 and end != -1:
    print("HEADER:")
    print(idx[start:end+9][:1500].encode('ascii', errors='replace').decode('ascii'))