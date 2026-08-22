# Let's inspect task-3865.log to see what requests the server is getting
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\.system_generated\tasks\task-3865.log", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()
print("".join(lines[-25:]))