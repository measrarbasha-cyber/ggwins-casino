# Let's verify that index.html, vip.html, and tournaments.html all have consistent banner, live chat, and game structures
import os

files = ['index.html', 'tournaments.html', 'vip.html', 'vip-lounge.html']
for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as fp:
            c = fp.read()
            has_chat = 'chat-sidebar' in c or 'chat-messages' in c or 'toggleChat' in c or 'ai-chat' in c
            print(f"{f}: Size={len(c)} B, Chat={'YES' if has_chat else 'NO'}")