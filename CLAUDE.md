# M-Studio Beauty – migrace webu na statické stránky

Web masérského studia v Opavě (www.m-studiobeauty.cz, hosting Wedos). Původně WordPress
(šablona Astra + Spectra, pluginy Amelia, CookieYes, MonsterInsights, AIOSEO), migruje se
na čistý statický web kvůli levnějšímu hostingu. Objednávky jen telefonicky/e-mailem —
rezervační systém Amelia byl **záměrně vyřazen** (potvrzeno majitelem 2026-07-06).

## Struktura projektu

- `static-web/` — **finální statický web** (nasazovaná verze). 5 stránek: `/`, `/sluzby/`,
  `/ceniky/`, `/nase-provozovna/`, `/kontakt/` + `assets/` (css, fonty, obrázky),
  `.htaccess`, `robots.txt`, `sitemap.xml`, `404.html`.
- `m-studiobeauty-static.zip` — archiv `static-web/` k nahrání na hosting.
- `m-studiobeauty-static-v1-wordpress-mirror.tar.gz` — **záloha původního webu**
  (wget mirror živého WordPressu vč. CSS/obrázků). Slouží jako reference vzhledu
  a pro případný návrat zpět.
- `build_site.py` — generátor stránek. Texty a struktura stránek jsou přímo v něm
  (česky, přehledně). Po úpravě spustit `python3 build_site.py` → přegeneruje
  `static-web/*.html`. Pak přebalit zip:
  `python3 -c "import shutil; shutil.make_archive('m-studiobeauty-static','zip','static-web')"`
- `www/` — stará kopie z hostingu; jen WP core + cache, **není kompletní**
  (chybí themes/plugins/uploads, obsah byl v DB). Nepoužívat jako zdroj.

## Vzhled = 1:1 kopie původní šablony (neměnit od oka!)

Naměřené hodnoty z originálu (Playwright/Chromium proti v1 mirroru):

- Boxový layout **1200 px** na gradientu `linear-gradient(156deg,#FDEEE4,#FBF1FB)`
- Růžová plocha hlavičky/patičky a podkladů: `#f9efef`; texty `#0F172A` / `#454F5E`
- Akcent oranžová `#FD9800`, hover `#E98C00`; tlačítko Rezervovat: **tmavý text**,
  radius 10 px, font 13 px, padding 18/28
- Fonty: Karla 400 (texty, menu 16 px), Rubik 500–600 (nadpisy 38/30 px) — lokální woff2
- Hero banner: pruh **211 px**, `object-fit:cover; object-position:49% 10%`;
  na Domů se pod 921 px **skrývá**; Ceníky a Provozovna hero **nemají** + mají růžové pozadí
- Kontakt: telefony vypadají jako běžný text (tel: odkazy s `color:inherit`)
- Mobil (≤921 px): oranžový hamburger 45×45, radius 4, bílá ikona

## Nástroje v tomto prostředí

- **Není** ImageMagick/PIL/pip → obrázky přes **ffmpeg** (umí i WebP: `-c:v libwebp`)
- Headless prohlížeč: `npm i playwright-core && npx playwright-core install chromium`
  (funguje, ~110 MB). Skripty ve scratchpadu session: `shot.js` (live web),
  `shot-local.js` (lokální složka přes interceptor), `probe.js` (computed styles)
- Lokální test: `python3 -m http.server` + curl

## Nasazení na hosting (Wedos)

1. Nahrát **kompletní obsah** `m-studiobeauty-static.zip` do web rootu — pozor na
   složku `assets/` a skrytý `.htaccess` (minule se nenahrály → web bez stylů!)
2. Ověřit: `https://www.m-studiobeauty.cz/assets/css/style.css` musí vrátit 200
3. `.htaccess` řeší: https+www redirect, 301 z `/panel-zakaznika/` a `/panel-masera/`
   na `/kontakt/`, 301 ze starých `/wp-content/uploads/...` obrázků, cache hlavičky

## Nedodělky / bezpečnost

- Na serveru smazat `info.php` (phpinfo) a zbytky WordPressu (`wp-content`, `wp-includes`)
- Po zrušení WP hostingu rotovat DB heslo (je v plaintextu ve `www/.../wp-config.php`)
- E-mail `info@m-studiobeauty.cz` musí zůstat funkční i po snížení tarifu
- Google Analytics `G-QL9HWX0Z2L` se načítá až po souhlasu v cookie liště
