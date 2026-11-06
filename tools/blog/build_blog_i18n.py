import re, sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import en_posts, de_posts, es_posts, fr_posts

SITE = sys.argv[1]
B = "https://livingstays.vercel.app"

# Italian originals: slug, image, minutes (order = blog order)
IT = [("cin-cir-affitti-brevi-sicilia", "/img/p/pantano-2.webp", 6),
      ("tasse-affitti-brevi-2026-cedolare-secca", "/img/p/kleos-3.webp", 5),
      ("quanto-si-guadagna-affitto-breve-catania", "/img/p/pantano-1.webp", 6),
      ("cosa-fa-un-co-host-quanto-costa", "/img/p/villa-2.webp", 5),
      ("airbnb-o-booking-dove-pubblicare", "/img/p/kleos-1.webp", 5)]

EN = {p["it"]: dict(slug=p["en"], title=p["title"], desc=p["desc"], body=p["body"]) for p in en_posts.POSTS}

L = {
 "en": dict(posts=EN, contact=("/en/contact/", "Contact"), owners="/en/owners/", explore="Explore", date="5 November 2026",
   readnext="Read next", allart="All articles", gtitle="Owner guides",
   glede="Rules, taxes, earnings and management: everything you need to know to rent short-term in Sicily, explained clearly.",
   gdesc="Practical guides for owners renting short-term in Sicily: CIN and CIR, taxes, earnings, co-hosting, Airbnb and Booking.com.",
   cta=("Own a property in Sicily?", "We’ll give you a free estimate of its rental potential and explain how we would manage it, with no obligation.", "Request a free valuation",
        "Hi, I read your blog and would like a valuation for my property")),
 "de": dict(posts=de_posts.POSTS, contact=("/de/kontakt/", "Kontakt"), owners="/de/eigentuemer/", explore="Entdecken", date="5. November 2026",
   readnext="Weiterlesen", allart="Alle Artikel", gtitle="Ratgeber für Eigentümer",
   glede="Vorschriften, Steuern, Einnahmen und Verwaltung: alles, was Sie für die Kurzzeitvermietung in Sizilien wissen müssen, klar erklärt.",
   gdesc="Praxisratgeber für Eigentümer mit Kurzzeitvermietung in Sizilien: CIN und CIR, Steuern, Einnahmen, Co-Hosting, Airbnb und Booking.com.",
   cta=("Sie besitzen eine Immobilie in Sizilien?", "Wir schätzen kostenlos das Vermietungspotenzial und erklären Ihnen, wie wir sie verwalten würden – unverbindlich.", "Kostenlose Bewertung anfragen",
        "Hallo, ich habe Ihren Blog gelesen und möchte eine Bewertung meiner Immobilie")),
 "es": dict(posts=es_posts.POSTS, contact=("/es/contacto/", "Contacto"), owners="/es/propietarios/", explore="Explorar", date="5 de noviembre de 2026",
   readnext="Sigue leyendo", allart="Todos los artículos", gtitle="Guías para propietarios",
   glede="Normativa, impuestos, ingresos y gestión: todo lo que necesitas saber para alquilar a corto plazo en Sicilia, explicado con claridad.",
   gdesc="Guías prácticas para propietarios con alquiler vacacional en Sicilia: CIN y CIR, impuestos, ingresos, co-hosting, Airbnb y Booking.com.",
   cta=("¿Tienes un inmueble en Sicilia?", "Te damos una estimación gratuita de su potencial de alquiler y te explicamos cómo lo gestionaríamos, sin compromiso.", "Solicita una valoración gratuita",
        "Hola, he leído vuestro blog y quiero una valoración de mi inmueble")),
 "fr": dict(posts=fr_posts.POSTS, contact=("/fr/contact/", "Contact"), owners="/fr/proprietaires/", explore="Explorer", date="5 novembre 2026",
   readnext="À lire aussi", allart="Tous les articles", gtitle="Guides pour propriétaires",
   glede="Règles, impôts, revenus et gestion : tout ce qu’il faut savoir pour louer en courte durée en Sicile, expliqué clairement.",
   gdesc="Guides pratiques pour les propriétaires en location courte durée en Sicile : CIN et CIR, impôts, revenus, co-hosting, Airbnb et Booking.com.",
   cta=("Vous possédez un bien en Sicile ?", "Nous estimons gratuitement son potentiel locatif et vous expliquons comment nous le gérerions, sans engagement.", "Demander une estimation gratuite",
        "Bonjour, j’ai lu votre blog et je souhaite une estimation de mon bien")),
}
ORDER = ["it", "en", "es", "fr", "de"]
NAMES = {"it": "Italiano", "en": "English", "es": "Español", "fr": "Français", "de": "Deutsch"}

def rd(p): return open(os.path.join(SITE, p), encoding="utf-8").read()
def wr(p, s):
    p = os.path.join(SITE, p); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)

def urls_for(it_slug):
    """lang -> URL path of this article (it_slug None = blog index)."""
    if it_slug is None:
        return {"it": "/blog/", **{l: f"/{l}/blog/" for l in L}}
    return {"it": f"/blog/{it_slug}/", **{l: f'/{l}/blog/{L[l]["posts"][it_slug]["slug"]}/' for l in L}}

def alternates(u):
    s = f'<link rel="canonical" href="{B}{{cur}}">'
    s += ''.join(f'<link rel="alternate" hreflang="{l}" href="{B}{u[l]}">' for l in ORDER)
    return s + f'<link rel="alternate" hreflang="x-default" href="{B}{u["it"]}">'

def switcher(u, cur):
    return ''.join(f'<a href="{u[l]}" hreflang="{l}" lang="{l}"' + (' class="on"' if l == cur else '') + f'>{NAMES[l]}</a>' for l in ORDER)

def footer_langs(u):
    return ''.join(f'<a href="{u[l]}" lang="{l}">{NAMES[l]}</a>' for l in ORDER)

def set_langs(html, u, cur):
    html = re.sub(r'(<details class="lang"><summary>[^<]*</summary><div>).*?(</div></details>)', lambda m: m.group(1) + switcher(u, cur) + m.group(2), html, count=1, flags=re.S)
    html = re.sub(r'(<h4 style="margin-top:20px">[^<]*</h4>).*?(</div></div><small>)', lambda m: m.group(1) + footer_langs(u) + m.group(2), html, count=1, flags=re.S)
    return html

def set_alternates(html, u, cur_url):
    headpart, rest = html.split('</head>', 1)
    headpart = re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>', '', headpart)
    headpart = headpart.replace('<meta property="og:title"', alternates(u).replace('{cur}', cur_url) + '<meta property="og:title"', 1)
    return headpart + '</head>' + rest

def add_blog_link(html, lang, on=False):
    path, label = L[lang]["contact"]; blog = f"/{lang}/blog/"
    cls = ' class="on"' if on else ''
    for c in ('', ' class="on"'):
        a = f'<a href="{path}"{c}>{label}</a>'
        html = html.replace(a + '<details', a + f'<a href="{blog}"{cls}>Blog</a><details', 1)
    ex = re.escape(L[lang]["explore"]); pa = re.escape(f'<a href="{path}">{label}</a>')
    html = re.sub(rf'(<h4>{ex}</h4>.*?{pa})(?!<a href="{blog}">)', rf'\1<a href="{blog}">Blog</a>', html, count=1, flags=re.S)
    return html

def card(lang, it_slug, img, mins):
    p = L[lang]["posts"][it_slug]
    return (f'<a class="bcard rv" href="/{lang}/blog/{p["slug"]}/"><div class="im"><img src="{img}" alt="{p["title"]}" loading="lazy" decoding="async"></div>'
            f'<div class="bd"><span class="k">{L[lang]["date"]} · {mins} min</span><h3>{p["title"]}</h3><p>{p["desc"]}</p></div></a>')

def chrome(lang, u):
    owners = rd(L[lang]["owners"].strip("/") + "/index.html")
    hdr = re.search(r'<header class="hd">.*?</header>', owners, re.S).group(0)
    ftr = re.search(r'<footer class="ft">.*?</footer>', owners, re.S).group(0)
    hdr = add_blog_link(re.sub(r' class="on"', '', hdr), lang, on=True)
    hdr = hdr.replace(f'<a href="/{lang}/blog/">Blog</a><details', f'<a href="/{lang}/blog/" class="on">Blog</a><details')
    ftr = add_blog_link(ftr, lang)
    return set_langs(hdr, u, lang), set_langs(ftr, u, lang)

def page(tpl, lang, title, desc, u, cur_url, img, og_type, main, ld=None):
    s = tpl.replace('<html lang="it">', f'<html lang="{lang}">')
    s = re.sub(r'<title>.*?</title>.*?(<link rel="icon")', lambda m:
        f'<title>{title} — Living Stays</title><meta name="description" content="{desc}">'
        f'<meta property="og:title" content="{title} — Living Stays"><meta property="og:description" content="{desc}">'
        f'<meta property="og:image" content="{B}{img}"><meta property="og:type" content="{og_type}">'
        + (f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else '') + m.group(1), s, count=1, flags=re.S)
    s = set_alternates(s, u, cur_url)
    hdr, ftr = chrome(lang, u)
    return re.sub(r'<header class="hd">.*</footer>', lambda m: hdr + main + ftr, s, count=1, flags=re.S)

new_urls = []
for lang, c in L.items():
    for i, (it_slug, img, mins) in enumerate(IT):
        p = c["posts"][it_slug]; u = urls_for(it_slug); cur = u[lang]
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
              "datePublished": "2026-11-05", "dateModified": "2026-11-06", "image": B + img, "inLanguage": lang,
              "author": {"@type": "Organization", "name": "Living Stays"},
              "publisher": {"@type": "Organization", "name": "Living Stays", "logo": {"@type": "ImageObject", "url": B + "/img/lion.png"}},
              "mainEntityOfPage": B + cur}
        h3, ptxt, btn, wa = c["cta"]
        cta = (f'<div class="cta"><h3>{h3}</h3><p>{ptxt}</p><div class="row"><a class="btn" href="{c["owners"]}#form">{btn} <span aria-hidden="true">→</span></a>'
               f'<a class="btn o" href="https://wa.me/393928896029?text={__import__("urllib.parse").parse.quote(wa)}">WhatsApp</a></div></div>')
        others = [x for x in IT if x[0] != it_slug][:3]
        main = (f'<main><article class="post"><header class="ph"><div class="w"><a class="eb" href="/{lang}/blog/" style="justify-content:center">Blog · {c["date"]} · {mins} min</a>'
                f'<h1>{p["title"]}</h1></div></header><div class="w pw"><div class="pimg"><img src="{img}" alt="{p["title"]}" decoding="async"></div>'
                f'<div class="pbody">{p["body"]}{cta}</div></div></article>'
                f'<section class="sec alt"><div class="w"><h2 class="st c">{c["readnext"]}</h2><div class="bgrid">{"".join(card(lang, *x) for x in others)}</div></div></section></main>')
        wr(cur.strip("/") + "/index.html", page(rd(f"blog/{it_slug}/index.html"), lang, p["title"], p["desc"], u, cur, img, "article", main, ld))
        new_urls.append(cur)
    # blog index
    u = urls_for(None)
    main = (f'<main><section class="ph"><div class="w"><span class="eb">Blog</span><h1>{c["gtitle"]}</h1><p class="lede">{c["glede"]}</p></div></section>'
            f'<section class="sec" style="padding-top:20px"><div class="w"><div class="bgrid">{"".join(card(lang, *x) for x in IT)}</div></div></section></main>')
    wr(f"{lang}/blog/index.html", page(rd("blog/index.html"), lang, c["gtitle"], c["gdesc"], u, u[lang], "/img/p/kleos-1.webp", "website", main))
    new_urls.append(u[lang])
    # existing pages of this language: Blog link; owners page: guides section
    for root, _, files in os.walk(os.path.join(SITE, lang)):
        if os.path.join(SITE, lang, "blog") in root: continue
        for fn in files:
            if fn != "index.html": continue
            rel = os.path.relpath(os.path.join(root, fn), SITE)
            s = add_blog_link(rd(rel), lang)
            if "/" + rel.replace(os.sep, "/").rsplit("index.html", 1)[0] == c["owners"] and f'href="/{lang}/blog/" style' not in s and 'class="btn o" href="/' + lang + '/blog/"' not in s:
                sec = (f'<section class="sec alt"><div class="w"><div class="c rv"><span class="eb">Blog</span><h2 class="st">{c["gtitle"]}</h2></div>'
                       f'<div class="bgrid">{"".join(card(lang, *x) for x in IT[:3])}</div><div class="c" style="margin-top:36px">'
                       f'<a class="btn o" href="/{lang}/blog/">{c["allart"]} <span aria-hidden="true">→</span></a></div></div></section>')
                s = s.replace('</main>', sec + '</main>', 1)
            wr(rel, s)

# Italian blog pages: full alternates + switchers
for it_slug in [None] + [x[0] for x in IT]:
    u = urls_for(it_slug); rel = u["it"].strip("/") + "/index.html"
    wr(rel, set_langs(set_alternates(rd(rel), u, u["it"]), u, "it"))

sm = rd("sitemap.xml")
add = ''.join(f'<url><loc>{B}{x}</loc></url>' for x in new_urls if f'{B}{x}<' not in sm)
wr("sitemap.xml", sm.replace('</urlset>', add + '</urlset>'))
print("pagine:", len(new_urls))
