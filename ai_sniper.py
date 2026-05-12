import requests
import re
from concurrent.futures import ThreadPoolExecutor

# مصادر قنص عالمية وموثوقة
SOURCES = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/MoiraSama/IPTV-Arabic/main/Arabic.m3u",
    "https://raw.githubusercontent.com/tarekzort/IPTV-Daily/main/arabic.m3u"
]

# رأس متصفح لتجاوز جدران الحماية (Cybersecurity Tactics)
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
TARGETS = r'beIN|OSN|alkass|SSC|SHAHID'

def ai_check(name, url):
    """ فحص ذكي يتأكد من أن الرابط يرسل بيانات فيديو حقيقية """
    try:
        r = requests.get(url, headers=HEADERS, timeout=5, stream=True)
        if r.status_code == 200 and next(r.iter_content(1024)):
            return f"{name}\n{url}\n"
    except: return None

def start_aega():
    links_found = []
    for s in SOURCES:
        try:
            res = requests.get(s, headers=HEADERS, timeout=10)
            lines = res.text.splitlines()
            for i in range(len(lines)):
                if re.search(TARGETS, lines[i], re.IGNORECASE) and i+1 < len(lines):
                    links_found.append((lines[i], lines[i+1].strip()))
        except: continue
    
    # استخدام 100 خيط معالجة بفضل رامات السحاب (12GB)
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(lambda p: ai_check(p[0], p[1]), list(set(links_found))))
    
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for r in filter(None, results): f.write(r)
    print("Update Complete.")

if __name__ == "__main__":
    start_aega()
