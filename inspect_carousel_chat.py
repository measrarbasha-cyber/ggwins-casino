with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

# Let's inspect carousel functions
c_idx = s.find("function goToSlide")
if c_idx != -1:
    print("CAROUSEL FUNCTIONS:")
    print(s[c_idx:c_idx+600].encode('ascii', errors='replace').decode('ascii'))

# Let's inspect chat functions
ch_idx = s.find("function sendChat")
if ch_idx == -1:
    ch_idx = s.find("chat-form")
if ch_idx != -1:
    print("\nCHAT FUNCTIONS:")
    print(s[ch_idx:ch_idx+800].encode('ascii', errors='replace').decode('ascii'))