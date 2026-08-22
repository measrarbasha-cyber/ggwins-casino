with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip-payment.html", "r", encoding="utf-8") as f:
    vp = f.read()

# Fix CSS to allow perfect vertical scrolling on all screen sizes
old_body_css = """body {
  background: radial-gradient(circle at 50% 10%, #151838 0%, #080914 60%, #030408 100%);
  color: #f8fafc;
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  margin: 0;
  display: flex;
  flex-direction: column;
  user-select: none;
}"""

new_body_css = """html, body {
  min-height: 100%;
  overflow-x: hidden;
  overflow-y: auto !important;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

body {
  background: radial-gradient(circle at 50% 10%, #151838 0%, #080914 60%, #030408 100%);
  color: #f8fafc;
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  margin: 0;
  display: flex;
  flex-direction: column;
  padding-bottom: 80px;
}"""

vp = vp.replace(old_body_css, new_body_css)

# Update UTR input to support Enter key submission
old_utr_input = """          <input type="text" class="form-input" id="checkout-utr" placeholder="e.g. 407123456789" maxlength="16" required>"""
new_utr_input = """          <input type="text" class="form-input" id="checkout-utr" placeholder="e.g. 407123456789" maxlength="24" required onkeydown="if(event.key==='Enter'){event.preventDefault();submitVipCheckout();}">"""

vp = vp.replace(old_utr_input, new_utr_input)

# Update submit button with prominent text and Enter keyboard hint
old_submit_btn = """      <button type="button" class="btn-submit-checkout" id="btn-submit-vip" onclick="submitVipCheckout()">
        ⚡ Submit VIP Membership Request (<span id="btn-price-label">₹5,499</span>)
      </button>"""

new_submit_btn = """      <button type="button" class="btn-submit-checkout" id="btn-submit-vip" onclick="submitVipCheckout()">
        ⚡ Submit VIP Membership Request (<span id="btn-price-label">₹5,499</span>) ↵ [Press Enter]
      </button>
      <div style="text-align:center;font-size:11.5px;color:#94a3b8;margin-top:10px">
        🔒 Payment is safely verified by Host. Badge &amp; VIP Lounge unlock automatically once approved.
      </div>"""

vp = vp.replace(old_submit_btn, new_submit_btn)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip-payment.html", "w", encoding="utf-8") as f:
    f.write(vp)

print("Updated vip-payment.html: Enabled full page scrolling, Enter key submission, and verified Admin approval requirement!")
