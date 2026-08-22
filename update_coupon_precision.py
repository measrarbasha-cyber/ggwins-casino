import re

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "r", encoding="utf-8") as f:
    wjs = f.read()

# 1. Update applyPromoCoupon
old_apply_func = """  window.applyPromoCoupon = function(code, autoAdjustAmount = true) {
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

new_apply_func = """  window.applyPromoCoupon = function(code, autoAdjustAmount = true) {
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

    // Auto-enter money logic:
    // 1. If user amount is below coupon minimum, auto-enter the exact amount mentioned in coupon
    // 2. If user entered above coupon minimum (e.g. 2000, 3500, 5000), keep the higher amount and give scaled bonus accordingly
    const amtInput = document.getElementById('wm-amount-input');
    let curAmt = parseFloat(amtInput ? amtInput.value : 0) || 0;
    const minReq = COUPONS[codeClean].minDeposit;

    if (autoAdjustAmount) {
      if (curAmt < minReq) {
        curAmt = minReq;
        if (amtInput) amtInput.value = minReq;
      }
    }

    appliedCouponCode = codeClean;

    const bonus = COUPONS[codeClean].calcBonus(curAmt);
    const pct = COUPONS[codeClean].getPercent(curAmt);

    if (typeof showToast === 'function') {
      showToast(`🎟️ Coupon ${codeClean} Applied! +₹${bonus.toFixed(2)} (${pct}%) Bonus calculated on ₹${curAmt.toFixed(2)}.`, 'success');
    }

    renderWalletModalContent();
  };

  window.updateLiveBonusPreview = function() {
    const previewEl = document.getElementById('wm-coupon-live-preview');
    if (!previewEl || !appliedCouponCode || !COUPONS[appliedCouponCode]) return;

    const c = COUPONS[appliedCouponCode];
    const amtInput = document.getElementById('wm-amount-input');
    const curAmt = Math.max(0, parseFloat(amtInput ? amtInput.value : 0) || 0);

    const bonusAmt = c.calcBonus(curAmt);
    const totalCredit = curAmt + bonusAmt;
    const targetWager = bonusAmt * 3;
    const pct = c.getPercent(curAmt);

    if (curAmt < c.minDeposit) {
      previewEl.innerHTML = `
        <div style="margin-top:10px;background:rgba(239,68,68,0.1);border:1px solid #ef4444;border-radius:10px;padding:10px">
          <div style="font-size:12px;color:#ef4444;font-weight:700">⚠️ Minimum deposit of ₹${c.minDeposit} required for coupon ${c.code}.</div>
          <div style="margin-top:4px"><button onclick="setModalAmount(${c.minDeposit})" style="background:#ef4444;color:#fff;border:none;border-radius:6px;padding:4px 8px;font-size:11px;font-weight:700;cursor:pointer">Set to ₹${c.minDeposit}</button></div>
        </div>
      `;
      return;
    }

    previewEl.innerHTML = `
      <div style="margin-top:10px;background:rgba(0,230,118,0.1);border:1px solid #00e676;border-radius:10px;padding:10px;animation:modalSlideUp 0.2s ease">
        <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
          <span style="color:#94a3b8">Base Deposit:</span>
          <span style="font-weight:700;color:#fff">₹${curAmt.toFixed(2)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
          <span style="color:#00e676;font-weight:700">Coupon Bonus (${c.code}):</span>
          <span style="font-weight:900;color:#00e676">+₹${bonusAmt.toFixed(2)} (${pct}%)</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:13px;border-top:1px dashed rgba(255,255,255,0.2);padding-top:4px;margin-top:4px">
          <span style="color:#ffd700;font-weight:800">Total Credited Balance:</span>
          <span style="font-weight:900;color:#ffd700">₹${totalCredit.toFixed(2)}</span>
        </div>
        <div style="margin-top:8px;font-size:11px;color:#94a3b8;background:rgba(0,0,0,0.3);border-radius:6px;padding:6px 8px;line-height:1.4">
          🎯 <strong>3× Bonus Task Rule:</strong> You must wager/earn <strong>3× the bonus amount (₹${targetWager.toFixed(2)})</strong> across games before bonus withdrawal is unlocked.
        </div>
      </div>
    `;
  };"""

wjs = wjs.replace(old_apply_func, new_apply_func)

# 2. Update setModalAmount to trigger updateLiveBonusPreview()
old_set_amount = """  window.setModalAmount = function(val) {
    const input = document.getElementById('wm-amount-input');
    if (input) input.value = val;
  };"""

new_set_amount = """  window.setModalAmount = function(val) {
    const input = document.getElementById('wm-amount-input');
    if (input) {
      input.value = val;
      if (typeof updateLiveBonusPreview === 'function') {
        updateLiveBonusPreview();
      }
    }
  };"""

wjs = wjs.replace(old_set_amount, new_set_amount)

# 3. Update input box HTML to include oninput="updateLiveBonusPreview()"
wjs = wjs.replace(
    """<input type="number" class="wm-input" id="wm-amount-input" value="${isUsdt ? '100.00' : '1000.00'}" min="${isUsdt ? 10 : 500}" max="${isUsdt ? 5000 : 100000}" step="${isUsdt ? 5 : 100}">""",
    """<input type="number" class="wm-input" id="wm-amount-input" value="${isUsdt ? '100.00' : (appliedCouponCode && COUPONS[appliedCouponCode] ? COUPONS[appliedCouponCode].minDeposit : '1000.00')}" min="${isUsdt ? 10 : 500}" max="${isUsdt ? 5000 : 100000}" step="${isUsdt ? 5 : 100}" oninput="updateLiveBonusPreview()">"""
)

# 4. Wrap bonus preview container with id="wm-coupon-live-preview"
old_preview_block = """            ${appliedCouponCode && COUPONS[appliedCouponCode] ? (function(){
              const c = COUPONS[appliedCouponCode];
              const curAmt = parseFloat(document.getElementById('wm-amount-input')?.value || (c.code==='GG1675'?1675:2500));
              const bonusAmt = c.calcBonus(curAmt);
              const totalCredit = curAmt + bonusAmt;
              const targetWager = bonusAmt * 3;
              return `
                <div style="margin-top:10px;background:rgba(0,230,118,0.1);border:1px solid #00e676;border-radius:10px;padding:10px;animation:modalSlideUp 0.3s ease">
                  <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
                    <span style="color:#94a3b8">Base Deposit:</span>
                    <span style="font-weight:700;color:#fff">₹${curAmt.toFixed(2)}</span>
                  </div>
                  <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
                    <span style="color:#00e676;font-weight:700">Coupon Bonus (${c.code}):</span>
                    <span style="font-weight:900;color:#00e676">+₹${bonusAmt.toFixed(2)} (${c.getPercent(curAmt)}%)</span>
                  </div>
                  <div style="display:flex;justify-content:space-between;font-size:13px;border-top:1px dashed rgba(255,255,255,0.2);padding-top:4px;margin-top:4px">
                    <span style="color:#ffd700;font-weight:800">Total Credited Balance:</span>
                    <span style="font-weight:900;color:#ffd700">₹${totalCredit.toFixed(2)}</span>
                  </div>
                  <div style="margin-top:8px;font-size:11px;color:#94a3b8;background:rgba(0,0,0,0.3);border-radius:6px;padding:6px 8px;line-height:1.4">
                    🎯 <strong>3× Bonus Task Rule:</strong> You must wager/earn <strong>3× the bonus amount (₹${targetWager.toFixed(2)})</strong> across games before bonus withdrawal is unlocked.
                  </div>
                </div>
              `;
            })() : ''}"""

new_preview_block = """            <div id="wm-coupon-live-preview">
              ${appliedCouponCode && COUPONS[appliedCouponCode] ? (function(){
                const c = COUPONS[appliedCouponCode];
                const amtInput = document.getElementById('wm-amount-input');
                const curAmt = parseFloat(amtInput?.value || c.minDeposit);
                const bonusAmt = c.calcBonus(curAmt);
                const totalCredit = curAmt + bonusAmt;
                const targetWager = bonusAmt * 3;
                return `
                  <div style="margin-top:10px;background:rgba(0,230,118,0.1);border:1px solid #00e676;border-radius:10px;padding:10px;animation:modalSlideUp 0.3s ease">
                    <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
                      <span style="color:#94a3b8">Base Deposit:</span>
                      <span style="font-weight:700;color:#fff">₹${curAmt.toFixed(2)}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
                      <span style="color:#00e676;font-weight:700">Coupon Bonus (${c.code}):</span>
                      <span style="font-weight:900;color:#00e676">+₹${bonusAmt.toFixed(2)} (${c.getPercent(curAmt)}%)</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:13px;border-top:1px dashed rgba(255,255,255,0.2);padding-top:4px;margin-top:4px">
                      <span style="color:#ffd700;font-weight:800">Total Credited Balance:</span>
                      <span style="font-weight:900;color:#ffd700">₹${totalCredit.toFixed(2)}</span>
                    </div>
                    <div style="margin-top:8px;font-size:11px;color:#94a3b8;background:rgba(0,0,0,0.3);border-radius:6px;padding:6px 8px;line-height:1.4">
                      🎯 <strong>3× Bonus Task Rule:</strong> You must wager/earn <strong>3× the bonus amount (₹${targetWager.toFixed(2)})</strong> across games before bonus withdrawal is unlocked.
                    </div>
                  </div>
                `;
              })() : ''}
            </div>"""

wjs = wjs.replace(old_preview_block, new_preview_block)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "w", encoding="utf-8") as f:
    f.write(wjs)

print("Updated wallet.js with precise auto-enter on Apply, higher custom amount scaling, and live preview!")
