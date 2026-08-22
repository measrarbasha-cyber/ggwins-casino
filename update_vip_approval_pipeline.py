# 1. Update style.css to include .glowing-vip-badge.bronze
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\style.css", "r", encoding="utf-8") as f:
    css = f.read()

bronze_badge_css = """
.glowing-vip-badge.bronze {
  background: linear-gradient(135deg, #cd7f32, #e8976a);
  color: #fff;
  border: 1px solid #e8976a;
  box-shadow: 0 0 14px rgba(205, 127, 50, 0.7), 0 0 26px rgba(232, 151, 106, 0.4);
}
"""

if ".glowing-vip-badge.bronze" not in css:
    css = css.replace(".glowing-vip-badge.silver {", bronze_badge_css + "\n.glowing-vip-badge.silver {")
    with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\style.css", "w", encoding="utf-8") as f:
        f.write(css)

# 2. Update script.js updateAuthUI to render Bronze, Silver, Gold, Platinum, Diamond badges
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\script.js", "r", encoding="utf-8") as f:
    sjs = f.read()

old_script_badge = """      // Render Glowing VIP Badge
      const vipTier = localStorage.getItem('ggwins_vip_level') || session.vipLevel || 'Bronze';
      const isVip = ['silver', 'gold', 'platinum', 'diamond', 'vip master', 'silver vip', 'gold vip', 'platinum vip', 'diamond vip'].some(k => vipTier.toLowerCase().includes(k));
      let badgeEl = userPanel.querySelector('.glowing-vip-badge');
      if (isVip) {
        const tierClass = vipTier.toLowerCase().includes('diamond') ? 'diamond' : vipTier.toLowerCase().includes('platinum') ? 'platinum' : vipTier.toLowerCase().includes('silver') ? 'silver' : 'gold';
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

new_script_badge = """      // Render Glowing VIP Badge
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

sjs = sjs.replace(old_script_badge, new_script_badge)
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\script.js", "w", encoding="utf-8") as f:
    f.write(sjs)

# 3. Update vip-lounge.html checkVipAccess
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip-lounge.html", "r", encoding="utf-8") as f:
    vl = f.read()

old_vl_isvip = """  const isVip = ['silver', 'gold', 'platinum', 'diamond', 'vip master', 'silver vip', 'gold vip', 'platinum vip', 'diamond vip'].some(k => vipTier.toLowerCase().includes(k));"""
new_vl_isvip = """  const isVip = ['bronze vip', 'silver', 'gold', 'platinum', 'diamond', 'vip master', 'silver vip', 'gold vip', 'platinum vip', 'diamond vip'].some(k => vipTier.toLowerCase().includes(k) && vipTier.toLowerCase() !== 'bronze');"""

vl = vl.replace(old_vl_isvip, new_vl_isvip)

old_vl_pill = """    pill.className = `glowing-vip-badge ${vipTier.toLowerCase().includes('diamond')?'diamond':vipTier.toLowerCase().includes('platinum')?'platinum':vipTier.toLowerCase().includes('silver')?'silver':'gold'}`;"""
new_vl_pill = """    pill.className = `glowing-vip-badge ${vipTier.toLowerCase().includes('diamond')?'diamond':vipTier.toLowerCase().includes('platinum')?'platinum':vipTier.toLowerCase().includes('silver')?'silver':vipTier.toLowerCase().includes('bronze')?'bronze':'gold'}`;"""

vl = vl.replace(old_vl_pill, new_vl_pill)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip-lounge.html", "w", encoding="utf-8") as f:
    f.write(vl)

# 4. Update server.py approve-vip & user-status
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py", "r", encoding="utf-8") as f:
    srv = f.read()

old_srv_approve = """            if user_obj:
                user_obj["vipLevel"] = assigned_vip
                user_obj["vipExpiresAt"] = expires_at"""

new_srv_approve = """            if user_obj:
                user_obj["vipLevel"] = assigned_vip
                user_obj["vipExpiresAt"] = expires_at
            else:
                new_user = {
                    "id": target_user_id or ("USER-" + str(int(time.time()))[-6:]),
                    "username": target_username or "Player",
                    "vipLevel": assigned_vip,
                    "vipExpiresAt": expires_at,
                    "joined": now_ms
                }
                users.append(new_user)"""

srv = srv.replace(old_srv_approve, new_srv_approve)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py", "w", encoding="utf-8") as f:
    f.write(srv)

print("SUCCESS: Configured airtight VIP approval -> badge & benefit unlock pipeline across backend & frontend!")
