with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "r", encoding="utf-8") as f:
    wjs = f.read()

# Update applyPromoCoupon definition default parameter to true
wjs = wjs.replace(
    "window.applyPromoCoupon = function(code, autoAdjustAmount = false) {",
    "window.applyPromoCoupon = function(code, autoAdjustAmount = true) {"
)

# Update the Apply button onclick to pass true explicitly
wjs = wjs.replace(
    """<button onclick="applyPromoCoupon(document.getElementById('wm-coupon-input').value)" style="background:linear-gradient(135deg,#00e676,#00b0ff);border:none;border-radius:8px;padding:8px 14px;color:#000;font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;cursor:pointer">Apply</button>""",
    """<button onclick="applyPromoCoupon(document.getElementById('wm-coupon-input').value, true)" style="background:linear-gradient(135deg,#00e676,#00b0ff);border:none;border-radius:8px;padding:8px 14px;color:#000;font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;cursor:pointer">Apply</button>"""
)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "w", encoding="utf-8") as f:
    f.write(wjs)

print("Updated applyPromoCoupon in wallet.js to auto-type minimum deposit amount when clicking Apply!")
