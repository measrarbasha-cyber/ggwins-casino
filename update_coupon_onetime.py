import re

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "r", encoding="utf-8") as f:
    wjs = f.read()

# 1. Update coupon helper functions
old_coupon_block = """  window.getBonusTask = function() {
    try {
      return JSON.parse(localStorage.getItem('ggwins_bonus_task') || 'null');
    } catch(e) {
      return null;
    }
  };"""

new_coupon_helpers = """  // ── ONE-TIME COUPON TRACKING ──
  window.getUsedCoupons = function() {
    try {
      return JSON.parse(localStorage.getItem('ggwins_used_coupons') || '[]');
    } catch(e) {
      return [];
    }
  };

  window.isCouponUsed = function(code) {
    const list = getUsedCoupons();
    return list.includes((code || '').toUpperCase().trim());
  };

  window.markCouponUsed = function(code) {
    const list = getUsedCoupons();
    const c = (code || '').toUpperCase().trim();
    if (!list.includes(c)) {
      list.push(c);
      localStorage.setItem('ggwins_used_coupons', JSON.stringify(list));
    }
  };

  window.restoreCoupon = function(code) {
    let list = getUsedCoupons();
    const c = (code || '').toUpperCase().trim();
    list = list.filter(item => item !== c);
    localStorage.setItem('ggwins_used_coupons', JSON.stringify(list));
  };

  window.getBonusTask = function() {
    try {
      return JSON.parse(localStorage.getItem('ggwins_bonus_task') || 'null');
    } catch(e) {
      return null;
    }
  };"""

if old_coupon_block in wjs and "window.getUsedCoupons" not in wjs:
    wjs = wjs.replace(old_coupon_block, new_coupon_helpers)

# 2. Update applyPromoCoupon to enforce one-time use and smart auto-typing rule
old_apply_coupon = """  window.applyPromoCoupon = function(code) {
    const codeClean = (code || '').toUpperCase().trim();
    if (!COUPONS[codeClean]) {
      if (typeof showToast === 'function') showToast('❌ Invalid coupon code', 'error');
      appliedCouponCode = null;
    } else {
      appliedCouponCode = codeClean;
      if (typeof showToast === 'function') showToast(`🎟️ Coupon ${codeClean} Applied!`, 'success');
    }
    renderWalletModalContent();
  };"""

new_apply_coupon = """  window.applyPromoCoupon = function(code, autoAdjustAmount = false) {
    const codeClean = (code || '').toUpperCase().trim();
    if (!COUPONS[codeClean]) {
      if (typeof showToast === 'function') showToast('❌ Invalid coupon code', 'error');
      appliedCouponCode = null;
      renderWalletModalContent();
      return;
    }

    if (isCouponUsed(codeClean)) {
      if (typeof showToast === 'function') {
        showToast(`⚠️ Coupon ${codeClean} is already used. Each coupon is one-time use only.`, 'warning');
      }
      appliedCouponCode = null;
      renderWalletModalContent();
      return;
    }

    // Auto-type logic:
    // If user clicks coupon card and current amount is below minDeposit, auto-type minDeposit (e.g. 1675 or 2500)
    // If current amount is already above minDeposit, DO NOT overwrite it!
    if (autoAdjustAmount) {
      const amtInput = document.getElementById('wm-amount-input');
      const curAmt = parseFloat(amtInput ? amtInput.value : 0) || 0;
      const minReq = COUPONS[codeClean].minDeposit;
      if (curAmt < minReq) {
        setModalAmount(minReq);
      }
    }

    appliedCouponCode = codeClean;
    if (typeof showToast === 'function') showToast(`🎟️ Coupon ${codeClean} Applied!`, 'success');
    renderWalletModalContent();
  };"""

if old_apply_coupon in wjs:
    wjs = wjs.replace(old_apply_coupon, new_apply_coupon)

# 3. Update cancelBonusTask to restore the coupon
old_cancel_save = """    // Remove active bonus task
    saveBonusTask(null);"""

new_cancel_save = """    // Restore the coupon so user can use it again
    if (task.coupon) {
      restoreCoupon(task.coupon);
    }

    // Remove active bonus task
    saveBonusTask(null);"""

if old_cancel_save in wjs:
    wjs = wjs.replace(old_cancel_save, new_cancel_save)

old_cancel_toast = """    if (typeof showToast === 'function') {
      showToast(`⚠️ Bonus task cancelled. -₹${bonusToDeduct.toFixed(2)} bonus and -₹${penaltyFee.toFixed(2)} (8% fee) deducted. Withdrawals are now 100% unlocked!`, 'warning');
    }"""

new_cancel_toast = """    if (typeof showToast === 'function') {
      showToast(`⚠️ Bonus task cancelled. -₹${bonusToDeduct.toFixed(2)} bonus and -₹${penaltyFee.toFixed(2)} (8% fee) deducted. Coupon [${task.coupon||'BONUS'}] has been restored for you!`, 'warning');
    }"""

if old_cancel_toast in wjs:
    wjs = wjs.replace(old_cancel_toast, new_cancel_toast)

# 4. Update executeModalDeposit to mark coupon as used
old_exec_mark = """        saveBonusTask(task);
      }
    }"""

new_exec_mark = """        saveBonusTask(task);
        markCouponUsed(couponUsed);
      }
    }"""

if old_exec_mark in wjs:
    wjs = wjs.replace(old_exec_mark, new_exec_mark)

# 5. Update the Quick Coupon Cards in HTML to call applyPromoCoupon('...', true) and show used state
old_card_1 = """<div onclick="setModalAmount(1675); applyPromoCoupon('GG1675')" style="background:rgba(0,0,0,0.3);border:1px solid ${appliedCouponCode==='GG1675'?'#00e676':'rgba(255,255,255,0.15)'};border-radius:10px;padding:8px 10px;cursor:pointer;transition:all 0.2s;box-shadow:${appliedCouponCode==='GG1675'?'0 0 15px rgba(0,230,118,0.3)':''}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;color:#ffd700">GG1675</span>
                  <span style="font-size:10px;font-weight:800;color:#00e676">UP TO 100%</span>
                </div>
                <div style="font-size:11px;color:#94a3b8;margin-top:2px">Deposit ₹1675+ (More you pay = Higher bonus)</div>
              </div>"""

new_card_1 = """<div onclick="${isCouponUsed('GG1675') ? \"showToast('⚠️ Coupon GG1675 has already been used on this account.','warning')\" : \"applyPromoCoupon('GG1675', true)\"}" style="background:rgba(0,0,0,0.3);border:1px solid ${isCouponUsed('GG1675')?'rgba(255,255,255,0.08)':appliedCouponCode==='GG1675'?'#00e676':'rgba(255,255,255,0.15)'};border-radius:10px;padding:8px 10px;cursor:${isCouponUsed('GG1675')?'not-allowed':'pointer'};opacity:${isCouponUsed('GG1675')?'0.55':'1'};transition:all 0.2s;box-shadow:${appliedCouponCode==='GG1675'?'0 0 15px rgba(0,230,118,0.3)':''}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;color:${isCouponUsed('GG1675')?'#94a3b8':'#ffd700'}">GG1675</span>
                  <span style="font-size:10px;font-weight:800;color:${isCouponUsed('GG1675')?'#ef4444':'#00e676'}">${isCouponUsed('GG1675')?'USED (1-TIME)':'UP TO 100%'}</span>
                </div>
                <div style="font-size:11px;color:#94a3b8;margin-top:2px">Deposit ₹1675+ (More you pay = Higher bonus)</div>
              </div>"""

old_card_2 = """<div onclick="setModalAmount(2500); applyPromoCoupon('INSTANT1500')" style="background:rgba(0,0,0,0.3);border:1px solid ${appliedCouponCode==='INSTANT1500'?'#00e676':'rgba(255,255,255,0.15)'};border-radius:10px;padding:8px 10px;cursor:pointer;transition:all 0.2s;box-shadow:${appliedCouponCode==='INSTANT1500'?'0 0 15px rgba(0,230,118,0.3)':''}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;color:#ffd700">INSTANT1500</span>
                  <span style="font-size:10px;font-weight:800;color:#00e676">+₹1500 FLAT</span>
                </div>
                <div style="font-size:11px;color:#94a3b8;margin-top:2px">Deposit ₹2500 to get instant ₹1500 bonus</div>
              </div>"""

new_card_2 = """<div onclick="${isCouponUsed('INSTANT1500') ? \"showToast('⚠️ Coupon INSTANT1500 has already been used on this account.','warning')\" : \"applyPromoCoupon('INSTANT1500', true)\"}" style="background:rgba(0,0,0,0.3);border:1px solid ${isCouponUsed('INSTANT1500')?'rgba(255,255,255,0.08)':appliedCouponCode==='INSTANT1500'?'#00e676':'rgba(255,255,255,0.15)'};border-radius:10px;padding:8px 10px;cursor:${isCouponUsed('INSTANT1500')?'not-allowed':'pointer'};opacity:${isCouponUsed('INSTANT1500')?'0.55':'1'};transition:all 0.2s;box-shadow:${appliedCouponCode==='INSTANT1500'?'0 0 15px rgba(0,230,118,0.3)':''}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;color:${isCouponUsed('INSTANT1500')?'#94a3b8':'#ffd700'}">INSTANT1500</span>
                  <span style="font-size:10px;font-weight:800;color:${isCouponUsed('INSTANT1500')?'#ef4444':'#00e676'}">${isCouponUsed('INSTANT1500')?'USED (1-TIME)':'⚡ +₹1500 FLAT'}</span>
                </div>
                <div style="font-size:11px;color:#94a3b8;margin-top:2px">Deposit ₹2500 to get instant ₹1500 bonus</div>
              </div>"""

wjs = wjs.replace(old_card_1, new_card_1)
wjs = wjs.replace(old_card_2, new_card_2)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "w", encoding="utf-8") as f:
    f.write(wjs)

print("Updated one-time coupon usage, auto-typing logic, and coupon restoration on task cancellation.")
