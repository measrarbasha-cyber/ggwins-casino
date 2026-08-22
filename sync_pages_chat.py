# Let's add the live AI chat drawer and script into tournaments.html and vip.html
with open("tournaments.html", "r", encoding="utf-8") as f:
    t = f.read()

chat_drawer_html = """
<!-- ── FULLY AI ANIMATED LIVE CHAT DRAWER ── -->
<div id="ai-chat-drawer" style="display:none;position:fixed;right:0;top:0;bottom:0;width:340px;max-width:92vw;background:#0d121f;border-left:2px solid #ffd700;z-index:99999;box-shadow:-10px 0 40px rgba(0,0,0,0.8);flex-direction:column;">
  <div style="padding:14px 16px;background:rgba(255,215,0,0.1);border-bottom:1px solid rgba(255,215,0,0.25);display:flex;align-items:center;justify-content:space-between">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:15px;font-weight:900;color:#ffd700;display:flex;align-items:center;gap:6px">
      <span>💬</span> Live AI Chat
      <span style="font-size:10px;background:rgba(0,230,118,0.2);color:#00e676;padding:2px 6px;border-radius:999px;font-weight:800">🟢 247 ONLINE</span>
    </div>
    <button onclick="toggleAiChatDrawer()" style="background:none;border:none;color:#94a3b8;font-size:20px;cursor:pointer">✕</button>
  </div>
  <div id="ai-chat-messages" style="flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:8px">
    <!-- Streamed messages -->
  </div>
  <div style="padding:12px;background:rgba(0,0,0,0.4);border-top:1px solid rgba(255,255,255,0.08);display:flex;gap:8px">
    <input type="text" id="ai-chat-input" placeholder="Ask AI Support or chat..." style="flex:1;background:#111827;border:1px solid rgba(255,255,255,0.15);border-radius:10px;padding:9px 12px;color:#fff;font-size:13px;outline:none" onkeydown="if(event.key==='Enter') sendAiDrawerMsg()">
    <button onclick="sendAiDrawerMsg()" style="background:linear-gradient(135deg,#00e676,#00b0ff);border:none;border-radius:10px;padding:0 14px;font-weight:900;color:#000;cursor:pointer">Send</button>
  </div>
</div>
"""

chat_drawer_js = """
// ── AI LIVE CHAT DRAWER LOGIC ──
function toggleAiChatDrawer() {
  const el = document.getElementById('ai-chat-drawer');
  if (!el) return;
  if (el.style.display === 'none' || !el.style.display) {
    el.style.display = 'flex';
  } else {
    el.style.display = 'none';
  }
}

const AI_RESPONSES = [
  { match: /deposit|recharge|payment|upi|gpay|paytm|add money|qr/i, reply: "💳 Deposits on GG Wins are instant with 0% fee! Tap the 'Real Balance' button at top to pay via UPI QR (GPay, PhonePe, Paytm). Bonus coupon GG1675 unlocks up to 100% bonus!" },
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
  { user: 'GG_AI_Host', role: 'ai', msg: '🤖 Tip: Arena Tournaments entry fee is ₹50 with a 60% grand cash payout to 1st place!' }
];

function appendAiDrawerMessage(user, msg, role = 'player') {
  const container = document.getElementById('ai-chat-messages');
  if (!container) return;

  const isAi = role === 'ai';
  const isVip = role === 'vip';
  const isUser = role === 'user';

  const msgDiv = document.createElement('div');
  msgDiv.style.padding = '8px 10px';
  msgDiv.style.borderRadius = '10px';
  msgDiv.style.fontSize = '12px';
  msgDiv.style.background = isAi 
    ? 'rgba(0, 230, 118, 0.12)' 
    : isVip 
      ? 'rgba(255, 215, 0, 0.12)' 
      : isUser 
        ? 'rgba(255, 255, 255, 0.1)' 
        : 'rgba(255, 255, 255, 0.05)';
  msgDiv.style.border = isAi 
    ? '1px solid rgba(0, 230, 118, 0.4)' 
    : isVip 
      ? '1px solid rgba(255, 215, 0, 0.4)' 
      : '1px solid rgba(255, 255, 255, 0.08)';

  const headerHtml = isAi 
    ? '<span style="color:#00e676;font-weight:900">🤖 GG AI Host</span>' 
    : isVip 
      ? `<span style="color:#ffd700;font-weight:900">👑 ${user}</span>` 
      : isUser 
        ? `<span style="color:#00e676;font-weight:900">👤 ${user} (You)</span>` 
        : `<span style="color:#cbd5e1;font-weight:800">👤 ${user}</span>`;

  msgDiv.innerHTML = `
    <div style="display:flex;justify-content:space-between;margin-bottom:2px">
      ${headerHtml}
      <span style="font-size:10px;color:#94a3b8">${new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</span>
    </div>
    <div style="color:#f8fafc;line-height:1.4">${msg}</div>
  `;

  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

function sendAiDrawerMsg() {
  const inputEl = document.getElementById('ai-chat-input');
  if (!inputEl) return;
  const text = inputEl.value.trim();
  if (!text) return;

  const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
  const userName = session.username || 'You';

  appendAiDrawerMessage(userName, text, 'user');
  inputEl.value = '';

  setTimeout(() => {
    let reply = "🤖 I'm your 24/7 AI Casino Host! Ask me about instant deposits, withdrawals, VIP perks, or game tips.";
    for (const rule of AI_RESPONSES) {
      if (rule.match.test(text)) {
        reply = rule.reply;
        break;
      }
    }
    appendAiDrawerMessage('GG AI Host', reply, 'ai');
  }, 700);
}

let drawerStreamIdx = 0;
setInterval(() => {
  const item = AUTO_CHAT_STREAM[drawerStreamIdx % AUTO_CHAT_STREAM.length];
  drawerStreamIdx++;
  appendAiDrawerMessage(item.user, item.msg, item.role);
}, 4000);
"""

# Update top nav in tournaments.html to include chat button
nav_with_chat = """<nav class="t-nav">
  <a href="index.html" style="display:flex;align-items:center;gap:6px;color:#f8fafc;text-decoration:none;font-weight:700;font-size:13px;background:rgba(255,255,255,0.08);padding:6px 12px;border-radius:8px">
    ← Back to Lobby
  </a>
  <div class="t-brand">
    <span>🏆</span> GG Wins <span>Arena Tournaments</span>
  </div>
  <div style="display:flex;align-items:center;gap:8px">
    <a href="#" onclick="if(typeof openWalletModal==='function') openWalletModal('deposit'); return false;" style="color:#00e676;text-decoration:none;font-size:13px;font-weight:800;background:rgba(0,230,118,0.15);padding:6px 12px;border-radius:8px;border:1px solid #00e676">
      💳 Real: <span id="t-user-balance">₹0.00</span>
    </a>
    <button onclick="toggleAiChatDrawer()" style="display:flex;align-items:center;gap:5px;background:rgba(255,215,0,0.15);border:1.5px solid #ffd700;color:#ffd700;font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:800;padding:6px 12px;border-radius:8px;cursor:pointer">
      <span>💬</span> Chat
    </button>
  </div>
</nav>"""

import re
t = re.sub(r'<nav class="t-nav">.*?</nav>', nav_with_chat, t, flags=re.DOTALL)

if "id=\"ai-chat-drawer\"" not in t:
    t = t.replace("</body>", chat_drawer_html + "\n</body>")

if "toggleAiChatDrawer" not in t:
    t = t.replace("</script>\n</body>", "\n" + chat_drawer_js + "\n</script>\n</body>")

with open("tournaments.html", "w", encoding="utf-8") as f:
    f.write(t)

print("SUCCESS: tournaments.html updated with AI Live Chat drawer and topbar button!")