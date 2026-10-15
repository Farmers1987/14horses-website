#!/usr/bin/env python3
"""Builds the 14horses site (EN at /, LT at /lt/) from one template.

Edit the TEXT dictionaries below and run:  python3 build/build.py
Anything wrapped in [[...]] is a placeholder still waiting for real content;
it is rendered with a dashed underline so it is easy to spot.
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "site"
SITE_URL = "https://14horses.com"

# Photos by G. Rozmanaite (14horses photo shoot), resized in site/assets/img
PHOTOS = {
    "hero_a": "/assets/img/hero-table.jpg",
    "hero_b": "/assets/img/hero-stone.jpg",
    "room":   "/assets/img/room-wide.jpg",
    "farm":   "/assets/img/farm-sheep.jpg",
    "g1":     "/assets/img/gallery-1.jpg",
    "g2":     "/assets/img/gallery-2.jpg",
    "g3":     "/assets/img/gallery-3.jpg",
    "g4":     "/assets/img/gallery-4.jpg",
}
PHOTO_CREDIT = "G. Rozmanaite"

# Official MICHELIN Bib Gourmand 2026 logo file (from the restaurant's Michelin award kit). Empty = placeholder.
BIB_LOGO = "/assets/michelin-2026.png"

CONTACT = {
    "email": "[[EMAIL]]",
    "phone": "[[PHONE]]",
    "instagram_handle": "@14horses_restaurant",
    "instagram_url": "https://www.instagram.com/14horses_restaurant/",
    "address": "Dominikonų g. 11, Vilnius",
    "maps": "https://maps.google.com/?q=Dominikon%C5%B3+g.+11,+Vilnius",
    # Link for "Visit Farmers Circle". Leave empty to hide the link.
    "farmers_circle_url": "",
}

EN = {
    "lang": "en", "home": "/", "other_home": "/lt/",
    "title": "14horses — Farm-to-table restaurant in Vilnius Old Town",
    "desc": "Farm-to-table restaurant in a restored historic mansion in Senatorių Pasažas, Vilnius. Seasonal four-step menu built on Lithuanian produce from our regenerative farm, Farmers Circle.",
    "skip": "Skip to content",
    "nav": ["About", "Menu", "Farmers Circle", "Events", "Policy", "Contact"],
    "reserve": "Reserve a table",
    "menu_open": "Open menu",
    "menu_btn": "Menu",
    "hero_over": "Senatorių Pasažas · Vilnius Old Town",
    "hero_h1": "Lithuanian produce, served at the pace of the seasons.",
    "hero_lead": "A farm-to-table kitchen in a restored historic mansion. Four courses, chosen freely, built on what our farm and our neighbours harvest this week.",
    "hero_menu": "See this season’s menu",
    "alt_hero_a": "A table set for dinner at 14horses",
    "alt_hero_b": "Old stone wall in Senatorių Pasažas",
    "strip": [("Dinner", "Tuesday – Saturday, 17:00&nbsp;–&nbsp;23:00"), ("Find us", "Dominikonų g. 11, Vilnius"), ("MICHELIN Guide 2026", "Bib Gourmand")],
    "about_over": "About us",
    "about_statement": "We sometimes call 14horses a travelling restaurant. This is our third home — and this time, we have reined in our horses and settled in Senatorių Pasažas for good.",
    "about_body": [
        "What has never changed is the thread: Lithuanian produce reaches the plate in the rhythm nature sets. Our own regenerative farm, Farmers Circle, and the farmers we work with all year keep us honest about the season.",
        "The whole dinner is packed into a four-step, fixed-price menu you choose freely — snacks, starter, main course and dessert — that shows the full picture of the 14horses philosophy, rooted in local cooking.",
    ],
    "menu_h2": "Four steps,<br>freely chosen.",
    "menu_intro": "One fixed price. You pick each course from a short, seasonal list. [[PRICE]] per guest · wine pairing [[PRICE]].",
    "steps": [("Step 1", "Snacks"), ("Step 2", "Starter"), ("Step 3", "Main course"), ("Step 4", "Dessert")],
    "dish": "[[Dishes from the chef]]",
    "menu_full": "Read the full menu",
    "farm_over": "Farmers Circle · 70 km from the table",
    "farm_h2": "Our farm sets the menu.",
    "farm_body": "Farmers Circle is our regenerative farm, just 70 km from Vilnius. Together with partner farms, it decides what arrives in the kitchen each week — and so what you eat tonight.",
    "farm_link": "Visit Farmers Circle",
    "alt_farm": "Lambs grazing at Farmers Circle, our regenerative farm",
    "farm_photo_todo": "Photo: Farmers Circle farm",
    "team_over": "Holding the reins",
    "team": [("[[Name]]", "Head chef"), ("[[Name]]", "Restaurant manager")],
    "gallery_label": "Gallery",
    "alt_gallery": ["Wine glasses by the window", "Tables by the wine wall", "A glass of wine on a set table", "A quiet corner of the dining room"],
    "alt_room": "The dining room at 14horses",
    "credit": "Photos",
    "events_h3": "Events &amp; private dining",
    "events_body": "Harvest dinners, guest chefs and the whole room for your own occasion.",
    "events_link": "Ask about events",
    "gift_h3": "Give an evening",
    "gift_body": "A gift voucher for 14horses in any amount from €20 to €1,000, bought online at Senatorių Pasažas.",
    "gift_link": "Buy a gift voucher",
    "res_h2": "Join us at the table.",
    "res_when": "Tuesday – Saturday from 17:00 · Dominikonų g. 11, Vilnius",
    "res_groups": 'Groups of 8+ — please write to us. See our <a href="#policy">restaurant policy</a> before booking.',
    "res_box_h": "Book online",
    "res_box_p": "Choose a date, time and number of guests. You will receive a confirmation by email.",
    "res_note": "Reservations by SevenRooms",
    "contact_h2": "Contact",
    "c_hours": "Opening hours", "c_hours_v": "Tuesday – Saturday<br>17:00&nbsp;–&nbsp;23:00", "c_closed": "Sunday – Monday closed",
    "c_write": "Write or call", "c_addr": "Address", "c_follow": "Follow the season",
    "policy_h2": "Restaurant policy", "policy_sub": "Good to know before you visit.",
    "policy": [
        ("Reservations &amp; cancellation", "We recommend booking a table, but walk-ins are always welcome when we have room. If your plans change, please cancel or move your booking at least 24 hours in advance, using the link in your confirmation email or by contacting us. For no-shows and late cancellations we may charge €30 per guest. We hold your table for 15 minutes after the booked time."),
        ("Allergies &amp; dietary needs", "Please tell us about allergies or dietary needs when you book, so the kitchen can prepare. The menu follows the season and what the farm delivers, so most courses can be adapted for vegetarian guests and common allergies. Our kitchen handles all common allergens, so we cannot guarantee a completely allergen-free meal."),
        ("Children", "Children are welcome. There is no separate children’s menu, but the kitchen is happy to prepare smaller portions. High chairs are available on request."),
        ("Groups &amp; private dining", "For groups of 8 or more, please contact us directly. Larger groups are served a set menu, and we may ask for a deposit to confirm the booking. The whole restaurant can be booked for private events."),
        ("Payment &amp; service charge", "A 10% service charge is added to the final bill. We accept all major payment cards. Please note that we do not accept cash."),
        ("Gift vouchers", 'Gift vouchers for 14horses are sold online by Senatorių Pasažas, in any amount from €20 to €1,000: <a href="https://www.senatoriupasazas.lt/#vouchers" rel="noopener" target="_blank">buy a gift voucher</a>. Vouchers are valid for 12 months from purchase, can be used in all our shops and restaurants in Senatorių Pasažas, and cannot be exchanged for cash.'),
    ],
    "f_nav": ["About us", "Menu", "Farmers Circle", "Reservations", "Restaurant policy", "Contact", "Instagram"],
    "nl_label": "Seasonal letter — new menus and harvest dinners",
    "nl_ph": "Your email", "nl_btn": "Sign up",
    "privacy": "Privacy policy",
    "service": "A 10% service charge is added to the final bill.",
    "lang_label": "Language",
}

LT = {
    "lang": "lt", "home": "/lt/", "other_home": "/",
    "title": "14horses — „nuo ūkio iki stalo“ restoranas Vilniaus senamiestyje",
    "desc": "„Nuo ūkio iki stalo“ restoranas restauruotame istoriniame dvare Senatorių pasaže, Vilniuje. Sezoninis keturių žingsnių meniu iš lietuviškų produktų, užaugintų mūsų regeneraciniame ūkyje Farmers Circle.",
    "skip": "Pereiti prie turinio",
    "nav": ["Apie mus", "Meniu", "Farmers Circle", "Renginiai", "Taisyklės", "Kontaktai"],
    "reserve": "Rezervuoti staliuką",
    "menu_open": "Atidaryti meniu",
    "menu_btn": "Meniu",
    "hero_over": "Senatorių pasažas · Vilniaus senamiestis",
    "hero_h1": "Lietuviški produktai – metų laikų ritmu.",
    "hero_lead": "„Nuo ūkio iki stalo“ virtuvė restauruotame istoriniame dvare. Keturi laisvai pasirenkami patiekalai iš to, ką šią savaitę užaugino mūsų ūkis ir kaimynai.",
    "hero_menu": "Šio sezono meniu",
    "alt_hero_a": "Vakarienei serviruotas stalas 14horses",
    "alt_hero_b": "Sena akmeninė siena Senatorių pasaže",
    "strip": [("Vakarienės", "Antradieniais – šeštadieniais 17:00&nbsp;–&nbsp;23:00"), ("Adresas", "Dominikonų g. 11, Vilnius"), ("MICHELIN gidas 2026", "Bib Gourmand")],
    "about_over": "Apie mus",
    "about_statement": "Kartais pavadiname 14horses keliaujančiu restoranu. Tai jau trečioji mūsų lokacija – tačiau šįkart pažabojome savus žirgus ir apsistojome Senatorių pasaže ilgam.",
    "about_body": [
        "Esminė pasakojimo linija nepasikeitė – lietuviški produktai nugula lėkštėse gamtos padiktuotu ritmu, o metų laikų kaitos nepamesti padeda mūsų regeneracinis ūkis Farmers Circle bei ūkininkai, su kuriais bendradarbiaujame ištisus metus.",
        "Visą vakarienę supakavome į keturių žingsnių laisvo pasirinkimo fiksuotos kainos meniu – užkandžiai, pirmasis patiekalas, pagrindinis patiekalas ir desertas atskleidžia pilną 14horses filosofijos, pagrįstos vietinės virtuvės principais, vaizdą.",
    ],
    "menu_h2": "Keturi žingsniai,<br>laisvas pasirinkimas.",
    "menu_intro": "Viena fiksuota kaina. Kiekvieną patiekalą renkatės iš trumpo sezoninio sąrašo. [[KAINA]] asmeniui · vynų derinimas [[KAINA]].",
    "steps": [("1 žingsnis", "Užkandžiai"), ("2 žingsnis", "Pirmasis patiekalas"), ("3 žingsnis", "Pagrindinis patiekalas"), ("4 žingsnis", "Desertas")],
    "dish": "[[Šefo patiekalai]]",
    "menu_full": "Visas meniu",
    "farm_over": "Farmers Circle · 70 km nuo stalo",
    "farm_h2": "Meniu sudaro mūsų ūkis.",
    "farm_body": "Farmers Circle – mūsų regeneracinis ūkis, vos 70 km nuo Vilniaus. Kartu su partneriais ūkininkais jis lemia, kas kiekvieną savaitę atkeliauja į virtuvę – ir ką ragausite šįvakar.",
    "farm_link": "Aplankykite Farmers Circle",
    "alt_farm": "Ėriukai ganosi Farmers Circle, mūsų regeneraciniame ūkyje",
    "farm_photo_todo": "Nuotrauka: Farmers Circle ūkis",
    "team_over": "Prie vadžių",
    "team": [("[[Vardas Pavardė]]", "Virtuvės vadovas"), ("[[Vardas Pavardė]]", "Restorano vadovas")],
    "gallery_label": "Galerija",
    "alt_gallery": ["Taurės prie lango", "Staliukai prie vyno sienos", "Vyno taurė ant serviruoto stalo", "Jaukus salės kampelis"],
    "alt_room": "14horses salė",
    "credit": "Nuotraukos",
    "events_h3": "Renginiai ir privatūs vakarai",
    "events_body": "Derliaus vakarienės, kviestiniai šefai ir visa salė jūsų progai.",
    "events_link": "Teiraukitės dėl renginių",
    "gift_h3": "Padovanokite vakarą",
    "gift_body": "14horses dovanų kuponas bet kokiai sumai nuo 20 iki 1 000 € – įsigykite internetu Senatorių pasaže.",
    "gift_link": "Pirkti dovanų kuponą",
    "res_h2": "Lauksime prie stalo.",
    "res_when": "Antradieniais – šeštadieniais nuo 17:00 · Dominikonų g. 11, Vilnius",
    "res_groups": 'Grupėms nuo 8 asmenų – parašykite mums. Prieš rezervuodami susipažinkite su <a href="#policy">restorano taisyklėmis</a>.',
    "res_box_h": "Rezervuokite internetu",
    "res_box_p": "Pasirinkite datą, laiką ir svečių skaičių. Patvirtinimą gausite el. paštu.",
    "res_note": "Rezervacijos per SevenRooms",
    "contact_h2": "Kontaktai",
    "c_hours": "Darbo laikas", "c_hours_v": "Antradieniais – šeštadieniais<br>17:00&nbsp;–&nbsp;23:00", "c_closed": "Sekmadienį – pirmadienį nedirbame",
    "c_write": "Rašykite ar skambinkite", "c_addr": "Adresas", "c_follow": "Sekite sezoną",
    "policy_h2": "Restorano taisyklės", "policy_sub": "Naudinga žinoti prieš apsilankant.",
    "policy": [
        ("Rezervacijos ir atšaukimas", "Rekomenduojame staliuką rezervuoti iš anksto, tačiau visada laukiame ir užsukusių be rezervacijos, jei turime vietos. Jei planai pasikeitė, rezervaciją atšaukite ar pakeiskite likus ne mažiau kaip 24 val. – per nuorodą patvirtinimo laiške arba susisiekę su mumis. Neatvykus ar atšaukus per vėlai, galime taikyti 30 € mokestį asmeniui. Staliuką laikome 15 min. po rezervuoto laiko."),
        ("Alergijos ir mitybos poreikiai", "Apie alergijas ar mitybos poreikius praneškite rezervuodami, kad virtuvė galėtų pasiruošti. Meniu keičiasi pagal sezoną ir ūkio derlių, todėl daugumą patiekalų galime pritaikyti vegetarams ir esant dažniausioms alergijoms. Mūsų virtuvėje naudojami visi dažniausi alergenai, todėl negalime garantuoti, kad patiekalas bus visiškai be alergenų."),
        ("Vaikai", "Vaikai laukiami. Atskiro vaikų meniu neturime, tačiau virtuvė mielai paruoš mažesnes porcijas. Paprašius suteiksime aukštą kėdutę."),
        ("Grupės ir privatūs vakarai", "Grupėms nuo 8 asmenų prašome susisiekti tiesiogiai. Didesnėms grupėms patiekiamas fiksuotas meniu, o rezervacijai patvirtinti galime paprašyti užstato. Visą restoraną galima užsisakyti privačiam renginiui."),
        ("Mokėjimas ir aptarnavimo mokestis", "Prie galutinės sąskaitos pridedamas 10 % aptarnavimo mokestis. Priimame visas pagrindines mokėjimo korteles. Atkreipiame dėmesį, kad grynųjų pinigų nepriimame."),
        ("Dovanų kuponai", '14horses dovanų kuponus internetu parduoda Senatorių pasažas – bet kokiai sumai nuo 20 iki 1 000 €: <a href="https://www.senatoriupasazas.lt/#vouchers" rel="noopener" target="_blank">pirkti dovanų kuponą</a>. Kuponas galioja 12 mėn. nuo įsigijimo, juo galima atsiskaityti visose mūsų parduotuvėse ir restoranuose Senatorių pasaže, tačiau jo negalima iškeisti į pinigus.'),
    ],
    "f_nav": ["Apie mus", "Meniu", "Farmers Circle", "Rezervacijos", "Restorano taisyklės", "Kontaktai", "Instagram"],
    "nl_label": "Sezoninis laiškas – nauji meniu ir derliaus vakarienės",
    "nl_ph": "Jūsų el. paštas", "nl_btn": "Prenumeruoti",
    "privacy": "Privatumo politika",
    "service": "Prie galutinės sąskaitos pridedamas 10 % aptarnavimo mokestis.",
    "lang_label": "Kalba",
}

IG_SVG = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.8"/></svg>'
MENU_SVG = ('<svg class="i-open" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 8h18M3 16h12"/></svg>'
            '<svg class="i-close" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>')
NUMS = ["一", "二", "三", "四"]


def ph(s: str) -> str:
    """Mark [[placeholders]] so they are visible until filled."""
    return re.sub(r"\[\[(.+?)\]\]", r'<span class="todo" title="Placeholder – replace before launch">[\1]</span>', s)


def page(t: dict) -> str:
    nav_ids = ["about", "menu", "farmers-circle", "events", "policy", "contact"]
    nav = "\n".join(f'          <a href="#{i}">{l}</a>' for i, l in zip(nav_ids, t["nav"]))
    en_cur = 'aria-current="true"' if t["lang"] == "en" else ""
    lt_cur = 'aria-current="true"' if t["lang"] == "lt" else ""
    strip = "\n".join(f"        <div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in t["strip"][:2])
    a3, b3 = t["strip"][2]
    bib = (f'<img class="bib" src="{BIB_LOGO}" alt="MICHELIN Guide 2026" width="56" height="56">' if BIB_LOGO
           else '<span class="bib bib--todo" role="img" aria-label="MICHELIN Bib Gourmand 2026"><span class="todo">[Bib Gourmand logo]</span></span>')
    strip += f'\n        <div class="strip__award">{bib}<div><dt>{a3}</dt><dd>{b3}</dd></div></div>'
    about_body = "\n".join(f"          <p>{p}</p>" for p in t["about_body"])
    steps = "\n".join(
        f'        <li><span class="num" aria-hidden="true">{n}</span><span class="lbl">{a}</span><span class="name">{b}</span><span class="dish">{ph(t["dish"])}</span></li>'
        for n, (a, b) in zip(NUMS, t["steps"]))
    team = "\n".join(
        f'      <div class="person"><div class="frame r{k+1}" aria-hidden="true"></div><div><span class="person__name">{ph(n)}</span><span class="person__role">{r}</span></div></div>'
        for k, (n, r) in enumerate(t["team"]))
    gal = "\n".join(
        f'    <div class="frame r{k+1}"><img src="{PHOTOS["g"+str(k+1)]}" alt="{a}" loading="lazy" decoding="async"></div>'
        for k, a in enumerate(t["alt_gallery"]))
    policy = "\n".join(
        f'          <details{" open" if k == 0 else ""}><summary>{q}</summary><p>{ph(a)}</p></details>'
        for k, (q, a) in enumerate(t["policy"]))
    f_ids = ["about", "menu", "farmers-circle", "reserve", "policy", "contact", CONTACT["instagram_url"]]
    f_nav = "\n".join(
        f'        <a href="{i if i.startswith("http") else "#" + i}"{" rel=\"noopener\" target=\"_blank\"" if i.startswith("http") else ""}>{l}</a>'
        for i, l in zip(f_ids, t["f_nav"]))
    canonical = SITE_URL + t["home"]
    alt_lang = "lt" if t["lang"] == "en" else "en"
    alt_url = SITE_URL + t["other_home"]
    mail = CONTACT["email"]; phone = CONTACT["phone"]
    fc = CONTACT["farmers_circle_url"]
    farm_img = (f'    <div class="frame r3"><img src="{PHOTOS["farm"]}" alt="{t["alt_farm"]}" loading="lazy" decoding="async"></div>' if PHOTOS["farm"]
                else f'    <div class="frame r3" style="display:flex;align-items:flex-end;padding:20px;font-size:14px;color:#3A352F" role="img" aria-label="{t["alt_farm"]}"><span class="todo">[{t["farm_photo_todo"]}]</span></div>')
    farm_link = f'      <a class="link" href="{fc}" rel="noopener" target="_blank">{t["farm_link"]}</a>\n' if fc else ""

    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{html.escape(t['desc'])}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="{t['lang']}" href="{canonical}">
<link rel="alternate" hreflang="{alt_lang}" href="{alt_url}">
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{html.escape(t['desc'])}">
<meta property="og:image" content="{SITE_URL}{PHOTOS['hero_a']}">
<meta property="og:type" content="restaurant">
<meta name="theme-color" content="#EFEAE2">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500&family=Karla:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Restaurant","name":"14horses","url":"{SITE_URL}/","image":"{SITE_URL}{PHOTOS['hero_a']}","servesCuisine":"Lithuanian, farm-to-table","address":{{"@type":"PostalAddress","streetAddress":"Dominikonų g. 11","addressLocality":"Vilnius","addressCountry":"LT"}},"openingHoursSpecification":[{{"@type":"OpeningHoursSpecification","dayOfWeek":["Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"17:00","closes":"23:00"}}],"acceptsReservations":"True"}}
</script>
</head>
<body>
<a class="skip" href="#main">{t['skip']}</a>

<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="nav__logo" href="{t['home']}"><img src="/assets/logo.png" alt="14horses" width="140" height="171"></a>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="{t['menu_open']}">{MENU_SVG}<span aria-hidden="true">{t['menu_btn']}</span></button>
    <div class="nav__links" id="nav-links">
{nav}
      <span class="nav__lang" aria-label="{t['lang_label']}"><a href="/lt/" hreflang="lt" lang="lt" {lt_cur}>LT</a> / <a href="/" hreflang="en" lang="en" {en_cur}>EN</a></span>
      <a class="btn" href="#reserve">{t['reserve']}</a>
    </div>
  </nav>
</header>

<main id="main">
  <section class="wrap hero">
    <div class="hero__text">
      <p class="overline">{t['hero_over']}</p>
      <h1>{t['hero_h1']}</h1>
      <p class="hero__lead">{t['hero_lead']}</p>
      <div class="hero__ctas">
        <a class="btn" href="#reserve">{t['reserve']}</a>
        <a class="link" href="#menu">{t['hero_menu']}</a>
      </div>
    </div>
    <div class="hero__images">
      <div class="frame r1 a"><img src="{PHOTOS['hero_a']}" alt="{t['alt_hero_a']}" fetchpriority="high"></div>
      <div class="frame r2 b"><img src="{PHOTOS['hero_b']}" alt="{t['alt_hero_b']}"></div>
    </div>
  </section>

  <section class="strip" aria-label="{t['strip'][0][0]}">
    <dl class="wrap">
{strip}
    </dl>
  </section>

  <section id="about" class="wrap split">
    <div class="split__aside"><h2 class="overline">{t['about_over']}</h2></div>
    <div class="split__main">
      <p class="statement">{t['about_statement']}</p>
      <div class="prose">
{about_body}
      </div>
    </div>
  </section>

  <section class="wrap feature">
    <div class="frame feature__img"><img src="{PHOTOS['room']}" alt="{t['alt_room']}" loading="lazy" decoding="async"></div>
  </section>

  <section id="menu" class="menu">
    <div class="wrap">
      <div class="menu__head">
        <h2>{t['menu_h2']}</h2>
        <p class="menu__intro">{ph(t['menu_intro'])}</p>
      </div>
      <ol class="steps">
{steps}
      </ol>
    </div>
  </section>

  <section id="farmers-circle" class="wrap farm">
{farm_img}
    <div class="farm__text">
      <p class="overline">{t['farm_over']}</p>
      <h2>{t['farm_h2']}</h2>
      <p class="muted">{t['farm_body']}</p>
{farm_link}    </div>
  </section>

  <section class="team" aria-labelledby="team-h">
    <div class="wrap">
      <h2 id="team-h" class="overline">{t['team_over']}</h2>
      <div class="team__people">
{team}
      </div>
    </div>
  </section>

  <section class="wrap gallery" aria-label="{t['gallery_label']}">
{gal}
  </section>

  <section class="wrap cards">
    <div id="events" class="card">
      <h3>{t['events_h3']}</h3>
      <p class="muted">{t['events_body']}</p>
      <a class="link" href="#contact">{t['events_link']}</a>
    </div>
    <div class="card">
      <h3>{t['gift_h3']}</h3>
      <p class="muted">{t['gift_body']}</p>
      <a class="link" href="https://www.senatoriupasazas.lt/#vouchers" rel="noopener" target="_blank">{t['gift_link']}</a>
    </div>
  </section>

  <section id="reserve" class="reserve">
    <div class="wrap">
      <div class="reserve__text">
        <h2>{t['res_h2']}</h2>
        <p>{t['res_when']}</p>
        <p style="font-size:15px">{ph(t['res_groups'])}</p>
      </div>
      <div class="reserve__box r1">
        <h3 style="font-size:28px">{t['res_box_h']}</h3>
        <p class="muted" style="font-size:15px">{t['res_box_p']}</p>
        <a id="sevenrooms-trigger" class="btn btn--lg" href="#contact">{t['reserve']}</a>
        <p class="reserve__note">{t['res_note']}</p>
      </div>
    </div>
  </section>

  <section id="policy" class="policy">
    <div class="wrap split">
      <div class="split__aside" style="display:flex;flex-direction:column;gap:12px">
        <h2 class="section-title">{t['policy_h2']}</h2>
        <p class="muted" style="font-size:15px">{t['policy_sub']}</p>
      </div>
      <div class="split__main accordion" style="gap:0">
{policy}
      </div>
    </div>
  </section>

  <section id="contact" class="wrap split">
    <div class="split__aside"><h2 class="section-title">{t['contact_h2']}</h2></div>
    <div class="split__main contact-grid">
      <div><span class="label">{t['c_hours']}</span><span>{t['c_hours_v']}</span><span class="muted">{t['c_closed']}</span></div>
      <div><span class="label">{t['c_write']}</span><a href="mailto:{mail}">{ph(mail)}</a><a href="tel:{phone}">{ph(phone)}</a></div>
      <div><span class="label">{t['c_addr']}</span><a href="{CONTACT['maps']}" rel="noopener" target="_blank">{CONTACT['address']}<br>Senatorių pasažas</a></div>
      <div><span class="label">{t['c_follow']}</span><a class="ig" href="{CONTACT['instagram_url']}" rel="noopener" target="_blank">{IG_SVG}<span>Instagram · {ph(CONTACT['instagram_handle'])}</span></a></div>
    </div>
  </section>

</main>

<footer>
  <div class="wrap footer">
    <address>
      <span class="footer__name">14horses</span>
      <span>{CONTACT['address']}</span>
      <span>Senatorių pasažas</span>
    </address>
    <nav aria-label="Footer">
{f_nav}
    </nav>
    <form class="newsletter" action="#" onsubmit="return false">
      <label for="nl">{t['nl_label']}</label>
      <div class="newsletter__row">
        <input id="nl" type="email" autocomplete="email" placeholder="{t['nl_ph']}">
        <button class="btn" type="submit">{t['nl_btn']}</button>
      </div>
    </form>
  </div>
  <div class="wrap">
    <div class="footer__bottom">
    <span>© <span data-year>2026</span> 14horses · {t['credit']}: {PHOTO_CREDIT}</span>
    <span>{t['service']}</span>
    <a href="#privacy">{t['privacy']}</a>
    </div>
  </div>
</footer>

<script src="/assets/main.js" defer></script>
</body>
</html>
"""


def main():
    (ROOT / "index.html").write_text(page(EN), encoding="utf-8")
    (ROOT / "lt").mkdir(exist_ok=True)
    (ROOT / "lt" / "index.html").write_text(page(LT), encoding="utf-8")
    print("built", ROOT)


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Artifact preview: one self-contained file with an EN/LT switch.
# Same content as the site; photos shown as labelled placeholders.
# Run:  python3 build/build.py artifact   ->  build/artifact/14horses.html
# ---------------------------------------------------------------------------
import base64

ARTIFACT_CSS = """
:root { color-scheme: light; }
.wrap { padding-left: max(var(--gutter), env(safe-area-inset-left, 0px)); padding-right: max(var(--gutter), env(safe-area-inset-right, 0px)); }
.site-header { top: env(safe-area-inset-top, 0px); }
.draftbar { background: var(--ink); color: var(--on-dark-2); font-size: 13px; }
.draftbar .wrap { display: flex; flex-wrap: wrap; gap: 6px 16px; justify-content: space-between; padding-block: 8px; }
.draftbar b { color: var(--on-dark); font-weight: 600; }
.ph { width: 100%; height: 100%; display: flex; align-items: flex-end; padding: 16px; font-size: 13px; color: #3A352F; line-height: 1.4; }
.todo { background: rgba(122, 92, 67, .12); border-radius: 2px; padding: 0 3px; }
.menu .todo { background: rgba(239, 234, 226, .10); }
"""


def _body(doc: str) -> str:
    b = doc.split("<body>", 1)[1].split("</body>", 1)[0]
    b = re.sub(r'<script src="/assets/main.js" defer></script>\s*', "", b)
    return b


def _artifact_body(t: dict, logo_uri: str) -> str:
    b = _body(page(t))
    # external photos -> labelled placeholders (artifact pages can't load images from other sites)
    b = re.sub(r'<img src="https?://[^"]+" alt="([^"]*)"[^>]*>',
               lambda m: f'<div class="ph">[{"Photo" if t["lang"] == "en" else "Nuotrauka"}: {m.group(1)}]</div>', b)
    b = b.replace('src="/assets/img/', 'src="assets/img/')
    b = b.replace('src="/assets/logo.png"', f'src="{logo_uri}"')
    b = b.replace('src="/assets/michelin-2026.png"', 'src="data:image/png;base64,' + base64.b64encode((ROOT / "assets" / "michelin-2026.png").read_bytes()).decode() + '"')
    b = b.replace(f'class="nav__logo" href="{t["home"]}"', 'class="nav__logo" href="#top"')
    b = re.sub(r'<a href="/lt/" hreflang="lt" lang="lt"', '<a href="#" data-setlang="lt" hreflang="lt" lang="lt"', b)
    b = re.sub(r'<a href="/" hreflang="en" lang="en"', '<a href="#" data-setlang="en" hreflang="en" lang="en"', b)
    b = b.replace('<form class="newsletter" action="#" onsubmit="return false">', '<form class="newsletter">')
    if t["lang"] == "lt":  # keep ids unique when both languages share one page
        b = re.sub(r'\bid="([\w-]+)"', r'id="lt-\1"', b)
        b = re.sub(r'href="#(?!")([\w-]+)"', r'href="#lt-\1"', b)
        b = re.sub(r'\b(for|aria-controls|aria-labelledby)="([\w-]+)"', r'\1="lt-\2"', b)
    return b


ARTIFACT_JS = r"""
(function () {
  var KEY = '14horses-lang';
  function setLang(l) {
    document.querySelectorAll('[data-lang]').forEach(function (el) { el.hidden = el.getAttribute('data-lang') !== l; });
    document.documentElement.lang = l;
    try { localStorage.setItem(KEY, l); } catch (e) {}
  }
  var start = 'en';
  if (location.hash === '#lt') start = 'lt';
  else { try { start = localStorage.getItem(KEY) || 'en'; } catch (e) {} }
  setLang(start === 'lt' ? 'lt' : 'en');

  document.addEventListener('click', function (e) {
    var a = e.target.closest('a');
    if (!a) return;
    var l = a.getAttribute('data-setlang');
    if (l) { e.preventDefault(); setLang(l); window.scrollTo(0, 0); return; }
    var href = a.getAttribute('href') || '';
    if (href === '#top') { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }
  });

  document.querySelectorAll('.site-header').forEach(function (header) {
    var toggle = header.querySelector('.nav__toggle');
    if (!toggle) return;
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    header.querySelectorAll('.nav__links a').forEach(function (a) {
      a.addEventListener('click', function () { header.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  });

  document.querySelectorAll('form.newsletter').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); });
  });
  document.querySelectorAll('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
"""


def build_artifact():
    logo_uri = "data:image/png;base64," + base64.b64encode((ROOT / "assets" / "logo.png").read_bytes()).decode()
    css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8") + ARTIFACT_CSS
    draft = ('<div class="draftbar"><div class="wrap"><span><b>Draft</b> · 14horses.com redesign · not public</span>'
             '<span>Text in [brackets] still needs real content</span></div></div>')
    html_out = f"""<title>14horses Website</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500&family=Karla:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{css}
</style>
<div id="top"></div>
{draft}
<div data-lang="en">
{_artifact_body(EN, logo_uri)}
</div>
<div data-lang="lt" lang="lt" hidden>
{_artifact_body(LT, logo_uri)}
</div>
<script>{ARTIFACT_JS}</script>
"""
    out = pathlib.Path(__file__).resolve().parent / "artifact"
    out.mkdir(exist_ok=True)
    (out / "14horses.html").write_text(html_out, encoding="utf-8")
    print("artifact built", out / "14horses.html")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "artifact":
        build_artifact()
