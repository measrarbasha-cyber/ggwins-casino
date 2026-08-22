# Python script to update wallet.js with promo coupons and 3x bonus wagering engine
import re

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "r", encoding="utf-8") as f:
    content = f.read()

# Let's add coupon helper functions to wallet.js
coupon_logic = '''
  // ── PROMO COUPONS & 3X WAGERING TASK ENGINE ────────────────────
  window.COUPONS = {
    'GG1675': {
      code: 'GG1675',
      name: 'Deposit ₹1675+ (Up to 100% Scaled Bonus)',
      minDeposit: 1675,
      description: 'Deposit ₹1675 to get bonus up to 100%. The more you deposit above ₹1675, the higher deposit bonus you unlock!',
      calcBonus: function(amt) {
        if (amt < 1675) return 0;
        // At 1675 = 50%, scaling smoothly to 100% at 5000+
        const pct = Math.min(100, Math.round(50 + ((amt - 1675) / (5000 - 1675)) * 50));
        return Math.round(amt * (pct / 100) * 100) / 100;
      },
      getPercent: function(amt) {
        if (amt < 1675) return 0;
        return Math.min(100, Math.round(50 + ((amt - 1675) / (5000 - 1675)) * 50));
      }
    },
    'INSTANT1500': {
      code: 'INSTANT1500',
      name: 'Deposit ₹2500 Get Instant ₹1500 Bonus',
      minDeposit: 2500,
      description: 'Deposit ₹2500 to receive instant ₹1500 bonus added to your balance.',
      calcBonus: function(amt) {
        if (amt < 2500) return 0;
        return 1500.00;
      },
      getPercent: function(amt) {
        if (amt < 2500) return 0;
        return Math.round((1500 / amt) * 100);
      }
    }
  };

  let appliedCouponCode = null;

  window.applyPromoCoupon = function(code) {
    const codeClean = (code || '').toUpperCase().trim();
    if (!COUPONS[codeClean]) {
      if (typeof showToast === 'function') showToast('❌ Invalid coupon code', 'error');
      appliedCouponCode = null;
    } else {
      appliedCouponCode = codeClean;
      if (typeof showToast === 'function') showToast(`🎟️ Coupon ${codeClean} Applied!`, 'success');
    }
    renderWalletModalContent();
  };

  window.removePromoCoupon = function() {
    appliedCouponCode = null;
    if (typeof showToast === 'function') showToast('Coupon removed', 'info');
    renderWalletModalContent();
  };

  window.getBonusTask = function() {
    try {
      return JSON.parse(localStorage.getItem('ggwins_bonus_task') || 'null');
    } catch(e) {
      return null;
    }
  };

  window.saveBonusTask = function(task) {
    if (task) {
      localStorage.setItem('ggwins_bonus_task', JSON.stringify(task));
    } else {
      localStorage.removeItem('ggwins_bonus_task');
    }
    window.dispatchEvent(new CustomEvent('bonusTaskUpdated', { detail: task }));
  };
'''

# Insert coupon_logic before createPendingDeposit
if "window.COUPONS" not in content:
    content = content.replace("window.createPendingDeposit =", coupon_logic + "\n  window.createPendingDeposit =")

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected COUPONS engine into wallet.js")
