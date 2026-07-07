# M-Studio Beauty — statický web

Web masérského studia v Opavě — **[www.m-studiobeauty.cz](https://www.m-studiobeauty.cz)**.

Původně WordPress (šablona Astra + Spectra), zmigrováno na čistě statické stránky
kvůli levnějšímu provozu. Objednávky probíhají jen telefonicky / e-mailem,
rezervační systém (Amelia) byl záměrně vyřazen.

## Struktura repozitáře

| Cesta | Popis |
|---|---|
| `static-web/` | Hotový web k nasazení — 5 stránek, assets (CSS, fonty, obrázky), `.htaccess`, `robots.txt`, `sitemap.xml`, `404.html` |
| `build_site.py` | Generátor stránek — veškeré texty a struktura jsou přímo v něm |
| `CLAUDE.md` | Poznámky k projektu (naměřené hodnoty vzhledu, postup nasazení, nedodělky) |

Stránky: `/` (Domů), `/sluzby/`, `/ceniky/`, `/nase-provozovna/`, `/kontakt/`.

## Úprava obsahu

Texty se needitují v HTML, ale v `build_site.py`. Po úpravě:

```bash
python3 build_site.py        # přegeneruje static-web/*.html
```

Vzhled je 1:1 kopie původní šablony — barvy, fonty a rozměry jsou naměřené
z originálu a popsané v `CLAUDE.md`. Neměnit „od oka".

## Nasazení

### Klasický hosting (Wedos)

Nahrát **kompletní obsah** složky `static-web/` do web rootu — včetně složky
`assets/` a skrytého souboru `.htaccess`. Ověření: `/assets/css/style.css`
musí vracet 200.

`.htaccess` zajišťuje: přesměrování na https+www, 301 ze starých WordPress
adres (`/panel-zakaznika/`, `/panel-masera/`, staré cesty k obrázkům) a cache
hlavičky.

### GitHub Pages (zdarma)

Repozitář obsahuje workflow `.github/workflows/deploy-pages.yml`, který při
každém pushi do `main` nasadí obsah `static-web/` na GitHub Pages.

Jednorázová aktivace: na GitHubu **Settings → Pages → Source: GitHub Actions**.
Web pak běží na `https://nofak.github.io/m-studiobeauty/`.

Pro provoz na vlastní doméně (www.m-studiobeauty.cz přes GitHub Pages):

1. Settings → Pages → Custom domain → vyplnit `www.m-studiobeauty.cz`
2. U registrátora domény nastavit CNAME záznam `www` → `nofak.github.io`
3. Ve workflow nastavit `BASE_PATH: ""` (přepis cest je pak zbytečný)

Pozn.: GitHub Pages neumí `.htaccess` — vynucené HTTPS řeší Pages samo,
staré WordPress adresy vrátí 404 (řeší je vlastní `404.html`).
