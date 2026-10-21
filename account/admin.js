import { supabaseURL, publishableKey } from './config.js';
const $ = selector => document.querySelector(selector);
const status = message => { $('#status').textContent = message; };
let busy = false, refresh;
const loadSession = () => { try { return JSON.parse(sessionStorage.getItem('tnn-admin-session')); } catch { return null; } };
const saveSession = value => sessionStorage.setItem('tnn-admin-session', JSON.stringify(value));
async function auth(path, body) {
  const response = await fetch(supabaseURL + '/auth/v1/' + path, {method:'POST',headers:{apikey:publishableKey,'Content-Type':'application/json'},body:JSON.stringify(body)});
  if (!response.ok) throw new Error(response.status === 429 ? 'Please wait before trying again.' : 'Sign-in failed. Request a new link.');
  const value = await response.json();
  if (value.access_token) { value.expires_at = Math.floor(Date.now()/1000) + value.expires_in; saveSession(value); }
  return value;
}
async function token() {
  let session = loadSession();
  if (!session) throw new Error('Sign in to continue.');
  if (session.expires_at < Date.now()/1000 + 60) {
    if (!refresh) refresh = auth('token?grant_type=refresh_token', {refresh_token:session.refresh_token}).finally(() => { refresh = null; });
    session = await refresh;
  }
  return session.access_token;
}
async function api(path, body) {
  const jwt = await token();
  const response = await fetch(supabaseURL + '/functions/v1/access' + path, {method:body?'POST':'GET',headers:{apikey:publishableKey,Authorization:'Bearer '+jwt,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined});
  const value = await response.json();
  if (!response.ok) throw new Error(value.message || 'Please try again.');
  return value;
}
async function perform(action) {
  if (busy) return;
  busy = true; document.querySelectorAll('button').forEach(el => { el.disabled = true; });
  try { await action(); } catch (error) { status(error.message); }
  finally { busy = false; document.querySelectorAll('button').forEach(el => { el.disabled = false; }); }
}
async function users() {
  const value = await api('/v1/admin/users?q=' + encodeURIComponent($('#search').value));
  const list = $('#users'); list.replaceChildren();
  for (const person of value.users) {
    const row = document.createElement('div'); row.className = 'user';
    const email = document.createElement('span'); email.textContent = person.email;
    const badge = document.createElement('span'); badge.className = 'badge'; badge.textContent = person.access === 'paid' ? 'Paid PRO' : person.access === 'beta' ? 'Free PRO' : 'Starter';
    row.append(email, badge);
    if (person.access === 'beta') {
      const remove = document.createElement('button'); remove.className = 'ghost'; remove.textContent = 'Revoke';
      remove.addEventListener('click', () => perform(async () => { await api('/v1/admin/users',{email:person.email,enabled:false}); await users(); status('Free access revoked for '+person.email+'.'); }));
      row.append(remove);
    }
    list.append(row);
  }
  if (!value.users.length) list.textContent = 'No matching emails.';
}
$('#login').addEventListener('submit', event => { event.preventDefault(); perform(async () => {
  if (!publishableKey) throw new Error('Account setup is in progress.');
  const verifier = btoa(String.fromCharCode(...crypto.getRandomValues(new Uint8Array(32)))).replaceAll('+','-').replaceAll('/','_').replaceAll('=','');
  const hash = await crypto.subtle.digest('SHA-256',new TextEncoder().encode(verifier));
  const challenge = btoa(String.fromCharCode(...new Uint8Array(hash))).replaceAll('+','-').replaceAll('/','_').replaceAll('=','');
  localStorage.setItem('tnn-admin-verifier',JSON.stringify({verifier,createdAt:Date.now()}));
  await auth('otp?redirect_to='+encodeURIComponent('https://thoughtsnotnotes.com/account/admin.html'), {email:$('#email').value.trim().toLowerCase(),create_user:true,code_challenge:challenge,code_challenge_method:'s256'});
  status('Check your email. Open its link in this browser.');
}); });
$('#grant').addEventListener('submit', event => { event.preventDefault(); perform(async () => {
  const emails = [...new Set($('#emails').value.split(/[\s,;]+/).map(v=>v.trim().toLowerCase()).filter(Boolean))];
  if (!emails.length || emails.length > 100 || emails.some(v=>v.length>254 || !/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(v))) throw new Error('Enter up to 100 valid emails.');
  let count = 0;
  for (const email of emails) { await api('/v1/admin/users',{email,enabled:true}); count++; status('Granted '+count+' of '+emails.length+'.'); }
  $('#emails').value = ''; await users(); status('Free PRO granted to '+count+' email'+(count===1?'':'s')+'.');
}); });
let searchTimer;
$('#search').addEventListener('input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(()=>perform(users),250); });
$('#sign-out').addEventListener('click', () => { sessionStorage.removeItem('tnn-admin-session'); localStorage.removeItem('tnn-admin-verifier'); location.reload(); });
await perform(async () => {
  const parameters = new URL(location.href).searchParams;
  const code = parameters.get('code');
  history.replaceState(null,'',location.pathname);
  if (code) {
    let saved; try { saved = JSON.parse(localStorage.getItem('tnn-admin-verifier')); } catch { /* Request a new link. */ }
    if (!saved?.verifier || Date.now()-saved.createdAt>900000) throw new Error('Open the latest link in the browser where you requested it.');
    await auth('token?grant_type=pkce',{auth_code:code,code_verifier:saved.verifier});
    localStorage.removeItem('tnn-admin-verifier');
  }
  if (loadSession()) {
    $('#sign-out').hidden = false;
    const account = await api('/v1/account');
    if (!account.administrator) throw new Error('Administrator access required.');
    $('#sign-in').hidden = true; $('#panel').hidden = false; await users();
  }
});
