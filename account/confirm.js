// Email scanners may open the page; only a deliberate click consumes the Auth link.
const button = document.querySelector('#confirm');
const message = document.querySelector('#message');
let confirmation;
function readLink() {
  confirmation = null;
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
        !['tnn://account-callback', 'https://thoughtsnotnotes.com/account/admin.html'].includes(redirect)) throw new Error();
    confirmation = candidate.href;
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
  if (!confirmation) return;
  button.disabled = true;
  button.textContent = 'Opening TNN…';
  location.assign(confirmation);
});
