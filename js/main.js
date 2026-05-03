const SEND_LINK_ENDPOINT = 'https://submit-formspark.io/f/YOUR_FORM_ID';
const DMG_URL = ''; // set to the .dmg URL when ready

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

document.querySelectorAll('[data-modal-open]').forEach((btn) => {
  btn.addEventListener('click', () => {
    if (isMobile) {
      openModal('mobile-modal');
    } else {
      if (DMG_URL) {
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

// ── Mobile: send download link form ──────────────────────────
const sendLinkForm    = document.getElementById('send-link-form');
const sendLinkSuccess = document.getElementById('send-link-success');

sendLinkForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const emailInput = document.getElementById('send-link-email');
  const email = emailInput.value.trim();

  if (!email || !email.includes('@')) {
    emailInput.classList.add('modal__input--error');
    emailInput.focus();
    setTimeout(() => emailInput.classList.remove('modal__input--error'), 2200);
    return;
  }

  const submitBtn = sendLinkForm.querySelector('[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Sending…';

  try {
    await fetch(SEND_LINK_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, type: 'send-link' }),
    });
  } catch {
    // show success regardless
  }

  sendLinkForm.style.display = 'none';
  sendLinkSuccess.style.display = 'block';
});
