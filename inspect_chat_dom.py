with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# Let's find chat container in index.html
start = idx.find('id="chat-sidebar"')
if start == -1:
    start = idx.find('class="chat-')
if start != -1:
    print(idx[start:start+1200].encode('ascii', errors='replace').decode('ascii'))