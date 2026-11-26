"""Diş hekimi kampanyası üretici.

Kullanım (repo kökünden):
    python3 tools/dis-kampanya/uret.py hekimler.json PANEL_KLASORU

hekimler.json: hekim listesi (şema README.md'de). Script:
  1. Her hekim için 1080x1350 kişisel görsel üretir (PANEL_KLASORU/img/<key>.png)
  2. ornek/g/<slug>.jpg  (WhatsApp link önizlemesi, 1200x628)
  3. ornek/<slug>/index.html (og etiketli yönlendirme sayfası)
  4. ornek/clinics.js içine hekimleri ekler/günceller (kişisel görünüm #h-<slug>)
  5. PANEL_KLASORU/data.js ve panel index.html'i hazırlar
Gerekenler: google-chrome, python3-pillow.
"""
import json, os, re, sys, html, shutil, subprocess
from PIL import Image

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(KIT, '..', '..'))
ORNEK = os.path.join(REPO, 'ornek')
BASE = 'https://bilalrahat.com.tr/ornek/'

T = {
 'turkuaz': dict(main='#0E8C96', mid='#14B8C4', light='#E3F6F7', soft='#F2FAFB', border='#CDEDEF'),
 'mavi': dict(main='#1D5FC4', mid='#3B82F6', light='#E6EFFD', soft='#F3F7FE', border='#CFE0FA'),
 'lacivert': dict(main='#133B6B', mid='#2E6DB4', light='#E7EEF7', soft='#F4F7FB', border='#D3DFEE'),
 'su': dict(main='#0A7383', mid='#22C3D6', light='#DFF7FA', soft='#F1FBFC', border='#C6EEF3'),
 'gok': dict(main='#156A9C', mid='#38A8E0', light='#E2F2FB', soft='#F2F9FD', border='#CBE6F5'),
 'petrol': dict(main='#0F5F73', mid='#1597A8', light='#E1F1F3', soft='#F1F8F9', border='#C9E4E8'),
}

def up(s):
    return s.replace('i', 'İ').replace('ı', 'I').upper()

def main(src, panel):
    H = json.load(open(src, encoding='utf-8'))
    body = open(os.path.join(KIT, 'sablon', 'KlinikOnizleme.html'), encoding='utf-8').read()
    os.makedirs(os.path.join(panel, 'img'), exist_ok=True)
    os.makedirs(os.path.join(ORNEK, 'g'), exist_ok=True)
    tmp = os.path.join(KIT, 'sablon')
    for c in H:
        key = c['key']; slug = key[2:]
        t = T.get(c.get('theme'), T['turkuaz'])
        firca = c.get('foto') == 'firca'
        v = {'name': c['name'], 'districtCaps': up(c['district']), 'cityCaps': up(c.get('city') or 'İstanbul'), 'address': c['address'],
             'hours1': c['h1'], 'hours2': c.get('h2', ''), 'phone': c.get('phone') or 'Ara',
             'headline': c.get('headline') or 'Muayene, tedavi ve kontrolleriniz için.',
             'domain': c.get('domain') or slug.replace('-', '') + '.com.tr'}
        v = {k: html.escape(x, quote=True) for k, x in v.items()}
        v['photo'] = 'firca.jpg' if firca else 'klinik.jpg'
        v['photo2'] = 'klinik.jpg' if firca else 'firca.jpg'
        for k, col in t.items():
            v['t.' + k] = col
        b = re.sub(r'\{\{([\w.]+)\}\}', lambda m: v[m.group(1)], body)
        doc = f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><link rel="stylesheet" href="jakarta.css"><style>body{{margin:0}}</style></head><body>{b}</body></html>'
        hp = os.path.join(tmp, '_r.html'); open(hp, 'w', encoding='utf-8').write(doc)
        png = os.path.join(panel, 'img', key + '.png')
        subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1080,1350', '--virtual-time-budget=3000', '--screenshot=' + png, 'file://' + hp], capture_output=True)
        im = Image.open(png).convert('RGB')
        im.crop((0, 40, 1080, 605)).resize((1200, 628), Image.LANCZOS).save(os.path.join(ORNEK, 'g', slug + '.jpg'), quality=84, optimize=True)
        name = html.escape(c['name'])
        os.makedirs(os.path.join(ORNEK, slug), exist_ok=True)
        open(os.path.join(ORNEK, slug, 'index.html'), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>{name} · Örnek web tasarımı</title>
<meta property="og:type" content="website"><meta property="og:site_name" content="Mozaik Film">
<meta property="og:title" content="{name} için örnek web tasarımı">
<meta property="og:description" content="Size özel hazırladığımız tasarımı ve gezilebilir örnek siteyi görüntüleyin.">
<meta property="og:url" content="{BASE}{slug}/">
<meta property="og:image" content="{BASE}g/{slug}.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="628">
<meta name="twitter:card" content="summary_large_image">
<meta http-equiv="refresh" content="0;url=../#{key}">
<script>location.replace('../#{key}')</script>
</head><body><a href="../#{key}">Örnek tasarımı aç</a></body></html>''')
        print('ok', key)
    os.remove(os.path.join(tmp, '_r.html'))
    # ornek/clinics.js birleştir
    cj = os.path.join(ORNEK, 'clinics.js')
    s = open(cj, encoding='utf-8').read()
    cur = json.loads(s[s.index('['):s.rindex(']') + 1])
    idx = {c['key']: i for i, c in enumerate(cur)}
    for c in H:
        e = {k: c.get(k, '') for k in ('key', 'name', 'district', 'address', 'h1', 'h2', 'phone', 'theme', 'kind')}
        if c.get('city'): e['city'] = c['city']
        if c['key'] in idx: cur[idx[c['key']]] = e
        else: cur.append(e)
    open(cj, 'w', encoding='utf-8').write('window.CLINICS=' + json.dumps(cur, ensure_ascii=False) + ';\n')
    # panel
    P = []
    for c in H:
        d = {k: c.get(k, '') for k in ('key', 'name', 'district', 'phone', 'hitap', 'open', 'kind', 'wa', 'ig')}
        d['igCheck'] = bool(c.get('igCheck'))
        for k in ('email', 'note'):
            if c.get(k): d[k] = c[k]
        if c.get('phone') and not c.get('wa'):
            n = re.sub(r'\D', '', c['phone'])
            d['waTry'] = '90' + n[1:] if n.startswith('0') else n
        P.append(d)
    open(os.path.join(panel, 'data.js'), 'w', encoding='utf-8').write('window.D=' + json.dumps(P, ensure_ascii=False) + ';\n')
    shutil.copy(os.path.join(KIT, 'panel', 'index.html'), os.path.join(panel, 'index.html'))
    print('panel hazır:', panel, len(P), 'hekim')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
