with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# Let's check where "Lobby" and chat buttons are in index.html
import re
print("Lobby in index.html:")
for m in re.finditer(r'lobby', idx, re.I):
    print(idx[m.start()-30:m.start()+80].encode('ascii', errors='replace').decode('ascii'))
    print("-" * 30)

print("\nChat in index.html:")
for m in re.finditer(r'chat', idx, re.I):
    print(idx[m.start()-30:m.start()+80].encode('ascii', errors='replace').decode('ascii'))
    print("-" * 30)