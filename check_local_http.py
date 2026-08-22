import urllib.request
res = urllib.request.urlopen("http://127.0.0.1:8000/index.html")
content = res.read().decode('utf-8')
print(f"Local HTTP index length: {len(content)}")
print(f"Contains hero-carousel: {'hero-carousel' in content}")