/* 14horses — site behaviour */
(function () {
  // ----- SevenRooms -----
  // Set VENUE_ID to the venue slug from SevenRooms (Manager > Widget settings).
  // Example: 'fourteenhorses'. While empty, the button links to the contact section.
  var SEVENROOMS = { VENUE_ID: '', CLIENT_TOKEN: '' };

  // Mobile menu
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav__toggle');
  if (header && toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    header.querySelectorAll('.nav__links a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // SevenRooms booking widget
  var trigger = document.getElementById('sevenrooms-trigger');
  if (trigger && SEVENROOMS.VENUE_ID) {
    trigger.setAttribute('href', 'https://www.sevenrooms.com/reservations/' + SEVENROOMS.VENUE_ID);
    var s = document.createElement('script');
    s.src = 'https://www.sevenrooms.com/widget/embed.js';
    s.async = true;
    s.onload = function () {
      if (window.SevenroomsWidget) {
        window.SevenroomsWidget.init({
          venueId: SEVENROOMS.VENUE_ID,
          triggerId: 'sevenrooms-trigger',
          type: 'reservations',
          styleButton: false,
          clientToken: SEVENROOMS.CLIENT_TOKEN
        });
      }
    };
    document.head.appendChild(s);
  }

  // Footer year
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
