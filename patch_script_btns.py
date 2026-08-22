with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

old_block = """['hero-claim-btn','race-join-btn','vip-join-btn'].forEach(id => {
  const el = $(id);
  if (el) el.addEventListener('click', () => {
    if (getSession()) { showToast('You already have an account! ?', 'info'); return; }
    openModal('register');
  });
});"""

new_block = """// Hero buttons redirect properly
const heroClaimBtn = $('hero-claim-btn');
if (heroClaimBtn) {
  heroClaimBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (typeof claimPromoWithCoupon === 'function') claimPromoWithCoupon('GG1675', 1675);
    else if (typeof openWalletModal === 'function') openWalletModal('deposit');
  });
}

const raceJoinBtn = $('race-join-btn');
if (raceJoinBtn) {
  raceJoinBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    window.location.href = 'tournaments.html';
  });
}

const vipJoinBtn = $('vip-join-btn');
if (vipJoinBtn) {
  vipJoinBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    window.location.href = 'vip.html';
  });
}"""

if old_block in s:
    s = s.replace(old_block, new_block)
else:
    import re
    s = re.sub(r"\['hero-claim-btn','race-join-btn','vip-join-btn'\]\.forEach\(.*?\n\}\);\n", new_block + "\n", s, flags=re.DOTALL)

with open("script.js", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: script.js hero button click handlers fixed!")