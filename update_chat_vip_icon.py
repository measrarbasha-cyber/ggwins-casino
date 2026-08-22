# 1. Update index.html
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html", "r", encoding="utf-8") as f:
    ihtml = f.read()

old_top_chat = """          <button class="chat-toggle-btn" id="chat-toggle-btn" aria-label="Toggle chat">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
            <span class="chat-count">247</span>
          </button>"""

new_top_chat = """          <!-- Small VIP Badge Icon next to Chat Box (Shown for new users, removed upon Admin approval) -->
          <a href="vip.html" class="vip-chat-mini-badge" id="vip-chat-mini-badge" title="Upgrade to VIP Club (Unlock VIP Lounge & Daily Cash Rewards)">
            <span class="vip-mini-crown">👑</span>
            <span class="vip-mini-txt">VIP</span>
          </a>

          <button class="chat-toggle-btn" id="chat-toggle-btn" aria-label="Toggle chat">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
            <span class="chat-count">247</span>
          </button>"""

ihtml = ihtml.replace(old_top_chat, new_top_chat)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html", "w", encoding="utf-8") as f:
    f.write(ihtml)

# 2. Update style.css with .vip-chat-mini-badge CSS styles
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\style.css", "r", encoding="utf-8") as f:
    css = f.read()

vip_mini_css = """
/* ── SMALL VIP BADGE ICON NEXT TO CHAT ── */
.vip-chat-mini-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.22), rgba(255, 140, 0, 0.18));
  border: 1.5px solid #ffd700;
  border-radius: 999px;
  padding: 4px 10px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 11px;
  font-weight: 900;
  color: #ffd700;
  text-decoration: none;
  box-shadow: 0 0 12px rgba(255, 215, 0, 0.4);
  animation: vipMiniPulse 2s infinite ease-in-out;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
  cursor: pointer;
  flex-shrink: 0;
}
.vip-chat-mini-badge:hover {
  transform: scale(1.08);
  background: linear-gradient(135deg, #ffd700, #ff8c00);
  color: #000;
  box-shadow: 0 0 22px rgba(255, 215, 0, 0.8);
}
.vip-mini-crown { font-size: 13px; }
.vip-mini-txt { letter-spacing: 0.05em; font-weight: 900; }

@keyframes vipMiniPulse {
  0%, 100% { transform: scale(1); box-shadow: 0 0 10px rgba(255, 215, 0, 0.35); }
  50% { transform: scale(1.06); box-shadow: 0 0 20px rgba(255, 215, 0, 0.75); }
}
"""

if ".vip-chat-mini-badge" not in css:
    css += vip_mini_css
    with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\style.css", "w", encoding="utf-8") as f:
        f.write(css)

# 3. Update script.js updateAuthUI to show/hide the mini badge and render the official user badge
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\script.js", "r", encoding="utf-8") as f:
    sjs = f.read()

old_auth_ui = """      // Render Glowing VIP Badge
      const vipTier = localStorage.getItem('ggwins_vip_level') || session.vipLevel || 'Bronze';
      const isVip = ['bronze vip', 'silver', 'gold', 'platinum', 'diamond', 'vip master', 'silver vip', 'gold vip', 'platinum vip', 'diamond vip'].some(k => vipTier.toLowerCase().includes(k) && vipTier.toLowerCase() !== 'bronze');
      let badgeEl = userPanel.querySelector('.glowing-vip-badge');
      if (isVip) {
        const tierClass = vipTier.toLowerCase().includes('diamond') ? 'diamond' 
          : vipTier.toLowerCase().includes('platinum') ? 'platinum' 
          : vipTier.toLowerCase().includes('silver') ? 'silver' 
          : vipTier.toLowerCase().includes('bronze') ? 'bronze' 
          : 'gold';
        if (!badgeEl) {
          badgeEl = document.createElement('span');
          userPanel.appendChild(badgeEl);
        }
        badgeEl.className = `glowing-vip-badge ${tierClass}`;
        badgeEl.innerHTML = `👑 ${vipTier.toUpperCase()}`;
        badgeEl.style.display = 'inline-flex';
        badgeEl.style.marginLeft = '6px';
      } else if (badgeEl) {
        badgeEl.style.display = 'none';
      }"""

new_auth_ui = """      // Render Glowing VIP Badge & Manage Mini Chat VIP Badge Icon
      const vipTier = localStorage.getItem('ggwins_vip_level') || session.vipLevel || 'Bronze';
      const isVip = ['bronze vip', 'silver', 'gold', 'platinum', 'diamond', 'vip master', 'silver vip', 'gold vip', 'platinum vip', 'diamond vip'].some(k => vipTier.toLowerCase().includes(k) && vipTier.toLowerCase() !== 'bronze');
      
      const chatMiniVip = document.getElementById('vip-chat-mini-badge');
      let badgeEl = userPanel.querySelector('.glowing-vip-badge');

      if (isVip) {
        // User is Approved VIP: Remove mini VIP icon next to chat box
        if (chatMiniVip) chatMiniVip.style.display = 'none';

        // Grant official glowing badge to user
        const tierClass = vipTier.toLowerCase().includes('diamond') ? 'diamond' 
          : vipTier.toLowerCase().includes('platinum') ? 'platinum' 
          : vipTier.toLowerCase().includes('silver') ? 'silver' 
          : vipTier.toLowerCase().includes('bronze') ? 'bronze' 
          : 'gold';

        if (!badgeEl) {
          badgeEl = document.createElement('span');
          userPanel.appendChild(badgeEl);
        }
        badgeEl.className = `glowing-vip-badge ${tierClass}`;
        badgeEl.innerHTML = `👑 ${vipTier.toUpperCase()}`;
        badgeEl.style.display = 'inline-flex';
        badgeEl.style.marginLeft = '6px';
      } else {
        // User is New / Non-VIP: Show small VIP badge icon next to chat box
        if (chatMiniVip) chatMiniVip.style.display = 'inline-flex';
        if (badgeEl) badgeEl.style.display = 'none';
      }"""

sjs = sjs.replace(old_auth_ui, new_auth_ui)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\script.js", "w", encoding="utf-8") as f:
    f.write(sjs)

print("SUCCESS: Added small VIP badge icon next to chat box for new users and auto-switch on Admin approval!")
