games_page_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>🎮 All Games – GG Wins Casino</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script src="security-guard.js"></script>
<style>
:root {
  --bg: #070a13;
  --bg-card: #0f1527;
  --gold: #ffd700;
  --green: #00e676;
  --border: rgba(255, 255, 255, 0.1);
  --border-gold: rgba(255, 215, 0, 0.35);
}

html, body {
  background: radial-gradient(circle at 50% 5%, #18122c 0%, #080914 60%, #030408 100%);
  color: #f8fafc;
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

/* ── TOP NAV BAR ── */
.g-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 28px;
  background: rgba(15, 21, 39, 0.95);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border-gold);
  position: sticky;
  top: 0;
  z-index: 100;
}

.g-brand {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px;
  font-weight: 900;
  color: #ffd700;
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

/* ── FULL WIDTH CONTAINER ── */
.games-full-wrapper {
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  padding: 24px 24px 80px 24px;
  box-sizing: border-box;
}

.g-hero {
  text-align: center;
  margin-bottom: 24px;
}

.g-hero-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(0, 230, 118, 0.15);
  border: 1.5px solid #00e676;
  color: #00e676;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 11.5px;
  font-weight: 900;
  padding: 4px 14px;
  border-radius: 999px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 10px;
  box-shadow: 0 0 15px rgba(0, 230, 118, 0.3);
}

.g-hero h1 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 34px;
  font-weight: 900;
  color: #fff;
  margin: 0 0 8px;
}
.g-hero h1 span {
  background: linear-gradient(135deg, #ffd700, #ff8c00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.g-hero p {
  font-size: 14.5px;
  color: #cbd5e1;
  margin: 0 auto;
}

/* ── CATEGORY FILTER TABS ── */
.g-filter-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 28px;
}

.g-filter-btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1.5px solid rgba(255, 255, 255, 0.12);
  color: #cbd5e1;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 800;
  padding: 9px 18px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.g-filter-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  border-color: #ffd700;
}
.g-filter-btn.active {
  background: linear-gradient(135deg, #ffd700, #ff8c00);
  color: #000;
  border-color: #ffd700;
  box-shadow: 0 0 16px rgba(255, 215, 0, 0.45);
}

/* ── FULL PAGE OCCUPYING GAMES GRID ── */
.g-full-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
  width: 100%;
}

.g-card {
  background: linear-gradient(145deg, #111827, #0d121f);
  border: 1.5px solid var(--border-gold);
  border-radius: 20px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  position: relative;
  overflow: hidden;
}

.g-card:hover {
  transform: translateY(-6px);
  border-color: #ffd700;
  box-shadow: 0 15px 40px rgba(255, 215, 0, 0.35);
}

.g-card-top {
  display: flex;
  align-items: center;
  gap: 14px;
}

.g-icon-box {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: radial-gradient(circle, rgba(255,215,0,0.25) 0%, rgba(15,21,39,0.95) 100%);
  border: 1.5px solid #ffd700;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34px;
  flex-shrink: 0;
  box-shadow: 0 0 16px rgba(255, 215, 0, 0.3);
}

.g-meta-col {
  flex: 1;
  min-width: 0;
}

.g-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 17px;
  font-weight: 900;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 2px;
}

.g-sub {
  font-size: 12px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 6px;
}

.g-badge {
  font-size: 9.5px;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 999px;
  text-transform: uppercase;
}
.g-badge.hot { background: rgba(239, 83, 80, 0.2); color: #ef5350; border: 1px solid #ef5350; }
.g-badge.orig { background: rgba(0, 230, 118, 0.2); color: #00e676; border: 1px solid #00e676; }
.g-badge.table { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #38bdf8; }

.g-card-body {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 10px 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}
.g-stat-lbl { color: #94a3b8; font-weight: 700; }
.g-stat-val { font-family: 'Space Grotesk', sans-serif; font-weight: 800; color: #ffd700; }

.btn-play-game {
  width: 100%;
  background: linear-gradient(135deg, #00e676, #00b0ff);
  color: #000;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 900;
  padding: 12px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  box-shadow: 0 0 16px rgba(0, 230, 118, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.btn-play-game:hover {
  transform: scale(1.02);
  box-shadow: 0 0 24px rgba(0, 230, 118, 0.65);
}
</style>
</head>
<body>

<nav class="g-nav">
  <a href="index.html" class="g-brand">
    <span>🎮</span> GG Wins <span style="color:#00e676">All Games Arena</span>
  </a>
  <div style="display:flex;align-items:center;gap:12px">
    <a href="index.html" style="color:#cbd5e1;text-decoration:none;font-weight:700;font-size:13px;background:rgba(255,255,255,0.08);padding:7px 14px;border-radius:8px">
      ← Main Lobby
    </a>
    <a href="tournaments.html" style="color:#ffd700;text-decoration:none;font-weight:800;font-size:13px;background:rgba(255,215,0,0.15);padding:7px 14px;border-radius:8px;border:1px solid #ffd700">
      🏆 Tournaments
    </a>
    <a href="vip.html" style="color:#ffd700;text-decoration:none;font-weight:800;font-size:13px;background:rgba(255,215,0,0.15);padding:7px 14px;border-radius:8px;border:1px solid #ffd700">
      👑 VIP Club
    </a>
    <a href="#" onclick="if(typeof openWalletModal==='function') openWalletModal('deposit'); return false;" style="color:#00e676;text-decoration:none;font-size:13px;font-weight:800;background:rgba(0,230,118,0.15);padding:7px 14px;border-radius:8px;border:1px solid #00e676">
      💳 Balance: <span id="g-user-balance">₹0.00</span>
    </a>
  </div>
</nav>

<div class="games-full-wrapper">
  <div class="g-hero">
    <div class="g-hero-chip">🎮 20 REAL CASINO GAMES • FULL PAGE OCCUPY</div>
    <h1>Explore All <span>20 Playable Games</span></h1>
    <p>Tap any game icon below to instantly launch and play with Real or Demo INR balances!</p>
  </div>

  <div class="g-filter-bar">
    <button class="g-filter-btn active" onclick="filterCategory('all', this)">🎮 All 20 Games</button>
    <button class="g-filter-btn" onclick="filterCategory('originals', this)">🔥 GG Originals (7)</button>
    <button class="g-filter-btn" onclick="filterCategory('table', this)">🃏 Cards &amp; Table (6)</button>
    <button class="g-filter-btn" onclick="filterCategory('arcade', this)">🎯 Casual &amp; Arcade (7)</button>
  </div>

  <!-- ── FULL PAGE OCCUPYING GAMES GRID ── -->
  <div class="g-full-grid" id="games-full-grid">
    <!-- Generated by JS -->
  </div>
</div>

<script src="wallet.js"></script>
<script>
const ALL_GAMES_INVENTORY = [
  // ── 1. GG ORIGINALS ──
  { id: 'crash', name: 'GG Crash', icon: '🚀', category: 'originals', badge: 'hot', tag: 'Multiplier Derby', players: 5821, url: 'games/crash.html', maxMultiplier: '1000x' },
  { id: 'mines', name: 'GG Mines', icon: '💣', category: 'originals', badge: 'hot', tag: 'Diamond Grid', players: 6420, url: 'games/mines.html', maxMultiplier: '500x' },
  { id: 'limbo', name: 'GG Limbo Rocket', icon: '📈', category: 'originals', badge: 'hot', tag: 'Target Rocket', players: 3984, url: 'games/limbo.html', maxMultiplier: '10000x' },
  { id: 'dragontower', name: 'Dragon Tower', icon: '🐉', category: 'originals', badge: 'hot', tag: 'Tower Climber', players: 5120, url: 'games/dragontower.html', maxMultiplier: '250x' },
  { id: 'diamonds', name: 'GG Diamond Rush', icon: '💎', category: 'originals', badge: 'hot', tag: 'Gem Match', players: 4920, url: 'games/diamonds.html', maxMultiplier: '100x' },
  { id: 'slots', name: 'GG Fortune Slots', icon: '🎰', category: 'originals', badge: 'hot', tag: 'Triple 7s Jackpot', players: 5244, url: 'games/slots.html', maxMultiplier: '5000x' },
  { id: 'plinko', name: 'GG Plinko Drop', icon: '⚽', category: 'originals', badge: 'hot', tag: 'Pegboard Rush', players: 4891, url: 'games/plinko.html', maxMultiplier: '1000x' },

  // ── 2. CARDS & TABLE GAMES ──
  { id: 'rummy', name: 'Indian Rummy 3D', icon: '🃏', category: 'table', badge: 'hot', tag: '13-Card Grand Slam', players: 7450, url: 'games/rummy.html', maxMultiplier: 'Live Table' },
  { id: 'baccarat', name: 'GG Baccarat 3D', icon: '👑', category: 'table', badge: 'table', tag: 'High-Stakes Table', players: 3870, url: 'games/baccarat.html', maxMultiplier: '8x Banker' },
  { id: 'blackjack', name: 'GG Blackjack 21', icon: '♣️', category: 'table', badge: 'hot', tag: '21 Pro League', players: 3980, url: 'games/blackjack.html', maxMultiplier: '3:2 Payout' },
  { id: 'roulette', name: 'GG Roulette Royale', icon: '🔴', category: 'table', badge: 'table', tag: 'European Wheel', players: 4201, url: 'games/roulette.html', maxMultiplier: '36x Straight' },
  { id: 'sicbo', name: 'GG Sic Bo 3-Dice', icon: '🎲', category: 'table', badge: 'table', tag: 'Triple Dice Cup', players: 3240, url: 'games/sicbo.html', maxMultiplier: '180x Triple' },
  { id: 'hilo', name: 'GG Hilo Master', icon: '🃏', category: 'table', badge: 'table', tag: 'Card Prediction', players: 3410, url: 'games/hilo.html', maxMultiplier: '12x Streak' },

  // ── 3. CASUAL & ARCADE GAMES ──
  { id: 'coinflip', name: 'GG Coin Flip 3D', icon: '🪙', category: 'arcade', badge: 'hot', tag: 'Streak Master', players: 4890, url: 'games/coinflip.html', maxMultiplier: '100x Streak' },
  { id: 'penalty', name: 'GG Penalty Shoot', icon: '⚽', category: 'arcade', badge: 'hot', tag: 'Golden Boot', players: 5610, url: 'games/penalty.html', maxMultiplier: '32x Goal' },
  { id: 'cups', name: 'GG Magic Shells', icon: '🪄', category: 'arcade', badge: 'hot', tag: '3-Cup Wizard', players: 6180, url: 'games/cups.html', maxMultiplier: '3x Round' },
  { id: 'ludo', name: 'GG Ludo Champions', icon: '🎲', category: 'arcade', badge: 'hot', tag: '4-Player Clash', players: 6420, url: 'games/ludo.html', maxMultiplier: 'Grand Pot' },
  { id: 'dice', name: 'GG Dice 3D', icon: '🎲', category: 'arcade', badge: 'orig', tag: 'Roll Over/Under', players: 3102, url: 'games/dice.html', maxMultiplier: '99x Win' },
  { id: 'wheel', name: 'Wheel of Fortune', icon: '🎡', category: 'arcade', badge: 'hot', tag: 'Fortune Spin', players: 4120, url: 'games/wheel.html', maxMultiplier: '50x Sector' },
  { id: 'keno', name: 'GG Keno Classic', icon: '🎱', category: 'arcade', badge: 'orig', tag: 'Lucky Numbers', players: 2830, url: 'games/keno.html', maxMultiplier: '1000x Hit' }
];

let activeCat = 'all';

function filterCategory(cat, btn) {
  activeCat = cat;
  document.querySelectorAll('.g-filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderGamesGrid();
}

function renderGamesGrid() {
  const container = document.getElementById('games-full-grid');
  if (!container) return;

  const wallets = typeof getWallets === 'function' ? getWallets() : { real: 0 };
  const userBalEl = document.getElementById('g-user-balance');
  if (userBalEl) userBalEl.textContent = '₹' + (parseFloat(wallets.real)||0).toLocaleString('en-IN', {minimumFractionDigits: 2});

  let filtered = ALL_GAMES_INVENTORY;
  if (activeCat !== 'all') {
    filtered = filtered.filter(g => g.category === activeCat);
  }

  container.innerHTML = filtered.map(g => {
    const badgeClass = g.badge === 'hot' ? 'hot' : g.badge === 'table' ? 'table' : 'orig';
    const badgeText = g.badge === 'hot' ? '🔥 HOT' : g.badge === 'table' ? '🃏 TABLE' : '✓ LIVE';

    return `
      <div class="g-card" onclick="window.location.href='${g.url}'">
        <div class="g-card-top">
          <div class="g-icon-box">${g.icon}</div>
          <div class="g-meta-col">
            <div class="g-title">${g.name}</div>
            <div class="g-sub">
              <span class="g-badge ${badgeClass}">${badgeText}</span>
              <span>•</span>
              <span>${g.tag}</span>
            </div>
          </div>
        </div>

        <div class="g-card-body">
          <div>
            <div class="g-stat-lbl">Active Players</div>
            <div class="g-stat-val">👥 ${g.players.toLocaleString()}</div>
          </div>
          <div style="text-align:right">
            <div class="g-stat-lbl">Max Multiplier</div>
            <div class="g-stat-val" style="color:#00e676">${g.maxMultiplier}</div>
          </div>
        </div>

        <button class="btn-play-game" onclick="event.stopPropagation(); window.location.href='${g.url}'">
          ▶ Play ${g.name} Now
        </button>
      </div>
    `;
  }).join('');
}

renderGamesGrid();
</script>
</body>
</html>
"""

with open("games.html", "w", encoding="utf-8") as f:
    f.write(games_page_html)

print("SUCCESS: games.html built as a full-page occupying games arena with all 20 game icon cards!")