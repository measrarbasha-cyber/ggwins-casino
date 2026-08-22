with open("games.html", "r", encoding="utf-8") as f:
    g = f.read()

# Update titles to Lobby
g = g.replace("🎮 All Games – GG Wins Casino", "🏠 Game Lobby – GG Wins Casino")
g = g.replace("GG Wins <span style=\"color:#00e676\">All Games Arena</span>", "GG Wins <span style=\"color:#00e676\">Game Lobby</span>")
g = g.replace("Explore All <span>20 Playable Games</span>", "GG Wins <span>Game Lobby (20 Playable Games)</span>")

with open("games.html", "w", encoding="utf-8") as f:
    f.write(g)

print("SUCCESS: games.html renamed and unified as Lobby!")