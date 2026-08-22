# Python script to inject the coupon UI and 3x wagering task UI into wallet.js
import re

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "r", encoding="utf-8") as f:
    wjs = f.read()

# Let's craft the UI snippet for the Active Bonus Task Banner and Promo Coupons section
coupon_ui_snippet = """
          ${!isUsdt ? `
          <!-- ── PROMO COUPONS & BONUS BOX ── -->
          <div style="background:linear-gradient(135deg,rgba(255,215,0,0.08),rgba(0,230,118,0.06));border:1.5px dashed rgba(255,215,0,0.4);border-radius:14px;padding:14px;margin-top:12px">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
              <div style="display:flex;align-items:center;gap:6px;font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:800;color:#ffd700">
                <span>🎟️</span>
                <span>Promo Coupons &amp; Deposit Bonus</span>
              </div>
              <span style="font-size:11px;font-weight:700;color:#00e676;background:rgba(0,230,118,0.15);padding:2px 8px;border-radius:999px">NEW USERS</span>
            </div>

            <!-- Quick Coupon Cards -->
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px">
              <div onclick="setModalAmount(1675); applyPromoCoupon('GG1675')" style="background:rgba(0,0,0,0.3);border:1px solid ${appliedCouponCode==='GG1675'?'#00e676':'rgba(255,255,255,0.15)'};border-radius:10px;padding:8px 10px;cursor:pointer;transition:all 0.2s;box-shadow:${appliedCouponCode==='GG1675'?'0 0 15px rgba(0,230,118,0.3)':''}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;color:#ffd700">GG1675</span>
                  <span style="font-size:10px;font-weight:800;color:#00e676">UP TO 100%</span>
                </div>
                <div style="font-size:11px;color:#94a3b8;margin-top:2px">Deposit ₹1675+ (More you pay = Higher bonus)</div>
              </div>

              <div onclick="setModalAmount(2500); applyPromoCoupon('INSTANT1500')" style="background:rgba(0,0,0,0.3);border:1px solid ${appliedCouponCode==='INSTANT1500'?'#00e676':'rgba(255,255,255,0.15)'};border-radius:10px;padding:8px 10px;cursor:pointer;transition:all 0.2s;box-shadow:${appliedCouponCode==='INSTANT1500'?'0 0 15px rgba(0,230,118,0.3)':''}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;color:#ffd700">INSTANT1500</span>
                  <span style="font-size:10px;font-weight:800;color:#00e676">+₹1500 FLAT</span>
                </div>
                <div style="font-size:11px;color:#94a3b8;margin-top:2px">Deposit ₹2500 to get instant ₹1500 bonus</div>
              </div>
            </div>

            <!-- Coupon Input & Apply -->
            <div style="display:flex;gap:6px">
              <input type="text" id="wm-coupon-input" placeholder="Enter coupon code (e.g. GG1675)" value="${appliedCouponCode||''}" style="flex:1;background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.2);border-radius:8px;padding:8px 12px;color:#fff;font-size:12px;text-transform:uppercase;font-weight:700">
              <button onclick="applyPromoCoupon(document.getElementById('wm-coupon-input').value)" style="background:linear-gradient(135deg,#00e676,#00b0ff);border:none;border-radius:8px;padding:8px 14px;color:#000;font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;cursor:pointer">Apply</button>
              ${appliedCouponCode ? `<button onclick="removePromoCoupon()" style="background:rgba(239,68,68,0.2);border:1px solid #ef4444;border-radius:8px;padding:8px 10px;color:#ef4444;font-size:12px;cursor:pointer">✕</button>` : ''}
            </div>

            ${appliedCouponCode && COUPONS[appliedCouponCode] ? (function(){
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
            })() : ''}
          </div>
          ` : ''}
"""

# Let's also create the Active Bonus Task Widget for Deposit & Withdraw tabs
active_task_banner = """
        ${(function(){
          const task = getBonusTask();
          if (!task) return '';
          const pct = Math.min(100, (task.currentWagered / task.targetWager) * 100).toFixed(1);
          const isDone = task.completed;
          return `
            <div style="background:linear-gradient(135deg,rgba(124,77,255,0.15),rgba(0,230,118,0.1));border:1.5px solid ${isDone?'#00e676':'#ffd700'};border-radius:14px;padding:12px 14px;margin-bottom:12px">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
                <div style="display:flex;align-items:center;gap:6px">
                  <span style="font-size:16px">${isDone?'🎉':'🎯'}</span>
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:12.5px;font-weight:800;color:#fff">
                    ${isDone ? '3× Bonus Task Completed!' : 'Active Bonus Task (3× Wagering Requirement)'}
                  </span>
                </div>
                <span style="font-size:10.5px;font-weight:800;padding:2px 8px;border-radius:999px;background:${isDone?'#00e676':'#ffd700'};color:#000">
                  ${isDone ? '🔓 UNLOCKED' : '🔒 LOCKED'}
                </span>
              </div>
              <div style="font-size:11.5px;color:#94a3b8;margin-bottom:6px">
                Claimed <strong>₹${task.bonusAmt.toFixed(2)} Bonus</strong> (${task.coupon}). Target: Wager/Earn <strong>₹${task.targetWager.toFixed(2)}</strong>.
              </div>
              <!-- Progress Bar -->
              <div style="background:rgba(0,0,0,0.5);border-radius:999px;height:10px;overflow:hidden;position:relative;margin-bottom:4px">
                <div style="background:linear-gradient(90deg,#ffd700,#00e676);height:100%;width:${pct}%;transition:width 0.4s ease"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:11px;color:#cbd5e1;font-weight:700">
                <span>Progress: ₹${task.currentWagered.toFixed(2)} / ₹${task.targetWager.toFixed(2)}</span>
                <span style="color:${isDone?'#00e676':'#ffd700'}">${pct}% ${isDone?'✓ Completed':'Remaining'}</span>
              </div>
            </div>
          `;
        })()}
"""

# Insert active_task_banner in Deposit tab right above Account Pills
wjs = wjs.replace(
    '<div>\n          <div class="wm-section-label">\n            <span>1. Choose Account to Deposit Into</span>',
    active_task_banner + '\n        <div>\n          <div class="wm-section-label">\n            <span>1. Choose Account to Deposit Into</span>'
)

# Insert active_task_banner in Withdraw tab right above Account Pills
wjs = wjs.replace(
    '<div>\n          <div class="wm-section-label">\n            <span>1. Select Account to Withdraw From</span>',
    active_task_banner + '\n        <div>\n          <div class="wm-section-label">\n            <span>1. Select Account to Withdraw From</span>'
)

# Insert coupon_ui_snippet right above the Name & UTR inputs in Deposit tab
wjs = wjs.replace(
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">\n            <div class="wm-input-group">\n              <label class="wm-input-label">Your Name</label>',
    coupon_ui_snippet + '\n          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">\n            <div class="wm-input-group">\n              <label class="wm-input-label">Your Name</label>'
)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "w", encoding="utf-8") as f:
    f.write(wjs)

print("Injected Coupon UI and 3x Bonus Task widgets into wallet.js")
