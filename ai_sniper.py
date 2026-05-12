import requests
import re
from concurrent.futures import ThreadPoolExecutor

# كلمات البحث (Dorks) لجعل الذكاء الاصطناعي يجد روابط جديدة في الويب
DORKS = [
    "https://www.bing.com/search?q=index+of+m3u+beIN+Sports+2026",
    "https://www.bing.com/search?q=SSC+Channels+m3u8+playlist+github",
    "https://www.bing.com/search?q=OSN+iptv+link+m3u+free"
]

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def deep_scan(url):
    """ الدخول لعمق المواقع واستخراج أي رابط بث """
    links = []
    try:
        # الدخول للموقع وجلب الكود المصدري
        content = requests.get(url, headers=HEADERS, timeout=10).text
        # استخراج أي رابط يبدأ بـ http وينتهي بـ m3u8 أو يحتوي على كلمة stream
        raw_links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        
        for link in raw_links:
            if "m3u8" in link or ".ts" in link:
                # محاولة استخراج اسم للقناة من الرابط نفسه
                name = link.split('/')[-1].split('?')[0]
                links.append(f"#EXTINF:-1, {name}\n{link}\n")
    except: pass
    return links

def run_aega_mega_scanner():
    print("AEGA AI is now crawling the web...")
    all_found = []
    
    # الخطوة 1: جلب روابط المواقع من محرك البحث
    sites_to_scan = []
    for dork in DORKS:
        try:
            r = requests.get(dork, headers=HEADERS, timeout=10)
            # استخراج الروابط الخارجية من نتائج البحث
            urls = re.findall(r'href="(http[s]?://.*?)"', r.text)
            sites_to_scan.extend([u for u in urls if "bing.com" not in u and "microsoft" not in u])
        except: continue

    # الخطوة 2: مسح المواقع المستخرجة (50 موقع في نفس الوقت)
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(deep_scan, list(set(sites_to_scan))))
        for r in results:
            all_found.extend(r)

    # الخطوة 3: الكتابة النهائية (حتى لو لم نجد الكثير، سنكتب ما وجدناه)
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        # إذا كانت القائمة فارغة، سنضيف روابط احتياطية ثابتة لضمان عمل الملف
        if not all_found:
            f.write("#EXTINF:-1, Backup-Channel\nhttps://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u\n")
        else:
            for item in list(set(all_found)):
                f.write(item)
    
    print(f"Success! Found {len(all_found)} potential streams.")

if __name__ == "__main__":
    run_aega_mega_scanner()
    
