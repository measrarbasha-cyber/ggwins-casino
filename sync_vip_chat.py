with open("vip.html", "r", encoding="utf-8") as f:
    v = f.read()

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
function toggleAiChatDrawer() {
  const el = document.getElementById('ai-chat-drawer');
  if (!el) return;
  if (el.style.display === 'none' || !el.style.display) el.style.display = 'flex';
  else el.style.display = 'none';
}

const AI_RESPONSES = [
  { match: /deposit|recharge|payment|upi|gpay|paytm|add money|qr/i, reply: "💳 Deposits on GG Wins are instant with 0% fee! Tap the 'Real Balance' button at top to pay via UPI QR (GPay, PhonePe, Paytm). Bonus coupon GG1675 unlocks up to 100% bonus!" },
  { match: /withdraw|payout|bank|cashout|transfer/i, reply: "⚡ Withdrawals are processed within 5–15 minutes directly to your bank account or UPI ID." },
  { match: /vip|membership|bronze|silver|gold|badge/i, reply: "👑 GG VIP Club gives you daily vault cash (₹35 Bronze / ₹60 Silver / ₹150 Gold) and glowing username badges for 30 days!" }
];

const AUTO_CHAT_STREAM = [
  { user: 'Vikram_Malhotra', role: 'vip', msg: 'Just cashed out 18.4x on Crash! 🚀 ₹9,200 win!' },
  { user: 'Kunal_Singhania', role: 'vip', msg: 'Hit 8 diamonds in a row in Mines! 🔥' },
  { user: 'Aarav_Sharma', role: 'vip', msg: 'VIP Bronze daily reward ₹35 credited automatically 👑' }
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
  msgDiv.style.background = isAi ? 'rgba(0, 230, 118, 0.12)' : isVip ? 'rgba(255, 215, 0, 0.12)' : 'rgba(255, 255, 255, 0.05)';
  msgDiv.style.border = isAi ? '1px solid rgba(0, 230, 118, 0.4)' : isVip ? '1px solid rgba(255, 215, 0, 0.4)' : '1px solid rgba(255, 255, 255, 0.08)';

  const headerHtml = isAi ? '<span style="color:#00e676;font-weight:900">🤖 GG AI Host</span>' : isVip ? `<span style="color:#ffd700;font-weight:900">👑 ${user}</span>` : `<span style="color:#cbd5e1;font-weight:800">👤 ${user}</span>`;
  msgDiv.innerHTML = `<div style="display:flex;justify-content:space-between;margin-bottom:2px">${headerHtml}<span style="font-size:10px;color:#94a3b8">${new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</span></div><div style="color:#f8fafc;line-height:1.4">${msg}</div>`;
  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

function sendAiDrawerMsg() {
  const inputEl = document.getElementById('ai-chat-input');
  if (!inputEl) return;
  const text = inputEl.value.trim();
  if (!text) return;
  appendAiDrawerMessage('You', text, 'user');
  inputEl.value = '';
  setTimeout(() => {
    let reply = "🤖 I'm your 24/7 AI Casino Host! Ask me about VIP rewards, instant deposits, or game strategies.";
    for (const rule of AI_RESPONSES) {
      if (rule.match.test(text)) { reply = rule.reply; break; }
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

if "id=\"ai-chat-drawer\"" not in v:
    v = v.replace("</body>", chat_drawer_html + "\n<script>\n" + chat_drawer_js + "\n</script>\n</body>")

with open("vip.html", "w", encoding="utf-8") as f:
    f.write(v)

print("SUCCESS: vip.html updated with AI Live Chat drawer!")