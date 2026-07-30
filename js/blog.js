// Blog chrome: theme toggle + nav shadow.
// The homepage keeps this logic inline; blog pages share this file instead.
// CTA modals come from js/main.js, which every blog page also loads.
(function () {
  var KEY = 'tnn-theme';
  var root = document.documentElement;
  var mql = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  var effective = stored ? stored : (mql && mql.matches ? 'dark' : 'light');
  if (effective === 'dark') root.setAttribute('data-theme', 'dark');

  var btn = document.querySelector('[data-theme-toggle]');
  if (btn) {
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      if (next === 'dark') root.setAttribute('data-theme', 'dark');
      else root.removeAttribute('data-theme');
      try { localStorage.setItem(KEY, next); } catch (e) {}
    });
  }

  var nav = document.getElementById('nav');
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('nav--scrolled', window.scrollY > 12);
    }, { passive: true });
  }
})();
