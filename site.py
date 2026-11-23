# Generates three single-language pages: /index.html (EN), /tr/index.html, /ar/index.html
import os

LANGS = {'en': '/', 'tr': '/tr/', 'ar': '/ar/'}
BASE = 'https://bilalrahat.com.tr'

def page(L):
    def t(en, tr, ar):
        return {'en': en, 'tr': tr, 'ar': ar}[L]
    A = '' if L == 'en' else '../'          # asset prefix
    rtl = L == 'ar'
    arrow = '←' if rtl else '→'
    ext = '↖' if rtl else '↗'

    title = t('Bilal Rahat · Film, CGI & AI Director',
              'Bilal Rahat · Film, CGI ve Yapay Zekâ Yönetmeni',
              'بلال راحت · مخرج أفلام وCGI وذكاء اصطناعي')
    desc = t('Product films, loops and campaign visuals made with live action, photoreal CGI and AI, for brands in Europe, the US and the Gulf.',
             "Avrupa, ABD ve Körfez'deki markalar için canlı çekim, foto-gerçekçi CGI ve yapay zekâ ile ürün filmleri, döngü videolar ve kampanya görselleri.",
             'أفلام منتجات ولقطات متكررة وصور حملات بالتصوير الحي وCGI الواقعي والذكاء الاصطناعي، لعلامات تجارية في أوروبا والولايات المتحدة والخليج.')

    hreflang = ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{p}">\n' for l, p in LANGS.items())
    langnav = ''.join(f'<a href="{p}" hreflang="{l}"{" class=on aria-current=page" if l == L else ""}>{l.upper()}</a>' for l, p in LANGS.items())

    def vid(name, alt, cls='', eager=False):
        src = f'{A}assets/video/{name}.mp4'
        poster = f'{A}assets/video/{name}.jpg'
        if eager:
            return f'<video class="{cls}" src="{src}" poster="{poster}" autoplay muted loop playsinline preload="auto" aria-label="{alt}"></video>'
        return f'<video class="{cls}" data-src="{src}" poster="{poster}" muted loop playsinline preload="none" aria-label="{alt}"></video>'

    services = [
        ('01', 'amber',
         t('CGI product films', 'CGI ürün filmleri', 'أفلام منتجات CGI'),
         t('Hero films that make a product feel worth its price.', 'Ürünü fiyatına layık hissettiren ana filmler.', 'أفلام رئيسية تجعل المنتج يبدو جديرًا بسعره.'),
         [t('Launch films', 'Lansman filmleri', 'أفلام الإطلاق'), t('Hero loops', 'Ana döngüler', 'لقطات رئيسية متكررة'),
          t('Campaign films', 'Kampanya filmleri', 'أفلام الحملات'), t('Paid social cut-downs', 'Reklam için kısa versiyonlar', 'نسخ قصيرة للإعلانات')]),
        ('02', 'serum',
         t('Launch visuals', 'Lansman görselleri', 'صور الإطلاق'),
         t('Stills and loops for e-commerce, social and press, without a photoshoot.', 'Fotoğraf çekimi olmadan e-ticaret, sosyal medya ve basın için görseller ve döngüler.', 'صور ولقطات متكررة للمتاجر الإلكترونية ووسائل التواصل والصحافة، دون جلسة تصوير.'),
         [t('Hero stills', 'Ana görseller', 'صور رئيسية'), t('E-commerce loops', 'E-ticaret döngüleri', 'لقطات للمتاجر الإلكترونية'),
          t('Packaging CGI', 'Ambalaj CGI', 'CGI للتغليف'), t('Social assets in 9:16, 1:1, 16:9', '9:16, 1:1, 16:9 sosyal medya içerikleri', 'محتوى بمقاسات 9:16 و1:1 و16:9')]),
        ('03', 'can',
         t('AI-assisted production', 'Yapay zekâ destekli prodüksiyon', 'إنتاج بمساعدة الذكاء الاصطناعي'),
         t('Generative AI for concepts, backgrounds and variations, finished by a director.', 'Konsept, arka plan ve varyasyonlar için üretken yapay zekâ; son dokunuş yönetmenden.', 'ذكاء اصطناعي توليدي للأفكار والخلفيات والنسخ، بلمسة مخرج نهائية.'),
         [t('Concept frames in days', 'Günler içinde konsept kareler', 'إطارات مفاهيمية خلال أيام'), t('Scene and background generation', 'Sahne ve arka plan üretimi', 'توليد المشاهد والخلفيات'),
          t('Variations for testing', 'Test için varyasyonlar', 'نسخ متعددة للاختبار'), t('Hybrid AI + CGI + live action', 'Hibrit yapay zekâ + CGI + canlı çekim', 'مزيج من الذكاء الاصطناعي وCGI والتصوير الحي')]),
        ('04', 'watch',
         t('Live action & FPV drone', 'Canlı çekim ve FPV drone', 'تصوير حي وطائرة FPV'),
         t('Cinema cameras, lighting and FPV one-takes, from the same director.', 'Sinema kameraları, ışık ve FPV tek plan çekimler; aynı yönetmenden.', 'كاميرات سينمائية وإضاءة ولقطات FPV متواصلة، من المخرج نفسه.'),
         [t('Commercial shoots', 'Reklam çekimleri', 'تصوير إعلاني'), t('FPV one-take films', 'FPV tek plan filmler', 'أفلام FPV بلقطة واحدة'),
          t('Hospitality and venues', 'Otel ve mekân filmleri', 'أفلام الفنادق والأماكن'), t('Editing and colour grading', 'Kurgu ve renk düzenleme', 'المونتاج وتصحيح الألوان')]),
        ('05', 'cream',
         t('Performance creative', 'Performans kreatifi', 'محتوى إعلاني عالي الأداء'),
         t('Ads built for Meta and Google, planned by someone who runs the campaigns.', 'Meta ve Google için kurgulanmış reklamlar; kampanyaları yöneten biri tarafından planlanır.', 'إعلانات مصممة لـMeta وGoogle، يخطط لها شخص يدير الحملات بنفسه.'),
         [t('Meta & Google Ads creative', 'Meta ve Google Ads kreatifleri', 'محتوى إعلانات Meta وGoogle'), t('Hooks and first-second motion', 'İlk saniyeyi yakalayan açılışlar', 'افتتاحيات تشد الانتباه من الثانية الأولى'),
          t('A/B variations', 'A/B varyasyonları', 'نسخ A/B'), t('Reporting on what works', 'Neyin çalıştığına dair raporlama', 'تقارير عما ينجح')]),
        ('06', 'drone',
         t('Technical CGI', 'Teknik CGI', 'CGI تقني'),
         t('Exploded views and assembly films that explain how a product is built.', 'Ürünün nasıl yapıldığını anlatan patlatılmış görünümler ve montaj filmleri.', 'مشاهد مفككة وأفلام تجميع تشرح كيف صُنع المنتج.'),
         [t('Exploded views', 'Patlatılmış görünümler', 'مشاهد مفككة'), t('Assembly animation', 'Montaj animasyonu', 'تحريك التجميع'),
          t('Cutaways and cross-sections', 'Kesit görünümler', 'مقاطع عرضية'), t('Built from your CAD files', 'CAD dosyalarınızdan modelleme', 'مبني من ملفات CAD الخاصة بك')]),
    ]
    svc_html = ''
    for n, v, h, line, items in services:
        lis = ''.join(f'<li>{i}</li>' for i in items)
        svc_html += f'''
    <article class="svc">
      <div class="media">{vid(v, h)}</div>
      <div class="body">
        <span class="num">{n}</span>
        <h3>{h}</h3>
        <p class="lead">{line}</p>
        <ul>{lis}</ul>
        <a class="tlink" href="#contact">{t('Plan this with me', 'Bunu birlikte planlayalım', 'لنخطط لهذا معًا')} {arrow}</a>
      </div>
    </article>'''

    work = [('amber', t('Amber', 'Amber', 'عنبر'), t('Fragrance', 'Parfüm', 'العطور')),
            ('serum', t('Serum', 'Serum', 'سيروم'), t('Skincare', 'Cilt bakımı', 'العناية بالبشرة')),
            ('can', t('Cold can', 'Soğuk kutu', 'علبة باردة'), t('Beverage', 'İçecek', 'المشروبات')),
            ('watch', t('Steel watch', 'Çelik saat', 'ساعة فولاذية'), t('Watches', 'Saat', 'الساعات')),
            ('cream', t('Cream jars', 'Krem kavanozları', 'برطمانات كريم'), t('Beauty', 'Kozmetik', 'التجميل')),
            ('glass', t('Tumbler', 'Kristal bardak', 'كأس'), t('Glassware', 'Cam ürünleri', 'الزجاجيات')),
            ('thermos', t('Thermos', 'Termos', 'ترمس'), t('Drinkware', 'Termos ve matara', 'أدوات الشرب')),
            ('vase', t('Ceramics', 'Seramik', 'خزفيات'), t('Home & decor', 'Ev ve dekorasyon', 'المنزل والديكور')),
            ('drone', t('FPV drone, exploded', 'FPV drone, patlatılmış', 'طائرة FPV مفككة'), t('Technical CGI', 'Teknik CGI', 'CGI تقني')),
            ('basin', t('Stone basin', 'Taş lavabo', 'حوض حجري'), t('Bathroom', 'Banyo', 'الحمّامات'))]
    work_html = ''.join(f'''
      <figure>{vid(v, name)}<figcaption><span>{i+1:02d} · {name}</span><span>{cat}</span></figcaption></figure>'''
                        for i, (v, name, cat) in enumerate(work))

    packs = [
        (t('Product Loop', 'Ürün Döngüsü', 'لقطة منتج متكررة'), '$600', False,
         [t('6–10 second seamless loop', '6–10 saniyelik kesintisiz döngü', 'لقطة متكررة من 6 إلى 10 ثوانٍ'),
          t('One product, one scene', 'Tek ürün, tek sahne', 'منتج واحد ومشهد واحد'),
          t('9:16, 1:1 and 16:9', '9:16, 1:1 ve 16:9', 'مقاسات 9:16 و1:1 و16:9'),
          t('Two rounds of revisions', 'İki revizyon turu', 'جولتان من التعديلات'),
          t('5–7 working days', '5–7 iş günü', 'من 5 إلى 7 أيام عمل')]),
        (t('Hero Product Film', 'Ana Ürün Filmi', 'فيلم المنتج الرئيسي'), '$1,200', True,
         [t('15–20 second film', '15–20 saniyelik film', 'فيلم من 15 إلى 20 ثانية'),
          t('Storyboard and styleframes', 'Storyboard ve stil kareleri', 'لوحة قصة وإطارات أسلوب'),
          t('Sound design', 'Ses tasarımı', 'تصميم صوتي'),
          t('All social formats', 'Tüm sosyal medya formatları', 'جميع مقاسات التواصل الاجتماعي'),
          t('10–14 working days', '10–14 iş günü', 'من 10 إلى 14 يوم عمل')]),
        (t('Campaign Pack', 'Kampanya Paketi', 'باقة الحملة'), '$2,500', False,
         [t('30 second hero film + 3 cut-downs', '30 saniyelik ana film + 3 kısa versiyon', 'فيلم رئيسي 30 ثانية + 3 نسخ قصيرة'),
          t('10 high-resolution stills', '10 yüksek çözünürlüklü görsel', '10 صور عالية الدقة'),
          t('Loops for web and ads', 'Web ve reklam için döngüler', 'لقطات متكررة للويب والإعلانات'),
          t('FOOH or launch concept', 'FOOH veya lansman konsepti', 'فكرة FOOH أو إطلاق'),
          t('Priority schedule', 'Öncelikli takvim', 'جدول بأولوية')]),
    ]
    pack_html = ''.join(f'''
      <article class="pack{' hi' if hi else ''}">
        <h3>{name}</h3>
        <p class="price">{t('from', 'başlangıç', 'ابتداءً من')}<b>{price}</b></p>
        <ul>{''.join(f'<li>{x}</li>' for x in items)}</ul>
      </article>''' for name, price, hi, items in packs)

    steps = [(t('Brief', 'Brief', 'الملخص'), t('Send the product, photos or CAD files, where the film will run and your deadline.', 'Ürünü, fotoğrafları ya da CAD dosyalarını, filmin nerede yayınlanacağını ve teslim tarihinizi gönderin.', 'أرسل المنتج أو الصور أو ملفات CAD، ومكان عرض الفيلم وموعدك النهائي.')),
             (t('Creative direction', 'Kreatif yön', 'التوجيه الإبداعي'), t('You approve the look, light and mood on still frames before any animation starts.', 'Animasyon başlamadan önce görünümü, ışığı ve atmosferi sabit karelerde onaylarsınız.', 'توافق على الشكل والإضاءة والأجواء في إطارات ثابتة قبل بدء التحريك.')),
             (t('Production', 'Prodüksiyon', 'الإنتاج'), t('Camera, motion and sound, shared as previews so you can steer at every stage.', 'Kamera, hareket ve ses; her aşamada yön verebilmeniz için önizlemelerle paylaşılır.', 'الكاميرا والحركة والصوت، تُشارك كمعاينات لتوجّه العمل في كل مرحلة.')),
             (t('Delivery', 'Teslim', 'التسليم'), t('Final masters in every size the campaign needs, plus the stills.', 'Kampanyanın ihtiyaç duyduğu her boyutta final dosyalar ve görseller.', 'النسخ النهائية بكل المقاسات التي تحتاجها الحملة، مع الصور.'))]
    steps_html = ''.join(f'<li><span class="num">{i+1:02d}</span><h3>{h}</h3><p>{p}</p></li>' for i, (h, p) in enumerate(steps))

    clients = ['National Geographic', 'Bahçeşehir Koleji', 'Öztiryakiler', 'Gapsan Tekstil', 'Transfomax', 'Ferat Dalgıç Pompa']

    return f'''<!DOCTYPE html>
<html lang="{L}" dir="{'rtl' if rtl else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/assets/og.jpg">
<meta property="og:url" content="{BASE}{LANGS[L]}">
<meta name="twitter:card" content="summary_large_image">
{hreflang}<link rel="alternate" hreflang="x-default" href="{BASE}/">
<link rel="canonical" href="{BASE}{LANGS[L]}">
<meta name="theme-color" content="#000000">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23000'/%3E%3Ctext x='32' y='43' font-family='Georgia,serif' font-size='30' text-anchor='middle' fill='%23fff'%3EBR%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=Inter:wght@400;500;600&display=swap{'&family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Noto+Naskh+Arabic:wght@500;600' if rtl else ''}" rel="stylesheet">
<style>
/* matte black studio: pure black ground, white serif display, one cool-blue accent for labels and links */
:root{{--bg:#000;--bg2:#0b0b0c;--card:#0f0f10;--line:#1f1f22;--ink:#f4f4f2;--mute:#9b9b9b;--accent:#5b8dff;--serif:"Newsreader",Georgia,serif;--sans:"Inter",system-ui,sans-serif;color-scheme:dark}}
html[lang=ar]{{--serif:"Noto Naskh Arabic","Newsreader",serif;--sans:"IBM Plex Sans Arabic","Inter",sans-serif}}
*{{box-sizing:border-box;min-width:0}}
html{{scroll-behavior:smooth;scroll-padding-top:80px}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--sans);overflow-x:clip;-webkit-font-smoothing:antialiased}}
img,video{{max-width:100%;display:block}}
a{{color:inherit}}
.wrap{{max-width:1320px;margin:0 auto;padding-inline:max(4vw,20px)}}
.band{{padding-block:clamp(72px,10vw,140px);border-top:1px solid var(--line)}}
.eyebrow{{font:600 12px/1.3 var(--sans);letter-spacing:.24em;text-transform:uppercase;color:var(--accent);margin:0 0 22px}}
html[lang=ar] .eyebrow{{letter-spacing:0;font-size:14px}}
h1,h2,h3{{font-family:var(--serif);font-weight:400;letter-spacing:-.015em;margin:0;text-wrap:balance}}
html[lang=ar] h1,html[lang=ar] h2,html[lang=ar] h3{{letter-spacing:0;font-weight:500}}
h2{{font-size:clamp(34px,4.6vw,64px);line-height:1.06}}
h2 .sub{{display:block;color:#bdbdbd}}
p{{margin:0}}
.lead{{color:var(--mute);font-size:17px;max-width:60ch}}
.num{{font:500 13px/1 var(--sans);letter-spacing:.12em;color:var(--accent)}}
.tlink{{display:inline-flex;gap:10px;font:600 13px/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--accent);text-decoration:none}}
html[lang=ar] .tlink{{letter-spacing:0;font-size:15px}}
.tlink:hover{{color:var(--ink)}}
.box{{display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:0 22px;border:1px solid rgba(255,255,255,.4);font:600 14px/1 var(--sans);text-decoration:none;white-space:nowrap;color:var(--ink)}}
.box:hover{{background:var(--ink);color:#000;border-color:var(--ink)}}
.box.solid{{background:var(--ink);color:#000;border-color:var(--ink)}}
.box.solid:hover{{background:var(--accent);border-color:var(--accent);color:#fff}}
/* header */
header{{position:fixed;inset:0 0 auto;z-index:20;background:rgba(0,0,0,.82);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}}
.nav{{display:flex;align-items:center;gap:30px;height:80px}}
.brand{{font:500 15px/1 var(--sans);letter-spacing:.32em;text-transform:uppercase;text-decoration:none;margin-inline-end:auto;white-space:nowrap}}
.links{{display:flex;gap:28px;font-size:15px;font-weight:500}}
.links a{{text-decoration:none;color:#d8d8d8;padding-block:6px;border-bottom:2px solid transparent}}
.links a:hover{{color:#fff;border-color:var(--accent)}}
.langs{{display:flex;gap:2px;font-size:12px;letter-spacing:.08em}}
.langs a{{padding:8px 6px;color:var(--mute);text-decoration:none}}
.langs a:hover{{color:var(--ink)}}
.langs a.on{{color:var(--ink);border-bottom:2px solid var(--accent)}}
.nav .box{{min-height:44px;font-size:13px}}
/* hero */
.hero{{position:relative;min-height:min(100svh,980px);display:flex;align-items:center;isolation:isolate;padding-top:80px}}
.hero video,.hero .still{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:30% 50%;transform:scaleX(-1);z-index:-2;filter:saturate(.5) brightness(.75)}}
html[lang=ar] .hero video{{transform:none}}
.hero::before{{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#000 0%,rgba(0,0,0,.85) 34%,rgba(0,0,0,.2) 70%),linear-gradient(0deg,#000 0%,rgba(0,0,0,0) 30%)}}
html[lang=ar] .hero::before{{background:linear-gradient(270deg,#000 0%,rgba(0,0,0,.85) 34%,rgba(0,0,0,.2) 70%),linear-gradient(0deg,#000 0%,rgba(0,0,0,0) 30%)}}
.hero .wrap{{width:100%;padding-block:80px}}
.hero h1{{font-size:clamp(52px,7vw,104px);line-height:1}}
.hero h1 .sub{{display:block;font-size:.62em;line-height:1.12;color:#cfcfcf;margin-top:14px;max-width:13em}}
.hero .lead{{margin:34px 0 40px;color:#e6e6e6;font-size:clamp(17px,1.4vw,20px);max-width:44ch}}
/* clients */
.clients{{border-top:1px solid var(--line);padding-block:34px}}
.clients .wrap{{display:flex;flex-wrap:wrap;align-items:center;gap:18px 44px}}
.clients small{{font:600 11px/1 var(--sans);letter-spacing:.24em;text-transform:uppercase;color:var(--mute);margin-inline-end:12px}}
.clients span{{font:400 19px/1 var(--serif);color:#cfcfcf}}
/* services */
.svcs{{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);margin-top:60px}}
.svc{{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);background:var(--bg)}}
.svc:nth-child(even) .media{{order:2}}
.svc .media{{aspect-ratio:16/10;background:var(--card);overflow:hidden}}
.svc .media video{{width:100%;height:100%;object-fit:cover}}
.svc .body{{padding:clamp(28px,4vw,56px);display:flex;flex-direction:column;gap:18px;justify-content:center}}
.svc h3{{font-size:clamp(28px,2.8vw,40px);line-height:1.1}}
.svc ul{{list-style:none;margin:6px 0 10px;padding:0;display:grid;gap:10px;color:#d4d4d4;font-size:15px}}
.svc li{{padding-inline-start:20px;position:relative}}
.svc li::before{{content:"";position:absolute;inset-inline-start:0;top:.72em;width:8px;height:1px;background:var(--accent)}}
/* work */
.work{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:56px}}
.work figure{{margin:0}}
.work video{{width:100%;aspect-ratio:16/10;object-fit:cover;background:var(--card)}}
.work figcaption{{display:flex;justify-content:space-between;gap:10px;margin-top:12px;font-size:13px;color:var(--mute)}}
.work figcaption span:first-child{{color:var(--ink)}}
/* master model */
.one{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,6vw,96px);align-items:start}}
.flow{{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}}
.flow li{{display:grid;grid-template-columns:56px minmax(0,1fr);gap:16px;padding:22px 0;border-bottom:1px solid var(--line)}}
.flow b{{font:400 22px/1.2 var(--serif)}}
.flow p{{grid-column:2;color:var(--mute);font-size:15px;margin-top:4px}}
/* packages */
.packs{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin-top:56px}}
.pack{{background:var(--bg);padding:36px 30px;display:flex;flex-direction:column;gap:18px}}
.pack.hi{{background:var(--card)}}
.pack h3{{font-size:28px}}
.price{{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}}
.price b{{display:block;font:400 44px/1.1 var(--serif);letter-spacing:0;text-transform:none;color:var(--ink);margin-top:6px}}
.pack ul{{list-style:none;margin:0;padding:0;display:grid;gap:10px;font-size:15px;color:#d4d4d4}}
.pack li{{padding-inline-start:20px;position:relative}}
.pack li::before{{content:"";position:absolute;inset-inline-start:0;top:.72em;width:8px;height:1px;background:var(--accent)}}
.note{{margin-top:22px;font-size:14px;color:var(--mute)}}
/* process */
.steps{{list-style:none;margin:56px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:32px}}
.steps li{{border-top:1px solid var(--ink);padding-top:22px}}
.steps h3{{font-size:26px;margin:16px 0 10px}}
.steps p{{font-size:15px;color:var(--mute)}}
/* start */
.start{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,6vw,96px)}}
.qs{{list-style:none;margin:0;padding:0;counter-reset:q;border-top:1px solid var(--line)}}
.qs li{{counter-increment:q;display:grid;grid-template-columns:56px minmax(0,1fr);padding:22px 0;border-bottom:1px solid var(--line);font:400 21px/1.35 var(--serif)}}
.qs li::before{{content:counter(q,decimal-leading-zero);font:500 13px/2 var(--sans);letter-spacing:.12em;color:var(--accent)}}
.ctas{{display:flex;flex-wrap:wrap;gap:12px;margin-top:36px}}
/* studio */
.studio{{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(28px,6vw,96px);align-items:center}}
.portrait{{aspect-ratio:4/5;overflow:hidden;background:var(--card)}}
.portrait img{{width:100%;height:100%;object-fit:cover;filter:grayscale(.35)}}
.studio p+p{{margin-top:16px}}
.studio h2{{margin-bottom:24px}}
.facts{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin-top:40px;border-top:1px solid var(--line);padding-top:26px}}
.facts b{{display:block;font:400 clamp(30px,3vw,44px)/1 var(--serif);white-space:nowrap}}
.facts span{{font-size:13px;color:var(--mute)}}
.contact{{display:grid;gap:0;margin-top:44px;max-width:760px}}
.contact a{{display:flex;justify-content:space-between;gap:16px;padding:22px 0;border-top:1px solid var(--line);text-decoration:none;font-size:clamp(17px,1.8vw,22px)}}
.contact a:last-child{{border-bottom:1px solid var(--line)}}
.contact small{{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--mute)}}
.contact a:hover{{color:var(--accent)}}
.contact .v{{direction:ltr;unicode-bidi:isolate}}
footer{{border-top:1px solid var(--line);padding:40px 0 48px;font-size:13px;color:var(--mute)}}
footer .wrap{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px}}
footer a{{text-decoration:none}} footer a:hover{{color:var(--ink)}}
@media (max-width:980px){{.links{{display:none}}.svc,.one,.start,.studio{{grid-template-columns:minmax(0,1fr)}}.svc:nth-child(even) .media{{order:0}}.work{{grid-template-columns:repeat(2,minmax(0,1fr))}}.packs{{grid-template-columns:minmax(0,1fr)}}.steps{{grid-template-columns:repeat(2,minmax(0,1fr))}}.portrait{{max-width:420px}}}}
@media (max-width:600px){{.nav{{gap:14px;height:68px}}.nav .box{{display:none}}.hero{{min-height:94svh;align-items:flex-end}}.hero video{{object-position:25% 50%}}.hero::before,html[lang=ar] .hero::before{{background:linear-gradient(0deg,#000 10%,rgba(0,0,0,.8) 50%,rgba(0,0,0,.3) 100%)}}.work{{grid-template-columns:minmax(0,1fr)}}.steps{{grid-template-columns:minmax(0,1fr)}}.facts{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
</style>
</head>
<body>

<header>
  <div class="wrap nav">
    <a class="brand" href="{LANGS[L]}">Bilal Rahat</a>
    <nav class="links" aria-label="Main">
      <a href="#work">{t('Work', 'İşler', 'الأعمال')}</a>
      <a href="#services">{t('Services', 'Hizmetler', 'الخدمات')}</a>
      <a href="#process">{t('Process', 'Süreç', 'طريقة العمل')}</a>
      <a href="#studio">{t('Studio', 'Stüdyo', 'الاستوديو')}</a>
    </nav>
    <nav class="langs" aria-label="Language">{langnav}</nav>
    <a class="box" href="#start">{t('Tell me about your project', 'Projenizi anlatın', 'حدّثني عن مشروعك')} {ext}</a>
  </div>
</header>

<main>
<section class="hero">
  {vid('amber', t('Amber perfume bottle rendered in Blender', "Blender'da render edilmiş amber parfüm şişesi", 'زجاجة عطر عنبرية مصنوعة في Blender'), eager=True)}
  <div class="wrap">
    <p class="eyebrow">{t('What I make', 'Ne üretiyorum?', 'ماذا أصنع')}</p>
    <h1>{t('Product films', 'Ürün filmleri', 'أفلام المنتجات')}<span class="sub">{t('for brands that want to look expensive.', 'pahalı görünmek isteyen markalar için.', 'لعلامات تريد أن تبدو فاخرة.')}</span></h1>
    <p class="lead">{t('I direct product films, loops and campaign visuals with live action, photoreal CGI and AI, for brands across Europe, the US and the Gulf.', "Avrupa, ABD ve Körfez'deki markalar için canlı çekim, foto-gerçekçi CGI ve yapay zekâ ile ürün filmleri, döngü videolar ve kampanya görselleri yönetiyorum.", 'أخرج أفلام منتجات ولقطات متكررة وصور حملات بالتصوير الحي وCGI الواقعي والذكاء الاصطناعي، لعلامات في أوروبا والولايات المتحدة والخليج.')}</p>
    <a class="tlink" href="#start">{t('Tell me about your project', 'Projenizi anlatın', 'حدّثني عن مشروعك')} {arrow}</a>
  </div>
</section>

<section class="clients" aria-label="{t('Productions for', 'Çalıştığımız markalar', 'إنتاجات لصالح')}">
  <div class="wrap"><small>{t('Productions for', 'Çalıştığımız markalar', 'إنتاجات لصالح')}</small>{''.join(f'<span>{c}</span>' for c in clients)}</div>
</section>

<section class="band" id="services">
  <div class="wrap">
    <p class="eyebrow">{t('Services', 'Hizmetler', 'الخدمات')}</p>
    <h2>{t('One director.', 'Tek yönetmen.', 'مخرج واحد.')}<span class="sub">{t('From the first frame to the final grade.', 'İlk kareden son renk düzenlemesine kadar.', 'من اللقطة الأولى حتى التصحيح اللوني الأخير.')}</span></h2>
    <div class="svcs">{svc_html}
    </div>
  </div>
</section>

<section class="band" id="work">
  <div class="wrap">
    <p class="eyebrow">{t('Selected studies', 'Seçili çalışmalar', 'دراسات مختارة')}</p>
    <h2>{t('Glass, liquid, metal, stone, ceramic.', 'Cam, sıvı, metal, taş, seramik.', 'زجاج وسائل ومعدن وحجر وخزف.')}<span class="sub">{t('Each lit like a campaign.', 'Her biri bir kampanya gibi ışıklandırıldı.', 'كلٌّ منها بإضاءة حملة إعلانية.')}</span></h2>
    <div class="work">{work_html}
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap one">
    <div>
      <p class="eyebrow">{t('One master model', 'Tek ana model', 'نموذج رئيسي واحد')}</p>
      <h2>{t('Build the product once.', 'Ürünü bir kez modelle.', 'اصنع المنتج مرة واحدة.')}<span class="sub">{t('Use it everywhere.', 'Her yerde kullan.', 'واستخدمه في كل مكان.')}</span></h2>
      <p class="lead" style="margin-top:26px">{t('Your product is modelled once at full detail. Films, loops, stills and cut-downs for every channel come from that single asset, so a new colour or a new market is days of work, not a new shoot.', 'Ürününüz bir kez, tüm detaylarıyla modellenir. Her kanal için filmler, döngüler, görseller ve kısa versiyonlar bu tek modelden çıkar. Yeni bir renk ya da yeni bir pazar, yeni bir çekim değil birkaç günlük iştir.', 'يُصمَّم منتجك مرة واحدة بكامل التفاصيل. ومن هذا الأصل الواحد تخرج الأفلام واللقطات المتكررة والصور والنسخ القصيرة لكل قناة، فيصبح اللون الجديد أو السوق الجديد عمل أيام لا تصويرًا جديدًا.')}</p>
    </div>
    <ul class="flow">
      <li><span class="num">01</span><b>{t('Films', 'Filmler', 'الأفلام')}</b><p>{t('Hero spots for launch and paid social', 'Lansman ve sponsorlu reklamlar için ana filmler', 'إعلانات رئيسية للإطلاق والإعلانات المدفوعة')}</p></li>
      <li><span class="num">02</span><b>{t('Loops', 'Döngüler', 'اللقطات المتكررة')}</b><p>{t('Seamless motion for web, e-commerce and stories', 'Web, e-ticaret ve hikâyeler için kesintisiz hareket', 'حركة متواصلة للويب والمتاجر والقصص')}</p></li>
      <li><span class="num">03</span><b>{t('Stills', 'Görseller', 'الصور')}</b><p>{t('Packshots and key visuals without a photoshoot', 'Fotoğraf çekimi olmadan ürün ve ana görseller', 'صور المنتج والصور الرئيسية دون جلسة تصوير')}</p></li>
      <li><span class="num">04</span><b>{t('Cut-downs', 'Kısa versiyonlar', 'النسخ القصيرة')}</b><p>{t('6, 10 and 15 second versions for every placement', 'Her yerleşim için 6, 10 ve 15 saniyelik versiyonlar', 'نسخ من 6 و10 و15 ثانية لكل موضع إعلاني')}</p></li>
    </ul>
  </div>
</section>

<section class="band" id="packages">
  <div class="wrap">
    <p class="eyebrow">{t('Packages', 'Paketler', 'الباقات')}</p>
    <h2>{t('Clear scope.', 'Net kapsam.', 'نطاق واضح.')}<span class="sub">{t('Fixed starting prices.', 'Sabit başlangıç fiyatları.', 'أسعار بداية ثابتة.')}</span></h2>
    <div class="packs">{pack_html}
    </div>
    <p class="note">{t('Quoted in USD or EUR. 50% to start, 50% on delivery, by bank transfer (Wise) or Payoneer.', 'USD veya EUR ile fiyatlandırılır. %50 başlangıçta, %50 teslimde; banka havalesi (Wise) veya Payoneer ile.', 'الأسعار بالدولار أو اليورو. 50% عند البدء و50% عند التسليم، بتحويل بنكي (Wise) أو Payoneer.')}</p>
  </div>
</section>

<section class="band" id="process">
  <div class="wrap">
    <p class="eyebrow">{t('Process', 'Süreç', 'طريقة العمل')}</p>
    <h2>{t('How every project runs.', 'Her proje nasıl ilerler.', 'كيف يسير كل مشروع.')}</h2>
    <ol class="steps">{steps_html}</ol>
  </div>
</section>

<section class="band" id="start">
  <div class="wrap start">
    <div>
      <p class="eyebrow">{t('Your next project', 'Sıradaki projeniz', 'مشروعك القادم')}</p>
      <h2>{t('Find the right starting point.', 'Doğru başlangıç noktasını bulun.', 'اعثر على نقطة البداية الصحيحة.')}</h2>
      <div class="ctas">
        <a class="box solid" href="mailto:studio@bilalrahat.com.tr">{t('Email the brief', 'Brief gönderin', 'أرسل الملخص')} {ext}</a>
        <a class="box" href="https://wa.me/905306264363">WhatsApp {ext}</a>
      </div>
    </div>
    <div>
      <p class="lead" style="margin-bottom:22px">{t('Three answers are enough to start:', 'Başlamak için üç cevap yeterli:', 'ثلاث إجابات تكفي للبدء:')}</p>
      <ol class="qs">
        <li>{t('What is the product, and do you have photos or CAD files?', 'Ürün nedir, fotoğraf ya da CAD dosyası var mı?', 'ما المنتج، وهل لديك صور أو ملفات CAD؟')}</li>
        <li>{t('Where will the film run: ads, website, launch event?', 'Film nerede yayınlanacak: reklam, web sitesi, lansman?', 'أين سيُعرض الفيلم: إعلانات، موقع، حدث إطلاق؟')}</li>
        <li>{t('When do you need it, and what budget range?', 'Ne zaman lazım ve bütçe aralığı nedir?', 'متى تحتاجه، وما نطاق الميزانية؟')}</li>
      </ol>
    </div>
  </div>
</section>

<section class="band" id="studio">
  <div class="wrap studio">
    <div class="portrait"><img src="{A}assets/bilal-rahat.jpg" alt="Bilal Rahat" loading="lazy"></div>
    <div>
      <p class="eyebrow">{t('Studio', 'Stüdyo', 'الاستوديو')}</p>
      <h2>{t('A director, backed by a production company.', 'Arkasında bir prodüksiyon şirketi olan yönetmen.', 'مخرج تدعمه شركة إنتاج.')}</h2>
      <p class="lead">{t("I'm Bilal Rahat. I founded Mozaik Film in 2009 and have spent the years since filming and producing for brands, from corporate campaigns to productions for National Geographic. Today I direct product films with live action, Blender CGI and AI, with the Mozaik team behind every project.", "Ben Bilal Rahat. 2009'da Mozaik Film'i kurdum; o günden bu yana kurumsal kampanyalardan National Geographic çekimlerine kadar markalar için film çekip prodüksiyon yapıyorum. Bugün canlı çekim, Blender CGI ve yapay zekâ ile ürün filmleri yönetiyorum; her projenin arkasında Mozaik ekibi var.", 'أنا بلال راحت. أسست موزاييك فيلم عام 2009، ومنذ ذلك الحين أصوّر وأنتج للعلامات التجارية، من الحملات المؤسسية إلى إنتاجات لصالح ناشيونال جيوغرافيك. اليوم أخرج أفلام المنتجات بالتصوير الحي وCGI في Blender والذكاء الاصطناعي، مع فريق موزاييك خلف كل مشروع.')}</p>
      <p class="lead">{t('Based in Istanbul on GMT+3, the same working day as Europe and the Gulf. English, Turkish and Arabic.', 'İstanbul merkezli, GMT+3; Avrupa ve Körfez ile aynı iş günü. İngilizce, Türkçe ve Arapça.', 'مقري إسطنبول بتوقيت GMT+3، يوم العمل نفسه مع أوروبا والخليج. الإنجليزية والتركية والعربية.')}</p>
      <div class="facts">
        <div><b>2009</b><span>{t('Mozaik Film founded', "Mozaik Film'in kuruluşu", 'تأسيس موزاييك فيلم')}</span></div>
        <div><b>500+</b><span>{t('Brand films', 'Marka filmi', 'فيلم لعلامات تجارية')}</span></div>
        <div><b>10+</b><span>{t('Production team', 'Prodüksiyon ekibi', 'فريق الإنتاج')}</span></div>
        <div><b>GMT+3</b><span>{t('Istanbul', 'İstanbul', 'إسطنبول')}</span></div>
      </div>
      <div class="contact" id="contact">
        <a href="mailto:studio@bilalrahat.com.tr"><small>{t('Email', 'E-posta', 'البريد')}</small><span class="v">studio@bilalrahat.com.tr</span></a>
        <a href="https://wa.me/905306264363"><small>WhatsApp</small><span class="v">+90 530 626 43 63</span></a>
        <a href="https://www.linkedin.com/in/bilalrahat"><small>LinkedIn</small><span class="v">/in/bilalrahat</span></a>
        <a href="https://www.instagram.com/bilalrahat_art/"><small>Instagram</small><span class="v">@bilalrahat_art</span></a>
      </div>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <span>© 2026 Bilal Rahat · {t('Film, CGI & AI Director · Founder of Mozaik Film', 'Film, CGI ve Yapay Zekâ Yönetmeni · Mozaik Film Kurucusu', 'مخرج أفلام وCGI وذكاء اصطناعي · مؤسس موزاييك فيلم')}</span>
    <span>{langnav.replace('class=on aria-current=page', 'aria-current=page')}</span>
  </div>
</footer>

<script>
{{
  const vids = document.querySelectorAll('video[data-src]');
  const io = new IntersectionObserver((es) => es.forEach(e => {{
    const v = e.target;
    if (e.isIntersecting) {{ if (!v.src) v.src = v.dataset.src; v.play().catch(() => {{}}); }}
    else v.pause();
  }}), {{ rootMargin: '200px' }});
  vids.forEach(v => io.observe(v));
}}
</script>
</body>
</html>
'''

for L, p in LANGS.items():
    out = 'index.html' if L == 'en' else f'{L}/index.html'
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    open(out, 'w', encoding='utf-8').write(page(L))
print('ok')
