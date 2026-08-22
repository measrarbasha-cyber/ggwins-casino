/* =============================================
   GG WINS — INTERACTIVE JAVASCRIPT
   ============================================= */

'use strict';

// ─── GAME DATA ───────────────────────────────────────────────
// ─── WALLET (delegates to centralized wallet.js multi-account system) ──
function refreshLobbyBalance() {
  if (typeof updateAllWalletDisplays === 'function') {
    updateAllWalletDisplays();
  } else {
    const bal = formatCurrency(getBalance());
    const el1 = document.getElementById('lobby-balance-val');
    const el2 = document.getElementById('lobby-balance-val-2');
    if (el1) el1.textContent = bal;
    if (el2) el2.textContent = bal;
  }
  // Also update user dropdown info
  const session = typeof getSession === 'function' ? getSession() : null;
  if (session) {
    const ddUser = document.getElementById('dd-username');
    const ddEmail = document.getElementById('dd-email');
    if (ddUser) ddUser.textContent = session.avatar + ' ' + session.username;
    if (ddEmail) ddEmail.textContent = session.email;
  }
}

const GAMES = [
  // ── 1. GG ORIGINALS ──
  { id: 1,  name: 'GG Crash',          provider: 'GG Originals',  icon: '🚀', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 5821, gameUrl: 'games/crash.html' },
  { id: 2,  name: 'GG Mines',          provider: 'GG Originals',  icon: '💣', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 6420, gameUrl: 'games/mines.html' },
  { id: 3,  name: 'GG Limbo Rocket',   provider: 'GG Originals',  icon: '📈', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 3984, gameUrl: 'games/limbo.html' },
  { id: 4,  name: 'Dragon Tower',      provider: 'GG Originals',  icon: '🐉', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 5120, gameUrl: 'games/dragontower.html' },
  { id: 5,  name: 'GG Diamond Rush',   provider: 'GG Originals',  icon: '💎', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 4920, gameUrl: 'games/diamonds.html' },
  { id: 6,  name: 'GG Fortune Slots',  provider: 'GG Originals',  icon: '🎰', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 5244, gameUrl: 'games/slots.html' },
  { id: 7,  name: 'GG Plinko Drop',    provider: 'GG Originals',  icon: '⚽', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 4891, gameUrl: 'games/plinko.html' },

  // ── 2. CARDS & TABLE GAMES ──
  { id: 8,  name: 'GG Indian Rummy 3D',provider: 'GG Originals',  icon: '🃏', grad: 'grad-table-1',    category: 'table',     badge: 'hot',      players: 7450, gameUrl: 'games/rummy.html' },
  { id: 9,  name: 'GG Baccarat 3D',    provider: 'GG Originals',  icon: '👑', grad: 'grad-table-1',    category: 'table',     badge: 'new',      players: 3870, gameUrl: 'games/baccarat.html' },
  { id: 10, name: 'GG Blackjack 21',   provider: 'GG Originals',  icon: '♣️', grad: 'grad-table-2',    category: 'table',     badge: 'hot',      players: 3980, gameUrl: 'games/blackjack.html' },
  { id: 11, name: 'GG Roulette Royale',provider: 'GG Originals',  icon: '🔴', grad: 'grad-table-1',    category: 'table',     badge: 'hot',      players: 4201, gameUrl: 'games/roulette.html' },
  { id: 12, name: 'GG Sic Bo 3-Dice',  provider: 'GG Originals',  icon: '🎲', grad: 'grad-table-2',    category: 'table',     badge: 'new',      players: 3240, gameUrl: 'games/sicbo.html' },
  { id: 13, name: 'GG Hilo Master',    provider: 'GG Originals',  icon: '🃏', grad: 'grad-table-1',    category: 'table',     badge: 'new',      players: 3410, gameUrl: 'games/hilo.html' },

  // ── 3. CASUAL & ARCADE GAMES ──
  { id: 14, name: 'GG Coin Flip 3D',   provider: 'GG Originals',  icon: '🪙', grad: 'grad-original-1', category: 'arcade',    badge: 'hot',      players: 4890, gameUrl: 'games/coinflip.html' },
  { id: 15, name: 'GG Penalty Shoot',  provider: 'GG Originals',  icon: '⚽', grad: 'grad-original-1', category: 'arcade',    badge: 'hot',      players: 5610, gameUrl: 'games/penalty.html' },
  { id: 16, name: 'GG Magic Shells',   provider: 'GG Originals',  icon: '🪄', grad: 'grad-original-1', category: 'arcade',    badge: 'hot',      players: 6180, gameUrl: 'games/cups.html' },
  { id: 17, name: 'GG Ludo Champions', provider: 'GG Originals',  icon: '🎲', grad: 'grad-original-1', category: 'arcade',    badge: 'hot',      players: 6420, gameUrl: 'games/ludo.html' },
  { id: 18, name: 'GG Dice 3D',        provider: 'GG Originals',  icon: '🎲', grad: 'grad-original-1', category: 'arcade',    badge: 'original', players: 3102, gameUrl: 'games/dice.html' },
  { id: 19, name: 'Wheel of Fortune',  provider: 'GG Originals',  icon: '🎡', grad: 'grad-original-1', category: 'arcade',    badge: 'hot',      players: 4120, gameUrl: 'games/wheel.html' },
  { id: 20, name: 'GG Keno Classic',   provider: 'GG Originals',  icon: '🎱', grad: 'grad-original-1', category: 'arcade',    badge: 'new',      players: 2830, gameUrl: 'games/keno.html' }
];

const PROMOS = [
  { id: 'p1', tag: 'Coupon: GG1675', title: 'Deposit ₹1675+ (Up to 100% Scaled Bonus)', desc: 'Deposit ₹1675 to get bonus up to 100%. The more you deposit above ₹1675, the higher deposit bonus you unlock!', icon: '🎟️', grad: 'promo-grad-1', ctaText: 'Use GG1675', ctaClass: 'btn-primary', couponCode: 'GG1675', depositAmt: 1675 },
  { id: 'p2', tag: 'Coupon: INSTANT1500', title: 'Deposit ₹2500 Get Instant ₹1500 Bonus', desc: 'Deposit ₹2500 to receive instant ₹1500 flat bonus. 3× Wagering task unlocks full withdrawal.', icon: '⚡', grad: 'promo-grad-2', ctaText: 'Use INSTANT1500', ctaClass: 'btn-primary', couponCode: 'INSTANT1500', depositAmt: 2500 },
  { id: 'p3', tag: 'Weekly Race', title: '₹5,00,000 Weekly Race', desc: 'Compete every week for your share of a ₹5,00,000 prize pool. Top 1000 players rewarded.', icon: '🏁', grad: 'promo-grad-3', ctaText: 'Join Now', ctaClass: 'btn-primary' },
  { id: 'p4', tag: 'VIP Rewards', title: 'Exclusive VIP Club & Cashback', desc: 'Unlock daily cashback, dedicated VIP host and tailored high-roller rewards.', icon: '💎', grad: 'promo-grad-4', ctaText: 'Join VIP', ctaClass: 'btn-primary' },
];

const SPORTS_EVENTS = [
  { id: 's1', league: 'Premier League', team1: 'Manchester City', team2: 'Arsenal', time: '45\'', score1: 2, score2: 1, live: true, odds: { h: '1.45', d: '4.20', a: '6.50' } },
  { id: 's2', league: 'NBA', team1: 'LA Lakers', team2: 'Golden State', time: 'Q3 8:24', score1: 78, score2: 82, live: true, odds: { h: '2.10', d: null, a: '1.75' } },
  { id: 's3', league: 'Champions League', team1: 'Real Madrid', team2: 'Bayern Munich', time: 'Tomorrow 21:00', score1: null, score2: null, live: false, odds: { h: '2.20', d: '3.40', a: '3.10' } },
  { id: 's4', league: 'ATP Masters', team1: 'Djokovic N.', team2: 'Alcaraz C.', time: 'Today 18:30', score1: null, score2: null, live: false, odds: { h: '1.85', d: null, a: '1.95' } },
  { id: 's5', league: 'IPL 2025', team1: 'Mumbai Indians', team2: 'Chennai Super Kings', time: 'Overs 28.3', score1: 187, score2: 164, live: true, odds: { h: '1.60', d: null, a: '2.25' } },
  { id: 's6', league: 'CS2 Major', team1: 'NAVI', team2: 'FaZe Clan', time: 'Map 2 - 8:6', score1: null, score2: null, live: true, odds: { h: '1.55', d: null, a: '2.40' } },
];

const CHAT_MESSAGES_SEED = [
  { user: 'CryptoKing99', msg: 'Just hit 247x on Crash! 🚀', badge: 'vip' },
  { user: 'LuckyStrike88', msg: 'GG Wins best platform ever fr fr', badge: null },
  { user: 'ModeratorAlex', msg: 'Welcome everyone! Enjoy today\'s race! 🏁', badge: 'mod' },
  { user: 'DiamondHands', msg: 'Anyone else grinding the weekly race?', badge: 'vip' },
  { user: 'SlotMaster', msg: 'Crazy Time just gave me 10x on the bonus! 🎪', badge: null },
  { user: 'RainMaker', msg: '🌧️ RAIN SENT — 0.005 BTC shared!', badge: 'rain', isRain: true },
  { user: 'ProBettor', msg: 'Lightning Roulette is 🔥 right now', badge: null },
  { user: 'NightOwl247', msg: 'What\'s everyone\'s fav original game?', badge: null },
  { user: 'CoinFlipKing', msg: 'GG Crash + Mines combo = insane session', badge: 'vip' },
  { user: 'FortuneFinder', msg: 'IPL match betting is heating up 🏏', badge: null },
  { user: 'GoldRush', msg: 'VIP support team is always top tier 💯', badge: 'vip' },
  { user: 'SpeedRunner', msg: 'Limbo is the way. Auto bet + patience 📈', badge: null },
];

const TICKER_DATA_POOL = [
  { game: 'GG Crash', icon: '🚀', mult: 247.5, category: 'mega' },
  { game: 'Sweet Bonanza', icon: '🍭', mult: 85.3, category: 'high' },
  { game: 'Lightning Roulette', icon: '⚡', mult: 500, category: 'mega' },
  { game: 'GG Mines', icon: '💣', mult: 12.8, category: 'mid' },
  { game: 'Gates of Olympus', icon: '⚡', mult: 32.5, category: 'mid' },
  { game: 'Crazy Time', icon: '🎪', mult: 100, category: 'mega' },
  { game: 'GG Plinko', icon: '🎯', mult: 4.2, category: 'low' },
  { game: 'Book of Dead', icon: '📖', mult: 7.8, category: 'low' },
  { game: 'Wolf Gold', icon: '🐺', mult: 1843.2, category: 'mega' },
  { game: 'Starburst', icon: '⭐', mult: 2.5, category: 'low' },
  { game: 'GG Dice', icon: '🎲', mult: 15.0, category: 'mid' },
  { game: 'Dream Catcher', icon: '🌈', mult: 40, category: 'high' },
  { game: 'Reactoonz', icon: '👾', mult: 6.2, category: 'low' },
  { game: 'Gonzo\'s Quest', icon: '🏺', mult: 18.4, category: 'mid' },
  { game: 'GG Limbo', icon: '📈', mult: 9999, category: 'mega' },
];

const PLAYER_NAMES = [
  'Shadow***', 'Ninja***', 'Lucky***', 'Crypto***', 'Pro***',
  'Star***', 'Gold***', 'Win***', 'Ace***', 'King***',
  'Fire***', 'Ice***', 'Max***', 'Dark***', 'Blaze***'
];

// ─── STATE ────────────────────────────────────────────────────
let currentSlide = 0;
let slideTimer = null;
let chatMessages = [...CHAT_MESSAGES_SEED];
let tickerRows = [];
let betSlipOpen = false;
let sidebarCollapsed = false;
let activeCategory = 'all';

// ─── DOM REFS ─────────────────────────────────────────────────
const $ = id => document.getElementById(id);

const dom = {
  authModal: $('auth-modal'),
  modalBox: $('modal-box'),
  modalCloseBtn: $('modal-close-btn'),
  tabLogin: $('tab-login'),
  tabRegister: $('tab-register'),
  formLogin: $('form-login'),
  formRegister: $('form-register'),
  headerSignIn: $('header-signin-btn'),
  headerRegister: $('header-register-btn'),
  signInBtn: $('sign-in-btn'),
  createAccountBtn: $('create-account-btn'),
  toast: $('toast'),
  sidebar: $('sidebar'),
  sidebarToggleBtn: $('sidebar-toggle-btn'),
  menuToggleBtn: $('menu-toggle-btn'),
  heroCarousel: $('hero-carousel'),
  prevSlideBtn: $('prev-slide-btn'),
  nextSlideBtn: $('next-slide-btn'),
  carouselDots: $('carousel-dots'),
  topPicksGrid: $('top-picks-grid'),
  trendingGrid: $('trending-grid'),
  newReleasesGrid: $('new-releases-grid'),
  tickerBody: $('ticker-body'),
  promosGrid: $('promos-grid'),
  sportsList: $('sports-list'),
  chatSidebar: $('chat-sidebar'),
  chatToggleBtn: $('chat-toggle-btn'),
  chatCloseBtn: $('chat-close-btn'),
  chatMessages: $('chat-messages'),
  chatInputField: $('chat-input-field'),
  chatSendBtn: $('chat-send-btn'),
  betSlipPanel: $('bet-slip-panel'),
  betSlipCloseBtn: $('bet-slip-close-btn'),
  betCount: $('bet-count'),
  onlineCount: $('online-count'),
  chatOnline: $('chat-online'),
  gameTabs: $('game-tabs'),
  searchInput: $('search-input'),
};

// ─── UTILS ────────────────────────────────────────────────────
function randomBetween(min, max) { return Math.random() * (max - min) + min; }
function randomInt(min, max) { return Math.floor(randomBetween(min, max + 1)); }
function randomPick(arr) { return arr[randomInt(0, arr.length - 1)]; }
function formatCurrency(n) {
  if (n >= 1000) return '₹' + (n / 1000).toFixed(2) + 'K';
  return '₹' + n.toFixed(2);
}
function timeAgo() {
  const secs = randomInt(5, 120);
  if (secs < 60) return secs + 's ago';
  return Math.floor(secs / 60) + 'm ago';
}

// ─── TOAST ───────────────────────────────────────────────────
let toastTimer = null;
function showToast(msg, type = 'info') {
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  dom.toast.innerHTML = `<span>${icons[type]}</span> ${msg}`;
  dom.toast.className = `toast show ${type}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { dom.toast.classList.remove('show'); }, 3000);
}

// ─── AUTH SYSTEM (localStorage persistence) ──────────────────
function getUsers()   { return JSON.parse(localStorage.getItem('ggwins_users') || '[]'); }
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

if (dom.headerSignIn) if (dom.headerSignIn) dom.headerSignIn.addEventListener('click', () => openModal('login'));
if (dom.headerRegister) if (dom.headerRegister) dom.headerRegister.addEventListener('click', () => openModal('register'));
if (dom.modalCloseBtn) if (dom.modalCloseBtn) dom.modalCloseBtn.addEventListener('click', closeModal);
if (dom.authModal) if (dom.authModal) dom.authModal.addEventListener('click', e => { if (e.target === dom.authModal) closeModal(); });
if (dom.tabLogin) if (dom.tabLogin) dom.tabLogin.addEventListener('click', () => switchModalTab('login'));
if (dom.tabRegister) if (dom.tabRegister) dom.tabRegister.addEventListener('click', () => switchModalTab('register'));

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
  const emailRegex = /^[a-zA-Z0-9._%+-]+@(gmail\.com|googlemail\.com|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$/i;
  if (!emailRegex.test(email) || email.length < 6) { 
    showToast('⚠️ Please enter a valid email address associated with a real Google / Gmail account.', 'error'); 
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

  const refCode = (document.getElementById('auth-reg-ref')?.value || localStorage.getItem('ggwins_applied_ref') || '').trim().toUpperCase();

  const localUserObj = {
    id: 'USR-' + Math.floor(100000 + Math.random() * 900000),
    username,
    email: email.toLowerCase(),
    password: hashPass(pass),
    plainPass: pass,
    avatar: getAvatar(username),
    vipLevel: 'None',
    referredBy: refCode || null,
    wallets: { demo: 10000, real: 0, usdt: 0 },
    stats: { totalWagered: 0, totalWon: 0, betsCount: 0, referralEarnings: 0, referralCount: 0 },
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
      body: JSON.stringify({ username, email, password: pass, dob, referralCode: refCode })
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
  localStorage.setItem('ggwins_vip_level', 'None');

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

if (dom.createAccountBtn) if (dom.createAccountBtn) dom.createAccountBtn.addEventListener('click', handleRegisterSubmit);
if (dom.signInBtn) if (dom.signInBtn) dom.signInBtn.addEventListener('click', handleLoginSubmit);

// Enter key submit handlers
['reg-user', 'reg-email', 'reg-pass'].forEach(id => {
  const el = document.getElementById(id);
  if (el) el.addEventListener('keydown', e => { if (e.key === 'Enter') handleRegisterSubmit(); });
});
['login-user', 'login-pass'].forEach(id => {
  const el = document.getElementById(id);
  if (el) el.addEventListener('keydown', e => { if (e.key === 'Enter') handleLoginSubmit(); });
});
    const data = await res.json();

    if (res.ok && data.success && data.user) {
      const u = data.user;
      const session = {
        id: u.id,
        username: u.username,
        email: u.email,
        avatar: u.avatar || getAvatar(u.username),
        vipLevel: u.vipLevel || 'Bronze',
        wallets: u.wallets || { demo: 10000, real: 0, usdt: 0 },
        stats: u.stats || {},
        joinDate: u.createdAt || Date.now()
      };
      saveSession(session);

      // Save initial wallets
      if (u.wallets && typeof saveWallets === 'function') {
        saveWallets(u.wallets);
      }
      localStorage.setItem('ggwins_vip_level', u.vipLevel || 'Bronze');

      showToast(`Welcome to GG Wins, ${u.username}! 🚀 Account created & progress saved permanently.`, 'success');
      setTimeout(() => {
        closeModal();
        updateAuthUI();
        if (typeof updateAllWalletDisplays === 'function') updateAllWalletDisplays();
      }, 500);
    } else {
      showToast(data.message || 'Registration failed. Please try again.', 'error');
    }
  } catch (err) {
    // Fallback local save
    const users = getUsers();
    const newUser = {
      username, email,
      password: hashPass(pass),
      avatar: getAvatar(username),
      joinDate: new Date().toISOString()
    };
    users.push(newUser);
    saveUsers(users);
    saveSession(newUser);
    showToast(`Welcome to GG Wins, ${username}! 🚀 Account created!`, 'success');
    setTimeout(() => { closeModal(); updateAuthUI(); }, 500);
  } finally {
    btn.disabled = false;
    btn.textContent = originalText;
  }
});

// ── Logout ───────────────────────────────────────────────────
window.logoutUser = function() {
  clearSession();
  showToast('You have been signed out. Sign in anytime to resume your progress! 👋', 'info');
  updateAuthUI();
  // Close dropdown if open
  const dd = $('user-dropdown');
  if (dd) dd.style.display = 'none';
};

// ── Update topbar based on auth state ────────────────────────
function updateAuthUI() {
  const session = getSession();
  const signInBtn  = $('header-signin-btn');
  const registerBtn= $('header-register-btn');
  const userPanel  = $('user-panel');
  const walletBtn  = $('wallet-btn');

  if (session) {
    // Logged in
    if (signInBtn)  signInBtn.style.display  = 'none';
    if (registerBtn) registerBtn.style.display = 'none';
    if (walletBtn)  walletBtn.style.display   = 'none';
    if (userPanel) {
      userPanel.style.display = 'flex';
      const av = userPanel.querySelector('#user-avatar-btn');
      const nm = userPanel.querySelector('#user-name-display');
      if (av) av.textContent = session.avatar;
      if (nm) nm.textContent = session.username;

      // Render Glowing VIP Badge & Manage Mini Chat VIP Badge Icon
      const vipTier = localStorage.getItem('ggwins_vip_level') || session.vipLevel || 'Bronze';
      const isVip = ['bronze vip', 'silver', 'gold', 'platinum', 'diamond', 'vip master', 'silver vip', 'gold vip', 'platinum vip', 'diamond vip'].some(k => vipTier.toLowerCase().includes(k) && vipTier.toLowerCase() !== 'bronze');
      
      const chatMiniVip = document.getElementById('vip-chat-mini-badge');
      let badgeEl = userPanel.querySelector('.glowing-vip-badge');

      if (isVip) {
        // User is Approved VIP: Remove mini VIP icon next to chat box
        if (chatMiniVip) chatMiniVip.style.display = 'none';

        // Grant official glowing badge to user
        const tierClass = vipTier.toLowerCase().includes('diamond') ? 'diamond' 
          : vipTier.toLowerCase().includes('platinum') ? 'platinum' 
          : vipTier.toLowerCase().includes('silver') ? 'silver' 
          : vipTier.toLowerCase().includes('bronze') ? 'bronze' 
          : 'gold';

        if (!badgeEl) {
          badgeEl = document.createElement('span');
          userPanel.appendChild(badgeEl);
        }
        badgeEl.className = `glowing-vip-badge ${tierClass}`;
        badgeEl.innerHTML = `👑 ${vipTier.toUpperCase()}`;
        badgeEl.style.display = 'inline-flex';
        badgeEl.style.marginLeft = '6px';
      } else {
        // User is New / Non-VIP: Show small VIP badge icon next to chat box
        if (chatMiniVip) chatMiniVip.style.display = 'inline-flex';
        if (badgeEl) badgeEl.style.display = 'none';
      }
    }
    refreshLobbyBalance();
  } else {
    // Logged out
    if (signInBtn)  signInBtn.style.display  = '';
    if (registerBtn) registerBtn.style.display = '';
    if (walletBtn)  walletBtn.style.display   = '';
    if (userPanel)  userPanel.style.display   = 'none';
  }
}

// Toggle user dropdown
window.toggleUserDropdown = function() {
  const dd = $('user-dropdown');
  if (!dd) return;
  const isOpen = dd.style.display === 'flex';
  dd.style.display = isOpen ? 'none' : 'flex';
  // Populate dropdown info each open
  if (!isOpen) {
    const session = getSession();
    if (session) {
      const ddUser = $('dd-username');
      const ddEmail = $('dd-email');
      if (ddUser) ddUser.textContent = session.avatar + ' ' + session.username;
      if (ddEmail) ddEmail.textContent = session.email;
    }
  }
};
document.addEventListener('click', e => {
  if (!e.target.closest('#user-panel')) {
    const dd = $('user-dropdown');
    if (dd) dd.style.display = 'none';
  }
});

// Hero buttons open modal
// Hero buttons redirect properly
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
}

// Password toggle
window.togglePass = function(inputId, btn) {
  const input = $(inputId);
  const isPass = input.type === 'password';
  input.type = isPass ? 'text' : 'password';
  btn.style.color = isPass ? 'var(--green)' : 'var(--text-muted)';
};

// Wallet btn (opens deposit modal directly)
const walletBtnEl = $('wallet-btn');
if (walletBtnEl) {
  walletBtnEl.addEventListener('click', () => {
    if (typeof openWalletModal === 'function') {
      openWalletModal('deposit');
    } else {
      showToast('Opening Wallet...', 'info');
    }
  });
}

// Initialize auth UI on page load
updateAuthUI();

// ─── SIDEBAR TOGGLE ──────────────────────────────────────────
if (dom.sidebarToggleBtn) dom.sidebarToggleBtn.addEventListener('click', () => {
  sidebarCollapsed = !sidebarCollapsed;
  dom.sidebar.classList.toggle('collapsed', sidebarCollapsed);
});

if (dom.menuToggleBtn) dom.menuToggleBtn.addEventListener('click', () => {
  dom.sidebar.classList.toggle('mobile-open');
});

// Sidebar nav items — allow navigation for real hrefs
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', e => {
    const href = item.getAttribute('href');
    if (!href || href === '#') {
      e.preventDefault();
    }
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    item.classList.add('active');
    // Close mobile sidebar
    if (window.innerWidth <= 860) dom.sidebar.classList.remove('mobile-open');
  });
});

// ─── HERO CAROUSEL (ACCESSIBLE & INTERACTIVE) ─────────────────
const slides = document.querySelectorAll('.hero-slide');
const dots = document.querySelectorAll('.dot');

// ── ENHANCED AUTO-RUNNING HERO CAROUSEL ──
function goToSlide(index) {
  if (!slides || !slides.length) return;
  slides[currentSlide].classList.remove('active');
  if (dots[currentSlide]) dots[currentSlide].classList.remove('active');
  currentSlide = (index + slides.length) % slides.length;
  slides[currentSlide].classList.add('active');
  if (dots[currentSlide]) dots[currentSlide].classList.add('active');
}

function startSlideTimer() {
  clearInterval(slideTimer);
  slideTimer = setInterval(() => {
    goToSlide(currentSlide + 1);
  }, 4500);
}

const heroCarouselEl = document.getElementById('hero-carousel') || document.querySelector('.hero-carousel');
if (heroCarouselEl) {
  heroCarouselEl.addEventListener('mouseenter', () => clearInterval(slideTimer));
  heroCarouselEl.addEventListener('mouseleave', () => startSlideTimer());
}
startSlideTimer(); });
if (dom.prevSlideBtn) if (dom.prevSlideBtn) dom.prevSlideBtn.addEventListener('click', (e) => { e.stopPropagation(); goToSlide(currentSlide - 1); startSlideTimer(); });

dots.forEach((dot, i) => {
  dot.addEventListener('click', (e) => { e.stopPropagation(); goToSlide(i); startSlideTimer(); });
});

// Explicit CTA click listeners
const heroClaimBtn = document.getElementById('hero-claim-btn');
if (heroClaimBtn) heroClaimBtn.addEventListener('click', (e) => { e.stopPropagation(); claimPromoWithCoupon('GG1675', 1675); });

const heroLearnBtn = document.getElementById('hero-learn-btn');
if (heroLearnBtn) heroLearnBtn.addEventListener('click', (e) => { e.stopPropagation(); claimPromoWithCoupon('GG1675', 1675); });

const vipJoinBtn = document.getElementById('vip-join-btn');
if (vipJoinBtn) vipJoinBtn.addEventListener('click', (e) => { e.stopPropagation(); window.location.href = 'vip.html'; });

const vipLearnBtn = document.getElementById('vip-learn-btn');
if (vipLearnBtn) vipLearnBtn.addEventListener('click', (e) => { e.stopPropagation(); window.location.href = 'vip.html'; });

startSlideTimer();

// ─── CANVAS COIN ANIMATION ───────────────────────────────────
const canvas = $('coins-canvas');
if (canvas) {
  const ctx = canvas.getContext('2d');
  const coins = Array.from({ length: 30 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: randomBetween(8, 18),
    vx: randomBetween(-0.8, 0.8),
    vy: randomBetween(-1.5, -0.3),
    alpha: randomBetween(0.4, 1),
    rotation: Math.random() * Math.PI * 2,
    rotSpeed: randomBetween(-0.04, 0.04),
    color: randomPick(['#ffd700', '#00e676', '#ffffff', '#ff6b35']),
  }));

  function drawCoin(coin) {
    ctx.save();
    ctx.globalAlpha = coin.alpha;
    ctx.translate(coin.x, coin.y);
    ctx.rotate(coin.rotation);
    // Coin body
    ctx.beginPath();
    ctx.ellipse(0, 0, coin.r, coin.r * Math.abs(Math.cos(coin.rotation * 2 + performance.now() / 400)), 0, 0, Math.PI * 2);
    ctx.fillStyle = coin.color;
    ctx.fill();
    ctx.strokeStyle = 'rgba(0,0,0,0.2)';
    ctx.lineWidth = 1;
    ctx.stroke();
    // Inner ring
    ctx.beginPath();
    ctx.ellipse(0, 0, coin.r * 0.65, coin.r * 0.65 * Math.abs(Math.cos(coin.rotation * 2 + performance.now() / 400)), 0, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(0,0,0,0.15)';
    ctx.stroke();
    ctx.restore();
  }

  function animateCoins() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    coins.forEach(c => {
      c.x += c.vx;
      c.y += c.vy;
      c.rotation += c.rotSpeed;
      c.vy += 0.015; // gravity
      if (c.y > canvas.height + 20) {
        c.y = -20;
        c.x = Math.random() * canvas.width;
        c.vy = randomBetween(-1.5, -0.5);
      }
      if (c.x < -20) c.x = canvas.width + 20;
      if (c.x > canvas.width + 20) c.x = -20;
      drawCoin(c);
    });
    requestAnimationFrame(animateCoins);
  }
  animateCoins();
}

// ─── RENDER GAME CARDS ───────────────────────────────────────
function launchGame(game) {
  if (game.gameUrl) {
    window.location.href = game.gameUrl;
  } else {
    showToast(`Launching ${game.name}…`, 'info');
  }
}

function createGameCard(game) {
  const badgeHtml = game.badge ? `<span class="game-badge badge-${game.badge}">${game.badge === 'jackpot' ? '💰 JACKPOT' : game.badge === 'hot' ? '🔥 HOT' : game.badge.toUpperCase()}</span>` : '';
  const hasGame = !!game.gameUrl;
  const div = document.createElement('div');
  div.className = 'game-card';
  div.dataset.category = game.category;
  div.innerHTML = `
    <div class="game-thumb ${game.grad || 'grad-original-1'}">
      ${badgeHtml}
      <div class="game-thumb-center">
        <span class="game-icon-bg" style="font-size:42px;display:block;margin-bottom:4px;filter:drop-shadow(0 0 10px rgba(255,215,0,0.4))">${game.icon}</span>
        <div class="game-logo-name" style="font-weight:900">${game.name}</div>
      </div>
      <div class="game-overlay">
        <button class="game-play-btn">▶ Play Now</button>
        <button class="game-demo-btn">${hasGame ? '⚡ Live Game' : 'Play Now'}</button>
      </div>
    </div>
    <div class="game-info">
      <div class="game-name" style="display:flex;align-items:center;gap:6px"><span>${game.icon}</span> ${game.name}</div>
      <div class="game-provider">${game.provider} • 👥 ${(game.players||3200).toLocaleString()} playing</div>
    </div>
  `;
  // Click card body = launch game immediately
  div.addEventListener('click', () => launchGame(game));
  // Play Now button
  const playBtn = div.querySelector('.game-play-btn');
  if (playBtn) {
    playBtn.addEventListener('click', e => {
      e.stopPropagation();
      launchGame(game);
    });
  }
  const demoBtn = div.querySelector('.game-demo-btn');
  if (demoBtn) {
    demoBtn.addEventListener('click', e => {
      e.stopPropagation();
      launchGame(game);
    });
  }
  return div;
}

function renderGames(category = 'all') {
  const origGrid = document.getElementById('originals-grid');
  const tableGrid = document.getElementById('table-grid');
  const arcadeGrid = document.getElementById('arcade-grid');

  if (origGrid) origGrid.innerHTML = '';
  if (tableGrid) tableGrid.innerHTML = '';
  if (arcadeGrid) arcadeGrid.innerHTML = '';

  GAMES.forEach(game => {
    const card = createGameCard(game);
    if (game.category === 'originals' && origGrid) {
      origGrid.appendChild(card);
    } else if (game.category === 'table' && tableGrid) {
      tableGrid.appendChild(card);
    } else if (game.category === 'arcade' && arcadeGrid) {
      arcadeGrid.appendChild(card);
    } else if (origGrid) {
      origGrid.appendChild(card);
    }
  });

  const countLbl = document.getElementById('originals-count-lbl');
  if (countLbl) countLbl.textContent = `${GAMES.filter(g => g.category === 'originals').length} Games`;
}

window.filterGamesSearch = function() {
  const input = document.getElementById('game-search-input');
  const kw = input ? input.value.trim() : '';
  renderGames('all', kw);
};

window.selectCategoryTab = function(cat) {
  const btn = document.querySelector(`.tab-btn[data-category="${cat}"]`);
  if (btn) btn.click();
};

renderGames();

// Category tabs
const gameTabsEl = document.getElementById('game-tabs');
if (gameTabsEl) {
  gameTabsEl.addEventListener('click', e => {
    const btn = e.target.closest('.tab-btn');
    if (!btn) return;
    document.querySelectorAll('.tab-btn').forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected', 'false'); });
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
    activeCategory = btn.dataset.category;
    renderGames(activeCategory);
  });
}

// ─── LIVE WINS TICKER ────────────────────────────────────────
function generateTickerRow(filter = 'all') {
  let data = randomPick(TICKER_DATA_POOL);
  if (filter === 'big') {
    data = TICKER_DATA_POOL.filter(d => d.mult >= 20)[Math.floor(Math.random() * TICKER_DATA_POOL.filter(d => d.mult >= 20).length)];
  } else if (filter === 'jackpot') {
    data = TICKER_DATA_POOL.filter(d => d.mult >= 100)[Math.floor(Math.random() * TICKER_DATA_POOL.filter(d => d.mult >= 100).length)];
  }
  const bet = Math.floor(randomBetween(50, 5000));
  const payout = (bet * data.mult);
  const betFormatted = typeof formatCurrency === 'function' ? formatCurrency(bet) : `₹${bet.toLocaleString('en-IN')}`;
  const payoutFormatted = typeof formatCurrency === 'function' ? formatCurrency(payout) : `₹${payout.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  return { ...data, player: randomPick(PLAYER_NAMES), time: timeAgo(), bet: betFormatted, payout: payoutFormatted };
}

let activeTickerFilter = 'all';

function renderTickerRow(row) {
  const div = document.createElement('div');
  div.className = 'ticker-row';
  div.innerHTML = `
    <span class="ticker-game"><span class="ticker-game-icon">${row.icon}</span>${row.game}</span>
    <span class="ticker-player">${row.player}</span>
    <span class="ticker-time">${row.time}</span>
    <span class="ticker-bet">${row.bet}</span>
    <span class="ticker-mult ${row.category}">${row.mult.toLocaleString()}×</span>
    <span class="ticker-payout">${row.payout}</span>
  `;
  return div;
}

function initTicker() {
  const body = dom.tickerBody;
  body.innerHTML = '';
  // Seed with 8 rows
  for (let i = 0; i < 8; i++) {
    body.appendChild(renderTickerRow(generateTickerRow(activeTickerFilter)));
  }
}
initTicker();

// Add new ticker row periodically
setInterval(() => {
  const body = dom.tickerBody;
  const newRow = renderTickerRow(generateTickerRow(activeTickerFilter));
  body.insertBefore(newRow, body.firstChild);
  if (body.children.length > 20) body.removeChild(body.lastChild);
}, 2200);

// Ticker filters
document.querySelectorAll('.ticker-filter').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.ticker-filter').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeTickerFilter = btn.dataset.filter;
    initTicker();
  });
});

// ─── RENDER PROMOTIONS (Excludes completed/used coupons) ────
function renderPromos() {
  dom.promosGrid.innerHTML = '';
  const isUsed = typeof isCouponUsed === 'function' ? isCouponUsed : function(code) {
    try {
      const list = JSON.parse(localStorage.getItem('ggwins_used_coupons') || '[]');
      return list.includes((code || '').toUpperCase().trim());
    } catch(e) { return false; }
  };

  const visiblePromos = PROMOS.filter(p => !p.couponCode || !isUsed(p.couponCode));

  visiblePromos.forEach(promo => {
    const div = document.createElement('div');
    div.className = 'promo-card';
    div.innerHTML = `
      <div class="promo-visual ${promo.grad}">
        <div class="promo-visual-icon">${promo.icon}</div>
      </div>
      <div class="promo-body">
        <div class="promo-tag" style="color: var(--green)">${promo.tag}</div>
        <div class="promo-title">${promo.title}</div>
        <div class="promo-desc">${promo.desc}</div>
        <button class="promo-cta btn-primary" style="margin-top:12px">${promo.ctaText}</button>
      </div>
    `;
    div.addEventListener('click', () => {
      if (promo.couponCode) {
        claimPromoWithCoupon(promo.couponCode, promo.depositAmt);
      } else {
        openModal('register');
      }
    });
    dom.promosGrid.appendChild(div);
  });
}
renderPromos();

// ─── RENDER SPORTS ───────────────────────────────────────────
function renderSports() {
  dom.sportsList.innerHTML = '';
  SPORTS_EVENTS.forEach(event => {
    const div = document.createElement('div');
    div.className = `sport-event${event.live ? ' live-event' : ''}`;
    const scoreHtml = event.score1 !== null
      ? `<div class="sport-teams-row"><span class="sport-team">${event.team1}</span><span class="sport-score">${event.score1} – ${event.score2}</span></div><div class="sport-time">${event.live ? `<span class="sport-live-tag">LIVE</span> ` : ''}${event.time}</div>`
      : `<div class="sport-teams-row"><span class="sport-team">${event.team1} vs ${event.team2}</span></div><div class="sport-time">${event.time}</div>`;
    const drawOdd = event.odds.d ? `<button class="odds-btn" data-event="${event.id}" data-outcome="draw"><span class="odds-label">Draw</span>${event.odds.d}</button>` : '';
    div.innerHTML = `
      <div class="sport-league">${event.league}</div>
      <div class="sport-teams">${scoreHtml}</div>
      <div class="sport-odds">
        <button class="odds-btn" data-event="${event.id}" data-outcome="home"><span class="odds-label">Home</span>${event.odds.h}</button>
        ${drawOdd}
        <button class="odds-btn" data-event="${event.id}" data-outcome="away"><span class="odds-label">Away</span>${event.odds.a}</button>
      </div>
    `;
    // Odds click
    div.querySelectorAll('.odds-btn').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        btn.classList.toggle('selected');
        updateBetSlip();
        showToast(`${event.team1} odds added to bet slip!`, 'success');
      });
    });
    div.addEventListener('click', () => showToast('Full market available after login.', 'info'));
    dom.sportsList.appendChild(div);
  });
}
renderSports();

// ─── BET SLIP ────────────────────────────────────────────────
function updateBetSlip() {
  const selected = document.querySelectorAll('.odds-btn.selected');
  dom.betCount.textContent = selected.length;
  if (selected.length > 0 && !betSlipOpen) {
    dom.betSlipPanel.classList.add('open');
    betSlipOpen = true;
  } else if (selected.length === 0) {
    dom.betSlipPanel.classList.remove('open');
    betSlipOpen = false;
  }
}
if (dom.betSlipCloseBtn) dom.betSlipCloseBtn.addEventListener('click', () => {
  dom.betSlipPanel.classList.remove('open');
  betSlipOpen = false;
});

// ─── LIVE CHAT ───────────────────────────────────────────────
function renderChatMessage(msg) {
  const div = document.createElement('div');
  if (msg.isRain) {
    div.className = 'rain-msg';
    div.textContent = `🌧️ ${msg.user} sent rain! Everyone gets a share!`;
  } else {
    div.className = 'chat-msg';
    const badgeIcon = msg.badge === 'vip' ? '👑 ' : msg.badge === 'mod' ? '🛡️ ' : msg.badge === 'rain' ? '🌧️ ' : '';
    const userClass = `chat-username${msg.badge ? ` chat-badge-${msg.badge}` : ''}`;
    div.innerHTML = `<div class="${userClass}">${badgeIcon}${msg.user}</div><div class="chat-text">${msg.msg}</div>`;
  }
  return div;
}

function initChat() {
  dom.chatMessages.innerHTML = '';
  chatMessages.forEach(msg => dom.chatMessages.appendChild(renderChatMessage(msg)));
  dom.chatMessages.scrollTop = dom.chatMessages.scrollHeight;
}
initChat();

// Add periodic chat messages
const BOT_MESSAGES = [
  { user: 'WinnerAlert', msg: '🎰 Just won ₹12,400 on Gates of Olympus!', badge: 'vip' },
  { user: 'CrashAddict', msg: 'Cashed out at 31.5x on Crash 💸', badge: null },
  { user: 'ModeratorSara', msg: 'Don\'t forget the weekly race ends in 2 hours!', badge: 'mod' },
  { user: 'LuckyPlayer', msg: 'First time here, already up 3x 🙏', badge: null },
  { user: 'BigBaller', msg: 'GG Wins > all other platforms tbh', badge: 'vip' },
  { user: 'RainBot', msg: '🌧️ RAIN SENT — 0.01 ETH shared among 50 users!', badge: 'rain', isRain: true },
  { user: 'SlotGod', msg: 'Crazy Time bonus round hit 100x 🎪🎪🎪', badge: null },
  { user: 'PlinkoMaster', msg: 'Plinko on 16 pegs = pure chaos 😂', badge: null },
];

let botMsgIndex = 0;
setInterval(() => {
  const msg = BOT_MESSAGES[botMsgIndex % BOT_MESSAGES.length];
  botMsgIndex++;
  const el = renderChatMessage(msg);
  dom.chatMessages.appendChild(el);
  dom.chatMessages.scrollTop = dom.chatMessages.scrollHeight;
  if (dom.chatMessages.children.length > 50) dom.chatMessages.removeChild(dom.chatMessages.firstChild);
}, 4000);

// Send chat message
// ── FULLY AI ANIMATED LIVE CHAT & AUTO-RUNNING FEED ENGINE ──
const AI_RESPONSES = [
  { match: /deposit|recharge|payment|upi|gpay|paytm|add money|qr/i, reply: "💳 Deposits on GG Wins are instant with 0% fee! Tap the 'Deposit & Wallet' button at top to pay via UPI QR (GPay, PhonePe, Paytm). Coupon code GG1675 unlocks up to 100% bonus!" },
  { match: /withdraw|payout|bank|cashout|transfer/i, reply: "⚡ Withdrawals are processed within 5–15 minutes directly to your bank account or UPI ID. Make sure standard 1x turnover on real deposits is completed." },
  { match: /vip|membership|bronze|silver|gold|badge/i, reply: "👑 GG VIP Club gives you daily vault cash (₹35 Bronze / ₹60 Silver / ₹150 Gold) and glowing username badges for 30 days! Visit vip.html to join." },
  { match: /tournament|arena|entry fee|leaderboard/i, reply: "🏆 Arena Tournaments are active across all 20 games! Entry fee is strictly ₹50 deducted from your Real Balance. 1st place wins 60% of the grand prize pool!" },
  { match: /crash|multiplier|plane/i, reply: "🚀 GG Crash: Place your wager before takeoff and cash out before the rocket crashes! Highest multiplier recorded today: 840.50x!" },
  { match: /mines|diamond/i, reply: "💣 GG Mines: Choose 1 to 24 mines on the 5x5 grid. The more diamonds you reveal without hitting a mine, the bigger your multiplier payout!" },
  { match: /rummy|cards|sequence/i, reply: "🃏 Indian Rummy 3D: Form valid pure sequences, sets, and declare your hand before opponents to win the prize table!" },
  { match: /hi|hello|hey|sup|good/i, reply: "👋 Welcome to GG Wins! I'm your AI Casino Support Host. How can I assist your gaming session today?" },
  { match: /win|hack|cheat|fair|provably/i, reply: "🛡️ All GG Wins games operate on certified Provably Fair cryptographic algorithms (SHA-256). Every round hash can be independently verified!" }
];

const AUTO_CHAT_STREAM = [
  { user: 'Vikram_Malhotra', role: 'vip', msg: 'Just cashed out 18.4x on Crash! 🚀 ₹9,200 win!' },
  { user: 'Kunal_Singhania', role: 'vip', msg: 'Hit 8 diamonds in a row in Mines! Diamond grid is on fire 🔥' },
  { user: 'Aarav_Sharma', role: 'vip', msg: 'VIP Bronze daily reward ₹35 credited automatically 👑' },
  { user: 'Priya_Patel', role: 'player', msg: 'Who is playing Indian Rummy table right now? 🃏' },
  { user: 'Rahul_Gupta', role: 'player', msg: 'Deposited via PhonePe and bonus code GG1675 worked instantly! 💳' },
  { user: 'Siddharth_Mehta', role: 'player', msg: 'Rank #2 on Sic Bo tournament leaderboard! 🎲' },
  { user: 'GG_AI_Host', role: 'ai', msg: '🤖 Tip: Claim your daily spin in Wheel of Fortune to unlock bonus vault coins!' },
  { user: 'Dev_Singhal', role: 'vip', msg: 'Blackjack 21 dealer busted 3 times in a row! ♣️' },
  { user: 'Ananya_Sen', role: 'player', msg: 'Penalty shootout top right corner never fails ⚽' },
  { user: 'GG_AI_Host', role: 'ai', msg: '💎 Active Jackpot Pool is currently at ₹4,85,000 across Arena Tournaments!' },
  { user: 'Manish_Pandey', role: 'player', msg: 'Fastest payout ever! Got ₹4,500 withdrawal in 3 mins ⚡' },
  { user: 'Harsh_Vardhan', role: 'vip', msg: 'VIP Gold tier gives 150 daily vault reward everyday! Best perk 👑' }
];

function appendChatMessage(user, msg, role = 'player') {
  const container = document.getElementById('chat-messages') || document.querySelector('.chat-messages');
  if (!container) return;

  const isAi = role === 'ai';
  const isVip = role === 'vip';
  const isUser = role === 'user';

  const msgDiv = document.createElement('div');
  msgDiv.className = `chat-msg ${isAi ? 'chat-msg-ai' : isVip ? 'chat-msg-vip' : isUser ? 'chat-msg-user' : ''}`;
  msgDiv.style.padding = '9px 12px';
  msgDiv.style.borderRadius = '12px';
  msgDiv.style.marginBottom = '8px';
  msgDiv.style.fontSize = '12.5px';
  msgDiv.style.background = isAi 
    ? 'linear-gradient(135deg, rgba(0, 230, 118, 0.12), rgba(0, 176, 255, 0.08))' 
    : isVip 
      ? 'linear-gradient(135deg, rgba(255, 215, 0, 0.12), rgba(255, 140, 0, 0.08))' 
      : isUser 
        ? 'rgba(255, 255, 255, 0.1)' 
        : 'rgba(255, 255, 255, 0.05)';
  msgDiv.style.border = isAi 
    ? '1.5px solid rgba(0, 230, 118, 0.4)' 
    : isVip 
      ? '1.5px solid rgba(255, 215, 0, 0.4)' 
      : isUser 
        ? '1.5px solid rgba(255, 255, 255, 0.2)' 
        : '1px solid rgba(255, 255, 255, 0.08)';

  const headerHtml = isAi 
    ? '<span style="color:#00e676;font-weight:900;display:flex;align-items:center;gap:4px">🤖 GG AI Host <span style="font-size:9px;background:rgba(0,230,118,0.2);padding:1px 5px;border-radius:4px">AI BOT</span></span>' 
    : isVip 
      ? `<span style="color:#ffd700;font-weight:900;display:flex;align-items:center;gap:4px">👑 ${user} <span style="font-size:9px;background:rgba(255,215,0,0.2);padding:1px 5px;border-radius:4px">VIP</span></span>` 
      : isUser 
        ? `<span style="color:#00e676;font-weight:900">👤 ${user} (You)</span>` 
        : `<span style="color:#cbd5e1;font-weight:800">👤 ${user}</span>`;

  msgDiv.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">
      ${headerHtml}
      <span style="font-size:10px;color:#94a3b8">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
    </div>
    <div style="color:#f8fafc;line-height:1.4">${msg}</div>
  `;

  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;

  // Keep max 60 messages in DOM for ultra-smooth performance
  while (container.children.length > 60) {
    container.removeChild(container.firstChild);
  }
}

function showTypingIndicator() {
  const container = document.getElementById('chat-messages') || document.querySelector('.chat-messages');
  if (!container) return null;

  const typingDiv = document.createElement('div');
  typingDiv.id = 'ai-typing-indicator';
  typingDiv.className = 'ai-typing-indicator';
  typingDiv.innerHTML = `
    <span>🤖 GG AI Host is typing</span>
    <span class="typing-dot"></span>
    <span class="typing-dot"></span>
    <span class="typing-dot"></span>
  `;
  container.appendChild(typingDiv);
  container.scrollTop = container.scrollHeight;
  return typingDiv;
}

function removeTypingIndicator() {
  const ind = document.getElementById('ai-typing-indicator');
  if (ind && ind.parentNode) ind.parentNode.removeChild(ind);
}

function sendChatMsg() {
  const inputEl = document.getElementById('chat-input-field') || (dom && dom.chatInputField);
  if (!inputEl) return;
  const userText = inputEl.value.trim();
  if (!userText) return;

  const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
  const userName = session.username || 'You';

  // Append User message
  appendChatMessage(userName, userText, 'user');
  inputEl.value = '';

  // Show animated AI typing indicator
  showTypingIndicator();

  // Process AI Response with animated delay
  setTimeout(() => {
    removeTypingIndicator();
    let reply = "🤖 I'm your 24/7 AI Casino Host! You can ask me about instant deposits, 5-min withdrawals, VIP perks, or game tips.";
    for (const rule of AI_RESPONSES) {
      if (rule.match.test(userText)) {
        reply = rule.reply;
        break;
      }
    }
    appendChatMessage('GG AI Host', reply, 'ai');
  }, 750);
}

// ── AUTO-RUNNING LIVE CHAT STREAM (POSTS ON ITS OWN EVERY 3.5 SECONDS) ──
let chatStreamIdx = 0;
function autoRunChatFeed() {
  const item = AUTO_CHAT_STREAM[chatStreamIdx % AUTO_CHAT_STREAM.length];
  chatStreamIdx++;

  if (item.role === 'ai') {
    showTypingIndicator();
    setTimeout(() => {
      removeTypingIndicator();
      appendChatMessage(item.user, item.msg, 'ai');
    }, 600);
  } else {
    appendChatMessage(item.user, item.msg, item.role);
  }

  // Update live online count smoothly
  const onlineEl = document.getElementById('chat-online');
  if (onlineEl) {
    const base = 240 + Math.floor(Math.sin(Date.now() / 20000) * 25) + Math.floor(Math.random() * 8);
    onlineEl.textContent = base.toString();
  }
}

// Start auto-running on its own!
setInterval(autoRunChatFeed, 3500);
setTimeout(autoRunChatFeed, 1000);
if (dom.chatSendBtn) dom.chatSendBtn.addEventListener('click', sendChatMsg);
if (dom.chatInputField) dom.chatInputField.addEventListener('keydown', e => { if (e.key === 'Enter') sendChatMsg(); });

// Chat toggle
if (dom.chatToggleBtn) dom.chatToggleBtn.addEventListener('click', () => {
  dom.chatSidebar.classList.toggle('hidden-chat');
});
if (dom.chatCloseBtn) dom.chatCloseBtn.addEventListener('click', () => {
  dom.chatSidebar.classList.add('hidden-chat');
});

// Chat room buttons
document.querySelectorAll('.room-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.room-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    if (btn.dataset.room === 'vip-chat') {
      showToast('VIP room requires VIP membership.', 'info');
    }
  });
});

// Rain button
$('rain-btn').addEventListener('click', () => openModal('login'));

// Emoji btn
$('emoji-btn').addEventListener('click', () => {
  const emojis = ['😊', '🚀', '💰', '🎉', '🔥', '💎', '🎲', '🃏', '⚡', '🌈'];
  dom.chatInputField.value += randomPick(emojis);
  dom.chatInputField.focus();
});

// ─── LIVE STATS ANIMATION ────────────────────────────────────
let onlinePlayers = 18432;
setInterval(() => {
  const delta = randomInt(-30, 50);
  onlinePlayers = Math.max(15000, onlinePlayers + delta);
  dom.onlineCount.textContent = onlinePlayers.toLocaleString();
  dom.chatOnline.textContent = randomInt(200, 300);
}, 3000);

// ─── SEARCH ──────────────────────────────────────────────────
if (dom.searchInput) dom.searchInput.addEventListener('input', e => {
  const query = e.target.value.toLowerCase();
  if (!query) { renderGames(activeCategory); return; }
  const filtered = GAMES.filter(g => g.name.toLowerCase().includes(query) || g.provider.toLowerCase().includes(query));
  dom.topPicksGrid.innerHTML = '';
  dom.trendingGrid.innerHTML = '';
  dom.newReleasesGrid.innerHTML = '';
  if (filtered.length === 0) {
    dom.topPicksGrid.innerHTML = '<p style="color:var(--text-muted);font-size:13px;padding:10px;">No games found.</p>';
  } else {
    filtered.forEach(g => dom.topPicksGrid.appendChild(createGameCard(g)));
  }
});

// Keyboard shortcut: Ctrl+K to focus search
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    dom.searchInput.focus();
  }
  if (e.key === 'Escape') {
    closeModal();
    if (dom.sidebar.classList.contains('mobile-open')) dom.sidebar.classList.remove('mobile-open');
  }
});

// ─── LIVE ODDS FLUCTUATION ───────────────────────────────────
setInterval(() => {
  document.querySelectorAll('.odds-btn:not(.selected)').forEach(btn => {
    const current = parseFloat(btn.textContent.replace(/[^\d.]/g, ''));
    if (isNaN(current)) return;
    const delta = (Math.random() - 0.5) * 0.1;
    const newVal = Math.max(1.01, current + delta).toFixed(2);
    const label = btn.querySelector('.odds-label');
    btn.innerHTML = '';
    if (label) btn.appendChild(label);
    btn.appendChild(document.createTextNode(newVal));
  });
}, 8000);

// ─── ONLINE COUNTER FOR GAME CARDS ───────────────────────────
setInterval(() => {
  document.querySelectorAll('.game-provider').forEach(el => {
    const match = el.textContent.match(/^(.+?) · ([\d,]+) playing$/);
    if (!match) return;
    const current = parseInt(match[2].replace(/,/g, ''));
    const next = Math.max(100, current + randomInt(-50, 80));
    el.textContent = `${match[1]} · ${next.toLocaleString()} playing`;
  });
}, 5000);

// ─── SCROLL ANIMATIONS (IntersectionObserver) ─────────────────
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.game-card, .promo-card, .sport-event').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
  observer.observe(el);
});

// ─── 4-HOUR ROTATING 24H JACKPOT ENGINE ──────────────────────
function update4hJackpot() {
  const el = document.getElementById('stat-jackpot');
  const timerEl = document.getElementById('jackpot-4h-timer');
  if (!el) return;

  const now = Date.now();
  const fourHoursMs = 4 * 60 * 60 * 1000;
  const currentIntervalIndex = Math.floor(now / fourHoursMs);
  const timeIntoInterval = now % fourHoursMs;
  const timeLeftMs = fourHoursMs - timeIntoInterval;

  // Base jackpot prize pools that rotate every 4 hours
  const basePools = [
    1845200, 2489100, 1675400, 3120800, 2210500, 2894000
  ];
  const baseVal = basePools[currentIntervalIndex % basePools.length];

  // Dynamic accumulator that slowly increases live (adds up to ₹250,000 over 4h)
  const growth = Math.floor((timeIntoInterval / fourHoursMs) * 250000) + (Math.floor(now / 3000) % 500) * 12;
  const totalJackpot = baseVal + growth;

  el.textContent = `₹${totalJackpot.toLocaleString('en-IN')}`;

  if (timerEl) {
    const hrs = Math.floor(timeLeftMs / 3600000);
    const mins = Math.floor((timeLeftMs % 3600000) / 60000);
    const secs = Math.floor((timeLeftMs % 60000) / 1000);
    timerEl.textContent = `⏳ 4H Reset: ${String(hrs).padStart(2,'0')}:${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`;
  }
}
setInterval(update4hJackpot, 1000);
update4hJackpot();

// Wire Promo CTAs to open Deposit Modal with Coupon pre-filled
window.claimPromoWithCoupon = function(couponCode, depositAmt) {
  if (typeof openWalletModal === 'function') {
    openWalletModal('deposit');
    setTimeout(() => {
      if (typeof applyPromoCoupon === 'function' && couponCode) applyPromoCoupon(couponCode, true);
    }, 150);
  }
};

// ─── INIT ─────────────────────────────────────────────────────
// Refresh balance & auth display on page load
updateAuthUI();
refreshLobbyBalance();

// Also refresh when user comes back from a game page
window.addEventListener('pageshow', () => { updateAuthUI(); refreshLobbyBalance(); });
window.addEventListener('focus', () => { updateAuthUI(); refreshLobbyBalance(); });

console.log('%c🎮 GG Wins — Loaded successfully!', 'color: #00e676; font-size: 16px; font-weight: bold; background: #0b1120; padding: 8px 16px; border-radius: 8px;');




// ── FULL PAGE QUICK LAUNCH GAMES POPULATOR ──
let activeGamesCategory = 'all';

function filterGamesCategory(category, btn) {
  activeGamesCategory = category;
  document.querySelectorAll('#game-tabs .tab-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderQuickLaunchGames();
}

function renderQuickLaunchGames() {
  const container = document.getElementById('full-quick-launch-grid');
  if (!container) return;

  let filtered = GAMES;
  if (activeGamesCategory !== 'all') {
    filtered = GAMES.filter(g => g.category === activeGamesCategory);
  }

  container.innerHTML = filtered.map(g => {
    const isHot = g.badge === 'hot';
    const tagText = g.category === 'originals' ? '🔥 Original' : g.category === 'table' ? '🃏 Table Royale' : '🎯 Casual & Arcade';
    const playersCount = (g.players || 4200).toLocaleString();

    return `
      <div class="ql-card" onclick="window.location.href='${g.gameUrl}'">
        <div class="ql-card-top">
          <div class="ql-icon-box">${g.icon}</div>
          <div class="ql-meta">
            <div class="ql-title">${g.name}</div>
            <div class="ql-sub">
              <span class="ql-tag">${tagText}</span>
              ${isHot ? '<span style="font-size:9px;background:rgba(239,68,68,0.18);color:#ef4444;padding:2px 5px;border-radius:4px;font-weight:900">HOT</span>' : ''}
            </div>
          </div>
        </div>

        <div class="ql-stats-row">
          <span style="color:#94a3b8">Live Players</span>
          <span style="font-weight:800;color:#ffd700">👥 ${playersCount}</span>
        </div>

        <button class="ql-play-btn" onclick="event.stopPropagation(); window.location.href='${g.gameUrl}'">
          ⚡ Quick Launch ${g.name}
        </button>
      </div>
    `;
  }).join('');
}

// ── AUTO-ROTATING HERO CAROUSEL ENGINE ──
let heroCurrentSlide = 0;
let heroSlideInterval = null;

function initHeroSlider() {
  const heroSlides = document.querySelectorAll('.carousel-slide');
  const heroDots = document.querySelectorAll('.carousel-dots .dot');
  if (!heroSlides.length) return;

  function showSlide(idx) {
    heroSlides.forEach((sl, i) => sl.classList.toggle('active', i === idx));
    heroDots.forEach((dt, i) => dt.classList.toggle('active', i === idx));
    heroCurrentSlide = idx;
  }

  function nextSlide() {
    showSlide((heroCurrentSlide + 1) % heroSlides.length);
  }

  function prevSlide() {
    showSlide((heroCurrentSlide - 1 + heroSlides.length) % heroSlides.length);
  }

  function startAutoRotate() {
    clearInterval(heroSlideInterval);
    heroSlideInterval = setInterval(nextSlide, 4500);
  }

  const prevBtn = document.getElementById('prev-slide-btn');
  const nextBtn = document.getElementById('next-slide-btn');
  if (prevBtn) prevBtn.addEventListener('click', (e) => { e.stopPropagation(); prevSlide(); startAutoRotate(); });
  if (nextBtn) nextBtn.addEventListener('click', (e) => { e.stopPropagation(); nextSlide(); startAutoRotate(); });

  heroDots.forEach((dt, idx) => {
    dt.addEventListener('click', (e) => {
      e.stopPropagation();
      showSlide(idx);
      startAutoRotate();
    });
  });

  const carouselBox = document.getElementById('hero-carousel');
  if (carouselBox) {
    carouselBox.addEventListener('mouseenter', () => clearInterval(heroSlideInterval));
    carouselBox.addEventListener('mouseleave', startAutoRotate);
  }

  startAutoRotate();
}

document.addEventListener('DOMContentLoaded', () => {
  renderQuickLaunchGames();
  initHeroSlider();
});
renderQuickLaunchGames();
initHeroSlider();


// ── HALF-PAGE LOBBY GAMES ARENA LOGIC ──
let activeHalfCategory = 'all';

function filterHalfGames(category, btn) {
  activeHalfCategory = category;
  document.querySelectorAll('#game-tabs .tab-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderHalfGames();
}

function renderHalfGames() {
  const container = document.getElementById('half-games-grid');
  if (!container) return;

  let filtered = GAMES;
  if (activeHalfCategory !== 'all') {
    filtered = GAMES.filter(g => g.category === activeHalfCategory);
  }

  container.innerHTML = filtered.map(g => {
    const isHot = g.badge === 'hot';
    const tagText = g.category === 'originals' ? '🔥 Original' : g.category === 'table' ? '🃏 Table' : '🎯 Arcade';
    const playersCount = (g.players || 4200).toLocaleString();

    return `
      <div class="half-game-card" onclick="window.location.href='${g.gameUrl}'">
        <div style="display:flex;align-items:center;gap:10px">
          <div class="h-icon-box">${g.icon}</div>
          <div style="flex:1;min-width:0">
            <div class="h-title">${g.name}</div>
            <div class="h-sub">
              <span>${tagText}</span>
              <span>•</span>
              <span style="color:#ffd700">👥 ${playersCount}</span>
            </div>
          </div>
        </div>
        <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='${g.gameUrl}'">
          ▶ Play Now
        </button>
      </div>
    `;
  }).join('');
}

document.addEventListener('DOMContentLoaded', () => {
  renderHalfGames();
});
renderHalfGames();
