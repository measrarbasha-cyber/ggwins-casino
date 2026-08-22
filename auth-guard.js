/* =====================================================
   auth-guard.js – GG Wins Game Auth Guard
   Drop-in: <script src="../auth-guard.js"></script>
   Call requireAuth() before any game action.
   ===================================================== */

(function() {
  // ── Inject modal styles ──────────────────────────────
  const style = document.createElement('style');
  style.textContent = `
    #gg-auth-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.82);
      backdrop-filter: blur(8px);
      z-index: 9999;
      align-items: center;
      justify-content: center;
    }
    #gg-auth-overlay.show { display: flex; }

    #gg-auth-modal {
      background: linear-gradient(145deg, #1e293b, #0f172a);
      border: 1.5px solid rgba(255,215,0,0.4);
      border-radius: 20px;
      padding: 36px 28px 28px;
      width: min(420px, 92vw);
      box-shadow: 0 0 50px rgba(255,215,0,0.15), 0 20px 60px rgba(0,0,0,0.8);
      font-family: 'Space Grotesk', sans-serif;
      position: relative;
      animation: authModalPop 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes authModalPop {
      0%  { transform: scale(0.8) translateY(30px); opacity: 0; }
      100%{ transform: scale(1)   translateY(0);    opacity: 1; }
    }

    .gg-auth-close {
      position: absolute;
      top: 14px; right: 16px;
      background: rgba(255,255,255,0.07);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 8px;
      color: #94a3b8;
      cursor: pointer;
      padding: 4px 10px;
      font-size: 16px;
      line-height: 1;
      transition: all 0.2s;
    }
    .gg-auth-close:hover { color: #fff; background: rgba(255,255,255,0.15); }

    .gg-auth-logo {
      text-align: center;
      font-size: 22px;
      font-weight: 900;
      color: #fff;
      margin-bottom: 4px;
    }
    .gg-auth-logo span { color: #ffd700; }
    .gg-auth-subtitle {
      text-align: center;
      font-size: 13px;
      color: #94a3b8;
      margin-bottom: 22px;
    }

    .gg-auth-tabs {
      display: flex;
      background: rgba(255,255,255,0.05);
      border-radius: 10px;
      padding: 3px;
      margin-bottom: 20px;
    }
    .gg-auth-tab {
      flex: 1;
      padding: 9px;
      text-align: center;
      font-weight: 800;
      font-size: 13px;
      color: #64748b;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .gg-auth-tab.active {
      background: linear-gradient(135deg, #7c4dff, #5c35cc);
      color: #fff;
      box-shadow: 0 4px 12px rgba(124,77,255,0.4);
    }

    .gg-auth-panel { display: none; }
    .gg-auth-panel.active { display: block; }

    .gg-auth-field {
      width: 100%;
      background: rgba(255,255,255,0.06);
      border: 1.5px solid rgba(255,255,255,0.1);
      border-radius: 10px;
      padding: 12px 14px;
      font-size: 14px;
      color: #fff;
      font-family: 'Space Grotesk', sans-serif;
      margin-bottom: 10px;
      box-sizing: border-box;
      transition: border-color 0.2s;
    }
    .gg-auth-field:focus {
      outline: none;
      border-color: #7c4dff;
      box-shadow: 0 0 0 3px rgba(124,77,255,0.2);
    }
    .gg-auth-field::placeholder { color: #475569; }

    .gg-auth-btn {
      width: 100%;
      padding: 13px;
      border-radius: 10px;
      border: none;
      background: linear-gradient(135deg, #7c4dff, #5c35cc);
      color: #fff;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 800;
      font-size: 15px;
      cursor: pointer;
      margin-top: 6px;
      transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      box-shadow: 0 4px 15px rgba(124,77,255,0.35);
    }
    .gg-auth-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(124,77,255,0.5);
    }

    .gg-auth-google-btn {
      width: 100%;
      padding: 11px;
      border-radius: 10px;
      border: 1.5px solid rgba(255,255,255,0.15);
      background: rgba(255,255,255,0.06);
      color: #fff;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      font-size: 14px;
      cursor: pointer;
      margin-top: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      transition: all 0.2s;
    }
    .gg-auth-google-btn:hover { background: rgba(255,255,255,0.1); }

    .gg-auth-divider {
      display: flex;
      align-items: center;
      gap: 10px;
      margin: 12px 0;
      color: #475569;
      font-size: 12px;
    }
    .gg-auth-divider::before,
    .gg-auth-divider::after {
      content: '';
      flex: 1;
      height: 1px;
      background: rgba(255,255,255,0.1);
    }

    .gg-auth-error {
      background: rgba(239,68,68,0.15);
      border: 1px solid rgba(239,68,68,0.3);
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 13px;
      color: #fca5a5;
      margin-bottom: 10px;
      display: none;
    }
    .gg-auth-success {
      background: rgba(0,230,118,0.15);
      border: 1px solid rgba(0,230,118,0.3);
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 13px;
      color: #6ee7b7;
      margin-bottom: 10px;
      display: none;
    }
  `;
  document.head.appendChild(style);

  // ── Inject modal HTML ────────────────────────────────
  const overlay = document.createElement('div');
  overlay.id = 'gg-auth-overlay';
  overlay.innerHTML = `
    <div id="gg-auth-modal">
      <button class="gg-auth-close" onclick="ggAuthClose()">✕</button>
      <div class="gg-auth-logo">GG <span>Wins</span></div>
      <div class="gg-auth-subtitle">🔒 Please sign in or register to play</div>

      <div class="gg-auth-tabs">
        <div class="gg-auth-tab active" id="tab-login-btn" onclick="ggAuthTab('login')">Sign In</div>
        <div class="gg-auth-tab" id="tab-reg-btn"   onclick="ggAuthTab('register')">Register</div>
      </div>

      <!-- LOGIN PANEL -->
      <div class="gg-auth-panel active" id="panel-login">
        <div class="gg-auth-error" id="login-err"></div>
        <div class="gg-auth-success" id="login-ok"></div>
        <input class="gg-auth-field" id="ga-login-email"    type="email"    placeholder="Email address">
        <input class="gg-auth-field" id="ga-login-password" type="password" placeholder="Password">
        <button class="gg-auth-btn" onclick="ggDoLogin()">Sign In & Play 🎮</button>
        <div class="gg-auth-divider">or</div>
        <button class="gg-auth-google-btn" onclick="ggGoogleAuth()">
          <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.55 10.78l7.98-6.19z"/><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.55 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/></svg>
          Continue with Google
        </button>
      </div>

      <!-- REGISTER PANEL -->
      <div class="gg-auth-panel" id="panel-register">
        <div class="gg-auth-error" id="reg-err"></div>
        <div class="gg-auth-success" id="reg-ok"></div>
        <input class="gg-auth-field" id="ga-reg-name"     type="text"     placeholder="Full Name">
        <input class="gg-auth-field" id="ga-reg-email"    type="email"    placeholder="Email address">
        <input class="gg-auth-field" id="ga-reg-mobile"   type="tel"      placeholder="Mobile number">
        <input class="gg-auth-field" id="ga-reg-password" type="password" placeholder="Create password (min 6 chars)">
        <button class="gg-auth-btn" onclick="ggDoRegister()">Create Account & Play 🎮</button>
        <div class="gg-auth-divider">or</div>
        <button class="gg-auth-google-btn" onclick="ggGoogleAuth()">
          <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.55 10.78l7.98-6.19z"/><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.55 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/></svg>
          Register with Google
        </button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  // ── Close on overlay click ───────────────────────────
  overlay.addEventListener('click', function(e){ if(e.target===overlay) ggAuthClose(); });

  // ── Guard function (called by every game action) ─────
  window.requireAuth = function() {
    const session = JSON.parse(localStorage.getItem('ggwins_session') || 'null');
    if(session && session.email) return true;
    // Show modal
    overlay.classList.add('show');
    return false;
  };

  // ── Tab switch ───────────────────────────────────────
  window.ggAuthTab = function(tab) {
    document.querySelectorAll('.gg-auth-tab').forEach(t=>t.classList.remove('active'));
    document.querySelectorAll('.gg-auth-panel').forEach(p=>p.classList.remove('active'));
    document.getElementById('tab-'+tab+'-btn').classList.add('active');
    document.getElementById('panel-'+tab).classList.add('active');
  };

  window.ggAuthClose = function() {
    overlay.classList.remove('show');
  };

  // ── Google OAuth ─────────────────────────────────────
  window.ggGoogleAuth = function() {
    window.open('https://accounts.google.com/o/oauth2/v2/auth?client_id=GGWINS_APP&redirect_uri=' +
      encodeURIComponent(location.origin) + '&response_type=token&scope=email%20profile', '_blank',
      'width=500,height=600,scrollbars=yes');
  };

  // ── DB helpers ───────────────────────────────────────
  function getDB(){ return JSON.parse(localStorage.getItem('ggwins_db') || '{"users":[]}'); }
  function saveDB(db){ localStorage.setItem('ggwins_db', JSON.stringify(db)); }

  function showErr(id, msg){ const el=document.getElementById(id); el.textContent=msg; el.style.display='block'; }
  function showOk(id, msg){  const el=document.getElementById(id); el.textContent=msg; el.style.display='block'; }
  function clearMsg(ids){ ids.forEach(id=>{ const el=document.getElementById(id); if(el) el.style.display='none'; }); }

  // ── Do Login ─────────────────────────────────────────
  window.ggDoLogin = function() {
    clearMsg(['login-err','login-ok']);
    const email = document.getElementById('ga-login-email').value.trim();
    const pass  = document.getElementById('ga-login-password').value;

    if(!email||!pass){ showErr('login-err','Please fill in all fields.'); return; }

    const db = getDB();
    const user = db.users.find(u=>u.email===email && u.password===pass);
    if(!user){ showErr('login-err','Invalid email or password.'); return; }

    localStorage.setItem('ggwins_session', JSON.stringify({ email: user.email, name: user.name }));
    showOk('login-ok','✅ Signed in! Starting game…');
    setTimeout(()=>{ ggAuthClose(); if(typeof updateAllWalletDisplays==='function') updateAllWalletDisplays(); }, 900);
  };

  // ── Do Register ──────────────────────────────────────
  window.ggDoRegister = function() {
    clearMsg(['reg-err','reg-ok']);
    const name   = document.getElementById('ga-reg-name').value.trim();
    const email  = document.getElementById('ga-reg-email').value.trim();
    const mobile = document.getElementById('ga-reg-mobile').value.trim();
    const pass   = document.getElementById('ga-reg-password').value;

    if(!name||!email||!mobile||!pass){ showErr('reg-err','Please fill in all fields.'); return; }
    if(pass.length < 6){ showErr('reg-err','Password must be at least 6 characters.'); return; }
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){ showErr('reg-err','Enter a valid email address.'); return; }

    const db = getDB();
    if(db.users.find(u=>u.email===email)){ showErr('reg-err','Email already registered. Please sign in.'); return; }

    const newUser = { name, email, mobile, password: pass, createdAt: new Date().toISOString() };
    db.users.push(newUser);
    saveDB(db);
    localStorage.setItem('ggwins_session', JSON.stringify({ email, name }));

    showOk('reg-ok','🎉 Account created! Welcome to GG Wins!');
    setTimeout(()=>{ ggAuthClose(); if(typeof updateAllWalletDisplays==='function') updateAllWalletDisplays(); }, 900);
  };

  // ── Auto-show on page load if not logged in (optional soft prompt) ──
  // Uncomment below to immediately prompt on entry:
  // window.addEventListener('load', ()=>{ if(!requireAuth()) {} });

})();
