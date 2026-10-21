import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import test from 'node:test';

const source = readFileSync(process.env.TNN_CONFIRM_SCRIPT || fileURLToPath(new URL('../account/confirm.js', import.meta.url)), 'utf8');
function page(redirect = 'tnn-sandbox-newuser://account-callback') {
  const clicks = [];
  const timers = new Map();
  const navigations = [];
  const button = { disabled: true, textContent: '', addEventListener(type, handler) { if (type === 'click') clicks.push(handler); } };
  const message = { textContent: '' };
  const verify = new URL('https://djyimnbupvgbzzdbgsom.supabase.co/auth/v1/verify');
  verify.search = new URLSearchParams({ type: 'magiclink', token: 'synthetic-placeholder', redirect_to: redirect });
  const location = { hash: '#' + verify.href, pathname: '/account/confirm.html', assign(url) { navigations.push(new URL(url)); } };
  vm.runInNewContext(source, {
    URL, document: { querySelector: selector => selector === '#confirm' ? button : message },
    location, history: { replaceState() { location.hash = ''; } },
    window: { addEventListener() {} },
    setTimeout(fn) { const id = timers.size + 1; timers.set(id, fn); return id; },
    clearTimeout(id) { timers.delete(id); }
  });
  return { button, message, location, navigations, click() { if (!button.disabled) clicks.forEach(fn => fn()); }, tick() { for (const fn of timers.values()) fn(); timers.clear(); } };
}

test('a blocked app handoff explains recovery and never reuses the one-time Auth link', () => {
  const p = page();
  assert.equal(p.location.hash, '');
  assert.equal(p.button.disabled, false);
  p.click();
  assert.equal(p.navigations.length, 1);
  assert.equal(p.navigations[0].pathname, '/auth/v1/verify');
  p.tick();
  assert.equal(p.button.disabled, false, 'the page must not remain stuck at Opening TNN');
  assert.equal(p.button.textContent, 'Open TNN');
  assert.match(p.message.textContent, /new sign-in link/);
  p.click();
  assert.equal(p.navigations.length, 2);
  assert.equal(p.navigations[1].href, 'tnn-sandbox-newuser://');
  assert.equal(p.navigations[1].search, '');
});

test('an unapproved app redirect cannot confirm or launch anything', () => {
  const p = page('other-app://account-callback');
  assert.equal(p.button.disabled, true);
  p.click();
  p.tick();
  assert.equal(p.navigations.length, 0);
});

test('the production callback gets a safe app-only recovery link', () => {
  const p = page('tnn://account-callback');
  assert.equal(p.navigations.length, 0, 'mail scanners must not consume the link');
  p.click();
  p.tick();
  p.click();
  assert.equal(p.navigations[1].href, 'tnn://');
});
