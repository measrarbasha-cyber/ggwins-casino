with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

import re
# Find carousel logic
car_match = re.search(r'//\s*Carousel.*?function', s, re.DOTALL)
if car_match:
    print("CAROUSEL LOGIC:")
    print(car_match.group(0)[:800].encode('ascii', errors='replace').decode('ascii'))

# Find chat logic
chat_match = re.search(r'//\s*Live Chat|function sendChatMessage', s, re.DOTALL)
if chat_match:
    print("CHAT LOGIC:")
    print(s[chat_match.start():chat_match.start()+1000].encode('ascii', errors='replace').decode('ascii'))