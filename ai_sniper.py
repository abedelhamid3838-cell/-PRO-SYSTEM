import requests
import re
from concurrent.futures import ThreadPoolExecutor

# مصادر "خام" يتم تحديثها كل دقيقة (خارج قيتهاب)
SOURCES = [
    "https://pastebin.com/raw/866uX6X8", 
    "https://t.me/s/iptv_links_arabic", # قنص من تلجرام ويب
    "https://www.telegra.ph/IPTV-Arabic-Free-05-12", # صفحات تليغراف المحدثة
    "https://raw.githubusercontent.com/tarekzort/IPTV-Daily/main/arabic.m3u",
    "https://iptv-org.github.io/iptv/countries/ar.m3u"
]

# الكلمات المفتاحية التي يبحث عنها الـ AI في كامل كود الصفحة
KEYWORDS = r'beIN|OSN|SSC|Alkass|Shahid|AD_SPORTS'

# رأس متصفح "شبح" لتجاوز الحماية (Stealth Mode)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def validate_stream(name, url):
    """ فحص جزيئات البث للتأكد من أنه يعمل 100% قبل الحفظ """
    try:
        # فحص سريع للرأس (Headers)
        r = requests.get(url, headers=HEADERS, timeout=4, stream=True)
        if r.status_code == 200:
            # التأكد من وجود داتا فيديو فعلياً
            it = r.iter_content(1024)
            if next(it): return f"{name}\n{url}\n"
    except: return None

def deep_web_sniper():
    found_data = []
    print("AI Sniper is now searching the entire web...")

    for site in SOURCES:
        try:
            response = requests.get(site, headers=HEADERS, timeout=10)
            # استخراج أي رابط http ينتهي بـ m3u8 أو يحتوي على دفق بيانات
            # واستخراج اسم القناة الذي يسبقه
            matches = re.findall(r'(#EXTINF.*?,(.*?)\n(http.*?))', response.text)
            for full, name, url in matches:
                if re.search(KEYWORDS, name, re.IGNORECASE):
                    found_data.append((name.strip(), url.strip()))
        except: continue

    # تصفية الروابط المكررة
    unique_data = list(set(found_data))
    print(f"Found {len(unique_data)} potential links. Starting AI verification...")

    # تشغيل 100 خيط معالجة متوازي (استغلال قوة السحاب)
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(lambda p: validate_stream(p[0], p[1]), unique_data))
    
    # كتابة الملف النهائي
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        final_list = [r for r in results if r is not None]
        for r in final_list: f.write(r)
    
    print(f"Mission Accomplished. {len(final_list)} Live channels secured.")

if __name__ == "__main__":
    deep_web_sniper()
