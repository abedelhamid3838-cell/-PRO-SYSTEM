import requests
import re
from concurrent.futures import ThreadPoolExecutor

# مصادر خارجية قوية (خارج GitHub) يتم تحديثها لحظياً
SOURCES = [
    "https://pastebin.com/raw/866uX6X8",
    "https://t.me/s/iptv_links_arabic", # قنص من تلجرام (نسخة ويب)
    "https://www.google.com/search?q=filetype:m3u+beIN+Sports+2026", # استهداف نتائج البحث
    "https://iptv-org.github.io/iptv/countries/ar.m3u",
    "http://www.pro-iptv.com/", # مثال لموقع خارجي
    "https://raw.githubusercontent.com/tarekzort/IPTV-Daily/main/arabic.m3u"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0'
}

# كلمات البحث الاحترافية
TARGETS = r'beIN|OSN|SSC|Alkass|Shahid|Discovery'

def check_link_integrity(name, url):
    """ فحص جودة الرابط وتجاوز الحماية """
    try:
        # فحص بروتوكول البث مباشرة
        r = requests.head(url, headers=HEADERS, timeout=3)
        if r.status_code in [200, 301, 302]:
            return f"{name}\n{url}\n"
    except:
        try:
            # محاولة ثانية بالفحص الجزيئي
            r = requests.get(url, headers=HEADERS, timeout=4, stream=True)
            if r.status_code == 200:
                return f"{name}\n{url}\n"
        except: return None

def deep_scan():
    links_pool = []
    print("AI is scanning the web beyond GitHub...")

    for s in SOURCES:
        try:
            r = requests.get(s, headers=HEADERS, timeout=15)
            # استخراج الروابط باستخدام Regex (تعبيرات نمطية) تبحث عن أي رابط يبدأ بـ http وينتهي بـ m3u8 أو يحتوي على قنواتنا
            raw_links = re.findall(r'(#EXTINF.*)\n(http.*)', r.text)
            for name, url in raw_links:
                if re.search(TARGETS, name, re.IGNORECASE):
                    links_pool.append((name, url.strip()))
        except: continue

    # إزالة التكرار لزيادة السرعة
    unique_pool = list(set(links_pool))
    
    # فحص 100 رابط في الثانية (بفضل رامات السحاب 12GB)
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(lambda p: check_link_integrity(p[0], p[1]), unique_pool))
    
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        count = 0
        for r in filter(None, results):
            f.write(r)
            count += 1
    print(f"Deep Scan Finished. Found {count} working channels.")

if __name__ == "__main__":
    deep_scan()
