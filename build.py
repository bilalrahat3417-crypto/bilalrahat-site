# Builds three separate single-language pages from src.html:
#   /index.html (English), /tr/index.html (Turkish), /ar/index.html (Arabic)
# src.html holds every text as <span class="en">..</span><span class="ar">..</span>;
# Turkish comes from TR below, keyed by the English text.
import re, os

TR = {
 'Work': 'İşler', 'Services': 'Hizmetler', 'Process': 'Süreç', 'Studio': 'Stüdyo',
 'Start a project': 'Proje başlat',
 'Product CGI, directed frame by frame.': 'Ürün filmleri, kare kare yönetilir.',
 'Cinematic product films, loops and campaign stills for perfume, beauty, tech and automotive brands across Europe, the US and the Gulf.':
   'Avrupa, ABD ve Körfez\'deki parfüm, kozmetik, teknoloji ve otomotiv markaları için sinematik ürün filmleri, döngü videolar ve kampanya görselleri.',
 'Tell me about your product': 'Ürününüzü anlatın',
 'See packages': 'Paketleri gör',
 'Bilal Rahat · Film, CGI & AI Director · Founder of Mozaik Film': 'Bilal Rahat · Film, CGI ve Yapay Zekâ Yönetmeni · Mozaik Film Kurucusu',
 'Selected work': 'Seçili işler',
 'Glass, liquid, metal, stone and ceramic. Lit like a campaign.': 'Cam, sıvı, metal, taş ve seramik. Kampanya ışığıyla.',
 'Study 01 · Amber': 'Çalışma 01 · Amber', 'Studio study': 'Stüdyo çalışması',
 'Amber, a perfume study': 'Amber, bir parfüm çalışması',
 'A self-initiated lighting study: thick refractive glass, an amber liquid and a brushed gold cap, lit like a fragrance campaign.':
   'Kişisel bir ışık çalışması: kalın kırıcı cam, amber renkli sıvı ve fırçalanmış altın kapak; bir parfüm kampanyası gibi ışıklandırıldı.',
 'Software': 'Yazılım', 'Category': 'Kategori',
 'Fragrance, beauty, beverage, home, watches': 'Parfüm, kozmetik, içecek, ev, saat',
 'More studies': 'Diğer çalışmalar',
 'Study 02 · Serum': 'Çalışma 02 · Serum', 'Skincare': 'Cilt bakımı',
 'Study 03 · Steel watch': 'Çalışma 03 · Çelik saat', 'Watches': 'Saat',
 'Study 04 · Cold can': 'Çalışma 04 · Soğuk kutu', 'Beverage': 'İçecek',
 'Study 05 · Cream jars': 'Çalışma 05 · Krem kavanozları', 'Beauty': 'Kozmetik',
 'Study 06 · Ceramics': 'Çalışma 06 · Seramik', 'Home & decor': 'Ev ve dekorasyon',
 'Study 07 · Stone basin': 'Çalışma 07 · Taş lavabo', 'Bathroom': 'Banyo',
 'Study 10 · Thermos': 'Çalışma 10 · Termos', 'Outdoor & drinkware': 'Outdoor ve termos',
 'Study 09 · Tumbler': 'Çalışma 09 · Kristal bardak', 'Spirits & glassware': 'İçki ve cam ürünleri',
 'Packages': 'Paketler', 'Clear scope. Fixed starting prices.': 'Net kapsam. Sabit başlangıç fiyatları.',
 'Product Loop': 'Ürün Döngüsü', 'from': 'başlangıç',
 '6–10 second seamless loop': '6–10 saniyelik kesintisiz döngü',
 'One product, one scene': 'Tek ürün, tek sahne',
 '9:16, 1:1 and 16:9 delivery': '9:16, 1:1 ve 16:9 teslim',
 'Two rounds of revisions': 'İki revizyon turu', '5–7 working days': '5–7 iş günü',
 'Hero Product Film': 'Ana Ürün Filmi', '15–20 second film': '15–20 saniyelik film',
 'Storyboard and styleframes': 'Storyboard ve stil kareleri', 'Sound design': 'Ses tasarımı',
 'All social formats': 'Tüm sosyal medya formatları', '10–14 working days': '10–14 iş günü',
 'Campaign Pack': 'Kampanya Paketi',
 '30 second hero film + 3 cut-downs': '30 saniyelik ana film + 3 kısa versiyon',
 '10 high-resolution stills': '10 yüksek çözünürlüklü görsel',
 'Looping assets for web and ads': 'Web ve reklam için döngü videolar',
 'FOOH or launch concept': 'FOOH veya lansman konsepti', 'Priority schedule': 'Öncelikli takvim',
 'Quoted in USD or EUR. 50% to start, 50% on delivery, by bank transfer (Wise) or Payoneer.':
   'USD veya EUR ile fiyatlandırılır. %50 başlangıçta, %50 teslimde; banka havalesi (Wise) veya Payoneer ile.',
 'One model, every format': 'Tek model, her format',
 'Build the product once. Use it everywhere.': 'Ürünü bir kez modelle. Her yerde kullan.',
 'Your product is modelled once at full detail. From that single asset come the films, loops, stills and cut-downs for every channel, so a new colourway or a new market is days of work, not a new shoot.':
   'Ürününüz bir kez, tüm detaylarıyla modellenir. Her kanal için filmler, döngüler, görseller ve kısa versiyonlar bu tek modelden çıkar. Yeni bir renk ya da yeni bir pazar, yeni bir çekim değil birkaç günlük iştir.',
 'Films': 'Filmler', 'Hero spots for launch and paid social': 'Lansman ve sponsorlu reklamlar için ana filmler',
 'Loops': 'Döngüler', 'Seamless motion for web, e-commerce and stories': 'Web, e-ticaret ve hikâyeler için kesintisiz hareket',
 'Stills': 'Görseller', 'Packshots and key visuals without a photoshoot': 'Fotoğraf çekimi olmadan ürün ve ana görseller',
 'Cut-downs': 'Kısa versiyonlar', '6, 10 and 15 second versions for every placement': 'Her yerleşim için 6, 10 ve 15 saniyelik versiyonlar',
 'From your product to finished film in four steps.': 'Ürününüzden bitmiş filme dört adımda.',
 'Brief': 'Brief',
 'Send the product, photos or CAD files, where the film will run and your deadline.': 'Ürünü, fotoğrafları ya da CAD dosyalarını, filmin nerede yayınlanacağını ve teslim tarihinizi gönderin.',
 'Styleframe': 'Stil karesi',
 'You approve the look, light and mood on still frames before any animation starts.': 'Animasyon başlamadan önce görünümü, ışığı ve atmosferi sabit karelerde onaylarsınız.',
 'Animation': 'Animasyon',
 'Camera, motion and sound, shared as previews so you can steer at every stage.': 'Kamera, hareket ve ses; her aşamada yön verebilmeniz için önizlemelerle paylaşılır.',
 'Delivery': 'Teslim',
 'Final masters in every size the campaign needs, plus the stills.': 'Kampanyanın ihtiyaç duyduğu her boyutta final dosyalar ve görseller.',
 'A director, backed by a production company.': 'Arkasında bir prodüksiyon şirketi olan yönetmen.',
 "I'm Bilal Rahat. I founded Mozaik Film in 2009 and have spent the years since filming and producing for brands, from corporate campaigns to productions for National Geographic. Today I direct product films with live action, Blender CGI and AI, with the Mozaik team behind every project.":
   "Ben Bilal Rahat. 2009'da Mozaik Film'i kurdum; o günden bu yana kurumsal kampanyalardan National Geographic çekimlerine kadar markalar için film çekip prodüksiyon yapıyorum. Bugün canlı çekim, Blender CGI ve yapay zekâ ile ürün filmleri yönetiyorum; her projenin arkasında Mozaik ekibi var.",
 'When a project also needs live action, drone or a full crew, it is already in house. Based in Istanbul on GMT+3, the same working day as Europe and the Gulf.':
   "Projede canlı çekim, drone ya da tam bir ekip gerekiyorsa hepsi zaten bünyemizde. İstanbul merkezliyiz (GMT+3); Avrupa ve Körfez ile aynı iş gününde çalışıyoruz.",
 'Mozaik Film founded': "Mozaik Film'in kuruluşu", 'Brands served': 'Hizmet verilen marka',
 'Production team': 'Prodüksiyon ekibi', 'Istanbul': 'İstanbul',
 'Contact': 'İletişim', 'Tell me about your product.': 'Ürününüzü anlatın.',
 'Send a photo or link, where it will run and your deadline. I reply within one working day.':
   'Bir fotoğraf ya da bağlantı, filmin nerede yayınlanacağını ve teslim tarihinizi gönderin. Bir iş günü içinde dönüş yaparım.',
 'Email': 'E-posta', 'WhatsApp': 'WhatsApp',
 'Film, CGI & AI Director · Founder of Mozaik Film': 'Film, CGI ve Yapay Zekâ Yönetmeni · Mozaik Film Kurucusu',
}

META = {
 'en': ('Bilal Rahat · Film, CGI & AI Director',
        'Bilal Rahat is a film, CGI and AI director and founder of Mozaik Film. Product films, loops and stills for brands in Europe, the US and the Gulf.'),
 'tr': ('Bilal Rahat · Film, CGI ve Yapay Zekâ Yönetmeni',
        "Bilal Rahat, film, CGI ve yapay zekâ yönetmeni ve Mozaik Film'in kurucusu. Avrupa, ABD ve Körfez'deki markalar için ürün filmleri, döngüler ve görseller."),
 'ar': ('بلال راحت · مخرج أفلام وCGI وذكاء اصطناعي',
        'بلال راحت مخرج أفلام وCGI وذكاء اصطناعي ومؤسس موزاييك فيلم. أفلام منتجات ولقطات متكررة وصور لعلامات تجارية في أوروبا والولايات المتحدة والخليج.'),
}
PATH = {'en': '/', 'tr': '/tr/', 'ar': '/ar/'}
BASE = 'https://bilalrahat.com.tr'

src = open('src.html', encoding='utf-8').read()

# text fixes applied in every language (positioning: Film, CGI & AI Director)
src = src.replace('Bilal Rahat · CGI & 3D Director · Founder of Mozaik Film', 'Bilal Rahat · Film, CGI & AI Director · Founder of Mozaik Film')
src = src.replace('<span class="en">CGI & 3D Director · Founder of Mozaik Film</span>', '<span class="en">Film, CGI & AI Director · Founder of Mozaik Film</span>')
src = src.replace('Today I direct product CGI in Blender, with the Mozaik team behind every project.', 'Today I direct product films with live action, Blender CGI and AI, with the Mozaik team behind every project.')
src = src.replace('مخرج CGI وثلاثي الأبعاد · مؤسس موزاييك فيلم', 'مخرج أفلام وCGI وذكاء اصطناعي · مؤسس موزاييك فيلم')
src = src.replace('بلال راحت · مخرج CGI وثلاثي الأبعاد · مؤسس موزاييك فيلم', 'بلال راحت · مخرج أفلام وCGI وذكاء اصطناعي · مؤسس موزاييك فيلم')

# old toggle button -> plain-code language links (no foreign script on any page)
src = re.sub(r'<button class="btn lang" id="lang".*?</button>', '@@LANGS@@', src, flags=re.S)

PAIR = re.compile(r'<span class="en">(.*?)</span><span class="ar">(.*?)</span>', re.S)
missing = set()

def build(lang):
    def pick(m):
        en, ar = m.group(1), m.group(2)
        if lang == 'en': return en
        if lang == 'ar': return ar
        if en not in TR: missing.add(en)
        return TR.get(en, en)
    html = PAIR.sub(pick, src)
    title, desc = META[lang]
    html = html.replace('<html lang="en" dir="ltr">', f'<html lang="{lang}" dir="{"rtl" if lang == "ar" else "ltr"}">')
    html = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', html)
    html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', html)
    html = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title}">', html)
    html = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{desc}">', html)
    html = html.replace('<meta property="og:url" content="https://bilalrahat.com.tr/">', f'<meta property="og:url" content="{BASE}{PATH[lang]}">')
    alt = ''.join(f'\n<link rel="alternate" hreflang="{l}" href="{BASE}{p}">' for l, p in PATH.items())
    alt += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}/">\n<link rel="canonical" href="{BASE}{PATH[lang]}">'
    html = html.replace('<meta name="theme-color"', alt.lstrip('\n') + '\n<meta name="theme-color"', 1)
    links = ''.join(
        f'<a class="{"on" if l == lang else ""}" href="{p}" hreflang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a>'
        for l, p in PATH.items())
    html = html.replace('@@LANGS@@', f'<nav class="langs" aria-label="Language">{links}</nav>')
    html = html.replace('.lang{min-height:36px;padding:0 14px;font-size:13px}',
        '.langs{display:flex;gap:2px;font-size:12px;letter-spacing:.08em}.langs a{padding:8px 7px;text-decoration:none;color:var(--mute);border-radius:4px}.langs a:hover{color:var(--ink)}.langs a.on{color:var(--amber)}')
    # language switching script no longer needed; keep the header scroll effect
    html = re.sub(r"  const root = document\.documentElement;.*?addEventListener\('click', \(\) => setLang\(root\.lang === 'ar' \? 'en' : 'ar'\)\);\n", '', html, flags=re.S)
    if lang != 'en':
        html = html.replace('src="assets/', 'src="../assets/').replace(', assets/', ', ../assets/').replace('srcset="assets/', 'srcset="../assets/').replace('href="assets/', 'href="../assets/')
    out = 'index.html' if lang == 'en' else f'{lang}/index.html'
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)

for l in PATH: build(l)
print('missing TR:', missing or 'none')
