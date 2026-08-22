with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

start = idx.find('id="auth-modal"')
end = idx.find('<!-- END AUTH MODAL -->', start)
if end == -1:
    end = idx.find('</div>\n  </div>', start)
print(idx[start:start+2500].encode('ascii', errors='replace').decode('ascii'))