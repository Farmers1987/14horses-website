#!/usr/bin/env python3
"""Builds the 14horses site (EN at /, LT at /lt/) from one template.

Edit the TEXT dictionaries below and run:  python3 build/build.py
Anything wrapped in [[...]] is a placeholder still waiting for real content;
it is rendered with a dashed underline so it is easy to spot.
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "site"
SITE_URL = "https://14horses.lt"

# Photos by G. Rozmanaite (14horses photo shoot), resized in site/assets/img
PHOTOS = {
    "hero":   "/assets/img/hero-wide.jpg",
    "hero_a": "/assets/img/hero-wide.jpg",
    "m1":     "/assets/img/room-wine.jpg",
    "m2":     "/assets/img/room-corner.jpg",
    "m3":     "/assets/img/room-detail.jpg",
    "g5":     "/assets/img/hero-table.jpg",
    "g6":     "/assets/img/room-light.jpg",
    "g7":     "/assets/img/room-detail.jpg",
    "hero_b": "/assets/img/hero-stone.jpg",
    "room":   "/assets/img/room-wide.jpg",
    "farm":   "/assets/img/farm-sheep-wide.jpg",
    "g1":     "/assets/img/gallery-1.jpg",
    "g2":     "/assets/img/gallery-2.jpg",
    "g3":     "/assets/img/gallery-3.jpg",
    "g4":     "/assets/img/gallery-4.jpg",
}
PHOTO_CREDIT = "G. Rozmanaite"

# MailerLite web form (Senatorių Pasažas newsletter, form code h8a6e9)
SEVENROOMS_URL = "https://www.sevenrooms.com/explore/14horses/reservations/create/search/"
MAILERLITE_URL = "https://static.mailerlite.com/webforms/submit/h8a6e9"

# Official MICHELIN Bib Gourmand 2026 logo file (from the restaurant's Michelin award kit). Empty = placeholder.
BIB_LOGO = "/assets/michelin-2026.png"

CONTACT = {
    "email": "14horses@bfr.lt",
    "phone": "+370 612 50845",
    "instagram_handle": "@14horses_restaurant",
    "instagram_url": "https://www.instagram.com/14horses_restaurant/",
    "address": "Dominikonų g. 11, Vilnius",
    "maps": "https://maps.google.com/?q=Dominikon%C5%B3+g.+11,+Vilnius",
    # Link for "Visit Farmers Circle". Leave empty to hide the link.
    "farmers_circle_url": "",
}

EN = {
    "res_box_h": "Booking",
    "lang": "en", "home": "/", "other_home": "/lt/",
    "title": "14 Horses – Contemporary Baltic–Scandinavian restaurant in Vilnius",
    "desc": "Within the historic walls of Vainai Palace, a new chapter unfolds at 14 Horses. Led by Chef Aleksandras Fedorovičius, our new team brings fresh creative energy to contemporary Baltic–Scandinavian cuisine, defined by bold flavours and unexpected combinations.",
    "skip": "Skip to content",
    "nav": ["About us", "Menu", "Farmers Circle", "Events", "Policy", "Contact"],
    "reserve": "Reserve a table",
    "menu_open": "Open menu",
    "menu_btn": "Menu",
    "hero_over": "Senatorių Pasažas · Vilnius Old Town",
    "hero_h1": "Our roots lie in the soil.",
    "hero_lead": "Within the historic walls of Vainai Palace, a new chapter unfolds at 14 Horses. Led by Chef Aleksandras Fedorovičius, our new team brings fresh creative energy to contemporary Baltic–Scandinavian cuisine, defined by bold flavours and unexpected combinations.",
    "hero_menu": "See the menu",
    "alt_hero_a": "A table set for dinner at 14 Horses",
    "alt_hero_b": "Old stone wall in Senatorių Pasažas",
    "strip": [("Opening hours", "Tuesday–Thursday 17:00–22:00<br>Friday–Saturday 17:00–23:00"), ("Address", "Dominikonų g. 11, Vilnius"), ("MICHELIN Guide 2026", "Bib Gourmand")],
    "about_over": "About us",
    "about_statement": "The historic walls of Vainai Palace, a renewed creative energy and an ambition for bold flavours.",
    "about_body": [
        "At Farmers Circle in the village of Radiškis, the seasons set the rhythm and inspire ideas for the menu to come. 14 Horses is part of this farm. From the soil to the creativity of the kitchen and the conversation at the table, an unbroken journey of discovery unfolds. Knowledge of what we grow, how we prepare it and why we choose it passes through our team to our guests, giving flavour its context and the experience its depth.",
        "!Nose to tail. Root to leaf.",
        "This is how we understand respect for an ingredient: knowing its origins, revealing its character and finding value in every part. In our kitchen, seasonal, local produce meets unexpected combinations, adventurous techniques and bold flavours.",
        "We find beauty in the natural: organic forms, textures and the traces left by time. An appreciation of imperfection, close to the philosophy of wabi-sabi, allows our historic setting and contemporary gastronomy to speak the same language.",
        "!At our table, this language becomes flavour - bold, distinctive and memorable.",
    ],
    "menu_h2": "Menu",
    "menus": ["Tasting menu", "Dining week", "À la carte"],
    "soon": "Coming soon", "close": "Close",
    "prev": "Previous photos", "next": "Next photos",
    "menu_intro": "Seasonal, local produce meets unexpected combinations, adventurous techniques and bold flavours. The menu follows what the season brings to Farmers Circle.",
    "steps": [("Step 1", "Snacks"), ("Step 2", "Starter"), ("Step 3", "Main course"), ("Step 4", "Dessert")],
    "dish": "[[MENU]]",
    "menu_full": "Read the full menu",
    "farm_over": "Farmers Circle",
    "farm_h2": "At Farmers Circle, the land tells the story.",
    "farm_body": "Founded in 2018 by Danish entrepreneur Niels Peter Pretzmann, this organic farm in Radiškis, Ukmergė district, nurtures the connection between soil, plants, animals and people. From the outset, it has grown around the belief that good food begins with a responsible relationship with nature. Here, the seasons set the pace, and every decision considers both the harvest to come and the land that will sustain it.",
    "farm_link": "Visit Farmers Circle",
    "read_more": "Read more", "read_less": "Show less",
    "farm_more": [
        "Grains grow in the fields, seasonal vegetables and culinary herbs fill the gardens, and Angus cattle graze the pastures. The farm’s produce also includes organic eggs and poultry, buckwheat, oats and flour. This diversity creates an interconnected system in which crop cultivation, market gardening and livestock farming support one another.",
        "Part of the harvest takes on a new form right here, in the farm’s own production kitchen. Vegetables are fermented and made into sauces, spreads and condiments, while the flavours of the seasons are preserved in jams, syrups and vinegars. The short distance between garden and kitchen allows freshly harvested produce to be processed promptly, preserving its character and finding value even in ingredients with an imperfect appearance.",
        "Care for the soil connects every aspect of the farm. Regenerative practices – reduced tillage, crop rotation, cover cropping, rotational grazing and composting – help restore soil vitality and support biodiversity. Organic matter returns to the soil through compost, nourishing future harvests. The end of one season becomes the beginning of the next.",
        "Farmers Circle is also a place for gathering and discovery. Its very name invites growers, chefs, like-minded people and curious guests into a shared circle, united by a desire to understand where their food comes from. Farm tours, educational activities and cooking experiences open a window onto everyday farming and the work behind each ingredient.",
        "This journey continues at Red Brick, the farm’s restaurant, where the harvest becomes a seasonal gastronomic experience. Event and meeting spaces, accommodation and a farm shop invite guests to stay a little longer – to observe, taste and settle into the rhythm of the place.",
    ],
    "farm_close": "From soil to harvest. From experience to knowledge shared. This is how the Farmers Circle turns.",
    "alt_farm": "Lambs grazing at Farmers Circle, our regenerative farm",
    "farm_photo_todo": "Photo: Farmers Circle farm",
    "team_over": "At the reins of 14 Horses",
    "team": [("Aleksandras Fedorovičius", "Head Chef"), ("Ela Žoromskė", "Restaurant Manager"), ("Matas Simaitis", "Restaurant Manager")],
    "gallery_label": "Gallery",
    "alt_gallery": ["Wine glasses by the window", "Tables by the wine wall", "A glass of wine on a set table", "A quiet corner of the dining room"],
    "alt_room": "The dining room at 14 Horses",
    "alt_hero": "A table by the window in the dining room at 14 Horses",
    "alt_mosaic": ["Tables in front of the wine wall", "A set table among oak and steel", "Wine glasses on an oak table"],
    "alt_more": ["A table set for dinner", "Soft light over a set table", "Wine glasses on an oak table"],
    "credit": "Photos",
    "events_h3": "Events &amp; private dining",
    "events_body": "Seasonal dinners, guest-chef evenings and exclusive use of our dining room for your special occasion.",
    "events_link": "Request for events",
    "gift_h3": "Give the gift of an evening at 14 Horses",
    "gift_body": "A gift voucher for 14 Horses in any amount from €20 to €1,000. Valid for 12 months at all our restaurants and shops in Senatorių Pasažas.",
    "gift_link": "Buy a gift voucher",
    "res_h2": "Join us at the table.",
    "res_when": "Tuesday - Saturday from 17:00 · Dominikonų g. 11, Vilnius",
    "res_groups": 'Groups of 8 or more are arranged individually - please contact us. Read our <a href="#policy">restaurant policy</a> before booking.',
    "res_deposit": "A deposit of €20 per person is required to confirm a reservation. This amount will be credited towards the final bill.",
    "res_box_p": "Choose a date, time and number of guests. A €20 per person deposit confirms your table and is credited to your bill.",
    "res_note": "Reservations by SevenRooms",
    "contact_h2": "Contact",
    "c_hours": "Opening hours", "c_hours_v": "Tuesday–Thursday 17:00–22:00<br>Friday–Saturday 17:00–23:00",
    "c_phone": "Phone number", "c_email": "Email", "c_social": "Social media", "c_closed": "Sunday–Monday closed",
    "aria_main": "Main", "aria_footer": "Footer", "bib_alt": "MICHELIN Guide 2026",
    "c_write": "Write or call", "c_addr": "Address", "c_follow": "Follow the season",
    "policy_h2": "Restaurant policy", "policy_sub": "Restaurant Rules and Reservation Terms",
    "policy": [
        ("Reservations and Dining Duration", "Tables are reserved for 2 hours. Longer visits must be arranged in advance. Reserved tables are held for 15 minutes after the reservation time. Please inform the restaurant team if you are running late. Reservations will be cancelled if guests arrive more than 15 minutes late without prior notice."),
        ("Reservation Deposit and Cancellation Terms", "A deposit of €20 per person is required to confirm a reservation. This amount will be credited towards the final bill. For cancellations made at least 24 hours before the reservation time, the deposit will be refunded. For later cancellations or no-shows, the deposit is non-refundable. The same cancellation and refund terms apply to prepaid tasting events."),
        ("Group Reservations", "Reservations for groups of 8 or more guests are arranged individually. Groups may choose dishes from the restaurant menu."),
        ("Children", "Children are welcome at the restaurant. High chairs are available. We do not offer a separate children’s menu."),
        ("Pets", "Pets are welcome both inside the restaurant and on the terrace. The accompanying guest is responsible for their pet’s care and behaviour. Pets must not disturb other guests or interfere with restaurant operations."),
        ("Allergies and Dietary Requirements", "Menu adaptations and specific adjustments are agreed with the restaurant team on an individual basis."),
        ("Kitchen Opening Hours", "The kitchen is open until 21:00 on Tuesdays, Wednesdays and Thursdays, and until 22:00 on Fridays and Saturdays."),
        ("Dress Code", "The recommended dress code is smart casual."),
        ("Payment and Service Charge", "The restaurant accepts card payments only. Cash is not accepted. A 10% service charge is added to the final bill."),
    ],
    "f_nav": ["About us", "Menu", "Farmers Circle", "Events", "Restaurant policy", "Contact", "Instagram"],
    "nl_label": "Sign up for stories from our restaurants, kitchens, farm and shops every two weeks.",
    "nl_ph": "Your email", "nl_btn": "Sign up",
    "nl_note": "Newsletter from Senatorių Pasažas.",
    "nl_ok": "Thank you! You have successfully subscribed to the newsletter.",
    "nl_err": "Please enter a valid email address.",
    "privacy": "Privacy policy",
    "service": "A 10% service charge is added to the final bill.",
    "ck_title": "Cookies",
    "ck_text": "We'd like to use cookies to see how guests use our website, so we can keep improving it, and to show you relevant news from us on Google and Meta. You can change your choice at any time under Cookie settings.",
    "ck_nec": ("Necessary", "Remembers your language and cookie choice. Always on."),
    "ck_stat": ("Statistics", "Google Analytics: how visitors use the site."),
    "ck_mkt": ("Marketing", "Google and Meta: showing relevant ads and measuring them."),
    "ck_accept": "Accept all",
    "ck_reject": "Reject all",
    "ck_settings": "Settings",
    "ck_save": "Save choices",
    "ck_footer": "Cookie settings",
    "lang_label": "Language",
}

LT = {
    "res_box_h": "Rezervacijos",
    "lang": "lt", "home": "/lt/", "other_home": "/",
    "title": "14 Horses – šiuolaikinės Baltijos ir Skandinavijos šalių virtuvės restoranas Vilniuje",
    "desc": "Tarp istorinių Vainų rūmų sienų atsiveria naujas „14 Horses“ skyrius. Šefo Aleksandro Fedorovičiaus vedama nauja komanda šiuolaikinei Baltijos ir Skandinavijos šalių virtuvei suteikia naujos kūrybinės energijos, atsiskleidžiančios ryškiais skoniais ir netikėtais deriniais.",
    "skip": "Pereiti prie turinio",
    "nav": ["Apie mus", "Meniu", "Farmers Circle", "Renginiai", "Taisyklės", "Kontaktai"],
    "reserve": "Rezervuoti staliuką",
    "menu_open": "Atidaryti meniu",
    "menu_btn": "Meniu",
    "hero_over": "Senatorių Pasažas · Vilniaus senamiestis",
    "hero_h1": "Mūsų pradžia – žemėje.",
    "hero_lead": "Tarp istorinių Vainų rūmų sienų atsiveria naujas „14 Horses“ skyrius. Šefo Aleksandro Fedorovičiaus vedama nauja komanda šiuolaikinei Baltijos ir Skandinavijos šalių virtuvei suteikia naujos kūrybinės energijos, atsiskleidžiančios ryškiais skoniais ir netikėtais deriniais.",
    "hero_menu": "Meniu",
    "alt_hero_a": "Vakarienei serviruotas stalas 14 Horses",
    "alt_hero_b": "Sena akmeninė siena Senatorių Pasaže",
    "strip": [("Darbo valandos", "Antradieniais–ketvirtadieniais 17:00–22:00<br>Penktadieniais–šeštadieniais 17:00–23:00"), ("Adresas", "Dominikonų g. 11, Vilnius"), ("MICHELIN gidas 2026", "Bib Gourmand")],
    "about_over": "Apie mus",
    "about_statement": "Istorinės Vainų rūmų sienos, nauja kūrybinė energija ir ryškaus skonio ambicija.",
    "about_body": [
        "Radiškių kaime įsikūrusiame „Farmers Circle“ ūkyje, kur metų laikai diktuoja ritmą ir augina būsimo meniu idėjas. „14 Horses“ yra šio ūkio dalis. Nuo dirvos iki kūrybos virtuvėje ir pokalbio prie stalo tęsiasi vientisa pažinimo kelionė. Žinios apie tai, ką auginame, kaip ruošiame ir kodėl renkamės, nuosekliai keliauja per mūsų komandą iki svečio, suteikdamos skoniui kontekstą, o patirčiai - gylį.",
        "!Nuo galvos iki uodegos. Nuo šaknų iki lapelių.",
        "Taip suprantame pagarbą ingredientui: pažinti jo kilmę, atskleisti charakterį ir atrasti vertę kiekvienoje jo dalyje. Sezoniškumas ir vietiniai produktai mūsų virtuvėje susitinka su netikėtais deriniais, drąsiomis technikomis ir ryškiais skoniais.",
        "Estetiką atrandame natūralume - organiškose formose, tekstūrose, laiko paliktuose pėdsakuose. „Wabi-sabi“ artimas gebėjimas įžvelgti grožį netobulume leidžia istorinei aplinkai ir šiuolaikinei gastronomijai kalbėti viena kalba.",
        "!Prie mūsų stalo ši kalba įgauna skonį - ryškų, savitą, įsimenantį.",
    ],
    "menu_h2": "Meniu",
    "menus": ["Degustacinis meniu", "Gastronomijos savaitė", "À la carte"],
    "soon": "Jau netrukus", "close": "Uždaryti",
    "prev": "Ankstesnės nuotraukos", "next": "Kitos nuotraukos",
    "menu_intro": "Sezoniškumas ir vietiniai produktai susitinka su netikėtais deriniais, drąsiomis technikomis ir ryškiais skoniais. Meniu seka tai, ką sezonas atneša į „Farmers Circle“ ūkį.",
    "steps": [("1 žingsnis", "Užkandžiai"), ("2 žingsnis", "Pirmasis patiekalas"), ("3 žingsnis", "Pagrindinis patiekalas"), ("4 žingsnis", "Desertas")],
    "dish": "[[MENIU]]",
    "menu_full": "Visas meniu",
    "farm_over": "Farmers Circle",
    "farm_h2": "„Farmers Circle“ istoriją rašo žemė.",
    "farm_body": "2018 metais danų verslininko Niels Peter Pretzmann įkurtas ekologinis ūkis Radiškio kaime, Ukmergės rajone, puoselėja ryšį tarp dirvožemio, augalų, gyvūnų ir žmogaus. Nuo pat pradžių jį augina įsitikinimas, kad geras maistas prasideda nuo atsakingo santykio su gamta. Čia metų laikai diktuoja darbų ritmą, o kiekvienas sprendimas priimamas galvojant ir apie būsimą derlių, ir apie žemę, kurioje jis užaugs.",
    "farm_link": "Aplankykite Farmers Circle",
    "read_more": "Skaityti daugiau", "read_less": "Rodyti mažiau",
    "farm_more": [
        "Ūkio laukuose auginami grūdai, daržuose – sezoninės daržovės ir prieskoninės žolelės, ganyklose ganosi angusų veislės galvijai. Ūkio produkciją papildo ekologiški kiaušiniai ir paukštiena, grikiai, avižos bei miltai. Ši įvairovė kuria tarpusavyje susijusią sistemą, kurioje augalininkystė, daržininkystė ir gyvulininkystė papildo viena kitą.",
        "Dalis derliaus įgauna naują pavidalą čia pat, ūkio perdirbimo virtuvėje. Daržovės fermentuojamos, iš jų gaminami padažai, užtepėlės ir pagardai, o sezonų skoniai išsaugomi džemuose, sirupuose bei actuose. Nedidelis atstumas tarp daržo ir gamybos leidžia apdoroti šviežią derlių, išsaugoti jo savitumą ir atrasti vertę net išvaizda netobuluose produktuose.",
        "Rūpestis dirvožemiu jungia visas ūkio veiklas. Regeneracinio ūkininkavimo praktikos – mažiau intensyvus žemės dirbimas, sėjomaina, tarpiniai pasėliai, rotacinis ganymas ir kompostavimas – padeda atkurti jo gyvybingumą ir palaikyti biologinę įvairovę. Organinės liekanos per kompostą sugrįžta į dirvą, maitindamos būsimą derlių. Taip vieno sezono pabaiga tampa kito pradžia.",
        "„Farmers Circle“ – ir susitikimų bei pažinimo vieta. Pats pavadinimas kviečia į bendrą ratą: augintojus, šefus, bendraminčius ir svečius, norinčius suprasti, iš kur atkeliauja jų maistas. Ekskursijos po ūkį, edukacijos ir maisto gaminimo patirtys atveria kasdienį ūkininkavimo pasaulį bei leidžia pažinti darbą, slypintį už kiekvieno ingrediento.",
        "Šį pažinimą pratęsia ūkyje įsikūręs restoranas „Red Brick“, kuriame derlius tampa sezonine gastronomine patirtimi. Renginių ir susitikimų erdvės, nakvynės vieta bei ūkio parduotuvė kviečia pasilikti ilgiau – stebėti, ragauti ir pajusti vietos ritmą.",
    ],
    "farm_close": "Nuo dirvos iki derliaus. Nuo patirties iki žinių, kuriomis dalijamės. Taip sukasi „Farmers Circle“ ratas.",
    "alt_farm": "Ėriukai ganosi Farmers Circle, mūsų regeneraciniame ūkyje",
    "farm_photo_todo": "Nuotrauka: Farmers Circle ūkis",
    "team_over": "Už 14 Horses vadžių stovi",
    "team": [("Aleksandras Fedorovičius", "Virtuvės vadovas"), ("Ela Žoromskė", "Restorano vadovė"), ("Matas Simaitis", "Restorano vadovas")],
    "gallery_label": "Galerija",
    "alt_gallery": ["Taurės prie lango", "Staliukai prie vyno sienos", "Vyno taurė ant serviruoto stalo", "Jaukus salės kampelis"],
    "alt_room": "14 Horses salė",
    "alt_hero": "Staliukas prie lango 14 Horses salėje",
    "alt_mosaic": ["Staliukai prie vyno sienos", "Serviruotas stalas tarp ąžuolo ir plieno", "Vyno taurės ant ąžuolinio stalo"],
    "alt_more": ["Vakarienei serviruotas stalas", "Švelni šviesa virš serviruoto stalo", "Vyno taurės ant ąžuolinio stalo"],
    "credit": "Nuotraukos",
    "events_h3": "Renginiai ir privatūs vakarai",
    "events_body": "Derliaus vakarienės, kviestiniai šefai ir visa salė jūsų progai.",
    "events_link": "Teiraukitės dėl renginių",
    "gift_h3": "Padovanokite vakarą",
    "gift_body": "14 Horses dovanų kuponas bet kokiai sumai nuo 20 iki 1 000 €. Galioja 12 mėn. visuose mūsų restoranuose ir parduotuvėse Senatorių Pasaže.",
    "gift_link": "Pirkti dovanų kuponą",
    "res_h2": "Lauksime prie stalo.",
    "res_when": "Antradieniais - šeštadieniais nuo 17:00 · Dominikonų g. 11, Vilnius",
    "res_groups": '8 ir daugiau asmenų grupių rezervacijos derinamos individualiai - susisiekite su mumis. Prieš rezervuodami susipažinkite su <a href="#policy">restorano taisyklėmis</a>.',
    "res_deposit": "Rezervacijai patvirtinti taikomas 20 € išankstinis mokėjimas kiekvienam asmeniui. Sumokėta suma įskaitoma į galutinę apsilankymo sąskaitą.",
    "res_box_p": "Pasirinkite datą, laiką ir svečių skaičių. Rezervaciją patvirtina 20 € išankstinis mokėjimas asmeniui, kuris įskaitomas į galutinę sąskaitą.",
    "res_note": "Rezervacijos per SevenRooms",
    "contact_h2": "Kontaktai",
    "c_hours": "Darbo valandos", "c_hours_v": "Antradieniais–ketvirtadieniais 17:00–22:00<br>Penktadieniais–šeštadieniais 17:00–23:00",
    "c_phone": "Tel. nr.", "c_email": "El. paštas", "c_social": "Socialiniai tinklai", "c_closed": "Sekmadieniais ir pirmadieniais nedirbame.",
    "aria_main": "Pagrindinis meniu", "aria_footer": "Poraštė", "bib_alt": "MICHELIN gidas 2026",
    "c_write": "Rašykite ar skambinkite", "c_addr": "Adresas", "c_follow": "Sekite sezoną",
    "policy_h2": "Restorano taisyklės", "policy_sub": "Restorano taisyklės ir rezervavimo sąlygos",
    "policy": [
        ("Rezervacijos ir apsilankymo trukmė", "Staliukas rezervuojamas 2 valandoms. Ilgesnė apsilankymo trukmė derinama iš anksto. Rezervuotas staliukas laikomas 15 minučių nuo rezervacijos pradžios. Apie vėlavimą prašome informuoti restorano komandą. Vėluojant ilgiau nei 15 minučių ir apie tai nepranešus, rezervacija atšaukiama."),
        ("Rezervacijos mokestis ir atšaukimo sąlygos", "Rezervacijai patvirtinti taikomas 20 € išankstinis mokėjimas kiekvienam asmeniui. Sumokėta suma įskaitoma į galutinę apsilankymo sąskaitą. Rezervaciją atšaukus likus ne mažiau kaip 24 valandoms iki rezervacijos pradžios, išankstinis mokėjimas grąžinamas. Atšaukus vėliau arba neatvykus, sumokėta suma negrąžinama. Tokia pati atšaukimo ir pinigų grąžinimo tvarka taikoma iš anksto apmokėtoms degustacijoms."),
        ("Grupių rezervacijos", "8 ir daugiau asmenų grupių rezervacijos derinamos individualiai. Grupėms siūloma rinktis patiekalus iš restorano meniu."),
        ("Apsilankymas su vaikais", "Restorane priimami svečiai su vaikais. Suteikiamos vaikiškos kėdutės. Atskiro vaikams skirto meniu nėra."),
        ("Apsilankymas su augintiniais", "Augintiniai priimami restorano vidaus patalpose ir terasoje. Už augintinio priežiūrą ir elgesį atsako jį lydintis asmuo. Augintinis neturi trukdyti kitų svečių patogumui ar restorano darbui."),
        ("Alergijos ir specialūs mitybos poreikiai", "Meniu pritaikymo galimybės ir konkretūs pakeitimai derinami individualiai su restorano komanda."),
        ("Virtuvės darbo laikas", "Antradieniais–ketvirtadieniais virtuvė dirba iki 21:00, penktadieniais ir šeštadieniais – iki 22:00."),
        ("Aprangos rekomendacija", "Rekomenduojamas aprangos stilius – „smart casual“ (laisvalaikio elegancija)."),
        ("Atsiskaitymas ir aptarnavimo mokestis", "Restorane atsiskaitoma tik mokėjimo kortelėmis. Grynieji pinigai nepriimami. Prie galutinės sąskaitos pridedamas 10 % aptarnavimo mokestis."),
    ],
    "f_nav": ["Apie mus", "Meniu", "Farmers Circle", "Renginiai", "Restorano taisyklės", "Kontaktai", "Instagram"],
    "nl_label": "Naujienlaiškis",
    "nl_ph": "Jūsų el. paštas", "nl_btn": "Prenumeruoti",
    "nl_note": "Senatorių Pasažo naujienlaiškis.",
    "nl_ok": "Ačiū!",
    "nl_err": "Įveskite teisingą el. pašto adresą.",
    "privacy": "Privatumo politika",
    "service": "Prie galutinės sąskaitos pridedamas 10 % aptarnavimo mokestis.",
    "ck_title": "Slapukai",
    "ck_text": "Norėtume naudoti slapukus, kad matytume, kaip svečiai naudojasi mūsų svetaine, ir galėtume ją tobulinti, bei rodytume jums aktualias mūsų naujienas „Google“ ir „Meta“ platformose. Pasirinkimą bet kada galite pakeisti skiltyje „Slapukų nustatymai“.",
    "ck_nec": ("Būtini", "Įsimena kalbą ir slapukų pasirinkimą. Visada įjungti."),
    "ck_stat": ("Statistika", "Google Analytics: kaip lankytojai naudojasi svetaine."),
    "ck_mkt": ("Rinkodara", "Google ir Meta: aktualios reklamos rodymas ir jos rezultatų matavimas."),
    "ck_accept": "Priimti visus",
    "ck_reject": "Atmesti visus",
    "ck_settings": "Nustatymai",
    "ck_save": "Išsaugoti pasirinkimą",
    "ck_footer": "Slapukų nustatymai",
    "lang_label": "Kalba",
}

IG_SVG = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.8"/></svg>'
MENU_SVG = ('<svg class="i-open" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 8h18M3 16h12"/></svg>'
            '<svg class="i-close" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>')
NUMS = ["一", "二", "三", "四"]


ARROW_L = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M15 4l-8 8 8 8"/></svg>'
ARROW_R = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M9 4l8 8-8 8"/></svg>'
CLOSE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M5 5l14 14M19 5L5 19"/></svg>'


# Menus, copied word for word from the restaurant's print PDFs (Oct 2026).
# Each item: ("dish", name, description) | ("course", label, description) | ("or",)
MENUS = {
    "en": {
        "tasting": {
            "title": "Tasting Menu",
            "items": [
                ("dish", "Welcome Bread", "Malted sourdough bread, kefir butter"),
                ("dish", "Sardine Crudo", "Cured Baltic sardines, fennel, sea buckthorn, buckwheat croustade"),
                ("dish", "Beef Tartare", "Brioche, Lithuanian beef, hazelnuts, pear, Gammel Knas cheese"),
                ("dish", "Chargrilled Eel", "Smoked and grilled eel, pickled seasonal beetroot, herb yoghurt cream, tomatillo"),
                ("dish", "Chanterelle Croquette", "Salted seasonal cucumber relish, smoked cheese, kohlrabi"),
                ("dish", "Apple &amp; Thyme Sorbet", "Farm-grown apple sorbet, vanilla"),
                ("dish", "Balandėlis", "Savoy cabbage, slow-cooked pork cheek, creamy herb sauce"),
                ("or", "or"),
                ("dish", "Potato &amp; Mushroom Dumpling", "Jerusalem artichoke, potato and porcini espuma, charred leek, black trumpet mushrooms"),
                ("dish", "Carrot &amp; Sea Buckthorn", "Almond mousse, vanilla sponge, sea buckthorn"),
            ],
            "price": "65 €",
            "notes": ["Please inform our staff of any dietary preferences before ordering.", "A 10% service charge is added to the bill."],
        },
        "week": {
            "title": "Gastronomy Week Menu",
            "items": [
                ("course", "Bread", "Dark beer bread, whipped kefir butter"),
                ("course", "Starter", "Smoked eel, Farmers Circle beetroot, tomatillo, smoked cow’s milk cheese"),
                ("course", "Main course", "Slow-braised beef ossobuco, grilled beef heart, seasonal Farmers Circle vegetables"),
                ("course", "Dessert", "Rice, almonds, Madagascar vanilla, cherry jam"),
            ],
            "price": "60 €",
            "notes": ["Please inform our staff of any dietary preferences before ordering."],
        },
    },
    "lt": {
        "tasting": {
            "title": "Degustacinis meniu",
            "items": [
                ("dish", "Duona pasitikimui", "Salyklinė raugo duona, kefyro sviestas"),
                ("dish", "Sardinių crudo", "Sūdytos Baltijos sardinės, pankoliai, šaltalankiai, grikių krepšelis"),
                ("dish", "Jautienos tartaras", "Sviestinė bandelė, lietuviška jautiena, lazdynų riešutai, kriaušė, „Gammel Knas“ sūris"),
                ("dish", "Ant žarijų keptas ungurys", "Rūkytas ir ant žarijų keptas ungurys, marinuoti sezoniniai burokėliai, žolelių jogurto kremas, dumplainiai"),
                ("dish", "Voveraičių kroketas", "Sūdytų sezoninių agurkų pagardas, rūkytas sūris, kaliaropė"),
                ("dish", "Obuolių ir čiobrelių šerbetas", "Ūkio obuolių šerbetas, vanilė"),
                ("dish", "Balandėlis", "Savojinis kopūstas, lėtai troškintas kiaulės žandas, grietinėlės ir žolelių padažas"),
                ("or", "arba"),
                ("dish", "Bulvių virtinis su grybais", "Topinambai, bulvių ir baravykų puta, degintas poras, juodieji trimitėliai"),
                ("dish", "Morkos ir šaltalankiai", "Migdolų putėsiai, vanilinis biskvitas, šaltalankiai"),
            ],
            "price": "65 €",
            "notes": ["Apie mitybos pageidavimus prašome informuoti personalą prieš užsakant.", "Prie sąskaitos pridedamas 10 % aptarnavimo mokestis."],
        },
        "week": {
            "title": "Gastronomijos savaitės meniu",
            "items": [
                ("course", "Duona", "Juoda alaus duona, plaktas kefyro sviestas"),
                ("course", "Užkandis", "Rūkytas ungurys, „Farmers Circle“ ūkio burokėliai, dumplainiai, rūkytas karvės pieno sūris"),
                ("course", "Pagrindinis patiekalas", "Lėtai troškinta jaučio kulninė, grilyje kepta jaučio širdis, sezoninės „Farmers Circle“ ūkio daržovės"),
                ("course", "Desertas", "Ryžiai, migdolai, Madagaskaro vanilė, vyšnių uogienė"),
            ],
            "price": "60 €",
            "notes": ["Apie mitybos pageidavimus prašome informuoti personalą prieš užsakant."],
        },
    },
}
MENU_KEYS = ["tasting", "week", None]  # order matches t["menus"]; None = à la carte (coming soon)


def menu_dialog(t: dict) -> str:
    m = MENUS[t["lang"]]
    tabs, panels = [], []
    for k, key in enumerate(MENU_KEYS[:2]):
        d = m[key]
        sel = "true" if k == 0 else "false"
        tabs.append(f'<button type="button" role="tab" class="mdlg__tab" id="mtab-{key}" aria-controls="mpanel-{key}" aria-selected="{sel}" data-menu-tab="{key}">{t["menus"][k]}</button>')
        rows = []
        for it in d["items"]:
            if it[0] == "or":
                rows.append(f'        <li class="mdlg__or">{it[1]}</li>')
            else:
                kind, name, desc = it
                rows.append(f'        <li class="mdlg__item mdlg__item--{kind}"><h3>{name}</h3><p>{desc}</p></li>')
        notes = "".join(f"<p>{n}</p>" for n in d["notes"])
        panels.append(
            f'    <section class="mdlg__card" role="tabpanel" id="mpanel-{key}" aria-labelledby="mtab-{key}" data-menu-panel="{key}"{"" if k == 0 else " hidden"}>\n'
            f'      <img class="mdlg__logo" src="/assets/logo.png" alt="" width="70" height="86">\n'
            f'      <h2 class="mdlg__title">{d["title"]}</h2>\n'
            f'      <ul class="mdlg__list">\n' + "\n".join(rows) + '\n      </ul>\n'
            f'      <p class="mdlg__price">{d["price"]}</p>\n'
            f'      <div class="mdlg__notes">{notes}</div>\n'
            f'    </section>')
    return (f'<div class="mdlg" data-menu-dialog hidden role="dialog" aria-modal="true" aria-label="{t["menu_h2"]}">\n'
            f'  <div class="mdlg__scroll">\n'
            f'    <div class="mdlg__tabs" role="tablist">{"".join(tabs)}</div>\n'
            + "\n".join(panels) +
            f'\n  </div>\n'
            f'  <button type="button" class="soon__close mdlg__close" data-menu-close aria-label="{t["close"]}">{CLOSE_SVG}</button>\n'
            f'</div>')


def ph(s: str) -> str:
    """Mark [[placeholders]] so they are visible until filled."""
    return re.sub(r"\[\[(.+?)\]\]", r'<span class="todo" title="Placeholder - replace before launch">[\1]</span>', s)


def _nb(v):
    """Keep ' - ' joined to the word before it, so no line starts with a hyphen."""
    if isinstance(v, str): return v.replace(" - ", "\u00a0- ").replace(" – ", "\u00a0– ")
    if isinstance(v, list): return [_nb(x) for x in v]
    if isinstance(v, tuple): return tuple(_nb(x) for x in v)
    return v


def _ver():
    import hashlib
    return {f: hashlib.md5((ROOT / "assets" / f).read_bytes()).hexdigest()[:8]
            for f in ("style.css", "main.js", "ui.js", "consent.js")}


def page(t: dict) -> str:
    global VER
    VER = _ver()
    t = {k: _nb(v) for k, v in t.items()}
    nav_ids = ["about", "menu", "farmers-circle", "events", "policy", "contact"]
    soon_btns = lambda cls: "".join(
        (f'<button type="button" class="{cls}" data-menu="{key}">{m}</button>' if key else
         f'<button type="button" class="{cls}" data-soon>{m}</button>')
        for m, key in zip(t["menus"], MENU_KEYS))
    nav = "\n".join(
        (f'          <div class="nav__item nav__item--menu"><button type="button" class="nav__menu-btn" aria-haspopup="true">{l}</button>'
         f'<div class="nav__sub">{soon_btns("nav__subitem")}</div></div>') if i == "menu"
        else f'          <a href="#{i}">{l}</a>' for i, l in zip(nav_ids, t["nav"]))
    en_cur = 'aria-current="true"' if t["lang"] == "en" else ""
    lt_cur = 'aria-current="true"' if t["lang"] == "lt" else ""
    strip = "\n".join(f"        <div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in t["strip"][:2])
    a3, b3 = t["strip"][2]
    bib = (f'<img class="bib" src="{BIB_LOGO}" alt="{t['bib_alt']}" width="56" height="56">' if BIB_LOGO
           else '<span class="bib bib--todo" role="img" aria-label="MICHELIN Bib Gourmand 2026"><span class="todo">[Bib Gourmand logo]</span></span>')
    strip += f'\n        <div class="strip__award">{bib}<div><dt>{a3}</dt><dd>{b3}</dd></div></div>'
    about_body = "\n".join(
        (f'          <p class="motto">{p[1:]}</p>' if p.startswith("!") else f"          <p>{p}</p>") for p in t["about_body"])
    farm_first = f"          <p>{t['farm_more'][0]}</p>"
    farm_more = "\n".join(f"            <p>{p}</p>" for p in t["farm_more"][1:])
    tel = "tel:" + CONTACT["phone"].replace(" ", "")
    steps = "\n".join(
        f'        <li><span class="num" aria-hidden="true">{n}</span><span class="lbl">{a}</span><span class="name">{b}</span><span class="dish">{ph(t["dish"])}</span></li>'
        for n, (a, b) in zip(NUMS, t["steps"]))
    team = "\n".join(
        f'      <div class="person"><div class="frame r{k+1}" aria-hidden="true"></div><div><span class="person__name">{ph(n)}</span><span class="person__role">{r}</span></div></div>'
        for k, (n, r) in enumerate(t["team"]))
    gal = "\n".join(
        f'        <li class="carousel__slide frame"><img src="{PHOTOS["g"+str(k+1)]}" alt="{a}" loading="lazy" decoding="async"></li>'
        for k, a in enumerate(t["alt_gallery"] + t["alt_more"]))
    farm_all = "\n".join(f"            <p>{p}</p>" for p in t["farm_more"])
    mosaic = "\n".join(
        f'    <div class="frame m{k+1}"><img src="{PHOTOS["m"+str(k+1)]}" alt="{a}" loading="lazy" decoding="async"></div>'
        for k, a in enumerate(t["alt_mosaic"]))
    policy = "\n".join(
        f'          <details{" open" if k == 0 else ""}><summary>{q}</summary><p>{ph(a)}</p></details>'
        for k, (q, a) in enumerate(t["policy"]))
    f_ids = ["about", "soon", "farmers-circle", "events", "policy", "contact", CONTACT["instagram_url"]]
    f_nav = "\n".join(
        (f'        <a href="#" data-menu="tasting">{l}</a>' if i == "soon" else
         f'        <a href="{i if i.startswith("http") else "#" + i}"{" rel=\"noopener\" target=\"_blank\"" if i.startswith("http") else ""}>{l}</a>')
        for i, l in zip(f_ids, t["f_nav"]))
    canonical = SITE_URL + t["home"]
    alt_lang = "lt" if t["lang"] == "en" else "en"
    alt_url = SITE_URL + t["other_home"]
    mail = CONTACT["email"]; phone = CONTACT["phone"]
    fc = CONTACT["farmers_circle_url"]
    farm_img = (f'    <div class="frame r3"><img src="{PHOTOS["farm"]}" alt="{t["alt_farm"]}" loading="lazy" decoding="async"></div>' if PHOTOS["farm"]
                else f'    <div class="frame r3" style="display:flex;align-items:flex-end;padding:20px;font-size:14px;color:#3A352F" role="img" aria-label="{t["alt_farm"]}"><span class="todo">[{t["farm_photo_todo"]}]</span></div>')
    farm_link = f'      <a class="link" href="{fc}" rel="noopener" target="_blank">{t["farm_link"]}</a>\n' if fc else ""

    ck = lambda k: f'<label class="consent__opt"><input type="checkbox" name="{k}"><span><b>{t["ck_" + {"analytics": "stat", "marketing": "mkt"}[k]][0]}</b><small>{t["ck_" + {"analytics": "stat", "marketing": "mkt"}[k]][1]}</small></span></label>'
    consent = f"""<div class="consent" data-consent hidden role="dialog" aria-label="{t['ck_title']}">
  <div class="consent__box">
    <p class="consent__text">{t['ck_text']}</p>
    <div class="consent__prefs" data-consent-prefs hidden>
      <label class="consent__opt"><input type="checkbox" checked disabled><span><b>{t['ck_nec'][0]}</b><small>{t['ck_nec'][1]}</small></span></label>
      {ck('analytics')}
      {ck('marketing')}
    </div>
    <div class="consent__actions">
      <button type="button" class="btn" data-consent-action="reject">{t['ck_reject']}</button>
      <button type="button" class="btn" data-consent-action="accept">{t['ck_accept']}</button>
      <button type="button" class="consent__link" data-consent-action="settings">{t['ck_settings']}</button>
      <button type="button" class="consent__link" data-consent-action="save" hidden>{t['ck_save']}</button>
    </div>
  </div>
</div>"""

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
<link rel="preload" href="/assets/fonts/ZillaSlab-500-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/Karla.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css?v={VER['style.css']}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Restaurant","name":"14 Horses","url":"{SITE_URL}/","image":"{SITE_URL}{PHOTOS['hero_a']}","address":{{"@type":"PostalAddress","streetAddress":"Dominikonų g. 11","addressLocality":"Vilnius","addressCountry":"LT"}},"telephone":"+37061250845","email":"14horses@bfr.lt","openingHoursSpecification":[{{"@type":"OpeningHoursSpecification","dayOfWeek":["Tuesday","Wednesday","Thursday"],"opens":"17:00","closes":"22:00"}},{{"@type":"OpeningHoursSpecification","dayOfWeek":["Friday","Saturday"],"opens":"17:00","closes":"23:00"}}],"servesCuisine":"Baltic, Scandinavian","acceptsReservations":"True"}}
</script>
</head>
<body>
<a class="skip" href="#main">{t['skip']}</a>

<header class="site-header">
  <nav class="wrap nav" aria-label="{t['aria_main']}">
    <a class="nav__logo" href="{t['home']}"><img src="/assets/logo.png" alt="14 Horses" width="140" height="171"></a>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="{t['menu_open']}">{MENU_SVG}<span aria-hidden="true">{t['menu_btn']}</span></button>
    <div class="nav__links" id="nav-links">
{nav}
      <span class="nav__lang" aria-label="{t['lang_label']}"><a href="/lt/" hreflang="lt" lang="lt" {lt_cur}>LT</a> / <a href="/" hreflang="en" lang="en" {en_cur}>EN</a></span>
      <a class="btn" href="{SEVENROOMS_URL}" rel="noopener" target="_blank">{t['reserve']}</a>
    </div>
  </nav>
</header>

<main id="main">
  <section id="about" class="hero">
    <img class="hero__bg" src="{PHOTOS['hero']}" alt="{t['alt_hero']}" fetchpriority="high">
    <div class="wrap hero__inner">
      <div class="hero__text">
        <p class="overline">{t['hero_over']}</p>
        <h1>{t['hero_h1']}</h1>
        <p class="hero__lead">{t['hero_lead']}</p>
        <div class="hero__ctas">
          <a id="sevenrooms-trigger" class="btn btn--light" href="{SEVENROOMS_URL}" rel="noopener" target="_blank">{t['reserve']}</a>
          <button type="button" class="link link--btn" data-menu="tasting">{t['hero_menu']}</button>
        </div>
      </div>
    </div>
  </section>

  <section class="strip" aria-label="{t['strip'][0][0]}">
    <dl class="wrap">
{strip}
    </dl>
  </section>

  <section id="farmers-circle" class="farm-section">
    <div class="banner banner--full">
      <img class="banner__bg" src="{PHOTOS['farm']}" alt="{t['alt_farm']}" loading="lazy" decoding="async">
      <div class="wrap banner__inner banner__inner--left">
        <p class="overline banner__over">{t['farm_over']}</p>
        <h2 class="banner__title">{t['farm_h2']}</h2>
        <p class="banner__text">{t['farm_body']}</p>
      </div>
    </div>
    <div class="wrap farm-more">
      <div class="farm-more__body">
        <div class="farm-more__cols">
{farm_all}
        </div>
      </div>
{farm_link}    </div>
  </section>

  <section id="events" class="wrap banner-wrap">
    <div class="banner">
      <img class="banner__bg" src="{PHOTOS['m1']}" alt="{t['alt_mosaic'][0]}" loading="lazy" decoding="async">
      <div class="banner__inner">
        <h2 class="banner__title">{t['events_h3']}</h2>
        <p class="banner__text">{t['events_body']}</p>
        <a class="link" href="mailto:{CONTACT['email']}">{t['events_link']}: {CONTACT['email']}</a>
      </div>
    </div>
  </section>

  <section class="wrap banner-wrap">
    <div class="banner">
      <img class="banner__bg" src="{PHOTOS['m2']}" alt="{t['alt_mosaic'][1]}" loading="lazy" decoding="async">
      <div class="banner__inner">
        <h2 class="banner__title">{t['gift_h3']}</h2>
        <p class="banner__text">{t['gift_body']}</p>
        <a class="link" href="https://www.senatoriupasazas.lt/#vouchers" rel="noopener" target="_blank">{t['gift_link']}</a>
      </div>
    </div>
  </section>

  <section class="wrap carousel" aria-label="{t['gallery_label']}" data-carousel>
    <button type="button" class="carousel__btn carousel__btn--prev" data-dir="-1" aria-label="{t['prev']}">{ARROW_L}</button>
    <ul class="carousel__track">
{gal}
    </ul>
    <button type="button" class="carousel__btn carousel__btn--next" data-dir="1" aria-label="{t['next']}">{ARROW_R}</button>
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
      <div><span class="label">{t['c_phone']}</span><a href="{tel}">{phone}</a></div>
      <div><span class="label">{t['c_email']}</span><a href="mailto:{mail}">{mail}</a></div>
      <div><span class="label">{t['c_hours']}</span><span>{t['c_hours_v']}</span><span class="muted">{t['c_closed']}</span></div>
      <div><span class="label">{t['c_social']}</span><a class="ig" href="{CONTACT['instagram_url']}" rel="noopener" target="_blank">{IG_SVG}<span>{CONTACT['instagram_handle']}</span></a></div>
      <div><span class="label">{t['c_addr']}</span><a href="{CONTACT['maps']}" rel="noopener" target="_blank">{CONTACT['address']}<br>Senatorių Pasažas</a></div>
    </div>
  </section>

</main>

<footer>
  <div class="wrap footer">
    <address>
      <span class="footer__name">14 Horses</span>
      <span>{CONTACT['address']}</span>
      <span>Senatorių Pasažas</span>
    </address>
    <nav aria-label="{t['aria_footer']}">
{f_nav}
    </nav>
    <form class="newsletter" action="{MAILERLITE_URL}" method="post" target="_blank" data-ok="{t['nl_ok']}" data-err="{t['nl_err']}">
      <label for="nl">{t['nl_label']}</label>
      <div class="newsletter__row">
        <input id="nl" type="email" name="fields[email]" required autocomplete="email" placeholder="{t['nl_ph']}">
        <button class="btn" type="submit">{t['nl_btn']}</button>
      </div>
      <input type="hidden" name="ml-submit" value="1">
      <p class="newsletter__note">{t['nl_note']}</p>
      <p class="newsletter__status" role="status" aria-live="polite" hidden></p>
    </form>
  </div>
  <div class="wrap">
    <div class="footer__bottom">
    <span>© <span data-year>2026</span> 14 Horses · {t['credit']}: {PHOTO_CREDIT}</span>
    <span>{t['service']}</span>
    <button type="button" class="footer__cookies" data-consent-open>{t['ck_footer']}</button>
    </div>
  </div>
</footer>

<div class="bookbar"><a class="btn" href="{SEVENROOMS_URL}" rel="noopener" target="_blank">{t['reserve']}</a></div>

{consent}
<div class="soon" data-soon-dialog hidden role="dialog" aria-modal="true" aria-label="{t['soon']}">
  <img class="soon__bg" src="{PHOTOS['g6']}" alt="" loading="lazy" decoding="async">
  <p class="soon__text">{t['soon']}</p>
  <button type="button" class="soon__close" data-soon-close aria-label="{t['close']}">{CLOSE_SVG}</button>
</div>
{menu_dialog(t)}
<script src="/assets/main.js?v={VER['main.js']}" defer></script>
<script src="/assets/ui.js?v={VER['ui.js']}" defer></script>
<script src="/assets/consent.js?v={VER['consent.js']}" defer></script>
</body>
</html>
"""


def extras():
    """robots.txt, sitemap.xml and a two-language 404 page."""
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    alt = (f'<xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}/"/>'
           f'<xhtml:link rel="alternate" hreflang="lt" href="{SITE_URL}/lt/"/>'
           f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/"/>')
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f'  <url><loc>{SITE_URL}/</loc>{alt}</url>\n'
        f'  <url><loc>{SITE_URL}/lt/</loc>{alt}</url>\n'
        '</urlset>\n', encoding="utf-8")
    v = _ver()
    (ROOT / "404.html").write_text(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>14 Horses - Page not found</title>
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/assets/style.css?v={v['style.css']}">
</head>
<body>
<main class="wrap notfound">
  <a href="/"><img src="/assets/logo.png" alt="14 Horses" width="140" height="171" style="height:96px;width:auto"></a>
  <h1>Page not found</h1>
  <p class="muted">The page may have moved with our new website.</p>
  <p><a class="link" href="/">Go to the front page</a></p>
  <h1 lang="lt">Puslapis nerastas</h1>
  <p class="muted" lang="lt">Puslapis galėjo būti perkeltas į naują mūsų svetainę.</p>
  <p lang="lt"><a class="link" href="/lt/">Eiti į pagrindinį puslapį</a></p>
</main>
</body>
</html>
""", encoding="utf-8")


def main():
    (ROOT / "index.html").write_text(page(EN), encoding="utf-8")
    (ROOT / "lt").mkdir(exist_ok=True)
    (ROOT / "lt" / "index.html").write_text(page(LT), encoding="utf-8")
    extras()
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
    b = re.sub(r'<script src="/assets/(main|consent|ui)\.js(\?v=\w+)?" defer></script>\s*', "", b)
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
    b = re.sub(r'<form class="newsletter" action="[^"]*" method="post" target="_blank"', '<form class="newsletter"', b)
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
  else {
    var saved = null;
    try { saved = localStorage.getItem(KEY); } catch (e) {}
    var langs = navigator.languages || [navigator.language || ''];
    start = saved || (/^lt\b/i.test(langs[0] || '') ? 'lt' : 'en');
  }
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
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var st = f.querySelector('.newsletter__status');
      st.hidden = false;
      st.textContent = document.documentElement.lang === 'lt'
        ? 'Juodraštis: prenumerata veiks tikroje svetainėje.'
        : 'Draft preview: sign-up works on the live site.';
    });
  });
  document.querySelectorAll('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
"""


def build_artifact():
    logo_uri = "data:image/png;base64," + base64.b64encode((ROOT / "assets" / "logo.png").read_bytes()).decode()
    css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8").replace("url('/assets/fonts/", "url('assets/fonts/") + ARTIFACT_CSS
    draft = ('<div class="draftbar"><div class="wrap"><span><b>Draft</b> · 14horses.lt redesign · not public</span>'
             '<span>Text in [brackets] still needs real content</span></div></div>')
    html_out = f"""<title>14horses Website</title>
<meta name="claude:viewport-fit-sides" content="cover">
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
<script>{(ROOT / "assets" / "ui.js").read_text(encoding="utf-8")}</script>
<script>{(ROOT / "assets" / "consent.js").read_text(encoding="utf-8")}</script>
"""
    out = pathlib.Path(__file__).resolve().parent / "artifact"
    out.mkdir(exist_ok=True)
    (out / "14horses.html").write_text(html_out, encoding="utf-8")
    print("artifact built", out / "14horses.html")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "artifact":
        build_artifact()
