import requests
import re
from concurrent.futures import ThreadPoolExecutor

# كلمات البحث المتقدمة (Dorks) لاستهداف القنوات العربية والأوروبية
SEARCH_QUERIES = [
    "https://www.bing.com/search?q=index+of+m3u+Arabic+France+Europe+2026",
    "https://www.bing.com/search?q=playlist+m3u8+Bein+Canal+Plus+Sky+Sports",
    "https://www.bing.com/search?q=iptv+links+daily+updated+m3u8"
]

# الفلتر الذكي للدول المستهدفة
# العربي، الفرنسي، الإسباني، الألماني، الإنجليزي
TARGET_LANGS = r'AR|FR|ES|DE|EN|UK|BEIN|CANAL|SKY|OSN'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def deep_extract(site_url):
    """ استخراج الروابط من المواقع التي تظهر في نتائج البحث """
    found = []
    try:
        # جلب كود المصدر للموقع
        r = requests.get(site_url, headers=HEADERS, timeout=8)
        # البحث عن أنماط روابط البث (http...m3u8)
        streams = re.findall(r'(#EXTINF.*)\n(http.*)', r.text)
        for name, link in streams:
            if re.search(TARGET_LANGS, name, re.IGNORECASE):
                found.append(f"{name}\n{link.strip()}\n")
    except:
        pass
    return found

def run_global_scanner():
    print("AEGA AI: Scanning World Channels (Arab & Europe)...")
    sites_to_visit = []
    
    # الخطوة 1: جمع روابط المواقع من محرك البحث
    for dork in SEARCH_QUERIES:
        try:
            res = requests.get(dork, headers=HEADERS, timeout=10)
            # استخراج روابط المواقع الحقيقية من نتائج البحث
            links = re.findall(r'href="(http[s]?://.*?)"', res.text)
            sites_to_visit.extend([l for l in links if "bing" not in l and "microsoft" not in l])
        except: continue

    # الخطوة 2: مسح المواقع المستخرجة بعمق (استغلال قوة السحاب)
    all_channels = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(deep_extract, list(set(sites_to_visit))))
        for r in results:
            all_channels.extend(r)

    # الخطوة 3: حفظ النتائج في ملفك
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        if not all_channels:
            # رابط احتياطي عالمي في حال فشل المسح الشامل
            f.write("#EXTINF:-1, Global-Backup-Stream\nhttps://iptv-org.github.io/iptv/index.m3u\n")
        else:
            for channel in list(set(all_channels)):
                f.write(channel)
    
    print(f"Mission Done! {len(set(all_channels))} channels secured.")

if __name__ == "__main__":
    run_global_scanner()
