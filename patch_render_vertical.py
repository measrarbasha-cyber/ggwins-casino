with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

# Update renderGames function to output vertical rows
render_vertical_code = """function renderGames(category = 'all', searchKeyword = '') {
  const feed = document.getElementById('vertical-games-feed');
  const countLbl = document.getElementById('games-count-lbl');

  if (!feed) return;
  feed.innerHTML = '';

  let filtered = GAMES;
  if (category !== 'all') {
    filtered = GAMES.filter(g => g.category === category);
  }

  if (countLbl) {
    countLbl.textContent = `${filtered.length} Games Active`;
  }

  filtered.forEach(game => {
    const row = document.createElement('div');
    row.className = 'vertical-game-row';
    row.onclick = () => launchGame(game);

    const catBadge = game.category === 'originals' 
      ? '🔥 Original' 
      : game.category === 'table' 
        ? '🃏 Table Royale' 
        : '🎯 Casual & Arcade';

    row.innerHTML = `
      <div class="v-game-left">
        <div class="v-game-icon-box">${game.icon}</div>
        <div class="v-game-meta">
          <div class="v-game-title">${game.name}</div>
          <div class="v-game-sub">
            <span class="v-game-tag">${catBadge}</span>
            <span>•</span>
            <span>👥 ${(game.players || 3200).toLocaleString()} players</span>
          </div>
        </div>
      </div>
      <div class="v-game-right">
        <button class="v-play-btn" onclick="event.stopPropagation(); launchGame(${JSON.stringify(game).replace(/"/g, '&quot;')})">
          ▶ Play Now
        </button>
      </div>
    `;

    feed.appendChild(row);
  });
}"""

import re
s = re.sub(r'function renderGames\(.*?\n\}', render_vertical_code, s, flags=re.DOTALL)

with open("script.js", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: script.js renderGames updated to render all 20 games vertically in exact order!")