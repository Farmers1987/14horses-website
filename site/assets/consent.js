/* 14horses - cookie consent
 *
 * Nothing that tracks is loaded until the visitor has said yes.
 *  - Statistics  -> Google Analytics 4
 *  - Marketing   -> Meta Pixel and Google Ads (via Google Tag Manager)
 *
 * Fill in the IDs below when the accounts are ready. Use EITHER GTM_ID
 * (and set up GA4 / Meta inside Tag Manager) OR GA4_ID + META_PIXEL_ID
 * directly - not both, or visits are counted twice.
 *
 * Inside Tag Manager: GA4 tags must require "analytics_storage", Meta and
 * Google Ads tags must require "ad_storage" (Consent settings on each tag).
 * Tag Manager itself is only loaded after the visitor accepts at least one
 * category, so before that nothing is sent to Google or Meta.
 *
 * The choice is stored in localStorage ('14horses-consent') for 12 months,
 * then the banner is shown again. Footer link "Cookie settings" reopens it.
 */
(function () {
  var CONFIG = {
    GTM_ID: '',          // e.g. 'GTM-XXXXXXX'
    GA4_ID: 'G-J0VGWZH8FD', // Google Analytics 4 (14 Horses)
    META_PIXEL_ID: ''    // e.g. '123456789012345' (only if not using GTM)
  };
  var KEY = '14horses-consent';
  var VERSION = 1;
  var MAX_AGE = 365 * 24 * 60 * 60 * 1000;

  // ----- storage -----
  function read() {
    try {
      var c = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (!c || c.v !== VERSION || !c.ts || Date.now() - c.ts > MAX_AGE) return null;
      return c;
    } catch (e) { return null; }
  }
  function write(c) {
    c.v = VERSION; c.ts = Date.now();
    try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {}
    return c;
  }

  // ----- Google consent mode (only matters once a Google tag is loaded) -----
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  gtag('consent', 'default', {
    analytics_storage: 'denied', ad_storage: 'denied',
    ad_user_data: 'denied', ad_personalization: 'denied',
    functionality_storage: 'granted', security_storage: 'granted',
    wait_for_update: 500
  });

  function addScript(src) {
    var s = document.createElement('script');
    s.async = true; s.src = src;
    document.head.appendChild(s);
  }

  var loaded = {};
  function apply(c) {
    gtag('consent', 'update', {
      analytics_storage: c.analytics ? 'granted' : 'denied',
      ad_storage: c.marketing ? 'granted' : 'denied',
      ad_user_data: c.marketing ? 'granted' : 'denied',
      ad_personalization: c.marketing ? 'granted' : 'denied'
    });

    if (CONFIG.GTM_ID && (c.analytics || c.marketing) && !loaded.gtm) {
      loaded.gtm = true;
      window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
      addScript('https://www.googletagmanager.com/gtm.js?id=' + CONFIG.GTM_ID);
    }
    if (CONFIG.GA4_ID && !CONFIG.GTM_ID && c.analytics && !loaded.ga4) {
      loaded.ga4 = true;
      gtag('js', new Date());
      gtag('config', CONFIG.GA4_ID);
      addScript('https://www.googletagmanager.com/gtag/js?id=' + CONFIG.GA4_ID);
    }
    if (CONFIG.META_PIXEL_ID && !CONFIG.GTM_ID && c.marketing && !loaded.meta) {
      loaded.meta = true;
      /* Meta Pixel base code */
      !function (f, b, e, v, n, t, s) {
        if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
        if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
        t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
      }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      window.fbq('init', CONFIG.META_PIXEL_ID);
      window.fbq('track', 'PageView');
    }
    window.dispatchEvent(new CustomEvent('consentchange', { detail: c }));
  }

  // Remove tracking cookies left from an earlier "yes".
  function clearCookies() {
    var names = document.cookie.split(';').map(function (s) { return s.split('=')[0].trim(); });
    var host = location.hostname.split('.');
    var domains = [''];
    for (var i = 0; i < host.length - 1; i++) domains.push('; domain=.' + host.slice(i).join('.'));
    names.forEach(function (n) {
      if (/^(_ga|_gid|_gat|_gcl|_fbp|_fbc|_uet|IDE|test_cookie)/.test(n)) {
        domains.forEach(function (d) { document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + d; });
      }
    });
  }

  // ----- banner -----
  var banners = document.querySelectorAll('[data-consent]');
  function show(withPrefs) {
    var c = read() || { analytics: false, marketing: false };
    banners.forEach(function (b) {
      b.hidden = false;
      b.querySelectorAll('input[name="analytics"]').forEach(function (i) { i.checked = !!c.analytics; });
      b.querySelectorAll('input[name="marketing"]').forEach(function (i) { i.checked = !!c.marketing; });
      setPrefs(b, !!withPrefs);
    });
    document.documentElement.classList.add('consent-open');
  }
  function hide() {
    banners.forEach(function (b) { b.hidden = true; });
    document.documentElement.classList.remove('consent-open');
  }
  function setPrefs(b, open) {
    var p = b.querySelector('[data-consent-prefs]');
    if (p) p.hidden = !open;
    b.querySelectorAll('[data-consent-action="settings"]').forEach(function (x) { x.hidden = open; });
    b.querySelectorAll('[data-consent-action="save"]').forEach(function (x) { x.hidden = !open; });
  }
  function decide(next) {
    var prev = read();
    write(next);
    hide();
    var withdrew = prev && ((prev.analytics && !next.analytics) || (prev.marketing && !next.marketing));
    if (withdrew) { clearCookies(); location.reload(); return; }
    apply(next);
  }

  document.addEventListener('click', function (e) {
    var open = e.target.closest('[data-consent-open]');
    if (open) { e.preventDefault(); show(true); return; }
    var btn = e.target.closest('[data-consent-action]');
    if (!btn) return;
    var box = btn.closest('[data-consent]');
    var act = btn.getAttribute('data-consent-action');
    if (act === 'accept') decide({ analytics: true, marketing: true });
    else if (act === 'reject') decide({ analytics: false, marketing: false });
    else if (act === 'settings') setPrefs(box, true);
    else if (act === 'save') decide({
      analytics: !!box.querySelector('input[name="analytics"]:checked'),
      marketing: !!box.querySelector('input[name="marketing"]:checked')
    });
  });

  var saved = read();
  if (saved) apply(saved); else show(false);
})();
