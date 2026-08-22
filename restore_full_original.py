# Rebuild the complete original, pristine index.html with all features
import os, shutil

scratch_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html"
brain_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\index.html"

full_original_index = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover" />
  <meta name="theme-color" content="#0b0f19" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <title>GG Wins – The #1 Crypto &amp; INR Casino</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@600;700;800;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="style.css" />
  <script src="security-guard.js"></script>
</head>
<body>
  <div class="app-layout">
    <!-- ── SIDEBAR NAVIGATION ── -->
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-logo">
        <div class="logo-mark">
          <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <polygon points="20,4 36,13 36,27 20,36 4,27 4,13" fill="none" stroke="#00e676" stroke-width="2"/>
            <text x="50%" y="55%" dominant-baseline="middle" text-anchor="middle" fill="#00e676" font-size="12" font-weight="900" font-family="Space Grotesk">GG</text>
          </svg>
        </div>
        <span class="logo-text">GG <span class="logo-accent">Wins</span></span>
        <button class="sidebar-toggle" id="sidebar-toggle-btn" aria-label="Toggle sidebar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
      </div>

      <nav class="sidebar-nav" aria-label="Main navigation">
        <!-- Casino Section -->
        <div class="nav-section">
          <span class="nav-section-label">Casino</span>
          <a href="index.html" class="nav-item active" id="nav-lobby">
            <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg></span>
            <span class="nav-label">Lobby</span>
          </a>
          <a href="index.html" class="nav-item" id="nav-originals">
            <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/></svg></span>
            <span class="nav-label">Originals</span>
            <span class="nav-badge hot-badge">HOT</span>
          </a>
          <a href="index.html" class="nav-item" id="nav-slots">
            <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg></span>
            <span class="nav-label">Slots</span>
          </a>
          <a href="games/blackjack.html" class="nav-item" id="nav-blackjack">
            <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="1"/><path d="M16 7V5a2 2 0 00-4 0v2"/><path d="M8 7V5a2 2 0 00-4 0v2"/></svg></span>
            <span class="nav-label">Blackjack</span>
          </a>
          <a href="games/roulette.html" class="nav-item" id="nav-roulette">
            <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/></svg></span>
            <span class="nav-label">Roulette</span>
          </a>
        </div>

        <!-- Direct Play Games Menu -->
        <div class="nav-section">
          <span class="nav-section-label">All Games</span>
          <a href="games/crash.html" class="nav-item"><span class="nav-icon">🚀</span><span class="nav-label">GG Crash</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/mines.html" class="nav-item"><span class="nav-icon">💣</span><span class="nav-label">GG Mines</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/rummy.html" class="nav-item"><span class="nav-icon">🃏</span><span class="nav-label">Indian Rummy</span><span class="nav-badge" style="background:#00e676;color:#000">3D</span></a>
          <a href="games/baccarat.html" class="nav-item"><span class="nav-icon">👑</span><span class="nav-label">Royale Baccarat</span></a>
          <a href="games/ludo.html" class="nav-item"><span class="nav-icon">🎲</span><span class="nav-label">Ludo Champions</span></a>
          <a href="games/wheel.html" class="nav-item"><span class="nav-icon">🎡</span><span class="nav-label">Wheel of Fortune</span></a>
        </div>

        <!-- Banking & Support -->
        <div class="nav-section">
          <span class="nav-section-label">Banking &amp; Account</span>
          <a href="#" class="nav-item" onclick="if(typeof openWalletModal==='function') openWalletModal('deposit'); return false;">
            <span class="nav-icon" style="color:var(--green)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 12V22H4a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4z"/><path d="M20 12a2 2 0 000-4H6"/></svg></span>
            <span class="nav-label" style="font-weight:700">Deposit &amp; Wallet</span>
          </a>
          <a href="#" class="nav-item" onclick="if(typeof openWalletModal==='function') openWalletModal('payment-history'); return false;">
            <span class="nav-icon" style="color:#38bdf8">📜</span>
            <span class="nav-label">Payment History</span>
          </a>
          <a href="vip.html" class="nav-item" id="nav-vip">
            <span class="nav-icon" style="color:#ffd700">👑</span>
            <span class="nav-label">VIP Club</span>
            <span class="nav-badge vip-badge">VIP</span>
          </a>
          <a href="vip-lounge.html" class="nav-item" id="nav-vip-lounge">
            <span class="nav-icon">💬</span>
            <span class="nav-label">VIP Lounge</span>
          </a>
          <a href="help-centre.html" class="nav-item">
            <span class="nav-icon">❓</span>
            <span class="nav-label">Help Centre</span>
          </a>
        </div>
      </nav>

      <div class="sidebar-footer">
        <div class="provably-fair">
          <svg viewBox="0 0 24 24" fill="none" stroke="#00e676" stroke-width="2" width="16" height="16"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>Provably Fair</span>
        </div>
      </div>
    </aside>

    <!-- ── MAIN CONTENT ── -->
    <div class="main-content">
      <!-- TOPBAR -->
      <header class="topbar" id="topbar">
        <div class="topbar-left">
          <button class="menu-toggle" id="menu-toggle-btn" aria-label="Toggle menu">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
          </button>
          <div class="mobile-logo">
            <span class="logo-text">GG <span class="logo-accent">Wins</span></span>
          </div>
          <div class="search-bar">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
            <input type="text" placeholder="Search games..." class="search-input" id="search-input" aria-label="Search games" />
            <div class="search-shortcut">Ctrl+K</div>
          </div>
        </div>
        <div class="topbar-right">
          <!-- Multi-Account Wallet Chip -->
          <div id="wallet-chip-target">
            <div class="wallet-switcher-container" id="ggwins-wallet-switcher">
              <button class="wallet-chip-btn" onclick="toggleWalletDropdown(event)" title="Switch Active Account">
                <span class="wallet-active-icon">🎮</span>
                <span class="wallet-active-name" style="color:#94a3b8;font-size:11px">Demo INR</span>
                <span id="lobby-balance-chip" style="font-family:'Space Grotesk',sans-serif;font-weight:800;color:var(--gold)">₹10,000.00</span>
                <span class="wallet-arrow-icon" style="font-size:10px;color:#94a3b8">▼</span>
              </button>
              <div class="wallet-dropdown-menu" id="wallet-dropdown-menu" style="display:none">
                <div class="wallet-dropdown-header">SWITCH ACCOUNT</div>
                <div class="wallet-option active-option" onclick="switchActiveWallet('demo')">
                  <div class="wallet-opt-left"><span class="wallet-opt-icon">🎮</span><div class="wallet-opt-text"><span class="wallet-opt-name">Demo Account</span><span class="wallet-opt-badge">RISK FREE</span></div></div>
                  <span class="wallet-opt-bal" id="dd-bal-demo">₹10,000.00</span>
                </div>
                <div class="wallet-option" onclick="switchActiveWallet('real')">
                  <div class="wallet-opt-left"><span class="wallet-opt-icon">🇮🇳</span><div class="wallet-opt-text"><span class="wallet-opt-name">Real INR</span><span class="wallet-opt-badge real-badge">INSTANT UPI</span></div></div>
                  <span class="wallet-opt-bal" id="dd-bal-real">₹0.00</span>
                </div>
                <div class="wallet-option" onclick="switchActiveWallet('usdt')">
                  <div class="wallet-opt-left"><span class="wallet-opt-icon">₮</span><div class="wallet-opt-text"><span class="wallet-opt-name">USDT (Crypto)</span><span class="wallet-opt-badge usdt-badge">GLOBAL</span></div></div>
                  <span class="wallet-opt-bal" id="dd-bal-usdt">$0.00</span>
                </div>
              </div>
            </div>
          </div>

          <button class="deposit-quick-btn" onclick="if(typeof openWalletModal==='function') openWalletModal('deposit'); return false;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="15" height="15"><path d="M12 5v14M5 12h14"/></svg>
            <span>Deposit</span>
          </button>

          <!-- User Auth Actions -->
          <div class="header-auth" id="header-auth">
            <button class="btn-ghost" id="header-signin-btn">Sign In</button>
            <button class="btn-primary" id="header-register-btn">Register</button>
          </div>

          <!-- User Profile Dropdown (when logged in) -->
          <div class="user-menu hidden" id="user-menu">
            <button class="user-avatar-btn" id="user-avatar-btn" aria-label="User menu">
              <span class="user-avatar" id="header-user-avatar">👑</span>
              <span class="user-name" id="header-username">Player</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M6 9l6 6 6-6"/></svg>
            </button>
            <div class="user-dropdown" id="user-dropdown">
              <div class="user-dropdown-header">
                <span class="user-dropdown-name" id="dd-username">Player</span>
                <span class="user-dropdown-email" id="dd-email">player@ggwins.io</span>
                <span class="vip-badge" id="dd-vip-badge">VIP Bronze</span>
              </div>
              <div class="user-dropdown-divider"></div>
              <a href="#" class="user-dropdown-item" onclick="openWalletModal('deposit'); return false;">💳 Deposit</a>
              <a href="#" class="user-dropdown-item" onclick="openWalletModal('withdraw'); return false;">⚡ Withdraw</a>
              <a href="#" class="user-dropdown-item" onclick="openWalletModal('payment-history'); return false;">📜 Payment History</a>
              <a href="vip.html" class="user-dropdown-item">👑 VIP Club</a>
              <div class="user-dropdown-divider"></div>
              <button class="user-dropdown-item text-danger" id="logout-btn">Log Out</button>
            </div>
          </div>

          <button class="chat-toggle-btn" id="chat-toggle-btn" aria-label="Toggle chat">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
            <span class="chat-count">247</span>
          </button>
        </div>
      </header>

      <!-- HERO CAROUSEL -->
      <main class="page-content" id="main-content">
        <section class="hero-carousel" id="hero-carousel" aria-label="Featured promotions">
          <div class="carousel-track">
            <!-- Slide 1: Welcome Deposit Bonus -->
            <div class="carousel-slide slide-1 active" id="slide-1" onclick="if(typeof openWalletModal==='function') openWalletModal('deposit')" style="cursor:pointer">
              <div class="slide-content">
                <span class="slide-badge">⚡ 100% WELCOME BONUS</span>
                <h1 class="slide-title">Double Your First Deposit <span class="text-gradient">Up to ₹50,000</span></h1>
                <p class="slide-desc">Use coupon code <strong style="color:#00e676;font-family:monospace;font-size:16px">GG1675</strong> for instant 100% matched cash on all UPI &amp; Bank deposits!</p>
                <div class="slide-actions">
                  <button class="btn-primary" onclick="event.stopPropagation(); if(typeof openWalletModal==='function') openWalletModal('deposit')">💳 Deposit with GG1675</button>
                  <button class="btn-secondary" onclick="event.stopPropagation(); document.getElementById('games-section').scrollIntoView({behavior:'smooth'})">Explore Games</button>
                </div>
              </div>
            </div>

            <!-- Slide 2: Daily Spin Wheel -->
            <div class="carousel-slide slide-2" id="slide-2" onclick="window.location.href='games/wheel.html'" style="cursor:pointer">
              <div class="slide-content">
                <span class="slide-badge" style="background:linear-gradient(135deg,#ffd700,#ff8c00);color:#000">🎡 DAILY SPIN &amp; WIN</span>
                <h2 class="slide-title">Lucky Spin Wheel <span class="text-gradient">Win Up to ₹25,000</span></h2>
                <p class="slide-desc">Spin the Fortune Wheel daily to win instant real cash rewards, multiplier boosters, and VIP vault chips!</p>
                <div class="slide-actions">
                  <button class="btn-primary" style="background:linear-gradient(135deg,#ffd700,#ff8c00);color:#000" onclick="event.stopPropagation(); window.location.href='games/wheel.html'">🎡 Spin the Wheel Now</button>
                  <button class="btn-secondary" onclick="event.stopPropagation(); window.location.href='games/crash.html'">Play GG Crash 🚀</button>
                </div>
              </div>
            </div>

            <!-- Slide 3: VIP Membership -->
            <div class="carousel-slide slide-3" id="slide-3" onclick="window.location.href='vip.html'" style="cursor:pointer">
              <div class="slide-content">
                <span class="slide-badge" style="background:rgba(255,215,0,0.2);color:#ffd700;border:1px solid #ffd700">👑 VIP CLUB</span>
                <h2 class="slide-title">Monthly VIP Status <span class="text-gradient">&amp; Daily Cash</span></h2>
                <p class="slide-desc">Join Bronze, Silver or Gold VIP to earn up to ₹150 daily cash vault drops, private lounge access, and glowing badges!</p>
                <div class="slide-actions">
                  <button class="btn-primary" onclick="event.stopPropagation(); window.location.href='vip.html'">👑 View VIP Plans</button>
                  <button class="btn-secondary" onclick="event.stopPropagation(); window.location.href='vip-lounge.html'">VIP Lounge 💬</button>
                </div>
              </div>
            </div>
          </div>

          <button class="carousel-nav-btn prev-btn" id="prev-slide-btn" aria-label="Previous slide">‹</button>
          <button class="carousel-nav-btn next-btn" id="next-slide-btn" aria-label="Next slide">›</button>

          <div class="carousel-dots" id="carousel-dots">
            <span class="dot active" data-slide="0"></span>
            <span class="dot" data-slide="1"></span>
            <span class="dot" data-slide="2"></span>
          </div>
        </section>

        <!-- STATS BAR -->
        <section class="stats-bar" aria-label="Platform statistics">
          <div class="stat-item"><span class="stat-value" id="stat-online">2,481</span><span class="stat-label">Players Online</span></div>
          <div class="stat-divider"></div>
          <div class="stat-item"><span class="stat-value" id="stat-wagered">₹142.8M</span><span class="stat-label">Total Wagered</span></div>
          <div class="stat-divider"></div>
          <div class="stat-item"><span class="stat-value" id="stat-payout">99.2%</span><span class="stat-label">Avg RTP</span></div>
          <div class="stat-divider"></div>
          <div class="stat-item"><span class="stat-value text-gold" id="stat-jackpot">₹8,450,000</span><span class="stat-label">Jackpot Pool</span></div>
        </section>

        <!-- GAME CATEGORY TABS & GRIDS -->
        <section class="section games-section" id="games-section">
          <div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;margin-bottom:20px">
            <div class="section-tabs" id="game-tabs" role="tablist">
              <button class="tab-btn active" id="tab-all" data-category="all" role="tab" aria-selected="true">🎮 All Games (20)</button>
              <button class="tab-btn" id="tab-originals-cat" data-category="originals" role="tab" aria-selected="false">🔥 GG Originals (7)</button>
              <button class="tab-btn" id="tab-table-cat" data-category="table" role="tab" aria-selected="false">🃏 Cards &amp; Table (6)</button>
              <button class="tab-btn" id="tab-arcade-cat" data-category="arcade" role="tab" aria-selected="false">🎯 Casual &amp; Arcade (7)</button>
            </div>
          </div>

          <!-- Section 1: GG Originals -->
          <div class="subsection" id="originals-subsection">
            <div class="subsection-header">
              <h2 class="subsection-title">🔥 GG Originals (Instant Play)</h2>
              <span style="font-size:12px;color:var(--text-muted);font-weight:600" id="originals-count-lbl">7 Games</span>
            </div>
            <div class="games-grid" id="originals-grid"></div>
          </div>

          <!-- Section 2: Cards & Table -->
          <div class="subsection" id="table-subsection">
            <div class="subsection-header">
              <h2 class="subsection-title">🃏 Cards &amp; Table Royale</h2>
            </div>
            <div class="games-grid" id="table-grid"></div>
          </div>

          <!-- Section 3: Arcade -->
          <div class="subsection" id="arcade-subsection">
            <div class="subsection-header">
              <h2 class="subsection-title">🎯 Casual &amp; Arcade</h2>
            </div>
            <div class="games-grid" id="arcade-grid"></div>
          </div>
        </section>

        <!-- LIVE BETS TICKER -->
        <section class="section ticker-section" id="ticker-section">
          <div class="section-header">
            <h2 class="section-title">⚡ Live Bets &amp; Recent Wins</h2>
            <div class="ticker-filters">
              <button class="ticker-filter active" id="filter-all-wins" data-filter="all">All</button>
              <button class="ticker-filter" id="filter-big-wins" data-filter="big">Big Wins</button>
            </div>
          </div>
          <div class="ticker-table" id="ticker-table">
            <div class="ticker-head">
              <span>Game</span><span>Player</span><span>Bet</span><span>Multiplier</span><span style="text-align:right">Payout</span>
            </div>
            <div class="ticker-body" id="ticker-body"></div>
          </div>
        </section>
      </main>
    </div>

    <!-- ── LIVE CHAT SIDEBAR ── -->
    <aside class="chat-sidebar hidden-chat" id="chat-sidebar">
      <div class="chat-header">
        <div class="chat-title">
          <span>💬</span> Live Chat
          <span class="online-chip"><span class="pulse-dot"></span><span id="chat-online">247</span> online</span>
        </div>
        <button class="chat-close-btn" id="chat-close-btn" aria-label="Close chat">✕</button>
      </div>
      <div class="chat-messages" id="chat-messages"></div>
      <div class="chat-input-area">
        <div class="chat-input-row">
          <input type="text" class="chat-input" placeholder="Type a message or ask AI..." id="chat-input-field" aria-label="Chat message" />
          <button class="chat-send-btn" id="chat-send-btn" aria-label="Send message">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22,2 15,22 11,13 2,9"/></svg>
          </button>
        </div>
      </div>
    </aside>
  </div>

  <!-- ── AUTH MODAL ── -->
  <div id="auth-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-label="Authentication">
    <div class="modal-box" id="modal-box">
      <button class="modal-close" id="modal-close-btn" aria-label="Close modal">✕</button>
      <div class="modal-tabs">
        <button class="modal-tab active" id="tab-login" data-tab="login">Sign In</button>
        <button class="modal-tab" id="tab-register" data-tab="register">Register</button>
      </div>

      <!-- Login Form -->
      <div class="modal-form" id="form-login">
        <h2 class="modal-title">Welcome Back</h2>
        <p class="modal-subtitle">Sign in to your GG Wins account</p>
        <div class="form-group">
          <label class="form-label">Username or Email</label>
          <input type="text" class="form-input" placeholder="Enter your username or email" id="login-user" />
        </div>
        <div class="form-group">
          <label class="form-label">Password</label>
          <input type="password" class="form-input" placeholder="Enter your password" id="login-pass" />
        </div>
        <button class="btn-primary full-width mt-md" id="sign-in-btn">Sign In</button>
      </div>

      <!-- Register Form -->
      <div class="modal-form hidden" id="form-register">
        <h2 class="modal-title">Create Account</h2>
        <p class="modal-subtitle">Join millions of players on GG Wins</p>
        <div class="form-group">
          <label class="form-label">Username</label>
          <input type="text" class="form-input" placeholder="Choose a username" id="reg-user" />
        </div>
        <div class="form-group">
          <label class="form-label">Email</label>
          <input type="email" class="form-input" placeholder="Enter your email" id="reg-email" />
        </div>
        <div class="form-group">
          <label class="form-label">Password</label>
          <input type="password" class="form-input" placeholder="Create a password" id="reg-pass" />
        </div>
        <label class="checkbox-label mt-sm">
          <input type="checkbox" id="terms-check" checked />
          I am 18+ and agree to the <a href="#" class="form-link">Terms of Service</a>
        </label>
        <button class="btn-primary full-width mt-md" id="create-account-btn">Create Account</button>
      </div>
    </div>
  </div>

  <!-- TOAST -->
  <div id="toast" class="toast" role="status" aria-live="polite"></div>

  <script src="wallet.js"></script>
  <script src="script.js"></script>
</body>
</html>
"""

with open(scratch_path, "w", encoding="utf-8") as f:
    f.write(full_original_index)

shutil.copy2(scratch_path, brain_path)
print("SUCCESS: index.html completely rewritten and restored to the pristine original state!")