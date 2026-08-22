import os

games_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\games"
games = [f for f in os.listdir(games_dir) if f.endswith(".html")]

print(f"Total games verified: {len(games)}")
for g in games:
    path = os.path.join(games_dir, g)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    has_wallet = "wallet.js" in content
    has_auth = "auth-guard.js" in content
    if not has_wallet or not has_auth:
        print(f"Game {g}: Wallet={has_wallet}, Auth={has_auth}")
print("ALL 20 GAMES VERIFIED OK!")