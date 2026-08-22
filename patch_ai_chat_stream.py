with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

ai_full_engine = """// ── FULLY AI ANIMATED LIVE CHAT & AUTO-RUNNING FEED ENGINE ──
const AI_RESPONSES = [
  { match: /deposit|recharge|payment|upi|gpay|paytm|add money|qr/i, reply: "💳 Deposits on GG Wins are instant with 0% fee! Tap the 'Deposit & Wallet' button at top to pay via UPI QR (GPay, PhonePe, Paytm). Coupon code GG1675 unlocks up to 100% bonus!" },
  { match: /withdraw|payout|bank|cashout|transfer/i, reply: "⚡ Withdrawals are processed within 5–15 minutes directly to your bank account or UPI ID. Make sure standard 1x turnover on real deposits is completed." },
  { match: /vip|membership|bronze|silver|gold|badge/i, reply: "👑 GG VIP Club gives you daily vault cash (₹35 Bronze / ₹60 Silver / ₹150 Gold) and glowing username badges for 30 days! Visit vip.html to join." },
  { match: /tournament|arena|entry fee|leaderboard/i, reply: "🏆 Arena Tournaments are active across all 20 games! Entry fee is strictly ₹50 deducted from your Real Balance. 1st place wins 60% of the grand prize pool!" },
  { match: /crash|multiplier|plane/i, reply: "🚀 GG Crash: Place your wager before takeoff and cash out before the rocket crashes! Highest multiplier recorded today: 840.50x!" },
  { match: /mines|diamond/i, reply: "💣 GG Mines: Choose 1 to 24 mines on the 5x5 grid. The more diamonds you reveal without hitting a mine, the bigger your multiplier payout!" },
  { match: /rummy|cards|sequence/i, reply: "🃏 Indian Rummy 3D: Form valid pure sequences, sets, and declare your hand before opponents to win the prize table!" },
  { match: /hi|hello|hey|sup|good/i, reply: "👋 Welcome to GG Wins! I'm your AI Casino Support Host. How can I assist your gaming session today?" },
  { match: /win|hack|cheat|fair|provably/i, reply: "🛡️ All GG Wins games operate on certified Provably Fair cryptographic algorithms (SHA-256). Every round hash can be independently verified!" }
];

const AUTO_CHAT_STREAM = [
  { user: 'Vikram_Malhotra', role: 'vip', msg: 'Just cashed out 18.4x on Crash! 🚀 ₹9,200 win!' },
  { user: 'Kunal_Singhania', role: 'vip', msg: 'Hit 8 diamonds in a row in Mines! Diamond grid is on fire 🔥' },
  { user: 'Aarav_Sharma', role: 'vip', msg: 'VIP Bronze daily reward ₹35 credited automatically 👑' },
  { user: 'Priya_Patel', role: 'player', msg: 'Who is playing Indian Rummy table right now? 🃏' },
  { user: 'Rahul_Gupta', role: 'player', msg: 'Deposited via PhonePe and bonus code GG1675 worked instantly! 💳' },
  { user: 'Siddharth_Mehta', role: 'player', msg: 'Rank #2 on Sic Bo tournament leaderboard! 🎲' },
  { user: 'GG_AI_Host', role: 'ai', msg: '🤖 Tip: Claim your daily spin in Wheel of Fortune to unlock bonus vault coins!' },
  { user: 'Dev_Singhal', role: 'vip', msg: 'Blackjack 21 dealer busted 3 times in a row! ♣️' },
  { user: 'Ananya_Sen', role: 'player', msg: 'Penalty shootout top right corner never fails ⚽' },
  { user: 'GG_AI_Host', role: 'ai', msg: '💎 Active Jackpot Pool is currently at ₹4,85,000 across Arena Tournaments!' },
  { user: 'Manish_Pandey', role: 'player', msg: 'Fastest payout ever! Got ₹4,500 withdrawal in 3 mins ⚡' },
  { user: 'Harsh_Vardhan', role: 'vip', msg: 'VIP Gold tier gives 150 daily vault reward everyday! Best perk 👑' }
];

function appendChatMessage(user, msg, role = 'player') {
  const container = document.getElementById('chat-messages') || document.querySelector('.chat-messages');
  if (!container) return;

  const isAi = role === 'ai';
  const isVip = role === 'vip';
  const isUser = role === 'user';

  const msgDiv = document.createElement('div');
  msgDiv.className = `chat-msg ${isAi ? 'chat-msg-ai' : isVip ? 'chat-msg-vip' : isUser ? 'chat-msg-user' : ''}`;
  msgDiv.style.padding = '9px 12px';
  msgDiv.style.borderRadius = '12px';
  msgDiv.style.marginBottom = '8px';
  msgDiv.style.fontSize = '12.5px';
  msgDiv.style.background = isAi 
    ? 'linear-gradient(135deg, rgba(0, 230, 118, 0.12), rgba(0, 176, 255, 0.08))' 
    : isVip 
      ? 'linear-gradient(135deg, rgba(255, 215, 0, 0.12), rgba(255, 140, 0, 0.08))' 
      : isUser 
        ? 'rgba(255, 255, 255, 0.1)' 
        : 'rgba(255, 255, 255, 0.05)';
  msgDiv.style.border = isAi 
    ? '1.5px solid rgba(0, 230, 118, 0.4)' 
    : isVip 
      ? '1.5px solid rgba(255, 215, 0, 0.4)' 
      : isUser 
        ? '1.5px solid rgba(255, 255, 255, 0.2)' 
        : '1px solid rgba(255, 255, 255, 0.08)';

  const headerHtml = isAi 
    ? '<span style="color:#00e676;font-weight:900;display:flex;align-items:center;gap:4px">🤖 GG AI Host <span style="font-size:9px;background:rgba(0,230,118,0.2);padding:1px 5px;border-radius:4px">AI BOT</span></span>' 
    : isVip 
      ? `<span style="color:#ffd700;font-weight:900;display:flex;align-items:center;gap:4px">👑 ${user} <span style="font-size:9px;background:rgba(255,215,0,0.2);padding:1px 5px;border-radius:4px">VIP</span></span>` 
      : isUser 
        ? `<span style="color:#00e676;font-weight:900">👤 ${user} (You)</span>` 
        : `<span style="color:#cbd5e1;font-weight:800">👤 ${user}</span>`;

  msgDiv.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">
      ${headerHtml}
      <span style="font-size:10px;color:#94a3b8">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
    </div>
    <div style="color:#f8fafc;line-height:1.4">${msg}</div>
  `;

  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;

  // Keep max 60 messages in DOM for ultra-smooth performance
  while (container.children.length > 60) {
    container.removeChild(container.firstChild);
  }
}

function showTypingIndicator() {
  const container = document.getElementById('chat-messages') || document.querySelector('.chat-messages');
  if (!container) return null;

  const typingDiv = document.createElement('div');
  typingDiv.id = 'ai-typing-indicator';
  typingDiv.className = 'ai-typing-indicator';
  typingDiv.innerHTML = `
    <span>🤖 GG AI Host is typing</span>
    <span class="typing-dot"></span>
    <span class="typing-dot"></span>
    <span class="typing-dot"></span>
  `;
  container.appendChild(typingDiv);
  container.scrollTop = container.scrollHeight;
  return typingDiv;
}

function removeTypingIndicator() {
  const ind = document.getElementById('ai-typing-indicator');
  if (ind && ind.parentNode) ind.parentNode.removeChild(ind);
}

function sendChatMsg() {
  const inputEl = document.getElementById('chat-input-field') || (dom && dom.chatInputField);
  if (!inputEl) return;
  const userText = inputEl.value.trim();
  if (!userText) return;

  const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
  const userName = session.username || 'You';

  // Append User message
  appendChatMessage(userName, userText, 'user');
  inputEl.value = '';

  // Show animated AI typing indicator
  showTypingIndicator();

  // Process AI Response with animated delay
  setTimeout(() => {
    removeTypingIndicator();
    let reply = "🤖 I'm your 24/7 AI Casino Host! You can ask me about instant deposits, 5-min withdrawals, VIP perks, or game tips.";
    for (const rule of AI_RESPONSES) {
      if (rule.match.test(userText)) {
        reply = rule.reply;
        break;
      }
    }
    appendChatMessage('GG AI Host', reply, 'ai');
  }, 750);
}

// ── AUTO-RUNNING LIVE CHAT STREAM (POSTS ON ITS OWN EVERY 3.5 SECONDS) ──
let chatStreamIdx = 0;
function autoRunChatFeed() {
  const item = AUTO_CHAT_STREAM[chatStreamIdx % AUTO_CHAT_STREAM.length];
  chatStreamIdx++;

  if (item.role === 'ai') {
    showTypingIndicator();
    setTimeout(() => {
      removeTypingIndicator();
      appendChatMessage(item.user, item.msg, 'ai');
    }, 600);
  } else {
    appendChatMessage(item.user, item.msg, item.role);
  }

  // Update live online count smoothly
  const onlineEl = document.getElementById('chat-online');
  if (onlineEl) {
    const base = 240 + Math.floor(Math.sin(Date.now() / 20000) * 25) + Math.floor(Math.random() * 8);
    onlineEl.textContent = base.toString();
  }
}

// Start auto-running on its own!
setInterval(autoRunChatFeed, 3500);
setTimeout(autoRunChatFeed, 1000);"""

import re
s = re.sub(r'// ── AI-POWERED LIVE CHAT ASSISTANT.*?setInterval\(\(\) => \{.*?\}, 12000\);', ai_full_engine, s, flags=re.DOTALL)

with open("script.js", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: script.js updated with fully AI animated live chat that runs on its own!")