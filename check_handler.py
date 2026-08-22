srv_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py"
with open(srv_path, "r", encoding="utf-8") as f:
    s = f.read()

# Let's inspect where GGWinsHandler handles do_GET and translate_path
print("Handler in server.py:")
idx = s.find("class GGWinsHandler")
print(s[idx:idx+1500])