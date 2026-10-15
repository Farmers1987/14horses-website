# 14horses.com — new website (Wabi Sabi)

Static site, no framework. English at `/`, Lithuanian at `/lt/`.

## Structure
- `site/` — the deployable site (point hosting/Vercel at this folder)
  - `index.html` (EN), `lt/index.html` (LT) — generated, do not edit by hand
  - `assets/style.css` — all styling; colour/typography tokens at the top
  - `assets/main.js` — mobile menu + SevenRooms widget
  - `vercel.json` — clean URLs + caching
- `build/build.py` — all page text (EN + LT) and settings. Edit text here, then run `python3 build/build.py`.

## Before launch
1. **SevenRooms**: set `VENUE_ID` (and `CLIENT_TOKEN` if used) in `assets/main.js`.
2. **Placeholders**: everything shown as `[...]` with a dashed underline. Fill in `build/build.py`:
   prices, dishes, email, phone, Instagram handle + URL, group size, policy texts,
   optional `farmers_circle_url`.
3. **Photos**: shoot photos by G. Rozmanaite are in `site/assets/img/` (credited in the footer). Still missing: portraits of the head chef and restaurant manager.
4. **Logo**: `assets/logo.png` is made from a PNG. Replace with the original vector logo (SVG) if available.
5. **Newsletter + privacy policy**: the sign-up form is not wired to a mailing service yet; `#privacy` needs a page.

## Draft preview (artifact)
`python3 build/build.py artifact` writes `build/artifact/14horses.html`: one self-contained page with an EN/LT switch,
used as the shared draft while content is collected. Publish it together with `site/assets/img/*` (referenced as `assets/img/...`).
