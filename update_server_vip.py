# Python script to add VIP Club backend endpoints to server.py
import re

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py", "r", encoding="utf-8") as f:
    s = f.read()

# 1. Add GET /api/all-vip-requests
get_vip_endpoint = """        elif url_path == "/api/all-vip-requests":
            self.send_json({"success": True, "vip_requests": db.get("vip_requests", [])})
            return
        elif url_path == "/api/pending-vip-requests":
            pending = [v for v in db.get("vip_requests", []) if v.get("status") == "Pending"]
            self.send_json({"success": True, "vip_requests": pending})
            return"""

if "api/all-vip-requests" not in s:
    s = s.replace('elif url_path == "/api/all-withdrawals":', get_vip_endpoint + '\n        elif url_path == "/api/all-withdrawals":')

# 2. Add POST /api/vip-request, /api/approve-vip, /api/reject-vip
post_vip_endpoints = """        # ── 11. VIP UPGRADE REQUEST (SUBMITTED BY USER) ───────────
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

            target["status"] = "Completed"
            target["approvedAt"] = int(time.time() * 1000)

            # Upgrade user's VIP Level in database
            target_user_id = target.get("userId")
            target_username = target.get("username")
            assigned_vip = target.get("tierName", "Gold VIP")

            users = db.get("users", [])
            user_obj = None
            if target_user_id:
                user_obj = next((u for u in users if u.get("id") == target_user_id), None)
            elif target_username:
                user_obj = next((u for u in users if u.get("username", "").lower() == target_username.lower()), None)

            if user_obj:
                user_obj["vipLevel"] = assigned_vip
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
            return"""

if "api/vip-request" not in s:
    s = s.replace('self.send_json({"success": False, "message": "Endpoint not found"}, status=HTTPStatus.NOT_FOUND)', post_vip_endpoints + '\n\n        self.send_json({"success": False, "message": "Endpoint not found"}, status=HTTPStatus.NOT_FOUND)')

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py", "w", encoding="utf-8") as f:
    f.write(s)

print("Updated server.py with VIP request, approve, and reject endpoints!")
