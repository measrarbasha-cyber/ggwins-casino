import os, time

directory = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins"
now = time.time()
print("Files in ggwins modified recently:")
for root, dirs, files in os.walk(directory):
    for f in files:
        path = os.path.join(root, f)
        mtime = os.path.getmtime(path)
        age_mins = (now - mtime) / 60
        if age_mins < 120:
            print(f"{os.path.relpath(path, directory)}: modified {age_mins:.1f} mins ago ({time.ctime(mtime)})")