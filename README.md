# 14horses.com - new website (Wabi Sabi)

Static site, no framework. English at `/`, Lithuanian at `/lt/`.

## Structure
- `site/` - the deployable site (point hosting/Vercel at this folder)
  - `index.html` (EN), `lt/index.html` (LT) - generated, do not edit by hand
  - `assets/style.css` - all styling; colour/typography tokens at the top
  - `assets/main.js` - mobile menu + SevenRooms widget
  (`vercel.json` in the repo root serves `site/` with clean URLs + caching)
- `build/build.py` - all page text (EN + LT) and settings. Edit text here, then run `python3 build/build.py`.

## Before launch
0. **Remove the `X-Robots-Tag: noindex` header** from `vercel.json` when the site moves to 14horses.com (it keeps the test version out of Google).
1. **Menu**: the menu section shows a placeholder until the chef's menu is ready (`dish` text in `build/build.py`).
2. **Team portraits**: the three portrait frames are empty until photos arrive.
3. **Privacy policy**: the `#privacy` links need a real page or URL.
4. **SevenRooms**: the "Reserve a table" button links to the 14Horses SevenRooms booking page
   (`SEVENROOMS_URL` in `build/build.py`). The embedded widget in `assets/main.js` stays off unless `VENUE_ID` is set.
5. **Newsletter**: the footer form posts to MailerLite form `h8a6e9` (Senatorių Pasažas list).

## Draft preview (artifact)
`python3 build/build.py artifact` writes `build/artifact/14horses.html`: one self-contained page with an EN/LT switch,
used as the shared draft while content is collected. Publish it together with `site/assets/img/*` (referenced as `assets/img/...`).
