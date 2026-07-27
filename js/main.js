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

// ── Download flow (2026-07-27): email gates the download ──────
// Desktop: CTA → #gate-modal (email required) → submit saves the email and
// redirects to /thanks.html?dl=1 — the DMG download starts THERE (an install
// page nothing can interrupt).
// Backend = a plain Google Form (no Apps Script, no extra permissions):
//   1. forms.new → one question: "Email", type Short answer, required
//   2. Send → link icon → copy the form link and give it to Claude
//      (we extract the entry ID and fill both constants below), or:
//      three dots → "Get pre-filled link" → fill any email → Copy link —
//      the URL contains "entry.XXXXXXXX=", that's TNN_FORM_ENTRY, and
//      TNN_FORM_ACTION is the form URL with /viewform → /formResponse.
//   Answers land in the form's Responses tab (linkable to a Sheet).
const TNN_FORM_ACTION = 'https://docs.google.com/forms/d/e/1FAIpQLSececSE0m02PtMMgQWWQffCOLDrGjijvJJNN1xyv614-YZ5iQ/formResponse';
const TNN_FORM_ENTRY  = 'entry.473938292';

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
      trackEvent('download_intent_desktop', { platform: 'desktop' });
      openModal('gate-modal');
    }
  });
});

const gateForm = document.getElementById('gate-form');
if (gateForm) {
  gateForm.addEventListener('submit', (ev) => {
    ev.preventDefault();
    const email = (document.getElementById('gate-input').value || '').trim();
    if (!email) return;

    // 1) save the lead (fire-and-forget; never blocks the download)
    if (TNN_FORM_ACTION && TNN_FORM_ENTRY) {
      const data = new URLSearchParams();
      data.append(TNN_FORM_ENTRY, email);
      fetch(TNN_FORM_ACTION, { method: 'POST', mode: 'no-cors', body: data }).catch(() => {});
    }
    try { localStorage.setItem('tnn-beta-email', email); } catch (e) {}
    trackEvent('generate_lead', { method: 'download-gate' });
    trackEvent('file_download', {
      file_name: 'TNN.dmg',
      file_extension: 'dmg',
      link_url: DMG_URL,
      platform: 'desktop',
    });

    // 2) hand over to /thanks — the download itself starts there (?dl=1),
    //    so no navigation can cancel it
    window.location.href = '/thanks.html?dl=1';
  });
}

// Mobile email collection is handled by the MailerLite embedded form (#mobile-modal).
