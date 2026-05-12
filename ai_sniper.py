import requests
import re
import concurrent.futures

# الكلمات المفتاحية للقنص (Target Keywords)
TARGETS = ["beIN Sports", "OSN", "SSC", "Shahid", "AlKass"]

# أنماط الروابط (Patterns) التي يبحث عنها الكود في صفحات الويب
LINK_PATTERN = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def scan_page(query):
    """ مسح نتائج محركات البحث لجلب روابط جديدة """
    found_links = []
    # محاكاة بحث جوجل أو بينج لجلب صفحات تحتوي على ملفات m3u
    search_url = f"https://www.bing.com/search?q={query}+filetype:m3u"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0'}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        # استخراج جميع الروابط من الصفحة
        potential_sites = re.findall(LINK_PATTERN, response.text)
        
        for site in potential_sites:
            if "bing" not in site and "microsoft" not in site:
                try:
                    # الدخول لكل موقع وجلب محتواه للبحث عن القنوات
                    content = requests.get(site, headers=headers, timeout=5).text
                    streams = re.findall(r'(#EXTINF.*)\n(http.*m3u8.*)', content)
                    for name, url in streams:
                        if any(t.lower() in name.lower() for t in TARGETS):
                            found_links.append(f"{name}\n{url.strip()}\n")
                except: continue
    except: pass
    return found_links

def aega_mega_scanner():
    print("AEGA AI is now scanning the entire web... Please wait.")
    
    # استعلامات بحث متقدمة (Dorks)
    queries = [
        "index+of+m3u+beIN",
        "intitle:index.of+m3u8+SSC",
        "OSN+m3u+playlist+2026",
        "Shahid+VIP+stream+m3u8"
    ]
    
    all_results = []
    # استخدام 50 خيط معالجة لمسح الإنترنت بسرعة
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_page, q) for q in queries]
        for future in concurrent.futures.as_completed(futures):
            all_results.extend(future.result())

    # حفظ النتائج في ملفك
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        # إزالة التكرار وحفظ الروابط الفريدة
        for link in list(set(all_results)):
            f.write(link)
            
    print(f"Scan complete. Found {len(set(all_results))} active streams from the open web.")

if __name__ == "__main__":
    aega_mega_scanner()deep_web_sniper()
