# Diş hekimi web sitesi kampanyası — kit

Mozaik Film'in web sitesi olmayan diş hekimlerine örnek tasarım gönderdiği kampanyanın araçları.
Örnek sayfalar `https://bilalrahat.com.tr/ornek/` altında yayında (GitHub Pages, bu repo).

## Akış
1. Google Haritalar'da bölgedeki diş hekimlerini tara; **web sitesi olmayanları** al (sponsorlu sonuçları atla).
   Puan sınırı yok. Cep numarası (05xx) olanlar WhatsApp kanalı; yoksa Instagram hesabını Google'da ara.
2. `hekimler.json` hazırla (şema aşağıda), sonra repo kökünden:
   `python3 tools/dis-kampanya/uret.py hekimler.json /tmp/panel`
3. `ornek/` değişikliklerini commit + push et (GitHub Pages ~1 dk'da yayına alır). `tools/` dışında başka dosyaya dokunma.
4. `/tmp/panel` klasörünü (index.html, data.js, img/) özel bir Claude artifact'ı olarak yayınla: "Diş Hekimi Gönderim Paneli – <bölge>".
5. Canlı linki kontrol et (ör. `https://bilalrahat.com.tr/ornek/<slug>/` og:title göstermeli).

## hekimler.json şeması
```json
[{
 "key": "h-ad-soyad",               // h- + slug, mevcut anahtarlarla çakışmasın (ornek/clinics.js'e bak)
 "name": "Dt. Ad Soyad",
 "district": "Maltepe",
 "address": "Mahalle, Cadde No, İlçe",
 "h1": "Pzt–Cum 09:00–19:00", "h2": "Cmt 10:00–16:00",
 "phone": "0532 000 00 00",
 "theme": "turkuaz",                 // turkuaz | mavi | lacivert | su | gok | petrol (sırayla dağıt)
 "foto": "klinik",                   // klinik | firca (dönüşümlü)
 "headline": "Muayene, tedavi ve kontrolleriniz için.",
 "domain": "dradsoyad.com.tr",       // önerilen alan adı (örnek)
 "hitap": "Ad Bey",                  // "Ad Bey" / "Ad Hanım"; iki hekimde "Ahmet Bey, Nuray Hanım"
 "open": "Maltepe'deki muayenehanenizi Google Haritalar'da gördüm; bağlı bir web siteniz görünmüyor.",
 "kind": "Muayenehane",              // Muayenehane | İki hekim | Poliklinik
 "wa": "905320000000",               // cep varsa; yoksa ""
 "ig": "kullaniciadi",               // WhatsApp yoksa; emin değilsen igCheck:true
 "igCheck": false,
 "email": "",                        // varsa
 "note": ""                          // panelde kırmızı uyarı (kapanmış olabilir vb.)
}]
```

## Mesaj kuralları
- Açılış cümlesi (`open`): puanı **4,8 ve üzeri ve 30+ değerlendirme** varsa "…X değerlendirmeyle Y puanınız var ama bağlı bir web siteniz görünmüyor." Diğerlerinde **puan anma**: "…Google Haritalar'da gördüm; bağlı bir web siteniz görünmüyor."
- WhatsApp metni ve Instagram kısa metni (≤1000 karakter) panelde otomatik kurulur; fiyatlar, 26 Aralık kampanya cümlesi, sosyal medya cümlesi, @mozaikfilm linki panel şablonunda.
- Göndermeyi Bilal kendisi yapar; günde 10–15 mesajı geçme.

## Mevzuat (Resmî Gazete 12.11.2025, sayı 33075)
Hekimin sitesinde fiyat, kampanya, hasta yorumu, önce-sonra, sertifikaya dayalı uzmanlık unvanı yok. Son güncelleme tarihi ve site sorumlusu bilgisi zorunlu. Kişisel görseldeki fiyatlar Mozaik'in hekime teklifidir, hekimin sitesinde yer almaz.
