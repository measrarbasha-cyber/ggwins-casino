import http.server
import ssl
import sys
import os
import time
import json
import hashlib
import threading
import urllib.parse
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from http import HTTPStatus

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "ggwinssupport@gmail.com")
ADMIN_EMAIL_PASSWORD = os.environ.get("ADMIN_EMAIL_PASSWORD", "dvqilktybosupeuh")
ADMIN_NOTIFY_RECEIVER = os.environ.get("ADMIN_NOTIFY_RECEIVER", "ggwinssupport@gmail.com")

def dispatch_admin_email_alert(subject, plain_text, html, receiver_override=None, sync=False):
    def _send():
        try:
            db = load_db()
            email_cfg = db.get("email_config", {})
            sender = (os.environ.get("ADMIN_EMAIL") or email_cfg.get("sender") or "ggwinssupport@gmail.com").strip()
            pwd = (os.environ.get("ADMIN_EMAIL_PASSWORD") or email_cfg.get("password") or "dvqilktybosupeuh").replace(" ", "").strip()
            receiver = (receiver_override or os.environ.get("ADMIN_NOTIFY_RECEIVER") or email_cfg.get("receiver") or "ggwinssupport@gmail.com").strip()
            webhook_url = (os.environ.get("EMAIL_WEBHOOK_URL") or email_cfg.get("webhook_url") or "").strip()
            resend_key = (os.environ.get("RESEND_API_KEY") or email_cfg.get("resend_key") or "").strip()
            tg_token = (os.environ.get("TELEGRAM_BOT_TOKEN") or email_cfg.get("telegram_bot_token") or "").strip()
            tg_chat_id = (os.environ.get("TELEGRAM_CHAT_ID") or email_cfg.get("telegram_chat_id") or "").strip()

            sent = False
            err_msg = ""
            delivery_channel = "SMTP"

            # ── 1. RESEND HTTPS API RELAY (PORT 443 - NEVER BLOCKED) ──────
            if not sent and resend_key:
                try:
                    resend_req = urllib.request.Request(
                        "https://api.resend.com/emails",
                        data=json.dumps({
                            "from": f"GG WINS Alerts <onboarding@resend.dev>",
                            "to": [receiver],
                            "subject": subject,
                            "html": html,
                            "text": plain_text
                        }).encode("utf-8"),
                        headers={
                            "Authorization": f"Bearer {resend_key}",
                            "Content-Type": "application/json",
                            "User-Agent": "GG-Wins-Alerts/1.0"
                        }
                    )
                    with urllib.request.urlopen(resend_req, timeout=10) as r:
                        if r.status in (200, 201):
                            sent = True
                            delivery_channel = "Resend HTTPS API"
                            print(f"[Email Alert Resend] Delivered: {subject} -> {receiver}")
                except Exception as e_resend:
                    err_msg += f"Resend Error: {e_resend}; "

            # ── 2. CUSTOM HTTPS WEBHOOK RELAY (PORT 443) ──────────────────
            if not sent and webhook_url:
                try:
                    payload = json.dumps({
                        "to": receiver,
                        "subject": subject,
                        "html": html,
                        "text": plain_text,
                        "timestamp": int(time.time() * 1000)
                    }).encode("utf-8")
                    wb_req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "GG-Wins-Relay/1.0"})
                    with urllib.request.urlopen(wb_req, timeout=10) as r:
                        if r.status in (200, 201, 204):
                            sent = True
                            delivery_channel = "HTTPS Webhook Relay"
                            print(f"[Email Alert Webhook] Dispatched: {subject} -> {webhook_url}")
                except Exception as e_wb:
                    err_msg += f"Webhook Error: {e_wb}; "

            # ── 3. TELEGRAM BOT INSTANT PUSH NOTIFICATION (PORT 443) ───────
            if tg_token and tg_chat_id:
                try:
                    clean_tg_text = f"🚨 *{subject}*\n\n{plain_text}"
                    tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
                    tg_payload = json.dumps({
                        "chat_id": tg_chat_id,
                        "text": clean_tg_text,
                        "parse_mode": "Markdown"
                    }).encode("utf-8")
                    tg_req = urllib.request.Request(tg_url, data=tg_payload, headers={"Content-Type": "application/json"})
                    with urllib.request.urlopen(tg_req, timeout=8) as r:
                        if r.status == 200:
                            sent = True
                            delivery_channel = "Telegram Bot Alert"
                            print(f"[Telegram Alert] Sent to Chat {tg_chat_id}")
                except Exception as e_tg:
                    err_msg += f"Telegram Error: {e_tg}; "

            # ── 4. DIRECT SMTP SSL-465 / STARTTLS-587 ─────────────────────
            if not sent:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = f"GG WINS Admin Alerts <{sender}>"
                msg["To"] = receiver
                msg["Reply-To"] = sender

                msg.attach(MIMEText(plain_text, "plain"))
                msg.attach(MIMEText(html, "html"))

                try:
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=8) as server:
                        server.login(sender, pwd)
                        server.sendmail(sender, receiver, msg.as_string())
                    sent = True
                    delivery_channel = "SMTP SSL-465"
                    print(f"[Email Alert SSL-465] Delivered: {subject} -> {receiver}")
                except Exception as e465:
                    err_msg += f"SSL-465: {e465}; "
                    try:
                        with smtplib.SMTP("smtp.gmail.com", 587, timeout=8) as server:
                            server.starttls()
                            server.login(sender, pwd)
                            server.sendmail(sender, receiver, msg.as_string())
                        sent = True
                        delivery_channel = "SMTP TLS-587"
                        print(f"[Email Alert TLS-587] Delivered: {subject} -> {receiver}")
                    except Exception as e587:
                        err_msg += f"TLS-587: {e587}"
                        print(f"[Email Alert Failed] {err_msg}")

            # Record in email dispatch logs
            log_entry = {
                "id": f"EML-{os.urandom(4).hex().upper()}",
                "to": receiver,
                "subject": subject,
                "channel": delivery_channel,
                "status": "Delivered" if sent else "Failed",
                "error": err_msg if not sent else None,
                "timestamp": int(time.time() * 1000)
            }
            db.setdefault("email_logs", []).insert(0, log_entry)
            db["email_logs"] = db["email_logs"][:60]
            save_db(db)
            return sent, (delivery_channel if sent else err_msg)
        except Exception as e:
            print(f"[Email Alert Exception] {e}")
            return False, str(e)

    if sync:
        return _send()
    else:
        threading.Thread(target=_send, daemon=True).start()
        return True, "Queued"

def send_deposit_email_notification(deposit):
    amt = deposit.get("amount", 0)
    u = deposit.get("username", "Player")
    qr = deposit.get("qrLabel") or f"QR {deposit.get('qrNumber', 1)}"
    utr = deposit.get("utr", "N/A")
    order_id = deposit.get("orderId", "N/A")
    sub = f"🚨 [GG WINS] New Deposit Alert: ₹{amt:,.2f} from @{u} ({qr})"
    plain = f"GG WINS New Deposit Alert\n\nPlayer: @{u}\nAmount: Rs.{amt:,.2f}\nGateway: {qr}\nUTR: {utr}\nOrder ID: {order_id}\n\nApprove at https://ggwins.site/host/index.html"
    html = f"""
    <div style="font-family: Arial, sans-serif; background-color: #0f172a; padding: 24px; color: #f8fafc; border-radius: 12px; max-width: 540px; margin: 0 auto; border: 1.5px solid #ffd700;">
        <div style="text-align: center; margin-bottom: 16px;">
            <h2 style="color: #ffd700; margin: 0;">🎮 GG WINS – New Deposit Alert</h2>
            <p style="color: #94a3b8; font-size: 13px; margin-top: 4px;">A player has submitted a new deposit request on your platform.</p>
        </div>
        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 16px; margin-bottom: 16px;">
            <p style="margin: 6px 0; font-size: 14px;"><strong>👤 Player Username:</strong> <span style="color: #38bdf8; font-weight: bold;">@{u}</span></p>
            <p style="margin: 6px 0; font-size: 14px;"><strong>💰 Deposit Amount:</strong> <span style="color: #00e676; font-size: 16px; font-weight: bold;">₹{amt:,.2f}</span></p>
            <p style="margin: 6px 0; font-size: 14px;"><strong>🎯 Payment Gateway / QR:</strong> <span style="color: #c084fc; font-weight: bold;">{qr}</span></p>
            <p style="margin: 6px 0; font-size: 14px;"><strong>🔢 12-Digit UTR Number:</strong> <span style="background: #1e293b; padding: 3px 8px; border-radius: 4px; font-family: monospace; color: #ffd700; font-weight: bold;">{utr}</span></p>
            <p style="margin: 6px 0; font-size: 14px;"><strong>📦 Order ID:</strong> {order_id}</p>
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <a href="https://ggwins.site/host/index.html" style="background: linear-gradient(135deg, #ffd700, #ff8c00); color: #000; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 14px; display: inline-block;">
                🔓 Open Admin Terminal to Approve
            </a>
        </div>
    </div>
    """
    dispatch_admin_email_alert(sub, plain, html)

def send_withdrawal_email_notification(withdrawal):
    amt = withdrawal.get("amount", 0)
    u = withdrawal.get("username", "Player")
    w_key = withdrawal.get("wallet", "real")
    method = withdrawal.get("method", "UPI Payout")
    upi = withdrawal.get("accountNo") or withdrawal.get("upiId") or "N/A"
    order_id = withdrawal.get("orderId", "N/A")
    curr = "$" if w_key == "usdt" else "₹"
    sub = f"💸 [GG WINS] New Withdrawal Request: {curr}{amt:,.2f} from @{u}"
    plain = f"GG WINS Withdrawal Request\n\nPlayer: @{u}\nAmount: {curr}{amt:,.2f}\nMethod: {method}\nPayout Target: {upi}\nOrder ID: {order_id}\n\nReview at https://ggwins.site/host/index.html"
    html = f"""
    <div style="font-family: Arial, sans-serif; background-color: #0f172a; padding: 24px; color: #f8fafc; border-radius: 12px; max-width: 540px; margin: 0 auto; border: 1.5px solid #00e676;">
        <div style="text-align: center; margin-bottom: 16px;">
            <h2 style="color: #00e676; margin: 0;">💸 GG WINS – Withdrawal Alert</h2>
            <p style="color: #94a3b8; font-size: 13px; margin-top: 4px;">A player has requested a cash withdrawal payout.</p>
        </div>
        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 16px; margin-bottom: 16px;">
            <p style="margin: 6px 0; font-size: 14px;"><strong>👤 Player:</strong> <span style="color: #38bdf8; font-weight: bold;">@{u}</span></p>
            <p style="margin: 6px 0; font-size: 14px;"><strong>💵 Payout Amount:</strong> <span style="color: #00e676; font-size: 16px; font-weight: bold;">{curr}{amt:,.2f}</span></p>
            <p style="margin: 6px 0; font-size: 14px;"><strong>🏦 Payout Method / Destination:</strong> <span style="color: #ffd700; font-weight: bold;">{method} ({upi})</span></p>
            <p style="margin: 6px 0; font-size: 14px;"><strong>📦 Order ID:</strong> {order_id}</p>
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <a href="https://ggwins.site/host/index.html" style="background: linear-gradient(135deg, #00e676, #00b0ff); color: #000; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 14px; display: inline-block;">
                🔓 Process Withdrawal in Admin Terminal
            </a>
        </div>
    </div>
    """
    dispatch_admin_email_alert(sub, plain, html)

BASE_DIR = Path(__file__).resolve().parent
USER_DIR = BASE_DIR
ADMIN_DIR = BASE_DIR / "host"
CERT_DIR = BASE_DIR / "cert"
DB_FILE = BASE_DIR / "data" / "database.json"

DB_FILE.parent.mkdir(parents=True, exist_ok=True)
db_lock = threading.Lock()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

in_memory_db = {
    "users": [],
    "wallets": {"demo": 10000.0, "real": 0.0, "usdt": 0.0},
    "deposits": [],
    "withdrawals": [],
    "vip_requests": [],
    "transactions": []
}

def generate_referral_code(existing_users=None):
    if existing_users is None:
        existing_users = []
    existing_codes = {str(u.get("referralCode", "")).upper() for u in existing_users}
    while True:
        code = f"GG-{os.urandom(3).hex().upper()}"
        if code not in existing_codes:
            return code

def load_db():
    global in_memory_db
    with db_lock:
        if DB_FILE.is_file():
            try:
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        loaded = json.loads(content)
                        if isinstance(loaded, dict) and "users" in loaded:
                            in_memory_db = loaded
            except Exception:
                pass

        in_memory_db.setdefault("users", [])
        in_memory_db.setdefault("deposits", [])
        in_memory_db.setdefault("withdrawals", [])
        in_memory_db.setdefault("vip_requests", [])
        in_memory_db.setdefault("transactions", [])
        in_memory_db.setdefault("email_logs", [])
        in_memory_db.setdefault("email_config", {"sender": "ggwinssupport@gmail.com", "receiver": "ggwinssupport@gmail.com"})
        in_memory_db.setdefault("wallets", {"demo": 10000.0, "real": 0.0, "usdt": 0.0})

        # Automatically assign unique User IDs and unique Referral Codes to any legacy/existing users
        dirty = False
        existing_codes = set()
        for u in in_memory_db["users"]:
            if not u.get("id"):
                u["id"] = f"USER-{os.urandom(4).hex().upper()}"
                dirty = True
            if not u.get("wallets"):
                u["wallets"] = {"demo": 10000.0, "real": 0.0, "usdt": 0.0}
                dirty = True
            ref = str(u.get("referralCode", "")).strip().upper()
            if not ref or not ref.startswith("GG-") or ref in existing_codes or ref == str(u.get("username", "")).upper():
                u["referralCode"] = generate_referral_code(in_memory_db["users"])
                dirty = True
            existing_codes.add(u["referralCode"])

        if dirty and DB_FILE.is_file():
            try:
                temp_file = DB_FILE.with_suffix('.tmp')
                with open(temp_file, "w", encoding="utf-8") as wf:
                    json.dump(in_memory_db, wf, indent=2)
                temp_file.replace(DB_FILE)
            except Exception:
                pass

        return in_memory_db

def save_db(data):
    global in_memory_db
    with db_lock:
        in_memory_db = data
        try:
            temp_file = DB_FILE.with_suffix('.tmp')
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            temp_file.replace(DB_FILE)
        except Exception:
            pass

STATIC_DIR = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins"

# ── CYBER SECURITY & ANTI-DDOS RATE LIMITER ──
rate_limit_lock = threading.Lock()
ip_request_counts = {}
ip_banned_until = {}

def is_rate_limited(ip, max_requests=120, window_sec=60):
    now = time.time()
    with rate_limit_lock:
        if ip in ip_banned_until:
            if now < ip_banned_until[ip]:
                return True
            else:
                del ip_banned_until[ip]

        timestamps = ip_request_counts.get(ip, [])
        timestamps = [t for t in timestamps if now - t < window_sec]
        timestamps.append(now)
        ip_request_counts[ip] = timestamps

        if len(timestamps) > max_requests:
            ip_banned_until[ip] = now + 120 # 2 minute cooldown for abusive IPs
            return True
        return False

class GGWinsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        super().end_headers()
    def log_message(self, format, *args):
        pass

    def send_json(self, data, status=HTTPStatus.OK):
        payload = json.dumps(data).encode("utf-8")
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(payload)
        except Exception:
            pass

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            url_path = urllib.parse.unquote(parsed.path)
            query = urllib.parse.parse_qs(parsed.query)

            # ── 0. HEALTH CHECK ENDPOINT (FOR 24/7 WATCHDOG) ────────────
            if url_path == "/api/health" or url_path == "/health":
                self.send_json({"status": "healthy", "uptime": time.time(), "service": "GG WINS PRODUCTION"})
                return

            db = load_db()

            # ── 1. USER PROFILE API ─────────────────────────────────────
            if url_path == "/api/user-profile":
                user_id = query.get("userId", [None])[0]
                username = query.get("username", [None])[0]
                users = db.get("users", [])
                target = None
                if user_id:
                    target = next((u for u in users if u.get("id") == user_id), None)
                elif username:
                    target = next((u for u in users if u.get("username", "").lower() == username.lower()), None)

                if target:
                    clean_user = {k: v for k, v in target.items() if k != "password"}
                    self.send_json({"success": True, "user": clean_user})
                else:
                    self.send_json({"success": False, "message": "User not found"}, status=HTTPStatus.NOT_FOUND)
                return

            # ── 2. DEPOSITS & WITHDRAWALS & VIP LIST APIS ──────────────
            elif url_path == "/api/pending-deposits":
                pending = [d for d in db.get("deposits", []) if d.get("status") == "Pending"]
                self.send_json({"success": True, "deposits": pending})
                return
            elif url_path == "/api/all-deposits":
                self.send_json({"success": True, "deposits": db.get("deposits", [])})
                return
            elif url_path == "/api/pending-withdrawals":
                pending = [w for w in db.get("withdrawals", []) if w.get("status") == "Pending"]
                self.send_json({"success": True, "withdrawals": pending})
                return
            elif url_path == "/api/all-vip-requests":
                self.send_json({"success": True, "vip_requests": db.get("vip_requests", [])})
                return
            elif url_path == "/api/pending-vip-requests":
                pending = [v for v in db.get("vip_requests", []) if v.get("status") == "Pending"]
                self.send_json({"success": True, "vip_requests": pending})
                return
            elif url_path == "/api/all-withdrawals":
                self.send_json({"success": True, "withdrawals": db.get("withdrawals", [])})
                return

            # ── 3. USER REAL-TIME STATUS SYNC ───────────────────────────
            elif url_path == "/api/user-status":
                user_id = (query.get("userId", [None])[0] or "").strip()
                username = (query.get("username", [None])[0] or "").strip()
                email = (query.get("email", [None])[0] or "").strip()
                vip = (query.get("vipLevel", [None])[0] or "None").strip()

                try:
                    c_real = max(0.0, float(query.get("real", [0.0])[0] or 0.0))
                    c_demo = max(0.0, float(query.get("demo", [10000.0])[0] or 10000.0))
                    c_usdt = max(0.0, float(query.get("usdt", [0.0])[0] or 0.0))
                except Exception:
                    c_real, c_demo, c_usdt = 0.0, 10000.0, 0.0

                users = db.get("users", [])
                target_user = None
                if user_id:
                    target_user = next((u for u in users if u.get("id", "").upper() == user_id.upper()), None)
                if not target_user and username:
                    target_user = next((u for u in users if u.get("username", "").lower() == username.lower() or u.get("id", "").upper() == username.upper()), None)

                # If an active player visits with a valid session that was created on client, auto-sync/register into server database with their client balance!
                if not target_user and (user_id or username):
                    target_user = {
                        "id": user_id if user_id.upper().startswith("USER-") else f"USER-{os.urandom(4).hex().upper()}",
                        "username": username or user_id or "Player",
                        "email": email or f"{(username or user_id).lower().replace(' ', '')}@gmail.com",
                        "avatar": "👑",
                        "wallets": {"demo": c_demo, "real": c_real, "usdt": c_usdt},
                        "vipLevel": vip if vip != "null" and vip else "None",
                        "stats": {"gamesPlayed": 0, "totalWagered": 0.0, "totalWon": 0.0, "biggestWin": 0.0, "xp": 0, "referralCount": 0, "referralEarnings": 0.0},
                        "transactions": [],
                        "createdAt": int(time.time() * 1000),
                        "lastLogin": int(time.time() * 1000)
                    }
                    db.setdefault("users", []).append(target_user)
                    save_db(db)
                elif target_user:
                    # If target_user exists on server with zero balance but client has funds (from recent games / admin adjustment), preserve client funds!
                    tw = target_user.setdefault("wallets", {"demo": 10000.0, "real": 0.0, "usdt": 0.0})
                    if float(tw.get("real", 0.0)) == 0.0 and c_real > 0.0:
                        tw["real"] = c_real
                        save_db(db)

                if target_user:
                    target_user["lastLogin"] = int(time.time() * 1000)
                    self.send_json({
                        "success": True,
                        "user": {k: v for k, v in target_user.items() if k != "password"},
                        "wallets": target_user.get("wallets", {"demo": 10000.0, "real": 0.0, "usdt": 0.0}),
                        "vipLevel": target_user.get("vipLevel", "None"),
                        "stats": target_user.get("stats", {}),
                        "deposits": [d for d in db.get("deposits", []) if d.get("userId") == target_user.get("id") or d.get("username") == target_user.get("username")],
                        "withdrawals": [w for w in db.get("withdrawals", []) if w.get("userId") == target_user.get("id") or w.get("username") == target_user.get("username")],
                        "transactions": [t for t in db.get("transactions", []) if t.get("userId") == target_user.get("id") or t.get("username") == target_user.get("username")]
                    })
                else:
                    self.send_json({
                        "success": True,
                        "isGuest": True,
                        "deposits": [],
                        "withdrawals": [],
                        "transactions": []
                    })
                return

            # ── 4. ADMIN USER DETAILS & WALLET AUDIT ───────────────────
            elif url_path == "/api/admin/all-users":
                users = db.get("users", [])
                clean_list = []
                for u in users:
                    clean_list.append({
                        "id": u.get("id", ""),
                        "username": u.get("username", ""),
                        "email": u.get("email", ""),
                        "avatar": u.get("avatar", "👑"),
                        "referralCode": u.get("referralCode", ""),
                        "wallets": u.get("wallets", {"demo": 10000.0, "real": 0.0, "usdt": 0.0}),
                        "vipLevel": u.get("vipLevel", "None"),
                        "stats": u.get("stats", {}),
                        "createdAt": u.get("createdAt", 0),
                        "lastLogin": u.get("lastLogin", 0)
                    })
                self.send_json({"success": True, "users": clean_list, "total": len(clean_list)})
                return

            elif url_path == "/api/admin/user-details":
                raw_uid = (query.get("userId", [None])[0] or "").strip()
                raw_uname = (query.get("username", [None])[0] or "").strip()
                q_term = (raw_uid or raw_uname).replace("#", "").replace("@", "").strip()

                users = db.get("users", [])
                target = None

                if q_term:
                    # 1. Exact match on ID, username, referralCode, or email (case-insensitive)
                    target = next((u for u in users if u.get("id", "").upper() == q_term.upper() or str(u.get("referralCode", "")).upper() == q_term.upper() or u.get("username", "").lower() == q_term.lower() or u.get("email", "").lower() == q_term.lower()), None)
                    
                    # 2. Substring / partial match on ID or username or referralCode
                    if not target:
                        target = next((u for u in users if q_term.upper() in u.get("id", "").upper() or q_term.upper() in str(u.get("referralCode", "")).upper() or q_term.lower() in u.get("username", "").lower()), None)

                    # 3. If Admin enters an ID like USER-4DA4F6FA that was generated on client, auto-provision and inspect!
                    if not target:
                        is_user_id_format = q_term.upper().startswith("USER-") or len(q_term) >= 4
                        target = {
                            "id": q_term.upper() if q_term.upper().startswith("USER-") else f"USER-{os.urandom(4).hex().upper()}",
                            "username": q_term if not q_term.upper().startswith("USER-") else f"Player_{q_term[-4:]}",
                            "email": f"{q_term.lower().replace('-', '')}@gmail.com",
                            "referralCode": generate_referral_code(users),
                            "avatar": "👑",
                            "wallets": {"demo": 10000.0, "real": 0.0, "usdt": 0.0},
                            "vipLevel": "None",
                            "stats": {"gamesPlayed": 0, "totalWagered": 0.0, "totalWon": 0.0, "biggestWin": 0.0, "xp": 0, "referralCount": 0, "referralEarnings": 0.0},
                            "transactions": [],
                            "createdAt": int(time.time() * 1000),
                            "lastLogin": int(time.time() * 1000)
                        }
                        db.setdefault("users", []).append(target)
                        save_db(db)

                if not target:
                    self.send_json({"success": False, "message": f"No user found matching '{q_term}'. Please check the User ID or Username."}, status=HTTPStatus.NOT_FOUND)
                    return

                # Gather all deposits for this user
                user_deposits = [d for d in db.get("deposits", []) if d.get("userId") == target.get("id") or str(d.get("username", "")).lower() == target.get("username", "").lower()]
                # Gather all withdrawals for this user
                user_withdrawals = [w for w in db.get("withdrawals", []) if w.get("userId") == target.get("id") or str(w.get("username", "")).lower() == target.get("username", "").lower()]
                # Gather all VIP requests for this user
                user_vips = [v for v in db.get("vip_requests", []) if v.get("userId") == target.get("id") or str(v.get("username", "")).lower() == target.get("username", "").lower()]
                # Gather all game wagers
                user_wagers = [gw for gw in db.get("game_wagers", []) if gw.get("userId") == target.get("id") or str(gw.get("username", "")).lower() == target.get("username", "").lower()]
                
                # Gather all users who registered using this user's referral code/username
                target_uname = target.get("username", "").lower()
                target_uid = target.get("id", "").upper()
                target_ref = str(target.get("referralCode", "")).strip().lower()
                referred_users = []
                for u in users:
                    ref_by = str(u.get("referredBy", "")).strip().lower()
                    if ref_by and (ref_by == target_uname or ref_by == target_uid.lower() or (target_ref and ref_by == target_ref) or ref_by == f"gg-{target_uname}" or ref_by == f"gg_{target_uname}"):
                        referred_users.append({
                            "id": u.get("id", ""),
                            "username": u.get("username", ""),
                            "email": u.get("email", ""),
                            "referralCode": u.get("referralCode", ""),
                            "createdAt": u.get("createdAt", 0),
                            "wallets": u.get("wallets", {}),
                            "bonusAwarded": 50.0
                        })

                clean_user = {k: v for k, v in target.items() if k != "password"}
                clean_user.setdefault("stats", {})
                clean_user["stats"]["referralCount"] = max(int(clean_user["stats"].get("referralCount", 0)), len(referred_users))
                clean_user["stats"]["referralEarnings"] = max(float(clean_user["stats"].get("referralEarnings", 0.0)), len(referred_users) * 50.0)

                self.send_json({
                    "success": True,
                    "user": clean_user,
                    "deposits": user_deposits,
                    "withdrawals": user_withdrawals,
                    "vipRequests": user_vips,
                    "gameWagers": user_wagers,
                    "referredUsers": referred_users,
                    "transactions": target.get("transactions", [])
                })
                return

            # ── 5. ADMIN EMAIL CONFIG & LOGS ──────────────────────────
            elif url_path == "/api/admin/get-email-config":
                email_cfg = db.get("email_config", {})
                sender = (os.environ.get("ADMIN_EMAIL") or email_cfg.get("sender") or "ggwinssupport@gmail.com").strip()
                receiver = (os.environ.get("ADMIN_NOTIFY_RECEIVER") or email_cfg.get("receiver") or "ggwinssupport@gmail.com").strip()
                logs = db.get("email_logs", [])
                self.send_json({
                    "success": True,
                    "config": {
                        "sender": sender,
                        "receiver": receiver,
                        "updatedAt": email_cfg.get("updatedAt", 0)
                    },
                    "logs": logs[:40]
                })
                return

            # Static File Serving
            super().do_GET()
        except Exception as e:
            try:
                self.send_json({"error": "Internal Server Exception", "detail": str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            except Exception:
                pass

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        url_path = urllib.parse.unquote(parsed.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
        try:
            req_data = json.loads(body)
        except Exception:
            req_data = {}

        # Anti-XSS Sanitization
        for k, v in list(req_data.items()):
            if isinstance(v, str):
                req_data[k] = re.sub(r'<[^>]*>', '', v).strip()

        db = load_db()

        # ── 1. USER REGISTRATION ───────────────────────────────────
        if url_path == "/api/register":
            username = req_data.get("username", "").strip()
            email = req_data.get("email", "").strip().lower()
            password = req_data.get("password", "").strip()
            dob = req_data.get("dob", "").strip()
            mobile = req_data.get("mobile", "").strip()

            if not username or len(username) < 3:
                self.send_json({"success": False, "message": "Username must be at least 3 characters long."}, status=HTTPStatus.BAD_REQUEST)
                return
            
            # Strict Google / Gmail registration validation
            google_email_pattern = r"^[a-zA-Z0-9][a-zA-Z0-9.]{4,28}[a-zA-Z0-9]@(gmail\.com|googlemail\.com)$"
            if not email or not re.match(google_email_pattern, email, re.I):
                self.send_json({"success": False, "message": "⚠️ Only valid Google Account emails (@gmail.com) are accepted for registration on GG WINS."}, status=HTTPStatus.BAD_REQUEST)
                return
            if not password or len(password) < 6:
                self.send_json({"success": False, "message": "Password must be at least 6 characters long."}, status=HTTPStatus.BAD_REQUEST)
                return

            users = db.get("users", [])
            if any(u.get("username", "").lower() == username.lower() for u in users):
                import random
                clean_u = re.sub(r'[^a-zA-Z0-9]', '', username) or "Player"
                suggestions = [
                    f"{clean_u}_{random.randint(10, 99)}",
                    f"{clean_u}_Pro",
                    f"{clean_u}_777",
                    f"{clean_u}_Win"
                ]
                self.send_json({
                    "success": False,
                    "message": f"Username '{username}' is already taken. Please choose another or pick a suggested username below.",
                    "suggestions": suggestions
                }, status=HTTPStatus.CONFLICT)
                return
            if any(u.get("email", "").lower() == email for u in users):
                self.send_json({"success": False, "message": "An account with this email address already exists. Please Sign In."}, status=HTTPStatus.CONFLICT)
                return

            user_id = f"USER-{os.urandom(4).hex().upper()}"
            user_ref_code = generate_referral_code(users)
            emojis = ['🎮','🎰','🚀','💎','🦁','🐉','⚡','🌟','🔥','🎯','🏆','💫']
            avatar = emojis[ord(username[0]) % len(emojis)]

            ref_code = str(req_data.get("referralCode", "")).strip().upper()
            referred_by = None
            if ref_code:
                # Normalize ref_code (supports 'GG-XXXXXX', 'XXXXXX', User ID, or legacy username)
                clean_ref = ref_code.replace("GG-", "").replace("GG_", "").replace("@", "").strip()
                referrer_user = next((
                    u for u in users 
                    if str(u.get("referralCode", "")).upper() == ref_code
                    or str(u.get("referralCode", "")).upper() == f"GG-{clean_ref}"
                    or str(u.get("referralCode", "")).replace("GG-", "").upper() == clean_ref
                    or str(u.get("id", "")).upper() == ref_code
                    or str(u.get("username", "")).upper() == ref_code
                    or str(u.get("username", "")).upper() == clean_ref
                ), None)

                if referrer_user and referrer_user.get("id") != user_id:
                    referred_by = referrer_user["username"]
                    # Instantly credit ₹50.00 Real Cash to Referrer's Real Wallet!
                    referrer_user.setdefault("wallets", {"demo": 10000.0, "real": 0.0, "usdt": 0.0})
                    referrer_user["wallets"]["real"] = round(float(referrer_user["wallets"].get("real", 0.0)) + 50.0, 2)
                    referrer_user.setdefault("stats", {})
                    referrer_user["stats"]["referralCount"] = int(referrer_user["stats"].get("referralCount", 0)) + 1
                    referrer_user["stats"]["referralEarnings"] = round(float(referrer_user["stats"].get("referralEarnings", 0.0)) + 50.0, 2)

                    ref_tx_id = f"REF-{os.urandom(4).hex().upper()}"
                    ref_tx = {
                        "id": ref_tx_id,
                        "orderId": f"ORD-REF-{int(time.time())%1000000:06d}",
                        "userId": referrer_user["id"],
                        "username": referrer_user["username"],
                        "type": "deposit",
                        "wallet": "real",
                        "amount": 50.0,
                        "currency": "INR",
                        "method": "Refer & Earn Bonus",
                        "status": "Completed",
                        "description": f"🎁 Earned ₹50.00 instant referral cash! New player @{username} used your code {referrer_user.get('referralCode', ref_code)}",
                        "timestamp": int(time.time() * 1000)
                    }
                    referrer_user.setdefault("transactions", []).insert(0, ref_tx)
                    db.setdefault("transactions", []).insert(0, ref_tx)

            new_user = {
                "id": user_id,
                "username": username,
                "email": email,
                "password": hash_password(password),
                "avatar": avatar,
                "dob": dob,
                "mobile": mobile,
                "referredBy": referred_by,
                "referralCode": user_ref_code,
                "wallets": {
                    "demo": 10000.0,   # demo practice credits (non-withdrawable)
                    "real": 0.0,       # new users start with 0 Rs real money
                    "usdt": 0.0        # new users start with 0 USDT
                },
                "vipLevel": "None",    # no membership given to new users
                "stats": {
                    "gamesPlayed": 0,
                    "totalWagered": 0.0,
                    "totalWon": 0.0,
                    "biggestWin": 0.0,
                    "xp": 0,
                    "referralCount": 0,
                    "referralEarnings": 0.0
                },
                "transactions": [],
                "createdAt": int(time.time() * 1000),
                "lastLogin": int(time.time() * 1000)
            }

            db.setdefault("users", []).append(new_user)
            save_db(db)

            clean_user = {k: v for k, v in new_user.items() if k != "password"}
            self.send_json({
                "success": True,
                "user": clean_user,
                "message": f"Welcome to GG Wins, {username}! Your account is created (Real Balance: ₹0.00, Demo: ₹10,000.00)." + (f" Referral bonus applied for {referred_by}!" if referred_by else "")
            })
            return

        # ── 1.5. ADMIN TERMINAL AUTHENTICATION LOCK ─────────────────
        elif url_path == "/api/admin/login":
            admin_user = str(req_data.get("username", "")).strip()
            admin_pass = str(req_data.get("password", "")).strip()

            ALLOWED_ADMINS = {
                "ASRAR admin": "ArCot.co.in",
                "KABILAN": "ValENtino",
                "REHAN": "QuResHi"
            }

            if admin_user in ALLOWED_ADMINS and ALLOWED_ADMINS[admin_user] == admin_pass:
                token = hashlib.sha256(f"ggwins_admin_{admin_user}_{admin_pass}".encode()).hexdigest()
                self.send_json({
                    "success": True,
                    "message": f"Welcome, Authorized Admin {admin_user}!",
                    "admin": admin_user,
                    "token": token
                })
            else:
                self.send_json({
                    "success": False,
                    "message": "Access Denied: Invalid Admin Username or Master Passkey."
                }, status=HTTPStatus.UNAUTHORIZED)
            return

        # ── 2. USER SIGN IN (LOGIN) ─────────────────────────────────
        elif url_path == "/api/login":
            identifier = req_data.get("identifier", "").strip()
            password = req_data.get("password", "").strip()

            if not identifier or not password:
                self.send_json({"success": False, "message": "Please enter your username/email and password."}, status=HTTPStatus.BAD_REQUEST)
                return

            users = db.get("users", [])
            target = next((u for u in users if u.get("username", "").lower() == identifier.lower() or u.get("email", "").lower() == identifier.lower() or u.get("id", "").upper() == identifier.upper()), None)

            if not target:
                self.send_json({"success": False, "message": "No account found with this User ID, Username, or Email."}, status=HTTPStatus.UNAUTHORIZED)
                return

            # Verify password hash (or plain fallback for legacy)
            hashed = hash_password(password)
            if target.get("password") != hashed and target.get("password") != password:
                self.send_json({"success": False, "message": "Incorrect password. Please check and try again."}, status=HTTPStatus.UNAUTHORIZED)
                return

            target["lastLogin"] = int(time.time() * 1000)
            save_db(db)

            clean_user = {k: v for k, v in target.items() if k != "password"}
            self.send_json({
                "success": True,
                "user": clean_user,
                "message": f"Welcome back, {target['username']}! All your progress and balance are synced."
            })
            return

        # ── 2B. SYNC CLIENT USER STATE ──────────────────────────────
        elif url_path == "/api/sync-client-user":
            user_id = str(req_data.get("id", "")).strip()
            username = str(req_data.get("username", "")).strip()
            email = str(req_data.get("email", "")).strip()
            vip_level = str(req_data.get("vipLevel", "None")).strip()
            wallets = req_data.get("wallets")

            users = db.get("users", [])
            target = None
            if user_id:
                target = next((u for u in users if u.get("id", "").upper() == user_id.upper()), None)
            if not target and username:
                target = next((u for u in users if u.get("username", "").lower() == username.lower()), None)

            if not target and (user_id or username):
                target = {
                    "id": user_id if user_id.upper().startswith("USER-") else f"USER-{os.urandom(4).hex().upper()}",
                    "username": username or user_id or "Player",
                    "email": email or f"{(username or user_id).lower().replace(' ', '')}@gmail.com",
                    "avatar": "👑",
                    "wallets": {"demo": 10000.0, "real": 0.0, "usdt": 0.0},
                    "vipLevel": vip_level if vip_level != "null" and vip_level else "None",
                    "stats": {"gamesPlayed": 0, "totalWagered": 0.0, "totalWon": 0.0, "biggestWin": 0.0, "xp": 0, "referralCount": 0, "referralEarnings": 0.0},
                    "transactions": [],
                    "createdAt": int(time.time() * 1000),
                    "lastLogin": int(time.time() * 1000)
                }
                users.append(target)

            if target:
                target["lastLogin"] = int(time.time() * 1000)
                if email and not target.get("email"):
                    target["email"] = email
                if wallets and isinstance(wallets, dict):
                    target.setdefault("wallets", {"demo": 10000.0, "real": 0.0, "usdt": 0.0})
                    # Keep server real balance if already credited
                    if "demo" in wallets and target["wallets"].get("demo") is None:
                        target["wallets"]["demo"] = float(wallets["demo"])
                save_db(db)

            clean_user = {k: v for k, v in target.items() if k != "password"} if target else None
            self.send_json({"success": True, "user": clean_user})
            return

        # ── 3. UPDATE USER PROGRESS (STATS, WALLETS, VIP) ───────────
        elif url_path == "/api/update-user-progress":
            user_id = req_data.get("userId")
            username = req_data.get("username")
            users = db.get("users", [])
            target = None
            if user_id:
                target = next((u for u in users if u.get("id") == user_id), None)
            elif username:
                target = next((u for u in users if u.get("username", "").lower() == username.lower()), None)

            if target:
                if "wallets" in req_data and isinstance(req_data["wallets"], dict):
                    target.setdefault("wallets", {})
                    target["wallets"].update(req_data["wallets"])
                if "stats" in req_data and isinstance(req_data["stats"], dict):
                    target.setdefault("stats", {})
                    target["stats"].update(req_data["stats"])
                if "vipLevel" in req_data:
                    target["vipLevel"] = req_data["vipLevel"]
                save_db(db)

                clean_user = {k: v for k, v in target.items() if k != "password"}
                self.send_json({"success": True, "user": clean_user, "message": "Progress saved."})
            else:
                if "wallets" in req_data and isinstance(req_data["wallets"], dict):
                    db.setdefault("wallets", {})
                    db["wallets"].update(req_data["wallets"])
                    save_db(db)
                self.send_json({"success": True, "message": "Global progress saved."})
            return

        # ── 4. DEPOSIT REQUEST (LINKED TO USER) ─────────────────────
        elif url_path == "/api/deposit-request":
            amount = float(req_data.get("amount", 0))
            wallet_key = req_data.get("wallet", "real")
            method = req_data.get("method", "UPI Instant")
            utr = req_data.get("utr", "")
            sender_name = req_data.get("senderName", "Player")
            user_id = req_data.get("userId", "")
            username = req_data.get("username", "")
            email = req_data.get("email", "")

            if amount <= 0:
                self.send_json({"success": False, "message": "Invalid deposit amount"}, status=HTTPStatus.BAD_REQUEST)
                return

            tx_id = req_data.get("id") or f"DEP-{os.urandom(4).hex().upper()}"
            order_id = req_data.get("orderId") or f"ORD-DEP-{int(time.time())%1000000:06d}"
            coupon = req_data.get("coupon")
            bonus_amount = float(req_data.get("bonusAmount", 0))

            # If coupon was supplied but bonusAmount was 0, calculate 100% scaled coupon bonus
            if bonus_amount <= 0 and coupon:
                c_up = coupon.upper().strip()
                if c_up == "GG1675" and amount >= 1675:
                    pct = min(1.0, 0.5 + ((amount - 1675) / (5000 - 1675)) * 0.5) if amount < 5000 else 1.0
                    bonus_amount = round(amount * pct, 2)
            qr_number = int(req_data.get("qrNumber", 1))
            qr_target = req_data.get("qrTarget") or ("amdasrarbasha-1@oksbi" if qr_number == 1 else "kabilanr2210@okhdfcbank" if qr_number == 2 else "txchem@slc")
            qr_label = req_data.get("qrLabel") or f"QR {qr_number} ({qr_target})"

            deposit_record = {
                "id": tx_id,
                "orderId": order_id,
                "userId": user_id,
                "username": username or sender_name,
                "email": email,
                "wallet": wallet_key,
                "amount": amount,
                "bonusAmount": bonus_amount,
                "coupon": coupon,
                "creditedAmount": amount + bonus_amount,
                "currency": "USDT" if wallet_key == "usdt" else "INR",
                "method": method,
                "qrNumber": qr_number,
                "qrTarget": qr_target,
                "qrLabel": qr_label,
                "utr": utr or f"UPI{os.urandom(6).hex()[:12].upper()}",
                "senderName": sender_name,
                "status": "Pending",
                "timestamp": int(time.time() * 1000)
            }
            db.setdefault("deposits", []).insert(0, deposit_record)
            save_db(db)
            send_deposit_email_notification(deposit_record)
            self.send_json({"success": True, "deposit": deposit_record, "message": "Deposit request submitted successfully."})
            return

        # ── EMAIL NOTIFICATION CONFIGURATION ────────────────────────
        elif url_path == "/api/admin/set-email-config":
            sender = (req_data.get("sender") or "ggwinssupport@gmail.com").strip()
            password = req_data.get("password", "").strip()
            receiver = (req_data.get("receiver") or sender).strip()

            db.setdefault("email_config", {})
            db["email_config"]["sender"] = sender
            db["email_config"]["receiver"] = receiver
            if password:
                db["email_config"]["password"] = password.replace(" ", "")
            db["email_config"]["updatedAt"] = int(time.time() * 1000)
            save_db(db)
            self.send_json({"success": True, "message": f"Email alert target saved: {receiver}", "config": db["email_config"]})
            return

        # ── SEND TEST NOTIFICATION EMAIL ──────────────────────────
        elif url_path == "/api/admin/send-test-email":
            receiver = (req_data.get("receiver") or os.environ.get("ADMIN_NOTIFY_RECEIVER") or db.get("email_config", {}).get("receiver") or "ggwinssupport@gmail.com").strip()
            sub = "🧪 [GG WINS] Admin Email Notification Test"
            plain = f"GG WINS Email Notification Test\n\nThis is a test notification confirming that the GG WINS email alert engine is operating smoothly and connected to {receiver}.\n\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            html = f"""
            <div style="font-family: Arial, sans-serif; background-color: #0f172a; padding: 24px; color: #f8fafc; border-radius: 12px; max-width: 540px; margin: 0 auto; border: 1.5px solid #00e676;">
                <div style="text-align: center; margin-bottom: 16px;">
                    <h2 style="color: #00e676; margin: 0;">🧪 GG WINS – Email Test Alert</h2>
                    <p style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Live notification dispatch test from Admin Terminal.</p>
                </div>
                <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                    <p style="margin: 6px 0; font-size: 14px;"><strong>✅ SMTP Status:</strong> <span style="color: #00e676; font-weight: bold;">CONNECTED & OPERATIONAL</span></p>
                    <p style="margin: 6px 0; font-size: 14px;"><strong>📬 Alert Target:</strong> <span style="color: #38bdf8; font-weight: bold;">{receiver}</span></p>
                    <p style="margin: 6px 0; font-size: 13px; color: #94a3b8;"><strong>⏰ Dispatched At:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                <div style="text-align: center; margin-top: 20px;">
                    <a href="https://ggwins.site/host/index.html" style="background: linear-gradient(135deg, #ffd700, #ff8c00); color: #000; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 14px; display: inline-block;">
                        🔓 Return to Admin Terminal
                    </a>
                </div>
            </div>
            """
            dispatch_admin_email_alert(sub, plain, html, receiver_override=receiver, sync=False)
            self.send_json({"success": True, "message": f"Test notification email dispatched to {receiver}! Check your inbox in 5-10 seconds."})
            return

        # ── 4B. ADMIN UPDATE USER WALLET BALANCE ───────────────────
        elif url_path == "/api/admin/update-user-wallet":
            user_id = req_data.get("userId")
            username = req_data.get("username")
            real_bal = req_data.get("real")
            demo_bal = req_data.get("demo")
            usdt_bal = req_data.get("usdt")
            vip_level = req_data.get("vipLevel")
            reason = req_data.get("reason", "Admin Balance Adjustment")

            users = db.get("users", [])
            target = None
            if user_id:
                target = next((u for u in users if u.get("id", "").upper() == str(user_id).upper()), None)
            if not target and username:
                target = next((u for u in users if u.get("username", "").lower() == str(username).lower() or u.get("id", "").upper() == str(username).upper()), None)

            if not target:
                self.send_json({"success": False, "message": "User not found."}, status=HTTPStatus.NOT_FOUND)
                return

            target.setdefault("wallets", {"demo": 10000.0, "real": 0.0, "usdt": 0.0})
            old_real = float(target["wallets"].get("real", 0.0))

            if real_bal is not None:
                target["wallets"]["real"] = max(0.0, round(float(real_bal), 2))
            if demo_bal is not None:
                target["wallets"]["demo"] = max(0.0, round(float(demo_bal), 2))
            if usdt_bal is not None:
                target["wallets"]["usdt"] = max(0.0, round(float(usdt_bal), 2))
            if vip_level:
                target["vipLevel"] = vip_level
                if vip_level != "None":
                    target["isVIP"] = True
                    target["vipApproved"] = True

            diff = round(target["wallets"]["real"] - old_real, 2)
            adj_tx = {
                "id": f"ADM-{os.urandom(4).hex().upper()}",
                "orderId": f"ORD-ADM-{int(time.time())%1000000:06d}",
                "userId": target.get("id", ""),
                "username": target.get("username", ""),
                "type": "adjustment",
                "wallet": "real",
                "amount": diff,
                "newBalance": target["wallets"]["real"],
                "currency": "INR",
                "method": f"Admin Adjustment: {reason}",
                "status": "Completed",
                "description": f"Balance adjusted by Admin ({'+' if diff>=0 else ''}₹{diff:,.2f}) - Reason: {reason}",
                "timestamp": int(time.time() * 1000)
            }
            target.setdefault("transactions", []).insert(0, adj_tx)
            db.setdefault("transactions", []).insert(0, adj_tx)
            save_db(db)

            clean_user = {k: v for k, v in target.items() if k != "password"}
            self.send_json({
                "success": True,
                "message": f"Successfully updated wallet for @{target['username']}! Real INR: ₹{target['wallets']['real']:,.2f}",
                "user": clean_user
            })
            return

        # ── 5. APPROVE DEPOSIT ──────────────────────────────────────
        elif url_path == "/api/approve-deposit":
            dep_id = req_data.get("id")
            deposits = db.get("deposits", [])
            target_dep = next((d for d in deposits if d.get("id") == dep_id or d.get("orderId") == dep_id), None)

            if not target_dep:
                self.send_json({"success": False, "message": "Deposit not found"}, status=HTTPStatus.NOT_FOUND)
                return

            if target_dep.get("status") == "Completed":
                self.send_json({"success": True, "message": "Deposit already approved", "deposit": target_dep})
                return

            target_dep["status"] = "Completed"
            target_dep["approvedAt"] = int(time.time() * 1000)

            # Credit user wallet (Base deposit + coupon bonus = e.g. 100,000 + 100,000 = 200,000)
            wkey = target_dep.get("wallet", "real")
            amt = float(target_dep.get("amount", 0))
            bonus_amt = float(target_dep.get("bonusAmount", 0))
            
            # Recalculate bonus if coupon was applied
            if bonus_amt <= 0 and target_dep.get("coupon"):
                c_up = str(target_dep.get("coupon")).upper().strip()
                if c_up == "GG1675" and amt >= 1675:
                    pct = min(1.0, 0.5 + ((amt - 1675) / (5000 - 1675)) * 0.5) if amt < 5000 else 1.0
                    bonus_amt = round(amt * pct, 2)
                elif c_up == "INSTANT1500" and amt >= 2500:
                    bonus_amt = 1500.0
                target_dep["bonusAmount"] = bonus_amt

            total_credit = amt + bonus_amt
            target_dep["creditedAmount"] = total_credit

            db.setdefault("wallets", {})
            db["wallets"][wkey] = db["wallets"].get(wkey, 0.0) + total_credit

            # Credit specific user account if registered
            dep_user_id = target_dep.get("userId")
            dep_username = target_dep.get("username")
            users = db.get("users", [])
            user_obj = None
            if dep_user_id:
                user_obj = next((u for u in users if u.get("id") == dep_user_id), None)
            elif dep_username:
                user_obj = next((u for u in users if u.get("username", "").lower() == dep_username.lower()), None)

            if user_obj:
                user_obj.setdefault("wallets", {"demo": 10000.0, "real": 0.0, "usdt": 0.0})
                user_obj["wallets"][wkey] = user_obj["wallets"].get(wkey, 0.0) + total_credit
                user_obj.setdefault("transactions", []).insert(0, {
                    "id": target_dep["id"],
                    "orderId": target_dep.get("orderId", target_dep["id"]),
                    "type": "deposit",
                    "wallet": wkey,
                    "amount": total_credit,
                    "baseAmount": amt,
                    "bonusAmount": bonus_amt,
                    "coupon": target_dep.get("coupon"),
                    "currency": target_dep.get("currency", "INR"),
                    "method": target_dep.get("method", "UPI Instant"),
                    "status": "Completed",
                    "timestamp": target_dep.get("timestamp")
                })

            # Add to global transactions log
            db.setdefault("transactions", []).insert(0, {
                "id": target_dep["id"],
                "orderId": target_dep.get("orderId", target_dep["id"]),
                "userId": dep_user_id,
                "username": dep_username or target_dep.get("senderName"),
                "type": "deposit",
                "wallet": wkey,
                "amount": amt,
                "currency": target_dep.get("currency", "INR"),
                "method": target_dep.get("method", "UPI Instant"),
                "status": "Completed",
                "timestamp": target_dep.get("timestamp")
            })

            save_db(db)
            self.send_json({
                "success": True,
                "message": f"Deposit of {amt} approved and credited to user account.",
                "deposit": target_dep,
                "wallets": (user_obj["wallets"] if user_obj else db["wallets"])
            })
            return

        # ── 6. REJECT DEPOSIT ───────────────────────────────────────
        elif url_path == "/api/reject-deposit":
            dep_id = req_data.get("id")
            deposits = db.get("deposits", [])
            target_dep = next((d for d in deposits if d.get("id") == dep_id or d.get("orderId") == dep_id), None)

            if not target_dep:
                self.send_json({"success": False, "message": "Deposit not found"}, status=HTTPStatus.NOT_FOUND)
                return

            target_dep["status"] = "Rejected"
            target_dep["rejectedAt"] = int(time.time() * 1000)
            save_db(db)
            self.send_json({"success": True, "message": "Deposit request rejected", "deposit": target_dep})
            return

        # ── 7. WITHDRAWAL REQUEST (LINKED TO USER) ──────────────────
        elif url_path == "/api/withdraw-request":
            amount = float(req_data.get("amount", 0))
            wallet_key = req_data.get("wallet", "real")
            name = req_data.get("name", "").strip()
            account_no = req_data.get("accountNo", "").strip()
            ifsc = req_data.get("ifsc", "").strip().upper()
            aadhaar = req_data.get("aadhaar", "").strip()
            mobile = req_data.get("mobile", "").strip()
            address = req_data.get("address", "").strip()
            method = req_data.get("method", "IMPS Bank Transfer")
            user_id = req_data.get("userId", "")
            username = req_data.get("username", "")
            email = req_data.get("email", "")

            if amount <= 0:
                self.send_json({"success": False, "message": "Invalid withdrawal amount"}, status=HTTPStatus.BAD_REQUEST)
                return

            # Deduct balance from user account
            users = db.get("users", [])
            user_obj = None
            if user_id:
                user_obj = next((u for u in users if u.get("id") == user_id), None)
            elif username:
                user_obj = next((u for u in users if u.get("username", "").lower() == username.lower()), None)

            if user_obj:
                user_obj.setdefault("wallets", {})
                current_bal = user_obj["wallets"].get(wallet_key, 0.0)
                user_obj["wallets"][wallet_key] = max(0.0, current_bal - amount)

            db.setdefault("wallets", {})
            g_bal = db["wallets"].get(wallet_key, 0.0)
            db["wallets"][wallet_key] = max(0.0, g_bal - amount)

            wth_id = req_data.get("id") or f"WTH-{os.urandom(4).hex().upper()}"
            order_id = req_data.get("orderId") or f"ORD-WTH-{int(time.time())%1000000:06d}"
            wth_record = {
                "id": wth_id,
                "orderId": order_id,
                "userId": user_id,
                "username": username or name,
                "email": email,
                "wallet": wallet_key,
                "amount": amount,
                "currency": "USDT" if wallet_key == "usdt" else "INR",
                "method": method,
                "name": name or "Player",
                "accountNo": account_no,
                "ifsc": ifsc,
                "aadhaar": aadhaar,
                "mobile": mobile,
                "address": address,
                "status": "Pending",
                "timestamp": int(time.time() * 1000)
            }
            db.setdefault("withdrawals", []).insert(0, wth_record)

            # Record transaction
            tx_record = {
                "id": wth_id,
                "orderId": order_id,
                "userId": user_id,
                "username": username or name,
                "type": "withdraw",
                "wallet": wallet_key,
                "amount": amount,
                "currency": wth_record["currency"],
                "method": method,
                "destination": f"{name} ({account_no or address})",
                "status": "Pending",
                "timestamp": wth_record["timestamp"]
            }
            db.setdefault("transactions", []).insert(0, tx_record)
            if user_obj:
                user_obj.setdefault("transactions", []).insert(0, tx_record)

            save_db(db)
            send_withdrawal_email_notification(wth_record)
            self.send_json({
                "success": True,
                "withdrawal": wth_record,
                "wallets": (user_obj["wallets"] if user_obj else db["wallets"]),
                "message": "Withdrawal request submitted successfully."
            })
            return

        # ── 8. APPROVE WITHDRAWAL ───────────────────────────────────
        elif url_path == "/api/approve-withdrawal":
            wth_id = req_data.get("id")
            withdrawals = db.get("withdrawals", [])
            target_wth = next((w for w in withdrawals if w.get("id") == wth_id), None)

            if not target_wth:
                self.send_json({"success": False, "message": "Withdrawal request not found"}, status=HTTPStatus.NOT_FOUND)
                return

            if target_wth.get("status") == "Completed":
                self.send_json({"success": True, "message": "Withdrawal already approved", "withdrawal": target_wth})
                return

            target_wth["status"] = "Completed"
            target_wth["approvedAt"] = int(time.time() * 1000)

            for tx in db.get("transactions", []):
                if tx.get("id") == wth_id:
                    tx["status"] = "Completed"

            save_db(db)
            self.send_json({
                "success": True,
                "message": f"Withdrawal {wth_id} marked as PAID and approved!",
                "withdrawal": target_wth,
                "wallets": db["wallets"]
            })
            return

        # ── 9. REJECT & REFUND WITHDRAWAL ───────────────────────────
        elif url_path == "/api/reject-withdrawal":
            wth_id = req_data.get("id")
            withdrawals = db.get("withdrawals", [])
            target_wth = next((w for w in withdrawals if w.get("id") == wth_id), None)

            if not target_wth:
                self.send_json({"success": False, "message": "Withdrawal request not found"}, status=HTTPStatus.NOT_FOUND)
                return

            if target_wth.get("status") == "Rejected":
                self.send_json({"success": True, "message": "Withdrawal already rejected", "withdrawal": target_wth})
                return

            target_wth["status"] = "Rejected"
            target_wth["rejectedAt"] = int(time.time() * 1000)

            # Refund amount back to user's wallet
            wkey = target_wth.get("wallet", "real")
            amt = float(target_wth.get("amount", 0))

            wth_user_id = target_wth.get("userId")
            wth_username = target_wth.get("username")
            users = db.get("users", [])
            user_obj = None
            if wth_user_id:
                user_obj = next((u for u in users if u.get("id") == wth_user_id), None)
            elif wth_username:
                user_obj = next((u for u in users if u.get("username", "").lower() == wth_username.lower()), None)

            if user_obj:
                user_obj.setdefault("wallets", {})
                user_obj["wallets"][wkey] = user_obj["wallets"].get(wkey, 0.0) + amt

            db.setdefault("wallets", {})
            db["wallets"][wkey] = db["wallets"].get(wkey, 0.0) + amt

            for tx in db.get("transactions", []):
                if tx.get("id") == wth_id:
                    tx["status"] = "Rejected (Refunded)"

            save_db(db)
            self.send_json({
                "success": True,
                "message": f"Withdrawal {wth_id} rejected and funds refunded to user wallet.",
                "withdrawal": target_wth,
                "wallets": (user_obj["wallets"] if user_obj else db["wallets"])
            })
            return

        # ── 9.5. CANCEL WITHDRAWAL (BY USER WITH AUTO-REFUND) ───────
        elif url_path == "/api/cancel-withdrawal":
            wth_id = req_data.get("id")
            withdrawals = db.get("withdrawals", [])
            target_wth = next((w for w in withdrawals if w.get("id") == wth_id or w.get("orderId") == wth_id), None)

            if not target_wth:
                self.send_json({"success": False, "message": "Withdrawal request not found"}, status=HTTPStatus.NOT_FOUND)
                return

            if target_wth.get("status") in ["Completed", "Cancelled by User"]:
                self.send_json({"success": True, "message": f"Withdrawal is already {target_wth.get('status')}", "withdrawal": target_wth})
                return

            target_wth["status"] = "Cancelled by User"
            target_wth["cancelledAt"] = int(time.time() * 1000)

            # Refund amount back to user's wallet
            wkey = target_wth.get("wallet", "real")
            amt = float(target_wth.get("amount", 0))

            wth_user_id = target_wth.get("userId")
            wth_username = target_wth.get("username")
            users = db.get("users", [])
            user_obj = None
            if wth_user_id:
                user_obj = next((u for u in users if u.get("id") == wth_user_id), None)
            elif wth_username:
                user_obj = next((u for u in users if u.get("username", "").lower() == wth_username.lower()), None)

            if user_obj:
                user_obj.setdefault("wallets", {"demo": 10000.0, "real": 0.0, "usdt": 0.0})
                user_obj["wallets"][wkey] = user_obj["wallets"].get(wkey, 0.0) + amt
                for tx in user_obj.get("transactions", []):
                    if tx.get("id") == wth_id or tx.get("orderId") == wth_id:
                        tx["status"] = "Cancelled (Refunded)"

            db.setdefault("wallets", {})
            db["wallets"][wkey] = db["wallets"].get(wkey, 0.0) + amt

            for tx in db.get("transactions", []):
                if tx.get("id") == wth_id or tx.get("orderId") == wth_id:
                    tx["status"] = "Cancelled (Refunded)"

            save_db(db)
            self.send_json({
                "success": True,
                "message": f"Withdrawal {wth_id} cancelled and ₹{amt:.2f} refunded back to balance!",
                "withdrawal": target_wth,
                "wallets": (user_obj["wallets"] if user_obj else db["wallets"])
            })
            return

        # ── 10. CLEAR ALL TEST DATA ─────────────────────────────────
        elif url_path == "/api/clear-data":
            fresh_db = {
                "users": [],
                "wallets": {"demo": 10000.0, "real": 0.0, "usdt": 0.0},
                "deposits": [],
                "withdrawals": [],
                "transactions": []
            }
            save_db(fresh_db)
            self.send_json({"success": True, "message": "All test history and accounts cleared. Database is 100% clean."})
            return

                # ── 11. VIP UPGRADE REQUEST (SUBMITTED BY USER) ───────────
        elif url_path == "/api/vip-request":
            tier = req_data.get("tier", "gold")
            tier_name = req_data.get("tierName", "Gold VIP")
            amount = float(req_data.get("amount", 0))
            utr = req_data.get("utr", "").strip()
            user_id = req_data.get("userId", "")
            username = req_data.get("username", "")
            method = req_data.get("method", "UPI Instant")

            vip_id = "VIP-" + str(int(time.time()))[-6:]
            order_id = "ORD-VIP-" + str(int(time.time() * 1000))[-6:]

            vip_record = {
                "id": vip_id,
                "orderId": order_id,
                "userId": user_id,
                "username": username or "Player",
                "tier": tier,
                "tierName": tier_name,
                "amount": amount,
                "utr": utr,
                "method": method,
                "status": "Pending",
                "timestamp": int(time.time() * 1000)
            }

            db.setdefault("vip_requests", []).insert(0, vip_record)
            save_db(db)

            self.send_json({
                "success": True,
                "message": f"VIP request for {tier_name} submitted successfully. Awaiting Admin approval.",
                "vip_request": vip_record
            })
            return

        # ── 12. APPROVE VIP REQUEST (ADMIN HOST) ───────────────────
        elif url_path == "/api/approve-vip":
            req_id = req_data.get("id")
            vip_list = db.get("vip_requests", [])
            target = next((v for v in vip_list if v.get("id") == req_id or v.get("orderId") == req_id), None)

            if not target:
                self.send_json({"success": False, "message": "VIP request not found"}, status=HTTPStatus.NOT_FOUND)
                return

            now_ms = int(time.time() * 1000)
            target["status"] = "Completed"
            target["approvedAt"] = now_ms
            # 1-Month (30 Days) Expiration timestamp
            expires_at = now_ms + (30 * 24 * 60 * 60 * 1000)
            target["expiresAt"] = expires_at

            # Upgrade user's VIP Level and Expiration in database
            target_user_id = target.get("userId")
            target_username = target.get("username")
            assigned_vip = target.get("tierName", "Gold VIP").replace(" (1 Month)", "")

            users = db.get("users", [])
            user_obj = None
            if target_user_id:
                user_obj = next((u for u in users if u.get("id") == target_user_id), None)
            elif target_username:
                user_obj = next((u for u in users if u.get("username", "").lower() == target_username.lower()), None)

            if user_obj:
                user_obj["vipLevel"] = assigned_vip
                user_obj["vipExpiresAt"] = expires_at
            else:
                user_obj = {
                    "id": target_user_id or ("USER-" + str(int(time.time()))[-6:]),
                    "username": target_username or "Player",
                    "vipLevel": assigned_vip,
                    "vipExpiresAt": expires_at,
                    "joined": now_ms,
                    "transactions": []
                }
                users.append(user_obj)

            user_obj.setdefault("transactions", []).insert(0, {
                "id": target["id"],
                "orderId": target.get("orderId", target["id"]),
                "type": "vip_upgrade",
                "wallet": "real",
                "amount": target.get("amount", 0),
                "currency": "INR",
                "method": f"VIP Upgrade to {assigned_vip}",
                "status": "Completed",
                "timestamp": target.get("timestamp")
            })

            save_db(db)
            self.send_json({
                "success": True,
                "message": f"VIP Upgrade to {assigned_vip} approved for {target_username or 'User'}!",
                "vip_request": target,
                "vipLevel": assigned_vip
            })
            return

        # ── 13. REJECT VIP REQUEST (ADMIN HOST) ────────────────────
        elif url_path == "/api/reject-vip":
            req_id = req_data.get("id")
            vip_list = db.get("vip_requests", [])
            target = next((v for v in vip_list if v.get("id") == req_id or v.get("orderId") == req_id), None)

            if not target:
                self.send_json({"success": False, "message": "VIP request not found"}, status=HTTPStatus.NOT_FOUND)
                return

            target["status"] = "Rejected"
            target["rejectedAt"] = int(time.time() * 1000)
            save_db(db)
            self.send_json({"success": True, "message": "VIP request rejected", "vip_request": target})
            return

        self.send_json({"success": False, "message": "Endpoint not found"}, status=HTTPStatus.NOT_FOUND)

    def translate_path(self, path):
        path = urllib.parse.unquote(path.split('?', 1)[0].split('#', 1)[0])
        
        if path in ("/host", "/host/", "/admin", "/admin/"):
            return str(ADMIN_DIR / "index.html")
        elif path.startswith("/host/") or path.startswith("/admin/"):
            prefix = "/host/" if path.startswith("/host/") else "/admin/"
            rel = path[len(prefix):].lstrip("/")
            target = ADMIN_DIR / rel
            return str(target)
        else:
            if path == "/" or path == "":
                return str(USER_DIR / "index.html")
            rel = path.lstrip("/")
            target = USER_DIR / rel
            return str(target)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

def run_https(port=8443):
    cert_file = CERT_DIR / "cert.pem"
    key_file = CERT_DIR / "key.pem"
    if not cert_file.exists() or not key_file.exists():
        return
    try:
        httpd = http.server.ThreadingHTTPServer(("0.0.0.0", port), GGWinsHandler)
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile=str(cert_file), keyfile=str(key_file))
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
        print(f"[HTTPS SERVER] https://0.0.0.0:{port}/")
        sys.stdout.flush()
        httpd.serve_forever()
    except Exception as e:
        print(f"[HTTPS] Optional local SSL not started: {e}")

def run_http(port=8000):
    httpd = http.server.ThreadingHTTPServer(("0.0.0.0", port), GGWinsHandler)
    print(f"[HTTP SERVER]  http://0.0.0.0:{port}/")
    sys.stdout.flush()
    httpd.serve_forever()

if __name__ == "__main__":
    main_port = int(os.environ.get("PORT", 8000))
    
    t_https = threading.Thread(target=run_https, args=(8443,), daemon=True)
    t_http = threading.Thread(target=run_http, args=(main_port,), daemon=True)

    t_https.start()
    t_http.start()

    print("==================================================")
    print(f" [GG WINS] 24/7 PRODUCTION SERVER ONLINE (PORT {main_port})")
    print(f" Web & API Engine: http://0.0.0.0:{main_port}/")
    print(" Admin Terminal:   /host/index.html")
    print("==================================================")
    sys.stdout.flush()

    t_http.join()
