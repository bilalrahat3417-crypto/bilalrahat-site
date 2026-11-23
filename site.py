# Generates the multi-page site in three languages.
#   /            home (hub)          /tr/ , /ar/
#   /cgi/        3D product CGI      /tr/cgi/ , /ar/cgi/
#   /film/       commercials & brand films
#   /drone/      FPV drone & aerial
#   /photo/      product & venue photography
#   /digital/    web, ads & social
#   /references/ reference portfolio
# Styles live in assets/site.css.
# Real footage: drop assets/work/<slug>.mp4 (+ .jpg poster) or assets/work/<slug>.jpg
# and re-run `python3 site.py`; the typographic tile is replaced automatically.
import os
import json
import refs

BASE = 'https://bilalrahat.com.tr'
LANGS = ['en', 'tr', 'ar']
PAGES = ['home', 'cgi', 'film', 'drone', 'photo', 'digital', 'references']
EMAIL = 'studio@bilalrahat.com.tr'
WA = 'https://wa.me/905306264363'


def url(L, page):
    pre = '/' if L == 'en' else f'/{L}/'
    return pre if page == 'home' else f'{pre}{page}/'


def media(slug, alt, eager=False, fallback=None):
    """Video if assets/work/<slug>.mp4 or assets/video/<slug>.mp4 exists, image if .jpg exists, else a typographic tile."""
    for d in ('work', 'video'):
        mp4 = f'assets/{d}/{slug}.mp4'
        if os.path.exists(mp4):
            poster = f'/assets/{d}/{slug}.jpg'
            if eager:
                return f'<video src="/{mp4}" poster="{poster}" autoplay muted loop playsinline preload="auto" aria-label="{alt}"></video>'
            return f'<video data-src="/{mp4}" poster="{poster}" muted loop playsinline preload="none" aria-label="{alt}"></video>'
    for d in ('work', 'video'):
        jpg = f'assets/{d}/{slug}.jpg'
        if os.path.exists(jpg):
            return f'<img src="/{jpg}" alt="{alt}" loading="lazy">'
    label, title = fallback or ('', alt)
    return f'<div class="tile" role="img" aria-label="{alt}"><i>{label}</i><b>{title}</b></div>'


def build(L, page):
    def t(en, tr, ar):
        return {'en': en, 'tr': tr, 'ar': ar}[L]
    rtl = L == 'ar'
    arrow = '←' if rtl else '→'
    ext = '↖' if rtl else '↗'
    U = lambda p: url(L, p)

    NAV = {
        'cgi': t('3D CGI', '3D CGI', 'CGI ثلاثي الأبعاد'),
        'film': t('Film', 'Film', 'الأفلام'),
        'drone': t('Drone', 'Drone', 'الدرون'),
        'photo': t('Photo', 'Fotoğraf', 'التصوير'),
        'digital': t('Web & Ads', 'Web ve Reklam', 'الويب والإعلانات'),
        'references': t('References', 'Referanslar', 'المراجع'),
    }
    DISC = {  # discipline labels for project meta and chips
        'cgi': t('3D CGI', '3D CGI', 'CGI'),
        'film': t('Film & video', 'Film ve video', 'أفلام وفيديو'),
        'drone': t('Drone', 'Drone', 'درون'),
        'photo': t('Photography', 'Fotoğraf', 'تصوير فوتوغرافي'),
        'digital': t('Web & ads', 'Web ve reklam', 'ويب وإعلانات'),
    }

    # ------------------------------------------------------------------ references data
    projects = [
        dict(slug='cgi-studies', discs=['cgi'], client='Bilal Rahat Studio',
             sector=t('Product CGI', 'Ürün CGI', 'CGI للمنتجات'),
             title=t('Ten product studies in Blender', "Blender'da on ürün çalışması", 'عشر دراسات منتجات في Blender'),
             text=t('Glass, liquid, metal, stone and ceramic, each lit like a campaign. Loops, stills and an exploded-view technical film.',
                    'Cam, sıvı, metal, taş ve seramik; her biri bir kampanya gibi ışıklandırıldı. Döngüler, görseller ve patlatılmış görünümlü teknik film.',
                    'زجاج وسائل ومعدن وحجر وخزف، كلٌّ منها بإضاءة حملة. لقطات متكررة وصور وفيلم تقني بمشهد مفكك.'),
             media='amber', link='cgi'),
        dict(slug='erik-nissan', ig='erikotomotivnissan', discs=['film', 'digital'], client='Erik Otomotiv · Nissan',
             sector=t('Automotive', 'Otomotiv', 'السيارات'),
             title=t('TV spot and Reels campaigns', 'TV reklamı ve Reels kampanyaları', 'إعلان تلفزيوني وحملات Reels'),
             text=t('A Kurban Bayramı film cut for TV and Reels, plus Reels campaigns for Juke, Townstar, Qashqai and X-Trail, scripted scene by scene.',
                    'TV ve Reels için kurgulanan Kurban Bayramı filmi; Juke, Townstar, Qashqai ve X-Trail için sahne sahne yazılmış Reels kampanyaları.',
                    'فيلم لعيد الأضحى بنسختين للتلفزيون وReels، وحملات Reels لطرازات Juke وTownstar وQashqai وX-Trail، مكتوبة مشهدًا بمشهد.')),
        dict(slug='festival', discs=['film', 'digital'], client=t('Şanlıurfa Sports, Life & Entertainment Festival', 'Şanlıurfa Spor, Yaşam ve Eğlence Festivali', 'مهرجان شانلي أورفا للرياضة والحياة والترفيه'),
             sector=t('Events', 'Etkinlik', 'الفعاليات'),
             title=t('12 films and 30 designs for one festival', 'Bir festival için 12 film ve 30 tasarım', '12 فيلمًا و30 تصميمًا لمهرجان واحد'),
             text=t('A two-phase campaign: stand sales to exhibitors first, then public attendance, with second-by-second scripts and music direction.',
                    'İki aşamalı kampanya: önce katılımcılara stant satışı, ardından halkın katılımı; saniye saniye senaryolar ve müzik yönü.',
                    'حملة على مرحلتين: بيع الأجنحة للعارضين أولًا، ثم جذب الجمهور، مع نصوص ثانية بثانية وتوجيه موسيقي.')),
        dict(slug='sembol', ig='mutfacto', discs=['drone', 'film'], client='Mutfacto × Sembol Ocakbaşı',
             sector=t('Industrial kitchens', 'Endüstriyel mutfak', 'المطابخ الصناعية'),
             title=t('Drone fly-through of a restaurant kitchen', 'Restoran mutfağında drone uçuşu', 'جولة بالدرون داخل مطبخ مطعم'),
             text=t('One continuous flight through the industrial kitchen Mutfacto built for Sembol Ocakbaşı, from the dining room to the grill.',
                    "Mutfacto'nun Sembol Ocakbaşı için kurduğu endüstriyel mutfakta, salondan ocağa kesintisiz tek uçuş.",
                    'رحلة متواصلة واحدة داخل المطبخ الصناعي الذي أنشأته Mutfacto لمطعم Sembol، من الصالة حتى الشواية.')),
        dict(slug='turbo-atom', ig='mutfacto', discs=['film'], client='Mutfacto × Turbo Atom',
             sector=t('Industrial kitchens', 'Endüstriyel mutfak', 'المطابخ الصناعية'),
             title=t('Presenter-led customer story', 'Sunuculu müşteri hikâyesi', 'قصة عميل يقدّمها مذيع'),
             text=t('A testimonial film with a presenter intro, interview and product visuals, made for social media on the supplier\'s behalf.',
                    'Tedarikçi adına sosyal medya için çekilen; sunucu girişi, röportaj ve ürün görselleri içeren referans filmi.',
                    'فيلم شهادة عميل بمقدمة مذيع ومقابلة وصور للمنتجات، أُنتج لوسائل التواصل نيابةً عن المورّد.')),
        dict(slug='maharet', ig='maharetrestaurant', discs=['film', 'drone', 'cgi', 'digital'], client='Maharet Ocakbaşı',
             sector=t('Restaurant', 'Restoran', 'مطعم'),
             title=t('Reels series, 3D logo and Meta ads', 'Reels serisi, 3D logo ve Meta reklamları', 'سلسلة Reels وشعار ثلاثي الأبعاد وإعلانات Meta'),
             text=t('Fast natural-sound Reels with drone openers and speed ramps, a looping brushed-metal 3D logo, and the restaurant\'s Meta ad campaigns.',
                    'Drone açılışlı, hız rampalı, doğal sesli hızlı Reels; fırçalanmış metal 3D logo döngüsü ve restoranın Meta reklam kampanyaları.',
                    'مقاطع Reels سريعة بالصوت الطبيعي وافتتاحيات بالدرون، وشعار معدني ثلاثي الأبعاد متكرر، وحملات Meta الإعلانية للمطعم.')),
        dict(slug='minik-dehalar', ig='minikdehalar.kres', discs=['film', 'digital'], client='Minik Dehalar',
             sector=t('Education', 'Eğitim', 'التعليم'),
             title=t('Reels series, ads and print for a preschool', 'Bir anaokulu için Reels, reklam ve basılı işler', 'Reels وإعلانات ومطبوعات لروضة أطفال'),
             text=t('A seven-part Reels series mixing real class footage with illustration, WhatsApp-objective Meta ads and printed brochures.',
                    'Gerçek sınıf görüntülerini illüstrasyonla birleştiren yedi bölümlük Reels serisi, WhatsApp hedefli Meta reklamları ve broşürler.',
                    'سلسلة Reels من سبعة أجزاء تمزج لقطات الصفوف الحقيقية بالرسوم، وإعلانات Meta بهدف واتساب، وكتيبات مطبوعة.')),
        dict(slug='zarifzade', discs=['digital'], client='Zarifzade Baklava',
             sector=t('Food retail', 'Gıda perakende', 'تجزئة الأغذية'),
             title=t('E-commerce site and store-opening ads', 'E-ticaret sitesi ve mağaza açılış reklamları', 'متجر إلكتروني وإعلانات افتتاح فرع'),
             text=t('zarifzade.com.tr on ikas, rebuilt so orders land in WhatsApp with cash on delivery, plus Meta ads for the Sancaktepe opening.',
                    "ikas üzerinde zarifzade.com.tr; siparişler WhatsApp'a düşecek, kapıda ödeme alınacak şekilde kurgulandı. Sancaktepe açılışı için Meta reklamları.",
                    'موقع zarifzade.com.tr على منصة ikas، أُعيد بناؤه لتصل الطلبات إلى واتساب مع الدفع عند الاستلام، وإعلانات Meta لافتتاح فرع سنجق تبه.')),
        dict(slug='home-art-bistro', discs=['digital', 'photo'], client='Home Art Bistro',
             sector=t('Café & interiors', 'Kafe ve iç mimari', 'مقهى وتصميم داخلي'),
             title=t('Content strategy with photo and video scripts', 'Fotoğraf ve video senaryolu içerik stratejisi', 'استراتيجية محتوى مع نصوص للتصوير والفيديو'),
             text=t('A minimal, editorial direction replacing generic posts: a 14-piece calendar with a shot plan for every photo and video.',
                    'Sıradan paylaşımların yerine minimal, editoryal bir yön: her fotoğraf ve video için çekim planı olan 14 içerikli takvim.',
                    'توجه بسيط وتحريري بدل المنشورات العامة: تقويم من 14 محتوى مع خطة تصوير لكل صورة وفيديو.')),
        dict(slug='mozaik-series', ig='mozaikfilm', discs=['film', 'digital'], client='Mozaik Film',
             sector=t('Own brand', 'Kendi markamız', 'علامتنا'),
             title=t('Motion-collage ad series', 'Hareketli kolaj reklam serisi', 'سلسلة إعلانات بأسلوب الكولاج المتحرك'),
             text=t('Short narrated films in a torn-paper collage style explaining to local businesses why planned content and paid ads matter.',
                    'Yırtık kâğıt kolaj tarzında, yerel işletmelere planlı içeriğin ve sponsorlu reklamın neden önemli olduğunu anlatan kısa seslendirmeli filmler.',
                    'أفلام قصيرة بتعليق صوتي وأسلوب كولاج الورق الممزق، تشرح للشركات المحلية أهمية المحتوى المخطط والإعلانات المدفوعة.')),
    ]
    wall = ['National Geographic', 'New York Times', 'Şanlıurfa Büyükşehir Belediyesi', 'Haliliye Belediyesi', 'Transfomax',
            'Ferat Dalgıç Pompa', 'İmbo Boru', 'Korkmaz Süt', 'Canoğlu Grup', 'Yetimoğlu Grup', 'Rima Grup', 'Gapsan Tekstil',
            'Bahçeşehir Koleji', 'TED Koleji', 'Çamlıca Koleji', 'Endülüs Koleji', 'Nissan · Erik Otomotiv', 'Pirelli · Badıllı',
            'Ceramo Seramik', 'Öztiryakiler', 'Mutfacto', 'Miroğlu Künefe', 'Taşsaray', 'Tatvera', 'Maharet', 'Minik Dehalar',
            'Zarifzade Baklava', 'Esomed', 'Saudi Halsa', 'Durrah App', 'IYGO Lojistik', 'Uluyıl İnşaat']

    def L3(x):
        return t(*x) if isinstance(x, tuple) else x

    def vid_card(v, big=False):
        client = L3(v['client'])
        kind, sector = t(*refs.KIND[v['kind']]), t(*refs.SECTOR[v['sector']])
        thumb = v.get('thumb') or f"https://i.ytimg.com/vi/{v['v']}/hqdefault.jpg"
        vers = ''
        if v.get('versions'):
            vers = '<div class="vers">' + ''.join(
                f'<button type="button" data-yt="{i}"{" data-short=1" if v.get("short") else ""}>{lab}</button>' for lab, i in v['versions']) + '</div>'
        note = f"<p>{t(*v['note'])}</p>" if big and v.get('note') else ''
        return f'''
      <article class="proj{' big' if big else ''}" data-d="{' '.join(v['discs'])}">
        <button type="button" class="m play" data-yt="{v['v']}"{" data-short=1" if v.get("short") else ""} aria-label="{t('Play', 'Oynat', 'تشغيل')}: {client}"><img src="{thumb}" alt="{client} · {kind}" loading="lazy"><span class="pi" aria-hidden="true"></span></button>
        <div class="meta"><span>{kind}</span><span>{sector}</span></div>
        <h3>{client}</h3>{note}{vers}
      </article>'''

    def proj_card(p):
        m = media(p['slug'] if p.get('media') is None else p['media'], f"{p['client']} · {p['title']}",
                  fallback=(p['sector'], p['client']))
        tags = ''.join(f'<span>{DISC[d]}</span>' for d in p['discs'])
        link = f'<a class="tlink" href="{U(p["link"])}">{t("See the work", "İşi gör", "شاهد العمل")} {arrow}</a>' if p.get('link') else ''
        if p.get('ig'):
            link += f'<a class="tlink" href="https://www.instagram.com/{p["ig"]}/" target="_blank" rel="noopener">Instagram @{p["ig"]} {ext}</a>'
        return f'''
      <article class="proj" data-d="{' '.join(p['discs'])}">
        <div class="m">{m}</div>
        <div class="meta"><span>{p['client']}</span><span>{p['sector']}</span></div>
        <h3>{p['title']}</h3>
        <p>{p['text']}</p>
        <div class="meta">{tags}</div>{link}
      </article>'''

    def projs_for(d, limit=6):
        vids = [v for v in refs.VIDEOS if d in v['discs']]
        vids.sort(key=lambda v: not v.get('feat'))
        out = ''.join(vid_card(v, big=bool(v.get('feat'))) for v in vids[:limit])
        n = limit - len(vids[:limit])
        if n > 0:
            out += ''.join(proj_card(p) for p in [p for p in projects if d in p['discs']][:n])
        return out

    # ------------------------------------------------------------------ shared pieces
    def block_html(blocks):
        out = ''
        for i, (h, line, items) in enumerate(blocks):
            lis = ''.join(f'<li>{x}</li>' for x in items)
            out += f'''
      <article class="block"><span class="num">{i+1:02d}</span><h3>{h}</h3><p class="lead">{line}</p><ul>{lis}</ul></article>'''
        return out

    def steps_html(steps):
        return ''.join(f'<li><span class="num">{i+1:02d}</span><h3>{h}</h3><p>{p}</p></li>' for i, (h, p) in enumerate(steps))

    generic_steps = [
        (t('Brief', 'Brief', 'الملخص'), t('Tell me what you sell, where it will run and when you need it.', 'Ne sattığınızı, nerede yayınlanacağını ve ne zaman lazım olduğunu anlatın.', 'أخبرني ماذا تبيع وأين سيُعرض ومتى تحتاجه.')),
        (t('Plan', 'Plan', 'الخطة'), t('Script, shot list and schedule, approved by you before a camera moves.', 'Kamera çalışmadan önce sizin onayınızla senaryo, çekim listesi ve takvim.', 'نص وقائمة لقطات وجدول، توافق عليها قبل أن تتحرك الكاميرا.')),
        (t('Shoot & edit', 'Çekim ve kurgu', 'التصوير والمونتاج'), t('Production, edit, colour and sound by the same team, with previews along the way.', 'Çekim, kurgu, renk ve ses aynı ekipten; süreç boyunca önizlemelerle.', 'التصوير والمونتاج والألوان والصوت من الفريق نفسه، مع معاينات خلال العمل.')),
        (t('Delivery', 'Teslim', 'التسليم'), t('Masters in every format you need: TV, web, Reels, stories and ads.', 'İhtiyacınız olan her formatta final dosyalar: TV, web, Reels, hikâye ve reklam.', 'نسخ نهائية بكل الصيغ التي تحتاجها: تلفزيون وويب وReels وقصص وإعلانات.')),
    ]

    def page_hero(eyebrow, h1, sub, lead):
        return f'''
<section class="phero">
  <div class="wrap">
    <p class="crumbs"><a href="{U('home')}">Bilal Rahat</a> / {eyebrow}</p>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}<span class="sub">{sub}</span></h1>
    <p class="lead">{lead}</p>
  </div>
</section>'''

    def band(id_, eyebrow, h2, sub, inner, cls=''):
        sub = f'<span class="sub">{sub}</span>' if sub else ''
        idattr = f' id="{id_}"' if id_ else ''
        return f'''
<section class="band{cls}"{idattr}>
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h2>{h2}{sub}</h2>{inner}
  </div>
</section>'''

    def projects_band(d, h2):
        return band('work', t('Selected references', 'Seçili referanslar', 'مراجع مختارة'), h2, '',
                    f'<div class="projs">{projs_for(d)}\n    </div>'
                    f'<p style="margin-top:40px"><a class="tlink" href="{U("references")}">{t("All references", "Tüm referanslar", "كل المراجع")} {arrow}</a></p>')

    def process_band(steps):
        return band('process', t('Process', 'Süreç', 'طريقة العمل'), t('How every project runs.', 'Her proje nasıl ilerler.', 'كيف يسير كل مشروع.'), '',
                    f'<ol class="steps">{steps_html(steps)}</ol>')

    quote_note = t('Every project is quoted to its scope. Send the brief and you get a written quote within one working day.',
                   'Her proje kapsamına göre fiyatlandırılır. Brief gönderin, bir iş günü içinde yazılı teklif alın.',
                   'يُسعَّر كل مشروع حسب نطاقه. أرسل الملخص وتصلك عرض سعر مكتوب خلال يوم عمل واحد.')

    def cta_band():
        return f'''
<section class="band" id="start">
  <div class="wrap cta">
    <div>
      <p class="eyebrow">{t('Your next project', 'Sıradaki projeniz', 'مشروعك القادم')}</p>
      <h2>{t('Tell me what you need to sell.', 'Ne satmanız gerektiğini anlatın.', 'أخبرني ماذا تريد أن تبيع.')}</h2>
      <p class="lead" style="margin-top:22px">{quote_note}</p>
    </div>
    <div class="ctas" style="margin-top:0">
      <a class="box solid" href="mailto:{EMAIL}">{t('Email the brief', 'Brief gönderin', 'أرسل الملخص')} {ext}</a>
      <a class="box" href="{WA}">WhatsApp {ext}</a>
    </div>
  </div>
</section>'''

    # ------------------------------------------------------------------ pages
    if page == 'home':
        title = t('Bilal Rahat · Film, CGI & AI Director', 'Bilal Rahat · Film, CGI ve Yapay Zekâ Yönetmeni', 'بلال راحت · مخرج أفلام وCGI وذكاء اصطناعي')
        desc = t('Commercials, 3D product CGI, FPV drone films, photography, websites and ad campaigns, directed by Bilal Rahat, founder of Mozaik Film.',
                 "Mozaik Film'in kurucusu Bilal Rahat'tan reklam filmleri, 3D ürün CGI, FPV drone filmleri, fotoğraf, web siteleri ve reklam kampanyaları.",
                 'إعلانات وCGI ثلاثي الأبعاد للمنتجات وأفلام درون FPV وتصوير ومواقع وحملات إعلانية، بإخراج بلال راحت مؤسس موزاييك فيلم.')
        discs = [
            ('cgi', 'amber', t('3D product CGI', '3D ürün CGI', 'CGI ثلاثي الأبعاد للمنتجات'),
             t('Photoreal product films, loops and stills made in Blender. No shoot needed.', "Blender'da foto-gerçekçi ürün filmleri, döngüler ve görseller. Çekime gerek yok.", 'أفلام ولقطات وصور واقعية للمنتجات في Blender، دون تصوير.')),
            ('film', 'film', t('Commercials & brand films', 'Reklam ve tanıtım filmleri', 'الإعلانات وأفلام العلامات'),
             t('TV spots, corporate films, Reels and presenter-led content, scripted to sell.', 'TV reklamları, kurumsal filmler, Reels ve sunuculu içerikler; satmak için yazılır.', 'إعلانات تلفزيونية وأفلام مؤسسية وReels ومحتوى بمذيع، مكتوبة لتبيع.')),
            ('drone', 'drone-fpv', t('FPV drone & aerial', 'FPV drone ve hava çekimi', 'درون FPV وتصوير جوي'),
             t('One-take FPV flights through venues, kitchens, factories and hotels.', 'Mekân, mutfak, fabrika ve otellerin içinden tek plan FPV uçuşlar.', 'رحلات FPV بلقطة واحدة داخل الأماكن والمطابخ والمصانع والفنادق.')),
            ('photo', 'photo', t('Product & venue photography', 'Ürün ve mekân fotoğrafı', 'تصوير المنتجات والأماكن'),
             t('Studio packshots, food and hospitality photography for menus, sites and ads.', 'Menü, site ve reklam için stüdyo ürün, yemek ve otel-mekân fotoğrafları.', 'صور استوديو للمنتجات والطعام والضيافة للقوائم والمواقع والإعلانات.')),
            ('digital', 'digital', t('Web, ads & social', 'Web, reklam ve sosyal medya', 'الويب والإعلانات والتواصل'),
             t('Websites, QR menus, Meta and Google ads, and the content plan behind them.', 'Web siteleri, QR menüler, Meta ve Google reklamları ve arkalarındaki içerik planı.', 'مواقع وقوائم QR وإعلانات Meta وGoogle وخطة المحتوى خلفها.')),
            ('references', 'references', t('Reference portfolio', 'Referans portfolyosu', 'ملف المراجع'),
             t('Projects for automotive, hospitality, education, events and industry.', 'Otomotiv, ağırlama, eğitim, etkinlik ve sanayi için yapılan projeler.', 'مشاريع للسيارات والضيافة والتعليم والفعاليات والصناعة.')),
        ]
        cards = ''
        for i, (p, slug, h, line) in enumerate(discs):
            m = media(slug, h, fallback=(t('Mozaik Film', 'Mozaik Film', 'موزاييك فيلم'), f'{i+1:02d}'))
            cards += f'''
      <a class="disc" href="{U(p)}"><div class="m">{m}</div><div class="b"><span class="num">{i+1:02d}</span><h3>{h}</h3><p>{line}</p><span class="tlink">{t('Open', 'Aç', 'افتح')} {arrow}</span></div></a>'''
        home_pick = [v for v in refs.VIDEOS if v['v'] in ('y8e8dVpC8Y8', 'CaEpDxcQTCc', 'gI_szqyD9NU', 'JT1DtpHhIiQ', '1r3RrJj6mlE', 'uEO5Zouc2eI')]
        clients = ['National Geographic', 'New York Times', 'Nissan', 'Bahçeşehir Koleji', 'Öztiryakiler', 'Gapsan Tekstil', 'Transfomax', 'Ferat Dalgıç Pompa']
        body = f'''
<section class="hero">
  {media('amber', t('Amber perfume bottle rendered in Blender', "Blender'da render edilmiş amber parfüm şişesi", 'زجاجة عطر عنبرية مصنوعة في Blender'), eager=True)}
  <div class="wrap">
    <p class="eyebrow">{t('Film · CGI · Drone · Photo · Digital', 'Film · CGI · Drone · Fotoğraf · Dijital', 'أفلام · CGI · درون · تصوير · رقمي')}</p>
    <h1>{t('One director.', 'Tek yönetmen.', 'مخرج واحد.')}<span class="sub">{t('Every way a brand needs to be seen.', 'Bir markanın görünmesi gereken her yol.', 'بكل الطرق التي تحتاج العلامة أن تُرى بها.')}</span></h1>
    <p class="lead">{t('Commercials, 3D product films, FPV drone, photography, websites and ad campaigns. Since 2009, with the Mozaik Film team behind every project.', "Reklam filmleri, 3D ürün filmleri, FPV drone, fotoğraf, web siteleri ve reklam kampanyaları. 2009'dan beri, her projenin arkasında Mozaik Film ekibiyle.", 'إعلانات وأفلام منتجات ثلاثية الأبعاد ودرون FPV وتصوير ومواقع وحملات إعلانية. منذ 2009، مع فريق موزاييك فيلم خلف كل مشروع.')}</p>
    <a class="tlink" href="#disciplines">{t('See what I make', 'Neler ürettiğimi görün', 'شاهد ما أصنعه')} {arrow}</a>
  </div>
</section>

<section class="clients" aria-label="{t('Productions for', 'Çalıştığımız markalar', 'إنتاجات لصالح')}">
  <div class="wrap"><small>{t('Productions for', 'Çalıştığımız markalar', 'إنتاجات لصالح')}</small>{''.join(f'<span>{c}</span>' for c in clients)}</div>
</section>
''' + band('disciplines', t('What I make', 'Ne üretiyorum?', 'ماذا أصنع'),
           t('Six ways to work together.', 'Birlikte çalışmanın altı yolu.', 'ست طرق للعمل معًا.'),
           t('Each with its own page.', 'Her birinin kendi sayfası var.', 'لكلٍّ منها صفحته.'),
           f'<div class="discs">{cards}\n    </div>') + \
        band('work', t('Recent references', 'Son referanslar', 'أحدث المراجع'),
             t('Work across every discipline.', 'Her disiplinden işler.', 'أعمال في كل التخصصات.'), '',
             f'<div class="projs">{"".join(vid_card(v, big=True) for v in home_pick)}\n    </div>'
             f'<p style="margin-top:40px"><a class="tlink" href="{U("references")}">{t("All references", "Tüm referanslar", "كل المراجع")} {arrow}</a></p>') + \
        studio_band(t, ext) + cta_band()

    elif page == 'cgi':
        title = t('3D Product CGI · Bilal Rahat', '3D Ürün CGI · Bilal Rahat', 'CGI ثلاثي الأبعاد للمنتجات · بلال راحت')
        desc = t('Photoreal product films, loops and launch visuals made in Blender, for brands in Europe, the US and the Gulf.',
                 "Avrupa, ABD ve Körfez'deki markalar için Blender'da foto-gerçekçi ürün filmleri, döngüler ve lansman görselleri.",
                 'أفلام ولقطات متكررة وصور إطلاق واقعية للمنتجات في Blender، لعلامات في أوروبا والولايات المتحدة والخليج.')
        body = cgi_body(t, arrow, ext, U)

    elif page == 'film':
        title = t('Commercials & Brand Films · Bilal Rahat', 'Reklam ve Tanıtım Filmleri · Bilal Rahat', 'الإعلانات وأفلام العلامات · بلال راحت')
        desc = t('TV commercials, corporate films, Reels and presenter-led content, scripted, shot, edited and graded by one team.',
                 'TV reklamları, kurumsal filmler, Reels ve sunuculu içerikler; tek ekip tarafından yazılır, çekilir, kurgulanır ve renklendirilir.',
                 'إعلانات تلفزيونية وأفلام مؤسسية وReels ومحتوى بمذيع، يكتبها ويصورها ويمنتجها فريق واحد.')
        blocks = [
            (t('Commercials', 'Reklam filmleri', 'الإعلانات'), t('Spots built around one idea that sells.', 'Satan tek bir fikir etrafında kurulan reklamlar.', 'إعلانات مبنية حول فكرة واحدة تبيع.'),
             [t('TV and cinema spots', 'TV ve sinema reklamları', 'إعلانات التلفزيون والسينما'), t('Seasonal and holiday campaigns', 'Sezon ve bayram kampanyaları', 'حملات المواسم والأعياد'),
              t('Script and storyboard', 'Senaryo ve storyboard', 'النص ولوحة القصة'), t('Cast, location and crew', 'Oyuncu, mekân ve ekip', 'الممثلون والموقع والطاقم')]),
            (t('Corporate & promo films', 'Kurumsal ve tanıtım filmleri', 'أفلام مؤسسية وترويجية'), t('Who you are, shown in a few minutes.', 'Kim olduğunuz, birkaç dakikada.', 'من أنت، في دقائق قليلة.'),
             [t('Company and factory films', 'Firma ve fabrika filmleri', 'أفلام الشركات والمصانع'), t('Hotel, restaurant and venue films', 'Otel, restoran ve mekân filmleri', 'أفلام الفنادق والمطاعم والأماكن'),
              t('Event and festival films', 'Etkinlik ve festival filmleri', 'أفلام الفعاليات والمهرجانات'), t('Documentary production', 'Belgesel prodüksiyon', 'إنتاج وثائقي')]),
            (t('Reels & short-form', 'Reels ve kısa video', 'Reels والفيديو القصير'), t('Vertical content made for the first second.', 'İlk saniye için üretilmiş dikey içerik.', 'محتوى عمودي مصنوع للثانية الأولى.'),
             [t('Monthly Reels series', 'Aylık Reels serileri', 'سلاسل Reels شهرية'), t('Hooks, captions and CTAs', 'Kanca, altyazı ve CTA', 'افتتاحيات وترجمات ودعوات للتفاعل'),
              t('Motion graphics and collage', 'Motion grafik ve kolaj', 'موشن جرافيك وكولاج'), t('Cut-downs for ads', 'Reklam için kısa versiyonlar', 'نسخ قصيرة للإعلانات')]),
            (t('Presenter & interview', 'Sunuculu ve röportaj', 'مذيع ومقابلات'), t('A face and a voice for your brand.', 'Markanız için bir yüz ve ses.', 'وجه وصوت لعلامتك.'),
             [t('Presenter-led product films', 'Sunuculu ürün filmleri', 'أفلام منتجات بمذيع'), t('Customer testimonials', 'Müşteri referans filmleri', 'شهادات العملاء'),
              t('Voice-over in Turkish, English, Arabic', 'Türkçe, İngilizce, Arapça seslendirme', 'تعليق صوتي بالتركية والإنجليزية والعربية'), t('Editing, colour grading and sound', 'Kurgu, renk ve ses', 'المونتاج والألوان والصوت')]),
        ]
        body = page_hero(NAV['film'], t('Commercials', 'Reklam filmleri', 'الإعلانات'),
                         t('and brand films that sell.', 've satan tanıtım filmleri.', 'وأفلام علامات تبيع.'),
                         t('TV spots, corporate films, Reels and presenter-led content. Written, shot, edited and graded by one team, from Mozaik Film since 2009.',
                           "TV reklamları, kurumsal filmler, Reels ve sunuculu içerikler. 2009'dan beri Mozaik Film'de tek ekip tarafından yazılır, çekilir, kurgulanır ve renklendirilir.",
                           'إعلانات تلفزيونية وأفلام مؤسسية وReels ومحتوى بمذيع. يكتبها ويصورها ويمنتجها فريق واحد في موزاييك فيلم منذ 2009.')) + \
            band('services', t('Services', 'Hizmetler', 'الخدمات'), t('From the script to the final grade.', 'Senaryodan son renk düzenlemesine.', 'من النص حتى التصحيح اللوني الأخير.'), '',
                 f'<div class="blocks">{block_html(blocks)}\n    </div>') + \
            projects_band('film', t('Films we have made.', 'Çektiğimiz filmler.', 'أفلام صنعناها.')) + \
            process_band(generic_steps) + cta_band()

    elif page == 'drone':
        title = t('FPV Drone & Aerial Films · Bilal Rahat', 'FPV Drone ve Hava Çekimi · Bilal Rahat', 'أفلام درون FPV والتصوير الجوي · بلال راحت')
        desc = t('One-take FPV drone flights through venues, kitchens, factories and hotels, and aerial cinematography for commercials.',
                 'Mekân, mutfak, fabrika ve otellerin içinden tek plan FPV drone uçuşları ve reklamlar için hava çekimi.',
                 'رحلات درون FPV بلقطة واحدة داخل الأماكن والمطابخ والمصانع والفنادق، وتصوير جوي للإعلانات.')
        blocks = [
            (t('FPV one-take films', 'FPV tek plan filmler', 'أفلام FPV بلقطة واحدة'), t('One continuous flight that tours the whole place.', 'Tüm mekânı gezen kesintisiz tek uçuş.', 'رحلة متواصلة واحدة تجول في المكان كله.'),
             [t('Restaurants and kitchens', 'Restoran ve mutfaklar', 'المطاعم والمطابخ'), t('Hotels and venues', 'Otel ve mekânlar', 'الفنادق والأماكن'),
              t('Factories and showrooms', 'Fabrika ve showroomlar', 'المصانع وصالات العرض'), t('Planned route, rehearsed before the take', 'Çekim öncesi provası yapılan planlı rota', 'مسار مخطط يُتدرّب عليه قبل اللقطة')]),
            (t('Aerial cinematography', 'Hava sinematografisi', 'التصوير السينمائي الجوي'), t('Scale and place for commercials and city films.', 'Reklam ve şehir filmleri için ölçek ve mekân hissi.', 'إحساس بالحجم والمكان للإعلانات وأفلام المدن.'),
             [t('Openers with speed ramps', 'Hız rampalı açılışlar', 'افتتاحيات بتغيير السرعة'), t('Real estate and construction', 'Emlak ve inşaat', 'العقارات والإنشاءات'),
              t('Events and festivals', 'Etkinlik ve festivaller', 'الفعاليات والمهرجانات'), t('Heritage and tourism', 'Tarih ve turizm', 'التراث والسياحة')]),
        ]
        body = page_hero(NAV['drone'], t('FPV drone', 'FPV drone', 'درون FPV'),
                         t('One flight, the whole story.', 'Tek uçuş, bütün hikâye.', 'رحلة واحدة، القصة كلها.'),
                         t('One-take FPV films that fly through a venue the way a guest walks it, and aerial shots that give a commercial its scale.',
                           'Bir mekânın içinden, bir misafirin gezdiği gibi uçan tek plan FPV filmler ve bir reklama ölçeğini veren hava çekimleri.',
                           'أفلام FPV بلقطة واحدة تطير داخل المكان كما يتجول فيه الضيف، ولقطات جوية تمنح الإعلان حجمه.')) + \
            band('services', t('Services', 'Hizmetler', 'الخدمات'), t('Inside and above.', 'İçeride ve yukarıda.', 'في الداخل ومن الأعلى.'), '',
                 f'<div class="blocks">{block_html(blocks)}\n    </div>') + \
            projects_band('drone', t('Flights we have made.', 'Yaptığımız uçuşlar.', 'رحلات صوّرناها.')) + \
            process_band(generic_steps) + cta_band()

    elif page == 'photo':
        title = t('Product & Venue Photography · Bilal Rahat', 'Ürün ve Mekân Fotoğrafı · Bilal Rahat', 'تصوير المنتجات والأماكن · بلال راحت')
        desc = t('Studio product photography, food and hospitality photography for menus, websites, e-commerce and ads.',
                 'Menü, web sitesi, e-ticaret ve reklam için stüdyo ürün, yemek ve otel-mekân fotoğrafçılığı.',
                 'تصوير منتجات في الاستوديو وتصوير الطعام والضيافة للقوائم والمواقع والمتاجر والإعلانات.')
        blocks = [
            (t('Product & studio', 'Ürün ve stüdyo', 'المنتجات والاستوديو'), t('Clean packshots and styled key visuals.', 'Temiz ürün çekimleri ve kurgulanmış ana görseller.', 'صور منتجات نظيفة وصور رئيسية منسقة.'),
             [t('White-background e-commerce', 'Beyaz fon e-ticaret', 'خلفية بيضاء للمتاجر'), t('Styled and lifestyle shots', 'Kurgulu ve yaşam tarzı kareler', 'لقطات منسقة وأسلوب حياة'),
              t('Retouching and cut-outs', 'Rötuş ve dekupe', 'التنقيح والقص'), t('Or CGI when the product is not ready yet', 'Ürün hazır değilse CGI', 'أو CGI إن لم يكن المنتج جاهزًا')]),
            (t('Food & hospitality', 'Yemek ve ağırlama', 'الطعام والضيافة'), t('Menus that make people order.', 'Sipariş verdiren menüler.', 'قوائم تجعل الناس يطلبون.'),
             [t('Menu and QR-menu photography', 'Menü ve QR menü fotoğrafları', 'صور القوائم وقوائم QR'), t('Restaurant and hotel interiors', 'Restoran ve otel iç mekânları', 'التصميم الداخلي للمطاعم والفنادق'),
              t('Chef and kitchen portraits', 'Şef ve mutfak portreleri', 'صور الطهاة والمطابخ'), t('Social media sets', 'Sosyal medya setleri', 'مجموعات لوسائل التواصل')]),
        ]
        body = page_hero(NAV['photo'], t('Photography', 'Fotoğraf', 'التصوير'),
                         t('for menus, sites and ads.', 'menü, site ve reklam için.', 'للقوائم والمواقع والإعلانات.'),
                         t('Product, food and venue photography shot with the same eye as our films, and delivered ready for e-commerce, print and paid social.',
                           'Filmlerimizle aynı gözle çekilen; e-ticaret, baskı ve sponsorlu reklama hazır teslim edilen ürün, yemek ve mekân fotoğrafları.',
                           'تصوير المنتجات والطعام والأماكن بالعين نفسها التي نصوّر بها أفلامنا، جاهزة للمتاجر والطباعة والإعلانات.')) + \
            band('services', t('Services', 'Hizmetler', 'الخدمات'), t('Every picture with a job to do.', 'Her fotoğrafın bir görevi var.', 'لكل صورة مهمة.'), '',
                 f'<div class="blocks">{block_html(blocks)}\n    </div>') + \
            projects_band('photo', t('Recent photography.', 'Son fotoğraf işleri.', 'أحدث أعمال التصوير.')) + \
            process_band(generic_steps) + cta_band()

    elif page == 'digital':
        title = t('Web, Ads & Social · Bilal Rahat', 'Web, Reklam ve Sosyal Medya · Bilal Rahat', 'الويب والإعلانات والتواصل · بلال راحت')
        desc = t('Websites, e-commerce, QR menus, Meta and Google ads management, and social media content strategy.',
                 'Web siteleri, e-ticaret, QR menüler, Meta ve Google reklam yönetimi ve sosyal medya içerik stratejisi.',
                 'مواقع ومتاجر إلكترونية وقوائم QR وإدارة إعلانات Meta وGoogle واستراتيجية محتوى للتواصل الاجتماعي.')
        blocks = [
            (t('Websites & e-commerce', 'Web sitesi ve e-ticaret', 'المواقع والمتاجر الإلكترونية'), t('Sites that turn a visit into an order.', 'Ziyareti siparişe çeviren siteler.', 'مواقع تحوّل الزيارة إلى طلب.'),
             [t('Company and portfolio sites', 'Kurumsal ve portfolyo siteleri', 'مواقع الشركات والملفات'), t('E-commerce on ikas and similar', 'ikas ve benzeri altyapılarda e-ticaret', 'متاجر على ikas وما يشبهها'),
              t('WhatsApp ordering flows', 'WhatsApp sipariş kurgusu', 'الطلب عبر واتساب'), t('Domain, hosting and corporate email', 'Alan adı, barındırma ve kurumsal e-posta', 'النطاق والاستضافة والبريد المؤسسي')]),
            (t('QR menus & sales pages', 'QR menü ve satış sayfaları', 'قوائم QR وصفحات البيع'), t('One scan from table to order.', 'Masadan siparişe tek okutma.', 'مسح واحد من الطاولة إلى الطلب.'),
             [t('QR menus for restaurants and cafés', 'Restoran ve kafeler için QR menü', 'قوائم QR للمطاعم والمقاهي'), t('QR sales pages for products', 'Ürünler için QR satış sayfaları', 'صفحات بيع QR للمنتجات'),
              t('Photographed and written by us', 'Fotoğrafı ve metni bizden', 'نصوّرها ونكتبها بأنفسنا'), t('Easy price updates', 'Kolay fiyat güncelleme', 'تحديث الأسعار بسهولة')]),
            (t('Meta & Google ads', 'Meta ve Google reklamları', 'إعلانات Meta وGoogle'), t('Campaigns run by the people who make the creative.', 'Kreatifi üreten ekip tarafından yönetilen kampanyalar.', 'حملات يديرها من يصنعون المحتوى.'),
             [t('Account and pixel setup', 'Hesap ve piksel kurulumu', 'إعداد الحساب والبكسل'), t('Message, traffic and awareness campaigns', 'Mesaj, trafik ve bilinirlik kampanyaları', 'حملات الرسائل والزيارات والوعي'),
              t('Local targeting by neighbourhood', 'Mahalle bazında yerel hedefleme', 'استهداف محلي حسب الحي'), t('Google Business profile', 'Google İşletme profili', 'ملف Google التجاري')]),
            (t('Social media content', 'Sosyal medya içeriği', 'محتوى التواصل الاجتماعي'), t('A plan first, then the posts.', 'Önce plan, sonra paylaşımlar.', 'الخطة أولًا، ثم المنشورات.'),
             [t('Content strategy and calendar', 'İçerik stratejisi ve takvim', 'استراتيجية وتقويم المحتوى'), t('Page and cover redesign', 'Sayfa ve kapak yenileme', 'إعادة تصميم الصفحة والأغلفة'),
              t('Graphics, stories and Reels', 'Grafik, hikâye ve Reels', 'تصاميم وقصص وReels'), t('Scheduling in Meta Business Suite', 'Meta Business Suite ile planlama', 'الجدولة عبر Meta Business Suite')]),
        ]
        body = page_hero(NAV['digital'], t('Web, ads', 'Web, reklam', 'الويب والإعلانات'),
                         t('and the content behind them.', 've arkalarındaki içerik.', 'والمحتوى خلفها.'),
                         t('Websites, QR menus and paid campaigns, built by the same team that shoots the content, so the site, the ad and the film say the same thing.',
                           'İçeriği çeken ekip tarafından kurulan web siteleri, QR menüler ve sponsorlu kampanyalar; böylece site, reklam ve film aynı şeyi söyler.',
                           'مواقع وقوائم QR وحملات مدفوعة يبنيها الفريق نفسه الذي يصوّر المحتوى، فيقول الموقع والإعلان والفيلم الشيء نفسه.')) + \
            band('services', t('Services', 'Hizmetler', 'الخدمات'), t('Seen, then chosen.', 'Önce görünmek, sonra seçilmek.', 'أن تُرى، ثم تُختار.'), '',
                 f'<div class="blocks">{block_html(blocks)}\n    </div>') + \
            projects_band('digital', t('Digital work.', 'Dijital işler.', 'أعمال رقمية.')) + \
            process_band(generic_steps) + cta_band()

    elif page == 'references':
        title = t('References · Bilal Rahat', 'Referanslar · Bilal Rahat', 'المراجع · بلال راحت')
        desc = t('Reference portfolio of Bilal Rahat and Mozaik Film: commercials, CGI, drone, photography and digital work.',
                 'Bilal Rahat ve Mozaik Film referans portfolyosu: reklam filmleri, CGI, drone, fotoğraf ve dijital işler.',
                 'ملف مراجع بلال راحت وموزاييك فيلم: إعلانات وCGI ودرون وتصوير وأعمال رقمية.')
        chips = f'<button type="button" data-f="all" aria-pressed="true">{t("All", "Tümü", "الكل")}</button>' + \
            ''.join(f'<button type="button" data-f="{k}" aria-pressed="false">{v}</button>' for k, v in DISC.items())
        wall_html = ''.join(f'<div><b>{n}</b></div>' for n in wall)
        feat = [v for v in refs.VIDEOS if v.get('feat')]
        rest = [v for v in refs.VIDEOS if not v.get('feat')]
        acc_html = ''.join(f'<a href="https://www.instagram.com/{h}/" target="_blank" rel="noopener"><b>{n}</b><span>@{h} {ext}</span></a>' for n, h in refs.ACCOUNTS)
        recent = [p for p in projects if p['slug'] != 'cgi-studies']
        body = page_hero(NAV['references'], t('References', 'Referanslar', 'المراجع'),
                         t('Brands we have filmed, built and run.', 'Çektiğimiz, kurduğumuz ve yönettiğimiz markalar.', 'علامات صوّرناها وبنيناها وأدرناها.'),
                         t('500+ brand films since 2009, for companies in Turkey, Germany, Austria, Saudi Arabia and Dubai. Press play on any of them.',
                           "2009'dan beri Türkiye, Almanya, Avusturya, Suudi Arabistan ve Dubai'deki firmalar için 500'den fazla marka filmi. Hepsini buradan izleyebilirsiniz.",
                           'أكثر من 500 فيلم لعلامات تجارية منذ 2009، لشركات في تركيا وألمانيا والنمسا والسعودية ودبي. شاهد أيًّا منها هنا.')) + f'''
<section class="band" id="work" style="border-top:0">
  <div class="wrap">
    <p class="eyebrow">{t('Featured', 'Öne çıkanlar', 'مختارات')}</p>
    <h2>{t('Selected films.', 'Seçili filmler.', 'أفلام مختارة.')}<span class="sub">{t('Several delivered in up to four languages.', 'Bazıları dört dile kadar teslim edildi.', 'بعضها سُلّم بما يصل إلى أربع لغات.')}</span></h2>
    <div class="projs">{''.join(vid_card(v, big=True) for v in feat)}
    </div>
  </div>
</section>
<section class="band" id="archive">
  <div class="wrap">
    <p class="eyebrow">{t('Archive', 'Arşiv', 'الأرشيف')}</p>
    <h2>{t('More films.', 'Daha fazla film.', 'المزيد من الأفلام.')}</h2>
    <div class="chips" role="group" aria-label="{t('Filter by discipline', 'Disipline göre filtrele', 'تصفية حسب التخصص')}">{chips}</div>
    <div class="projs" id="projs">{''.join(vid_card(v) for v in rest)}
    </div>
    <p style="margin-top:40px"><a class="tlink" href="https://www.youtube.com/@mozaikfilm/videos" target="_blank" rel="noopener">{t('All 230+ films on YouTube', "YouTube'da 230'dan fazla film", 'أكثر من 230 فيلمًا على يوتيوب')} {ext}</a></p>
  </div>
</section>
<section class="band" id="recent">
  <div class="wrap">
    <p class="eyebrow">2026</p>
    <h2>{t('Current work.', 'Güncel işler.', 'أعمال حالية.')}<span class="sub">{t('Campaigns, Reels and ads running now.', 'Şu an yayında olan kampanyalar, Reels ve reklamlar.', 'حملات وReels وإعلانات قيد العرض الآن.')}</span></h2>
    <div class="projs">{''.join(proj_card(p) for p in recent)}
    </div>
  </div>
</section>
<section class="band" id="social">
  <div class="wrap">
    <p class="eyebrow">{t('Social media management', 'Sosyal medya yönetimi', 'إدارة وسائل التواصل')}</p>
    <h2>{t('Accounts we run.', 'Yönettiğimiz hesaplar.', 'حسابات نديرها.')}</h2>
    <div class="accs">{acc_html}</div>
  </div>
</section>''' + band('clients', t('Clients', 'Müşteriler', 'العملاء'), t('Who we have worked for.', 'Kimlerle çalıştık.', 'لمن عملنا.'), '',
                     f'<div class="wall">{wall_html}</div>') + cta_band()

    return shell(L, page, title, desc, body, NAV, t, ext)


# ---------------------------------------------------------------------- studio band (home)
def studio_band(t, ext):
    return f'''
<section class="band" id="studio">
  <div class="wrap studio">
    <div class="portrait"><img src="/assets/bilal-rahat.jpg" alt="Bilal Rahat" loading="lazy"></div>
    <div>
      <p class="eyebrow">{t('Studio', 'Stüdyo', 'الاستوديو')}</p>
      <h2>{t('A director, backed by a production company.', 'Arkasında bir prodüksiyon şirketi olan yönetmen.', 'مخرج تدعمه شركة إنتاج.')}</h2>
      <p class="lead">{t("I'm Bilal Rahat. I founded Mozaik Film in 2009 and have spent the years since filming and producing for brands, from corporate campaigns to productions for National Geographic. Today I direct commercials, CGI product films, drone work and digital campaigns, with the Mozaik team behind every project.", "Ben Bilal Rahat. 2009'da Mozaik Film'i kurdum; o günden bu yana kurumsal kampanyalardan National Geographic çekimlerine kadar markalar için film çekip prodüksiyon yapıyorum. Bugün reklam filmleri, CGI ürün filmleri, drone çekimleri ve dijital kampanyalar yönetiyorum; her projenin arkasında Mozaik ekibi var.", 'أنا بلال راحت. أسست موزاييك فيلم عام 2009، ومنذ ذلك الحين أصوّر وأنتج للعلامات التجارية، من الحملات المؤسسية إلى إنتاجات لصالح ناشيونال جيوغرافيك. اليوم أخرج الإعلانات وأفلام CGI للمنتجات وتصوير الدرون والحملات الرقمية، مع فريق موزاييك خلف كل مشروع.')}</p>
      <p class="lead">{t('Offices in Istanbul and Şanlıurfa, GMT+3, the same working day as Europe and the Gulf. English, Turkish and Arabic.', 'İstanbul ve Şanlıurfa ofisleri, GMT+3; Avrupa ve Körfez ile aynı iş günü. İngilizce, Türkçe ve Arapça.', 'مكاتب في إسطنبول وشانلي أورفا، بتوقيت GMT+3، يوم العمل نفسه مع أوروبا والخليج. الإنجليزية والتركية والعربية.')}</p>
      <div class="facts">
        <div><b>2009</b><span>{t('Mozaik Film founded', "Mozaik Film'in kuruluşu", 'تأسيس موزاييك فيلم')}</span></div>
        <div><b>500+</b><span>{t('Brand films', 'Marka filmi', 'فيلم لعلامات تجارية')}</span></div>
        <div><b>10+</b><span>{t('Production team', 'Prodüksiyon ekibi', 'فريق الإنتاج')}</span></div>
        <div><b>GMT+3</b><span>{t('Istanbul', 'İstanbul', 'إسطنبول')}</span></div>
      </div>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------------- 3D CGI page (former home page)
def cgi_body(t, arrow, ext, U):
    def vid(name, alt):
        return media(name, alt)

    services = [
        ('01', 'amber', t('CGI product films', 'CGI ürün filmleri', 'أفلام منتجات CGI'),
         t('Hero films that make a product feel worth its price.', 'Ürünü fiyatına layık hissettiren ana filmler.', 'أفلام رئيسية تجعل المنتج يبدو جديرًا بسعره.'),
         [t('Launch films', 'Lansman filmleri', 'أفلام الإطلاق'), t('Hero loops', 'Ana döngüler', 'لقطات رئيسية متكررة'),
          t('Campaign films', 'Kampanya filmleri', 'أفلام الحملات'), t('Paid social cut-downs', 'Reklam için kısa versiyonlar', 'نسخ قصيرة للإعلانات')]),
        ('02', 'serum', t('Launch visuals', 'Lansman görselleri', 'صور الإطلاق'),
         t('Stills and loops for e-commerce, social and press, without a photoshoot.', 'Fotoğraf çekimi olmadan e-ticaret, sosyal medya ve basın için görseller ve döngüler.', 'صور ولقطات متكررة للمتاجر الإلكترونية ووسائل التواصل والصحافة، دون جلسة تصوير.'),
         [t('Hero stills', 'Ana görseller', 'صور رئيسية'), t('E-commerce loops', 'E-ticaret döngüleri', 'لقطات للمتاجر الإلكترونية'),
          t('Packaging CGI', 'Ambalaj CGI', 'CGI للتغليف'), t('Social assets in 9:16, 1:1, 16:9', '9:16, 1:1, 16:9 sosyal medya içerikleri', 'محتوى بمقاسات 9:16 و1:1 و16:9')]),
        ('03', 'can', t('AI-assisted production', 'Yapay zekâ destekli prodüksiyon', 'إنتاج بمساعدة الذكاء الاصطناعي'),
         t('Generative AI for concepts, backgrounds and variations, finished by a director.', 'Konsept, arka plan ve varyasyonlar için üretken yapay zekâ; son dokunuş yönetmenden.', 'ذكاء اصطناعي توليدي للأفكار والخلفيات والنسخ، بلمسة مخرج نهائية.'),
         [t('Concept frames in days', 'Günler içinde konsept kareler', 'إطارات مفاهيمية خلال أيام'), t('Scene and background generation', 'Sahne ve arka plan üretimi', 'توليد المشاهد والخلفيات'),
          t('Variations for testing', 'Test için varyasyonlar', 'نسخ متعددة للاختبار'), t('Hybrid AI + CGI + live action', 'Hibrit yapay zekâ + CGI + canlı çekim', 'مزيج من الذكاء الاصطناعي وCGI والتصوير الحي')]),
        ('04', 'drone', t('Technical CGI', 'Teknik CGI', 'CGI تقني'),
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
        <a class="tlink" href="#start">{t('Plan this with me', 'Bunu birlikte planlayalım', 'لنخطط لهذا معًا')} {arrow}</a>
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

    return f'''
<section class="hero">
  {media('amber', t('Amber perfume bottle rendered in Blender', "Blender'da render edilmiş amber parfüm şişesi", 'زجاجة عطر عنبرية مصنوعة في Blender'), eager=True)}
  <div class="wrap">
    <p class="crumbs"><a href="{U('home')}">Bilal Rahat</a> / 3D CGI</p>
    <p class="eyebrow">{t('3D product CGI', '3D ürün CGI', 'CGI ثلاثي الأبعاد للمنتجات')}</p>
    <h1>{t('Product films', 'Ürün filmleri', 'أفلام المنتجات')}<span class="sub">{t('for brands that want to look expensive.', 'pahalı görünmek isteyen markalar için.', 'لعلامات تريد أن تبدو فاخرة.')}</span></h1>
    <p class="lead">{t('Photoreal product films, loops and launch visuals made in Blender, for brands across Europe, the US and the Gulf. No shoot, no studio, no shipping the product.', "Avrupa, ABD ve Körfez'deki markalar için Blender'da foto-gerçekçi ürün filmleri, döngüler ve lansman görselleri. Çekim yok, stüdyo yok, ürün kargolamak yok.", 'أفلام ولقطات وصور إطلاق واقعية للمنتجات في Blender، لعلامات في أوروبا والولايات المتحدة والخليج. بلا تصوير ولا استوديو ولا شحن للمنتج.')}</p>
    <a class="tlink" href="#start">{t('Tell me about your product', 'Ürününüzü anlatın', 'حدّثني عن منتجك')} {arrow}</a>
  </div>
</section>

<section class="band" id="services">
  <div class="wrap">
    <p class="eyebrow">{t('Services', 'Hizmetler', 'الخدمات')}</p>
    <h2>{t('Built in 3D.', '3D olarak üretilir.', 'مصنوع بالأبعاد الثلاثية.')}<span class="sub">{t('From the first frame to the final grade.', 'İlk kareden son renk düzenlemesine kadar.', 'من اللقطة الأولى حتى التصحيح اللوني الأخير.')}</span></h2>
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
        <a class="box solid" href="mailto:{EMAIL}">{t('Email the brief', 'Brief gönderin', 'أرسل الملخص')} {ext}</a>
        <a class="box" href="{WA}">WhatsApp {ext}</a>
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
</section>'''


# ---------------------------------------------------------------------- structured data (Google)
SAME_AS = [
    'https://www.instagram.com/bilalrahatstudio/',
    'https://www.instagram.com/mozaikfilm/',
    'https://www.youtube.com/@mozaikfilm',
    'https://www.linkedin.com/in/bilalrahat',
]


def jsonld(L, page, desc):
    org = {
        '@type': 'Organization', '@id': BASE + '/#mozaik', 'name': 'Mozaik Film',
        'foundingDate': '2009', 'founder': {'@id': BASE + '/#bilal'},
        'url': BASE + '/', 'email': EMAIL,
        'sameAs': ['https://www.instagram.com/mozaikfilm/', 'https://www.youtube.com/@mozaikfilm'],
        'address': [
            {'@type': 'PostalAddress', 'addressLocality': 'Şanlıurfa', 'addressCountry': 'TR'},
            {'@type': 'PostalAddress', 'addressLocality': 'İstanbul', 'addressCountry': 'TR'},
        ],
    }
    person = {
        '@type': 'Person', '@id': BASE + '/#bilal', 'name': 'Bilal Rahat',
        'jobTitle': 'Film, CGI & AI Director', 'url': BASE + '/',
        'image': BASE + '/assets/bilal-rahat.jpg', 'email': EMAIL,
        'worksFor': {'@id': BASE + '/#mozaik'}, 'founder': {'@id': BASE + '/#mozaik'},
        'knowsLanguage': ['tr', 'en', 'ar'], 'sameAs': SAME_AS,
    }
    site = {'@type': 'WebSite', '@id': BASE + '/#site', 'url': BASE + '/', 'name': 'Bilal Rahat',
            'inLanguage': LANGS, 'publisher': {'@id': BASE + '/#bilal'}}
    webpage = {'@type': 'WebPage', 'url': BASE + url(L, page), 'inLanguage': L,
               'description': desc, 'isPartOf': {'@id': BASE + '/#site'}, 'about': {'@id': BASE + '/#bilal'}}
    graph = [person, org, site, webpage]
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    return '<script type="application/ld+json">' + data.replace('</', '<\\/') + '</script>\n'


def write_seo_files():
    open('robots.txt', 'w', encoding='utf-8').write(
        f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
    import datetime
    today = datetime.date.today().isoformat()
    rows = []
    for p in PAGES:
        for L in LANGS:
            alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{BASE}{url(l, p)}"/>' for l in LANGS)
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{url("en", p)}"/>'
            pr = '1.0' if p == 'home' else '0.8'
            rows.append(f'  <url>\n    <loc>{BASE}{url(L, p)}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{pr}</priority>{alts}\n  </url>')
    open('sitemap.xml', 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + '\n'.join(rows) + '\n</urlset>\n')


# ---------------------------------------------------------------------- page shell
def shell(L, page, title, desc, body, NAV, t, ext):
    import hashlib
    CSSV = hashlib.md5(open('assets/site.css', 'rb').read()).hexdigest()[:8]
    rtl = L == 'ar'
    hreflang = ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{url(l, page)}">\n' for l in LANGS)
    langnav = ''.join(f'<a href="{url(l, page)}" hreflang="{l}"{" class=on aria-current=page" if l == L else ""}>{l.upper()}</a>' for l in LANGS)
    links = ''.join(f'<a href="{url(L, p)}"{" class=on aria-current=page" if p == page else ""}>{NAV[p]}</a>' for p in PAGES if p != 'home')
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
<meta property="og:url" content="{BASE}{url(L, page)}">
<meta name="twitter:card" content="summary_large_image">
{hreflang}<link rel="alternate" hreflang="x-default" href="{BASE}{url('en', page)}">
<link rel="canonical" href="{BASE}{url(L, page)}">
<meta name="theme-color" content="#000000">
<meta name="robots" content="index, follow, max-image-preview:large">
{jsonld(L, page, desc)}<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23000'/%3E%3Ctext x='32' y='43' font-family='Georgia,serif' font-size='30' text-anchor='middle' fill='%23fff'%3EBR%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=Inter:wght@400;500;600&display=swap{'&family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Noto+Naskh+Arabic:wght@500;600' if rtl else ''}" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={CSSV}">
</head>
<body>

<header>
  <div class="wrap nav">
    <a class="brand" href="{url(L, 'home')}">Bilal Rahat</a>
    <nav class="links" aria-label="Main">{links}</nav>
    <nav class="langs" aria-label="Language">{langnav}</nav>
    <a class="box" href="#start">{t('Tell me about your project', 'Projenizi anlatın', 'حدّثني عن مشروعك')} {ext}</a>
    <details class="menu"><summary>{t('Menu', 'Menü', 'القائمة')}</summary><nav aria-label="Mobile">{links}<div class="langs-m">{langnav}</div></nav></details>
  </div>
</header>

<main>{body}
</main>

<footer>
  <div class="wrap">
    <span>© 2026 Bilal Rahat · {t('Director · Founder of Mozaik Film', 'Yönetmen · Mozaik Film Kurucusu', 'مخرج · مؤسس موزاييك فيلم')}</span>
    <span><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="https://www.instagram.com/bilalrahatstudio/">@bilalrahatstudio</a> · <a href="https://www.instagram.com/mozaikfilm/">@mozaikfilm</a> · <a href="https://www.linkedin.com/in/bilalrahat">LinkedIn</a></span>
    <span>{langnav.replace('class=on aria-current=page', 'aria-current=page')}</span>
  </div>
</footer>

<dialog class="lb" id="lb" aria-label="Video"><button type="button" class="x">{t('Close', 'Kapat', 'إغلاق')} ✕</button><div class="fr"></div></dialog>

<script>
{{
  const vids = document.querySelectorAll('video[data-src]');
  const io = new IntersectionObserver((es) => es.forEach(e => {{
    const v = e.target;
    if (e.isIntersecting) {{ if (!v.src) v.src = v.dataset.src; v.play().catch(() => {{}}); }}
    else v.pause();
  }}), {{ rootMargin: '200px' }});
  vids.forEach(v => io.observe(v));
  const chips = document.querySelectorAll('.chips button');
  chips.forEach(b => b.addEventListener('click', () => {{
    chips.forEach(c => c.setAttribute('aria-pressed', c === b));
    const f = b.dataset.f;
    document.querySelectorAll('#projs .proj').forEach(p => p.hidden = f !== 'all' && !p.dataset.d.split(' ').includes(f));
  }}));
  const lb = document.getElementById('lb'), fr = lb.querySelector('.fr');
  document.addEventListener('click', e => {{
    const b = e.target.closest('[data-yt]');
    if (!b) return;
    lb.classList.toggle('short', !!b.dataset.short);
    fr.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + b.dataset.yt + '?autoplay=1&rel=0" allow="autoplay; fullscreen; encrypted-media" allowfullscreen title="Video"></iframe>';
    lb.showModal();
  }});
  lb.addEventListener('close', () => fr.innerHTML = '');
  lb.addEventListener('click', e => {{ if (e.target === lb || e.target.closest('.x')) lb.close(); }});
  document.querySelectorAll('.menu nav a').forEach(a => a.addEventListener('click', () => a.closest('details').open = false));
}}
</script>
</body>
</html>
'''


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs('assets/work', exist_ok=True)
    n = 0
    for L in LANGS:
        for p in PAGES:
            out = url(L, p).lstrip('/') + 'index.html'
            os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
            open(out, 'w', encoding='utf-8').write(build(L, p))
            n += 1
    write_seo_files()
    print(f'ok: {n} pages + robots.txt + sitemap.xml')
