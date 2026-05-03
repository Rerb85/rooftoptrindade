import re, time, urllib.parse, json
from pathlib import Path
import urllib.request
text = Path('index.html').read_text(encoding='utf-8')
start = text.find('const places = [')
end = text.find('];', start)
block = text[start:end]
entries = []
for line in block.splitlines():
    if 'name:' in line and 'lat:' in line and 'lng:' in line:
        m = re.search(r"name:'([^']+)'", line)
        n = re.search(r'lat:([\-0-9\.]+)', line)
        o = re.search(r'lng:([\-0-9\.]+)', line)
        if m and n and o:
            entries.append((m.group(1), n.group(1), o.group(1), line.strip()))
for name, lat, lng, line in entries:
    query = urllib.parse.quote(f"{name}, Florianópolis, Brazil")
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=3&addressdetails=0"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; CopilotBot/1.0)'})
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            data = json.load(res)
    except Exception as e:
        print(f'ERROR\t{name}\t{e}')
        data = []
    if data:
        print(f"{name}\t{lat}\t{lng}\t->\t{data[0]['lat']}\t{data[0]['lon']}\t{data[0].get('display_name','')}")
        if len(data) > 1:
            for alt in data[1:3]:
                print(f"  alt -> {alt['lat']}\t{alt['lon']}\t{alt.get('display_name','')}")
    else:
        print(f"{name}\t{lat}\t{lng}\t->\tNORESULT")
    time.sleep(1)
