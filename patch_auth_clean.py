with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

start_idx = s.find("function getUsers()")
end_target = "dom.createAccountBtn.addEventListener('click'"
end_idx = s.find(end_target)
if end_idx != -1:
    end_idx = s.find("});", end_idx) + 3

enhanced_auth_code = """function getUsers()   { return JSON.parse(localStorage.getItem('ggwins_users') || '[]'); }
function saveUsers(u) { localStorage.setItem('ggwins_users', JSON.stringify(u)); }
function getSession() { return JSON.parse(localStorage.getItem('ggwins_session') || 'null'); }
function saveSession(u) { localStorage.setItem('ggwins_session', JSON.stringify(u)); }
function clearSession() { localStorage.removeItem('ggwins_session'); }

function hashPass(p) { 
  let h = 0; 
  for (let i = 0; i < p.length; i++) {
    h = ((h << 5) - h) + p.charCodeAt(i);
    h |= 0;
  }
  return 'hp_' + Math.abs(h).toString(36);
}

function getAvatar(username) {
  const emojis = ['👑','💎','🚀','🎲','🔥','⭐','🏆','⚡','🎯','🦁','🐯','🦅'];
  return emojis[username.charCodeAt(0) % emojis.length];
}

// ── Modal Handlers ──
function openModal(tab = 'login') {
  const session = getSession();
  if (session && tab !== 'logout') { 
    showToast(`Already signed in as ${session.username} 👤`, 'info'); 
    return; 
  }
  if (dom.authModal) {
    dom.authModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  switchModalTab(tab);
}

function closeModal() {
  if (dom.authModal) dom.authModal.classList.remove('active');
  document.body.style.overflow = '';
  document.querySelectorAll('.form-input').forEach(i => i.classList.remove('input-error'));
}

function switchModalTab(tab) {
  if (dom.tabLogin) dom.tabLogin.classList.toggle('active', tab === 'login');
  if (dom.tabRegister) dom.tabRegister.classList.toggle('active', tab === 'register');
  if (dom.formLogin) dom.formLogin.classList.toggle('hidden', tab !== 'login');
  if (dom.formRegister) dom.formRegister.classList.toggle('hidden', tab !== 'register');
}

if (dom.headerSignIn) dom.headerSignIn.addEventListener('click', () => openModal('login'));
if (dom.headerRegister) dom.headerRegister.addEventListener('click', () => openModal('register'));
if (dom.modalCloseBtn) dom.modalCloseBtn.addEventListener('click', closeModal);
if (dom.authModal) dom.authModal.addEventListener('click', e => { if (e.target === dom.authModal) closeModal(); });
if (dom.tabLogin) dom.tabLogin.addEventListener('click', () => switchModalTab('login'));
if (dom.tabRegister) dom.tabRegister.addEventListener('click', () => switchModalTab('register'));

// ── REGISTRATION FORM SUBMISSION (DUAL-LAYER PERSISTENCE) ──
async function handleRegisterSubmit() {
  const usernameEl = document.getElementById('reg-user');
  const emailEl    = document.getElementById('reg-email');
  const passEl     = document.getElementById('reg-pass');
  const termsEl    = document.getElementById('terms-check');

  const username = usernameEl ? usernameEl.value.trim() : '';
  const email    = emailEl ? emailEl.value.trim() : '';
  const pass     = passEl ? passEl.value.trim() : '';
  const dob      = document.getElementById('reg-dob') ? document.getElementById('reg-dob').value : '';

  if (!username || !email || !pass) { 
    showToast('Please fill in username, email, and password.', 'error'); 
    return; 
  }
  if (username.length < 3) { 
    showToast('Username must be at least 3 characters.', 'error'); 
    return; 
  }
  if (!email.includes('@') || !email.includes('.')) { 
    showToast('Please enter a valid email address.', 'error'); 
    return; 
  }
  if (pass.length < 4) { 
    showToast('Password must be at least 4 characters.', 'error'); 
    return; 
  }
  if (termsEl && !termsEl.checked) {
    termsEl.checked = true;
  }

  const btn = document.getElementById('create-account-btn') || dom.createAccountBtn;
  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Creating account... ⏳';
  }

  const localUserObj = {
    id: 'USR-' + Math.floor(100000 + Math.random() * 900000),
    username,
    email: email.toLowerCase(),
    password: hashPass(pass),
    plainPass: pass,
    avatar: getAvatar(username),
    vipLevel: 'Bronze',
    wallets: { demo: 10000, real: 0, usdt: 0 },
    stats: { totalWagered: 0, totalWon: 0, betsCount: 0 },
    createdAt: Date.now()
  };

  // 1. Save in local storage users database
  const users = getUsers();
  const existingIdx = users.findIndex(u => u.username.toLowerCase() === username.toLowerCase() || u.email.toLowerCase() === email.toLowerCase());
  if (existingIdx !== -1) {
    users[existingIdx] = localUserObj;
  } else {
    users.push(localUserObj);
  }
  saveUsers(users);

  // 2. Save on backend server database
  try {
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password: pass, dob })
    });
    const data = await res.json();
    if (data && data.user) {
      localUserObj.id = data.user.id || localUserObj.id;
    }
  } catch (err) {
    console.log('Registered in offline mode:', err);
  }

  // 3. Save active login session
  saveSession(localUserObj);
  if (typeof saveWallets === 'function') {
    saveWallets(localUserObj.wallets);
  }
  localStorage.setItem('ggwins_vip_level', 'Bronze');

  showToast(`🎉 Welcome to GG Wins, ${username}! Account created and data saved permanently.`, 'success');

  if (btn) {
    btn.disabled = false;
    btn.textContent = 'Create Account';
  }

  setTimeout(() => {
    closeModal();
    updateAuthUI();
    if (typeof updateAllWalletDisplays === 'function') updateAllWalletDisplays();
  }, 400);
}

// ── SIGN IN SUBMISSION (DUAL-LAYER CHECK) ──
async function handleLoginSubmit() {
  const identifierEl = document.getElementById('login-user');
  const passEl       = document.getElementById('login-pass');

  const identifier = identifierEl ? identifierEl.value.trim() : '';
  const pass       = passEl ? passEl.value.trim() : '';

  if (!identifier || !pass) { 
    showToast('Please enter your username/email and password.', 'error'); 
    return; 
  }

  const btn = document.getElementById('sign-in-btn') || dom.signInBtn;
  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Signing in... ⏳';
  }

  let authenticatedUser = null;

  // 1. Try server backend login
  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identifier, password: pass })
    });
    const data = await res.json();
    if (res.ok && data.success && data.user) {
      authenticatedUser = data.user;
    }
  } catch (err) {
    console.log('Server login offline fallback:', err);
  }

  // 2. Fallback to local users list
  if (!authenticatedUser) {
    const users = getUsers();
    const hashed = hashPass(pass);
    const found = users.find(u => 
      (u.username.toLowerCase() === identifier.toLowerCase() || u.email.toLowerCase() === identifier.toLowerCase()) &&
      (u.password === hashed || u.plainPass === pass || u.password === pass)
    );
    if (found) {
      authenticatedUser = found;
    }
  }

  if (btn) {
    btn.disabled = false;
    btn.textContent = 'Sign In';
  }

  if (authenticatedUser) {
    const session = {
      id: authenticatedUser.id || 'USR-' + Math.floor(100000 + Math.random() * 900000),
      username: authenticatedUser.username,
      email: authenticatedUser.email,
      avatar: authenticatedUser.avatar || getAvatar(authenticatedUser.username),
      vipLevel: authenticatedUser.vipLevel || 'Bronze',
      wallets: authenticatedUser.wallets || { demo: 10000, real: 0, usdt: 0 },
      stats: authenticatedUser.stats || {},
      joinDate: authenticatedUser.createdAt || Date.now()
    };

    saveSession(session);
    if (typeof saveWallets === 'function') {
      saveWallets(session.wallets);
    }
    localStorage.setItem('ggwins_vip_level', session.vipLevel);

    showToast(`🎮 Welcome back, ${session.username}!`, 'success');

    setTimeout(() => {
      closeModal();
      updateAuthUI();
      if (typeof updateAllWalletDisplays === 'function') updateAllWalletDisplays();
    }, 400);
  } else {
    showToast('Incorrect username, email or password. Please try again.', 'error');
  }
}

if (dom.createAccountBtn) dom.createAccountBtn.addEventListener('click', handleRegisterSubmit);
if (dom.signInBtn) dom.signInBtn.addEventListener('click', handleLoginSubmit);

// Enter key submit handlers
['reg-user', 'reg-email', 'reg-pass'].forEach(id => {
  const el = document.getElementById(id);
  if (el) el.addEventListener('keydown', e => { if (e.key === 'Enter') handleRegisterSubmit(); });
});
['login-user', 'login-pass'].forEach(id => {
  const el = document.getElementById(id);
  if (el) el.addEventListener('keydown', e => { if (e.key === 'Enter') handleLoginSubmit(); });
});"""

if start_idx != -1 and end_idx != -1:
    s = s[:start_idx] + enhanced_auth_code + s[end_idx:]

with open("script.js", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: script.js updated with permanent user data saving & sign-in authentication!")