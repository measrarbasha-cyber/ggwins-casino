with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip.html", "r", encoding="utf-8") as f:
    vhtml = f.read()

# Update openVipPayment function in vip.html
old_open_func = """  function openVipPayment(tierKey, icon, name, price) {"""
new_open_func = """  function openVipPayment(tierKey, icon, name, price) {
    window.location.href = `vip-payment.html?tier=${tierKey}`;
    return;"""

vhtml = vhtml.replace(old_open_func, new_open_func)

# Also update the buttons
vhtml = vhtml.replace(
    """onclick="openVipPayment('bronze','🥉','Bronze VIP','1699')\"""",
    """onclick="window.location.href='vip-payment.html?tier=bronze'\""""
)
vhtml = vhtml.replace(
    """onclick="openVipPayment('silver','🥈','Silver VIP','2899')\"""",
    """onclick="window.location.href='vip-payment.html?tier=silver'\""""
)
vhtml = vhtml.replace(
    """onclick="openVipPayment('gold','👑','Gold VIP','5499')\"""",
    """onclick="window.location.href='vip-payment.html?tier=gold'\""""
)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip.html", "w", encoding="utf-8") as f:
    f.write(vhtml)

print("Updated vip.html to navigate to the separate vip-payment.html tab!")
