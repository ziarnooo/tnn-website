// Email scanners may open the page; only a deliberate click consumes the Auth link.
const button = document.querySelector('#confirm');
const message = document.querySelector('#message');
let confirmation;
let openApplication;
let recoveryTimer;

function readLink() {
  clearTimeout(recoveryTimer);
  confirmation = null;
  openApplication = null;
  button.disabled = true;
  button.textContent = 'Confirm email';
  try {
    const fragment = location.hash.slice(1);
    // Go's HTML template context may percent-encode a URL nested in a fragment.
    const candidate = new URL(/^https%3a%2f%2f/i.test(fragment) ? decodeURIComponent(fragment) : fragment);
    const redirect = candidate.searchParams.get('redirect_to');
    if (candidate.origin !== 'https://djyimnbupvgbzzdbgsom.supabase.co' || candidate.pathname !== '/auth/v1/verify' ||
        candidate.username || candidate.password ||
        !['signup', 'magiclink', 'email'].includes(candidate.searchParams.get('type')) ||
        !['tnn://account-callback', 'tnn-sandbox-newuser://account-callback', 'https://thoughtsnotnotes.com/account/admin.html'].includes(redirect)) throw new Error();
    confirmation = candidate.href;
    if (redirect.startsWith('tnn:') || redirect.startsWith('tnn-sandbox-newuser:')) {
      openApplication = new URL(redirect).protocol + '//';
    }
    button.disabled = false;
    message.textContent = 'Confirm your email to continue to TNN.';
  } catch {
    message.textContent = 'Open the latest sign-in email and try its link again.';
  }
  // Keep the sign-in secret out of browser history, referrers and copied URLs.
  history.replaceState(null, '', location.pathname);
}
readLink();
window.addEventListener('hashchange', readLink);
button.addEventListener('click', () => {
  if (!confirmation) {
    if (openApplication) location.assign(openApplication);
    return;
  }
  const link = confirmation;
  confirmation = null; // The Auth link is single-use; recovery must never consume it again.
  button.disabled = true;
  button.textContent = 'Opening TNN…';
  if (openApplication) {
    recoveryTimer = setTimeout(() => {
      message.textContent = 'If TNN didn’t open, allow your browser to open the app. Or open TNN manually and request a new sign-in link.';
      button.textContent = 'Open TNN';
      button.disabled = false;
    }, 2500);
  }
  location.assign(link);
});
