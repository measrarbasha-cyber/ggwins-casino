with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py", "r", encoding="utf-8") as f:
    s = f.read()

old_block = """            if user_obj:
                user_obj["vipLevel"] = assigned_vip
                user_obj["vipExpiresAt"] = expires_at
            else:
                new_user = {
                    "id": target_user_id or ("USER-" + str(int(time.time()))[-6:]),
                    "username": target_username or "Player",
                    "vipLevel": assigned_vip,
                    "vipExpiresAt": expires_at,
                    "joined": now_ms
                }
                users.append(new_user)
                user_obj["vipExpiresAt"] = expires_at
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
                })"""

new_block = """            if user_obj:
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
            })"""

s = s.replace(old_block, new_block)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: Fixed approve-vip assignment bug!")
