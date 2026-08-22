with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

start = idx.find('<div class="hero-carousel"')
end = idx.find('</div><!-- /.hero-carousel -->', start)
if end == -1:
    end = idx.find('</section>', start)
print(idx[start:end+50].encode('ascii', errors='replace').decode('ascii'))