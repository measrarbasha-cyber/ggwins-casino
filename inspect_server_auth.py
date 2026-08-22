with open("server.py", "r", encoding="utf-8") as f:
    srv = f.read()

import re
reg_route = re.search(r'def handle_register|def handle_login|/api/register|/api/login', srv, re.I)
if reg_route:
    print("SERVER.PY AUTH HANDLERS:")
    print(srv[reg_route.start()-50:reg_route.start()+2500].encode('ascii', errors='replace').decode('ascii'))