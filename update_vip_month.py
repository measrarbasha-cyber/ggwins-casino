import re, time

# 1. Update vip-lounge.html
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip-lounge.html", "r", encoding="utf-8") as f:
    vl = f.read()

# Change 1000 to 150 daily vault reward
vl = vl.replace('Claim your exclusive VIP daily free reward (₹1,000 INR). Refreshes every 24 hours.', 'Claim your exclusive VIP daily free reward (₹150 INR). Refreshes every 24 hours (Monthly VIP Benefit).')
vl = vl.replace('⚡ Claim ₹1,000 Daily Vault', '⚡ Claim ₹150 Daily Vault')
vl = vl.replace('wallets.real = (parseFloat(wallets.real) || 0) + 1000.00;', 'wallets.real = (parseFloat(wallets.real) || 0) + 150.00;')
vl = vl.replace('amount: 1000.00,', 'amount: 150.00,')
vl = vl.replace("method: 'Daily VIP Cashback Vault',", "method: 'Daily VIP Cashback Vault (₹150)',")
vl = vl.replace("btn.textContent = '✅ ₹1,000 Claimed Today!';", "btn.textContent = '✅ ₹150 Claimed Today!';")
vl = vl.replace("showToast('🎉 ₹1,000 Daily VIP Vault reward added to your balance!', 'success');", "showToast('🎉 ₹150 Daily VIP Vault reward added to your balance!', 'success');")

# Add 30-day monthly expiration check in vip-lounge.html
old_check_vip = """// Check VIP Access
function checkVipAccess() {
  const session = JSON.parse(localStorage.getItem('ggwins_session') || 'null');
  const vipTier = localStorage.getItem('ggwins_vip_level') || (session ? session.vipLevel : 'Bronze') || 'Bronze';
  const isVip = ['silver', 'gold', 'platinum', 'diamond', 'vip master', 'silver vip', 'gold vip', 'platinum vip', 'diamond vip'].some(k => vipTier.toLowerCase().includes(k));"""

new_check_vip = """// Check VIP Access with 1-Month Expiry Rule
function checkVipAccess() {
  const session = JSON.parse(localStorage.getItem('ggwins_session') || 'null');
  let vipTier = localStorage.getItem('ggwins_vip_level') || (session ? session.vipLevel : 'Bronze') || 'Bronze';
  const expiresAt = parseInt(localStorage.getItem('ggwins_vip_expires_at') || (session ? session.vipExpiresAt : 0) || '0');

  // Check 1-Month Expiry
  if (expiresAt > 0 && Date.now() > expiresAt) {
    vipTier = 'Bronze';
    localStorage.setItem('ggwins_vip_level', 'Bronze');
    if (session) { session.vipLevel = 'Bronze'; localStorage.setItem('ggwins_session', JSON.stringify(session)); }
  }

  const isVip = ['silver', 'gold', 'platinum', 'diamond', 'vip master', 'silver vip', 'gold vip', 'platinum vip', 'diamond vip'].some(k => vipTier.toLowerCase().includes(k));"""

vl = vl.replace(old_check_vip, new_check_vip)

# Show remaining validity days
old_pill_set = """    const pill = document.getElementById('vip-glowing-pill');
    pill.textContent = `👑 ${vipTier.toUpperCase()}`;"""

new_pill_set = """    const pill = document.getElementById('vip-glowing-pill');
    let daysRemainingText = '';
    if (expiresAt > 0) {
      const daysLeft = Math.max(1, Math.ceil((expiresAt - Date.now()) / (24 * 3600 * 1000)));
      daysRemainingText = ` • ⏳ ${daysLeft}D Left`;
    }
    pill.textContent = `👑 ${vipTier.toUpperCase()}${daysRemainingText}`;"""

vl = vl.replace(old_pill_set, new_pill_set)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip-lounge.html", "w", encoding="utf-8") as f:
    f.write(vl)

# 2. Update vip.html to clearly state "/ Month" and "Per Month Membership"
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip.html", "r", encoding="utf-8") as f:
    vhtml = f.read()

# Update hero badge
vhtml = vhtml.replace('👑 Exclusive Membership', '👑 Monthly VIP Membership Pass (30 Days Validity)')
vhtml = vhtml.replace('Choose your tier and start winning bigger.', 'Choose your tier. All VIP memberships are valid for 1 Month (30 Days) with daily ₹150 vault rewards.')

# Update tier cards price text to per month
vhtml = vhtml.replace('<div class="price-amount">₹1,699</div>\n      <div class="price-sub">One-time activation fee</div>', '<div class="price-amount">₹1,699 <span style="font-size:15px;color:#94a3b8;font-weight:600">/ Month</span></div>\n      <div class="price-sub" style="color:#00e676;font-weight:700">📅 Valid for 30 Days (Monthly Plan)</div>')
vhtml = vhtml.replace('<div class="price-amount">₹2,899</div>\n      <div class="price-sub">One-time activation fee</div>', '<div class="price-amount">₹2,899 <span style="font-size:15px;color:#94a3b8;font-weight:600">/ Month</span></div>\n      <div class="price-sub" style="color:#00e676;font-weight:700">📅 Valid for 30 Days (Monthly Plan)</div>')
vhtml = vhtml.replace('<div class="price-amount">₹5,499</div>\n      <div class="price-sub">One-time activation fee</div>', '<div class="price-amount">₹5,499 <span style="font-size:15px;color:#94a3b8;font-weight:600">/ Month</span></div>\n      <div class="price-sub" style="color:#00e676;font-weight:700">📅 Valid for 30 Days (Monthly Plan)</div>')

# Update price display in payment modal
vhtml = vhtml.replace('<div class="pm-subtitle">Secure one-time payment</div>', '<div class="pm-subtitle">📅 1-Month Pass (Valid for 30 Days)</div>')

# Update tierConfig descriptions
old_cfg = """    bronze: {
      icon: '🥉', name: 'Bronze VIP', price: '1,699',
      raw: 1699, upi: 'ggwins@ybl',
      badgeBg: 'rgba(205,127,50,0.15)', payColor: 'linear-gradient(135deg,#cd7f32,#e8976a)', payText: '#fff'
    },
    silver: {
      icon: '🥈', name: 'Silver VIP', price: '2,899',
      raw: 2899, upi: 'ggwins@ybl',
      badgeBg: 'rgba(192,192,192,0.12)', payColor: 'linear-gradient(135deg,#9e9e9e,#d4d4d4)', payText: '#000'
    },
    gold: {
      icon: '👑', name: 'Gold VIP', price: '5,499',
      raw: 5499, upi: 'ggwins@ybl',
      badgeBg: 'rgba(255,190,11,0.15)', payColor: 'linear-gradient(135deg,#ffbe0b,#ffe066)', payText: '#000'
    },"""

new_cfg = """    bronze: {
      icon: '🥉', name: 'Bronze VIP (1 Month)', price: '1,699 / Month',
      raw: 1699, upi: 'ggwins@ybl',
      badgeBg: 'rgba(205,127,50,0.15)', payColor: 'linear-gradient(135deg,#cd7f32,#e8976a)', payText: '#fff'
    },
    silver: {
      icon: '🥈', name: 'Silver VIP (1 Month)', price: '2,899 / Month',
      raw: 2899, upi: 'ggwins@ybl',
      badgeBg: 'rgba(192,192,192,0.12)', payColor: 'linear-gradient(135deg,#9e9e9e,#d4d4d4)', payText: '#000'
    },
    gold: {
      icon: '👑', name: 'Gold VIP (1 Month)', price: '5,499 / Month',
      raw: 5499, upi: 'ggwins@ybl',
      badgeBg: 'rgba(255,190,11,0.15)', payColor: 'linear-gradient(135deg,#ffbe0b,#ffe066)', payText: '#000'
    },"""

vhtml = vhtml.replace(old_cfg, new_cfg)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip.html", "w", encoding="utf-8") as f:
    f.write(vhtml)

# 3. Update server.py approve-vip to stamp 30-day (1-month) expiration
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py", "r", encoding="utf-8") as f:
    s = f.read()

old_approve = """            target["status"] = "Completed"
            target["approvedAt"] = int(time.time() * 1000)

            # Upgrade user's VIP Level in database
            target_user_id = target.get("userId")
            target_username = target.get("username")
            assigned_vip = target.get("tierName", "Gold VIP")"""

new_approve = """            now_ms = int(time.time() * 1000)
            target["status"] = "Completed"
            target["approvedAt"] = now_ms
            # 1-Month (30 Days) Expiration timestamp
            expires_at = now_ms + (30 * 24 * 60 * 60 * 1000)
            target["expiresAt"] = expires_at

            # Upgrade user's VIP Level and Expiration in database
            target_user_id = target.get("userId")
            target_username = target.get("username")
            assigned_vip = target.get("tierName", "Gold VIP").replace(" (1 Month)", "")"""

s = s.replace(old_approve, new_approve)

old_user_upgrade = """            if user_obj:
                user_obj["vipLevel"] = assigned_vip"""

new_user_upgrade = """            if user_obj:
                user_obj["vipLevel"] = assigned_vip
                user_obj["vipExpiresAt"] = expires_at"""

s = s.replace(old_user_upgrade, new_user_upgrade)

# In api/user-status, check for 1-month VIP expiration
old_user_status = """            if target_user:
                self.send_json({"""

new_user_status = """            if target_user:
                # Check 1-Month VIP Expiry
                u_exp = target_user.get("vipExpiresAt", 0)
                if u_exp > 0 and int(time.time() * 1000) > u_exp:
                    target_user["vipLevel"] = "Bronze"
                    target_user["vipExpiresAt"] = 0
                    save_db(db)

                self.send_json({"""

s = s.replace(old_user_status, new_user_status)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: Updated daily vault to 150, set 1-month VIP expiry, and updated VIP pricing to / Month!")
