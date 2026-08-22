tournaments_code = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>🏆 Arena Tournaments – GG Wins</title>
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

body {
  background: radial-gradient(circle at 50% 10%, #17122b 0%, #080914 60%, #030408 100%);
  color: #f8fafc;
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  margin: 0;
  padding-bottom: 80px;
}

.t-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
  background: rgba(15, 21, 39, 0.95);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border-gold);
  position: sticky;
  top: 0;
  z-index: 100;
}

.t-brand {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 20px;
  font-weight: 900;
  color: #ffd700;
  display: flex;
  align-items: center;
  gap: 8px;
}

.t-hero {
  text-align: center;
  padding: 24px 16px 14px;
  max-width: 850px;
  margin: 0 auto;
}

.t-hero-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 215, 0, 0.15);
  border: 1.5px solid #ffd700;
  color: #ffd700;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 11.5px;
  font-weight: 900;
  padding: 4px 14px;
  border-radius: 999px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 10px;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
}

.t-hero h1 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 32px;
  font-weight: 900;
  color: #fff;
  margin: 0 0 8px;
  line-height: 1.2;
}
.t-hero h1 span {
  background: linear-gradient(135deg, #ffd700, #ff8c00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.t-hero p {
  font-size: 14px;
  color: #cbd5e1;
  line-height: 1.5;
  margin: 0 auto 14px;
}

/* ── SMOOTH HORIZONTALLY SCROLLABLE GAME TABS ── */
.t-tabs-section {
  max-width: 1200px;
  margin: 0 auto 20px;
  padding: 0 16px;
}

.t-tabs-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.t-tabs-heading {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13.5px;
  font-weight: 800;
  color: #ffd700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  gap: 6px;
}
.t-tabs-hint {
  font-size: 11.5px;
  color: #94a3b8;
}

.t-scrollable-tabs-strip {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 10px 6px 14px 6px;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
  scrollbar-color: #ffd700 rgba(255,255,255,0.06);
}
.t-scrollable-tabs-strip::-webkit-scrollbar {
  height: 6px;
}
.t-scrollable-tabs-strip::-webkit-scrollbar-track {
  background: rgba(15, 21, 39, 0.6);
  border-radius: 999px;
}
.t-scrollable-tabs-strip::-webkit-scrollbar-thumb {
  background: linear-gradient(90deg, #ffd700, #00e676);
  border-radius: 999px;
}

.t-game-tab-pill {
  flex: 0 0 auto;
  min-width: 120px;
  background: #111827;
  border: 1.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
  text-align: center;
  user-select: none;
}
.t-game-tab-pill:hover {
  transform: translateY(-3px);
  border-color: #ffd700;
  background: #1e293b;
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.3);
}
.t-game-tab-pill.active {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.22), rgba(255, 140, 0, 0.18));
  border-color: #ffd700;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
  transform: scale(1.03);
}
.t-pill-icon { font-size: 28px; line-height: 1; }
.t-pill-name { font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 800; color: #fff; white-space: nowrap; }
.t-pill-chip { font-size: 10px; color: #00e676; font-weight: 800; background: rgba(0, 230, 118, 0.15); padding: 2px 8px; border-radius: 999px; }

/* ── SELECTED GAME ARENA SHOWCASE ── */
.t-arena-showcase {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

.t-showcase-card {
  background: linear-gradient(145deg, #111827, #0b1120);
  border: 2px solid #ffd700;
  border-radius: 22px;
  padding: 24px;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.7), 0 0 35px rgba(255, 215, 0, 0.25);
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 24px;
}

@media (max-width: 860px) {
  .t-showcase-card { grid-template-columns: 1fr; }
}

.t-showcase-left {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 16px;
}

.t-showcase-header {
  display: flex;
  align-items: center;
  gap: 14px;
}
.t-s-icon { font-size: 46px; }
.t-s-title { font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 900; color: #fff; }
.t-s-tag { font-size: 11.5px; font-weight: 800; color: #00e676; text-transform: uppercase; }

.t-s-stats-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.t-s-stat-box {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid var(--border-gold);
  border-radius: 14px;
  padding: 12px 14px;
}
.t-s-stat-lbl { font-size: 10.5px; color: #94a3b8; font-weight: 700; text-transform: uppercase; }
.t-s-stat-val { font-family: 'Space Grotesk', sans-serif; font-size: 19px; font-weight: 900; color: #ffd700; margin-top: 2px; }

/* Leaderboard */
.t-showcase-right {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.t-leaderboard-box {
  background: #090e17;
  border: 1.5px solid rgba(255, 215, 0, 0.3);
  border-radius: 14px;
  overflow: hidden;
}
.t-leaderboard-head {
  padding: 10px 16px;
  background: rgba(255, 215, 0, 0.08);
  display: grid;
  grid-template-columns: 46px 1fr 120px;
  font-size: 11px;
  font-weight: 800;
  color: #ffd700;
  text-transform: uppercase;
}
.t-leaderboard-row {
  padding: 11px 16px;
  display: grid;
  grid-template-columns: 46px 1fr 120px;
  align-items: center;
  font-size: 13px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}
.t-leaderboard-row.rank-1 {
  background: rgba(255, 215, 0, 0.12);
  color: #ffd700;
  font-weight: 800;
}
.t-leaderboard-row.rank-2 { background: rgba(192, 192, 192, 0.05); color: #cbd5e1; }
.t-leaderboard-row.rank-3 { background: rgba(205, 127, 50, 0.05); color: #e8976a; }
.t-leaderboard-row.user-row {
  background: rgba(0, 230, 118, 0.12);
  border-top: 1.5px dashed #00e676;
  border-bottom: 1.5px dashed #00e676;
  font-weight: 900;
  color: #00e676;
}

.t-rank-badge { font-weight: 900; }
.t-player-name { display: flex; align-items: center; gap: 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.t-points { text-align: right; font-family: monospace; font-weight: 800; font-size: 12.5px; }

/* Buttons */
.btn-enter-t {
  width: 100%;
  background: linear-gradient(135deg, #00e676, #00b0ff);
  color: #000;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  font-weight: 900;
  padding: 14px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 0 20px rgba(0, 230, 118, 0.4);
}
.btn-enter-t:hover {
  transform: translateY(-2px);
  filter: brightness(1.1);
  box-shadow: 0 0 30px rgba(0, 230, 118, 0.7);
}

.btn-enrolled-t {
  width: 100%;
  background: linear-gradient(135deg, #ffd700, #ff8c00);
  color: #000;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  font-weight: 900;
  padding: 14px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
}
.btn-enrolled-t:hover { transform: translateY(-2px); filter: brightness(1.1); }

/* ── ₹50 POPUP REGISTRATION MODAL ── */
.t-modal-overlay {
  position: fixed; inset: 0; background: rgba(0, 0, 0, 0.84); backdrop-filter: blur(12px);
  z-index: 9999; display: none; align-items: center; justify-content: center; padding: 16px;
}
.t-modal-overlay.open { display: flex; animation: modalFadeIn 0.2s ease; }
@keyframes modalFadeIn { from { opacity: 0; transform: scale(0.96); } to { opacity: 1; transform: scale(1); } }

.t-modal-card {
  background: #111827; border: 2px solid #ffd700; border-radius: 22px; max-width: 440px; width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,0.85), 0 0 40px rgba(255,215,0,0.35); overflow: hidden;
}
.t-modal-header {
  background: linear-gradient(135deg, rgba(255,215,0,0.15), rgba(0,230,118,0.08));
  padding: 16px 20px; border-bottom: 1px solid var(--border-gold); display: flex; align-items: center; justify-content: space-between;
}
.t-modal-title { font-family: 'Space Grotesk', sans-serif; font-size: 16px; font-weight: 900; color: #ffd700; display: flex; align-items: center; gap: 8px; }
.t-modal-close { background: none; border: none; color: #94a3b8; font-size: 20px; cursor: pointer; }
.t-modal-close:hover { color: #fff; }
.t-modal-body { padding: 20px; display: flex; flex-direction: column; gap: 14px; }
.t-modal-game-info { display: flex; align-items: center; gap: 12px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px 14px; }
.t-m-icon { font-size: 36px; }
.t-m-name { font-family: 'Space Grotesk', sans-serif; font-size: 16px; font-weight: 900; color: #fff; }
.t-m-pool { font-size: 12px; color: #ffd700; font-weight: 800; }
.t-modal-breakdown { background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px 14px; display: flex; flex-direction: column; gap: 8px; }
.t-b-row { display: flex; justify-content: space-between; font-size: 13px; color: #cbd5e1; }
.t-b-row.total { border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px; font-weight: 800; font-size: 14px; }
.t-b-row.total .val { color: #00e676; font-size: 16px; }
</style>
</head>
<body>

<nav class="t-nav">
  <a href="index.html" style="display:flex;align-items:center;gap:6px;color:#f8fafc;text-decoration:none;font-weight:700;font-size:13px;background:rgba(255,255,255,0.08);padding:6px 12px;border-radius:8px">
    ← Back to Lobby
  </a>
  <div class="t-brand">
    <span>🏆</span> GG Wins <span>Arena Tournaments</span>
  </div>
  <a href="#" onclick="if(typeof openWalletModal==='function') openWalletModal('deposit'); return false;" style="color:#00e676;text-decoration:none;font-size:13px;font-weight:800;background:rgba(0,230,118,0.15);padding:6px 12px;border-radius:8px;border:1px solid #00e676">
    💳 Real Balance: <span id="t-user-balance">₹0.00</span>
  </a>
</nav>

<div class="t-hero">
  <div class="t-hero-chip">🏆 ALL 20 GAMES CHAMPIONSHIP LEAGUE</div>
  <h1>Click Any Game Tab to <span>Enter Tournament</span></h1>
  <p>Scroll &amp; tap any game below. Pay <strong>₹50 Registration Entry Fee</strong> (deducted from your Real Balance) to enter the leaderboard and compete for grand cash prizes!</p>
</div>

<!-- ── SCROLLABLE GAME TABS ── -->
<div class="t-tabs-section">
  <div class="t-tabs-header-row">
    <div class="t-tabs-heading">
      <span>🎮</span> 20 Game Tournaments (Scroll &amp; Tap to Enter)
    </div>
    <div class="t-tabs-hint">
      ← Scroll Tabs →
    </div>
  </div>
  <div class="t-scrollable-tabs-strip" id="game-tabs-container">
    <!-- Generated by JS -->
  </div>
</div>

<!-- ── ACTIVE GAME ARENA SHOWCASE ── -->
<div class="t-arena-showcase" id="arena-showcase-wrapper">
  <!-- Active tournament rendered here by JS -->
</div>

<!-- ₹50 REGISTRATION CONFIRMATION MODAL POPUP -->
<div class="t-modal-overlay" id="tournament-modal">
  <div class="t-modal-card">
    <div class="t-modal-header">
      <div class="t-modal-title">
        <span>🏆</span> Tournament Registration
      </div>
      <button class="t-modal-close" onclick="closeTournamentModal()">✕</button>
    </div>
    <div class="t-modal-body">
      <div class="t-modal-game-info">
        <div class="t-m-icon" id="m-game-icon">🚀</div>
        <div>
          <div class="t-m-name" id="m-game-title">VIP Crash Royale</div>
          <div class="t-m-pool" id="m-game-pool">Grand Prize Pool: ₹25,000</div>
        </div>
      </div>

      <div class="t-modal-breakdown">
        <div class="t-b-row">
          <span>Tournament Entry Fee:</span>
          <span style="font-weight:800;color:#ffd700">₹50.00 INR</span>
        </div>
        <div class="t-b-row">
          <span>Your Active Real Balance:</span>
          <span id="m-user-bal" style="font-weight:800;color:#00e676">₹0.00</span>
        </div>
        <div class="t-b-row total">
          <span>Amount Deducted from Balance:</span>
          <span class="val">₹50.00</span>
        </div>
      </div>

      <div id="m-insufficient-warn" style="display:none;background:rgba(239,83,80,0.15);border:1px solid #ef5350;color:#ef5350;padding:10px;border-radius:10px;font-size:12.5px;font-weight:700;text-align:center">
        ⚠️ Insufficient Real Balance. Please deposit at least ₹50 to enter.
      </div>

      <div class="t-modal-actions">
        <button class="btn-enter-t" id="btn-confirm-reg" onclick="confirmTournamentPayment()">
          ⚡ Confirm &amp; Pay ₹50 Entry Fee
        </button>
        <button class="btn-enter-t" id="btn-deposit-needed" onclick="openDepositFromTournament()" style="display:none;background:linear-gradient(135deg,#ffd700,#ff8c00)">
          💳 Deposit Funds to Pay Entry Fee
        </button>
      </div>
    </div>
  </div>
</div>

<script src="wallet.js"></script>
<script>
// ── ALL 20 GAMES WITH REALISTIC HUMAN PLAYERS AT TOP ──
const ALL_GAMES = [
  { id: 't_crash', game: 'VIP Crash Royale', icon: '🚀', category: 'originals', url: 'games/crash.html', tag: 'Multiplier Derby', prize: 25000, fee: 50, enrolled: 142, bots: [{ rank: 1, name: 'Aarav_Sharma', score: '428,500 pts' }, { rank: 2, name: 'Vikram_Malhotra', score: '385,200 pts' }, { rank: 3, name: 'Rohan_Verma', score: '312,800 pts' }] },
  { id: 't_mines', game: 'Diamond Mines VIP', icon: '💣', category: 'originals', url: 'games/mines.html', tag: 'Diamond Grid Quest', prize: 20000, fee: 50, enrolled: 156, bots: [{ rank: 1, name: 'Kunal_Singhania', score: '410,400 pts' }, { rank: 2, name: 'Aditya_Roy', score: '364,700 pts' }, { rank: 3, name: 'Manish_Pandey', score: '298,300 pts' }] },
  { id: 't_coinflip', game: 'Coin Flip 3D', icon: '🪙', category: 'casual', url: 'games/coinflip.html', tag: 'Streak Master', prize: 15000, fee: 50, enrolled: 98, bots: [{ rank: 1, name: 'Varun_Kapoor', score: '395,100 pts' }, { rank: 2, name: 'Sameer_Khan', score: '342,600 pts' }, { rank: 3, name: 'Nikhil_Joshi', score: '280,400 pts' }] },
  { id: 't_sicbo', game: 'Sic Bo 3-Dice Arena', icon: '🎲', category: 'table', url: 'games/sicbo.html', tag: 'Triple Dice Cup', prize: 20000, fee: 50, enrolled: 116, bots: [{ rank: 1, name: 'Arjun_Reddy', score: '418,900 pts' }, { rank: 2, name: 'Priya_Patel', score: '365,200 pts' }, { rank: 3, name: 'Deepak_Nair', score: '305,700 pts' }] },
  { id: 't_penalty', game: 'Penalty Shootout', icon: '⚽', category: 'casual', url: 'games/penalty.html', tag: 'Golden Boot League', prize: 18000, fee: 50, enrolled: 124, bots: [{ rank: 1, name: 'Rahul_Gupta', score: '432,600 pts' }, { rank: 2, name: 'Siddharth_Mehta', score: '374,100 pts' }, { rank: 3, name: 'Ananya_Sen', score: '319,500 pts' }] },
  { id: 't_cups', game: 'Magic Shells 3D', icon: '🪄', category: 'casual', url: 'games/cups.html', tag: 'Wizard Cup', prize: 15000, fee: 50, enrolled: 89, bots: [{ rank: 1, name: 'Suresh_Raina', score: '388,400 pts' }, { rank: 2, name: 'Karan_Oberoi', score: '332,900 pts' }, { rank: 3, name: 'Neha_Chopra', score: '275,100 pts' }] },
  { id: 't_rummy', game: 'Indian Rummy 3D', icon: '🃏', category: 'table', url: 'games/rummy.html', tag: '13-Card Grand Slam', prize: 35000, fee: 50, enrolled: 210, bots: [{ rank: 1, name: 'Rajesh_Bansal', score: '485,200 pts' }, { rank: 2, name: 'Harsh_Vardhan', score: '420,800 pts' }, { rank: 3, name: 'Gaurav_Taneja', score: '360,400 pts' }] },
  { id: 't_baccarat', game: 'Royale Baccarat 3D', icon: '👑', category: 'table', url: 'games/baccarat.html', tag: 'High-Stakes Invitational', prize: 25000, fee: 50, enrolled: 135, bots: [{ rank: 1, name: 'Amitabh_K', score: '442,900 pts' }, { rank: 2, name: 'Kabir_Merchant', score: '389,100 pts' }, { rank: 3, name: 'Tanvi_Deshmukh', score: '325,600 pts' }] },
  { id: 't_roulette', game: 'Roulette Royale 3D', icon: '🔴', category: 'table', url: 'games/roulette.html', tag: 'European Wheel Derby', prize: 18000, fee: 50, enrolled: 104, bots: [{ rank: 1, name: 'Vivek_Rathore', score: '405,800 pts' }, { rank: 2, name: 'Abhishek_Bose', score: '352,400 pts' }, { rank: 3, name: 'Rishi_Khurana', score: '294,200 pts' }] },
  { id: 't_blackjack', game: 'Blackjack 21 Pro', icon: '♣️', category: 'table', url: 'games/blackjack.html', tag: '21 Pro League', prize: 22000, fee: 50, enrolled: 148, bots: [{ rank: 1, name: 'Dev_Singhal', score: '436,200 pts' }, { rank: 2, name: 'Pranav_Bhatia', score: '378,500 pts' }, { rank: 3, name: 'Ishaan_Roy', score: '318,100 pts' }] },
  { id: 't_dice', game: 'Classic Dice 3D', icon: '🎲', category: 'casual', url: 'games/dice.html', tag: 'Roll Over Master', prize: 16000, fee: 50, enrolled: 92, bots: [{ rank: 1, name: 'Karthik_S', score: '390,400 pts' }, { rank: 2, name: 'Yash_Chauhan', score: '335,900 pts' }, { rank: 3, name: 'Ayush_Mehra', score: '282,300 pts' }] },
  { id: 't_dragontower', game: 'Dragon Tower', icon: '🐉', category: 'originals', url: 'games/dragontower.html', tag: 'Tower Climber', prize: 22000, fee: 50, enrolled: 110, bots: [{ rank: 1, name: 'Shravan_Kumar', score: '415,600 pts' }, { rank: 2, name: 'Raghav_Dixit', score: '356,200 pts' }, { rank: 3, name: 'Naveen_Patil', score: '299,700 pts' }] },
  { id: 't_ludo', game: 'GG Ludo Championship', icon: '🎲', category: 'casual', url: 'games/ludo.html', tag: '4-Player Token Clash', prize: 30000, fee: 50, enrolled: 175, bots: [{ rank: 1, name: 'Sunil_Gavaskar', score: '465,800 pts' }, { rank: 2, name: 'Rohit_Sood', score: '398,200 pts' }, { rank: 3, name: 'Vikas_Gupta', score: '338,100 pts' }] },
  { id: 't_diamonds', game: 'Diamond Rush', icon: '💎', category: 'originals', url: 'games/diamonds.html', tag: 'Gem Pattern Rush', prize: 18000, fee: 50, enrolled: 105, bots: [{ rank: 1, name: 'Mehul_Choksi', score: '398,400 pts' }, { rank: 2, name: 'Rajat_Sharma', score: '340,600 pts' }, { rank: 3, name: 'Dhruv_Rathi', score: '285,200 pts' }] },
  { id: 't_hilo', game: 'Hilo Master', icon: '🃏', category: 'table', url: 'games/hilo.html', tag: 'Card Guess Challenge', prize: 16000, fee: 50, enrolled: 88, bots: [{ rank: 1, name: 'Mohit_Suri', score: '382,900 pts' }, { rank: 2, name: 'Alok_Nath', score: '328,400 pts' }, { rank: 3, name: 'Pooja_Hegde', score: '271,800 pts' }] },
  { id: 't_limbo', game: 'Limbo Rocket', icon: '📈', category: 'originals', url: 'games/limbo.html', tag: '1000x Multiplier Hunt', prize: 24000, fee: 50, enrolled: 130, bots: [{ rank: 1, name: 'Aakash_Banerjee', score: '440,500 pts' }, { rank: 2, name: 'Anand_Kumar', score: '379,100 pts' }, { rank: 3, name: 'Shashank_Vyas', score: '316,400 pts' }] },
  { id: 't_wheel', game: 'Wheel of Fortune', icon: '🎡', category: 'casual', url: 'games/wheel.html', tag: 'Fortune Spin Cup', prize: 14000, fee: 50, enrolled: 82, bots: [{ rank: 1, name: 'Sanjay_Dutt', score: '375,200 pts' }, { rank: 2, name: 'Ravi_Shastri', score: '318,400 pts' }, { rank: 3, name: 'Kapil_Dev', score: '264,800 pts' }] },
  { id: 't_keno', game: 'Keno Classic', icon: '🎱', category: 'casual', url: 'games/keno.html', tag: 'Lucky Numbers Derby', prize: 15000, fee: 50, enrolled: 76, bots: [{ rank: 1, name: 'Pankaj_Tripathi', score: '380,600 pts' }, { rank: 2, name: 'Manoj_Bajpayee', score: '325,100 pts' }, { rank: 3, name: 'Nawaz_Siddiqui', score: '269,400 pts' }] },
  { id: 't_slots', game: 'Fortune Slots 777', icon: '🎰', category: 'originals', url: 'games/slots.html', tag: 'Triple 7s Jackpot', prize: 28000, fee: 50, enrolled: 160, bots: [{ rank: 1, name: 'Vijay_Mallya', score: '470,200 pts' }, { rank: 2, name: 'Harshad_Mehta', score: '412,800 pts' }, { rank: 3, name: 'Rakesh_J', score: '355,900 pts' }] },
  { id: 't_plinko', game: 'Plinko Drop', icon: '⚽', category: 'casual', url: 'games/plinko.html', tag: 'Pegboard Gravity Rush', prize: 17000, fee: 50, enrolled: 95, bots: [{ rank: 1, name: 'Sourav_Ganguly', score: '392,400 pts' }, { rank: 2, name: 'Hardik_Pandya', score: '338,700 pts' }, { rank: 3, name: 'Jasprit_Bumrah', score: '281,300 pts' }] }
];

let selectedGameId = 't_crash';
let modalTargetGame = null;

function isRegistered(tId) {
  try {
    return localStorage.getItem('ggwins_tournament_' + tId) === 'true';
  } catch(e) { return false; }
}

function getUserScore(tId) {
  try {
    return parseInt(localStorage.getItem('ggwins_t_score_' + tId) || '48500');
  } catch(e) { return 48500; }
}

// ── RENDER SCROLLABLE TABS ──
function renderTabs() {
  const tabsContainer = document.getElementById('game-tabs-container');
  if (!tabsContainer) return;

  tabsContainer.innerHTML = ALL_GAMES.map(g => {
    const isActive = g.id === selectedGameId;
    const registered = isRegistered(g.id);

    return `
      <div class="t-game-tab-pill ${isActive ? 'active' : ''}" onclick="handleTabClick('${g.id}')">
        <span class="t-pill-icon">${g.icon}</span>
        <span class="t-pill-name">${g.game}</span>
        <span class="t-pill-chip">${registered ? '✓ ENROLLED' : '₹50 ENTRY'}</span>
      </div>
    `;
  }).join('');
}

// ── CLICKING A GAME TAB SELECTS & OPENS ₹50 MODAL ──
function handleTabClick(gId) {
  selectedGameId = gId;
  renderTabs();
  renderShowcase();

  const registered = isRegistered(gId);
  if (!registered) {
    // Open ₹50 entry registration popup immediately
    openRegistrationModal(gId);
  } else {
    const target = ALL_GAMES.find(item => item.id === gId);
    if (target) {
      if (typeof showToast === 'function') showToast('Opening ' + target.game + '...', 'info');
      setTimeout(() => { window.location.href = target.url; }, 400);
    }
  }
}

function renderShowcase() {
  const showcaseWrapper = document.getElementById('arena-showcase-wrapper');
  if (!showcaseWrapper) return;

  const g = ALL_GAMES.find(item => item.id === selectedGameId) || ALL_GAMES[0];
  const registered = isRegistered(g.id);
  const uScore = getUserScore(g.id);

  const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
  const userName = session.username || 'You (Player)';
  const wallets = typeof getWallets === 'function' ? getWallets() : { real: 0 };
  const userBalEl = document.getElementById('t-user-balance');
  if (userBalEl) userBalEl.textContent = '₹' + (parseFloat(wallets.real)||0).toLocaleString('en-IN', {minimumFractionDigits: 2});

  showcaseWrapper.innerHTML = `
    <div class="t-showcase-card">
      <div class="t-showcase-left">
        <div>
          <div class="t-showcase-header">
            <div class="t-s-icon">${g.icon}</div>
            <div>
              <div class="t-s-title">${g.game}</div>
              <div class="t-s-tag">🏆 ${g.tag} Tournament</div>
            </div>
          </div>

          <p style="font-size:13.5px;color:#cbd5e1;line-height:1.5;margin:16px 0">
            Compete against top players in <strong>${g.game}</strong>. Tournament entry fee is strictly <strong>₹50.00</strong> deducted directly from your Real INR Balance.
          </p>

          <div class="t-s-stats-row">
            <div class="t-s-stat-box">
              <div class="t-s-stat-lbl">Grand Prize Pool</div>
              <div class="t-s-stat-val">₹${g.prize.toLocaleString('en-IN')}</div>
            </div>
            <div class="t-s-stat-box">
              <div class="t-s-stat-lbl">Registration Fee</div>
              <div class="t-s-stat-val" style="color:#00e676">₹${g.fee}.00</div>
            </div>
            <div class="t-s-stat-box">
              <div class="t-s-stat-lbl">Enrolled Players</div>
              <div class="t-s-stat-val" style="font-size:16px;color:#cbd5e1">👥 ${g.enrolled + (registered ? 1 : 0)} Players</div>
            </div>
            <div class="t-s-stat-box">
              <div class="t-s-stat-lbl">1st Place Prize</div>
              <div class="t-s-stat-val" style="font-size:16px;color:#ffd700">🥇 60% (₹${Math.floor(g.prize * 0.6).toLocaleString('en-IN')})</div>
            </div>
          </div>
        </div>

        <div>
          ${registered ? `
            <button class="btn-enrolled-t" onclick="window.location.href='${g.url}'">
              ✅ Enrolled &amp; Active • Launch ${g.game} &amp; Climb 🎮
            </button>
          ` : `
            <button class="btn-enter-t" onclick="openRegistrationModal('${g.id}')">
              ⚡ Pay ₹50 Entry Fee &amp; Join ${g.game} Tournament
            </button>
          `}
        </div>
      </div>

      <div class="t-showcase-right">
        <div class="t-leaderboard-box">
          <div class="t-leaderboard-head">
            <span>Rank</span>
            <span>Player</span>
            <span style="text-align:right">Tournament Pts</span>
          </div>

          <!-- Rank 1 -->
          <div class="t-leaderboard-row rank-1">
            <span class="t-rank-badge">🥇 #1</span>
            <span class="t-player-name">👑 ${g.bots[0].name}</span>
            <span class="t-points">${g.bots[0].score}</span>
          </div>

          <!-- Rank 2 -->
          <div class="t-leaderboard-row rank-2">
            <span class="t-rank-badge">🥈 #2</span>
            <span class="t-player-name">⭐ ${g.bots[1].name}</span>
            <span class="t-points">${g.bots[1].score}</span>
          </div>

          <!-- Rank 3 -->
          <div class="t-leaderboard-row rank-3">
            <span class="t-rank-badge">🥉 #3</span>
            <span class="t-player-name">🎖️ ${g.bots[2].name}</span>
            <span class="t-points">${g.bots[2].score}</span>
          </div>

          <!-- User Standing -->
          ${registered ? `
            <div class="t-leaderboard-row user-row">
              <span class="t-rank-badge">🎮 #4</span>
              <span class="t-player-name">👤 ${userName}</span>
              <span class="t-points">${uScore.toLocaleString('en-IN')} pts</span>
            </div>
          ` : `
            <div style="padding:10px 14px;font-size:12px;color:#94a3b8;text-align:center;background:rgba(0,0,0,0.35);border-top:1px solid rgba(255,255,255,0.05)">
              🔒 Tap to pay <strong>₹50 Entry Fee</strong> and add your score to this leaderboard!
            </div>
          `}
        </div>
      </div>
    </div>
  `;
}

// ── ₹50 POPUP REGISTRATION MODAL ──
function openRegistrationModal(gId) {
  const g = ALL_GAMES.find(item => item.id === gId) || ALL_GAMES[0];
  modalTargetGame = g;

  document.getElementById('m-game-icon').textContent = g.icon;
  document.getElementById('m-game-title').textContent = g.game;
  document.getElementById('m-game-pool').textContent = 'Grand Prize Pool: ₹' + g.prize.toLocaleString('en-IN');

  const wallets = typeof getWallets === 'function' ? getWallets() : { real: 0 };
  const curBal = parseFloat(wallets.real || 0);
  document.getElementById('m-user-bal').textContent = '₹' + curBal.toLocaleString('en-IN', {minimumFractionDigits: 2});

  const warnEl = document.getElementById('m-insufficient-warn');
  const confirmBtn = document.getElementById('btn-confirm-reg');
  const depositBtn = document.getElementById('btn-deposit-needed');

  if (curBal < g.fee) {
    if (warnEl) warnEl.style.display = 'block';
    if (confirmBtn) confirmBtn.style.display = 'none';
    if (depositBtn) depositBtn.style.display = 'block';
  } else {
    if (warnEl) warnEl.style.display = 'none';
    if (confirmBtn) confirmBtn.style.display = 'block';
    if (depositBtn) depositBtn.style.display = 'none';
  }

  document.getElementById('tournament-modal').classList.add('open');
}

function closeTournamentModal() {
  document.getElementById('tournament-modal').classList.remove('open');
  modalTargetGame = null;
}

function openDepositFromTournament() {
  closeTournamentModal();
  if (typeof openWalletModal === 'function') openWalletModal('deposit');
}

function confirmTournamentPayment() {
  if (!modalTargetGame) return;
  const g = modalTargetGame;
  const fee = g.fee || 50;

  const wallets = typeof getWallets === 'function' ? getWallets() : { real: 0 };
  const currentRealBal = parseFloat(wallets.real || 0);

  if (currentRealBal < fee) {
    alert('Insufficient balance. Please deposit at least ₹50 to enter.');
    openDepositFromTournament();
    return;
  }

  // Deduct ₹50.00 from Real Balance
  wallets.real = Math.max(0, currentRealBal - fee);
  if (typeof saveWallets === 'function') saveWallets(wallets);

  // Save registration & score
  localStorage.setItem('ggwins_tournament_' + g.id, 'true');
  localStorage.setItem('ggwins_t_score_' + g.id, (Math.floor(42000 + Math.random() * 18000)).toString());

  // Log transaction
  if (typeof addTransaction === 'function') {
    addTransaction({
      id: 'TRN-' + Math.floor(100000 + Math.random() * 900000),
      orderId: 'ORD-TRN-' + Math.floor(100000 + Math.random() * 900000),
      type: 'withdraw',
      wallet: 'real',
      amount: fee,
      currency: 'INR',
      method: 'Tournament Entry Fee (₹' + fee + ') - ' + g.game,
      status: 'Completed',
      timestamp: Date.now()
    });
  }

  closeTournamentModal();

  if (typeof showToast === 'function') {
    showToast('🎉 Registered for ' + g.game + ' Tournament! ₹' + fee + ' fee paid from Real INR. Opening game...', 'success');
  }

  renderTabs();
  renderShowcase();

  setTimeout(() => {
    window.location.href = g.url;
  }, 800);
}

renderTabs();
renderShowcase();
</script>
</body>
</html>
"""

with open("tournaments.html", "w", encoding="utf-8") as f:
    f.write(tournaments_code)

print("SUCCESS: Updated tournaments.html with scrollable tabs, instant modal popup on click, and real human names on leaderboard!")