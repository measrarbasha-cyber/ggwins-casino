with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

# 1. Update GAMES array in perfect order (Originals, Table, Arcade/Casual, Slots)
games_ordered = """const GAMES = [
  // ── 1. GG ORIGINALS ──
  { id: 1,  name: 'GG Crash',          provider: 'GG Originals',  icon: '🚀', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 5821, gameUrl: 'games/crash.html' },
  { id: 2,  name: 'GG Mines',          provider: 'GG Originals',  icon: '💣', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 6420, gameUrl: 'games/mines.html' },
  { id: 3,  name: 'GG Limbo Rocket',   provider: 'GG Originals',  icon: '📈', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 3984, gameUrl: 'games/limbo.html' },
  { id: 4,  name: 'Dragon Tower',      provider: 'GG Originals',  icon: '🐉', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 5120, gameUrl: 'games/dragontower.html' },
  { id: 5,  name: 'GG Diamond Rush',   provider: 'GG Originals',  icon: '💎', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 4920, gameUrl: 'games/diamonds.html' },
  { id: 6,  name: 'GG Fortune Slots',  provider: 'GG Originals',  icon: '🎰', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 5244, gameUrl: 'games/slots.html' },
  { id: 7,  name: 'GG Plinko Drop',    provider: 'GG Originals',  icon: '⚽', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 4891, gameUrl: 'games/plinko.html' },

  // ── 2. CARDS & TABLE GAMES ──
  { id: 8,  name: 'GG Indian Rummy 3D',provider: 'GG Originals',  icon: '🃏', grad: 'grad-table-1',    category: 'table',     badge: 'hot',      players: 7450, gameUrl: 'games/rummy.html' },
  { id: 9,  name: 'GG Baccarat 3D',    provider: 'GG Originals',  icon: '👑', grad: 'grad-table-1',    category: 'table',     badge: 'new',      players: 3870, gameUrl: 'games/baccarat.html' },
  { id: 10, name: 'GG Blackjack 21',   provider: 'GG Originals',  icon: '♣️', grad: 'grad-table-2',    category: 'table',     badge: 'hot',      players: 3980, gameUrl: 'games/blackjack.html' },
  { id: 11, name: 'GG Roulette Royale',provider: 'GG Originals',  icon: '🔴', grad: 'grad-table-1',    category: 'table',     badge: 'hot',      players: 4201, gameUrl: 'games/roulette.html' },
  { id: 12, name: 'GG Sic Bo 3-Dice',  provider: 'GG Originals',  icon: '🎲', grad: 'grad-table-2',    category: 'table',     badge: 'new',      players: 3240, gameUrl: 'games/sicbo.html' },
  { id: 13, name: 'GG Hilo Master',    provider: 'GG Originals',  icon: '🃏', grad: 'grad-table-1',    category: 'table',     badge: 'new',      players: 3410, gameUrl: 'games/hilo.html' },

  // ── 3. CASUAL & ARCADE GAMES ──
  { id: 14, name: 'GG Coin Flip 3D',   provider: 'GG Originals',  icon: '🪙', grad: 'grad-original-1', category: 'arcade',    badge: 'hot',      players: 4890, gameUrl: 'games/coinflip.html' },
  { id: 15, name: 'GG Penalty Shoot',  provider: 'GG Originals',  icon: '⚽', grad: 'grad-original-1', category: 'arcade',    badge: 'hot',      players: 5610, gameUrl: 'games/penalty.html' },
  { id: 16, name: 'GG Magic Shells',   provider: 'GG Originals',  icon: '🪄', grad: 'grad-original-1', category: 'arcade',    badge: 'hot',      players: 6180, gameUrl: 'games/cups.html' },
  { id: 17, name: 'GG Ludo Champions', provider: 'GG Originals',  icon: '🎲', grad: 'grad-original-1', category: 'arcade',    badge: 'hot',      players: 6420, gameUrl: 'games/ludo.html' },
  { id: 18, name: 'GG Dice 3D',        provider: 'GG Originals',  icon: '🎲', grad: 'grad-original-1', category: 'arcade',    badge: 'original', players: 3102, gameUrl: 'games/dice.html' },
  { id: 19, name: 'Wheel of Fortune',  provider: 'GG Originals',  icon: '🎡', grad: 'grad-original-1', category: 'arcade',    badge: 'hot',      players: 4120, gameUrl: 'games/wheel.html' },
  { id: 20, name: 'GG Keno Classic',   provider: 'GG Originals',  icon: '🎱', grad: 'grad-original-1', category: 'arcade',    badge: 'new',      players: 2830, gameUrl: 'games/keno.html' }
];"""

import re
s = re.sub(r'const GAMES = \[.*?\];', games_ordered, s, flags=re.DOTALL)

# 2. Carousel Auto-slide Enhancement (Auto-run every 4.5s & pause on hover)
carousel_auto_code = """// ── ENHANCED AUTO-RUNNING HERO CAROUSEL ──
function goToSlide(index) {
  if (!slides || !slides.length) return;
  slides[currentSlide].classList.remove('active');
  if (dots[currentSlide]) dots[currentSlide].classList.remove('active');
  currentSlide = (index + slides.length) % slides.length;
  slides[currentSlide].classList.add('active');
  if (dots[currentSlide]) dots[currentSlide].classList.add('active');
}

function startSlideTimer() {
  clearInterval(slideTimer);
  slideTimer = setInterval(() => {
    goToSlide(currentSlide + 1);
  }, 4500);
}

const heroCarouselEl = document.getElementById('hero-carousel') || document.querySelector('.hero-carousel');
if (heroCarouselEl) {
  heroCarouselEl.addEventListener('mouseenter', () => clearInterval(slideTimer));
  heroCarouselEl.addEventListener('mouseleave', () => startSlideTimer());
}
startSlideTimer();"""

s = re.sub(r'function goToSlide\(index\)\s*\{.*?startSlideTimer\(\);', carousel_auto_code, s, flags=re.DOTALL)

# 3. AI-Powered Casino Chat Assistant & Live Player Simulation
ai_chat_code = """// ── AI-POWERED LIVE CHAT ASSISTANT ──
const AI_RESPONSES = [
  { match: /deposit|recharge|payment|upi|gpay|paytm|add money|qr/i, reply: "💳 Deposits on GG Wins are instant with 0% fee! Tap the 'Deposit & Wallet' button at top to pay via UPI QR (GPay, PhonePe, Paytm). Bonus code GG1675 unlocks up to 100% bonus!" },
  { match: /withdraw|payout|bank|cashout|transfer/i, reply: "⚡ Withdrawals are processed within 5–15 minutes directly to your bank account or UPI ID. Make sure you have completed standard 1x turnover on real deposits." },
  { match: /vip|membership|bronze|silver|gold|badge/i, reply: "👑 GG VIP Club gives you daily vault cash (₹35 Bronze / ₹60 Silver / ₹150 Gold) and glowing username badges for 30 days! Visit vip.html to join." },
  { match: /tournament|arena|entry fee|leaderboard/i, reply: "🏆 Arena Tournaments are active across all 20 games! Entry fee is strictly ₹50 deducted from your Real Balance. 1st place wins 60% of the grand prize pool!" },
  { match: /crash|multiplier|plane/i, reply: "🚀 GG Crash: Place your wager before takeoff and cash out before the rocket crashes! Highest multiplier recorded this week: 840.50x!" },
  { match: /mines|diamond/i, reply: "💣 GG Mines: Choose 1 to 24 mines on the 5x5 grid. The more diamonds you reveal without hitting a mine, the bigger your multiplier payout!" },
  { match: /rummy|cards|sequence/i, reply: "🃏 Indian Rummy 3D: Form valid pure sequences, sets, and declare your hand before opponents to take the prize table!" },
  { match: /hi|hello|hey|sup|good/i, reply: "👋 Welcome to GG Wins! I'm your AI Casino Support Host. How can I assist your gaming session today?" },
  { match: /win|hack|cheat|fair|provably/i, reply: "🛡️ All GG Wins games operate on certified Provably Fair cryptographic algorithms (SHA-256). Every round hash can be independently verified!" }
];

const COMMUNITY_BOT_CHATS = [
  { user: 'Vikram_Malhotra', msg: 'Just hit 14.5x on Crash! 🚀 ₹7,250 win!' },
  { user: 'Kunal_Singhania', msg: 'Diamond Mines grid was hot today 🔥' },
  { user: 'Aarav_Sharma', msg: 'VIP Bronze daily reward credited automatically ₹35 👑' },
  { user: 'Priya_Patel', msg: 'Who is playing Indian Rummy table right now? 🃏' },
  { user: 'Rahul_Gupta', msg: 'Deposited via PhonePe and bonus code GG1675 worked instantly! 💳' },
  { user: 'Siddharth_M', msg: 'Rank #2 on Sic Bo tournament leaderboard! 🎲' }
];

function appendChatMessage(user, msg, isAi = false, isUser = false) {
  const container = document.getElementById('chat-messages') || document.querySelector('.chat-messages');
  if (!container) return;

  const msgDiv = document.createElement('div');
  msgDiv.className = 'chat-msg';
  msgDiv.style.padding = '8px 10px';
  msgDiv.style.borderRadius = '10px';
  msgDiv.style.marginBottom = '8px';
  msgDiv.style.fontSize = '12.5px';
  msgDiv.style.background = isAi 
    ? 'rgba(0, 230, 118, 0.12)' 
    : isUser 
      ? 'rgba(255, 215, 0, 0.15)' 
      : 'rgba(255, 255, 255, 0.05)';
  msgDiv.style.border = isAi 
    ? '1px solid rgba(0, 230, 118, 0.3)' 
    : isUser 
      ? '1px solid rgba(255, 215, 0, 0.3)' 
      : '1px solid rgba(255, 255, 255, 0.08)';

  const headerHtml = isAi 
    ? '<span style="color:#00e676;font-weight:900">🤖 GG AI Support</span>' 
    : isUser 
      ? `<span style="color:#ffd700;font-weight:900">👤 ${user}</span>` 
      : `<span style="color:#cbd5e1;font-weight:800">👤 ${user}</span>`;

  msgDiv.innerHTML = `
    <div style="display:flex;justify-content:space-between;margin-bottom:2px">
      ${headerHtml}
      <span style="font-size:10px;color:#94a3b8">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
    </div>
    <div style="color:#f8fafc;line-height:1.4">${msg}</div>
  `;

  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

function sendChatMsg() {
  const inputEl = document.getElementById('chat-input-field') || (dom && dom.chatInputField);
  if (!inputEl) return;
  const userText = inputEl.value.trim();
  if (!userText) return;

  const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
  const userName = session.username || 'You (Player)';

  // Append User message
  appendChatMessage(userName, userText, false, true);
  inputEl.value = '';

  // Process AI Response
  setTimeout(() => {
    let reply = "🤖 I'm here 24/7 to help! For deposits, withdrawals, games or VIP perks, feel free to ask or contact support in Help Centre.";
    for (const rule of AI_RESPONSES) {
      if (rule.match.test(userText)) {
        reply = rule.reply;
        break;
      }
    }
    appendChatMessage('GG AI Support', reply, true, false);
  }, 700);
}

// Simulated active player messages every 12 seconds
setInterval(() => {
  if (Math.random() > 0.3) {
    const item = COMMUNITY_BOT_CHATS[Math.floor(Math.random() * COMMUNITY_BOT_CHATS.length)];
    appendChatMessage(item.user, item.msg, false, false);
  }
}, 12000);"""

s = re.sub(r'function sendChatMsg\(.*?\n\}\n(?=dom\.chatSendBtn|\$)', ai_chat_code + '\n', s, flags=re.DOTALL)

with open("script.js", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: script.js updated with ordered games, auto-running banner slider, and AI chat assistant!")