import re

clean_help_centre_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Help Centre – GG Wins</title>
<meta name="description" content="GG Wins Help Centre – Find answers to common questions about accounts, payments, games, tournaments, and VIP.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {
  --bg:#0b1120;--bg2:#111827;--bg3:#1a2332;--card:#1e2d3d;--card2:#243447;
  --green:#00e676;--green-dim:rgba(0,230,118,0.1);--gold:#ffd700;--red:#ef5350;
  --text:#e8edf5;--text2:#8fa3b8;--muted:#4d6478;
  --border:rgba(255,255,255,0.07);--border2:rgba(255,255,255,0.13);
  --radius:12px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text2);min-height:100vh;}
a{color:var(--green);text-decoration:none;}
a:hover{text-decoration:underline;}

/* NAV */
.site-nav{position:sticky;top:0;z-index:100;background:rgba(11,17,32,0.95);backdrop-filter:blur(16px);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;padding:0 24px;height:60px;gap:16px;}
.nav-logo{font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:800;color:var(--text);}
.nav-logo span{color:var(--green);}
.nav-links{display:flex;gap:6px;flex-wrap:wrap;}
.nav-link{font-size:13px;font-weight:600;color:var(--text2);padding:6px 14px;border-radius:20px;border:1px solid var(--border);transition:all 0.2s;}
.nav-link:hover,.nav-link.active{color:var(--text);border-color:var(--border2);background:var(--card);text-decoration:none;}
.nav-link.home{background:var(--green);color:#000;border-color:var(--green);}

/* HERO */
.help-hero{background:linear-gradient(135deg,#0b1120,#0d1a2e,#0b1120);border-bottom:1px solid var(--border);padding:56px 24px 40px;text-align:center;position:relative;overflow:hidden;}
.help-hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(0,230,118,0.07) 0%,transparent 65%);pointer-events:none;}
.hero-badge{display:inline-flex;align-items:center;gap:6px;background:var(--green-dim);border:1px solid rgba(0,230,118,0.25);border-radius:20px;padding:5px 14px;font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--green);margin-bottom:16px;}
.help-hero h1{font-family:'Space Grotesk',sans-serif;font-size:clamp(28px,5vw,48px);font-weight:900;color:var(--text);margin-bottom:12px;}
.help-hero h1 span{color:var(--green);}
.help-hero p{font-size:15px;color:var(--text2);max-width:500px;margin:0 auto 28px;}

/* SEARCH */
.help-search-wrap{max-width:540px;margin:0 auto;position:relative;}
.help-search{width:100%;padding:14px 20px 14px 48px;border-radius:12px;background:var(--bg2);border:1.5px solid var(--border2);color:var(--text);font-size:15px;font-family:'Inter',sans-serif;outline:none;transition:all 0.2s;}
.help-search:focus{border-color:var(--green);box-shadow:0 0 0 3px rgba(0,230,118,0.1);}
.help-search::placeholder{color:var(--muted);}
.search-ico{position:absolute;left:16px;top:50%;transform:translateY(-50%);color:var(--muted);pointer-events:none;}
.search-clear{position:absolute;right:16px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--muted);cursor:pointer;font-size:16px;display:none;}

/* CATEGORIES */
.help-main{max-width:1100px;margin:0 auto;padding:48px 24px;}
.section-title{font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:800;color:var(--text);margin-bottom:6px;}
.section-sub{font-size:14px;color:var(--text2);margin-bottom:24px;}

.category-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;margin-bottom:56px;}
.cat-card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:22px;cursor:pointer;transition:all 0.2s;display:flex;flex-direction:column;gap:10px;text-decoration:none;}
.cat-card:hover{border-color:var(--border2);background:var(--card);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.3);text-decoration:none;}
.cat-icon{font-size:28px;line-height:1;}
.cat-name{font-family:'Space Grotesk',sans-serif;font-size:15px;font-weight:700;color:var(--text);}
.cat-desc{font-size:12px;color:var(--text2);line-height:1.5;}
.cat-count{font-size:11px;font-weight:700;color:var(--muted);margin-top:auto;}

/* FAQ ACCORDION */
.faq-section{margin-bottom:48px;}
.faq-section-header{display:flex;align-items:center;gap:10px;margin-bottom:16px;}
.faq-section-icon{font-size:22px;}
.faq-section-title{font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:800;color:var(--text);}

.faq-item{background:var(--bg2);border:1px solid var(--border);border-radius:10px;margin-bottom:8px;overflow:hidden;transition:border-color 0.2s;}
.faq-item.open{border-color:rgba(0,230,118,0.25);}
.faq-q{display:flex;align-items:center;justify-content:space-between;padding:16px 18px;cursor:pointer;gap:12px;user-select:none;}
.faq-q-text{font-size:14px;font-weight:600;color:var(--text);line-height:1.4;}
.faq-chevron{width:20px;height:20px;flex-shrink:0;color:var(--muted);transition:transform 0.25s;}
.faq-item.open .faq-chevron{transform:rotate(180deg);color:var(--green);}
.faq-a{max-height:0;overflow:hidden;transition:max-height 0.3s ease;}
.faq-item.open .faq-a{max-height:600px;}
.faq-a-inner{padding:0 18px 16px;font-size:13.5px;color:var(--text2);line-height:1.7;border-top:1px solid var(--border);}
.faq-a-inner p{margin-bottom:8px;}
.faq-a-inner p:last-child{margin-bottom:0;}
.faq-a-inner a{color:var(--green);}
.faq-a-inner ul{padding-left:18px;margin:8px 0;}
.faq-a-inner li{margin-bottom:6px;}

/* Contact box */
.contact-box{background:linear-gradient(135deg,rgba(0,230,118,0.07),rgba(0,180,100,0.04));border:1px solid rgba(0,230,118,0.2);border-radius:var(--radius);padding:28px;text-align:center;margin-top:48px;}
.contact-box h3{font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:800;color:var(--text);margin-bottom:8px;}
.contact-box p{font-size:14px;color:var(--text2);margin-bottom:20px;}
.contact-btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;}
.btn-contact{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;border-radius:8px;font-size:13px;font-weight:700;cursor:pointer;transition:all 0.2s;text-decoration:none;border:none;}
.btn-contact.primary{background:var(--green);color:#000;}
.btn-contact.primary:hover{filter:brightness(1.1);text-decoration:none;}
.btn-contact.secondary{background:var(--bg2);color:var(--text);border:1px solid var(--border2);}
.btn-contact.secondary:hover{border-color:var(--green);color:var(--green);text-decoration:none;}

/* No results */
.no-results{text-align:center;padding:48px;color:var(--muted);display:none;}
.no-results-icon{font-size:48px;margin-bottom:12px;}

/* Footer */
.page-footer{background:var(--bg2);border-top:1px solid var(--border);padding:24px;text-align:center;font-size:12px;color:var(--muted);}
.footer-links{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-bottom:10px;}
.footer-links a{color:var(--text2);font-size:12px;}
.footer-links a:hover{color:var(--green);text-decoration:none;}

/* highlight */
mark{background:rgba(0,230,118,0.2);color:var(--green);border-radius:2px;padding:0 2px;}
</style>
<script src="security-guard.js"></script>
</head>
<body>
<nav class="site-nav">
  <div class="nav-logo">GG <span>Wins</span></div>
  <div class="nav-links">
    <a href="index.html" class="nav-link home">← Back to Lobby</a>
    <a href="tournaments.html" class="nav-link">🏆 Tournaments</a>
    <a href="vip.html" class="nav-link">👑 VIP Club</a>
    <a href="help-centre.html" class="nav-link active">Help Centre</a>
    <a href="privacy-policy.html" class="nav-link">Privacy</a>
    <a href="terms.html" class="nav-link">Terms</a>
  </div>
</nav>

<!-- HERO -->
<div class="help-hero">
  <div class="hero-badge">💬 24/7 Support</div>
  <h1>How can we <span>help you?</span></h1>
  <p>Search our knowledge base or browse categories below to find instant answers.</p>
  <div class="help-search-wrap">
    <svg class="search-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
    <input type="text" class="help-search" id="search-faq" placeholder="Search for answers..." autocomplete="off">
    <button class="search-clear" id="search-clear-btn" onclick="clearSearch()">✕</button>
  </div>
</div>

<main class="help-main">

  <!-- CATEGORIES -->
  <div id="category-section">
    <div class="section-title">Browse by Topic</div>
    <div class="section-sub">Find answers by selecting a category</div>
    <div class="category-grid">
      <a href="#account" class="cat-card" onclick="scrollToSection('account')">
        <div class="cat-icon">👤</div>
        <div class="cat-name">Account &amp; Profile</div>
        <div class="cat-desc">Registration, login, password recovery and security</div>
        <div class="cat-count">4 articles</div>
      </a>
      <a href="#deposits" class="cat-card" onclick="scrollToSection('deposits')">
        <div class="cat-icon">💳</div>
        <div class="cat-name">Deposits &amp; Payments</div>
        <div class="cat-desc">UPI, QR Code, USDT TRC20 and instant processing</div>
        <div class="cat-count">5 articles</div>
      </a>
      <a href="#withdrawals" class="cat-card" onclick="scrollToSection('withdrawals')">
        <div class="cat-icon">💸</div>
        <div class="cat-name">Withdrawals</div>
        <div class="cat-desc">IMPS Bank Transfer, processing times and limits</div>
        <div class="cat-count">4 articles</div>
      </a>
      <a href="#tournaments" class="cat-card" onclick="scrollToSection('tournaments')">
        <div class="cat-icon">🏆</div>
        <div class="cat-name">Arena Tournaments</div>
        <div class="cat-desc">₹50 registration fee, leaderboards and cash prizes</div>
        <div class="cat-count">3 articles</div>
      </a>
      <a href="#vip" class="cat-card" onclick="scrollToSection('vip')">
        <div class="cat-icon">👑</div>
        <div class="cat-name">VIP Club &amp; Lounge</div>
        <div class="cat-desc">Bronze, Silver, Gold memberships and daily vault rewards</div>
        <div class="cat-count">4 articles</div>
      </a>
      <a href="#bonuses" class="cat-card" onclick="scrollToSection('bonuses')">
        <div class="cat-icon">🎁</div>
        <div class="cat-name">Bonuses &amp; Coupons</div>
        <div class="cat-desc">Promo coupons, deposit scaling and wagering tasks</div>
        <div class="cat-count">3 articles</div>
      </a>
      <a href="#games" class="cat-card" onclick="scrollToSection('games')">
        <div class="cat-icon">🎮</div>
        <div class="cat-name">Games &amp; Fairness</div>
        <div class="cat-desc">Provably Fair cryptographic verification and game rules</div>
        <div class="cat-count">4 articles</div>
      </a>
      <a href="#technical" class="cat-card" onclick="scrollToSection('technical')">
        <div class="cat-icon">🔧</div>
        <div class="cat-name">Technical Support</div>
        <div class="cat-desc">Browser compatibility, local storage and troubleshooting</div>
        <div class="cat-count">3 articles</div>
      </a>
    </div>
  </div>

  <!-- FAQ LIST -->
  <div id="faq-container">

    <!-- ACCOUNT -->
    <div class="faq-section" id="account" style="scroll-margin-top:80px">
      <div class="faq-section-header">
        <span class="faq-section-icon">👤</span>
        <span class="faq-section-title">Account &amp; Profile</span>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">How do I create an account on GG Wins?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>Creating an account takes less than 30 seconds:</p>
          <ul>
            <li>Click the <strong>Register</strong> button in the top-right corner of any page.</li>
            <li>Choose a unique username (minimum 3 characters).</li>
            <li>Enter a valid email address and secure password (minimum 6 characters).</li>
            <li>Confirm you are 18+ and accept the Terms of Service.</li>
            <li>Click <strong>Create Account</strong>. You'll instantly receive <strong>₹50,000 Demo INR</strong> practice funds!</li>
          </ul>
        </div></div>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">I forgot my password. How can I reset it?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>Click <strong>Sign In</strong> in the top header, then click <em>"Forgot password?"</em>. Enter the email address registered with your account, and we will send you a reset link. Alternatively, email our support team at <a href="mailto:support@ggwins.com">support@ggwins.com</a> with your username.</p>
        </div></div>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">Can I switch between Demo INR, Real INR, and USDT accounts?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>Yes! GG Wins features a <strong>3-in-1 Multi-Account Wallet System</strong>. Click your balance chip in the top header to instantly switch between:</p>
          <ul>
            <li><strong>🎮 Demo INR:</strong> Practice funds with instant 1-click refill.</li>
            <li><strong>💵 Real INR:</strong> Real money balance deposited via instant UPI / QR Code.</li>
            <li><strong>₮ USDT (TRC20):</strong> Crypto account for international high-rollers.</li>
          </ul>
        </div></div>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">How do I change my avatar or display name?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>Click your avatar circle in the top right header to open your user panel. You can select from dozens of gaming emojis and avatar styles to represent you at live multiplayer tables.</p>
        </div></div>
      </div>
    </div>

    <!-- DEPOSITS -->
    <div class="faq-section" id="deposits" style="scroll-margin-top:80px">
      <div class="faq-section-header">
        <span class="faq-section-icon">💳</span>
        <span class="faq-section-title">Deposits &amp; Payments</span>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">How do I deposit money using UPI &amp; QR Codes?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>Depositing is simple and takes under 1 minute:</p>
          <ul>
            <li>Click <strong>Wallet / Deposit</strong> in the header or sidebar.</li>
            <li>Select your deposit amount (or apply a bonus coupon).</li>
            <li>Scan one of the 3 official UPI QR codes using Google Pay, PhonePe, Paytm, or BHIM.</li>
            <li>Copy the 12-digit UTR / Transaction Reference Number from your payment app.</li>
            <li>Paste the 12-digit UTR into the confirmation box and hit <strong>Submit Deposit</strong>. Funds are credited instantly upon host confirmation!</li>
          </ul>
        </div></div>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">What are the supported payment QR Codes and UPI IDs?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>GG Wins rotates across 3 dedicated banking endpoints for 100% uptime:</p>
          <ul>
            <li><strong>QR #1:</strong> <code>amdasrarbasha-1@oksbi</code></li>
            <li><strong>QR #2:</strong> <code>kabilanr2210@okhdfcbank</code></li>
            <li><strong>QR #3:</strong> <code>txchem@slc</code></li>
          </ul>
          <p>You can switch QR codes at any time inside the payment window using the <strong>🔄 Switch QR</strong> button.</p>
        </div></div>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">What is the minimum deposit amount?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>The standard minimum deposit is <strong>₹100 INR</strong>. For promotional coupon bonuses (such as <code>GG1675</code>), the minimum deposit is <strong>₹1,675.00 INR</strong> to qualify for up to 100% bonus rewards.</p>
        </div></div>
      </div>
    </div>

    <!-- WITHDRAWALS -->
    <div class="faq-section" id="withdrawals" style="scroll-margin-top:80px">
      <div class="faq-section-header">
        <span class="faq-section-icon">💸</span>
        <span class="faq-section-title">Withdrawals</span>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">How do I withdraw my winnings to my bank account?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>To withdraw your real funds:</p>
          <ul>
            <li>Open the <strong>Wallet</strong> modal and switch to the <strong>Withdraw</strong> tab.</li>
            <li>Enter your withdrawal amount (minimum ₹500 INR).</li>
            <li>Fill in your Bank Name, Account Number, and IFSC Code.</li>
            <li>Click <strong>Submit Withdrawal</strong>. Funds are transferred via direct 24/7 IMPS transfer.</li>
          </ul>
        </div></div>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">How long does a withdrawal take?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>IMPS bank transfers are typically processed within <strong>5 to 15 minutes</strong>. Crypto USDT TRC20 withdrawals are confirmed within 1 to 3 blockchain network confirmations.</p>
        </div></div>
      </div>
    </div>

    <!-- TOURNAMENTS -->
    <div class="faq-section" id="tournaments" style="scroll-margin-top:80px">
      <div class="faq-section-header">
        <span class="faq-section-icon">🏆</span>
        <span class="faq-section-title">Arena Game Tournaments</span>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">How do I enter an Arena Game Tournament?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>Navigate to the <a href="tournaments.html">🏆 Tournaments</a> tab in the sidebar navigation. Choose any casino game (e.g. VIP Crash Royale, Sic Bo, Coin Flip, Rummy) and click <strong>Pay ₹50 Entry Fee &amp; Join Tournament</strong>. ₹50 is deducted from your Real Balance and you are immediately enrolled on that game's live tournament leaderboard!</p>
        </div></div>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">How are tournament prizes distributed?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>Tournament prize pools range from ₹15,000 to ₹35,000 per game. The top 1 winner takes <strong>60% of the grand prize pool</strong>, 2nd place receives 25%, and 3rd place receives 15%.</p>
        </div></div>
      </div>
    </div>

    <!-- VIP -->
    <div class="faq-section" id="vip" style="scroll-margin-top:80px">
      <div class="faq-section-header">
        <span class="faq-section-icon">👑</span>
        <span class="faq-section-title">VIP Club &amp; Members Lounge</span>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">What are the VIP Membership plans and daily vault rewards?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>GG Wins offers 3 tiered 1-Month (30 Days) VIP memberships:</p>
          <ul>
            <li>🥉 <strong>Bronze VIP (₹1,699 / Month):</strong> Unlocks <strong>₹35 Daily Vault Cash Reward</strong> (₹1,050/mo cashback) + Glowing Bronze Badge.</li>
            <li>🥈 <strong>Silver VIP (₹2,899 / Month):</strong> Unlocks <strong>₹60 Daily Vault Cash Reward</strong> (₹1,800/mo cashback) + Glowing Silver Aura.</li>
            <li>👑 <strong>Gold VIP (₹5,499 / Month):</strong> Unlocks <strong>₹150 Daily Vault Cash Reward</strong> (₹4,500/mo cashback) + Glowing Gold Badge + Private Lounge Access.</li>
          </ul>
        </div></div>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">How do I unlock the VIP Members Lounge?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>Visit the <a href="vip.html">VIP Club</a> page, select your membership plan, and complete checkout on the dedicated VIP payment tab. Once approved by the host, your glowing VIP badge appears beside your username and the <a href="vip-lounge.html">Royale VIP Lounge</a> unlocks automatically for 30 days!</p>
        </div></div>
      </div>
    </div>

    <!-- TECHNICAL -->
    <div class="faq-section" id="technical" style="scroll-margin-top:80px">
      <div class="faq-section-header">
        <span class="faq-section-icon">🔧</span>
        <span class="faq-section-title">Technical Support</span>
      </div>
      <div class="faq-item">
        <div class="faq-q" onclick="toggleFaq(this)">
          <span class="faq-q-text">The site is not loading properly — what should I do?</span>
          <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="faq-a"><div class="faq-a-inner">
          <p>Try these quick troubleshooting steps:</p>
          <ul>
            <li>Hard refresh your browser page (Ctrl+Shift+R or Cmd+Shift+R).</li>
            <li>Clear browser cache and site cookies.</li>
            <li>Ensure JavaScript is enabled.</li>
            <li>Try Chrome, Firefox, or Safari on desktop or mobile.</li>
          </ul>
        </div></div>
      </div>
    </div>

  </div><!-- /faq-container -->

  <div class="no-results" id="no-results">
    <div class="no-results-icon">🔍</div>
    <p>No results found for "<span id="search-term"></span>"</p>
    <p style="margin-top:8px;font-size:13px">Try different keywords or browse the categories above.</p>
  </div>

  <!-- CONTACT -->
  <div class="contact-box">
    <h3>Still need help? 💬</h3>
    <p>Our support team is available 24/7. You can also use the AI chat assistant button in the bottom-right corner of any page for instant answers.</p>
    <div class="contact-btns">
      <a href="mailto:support@ggwins.com" class="btn-contact primary">✉️ Email Support</a>
      <a href="index.html" class="btn-contact secondary">🎮 Back to Lobby</a>
    </div>
  </div>

</main>

<footer class="page-footer">
  <div class="footer-links">
    <a href="index.html">Back to Lobby</a>
    <a href="tournaments.html">Tournaments</a>
    <a href="vip.html">VIP Club</a>
    <a href="privacy-policy.html">Privacy Policy</a>
    <a href="terms.html">Terms &amp; Conditions</a>
    <a href="mailto:support@ggwins.com">Contact Support</a>
  </div>
  <p>© 2025 GG Wins. All rights reserved. | Play responsibly. 18+</p>
</footer>

<script>
function toggleFaq(el) {
  const item = el.parentElement;
  const wasOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
  if (!wasOpen) item.classList.add('open');
}

function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) { el.scrollIntoView({ behavior: 'smooth' }); if (window.event) window.event.preventDefault(); }
}

// SEARCH
const searchInput = document.getElementById('search-faq');
const clearBtn = document.getElementById('search-clear-btn');
const noResults = document.getElementById('no-results');
const catSection = document.getElementById('category-section');

if (searchInput) {
  searchInput.addEventListener('input', () => {
    const q = searchInput.value.trim().toLowerCase();
    if (clearBtn) clearBtn.style.display = q ? 'block' : 'none';
    filterFaqs(q);
  });
}

function clearSearch() {
  if (searchInput) {
    searchInput.value = '';
    if (clearBtn) clearBtn.style.display = 'none';
    filterFaqs('');
    searchInput.focus();
  }
}

function filterFaqs(q) {
  const items = document.querySelectorAll('.faq-item');
  const sections = document.querySelectorAll('.faq-section');
  let anyVisible = false;

  if (!q) {
    items.forEach(i => { i.style.display = ''; });
    sections.forEach(s => { s.style.display = ''; });
    if (catSection) catSection.style.display = '';
    if (noResults) noResults.style.display = 'none';
    document.querySelectorAll('.faq-q-text').forEach(t => { t.innerHTML = t.dataset.original || t.innerHTML; });
    return;
  }

  if (catSection) catSection.style.display = 'none';
  items.forEach(item => {
    const qEl = item.querySelector('.faq-q-text');
    const aEl = item.querySelector('.faq-a-inner');
    const text = ((qEl ? qEl.textContent : '') + ' ' + (aEl ? aEl.textContent : '')).toLowerCase();
    if (text.includes(q)) {
      item.style.display = '';
      item.classList.add('open');
      anyVisible = true;
      if (qEl) {
        if (!qEl.dataset.original) qEl.dataset.original = qEl.innerHTML;
        const re = new RegExp(`(${q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')})`, 'gi');
        qEl.innerHTML = (qEl.dataset.original || qEl.textContent).replace(re, '<mark>$1</mark>');
      }
    } else {
      item.style.display = 'none';
    }
  });

  sections.forEach(s => {
    const visible = [...s.querySelectorAll('.faq-item')].some(i => i.style.display !== 'none');
    s.style.display = visible ? '' : 'none';
  });

  if (noResults) noResults.style.display = anyVisible ? 'none' : 'block';
  const searchTermEl = document.getElementById('search-term');
  if (searchTermEl && searchInput) searchTermEl.textContent = searchInput.value;
}

document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); if (searchInput) searchInput.focus(); }
  if (e.key === 'Escape') { clearSearch(); }
});
</script>
</body>
</html>
"""

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\help-centre.html", "w", encoding="utf-8") as f:
    f.write(clean_help_centre_html)

print("SUCCESS: Cleaned and modernized help-centre.html without any strange symbols or encoding errors!")
