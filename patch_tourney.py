with open("tournaments.html", "r", encoding="utf-8") as f:
    t = f.read()

# Add all remaining games to ALL_GAMES list if missing
more_games = """  {
    id: 't_dice',
    game: 'Classic Dice 3D',
    icon: '🎲',
    category: 'casual',
    url: 'games/dice.html',
    tag: 'Roll Over Master',
    prize: 16000,
    fee: 50,
    enrolled: 92,
    bots: [
      { rank: 1, name: 'DiceRoll_Bot99', score: '287,400 pts', badge: 'TOP BOT' },
      { rank: 2, name: 'HighLowKing', score: '228,900 pts', badge: 'BOT' },
      { rank: 3, name: 'RollMaster_AI', score: '179,300 pts', badge: 'BOT' }
    ]
  },
  {
    id: 't_dragontower',
    game: 'Dragon Tower',
    icon: '🐉',
    category: 'originals',
    url: 'games/dragontower.html',
    tag: 'Tower Climber',
    prize: 22000,
    fee: 50,
    enrolled: 110,
    bots: [
      { rank: 1, name: 'DragonSlayer_AI', score: '324,500 pts', badge: 'TOP BOT' },
      { rank: 2, name: 'TowerLord88', score: '261,200 pts', badge: 'BOT' },
      { rank: 3, name: 'FlameClimber', score: '198,700 pts', badge: 'BOT' }
    ]
  },
  {
    id: 't_ludo',
    game: 'GG Ludo Championship',
    icon: '🎲',
    category: 'casual',
    url: 'games/ludo.html',
    tag: '4-Player Token Clash',
    prize: 30000,
    fee: 50,
    enrolled: 175,
    bots: [
      { rank: 1, name: 'LudoGrandMaster', score: '394,600 pts', badge: 'TOP BOT' },
      { rank: 2, name: 'TokenHunter_AI', score: '315,800 pts', badge: 'BOT' },
      { rank: 3, name: 'SixRollKing', score: '246,100 pts', badge: 'BOT' }
    ]
  },
  {
    id: 't_diamonds',
    game: 'Diamond Rush',
    icon: '💎',
    category: 'originals',
    url: 'games/diamonds.html',
    tag: 'Gem Pattern Rush',
    prize: 18000,
    fee: 50,
    enrolled: 105,
    bots: [
      { rank: 1, name: 'GemCollector_AI', score: '302,400 pts', badge: 'TOP BOT' },
      { rank: 2, name: 'DiamondStrike', score: '241,600 pts', badge: 'BOT' },
      { rank: 3, name: 'RubyKing88', score: '185,200 pts', badge: 'BOT' }
    ]
  },
  {
    id: 't_hilo',
    game: 'Hilo Master',
    icon: '🃏',
    category: 'table',
    url: 'games/hilo.html',
    tag: 'Card Guess Challenge',
    prize: 16000,
    fee: 50,
    enrolled: 88,
    bots: [
      { rank: 1, name: 'HiloOracle_AI', score: '291,300 pts', badge: 'TOP BOT' },
      { rank: 2, name: 'CardPredictor', score: '234,800 pts', badge: 'BOT' },
      { rank: 3, name: 'AceHighPro', score: '172,900 pts', badge: 'BOT' }
    ]
  },
  {
    id: 't_limbo',
    game: 'Limbo Rocket',
    icon: '📈',
    category: 'originals',
    url: 'games/limbo.html',
    tag: '1000x Multiplier Hunt',
    prize: 24000,
    fee: 50,
    enrolled: 130,
    bots: [
      { rank: 1, name: 'RocketLauncher_AI', score: '358,900 pts', badge: 'TOP BOT' },
      { rank: 2, name: 'LimboKing99', score: '289,400 pts', badge: 'BOT' },
      { rank: 3, name: 'HyperMultiplier', score: '215,600 pts', badge: 'BOT' }
    ]
  },
  {
    id: 't_wheel',
    game: 'Wheel of Fortune',
    icon: '🎡',
    category: 'casual',
    url: 'games/wheel.html',
    tag: 'Fortune Spin Cup',
    prize: 14000,
    fee: 50,
    enrolled: 82,
    bots: [
      { rank: 1, name: 'MegaSpinner_AI', score: '276,400 pts', badge: 'TOP BOT' },
      { rank: 2, name: 'LuckySector88', score: '218,200 pts', badge: 'BOT' },
      { rank: 3, name: 'SpinDoctor_X', score: '164,500 pts', badge: 'BOT' }
    ]
  },
  {
    id: 't_keno',
    game: 'Keno Classic',
    icon: '🎱',
    category: 'casual',
    url: 'games/keno.html',
    tag: 'Lucky Numbers Derby',
    prize: 15000,
    fee: 50,
    enrolled: 76,
    bots: [
      { rank: 1, name: 'KenoMaster_AI', score: '281,200 pts', badge: 'TOP BOT' },
      { rank: 2, name: 'NumberMatcher', score: '224,600 pts', badge: 'BOT' },
      { rank: 3, name: 'Hit10Hunter', score: '169,800 pts', badge: 'BOT' }
    ]
  },
  {
    id: 't_slots',
    game: 'Fortune Slots 777',
    icon: '🎰',
    category: 'originals',
    url: 'games/slots.html',
    tag: 'Triple 7s Jackpot',
    prize: 28000,
    fee: 50,
    enrolled: 160,
    bots: [
      { rank: 1, name: 'JackpotReeler_AI', score: '388,400 pts', badge: 'TOP BOT' },
      { rank: 2, name: 'TripleSevenKing', score: '318,100 pts', badge: 'BOT' },
      { rank: 3, name: 'WildScatter_X', score: '242,900 pts', badge: 'BOT' }
    ]
  },
  {
    id: 't_plinko',
    game: 'Plinko Drop',
    icon: '⚽',
    category: 'casual',
    url: 'games/plinko.html',
    tag: 'Pegboard Gravity Rush',
    prize: 17000,
    fee: 50,
    enrolled: 95,
    bots: [
      { rank: 1, name: 'PlinkoDrop_AI', score: '294,800 pts', badge: 'TOP BOT' },
      { rank: 2, name: 'EdgeBouncer99', score: '236,100 pts', badge: 'BOT' },
      { rank: 3, name: 'HighPegMaster', score: '178,300 pts', badge: 'BOT' }
    ]
  }
];"""

if "t_plinko" not in t:
    t = t.replace("];\n\nfunction isRegistered", more_games + "\n\nfunction isRegistered")

# Add Popup Modal HTML & CSS
modal_css = """
/* ── ₹50 REGISTRATION POPUP MODAL ── */
.t-modal-overlay {
  position: fixed; inset: 0; background: rgba(0, 0, 0, 0.82); backdrop-filter: blur(10px);
  z-index: 9999; display: none; align-items: center; justify-content: center; padding: 16px;
}
.t-modal-overlay.open { display: flex; animation: modalFadeIn 0.2s ease; }
@keyframes modalFadeIn { from { opacity: 0; transform: scale(0.96); } to { opacity: 1; transform: scale(1); } }
.t-modal-card {
  background: #111827; border: 2px solid #ffd700; border-radius: 20px; max-width: 440px; width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,0.8), 0 0 35px rgba(255,215,0,0.3); overflow: hidden;
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
.t-m-icon { font-size: 34px; }
.t-m-name { font-family: 'Space Grotesk', sans-serif; font-size: 16px; font-weight: 900; color: #fff; }
.t-m-pool { font-size: 12px; color: #ffd700; font-weight: 800; }
.t-modal-breakdown { background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px 14px; display: flex; flex-direction: column; gap: 8px; }
.t-b-row { display: flex; justify-content: space-between; font-size: 13px; color: #cbd5e1; }
.t-b-row.total { border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px; font-weight: 800; font-size: 14px; }
.t-b-row.total .val { color: #00e676; font-size: 16px; }
"""

if ".t-modal-overlay" not in t:
    t = t.replace("</style>", modal_css + "\n</style>")

modal_html = """<!-- ₹50 REGISTRATION CONFIRMATION MODAL POPUP -->
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
        <button class="btn-register-t" id="btn-confirm-reg" onclick="confirmTournamentPayment()">
          ⚡ Confirm &amp; Pay ₹50 Entry Fee
        </button>
        <button class="btn-register-t" id="btn-deposit-needed" onclick="openDepositFromTournament()" style="display:none;background:linear-gradient(135deg,#ffd700,#ff8c00)">
          💳 Deposit Funds to Pay Entry Fee
        </button>
      </div>
    </div>
  </div>
</div>"""

if "id=\"tournament-modal\"" not in t:
    t = t.replace("</div>\n</div>\n\n<script src=\"wallet.js\">", "</div>\n</div>\n\n" + modal_html + "\n\n<script src=\"wallet.js\">")

# Update card click and modal functions in script
modal_funcs = """
let selectedTournament = null;

function openTournamentModal(tId) {
  const target = ALL_GAMES.find(g => g.id === tId) || TOURNAMENTS.find(g => g.id === tId);
  if (!target) return;

  if (isRegistered(tId)) {
    window.location.href = target.url;
    return;
  }

  selectedTournament = target;

  document.getElementById('m-game-icon').textContent = target.icon;
  document.getElementById('m-game-title').textContent = target.game;
  document.getElementById('m-game-pool').textContent = 'Grand Prize Pool: ₹' + (target.prize||25000).toLocaleString('en-IN');

  const wallets = typeof getWallets === 'function' ? getWallets() : { real: 0 };
  const curBal = parseFloat(wallets.real || 0);
  document.getElementById('m-user-bal').textContent = '₹' + curBal.toLocaleString('en-IN', {minimumFractionDigits: 2});

  const warnEl = document.getElementById('m-insufficient-warn');
  const confirmBtn = document.getElementById('btn-confirm-reg');
  const depositBtn = document.getElementById('btn-deposit-needed');

  if (curBal < (target.fee || 50)) {
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
  selectedTournament = null;
}

function openDepositFromTournament() {
  closeTournamentModal();
  if (typeof openWalletModal === 'function') {
    openWalletModal('deposit');
  }
}

function confirmTournamentPayment() {
  if (!selectedTournament) return;
  const t = selectedTournament;
  const fee = t.fee || 50;

  const wallets = typeof getWallets === 'function' ? getWallets() : { real: 0 };
  const currentRealBal = parseFloat(wallets.real || 0);

  if (currentRealBal < fee) {
    alert('Insufficient balance. Please deposit at least ₹50 to enter.');
    openDepositFromTournament();
    return;
  }

  wallets.real = Math.max(0, currentRealBal - fee);
  if (typeof saveWallets === 'function') saveWallets(wallets);

  localStorage.setItem('ggwins_tournament_' + t.id, 'true');
  localStorage.setItem('ggwins_t_score_' + t.id, (Math.floor(42000 + Math.random() * 18000)).toString());

  if (typeof addTransaction === 'function') {
    addTransaction({
      id: 'TRN-' + Math.floor(100000 + Math.random() * 900000),
      orderId: 'ORD-TRN-' + Math.floor(100000 + Math.random() * 900000),
      type: 'withdraw',
      wallet: 'real',
      amount: fee,
      currency: 'INR',
      method: 'Tournament Entry Fee (₹' + fee + ') - ' + t.game,
      status: 'Completed',
      timestamp: Date.now()
    });
  }

  closeTournamentModal();

  if (typeof showToast === 'function') {
    showToast('🎉 Registered for ' + t.game + ' Tournament! ₹' + fee + ' fee paid. Opening game...', 'success');
  }

  renderTournaments();

  setTimeout(() => {
    window.location.href = t.url;
  }, 800);
}
"""

if "function openTournamentModal" not in t:
    t += "\n" + modal_funcs

# Make card click trigger openTournamentModal
t = t.replace("class=\"btn-register-t\" onclick=\"registerTournament", "class=\"btn-register-t\" onclick=\"openTournamentModal")
t = t.replace("<div class=\"t-card\" id=\"card-${t.id}\">", "<div class=\"t-card\" id=\"card-${t.id}\" onclick=\"openTournamentModal('${t.id}')\">")

with open("tournaments.html", "w", encoding="utf-8") as f:
    f.write(t)

print("SUCCESS: Updated tournaments.html with all 20 games and ₹50 popup registration modal!")