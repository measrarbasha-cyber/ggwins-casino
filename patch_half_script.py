import os, shutil

scratch_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\script.js"
brain_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\script.js"

with open(scratch_path, "r", encoding="utf-8") as f:
    s = f.read()

half_games_js = """
// ── HALF-PAGE LOBBY GAMES ARENA LOGIC ──
let activeHalfCategory = 'all';

function filterHalfGames(category, btn) {
  activeHalfCategory = category;
  document.querySelectorAll('#game-tabs .tab-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderHalfGames();
}

function renderHalfGames() {
  const container = document.getElementById('half-games-grid');
  if (!container) return;

  let filtered = GAMES;
  if (activeHalfCategory !== 'all') {
    filtered = GAMES.filter(g => g.category === activeHalfCategory);
  }

  container.innerHTML = filtered.map(g => {
    const isHot = g.badge === 'hot';
    const tagText = g.category === 'originals' ? '🔥 Original' : g.category === 'table' ? '🃏 Table' : '🎯 Arcade';
    const playersCount = (g.players || 4200).toLocaleString();

    return `
      <div class="half-game-card" onclick="window.location.href='${g.gameUrl}'">
        <div style="display:flex;align-items:center;gap:10px">
          <div class="h-icon-box">${g.icon}</div>
          <div style="flex:1;min-width:0">
            <div class="h-title">${g.name}</div>
            <div class="h-sub">
              <span>${tagText}</span>
              <span>•</span>
              <span style="color:#ffd700">👥 ${playersCount}</span>
            </div>
          </div>
        </div>
        <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='${g.gameUrl}'">
          ▶ Play Now
        </button>
      </div>
    `;
  }).join('');
}

document.addEventListener('DOMContentLoaded', () => {
  renderHalfGames();
});
renderHalfGames();
"""

if "renderHalfGames" not in s:
    s += "\n" + half_games_js

with open(scratch_path, "w", encoding="utf-8") as f:
    f.write(s)

shutil.copy2(scratch_path, brain_path)
print("SUCCESS: script.js updated with half-page games rendering logic!")