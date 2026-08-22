with open("tournaments.html", "r", encoding="utf-8") as f:
    t = f.read()

# 1. Replace stats banner with clean 4 boxes: Entry Fee, Prize Pool, Total Wagered, Total Players
clean_stats_banner = """<!-- ── STATS COUNTER BOXES (TOTAL WAGERED & TOTAL PLAYERS DYNAMICALLY UPDATING) ── -->
<div class="t-stats-banner">
  <div class="t-stat-card">
    <div class="t-stat-icon">🎟️</div>
    <div class="t-stat-title">Tournament Entry Fee</div>
    <div class="t-stat-val">₹50.00 / Game</div>
  </div>
  <div class="t-stat-card">
    <div class="t-stat-icon">💰</div>
    <div class="t-stat-title">Total Active Prize Pool</div>
    <div class="t-stat-val">₹4,85,000</div>
  </div>
  <div class="t-stat-card">
    <div class="t-stat-icon">📈</div>
    <div class="t-stat-title">Total Tournament Wagered</div>
    <div class="t-stat-val" id="live-total-wagered">₹28,45,200</div>
  </div>
  <div class="t-stat-card">
    <div class="t-stat-icon">👥</div>
    <div class="t-stat-title">Total Active Players</div>
    <div class="t-stat-val" id="live-total-players">3,420</div>
  </div>
</div>"""

# Remove old stats banner & activity ticker
import re
t = re.sub(r'<!-- ── LIVE STATS COUNTER BOXES.*?<!-- ── STICKY HORIZONTALLY SCROLLABLE GAME TABS BAR ── -->', clean_stats_banner + '\n\n<!-- ── STICKY HORIZONTALLY SCROLLABLE GAME TABS BAR ── -->', t, flags=re.DOTALL)

# Replace the simulation JS with ONLY Total Wagered and Total Players update
clean_sim_js = """
// ── ONLY TOTAL WAGERED & TOTAL PLAYERS COUNTERS UPDATE DYNAMICALLY ──
let totalWagered = 2845200;
let totalPlayers = 3420;

function updateWageredAndPlayers() {
  // Increment Total Wagered smoothly
  totalWagered += Math.floor(350 + Math.random() * 1800);
  const wagEl = document.getElementById('live-total-wagered');
  if (wagEl) {
    wagEl.textContent = '₹' + totalWagered.toLocaleString('en-IN');
  }

  // Increment / fluctuate Total Players
  if (Math.random() > 0.35) {
    totalPlayers += Math.floor(1 + Math.random() * 3);
    const plyEl = document.getElementById('live-total-players');
    if (plyEl) {
      plyEl.textContent = totalPlayers.toLocaleString('en-IN');
    }
  }
}

setInterval(updateWageredAndPlayers, 3000);
"""

t = re.sub(r'// ── REAL-TIME SIMULATION TICKERS.*?setInterval\(runLiveTournamentSimulation, 2800\);', clean_sim_js, t, flags=re.DOTALL)

with open("tournaments.html", "w", encoding="utf-8") as f:
    f.write(t)

print("SUCCESS: tournaments.html streamlined to only dynamically update Total Wagered and Total Players!")