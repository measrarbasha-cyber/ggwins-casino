with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

# Replace createGameCard with clean UTF-8 icons and instant click-to-play
new_create_card = """function createGameCard(game) {
  const badgeHtml = game.badge ? `<span class="game-badge badge-${game.badge}">${game.badge === 'jackpot' ? '💰 JACKPOT' : game.badge === 'hot' ? '🔥 HOT' : game.badge.toUpperCase()}</span>` : '';
  const hasGame = !!game.gameUrl;
  const div = document.createElement('div');
  div.className = 'game-card';
  div.dataset.category = game.category;
  div.innerHTML = `
    <div class="game-thumb ${game.grad || 'grad-original-1'}">
      ${badgeHtml}
      <div class="game-thumb-center">
        <span class="game-icon-bg" style="font-size:42px;display:block;margin-bottom:4px;filter:drop-shadow(0 0 10px rgba(255,215,0,0.4))">${game.icon}</span>
        <div class="game-logo-name" style="font-weight:900">${game.name}</div>
      </div>
      <div class="game-overlay">
        <button class="game-play-btn">▶ Play Now</button>
        <button class="game-demo-btn">${hasGame ? '⚡ Live Game' : 'Play Now'}</button>
      </div>
    </div>
    <div class="game-info">
      <div class="game-name" style="display:flex;align-items:center;gap:6px"><span>${game.icon}</span> ${game.name}</div>
      <div class="game-provider">${game.provider} • 👥 ${(game.players||3200).toLocaleString()} playing</div>
    </div>
  `;
  // Click card body = launch game immediately
  div.addEventListener('click', () => launchGame(game));
  // Play Now button
  const playBtn = div.querySelector('.game-play-btn');
  if (playBtn) {
    playBtn.addEventListener('click', e => {
      e.stopPropagation();
      launchGame(game);
    });
  }
  const demoBtn = div.querySelector('.game-demo-btn');
  if (demoBtn) {
    demoBtn.addEventListener('click', e => {
      e.stopPropagation();
      launchGame(game);
    });
  }
  return div;
}"""

import re
s = re.sub(r'function createGameCard\(game\)\s*\{.*?\n\}', new_create_card, s, flags=re.DOTALL)

with open("script.js", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: script.js createGameCard updated with vivid game icons and 1-click launch!")