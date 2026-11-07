/* 14horses - photo carousel, menu window, "Coming soon" window (à la carte) */
(function () {
  // ----- Carousel: three photos at a time, arrows move one photo -----
  document.querySelectorAll('[data-carousel]').forEach(function (c) {
    var track = c.querySelector('.carousel__track');
    var prev = c.querySelector('[data-dir="-1"]');
    var next = c.querySelector('[data-dir="1"]');
    function step() {
      var s = track.querySelector('.carousel__slide');
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      return s ? s.getBoundingClientRect().width + gap : track.clientWidth;
    }
    [prev, next].forEach(function (b) {
      b.addEventListener('click', function () {
        var dir = Number(b.getAttribute('data-dir'));
        var max = track.scrollWidth - track.clientWidth;
        var target = track.scrollLeft + dir * step();
        // wrap around at the ends
        if (dir > 0 && track.scrollLeft >= max - 2) target = 0;
        if (dir < 0 && track.scrollLeft <= 2) target = max;
        track.scrollTo({ left: target, behavior: 'smooth' });
      });
    });
  });

  // ----- "Coming soon" window -----
  var lastFocus = null;
  function scope(el) { return el.closest('[data-lang]') || document; }
  function openSoon(from, byKeyboard) {
    var d = scope(from).querySelector('[data-soon-dialog]');
    if (!d) return;
    lastFocus = byKeyboard ? from : null; // only hand focus back for keyboard users
    clearTimeout(d._t);
    d.hidden = false;
    void d.offsetWidth; // let the browser draw the start state, then fade in
    d.classList.add('is-visible');
    document.documentElement.classList.add('soon-open');
    var x = d.querySelector('[data-soon-close]');
    if (x) x.focus();
    // close the mobile menu panel if it is open
    document.querySelectorAll('.site-header.is-open').forEach(function (h) {
      h.classList.remove('is-open');
      var t = h.querySelector('.nav__toggle'); if (t) t.setAttribute('aria-expanded', 'false');
    });
  }
  function closeSoon() {
    document.querySelectorAll('[data-soon-dialog]').forEach(function (d) {
      if (d.hidden) return;
      d.classList.remove('is-visible');
      clearTimeout(d._t);
      d._t = setTimeout(function () { d.hidden = true; }, 450); // after the fade-out
    });
    document.documentElement.classList.remove('soon-open');
    if (lastFocus) { try { lastFocus.focus(); } catch (e) {} }
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-soon]');
    if (b) { e.preventDefault(); openSoon(b, e.detail === 0); return; }
    if (e.target.closest('[data-soon-close]')) { closeSoon(); return; }
    var d = e.target.closest('[data-soon-dialog]');
    if (d && e.target === d) closeSoon();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && document.documentElement.classList.contains('soon-open')) closeSoon();
  });
  // ----- Menus: Tasting / Gastronomy week in one window with two tabs -----
  var menuFocus = null;
  function showTab(d, key) {
    d.querySelectorAll('[data-menu-tab]').forEach(function (b) { b.setAttribute('aria-selected', b.getAttribute('data-menu-tab') === key ? 'true' : 'false'); });
    d.querySelectorAll('[data-menu-panel]').forEach(function (p) { p.hidden = p.getAttribute('data-menu-panel') !== key; });
  }
  function openMenu(from, byKeyboard) {
    var d = document.querySelector('[data-menu-dialog]');
    if (!d) return;
    menuFocus = byKeyboard ? from : null;
    showTab(d, from.getAttribute('data-menu') || 'tasting');
    try { (window.dataLayer = window.dataLayer || []).push({ event: 'menu_open', menu_name: from.getAttribute('data-menu') || 'tasting', page_language: document.documentElement.lang }); } catch (e) {}
    clearTimeout(d._t);
    d.hidden = false;
    d.querySelector('.mdlg__scroll').scrollTop = 0;
    void d.offsetWidth;
    d.classList.add('is-visible');
    document.documentElement.classList.add('menu-open');
    var x = d.querySelector('[data-menu-close]'); if (x) x.focus();
    document.querySelectorAll('.site-header.is-open').forEach(function (h) {
      h.classList.remove('is-open');
      var t = h.querySelector('.nav__toggle'); if (t) t.setAttribute('aria-expanded', 'false');
    });
  }
  function closeMenu() {
    var d = document.querySelector('[data-menu-dialog]');
    if (!d || d.hidden) return;
    d.classList.remove('is-visible');
    clearTimeout(d._t);
    d._t = setTimeout(function () { d.hidden = true; }, 400);
    document.documentElement.classList.remove('menu-open');
    if (menuFocus) { try { menuFocus.focus(); } catch (e) {} }
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-menu]');
    if (b) { e.preventDefault(); openMenu(b, e.detail === 0); return; }
    var tab = e.target.closest('[data-menu-tab]');
    if (tab) { var dd = tab.closest('[data-menu-dialog]'); showTab(dd, tab.getAttribute('data-menu-tab')); dd.querySelector('.mdlg__scroll').scrollTop = 0; return; }
    if (e.target.closest('[data-menu-close]')) { closeMenu(); return; }
    if (e.target.classList && (e.target.matches('[data-menu-dialog]') || e.target.matches('.mdlg__scroll'))) closeMenu();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && document.documentElement.classList.contains('menu-open')) closeMenu();
  });
  // ----- Event pop-up: once a day, after the cookie choice, until the event is over -----
  (function () {
    var p = document.querySelector('[data-promo]');
    if (!p) return;
    var key = 'promo-' + p.getAttribute('data-promo');
    var until = Date.parse(p.getAttribute('data-promo-until'));
    if (!(Date.now() < until)) return;
    var seen = 0;
    try { seen = Number(localStorage.getItem(key)) || 0; } catch (e) {}
    if (Date.now() - seen < 24 * 60 * 60 * 1000) return;
    function mark() { try { localStorage.setItem(key, String(Date.now())); } catch (e) {} }
    function open() {
      if (document.documentElement.classList.contains('menu-open') || document.documentElement.classList.contains('soon-open')) return;
      var img = p.querySelector('.promo__img');
      img.onload = function () {
        p.hidden = false; void p.offsetWidth;
        p.classList.add('is-visible');
        document.documentElement.classList.add('promo-open');
        mark();
      };
      img.src = p.getAttribute('data-promo-img');
    }
    function close() {
      p.classList.remove('is-visible');
      document.documentElement.classList.remove('promo-open');
      setTimeout(function () { p.hidden = true; }, 450);
    }
    p.addEventListener('click', function (e) {
      if (e.target.closest('[data-promo-close]') || e.target === p) close();
      else if (e.target.closest('[data-promo-go]')) { mark(); close(); }
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !p.hidden) close(); });
    // wait until the cookie bar is answered, then show it after a short pause
    function start() {
      if (document.documentElement.classList.contains('consent-open')) {
        window.addEventListener('consentchange', function once() { window.removeEventListener('consentchange', once); setTimeout(open, 600); });
      } else setTimeout(open, 1200);
    }
    if (document.readyState === 'complete') setTimeout(start, 50); else window.addEventListener('load', function () { setTimeout(start, 50); });
  })();
})();
