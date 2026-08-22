import re

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip.html", "r", encoding="utf-8") as f:
    vip_html = f.read()

# Add Lightbox and 3-QR CSS styles into vip.html
extra_css = """
/* ── 3-QR ROTATOR & LIGHTBOX STYLES ── */
.vip-qr-box {
  display: flex;
  gap: 12px;
  background: #090e17;
  border: 1.5px solid rgba(255,215,0,0.3);
  border-radius: 14px;
  padding: 12px;
  align-items: center;
}
.vip-qr-thumb {
  width: 90px;
  height: 90px;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  padding: 4px;
  position: relative;
  cursor: pointer;
  border: 1.5px solid #ffd700;
  flex-shrink: 0;
  transition: transform 0.2s;
}
.vip-qr-thumb:hover { transform: scale(1.03); }
.vip-qr-thumb img { width: 100%; height: 100%; object-fit: contain; display: block; border-radius: 6px; }
.vip-qr-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background: #ffd700;
  color: #000;
  font-size: 9px;
  font-weight: 900;
  padding: 1px 5px;
  border-radius: 999px;
}
.vip-qr-details { flex: 1; overflow: hidden; }
.vip-upi-lbl { font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 2px; }
.vip-upi-txt { font-family: monospace; font-size: 13px; font-weight: 800; color: #00e676; margin-bottom: 6px; word-break: break-all; }
.vip-qr-btn-row { display: flex; gap: 6px; flex-wrap: wrap; }
.vip-btn-rot {
  background: rgba(255,215,0,0.15);
  border: 1px solid #ffd700;
  color: #ffd700;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 11px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.vip-btn-rot:hover { background: #ffd700; color: #000; }
.vip-btn-copy {
  background: rgba(0,230,118,0.15);
  border: 1px solid #00e676;
  color: #00e676;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 11px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.vip-btn-copy:hover { background: #00e676; color: #000; }
.vip-btn-pop {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.2);
  color: #fff;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.vip-btn-pop:hover { background: rgba(255,255,255,0.18); }

/* QR Lightbox Popup Modal */
.vip-lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.92);
  backdrop-filter: blur(16px);
  z-index: 1000000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 16px;
}
.vip-lightbox-overlay.show { display: flex; animation: pmOverlay 0.2s ease; }
.vip-lightbox-card {
  background: #111827;
  border: 2px solid #ffd700;
  border-radius: 20px;
  padding: 24px;
  max-width: 380px;
  width: 100%;
  text-align: center;
  position: relative;
  box-shadow: 0 0 50px rgba(255,215,0,0.3);
}
.vip-lightbox-close {
  position: absolute;
  top: 14px;
  right: 14px;
  background: rgba(255,255,255,0.1);
  border: none;
  color: #fff;
  font-size: 14px;
  font-weight: 800;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
}
.vip-lightbox-img-box {
  width: 200px;
  height: 200px;
  background: #fff;
  border-radius: 12px;
  padding: 8px;
  margin: 14px auto;
  position: relative;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}
.vip-lightbox-img-box img { width: 100%; height: 100%; object-fit: contain; display: block; border-radius: 8px; }
"""

vip_html = vip_html.replace('</style>', extra_css + '\n</style>')

# Replace the pm-upi-section in HTML with the dynamic 3-QR Rotator
old_upi_section = """      <!-- UPI Details (shown by default) -->
      <div id="pm-upi-section">
        <div class="pm-section-label">Scan or Copy UPI ID</div>
        <div class="pm-upi-box">
          <div class="pm-qr">⬛</div>
          <div class="pm-upi-info">
            <div class="pm-upi-id-label">UPI Payment ID</div>
            <div class="pm-upi-id" id="pm-upi-id">ggwins@ybl</div>
            <div class="pm-upi-copy" onclick="copyUpiId()">📋 Tap to copy UPI ID</div>
            <div class="pm-upi-step">Open any UPI app → Pay → Enter UPI ID or scan QR</div>
          </div>
        </div>
      </div>"""

new_upi_section = """      <!-- UPI Details (3 QR Codes Rotator) -->
      <div id="pm-upi-section">
        <div class="pm-section-label" style="display:flex;justify-content:space-between;align-items:center">
          <span>Scan QR or Copy UPI ID</span>
          <button type="button" class="vip-btn-rot" onclick="rotateVipQR()" id="vip-rot-btn-top">🔄 Next QR (1/3)</button>
        </div>
        <div class="vip-qr-box" id="vip-qr-rotator-box">
          <div class="vip-qr-thumb" onclick="openVipQRLightbox()" title="Click to enlarge & save QR">
            <img id="vip-qr-img" src="assets/qr1.jpg" alt="UPI QR Code" data-idx="0">
            <div class="vip-qr-badge" id="vip-qr-badge">1/3</div>
          </div>
          <div class="vip-qr-details">
            <div class="vip-upi-lbl">Pay to UPI ID:</div>
            <div class="vip-upi-txt" id="vip-upi-id-display">amdasrarbasha-1@oksbi</div>
            <div class="vip-qr-btn-row">
              <button type="button" class="vip-btn-copy" id="vip-copy-btn" onclick="copyCurrentVipUPI(this)">📋 Copy UPI</button>
              <button type="button" class="vip-btn-pop" onclick="openVipQRLightbox()">🔍 Pop up &amp; Save</button>
              <button type="button" class="vip-btn-rot" onclick="rotateVipQR()">🔄 Switch</button>
            </div>
          </div>
        </div>
        <div style="font-size:11px;color:#94a3b8;margin-top:6px">
          💡 <strong>Tip:</strong> Tap the QR to enlarge and screenshot, or copy the UPI ID and pay via GPay, PhonePe, Paytm, or BHIM.
        </div>
      </div>"""

vip_html = vip_html.replace(old_upi_section, new_upi_section)

# Add Lightbox HTML container before </body>
lightbox_html = """
<!-- ── VIP QR FULLSCREEN LIGHTBOX POPUP ── -->
<div id="vip-qr-lightbox" class="vip-lightbox-overlay" onclick="closeVipQRLightbox()">
  <div class="vip-lightbox-card" onclick="event.stopPropagation()">
    <button class="vip-lightbox-close" onclick="closeVipQRLightbox()">✕</button>
    <div style="font-family:'Space Grotesk',sans-serif;font-size:17px;font-weight:900;color:#ffd700">📸 Scan &amp; Pay via UPI</div>
    <div style="font-size:11.5px;color:#94a3b8;margin-top:2px" id="vip-lightbox-sub">Option 1 of 3 • Screenshot or Download to Pay</div>

    <div class="vip-lightbox-img-box">
      <img src="assets/qr1.jpg" alt="UPI QR Code" id="vip-lightbox-img">
    </div>

    <div style="background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:8px 12px;display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:12px">
      <div style="text-align:left;overflow:hidden">
        <div style="font-size:10px;color:#94a3b8;font-weight:700">UPI ID:</div>
        <div style="font-family:monospace;font-size:13px;font-weight:800;color:#00e676" id="vip-lightbox-upi-txt">amdasrarbasha-1@oksbi</div>
      </div>
      <button class="vip-btn-copy" onclick="copyCurrentVipUPI(this)" style="padding:6px 12px">📋 Copy</button>
    </div>

    <div style="display:flex;gap:8px;justify-content:center">
      <a href="assets/qr1.jpg" download="ggwins-vip-qr.jpg" id="vip-lightbox-dl-btn" style="flex:1;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;text-decoration:none;font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:800;padding:10px;border-radius:10px;display:inline-block">
        📥 Download QR
      </a>
      <button class="vip-btn-rot" onclick="rotateVipLightboxQR()" style="flex:1;padding:10px;font-size:12px;border-radius:10px">
        🔄 Next QR
      </button>
    </div>
  </div>
</div>
"""

vip_html = vip_html.replace('</body>', lightbox_html + '\n</body>')

# Add 3-QR JavaScript rotator and lightbox functions into <script>
qr_js_script = """
  // ── 3 QR CODES DATA & ROTATOR ──
  const VIP_QR_DATA = [
    { src: 'assets/qr1.jpg', upi: 'amdasrarbasha-1@oksbi' },
    { src: 'assets/qr2.jpg', upi: 'kabilanr2210@okhdfcbank' },
    { src: 'assets/qr3.jpg', upi: 'txchem@slc' }
  ];

  let currentVipQrIdx = 0;

  function rotateVipQR() {
    currentVipQrIdx = (currentVipQrIdx + 1) % VIP_QR_DATA.length;
    updateVipQRDisplay();
  }

  function updateVipQRDisplay() {
    const item = VIP_QR_DATA[currentVipQrIdx];
    const img = document.getElementById('vip-qr-img');
    const badge = document.getElementById('vip-qr-badge');
    const upiTxt = document.getElementById('vip-upi-id-display');
    const topBtn = document.getElementById('vip-rot-btn-top');

    if (img) {
      img.src = item.src;
      img.dataset.idx = currentVipQrIdx;
    }
    if (badge) badge.textContent = `${currentVipQrIdx + 1}/3`;
    if (upiTxt) upiTxt.textContent = item.upi;
    if (topBtn) topBtn.textContent = `🔄 Next QR (${currentVipQrIdx + 1}/3)`;
  }

  function copyCurrentVipUPI(btn) {
    const upi = VIP_QR_DATA[currentVipQrIdx].upi;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(upi);
    }
    const orig = btn.textContent;
    btn.textContent = 'Copied! ✓';
    btn.style.background = '#00e676';
    btn.style.color = '#000';
    setTimeout(() => {
      btn.textContent = orig;
      btn.style.background = '';
      btn.style.color = '';
    }, 1500);
  }

  function openVipQRLightbox() {
    const item = VIP_QR_DATA[currentVipQrIdx];
    document.getElementById('vip-lightbox-img').src = item.src;
    document.getElementById('vip-lightbox-upi-txt').textContent = item.upi;
    document.getElementById('vip-lightbox-sub').textContent = `Option ${currentVipQrIdx + 1} of 3 • Screenshot or Download to Pay`;
    document.getElementById('vip-lightbox-dl-btn').href = item.src;
    document.getElementById('vip-qr-lightbox').classList.add('show');
  }

  function closeVipQRLightbox() {
    document.getElementById('vip-qr-lightbox').classList.remove('show');
  }

  function rotateVipLightboxQR() {
    rotateVipQR();
    openVipQRLightbox();
  }
"""

vip_html = vip_html.replace('</script>', qr_js_script + '\n</script>')

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\vip.html", "w", encoding="utf-8") as f:
    f.write(vip_html)

print("Updated vip.html with 3 QR codes, rotator, UPI IDs, and Fullscreen Lightbox!")
