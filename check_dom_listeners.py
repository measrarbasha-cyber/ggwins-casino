with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

import re

# Look for direct addEventListener calls on dom objects without null checks
add_listeners = re.findall(r'dom\.[a-zA-Z0-9_]+\.addEventListener', s)
print(f"Total dom addEventListener calls: {len(add_listeners)}")
for al in set(add_listeners):
    print(al)