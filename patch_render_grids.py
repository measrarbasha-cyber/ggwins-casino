with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

# Restore standard renderGames function that populates originals-grid, table-grid, arcade-grid
standard_render_games = """function renderGames(category = 'all') {
  const origGrid = document.getElementById('originals-grid');
  const tableGrid = document.getElementById('table-grid');
  const arcadeGrid = document.getElementById('arcade-grid');

  if (origGrid) origGrid.innerHTML = '';
  if (tableGrid) tableGrid.innerHTML = '';
  if (arcadeGrid) arcadeGrid.innerHTML = '';

  GAMES.forEach(game => {
    const card = createGameCard(game);
    if (game.category === 'originals' && origGrid) {
      origGrid.appendChild(card);
    } else if (game.category === 'table' && tableGrid) {
      tableGrid.appendChild(card);
    } else if (game.category === 'arcade' && arcadeGrid) {
      arcadeGrid.appendChild(card);
    } else if (origGrid) {
      origGrid.appendChild(card);
    }
  });

  const countLbl = document.getElementById('originals-count-lbl');
  if (countLbl) countLbl.textContent = `${GAMES.filter(g => g.category === 'originals').length} Games`;
}"""

import re
s = re.sub(r'function renderGames\(.*?\n\}', standard_render_games, s, flags=re.DOTALL)

with open("script.js", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: script.js renderGames restored to standard grid populator!")