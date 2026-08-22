with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

import re
reg_match = re.search(r'function handleRegister|function handleLogin|submit-btn|register-form|login-form', s, re.I)
if reg_match:
    print("REG/LOGIN CODE IN SCRIPT.JS:")
    print(s[reg_match.start()-50:reg_match.start()+1200].encode('ascii', errors='replace').decode('ascii'))