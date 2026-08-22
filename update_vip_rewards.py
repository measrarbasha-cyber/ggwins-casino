# 1. Update vip-lounge.html
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip-lounge.html", "r", encoding="utf-8") as f:
    vl = f.read()

# Update checkVipAccess in vip-lounge.html to set the dynamic tier daily reward amount
old_check_vip_block = """  if (isVip) {
    lockedGate.style.display = 'none';
    unlockedSuite.style.display = 'flex';
    document.getElementById('vip-player-name').textContent = session ? session.username : 'VIP Member';
    
    const pill = document.getElementById('vip-glowing-pill');
    let daysRemainingText = '';
    if (expiresAt > 0) {
      const daysLeft = Math.max(1, Math.ceil((expiresAt - Date.now()) / (24 * 3600 * 1000)));
      daysRemainingText = ` • ⏳ ${daysLeft}D Left`;
    }
    pill.textContent = `👑 ${vipTier.toUpperCase()}${daysRemainingText}`;
    pill.className = `glowing-vip-badge ${vipTier.toLowerCase().includes('diamond')?'diamond':vipTier.toLowerCase().includes('platinum')?'platinum':'gold'}`;

    if (userBadge) {
      userBadge.innerHTML = `<span class="glowing-vip-badge gold" style="font-size:11px">👑 ${vipTier.toUpperCase()}</span>`;
    }
  }"""

new_check_vip_block = """  if (isVip) {
    lockedGate.style.display = 'none';
    unlockedSuite.style.display = 'flex';
    document.getElementById('vip-player-name').textContent = session ? session.username : 'VIP Member';
    
    const pill = document.getElementById('vip-glowing-pill');
    let daysRemainingText = '';
    if (expiresAt > 0) {
      const daysLeft = Math.max(1, Math.ceil((expiresAt - Date.now()) / (24 * 3600 * 1000)));
      daysRemainingText = ` • ⏳ ${daysLeft}D Left`;
    }
    pill.textContent = `👑 ${vipTier.toUpperCase()}${daysRemainingText}`;
    pill.className = `glowing-vip-badge ${vipTier.toLowerCase().includes('diamond')?'diamond':vipTier.toLowerCase().includes('platinum')?'platinum':vipTier.toLowerCase().includes('silver')?'silver':'gold'}`;

    if (userBadge) {
      userBadge.innerHTML = `<span class="glowing-vip-badge gold" style="font-size:11px">👑 ${vipTier.toUpperCase()}</span>`;
    }

    // Dynamic daily vault reward per tier: Bronze = 35, Silver = 60, Gold = 150
    const dailyRewardAmt = getDailyRewardAmount(vipTier);
    const vaultDesc = document.getElementById('vip-vault-desc');
    const claimBtn = document.getElementById('btn-claim-vault');
    if (vaultDesc) vaultDesc.textContent = `Claim your exclusive VIP daily free reward (₹${dailyRewardAmt} INR for ${vipTier}). Refreshes every 24 hours (Monthly VIP Benefit).`;
    if (claimBtn && !claimBtn.disabled) claimBtn.textContent = `⚡ Claim ₹${dailyRewardAmt} Daily Vault`;
  }"""

vl = vl.replace(old_check_vip_block, new_check_vip_block)

# Update the HTML elements for vault card in vip-lounge.html
old_vault_card = """    <!-- Daily VIP Vault Card -->
    <div class="vip-vault-card">
      <div style="display:flex;align-items:center;gap:14px">
        <div style="font-size:42px">🎁</div>
        <div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:900;color:#f8fafc">Daily VIP Cashback Vault</div>
          <div style="font-size:12.5px;color:#cbd5e1">Claim your exclusive VIP daily free reward (₹150 INR). Refreshes every 24 hours (Monthly VIP Benefit).</div>
        </div>
      </div>
      <button class="btn-vault-claim" id="btn-claim-vault" onclick="claimDailyVipReward()">
        ⚡ Claim ₹150 Daily Vault
      </button>
    </div>"""

new_vault_card = """    <!-- Daily VIP Vault Card -->
    <div class="vip-vault-card">
      <div style="display:flex;align-items:center;gap:14px">
        <div style="font-size:42px">🎁</div>
        <div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:900;color:#f8fafc">Daily VIP Cashback Vault</div>
          <div style="font-size:12.5px;color:#cbd5e1" id="vip-vault-desc">Claim your exclusive VIP daily free reward (₹35 Bronze / ₹60 Silver / ₹150 Gold). Refreshes every 24 hours.</div>
        </div>
      </div>
      <button class="btn-vault-claim" id="btn-claim-vault" onclick="claimDailyVipReward()">
        ⚡ Claim Daily Vault
      </button>
    </div>"""

vl = vl.replace(old_vault_card, new_vault_card)

# Update claimDailyVipReward function
old_claim_func = """// Claim Daily VIP Vault Reward
function claimDailyVipReward() {
  const lastClaim = parseInt(localStorage.getItem('ggwins_vip_vault_last') || '0');
  const now = Date.now();
  const dayMs = 24 * 60 * 60 * 1000;

  if (now - lastClaim < dayMs) {
    const remainingH = Math.ceil((dayMs - (now - lastClaim)) / 3600000);
    alert(`⏳ Daily VIP Vault already claimed today! Please come back in ${remainingH} hours.`);
    return;
  }

  const wallets = getWallets();
  wallets.real = (parseFloat(wallets.real) || 0) + 150.00;
  saveWallets(wallets);
  localStorage.setItem('ggwins_vip_vault_last', now.toString());

  addTransaction({
    id: 'VAULT-' + Math.floor(100000 + Math.random() * 900000),
    orderId: 'VIP-REWARD-' + Math.floor(100000 + Math.random() * 900000),
    type: 'deposit',
    wallet: 'real',
    amount: 150.00,
    currency: 'INR',
    method: 'Daily VIP Cashback Vault (₹150)',
    status: 'Completed',
    timestamp: now
  });

  const btn = document.getElementById('btn-claim-vault');
  btn.textContent = '✅ ₹150 Claimed Today!';
  btn.style.background = '#475569';
  btn.style.color = '#fff';
  btn.disabled = true;

  if (typeof showToast === 'function') {
    showToast('🎉 ₹150 Daily VIP Vault reward added to your balance!', 'success');
  }
}"""

new_claim_func = """function getDailyRewardAmount(tier) {
  const t = (tier || '').toLowerCase();
  if (t.includes('gold')) return 150.00;
  if (t.includes('silver')) return 60.00;
  if (t.includes('bronze')) return 35.00;
  if (t.includes('platinum')) return 300.00;
  if (t.includes('diamond')) return 500.00;
  return 35.00;
}

// Claim Daily VIP Vault Reward (Tier Specific: Bronze ₹35, Silver ₹60, Gold ₹150)
function claimDailyVipReward() {
  const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
  const vipTier = localStorage.getItem('ggwins_vip_level') || session.vipLevel || 'Bronze';
  const rewardAmt = getDailyRewardAmount(vipTier);

  const lastClaim = parseInt(localStorage.getItem('ggwins_vip_vault_last') || '0');
  const now = Date.now();
  const dayMs = 24 * 60 * 60 * 1000;

  if (now - lastClaim < dayMs) {
    const remainingH = Math.ceil((dayMs - (now - lastClaim)) / 3600000);
    alert(`⏳ Daily VIP Vault already claimed today! Please come back in ${remainingH} hours.`);
    return;
  }

  const wallets = getWallets();
  wallets.real = (parseFloat(wallets.real) || 0) + rewardAmt;
  saveWallets(wallets);
  localStorage.setItem('ggwins_vip_vault_last', now.toString());

  addTransaction({
    id: 'VAULT-' + Math.floor(100000 + Math.random() * 900000),
    orderId: 'VIP-REWARD-' + Math.floor(100000 + Math.random() * 900000),
    type: 'deposit',
    wallet: 'real',
    amount: rewardAmt,
    currency: 'INR',
    method: `Daily VIP Cashback Vault (₹${rewardAmt.toFixed(2)} - ${vipTier})`,
    status: 'Completed',
    timestamp: now
  });

  const btn = document.getElementById('btn-claim-vault');
  btn.textContent = `✅ ₹${rewardAmt.toFixed(2)} Claimed Today!`;
  btn.style.background = '#475569';
  btn.style.color = '#fff';
  btn.disabled = true;

  if (typeof showToast === 'function') {
    showToast(`🎉 ₹${rewardAmt.toFixed(2)} Daily ${vipTier} Vault reward added to your balance!`, 'success');
  }
}"""

vl = vl.replace(old_claim_func, new_claim_func)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip-lounge.html", "w", encoding="utf-8") as f:
    f.write(vl)

# 2. Update vip.html perk lists for Bronze, Silver, Gold
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip.html", "r", encoding="utf-8") as f:
    vhtml = f.read()

# Update Bronze perks
old_bronze_perks = """    <ul class="tier-perks">
      <li><span class="perk-dot"></span> Weekly Bonus Rewards</li>
      <li><span class="perk-dot"></span> Monthly Cashback</li>
      <li><span class="perk-dot"></span> Level-Up Bonus</li>
      <li><span class="perk-dot"></span> Priority Chat Support</li>
      <li><span class="perk-dot"></span> Exclusive Bronze Events</li>
    </ul>"""

new_bronze_perks = """    <ul class="tier-perks">
      <li><span class="perk-dot"></span> 🎁 <strong>₹35 Daily Cash Vault</strong> (₹1,050/mo)</li>
      <li><span class="perk-dot"></span> Weekly Bonus Rewards</li>
      <li><span class="perk-dot"></span> Monthly Cashback</li>
      <li><span class="perk-dot"></span> Priority Chat Support</li>
      <li><span class="perk-dot"></span> VIP Lounge Room Access</li>
    </ul>"""

vhtml = vhtml.replace(old_bronze_perks, new_bronze_perks)

# Update Silver perks
old_silver_perks = """    <ul class="tier-perks">
      <li><span class="perk-dot"></span> All Bronze Perks</li>
      <li><span class="perk-dot"></span> Enhanced Bonus Growth</li>
      <li><span class="perk-dot"></span> Rakeback Access (5%)</li>
      <li><span class="perk-dot"></span> Dedicated Account Manager</li>
      <li><span class="perk-dot"></span> Silver-Only Tournaments</li>
    </ul>"""

new_silver_perks = """    <ul class="tier-perks">
      <li><span class="perk-dot"></span> 🎁 <strong>₹60 Daily Cash Vault</strong> (₹1,800/mo)</li>
      <li><span class="perk-dot"></span> All Bronze Perks Included</li>
      <li><span class="perk-dot"></span> Rakeback Access (5%)</li>
      <li><span class="perk-dot"></span> Dedicated Account Manager</li>
      <li><span class="perk-dot"></span> VIP Lounge Room Access</li>
    </ul>"""

vhtml = vhtml.replace(old_silver_perks, new_silver_perks)

# Update Gold perks
old_gold_perks = """    <ul class="tier-perks">
      <li><span class="perk-dot"></span> All Silver Perks</li>
      <li><span class="perk-dot"></span> Personal VIP Host</li>
      <li><span class="perk-dot"></span> Daily Reload Bonuses</li>
      <li><span class="perk-dot"></span> Rakeback Access (10%)</li>
      <li><span class="perk-dot"></span> Exclusive Gold Withdrawals</li>
    </ul>"""

new_gold_perks = """    <ul class="tier-perks">
      <li><span class="perk-dot"></span> 🎁 <strong>₹150 Daily Cash Vault</strong> (₹4,500/mo)</li>
      <li><span class="perk-dot"></span> All Silver Perks Included</li>
      <li><span class="perk-dot"></span> Personal 24/7 VIP Host</li>
      <li><span class="perk-dot"></span> Rakeback Access (10%)</li>
      <li><span class="perk-dot"></span> VIP Lounge & Exclusive Fast Withdrawals</li>
    </ul>"""

vhtml = vhtml.replace(old_gold_perks, new_gold_perks)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip.html", "w", encoding="utf-8") as f:
    f.write(vhtml)

print("SUCCESS: Configured tier-specific daily rewards (Bronze: 35, Silver: 60, Gold: 150)!")
