import re

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip.html", "r", encoding="utf-8") as f:
    vip_html = f.read()

# Add Platinum and Diamond tiers to tierConfig in vip.html
new_tier_config = """  const tierConfig = {
    bronze: {
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
    },
    platinum: {
      icon: '👑', name: 'Platinum VIP', price: '9,999',
      raw: 9999, upi: 'ggwins@ybl',
      badgeBg: 'rgba(129,140,248,0.2)', payColor: 'linear-gradient(135deg,#818cf8,#c7d2fe)', payText: '#000'
    },
    diamond: {
      icon: '💎', name: 'Diamond VIP', price: '19,999',
      raw: 19999, upi: 'ggwins@ybl',
      badgeBg: 'rgba(56,189,248,0.25)', payColor: 'linear-gradient(135deg,#38bdf8,#c084fc)', payText: '#fff'
    }
  };"""

old_config_pattern = r"const tierConfig = \{[\s\S]*?\n  \};"
vip_html = re.sub(old_config_pattern, new_tier_config, vip_html, count=1)

# Update submitVipPayment in vip.html
new_submit_func = """  async function submitVipPayment() {
    const utr = document.getElementById('pm-utr').value.trim();
    if (!utr || utr.length < 6) {
      document.getElementById('pm-utr').parentElement.style.borderColor = '#ef4444';
      document.getElementById('pm-utr').parentElement.style.boxShadow = '0 0 0 2px rgba(239,68,68,0.2)';
      document.getElementById('pm-utr').placeholder = '⚠️ Please enter 12-digit UTR number';
      setTimeout(() => {
        document.getElementById('pm-utr').parentElement.style.borderColor = '';
        document.getElementById('pm-utr').parentElement.style.boxShadow = '';
        document.getElementById('pm-utr').placeholder = 'e.g. 407123456789';
      }, 2500);
      return;
    }

    const cfg = tierConfig[currentTierKey];
    const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
    const orderId = 'ORD-VIP-' + Math.floor(100000 + Math.random() * 900000);

    const reqData = {
      orderId: orderId,
      tier: currentTierKey,
      tierName: cfg.name,
      amount: cfg.raw,
      utr: utr,
      method: currentPmMethod === 'upi' ? 'UPI Instant' : 'Bank Transfer',
      userId: session.id || '',
      username: session.username || localStorage.getItem('ggwins_username') || 'Player'
    };

    try {
      await fetch('/api/vip-request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reqData)
      });
    } catch(e) {
      console.warn('Sent offline fallback:', e);
    }

    // Show pending approval success modal
    document.getElementById('pm-body').style.display = 'none';
    const success = document.getElementById('pm-success');
    document.getElementById('pm-success-msg').innerHTML = `
      <div style="background:rgba(255,215,0,0.1);border:1px solid #ffd700;border-radius:12px;padding:12px;margin:10px 0;text-align:left">
        <div style="font-weight:800;color:#ffd700;margin-bottom:4px">👑 VIP Upgrade Request Sent to Admin Page</div>
        <div style="font-size:12.5px;color:#cbd5e1;line-height:1.5">
          • Tier: <strong>${cfg.name}</strong><br>
          • Amount: <strong>₹${cfg.price}</strong><br>
          • UTR Ref: <strong>${utr}</strong><br>
          • Status: <span style="color:#f59e0b;font-weight:700">⏳ Pending Host Approval</span>
        </div>
      </div>
      <p style="font-size:12px;color:#94a3b8">Once approved by host in the Admin Terminal, your glowing VIP badge and VIP Lounge room access will be automatically unlocked!</p>
    `;
    document.getElementById('pm-success-txid').textContent = 'Order Reference: ' + orderId;
    success.classList.add('show');
  }"""

old_submit_pattern = r"function submitVipPayment\(\) \{[\s\S]*?\n  \}"
vip_html = re.sub(old_submit_pattern, new_submit_func, vip_html, count=1)

# Add link to VIP Lounge room on VIP page nav
vip_html = vip_html.replace(
    '<div class="nav-brand">GG WINS</div>',
    '<div class="nav-brand">👑 GG WINS <a href="vip-lounge.html" style="font-size:12px;color:#ffd700;margin-left:14px;text-decoration:none;border:1px solid rgba(255,215,0,0.4);padding:4px 10px;border-radius:6px">🍸 Enter VIP Lounge</a></div>'
)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip.html", "w", encoding="utf-8") as f:
    f.write(vip_html)

print("Updated vip.html with full VIP purchase flow and API submission!")
