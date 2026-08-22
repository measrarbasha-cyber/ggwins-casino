with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py", "r", encoding="utf-8") as f:
    srv = f.read()

import re
root_match = re.search(r'STATIC_DIR|DIRECTORY|os\.getcwd|DOCUMENT_ROOT|BASE_DIR|SimpleHTTPRequestHandler', srv)
if root_match:
    print(srv[root_match.start()-50:root_match.start()+500])
else:
    print("No direct match, showing first 500 chars:")
    print(srv[:500])