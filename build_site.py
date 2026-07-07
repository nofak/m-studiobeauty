# Generátor čistých statických stránek M-Studio Beauty (vzhled 1:1 podle původního webu)
import pathlib

OUT = pathlib.Path(__file__).parent / "static-web"
BASE = "https://www.m-studiobeauty.cz"
GA_ID = "G-QL9HWX0Z2L"

# CSS je malé (~9 kB / ~2,7 kB gzip) → vkládáme ho inline do <head>,
# aby nevznikal render-blokující požadavek navíc (doporučení PageSpeed).
# Zdrojem zůstává assets/css/style.css – upravuj tam, build ho vloží.
CSS = (OUT / "assets" / "css" / "style.css").read_text(encoding="utf-8")

NAV = [
    ("/", "Domů"),
    ("/sluzby/", "Naše služby"),
    ("/nase-provozovna/", "Naše provozovna"),
    ("/ceniky/", "Ceníky"),
    ("/kontakt/", "Kontakt"),
]

JSONLD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BeautySalon",
  "name": "M-Studio Beauty",
  "description": "Masérské studio v Opavě – lymfatické masáže VacuPress, maderoterapie, masáže zad a šíje.",
  "url": "https://www.m-studiobeauty.cz/",
  "email": "info@m-studiobeauty.cz",
  "telephone": "+420721381939",
  "image": "https://www.m-studiobeauty.cz/assets/img/og-image.jpg",
  "logo": "https://www.m-studiobeauty.cz/assets/img/logo-262.png",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rolnická 1538/38, Kateřinky",
    "addressLocality": "Opava",
    "postalCode": "747 05",
    "addressCountry": "CZ"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 49.9468646,
    "longitude": 17.9096427
  },
  "sameAs": ["https://www.facebook.com/mstudiobeauty.cz"],
  "employee": [
    {"@type": "Person", "name": "Markéta Cojocaru", "telephone": "+420722612252"},
    {"@type": "Person", "name": "Michaela Nováková", "telephone": "+420721381939"}
  ]
}
</script>"""

COOKIES_GA = """<div class="cookie-banner" id="cookie-banner" role="dialog" aria-label="Souhlas s cookies">
<p>Používáme soubory cookies k měření návštěvnosti (Google Analytics). Souhlasíte s jejich použitím?</p>
<div class="tlacitka">
<button type="button" class="prijmout" onclick="cookieVolba(true)">Přijmout</button>
<button type="button" class="odmitnout" onclick="cookieVolba(false)">Odmítnout</button>
</div>
</div>
<script>
function nactiGA(){
  var s=document.createElement('script');s.async=true;
  s.src='https://www.googletagmanager.com/gtag/js?id=%GA%';
  document.head.appendChild(s);
  window.dataLayer=window.dataLayer||[];
  function gtag(){dataLayer.push(arguments);}
  window.gtag=gtag;gtag('js',new Date());gtag('config','%GA%',{anonymize_ip:true});
}
function cookieVolba(souhlas){
  localStorage.setItem('cookie-souhlas',souhlas?'ano':'ne');
  document.getElementById('cookie-banner').classList.remove('zobrazit');
  if(souhlas)nactiGA();
}
(function(){
  var v=localStorage.getItem('cookie-souhlas');
  if(v==='ano'){nactiGA();}
  else if(v===null){document.getElementById('cookie-banner').classList.add('zobrazit');}
})();
</script>""".replace("%GA%", GA_ID)

FB_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" aria-hidden="true"><path d="M504 256C504 119 393 8 256 8S8 119 8 256c0 123.78 90.69 226.38 209.25 245V327.69h-63V256h63v-54.64c0-62.15 37-96.48 93.67-96.48 27.14 0 55.52 4.84 55.52 4.84v61h-31.28c-30.8 0-40.41 19.12-40.41 38.73V256h68.78l-11 71.69h-57.78V501C413.31 482.38 504 379.78 504 256z"/></svg>"""
MAIL_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M0 3v18h24v-18h-24zm6.623 7.929l-4.623 5.712v-9.458l4.623 3.746zm-4.141-5.929h19.035l-9.517 7.713-9.518-7.713zm5.694 7.188l3.824 3.099 3.83-3.104 5.612 6.817h-18.779l5.513-6.812zm9.208-1.264l4.616-3.741v9.348l-4.616-5.607z"/></svg>"""
MENU_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 13h18c0.552 0 1-0.448 1-1s-0.448-1-1-1h-18c-0.552 0-1 0.448-1 1s0.448 1 1 1zM3 7h18c0.552 0 1-0.448 1-1s-0.448-1-1-1h-18c-0.552 0-1 0.448-1 1s0.448 1 1 1zM3 19h18c0.552 0 1-0.448 1-1s-0.448-1-1-1h-18c-0.552 0-1 0.448-1 1s0.448 1 1 1z"/></svg>"""


def picture(name, widths, sizes, alt, loading="lazy", ext="jpg", wh=None):
    src_webp = ", ".join(f"/assets/img/{name}-{w}.webp {w}w" for w in widths)
    src_img = ", ".join(f"/assets/img/{name}-{w}.{ext} {w}w" for w in widths)
    fallback = f"/assets/img/{name}-{widths[-1]}.{ext}"
    dims = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
    lazy = f' loading="{loading}"' if loading else ""
    return (f'<picture>'
            f'<source type="image/webp" srcset="{src_webp}" sizes="{sizes}">'
            f'<img src="{fallback}" srcset="{src_img}" sizes="{sizes}" alt="{alt}"{dims}{lazy} decoding="async">'
            f'</picture>')


def page(path, title, description, content, hero=True, hero_hide_mobile=False):
    url = BASE + path
    nav_items = "\n".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == path else ""}>{label}</a></li>'
        for href, label in NAV
    )
    hero_html = ""
    hero_preload = ""
    if hero:
        cls = "hero hero--skryt-mobil" if hero_hide_mobile else "hero"
        hero_html = f"""<div class="{cls}">
<picture>
<source type="image/webp" srcset="/assets/img/hero-800.webp 800w, /assets/img/hero-1200.webp 1200w" sizes="(max-width: 1200px) 100vw, 1200px">
<img src="/assets/img/hero-1200.jpg" srcset="/assets/img/hero-800.jpg 800w, /assets/img/hero-1200.jpg 1200w" sizes="(max-width: 1200px) 100vw, 1200px" alt="" width="1200" height="500" fetchpriority="high" decoding="async">
</picture>
</div>"""
        # Preload LCP obrázku (hero) – prohlížeč ho začne stahovat hned při parsování <head>.
        # Na Domů je hero pod 921 px skrytý → preload jen pro desktop (media), ať se na mobilu nestahuje.
        media = ' media="(min-width: 922px)"' if hero_hide_mobile else ""
        hero_preload = (
            '\n<link rel="preload" as="image" href="/assets/img/hero-1200.webp" '
            'imagesrcset="/assets/img/hero-800.webp 800w, /assets/img/hero-1200.webp 1200w" '
            'imagesizes="(max-width: 1200px) 100vw, 1200px" type="image/webp"' + media + ">"
        )

    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:locale" content="cs_CZ">
<meta property="og:type" content="website">
<meta property="og:site_name" content="M-Studio Beauty">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/karla-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/rubik-latin.woff2" as="font" type="font/woff2" crossorigin>{hero_preload}
<style>{CSS}</style>
{JSONLD}
</head>
<body>
<a class="skip-link" href="#obsah">Přeskočit na obsah</a>
<div class="site">
<header class="site-header">
<div class="header-inner">
<a class="logo" href="/" aria-label="M-Studio Beauty – úvodní stránka">
<img src="/assets/img/logo-131.png" srcset="/assets/img/logo-131.png 1x, /assets/img/logo-262.png 2x" alt="M-Studio Beauty" width="131" height="147">
</a>
<input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">
<label for="nav-toggle" class="nav-toggle-label" aria-label="Otevřít menu">{MENU_SVG}</label>
<nav class="site-nav" aria-label="Hlavní navigace">
<ul>
{nav_items}
<li class="polozka-btn"><a class="btn" href="/sluzby/">Rezervovat</a></li>
</ul>
</nav>
</div>
</header>
{hero_html}
<main id="obsah">
{content}
</main>
<footer class="site-footer">
<div class="footer-social">
<a href="https://www.facebook.com/mstudiobeauty.cz" aria-label="Facebook M-Studio Beauty">{FB_SVG}</a>
<a href="mailto:info@m-studiobeauty.cz" aria-label="Napsat e-mail">{MAIL_SVG}</a>
</div>
<p>Copyright &copy; 2026 M-Studio Beauty</p>
<div></div>
</footer>
</div>
{COOKIES_GA}
</body>
</html>
"""


# ---------- Domů ----------
home_content = f"""<section class="sekce-sluzby">
<h1 class="nadpis">Naše nabídka služeb</h1>
<p class="uvod">Objednejte si relaxaci a omlazení prostřednictvím kvalitních masáží poskytovaných naším masérským studiem.</p>
<div class="sloupce">
<div class="sloupec">
{picture("vacupress", [380, 760], "(max-width: 921px) 100vw, 347px", "Lymfatická masáž přístrojem VacuPress", wh=(380, 426))}
<h2>Vacupress lymfatická masáž podtlakem</h2>
<p>Mechanicky oddělí tukové buňky ze shluků tak, aby se jejich přirozený metabolismus vrátil do normálu a zároveň výrazně zpevní podkožní vazivo. Vhodným ošetřením se dosáhne detoxikace organismu, velmi pevné, pružné a hladké pokožky a zmenšení objemu na ošetřovaných místech. Dochází k prokrvení pokožky, kůže je pak hladká, hebká, pevná a pružná. Propínají se svaly břišní stěny a vnitřní strany stehen. Odstraňují se bolestivé spasmy páteře, zvyšuje se látková výměna, kloubní pohyblivost.</p>
</div>
<div class="sloupec">
{picture("maderoterapie", [380, 760], "(max-width: 921px) 100vw, 347px", "Dřevěné nástroje pro maderoterapii", wh=(380, 426))}
<h2>Maderoterapie</h2>
<p>Je moderní masážní technika, která využívá dřevěné anatomicky tvarované nástroje k odbourávání celulitidy, dochází k podpoře lymfatického systému a tvarování postavy. Opakovanými masážními pohyby dojde k odplavení tuku, toxinů a přebytečných tekutin, zároveň se vám prokrví svaly i pokožka a pomerančová kůže mizí.</p>
</div>
<div class="sloupec">
{picture("masaz-zad", [380, 760], "(max-width: 921px) 100vw, 347px", "Masáž zad a šíje", wh=(380, 426))}
<h2>Masáž zad a šíje</h2>
<p>Snižuje bolest a napětí v oblastech hlubokého napětí, jako jsou záda, krk a ramena. Zabraňte rozvoji bolestí hlavy a migrény. Zlepšená cirkulace krve a odtok lymfy z horní části těla. Skvělý způsob, jak se zbavit stresu a zlepšit pocit pohody.</p>
</div>
</div>
</section>
"""

# ---------- Služby ----------
sluzby_content = """<div class="obsah-sluzby">
<h1 class="sr-only">Naše služby</h1>
<p>Pro objednání nás prosím kontaktujte telefonicky a nebo emailem.</p>
<p>Děkujeme</p>
</div>
"""

# ---------- Ceníky ----------
ceniky_content = f"""<div class="obsah-ceniky">
<h1 class="sr-only">Ceníky</h1>
<div class="ceniky-grid">
<figure>
{picture("cenik-procedur", [600, 848], "(max-width: 921px) 100vw, 588px", "Ceník procedur M-Studio Beauty", wh=(848, 1200))}
</figure>
<figure>
{picture("cenik-permanentky", [600, 848], "(max-width: 921px) 100vw, 588px", "Ceník permanentek M-Studio Beauty", wh=(848, 1200))}
</figure>
</div>
</div>
"""

# ---------- Naše provozovna ----------
prov_content = f"""<div class="obsah-provozovna">
<h1 class="sr-only">Naše provozovna</h1>
<div class="galerie">
<figure class="orez">
{picture("salon1", [600], "(max-width: 921px) 100vw, 357px", "Masérské lehátko s dřevěnými nástroji na maderoterapii", wh=(600, 940))}
</figure>
<figure class="orez">
{picture("salon4", [1000], "(max-width: 921px) 100vw, 357px", "Masérské lehátko v M-Studio Beauty", wh=(1000, 600))}
</figure>
<figure class="orez">
{picture("salon3", [600], "(max-width: 921px) 100vw, 357px", "Interiér masérského studia M-Studio Beauty", wh=(600, 1008))}
</figure>
<figure class="cela">
{picture("salon2", [600, 850], "(max-width: 1200px) 100vw, 1120px", "Odpočinkový koutek s křesly a logem M-Studio Beauty", wh=(850, 1200))}
</figure>
</div>
</div>
"""

# ---------- Kontakt ----------
kontakt_content = """<div class="obsah-kontakt">
<h1 class="sr-only">Kontakt</h1>
<div class="kontakt-grid">
<div>
<h2>Provozovna</h2>
<p>Rolnická 1538/38, Kateřinky 747 05, Opava 5</p>
<h2>Markéta Cojocaru</h2>
<p>IČO: 08822077<br>Tel.: <a class="tel" href="tel:+420722612252">722 612 252</a></p>
<h2>Michaela Nováková</h2>
<p>IČO: 87373980<br>Tel.: <a class="tel" href="tel:+420721381939">721 381 939</a></p>
<h2>Email</h2>
<p><a href="mailto:info@m-studiobeauty.cz">info@m-studiobeauty.cz</a></p>
<p>Facebook <a href="https://www.facebook.com/mstudiobeauty.cz">https://www.facebook.com/mstudiobeauty.cz</a></p>
</div>
<div class="mapa">
<iframe src="https://frame.mapy.cz/zakladni?x=17.9096427142&amp;y=49.9468646462&amp;z=17&amp;source=firm&amp;id=13624673&amp;widgetFirmy=13624673" title="Mapa – M-Studio Beauty, Rolnická 1538/38, Opava" loading="lazy" allowfullscreen></iframe>
</div>
</div>
</div>
"""

pages = [
    ("index.html", "/", "Luxusní masáže v M-Studio Beauty v Opavě",
     "Luxusní masáže v M-Studio Beauty. Podpořte svou krásu a zdraví rozmanitými masážemi v Opavě. Zažijte relaxaci a omlazení díky lymfatické masáže VacuPressem.",
     home_content, dict(hero=True, hero_hide_mobile=True)),
    ("sluzby/index.html", "/sluzby/", "Služby - M-Studio Beauty",
     "Prohlédněte si naše služby s přístrojem VacuPress, ceník a rovnou se můžete objednat na termín.",
     sluzby_content, dict(hero=True)),
    ("ceniky/index.html", "/ceniky/", "Ceníky - M-Studio Beauty",
     "Aktuální ceník masáží a procedur v M-Studio Beauty Opava – VacuPress, maderoterapie, masáž zad a šíje i cenově zvýhodněné permanentky.",
     ceniky_content, dict(hero=False)),
    ("nase-provozovna/index.html", "/nase-provozovna/", "Naše provozovna - M-Studio Beauty",
     "Prohlédněte si prostory našeho masérského studia v Opavě-Kateřinkách na adrese Rolnická 1538/38. Příjemné prostředí pro vaši relaxaci.",
     prov_content, dict(hero=True)),
    ("kontakt/index.html", "/kontakt/", "Kontakt - M-Studio Beauty",
     "Kontaktujte nás: +420 721 381 939 Míša, +420 722 612 252 Markéta nebo Email: info@m-studiobeauty.cz",
     kontakt_content, dict(hero=True)),
]

for fname, path, title, desc, content, opts in pages:
    f = OUT / fname
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(page(path, title, desc, content, **opts), encoding="utf-8")
    print("OK", fname)
