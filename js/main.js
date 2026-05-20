const DMG_URL = 'https://github.com/ziarnooo/tnn-website/releases/latest/download/TNN.dmg';

// ── Scroll-reveal ─────────────────────────────────────────────
const revealObserver = new IntersectionObserver(
  (entries) => entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  }),
  { threshold: 0.08, rootMargin: '0px 0px -32px 0px' }
);

document.querySelectorAll('.reveal').forEach((el) => revealObserver.observe(el));

document.querySelectorAll('#hero .reveal').forEach((el, i) => {
  setTimeout(() => {
    el.classList.add('visible');
    revealObserver.unobserve(el);
  }, 100 + i * 140);
});

// ── Nav scroll shadow ─────────────────────────────────────────
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('nav--scrolled', window.scrollY > 12);
}, { passive: true });

// ── Modal helpers ─────────────────────────────────────────────
function openModal(id) {
  closeAllModals();
  const overlay = document.getElementById(id);
  overlay.classList.add('modal-overlay--open');
  document.body.style.overflow = 'hidden';
  const input = overlay.querySelector('input');
  if (input) setTimeout(() => input.focus(), 300);
}

function closeAllModals() {
  document.querySelectorAll('.modal-overlay--open').forEach((el) => {
    el.classList.remove('modal-overlay--open');
  });
  document.body.style.overflow = '';
}

document.querySelectorAll('[data-modal-close]').forEach((btn) =>
  btn.addEventListener('click', closeAllModals)
);

document.querySelectorAll('.modal-overlay').forEach((overlay) => {
  overlay.addEventListener('click', (e) => { if (e.target === overlay) closeAllModals(); });
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeAllModals();
});

// ── Download buttons ──────────────────────────────────────────
const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

function trackEvent(name, params) {
  if (typeof window.gtag === 'function') {
    window.gtag('event', name, params || {});
  }
}

document.querySelectorAll('[data-modal-open]').forEach((btn) => {
  btn.addEventListener('click', () => {
    if (isMobile) {
      trackEvent('download_intent_mobile', {
        file_name: 'TNN.dmg',
        platform: 'mobile',
      });
      openModal('mobile-modal');
    } else {
      if (DMG_URL) {
        trackEvent('file_download', {
          file_name: 'TNN.dmg',
          file_extension: 'dmg',
          link_url: DMG_URL,
          platform: 'desktop',
        });
        const a = document.createElement('a');
        a.href = DMG_URL;
        a.download = 'TNN.dmg';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
      openModal('install-modal');
    }
  });
});

// Mobile email collection is handled by the MailerLite embedded form (#mobile-modal).
