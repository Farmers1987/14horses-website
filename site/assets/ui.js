/* 14horses - photo carousel, "Coming soon" window for the menus */
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
    d.hidden = false;
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
    document.querySelectorAll('[data-soon-dialog]').forEach(function (d) { d.hidden = true; });
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
})();
