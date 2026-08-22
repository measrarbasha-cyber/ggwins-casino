import os, re, shutil

scratch_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js"
brain_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\wallet.js"

with open(scratch_path, "r", encoding="utf-8") as f:
    s = f.read()

# Update initial balance config
s = s.replace("initial: 0.00,\n      description: 'Deposited real INR balance", "initial: 25000.00,\n      description: 'Deposited real INR balance")
s = s.replace("initial: 0.00,\n      description: 'Tether USD", "initial: 500.00,\n      description: 'Tether USD")
s = s.replace("demo: 10000.00,  // ₹10,000 demo practice balance only\n        real: 0.00,      // ₹0 — must deposit to get real money\n        usdt: 0.00       // ₹0 — must deposit to get USDT", "demo: 10000.00,\n        real: 25000.00,\n        usdt: 500.00")

with open(scratch_path, "w", encoding="utf-8") as f:
    f.write(s)

shutil.copy2(scratch_path, brain_path)
print("SUCCESS: wallet.js updated with funded Real INR and USDT Crypto initial balances!")