with open("tournaments.html", "r", encoding="utf-8") as f:
    t = f.read()

# Add stats banner HTML above tabs
stats_banner = """<!-- ── LIVE STATS COUNTER BOXES (UPDATING IN REAL TIME) ── -->
<div class="t-stats-banner">
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
    <div class="t-stat-icon">🏆</div>
    <div class="t-stat-title">Total Tournament Winners</div>
    <div class="t-stat-val" id="live-total-winners">1,847</div>
  </div>
  <div class="t-stat-card">
    <div class="t-stat-icon">👥</div>
    <div class="t-stat-title">Active Live Competitors</div>
    <div class="t-stat-val" id="live-active-players">3,420</div>
  </div>
</div>

<!-- ── REAL-TIME LIVE ACTIVITY STREAM TICKER ── -->
<div class="t-activity-ticker-wrap">
  <div class="t-activity-ticker">
    <div class="t-pulse-dot"></div>
    <span id="live-ticker-text">⚡ Aarav_Sharma just scored +1,250 pts in VIP Crash Royale!</span>
  </div>
</div>
"""

stats_css = """
/* ── LIVE STATS TICKER COUNTER BOXES ── */
.t-stats-banner {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 12px;
  max-width: 1000px;
  margin: 0 auto 16px;
  padding: 0 16px;
}
.t-stat-card {
  background: rgba(15, 21, 39, 0.85);
  border: 1px solid var(--border-gold);
  border-radius: 14px;
  padding: 12px 14px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.t-stat-icon { font-size: 22px; margin-bottom: 2px; }
.t-stat-title { font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
.t-stat-val { font-family: 'Space Grotesk', sans-serif; font-size: 19px; font-weight: 900; color: #ffd700; margin-top: 2px; transition: color 0.3s; }
.t-stat-val.flash { color: #00e676; text-shadow: 0 0 12px #00e676; }

/* ── LIVE REAL-PLAYER ACTIVITY TICKER ── */
.t-activity-ticker-wrap {
  max-width: 1000px;
  margin: 0 auto 20px;
  padding: 0 16px;
}
.t-activity-ticker {
  background: rgba(0, 230, 118, 0.08);
  border: 1px solid rgba(0, 230, 118, 0.3);
  border-radius: 999px;
  padding: 8px 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 12.5px;
  color: #00e676;
  font-weight: 700;
  box-shadow: 0 0 15px rgba(0, 230, 118, 0.15);
}
.t-pulse-dot {
  width: 8px;
  height: 8px;
  background: #00e676;
  border-radius: 50%;
  box-shadow: 0 0 8px #00e676;
  animation: livePulse 1.4s infinite;
}
@keyframes livePulse {
  0% { transform: scale(0.9); opacity: 0.7; }
  50% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 14px #00e676; }
  100% { transform: scale(0.9); opacity: 0.7; }
}
.t-leaderboard-row.score-flash {
  background: rgba(0, 230, 118, 0.25) !important;
  color: #00e676 !important;
}
"""

if ".t-stats-banner" not in t:
    t = t.replace("</style>", stats_css + "\n</style>")

if "id=\"live-total-wagered\"" not in t:
    t = t.replace("<div class=\"t-sticky-tabs-wrapper\">", stats_banner + "\n<div class=\"t-sticky-tabs-wrapper\">")

# Add IDs to leaderboard rows for dynamic updates
t = t.replace("<!-- Rank 1 -->\n            <div class=\"t-leaderboard-row rank-1\">", "<!-- Rank 1 -->\n            <div class=\"t-leaderboard-row rank-1\" id=\"row-${g.id}-1\">")
t = t.replace("<!-- Rank 2 -->\n            <div class=\"t-leaderboard-row rank-2\">", "<!-- Rank 2 -->\n            <div class=\"t-leaderboard-row rank-2\" id=\"row-${g.id}-2\">")
t = t.replace("<!-- Rank 3 -->\n            <div class=\"t-leaderboard-row rank-3\">", "<!-- Rank 3 -->\n            <div class=\"t-leaderboard-row rank-3\" id=\"row-${g.id}-3\">")

t = t.replace("<span class=\"t-points\">${g.bots[0].score}", "<span class=\"t-points\" id=\"pts-${g.id}-1\">${g.bots[0].score}")
t = t.replace("<span class=\"t-points\">${g.bots[1].score}", "<span class=\"t-points\" id=\"pts-${g.id}-2\">${g.bots[1].score}")
t = t.replace("<span class=\"t-points\">${g.bots[2].score}", "<span class=\"t-points\" id=\"pts-${g.id}-3\">${g.bots[2].score}")

sim_js = """
// ── REAL-TIME SIMULATION TICKERS: TOTAL WAGERED, TOTAL WINNERS & LIVE LEADERBOARD POINTS ──
let totalWagered = 2845200;
let totalWinners = 1847;
let activePlayers = 3420;

const ACTIVITY_TEMPLATES = [
  "⚡ {name} scored +{pts} pts in {game}!",
  "🏆 {name} climbed to {score} pts in {game}!",
  "💰 {name} won a ₹{win} tournament bonus in {game}!",
  "🔥 {name} hit a 5x streak in {game} (+{pts} pts)!",
  "🎯 {name} entered {game} tournament leaderboard!"
];

function runLiveTournamentSimulation() {
  // 1. Increment Total Wagered smoothly
  totalWagered += Math.floor(450 + Math.random() * 2400);
  const wagEl = document.getElementById('live-total-wagered');
  if (wagEl) {
    wagEl.textContent = '₹' + totalWagered.toLocaleString('en-IN');
    wagEl.classList.add('flash');
    setTimeout(() => wagEl.classList.remove('flash'), 600);
  }

  // 2. Increment Winners periodically
  if (Math.random() > 0.4) {
    totalWinners += 1;
    const winEl = document.getElementById('live-total-winners');
    if (winEl) winEl.textContent = totalWinners.toLocaleString('en-IN');
  }

  // 3. Fluctuating Active Players
  activePlayers += Math.floor((Math.random() - 0.45) * 6);
  const actEl = document.getElementById('live-active-players');
  if (actEl) actEl.textContent = activePlayers.toLocaleString('en-IN');

  // 4. Update Random Player Points on Leaderboards
  if (typeof ALL_GAMES !== 'undefined' && ALL_GAMES.length > 0) {
    const randGame = ALL_GAMES[Math.floor(Math.random() * ALL_GAMES.length)];
    const randBotIdx = Math.floor(Math.random() * 3);
    const pointGain = Math.floor(250 + Math.random() * 1600);
    
    let curScore = typeof randGame.bots[randBotIdx].score === 'number' 
      ? randGame.bots[randBotIdx].score 
      : parseInt(String(randGame.bots[randBotIdx].score).replace(/[^0-9]/g, '')) || 350000;
    
    curScore += pointGain;
    randGame.bots[randBotIdx].score = curScore;

    const ptsEl = document.getElementById(`pts-${randGame.id}-${randBotIdx + 1}`);
    const rowEl = document.getElementById(`row-${randGame.id}-${randBotIdx + 1}`);
    if (ptsEl) {
      ptsEl.textContent = curScore.toLocaleString('en-IN') + ' pts';
    }
    if (rowEl) {
      rowEl.classList.add('score-flash');
      setTimeout(() => rowEl.classList.remove('score-flash'), 1200);
    }

    // 5. Update Activity Ticker text
    const tickerEl = document.getElementById('live-ticker-text');
    if (tickerEl) {
      const tmpl = ACTIVITY_TEMPLATES[Math.floor(Math.random() * ACTIVITY_TEMPLATES.length)];
      const msg = tmpl
        .replace('{name}', randGame.bots[randBotIdx].name)
        .replace('{pts}', pointGain.toLocaleString('en-IN'))
        .replace('{score}', curScore.toLocaleString('en-IN'))
        .replace('{game}', randGame.game)
        .replace('{win}', (Math.floor(1200 + Math.random() * 4500)).toLocaleString('en-IN'));
      tickerEl.textContent = msg;
    }
  }
}

setInterval(runLiveTournamentSimulation, 2800);
"""

if "runLiveTournamentSimulation" not in t:
    t = t.replace("renderAll();\n</script>", "renderAll();\n" + sim_js + "\n</script>")

with open("tournaments.html", "w", encoding="utf-8") as f:
    f.write(t)

print("SUCCESS: Live ticker simulation and stats counters successfully patched into tournaments.html!")