# TNN: system na ruch (SEO + ads)

Cel nadrzędny: pobrania appki. North Star na teraz to 100 pobrań -> 20 wywiadów.
Wszystko poniżej jest podporządkowane temu jednemu łańcuchowi:

```
wyświetlenia -> kliki -> download_intent -> file_download -> instalacja
```

Każdy pomysł na "content" albo "kampanię" oceniaj po tym, który krok tego
łańcucha ruszy. Jeśli żadnego, nie robimy.

---

## 1. Stan wyjściowy (audyt 2026-07-29)

Zrobione w tym przejściu:

| Rzecz | Było | Jest |
|---|---|---|
| `<title>` | "Every conversation, organized." (0 słów kluczowych) | "Private Meeting Transcription for Mac, On-Device" |
| meta description | ok, ale bez "no subscription" | przepisana, z ceną i beta |
| canonical | brak | `index`, `privacy`, `terms` |
| og:image | **brak, zero podglądu przy share** | `assets/og-image.png` 1200x630 |
| twitter:card | `summary` (mały kafel) | `summary_large_image` |
| structured data | brak | SoftwareApplication + Organization + WebSite + FAQPage |
| robots.txt | brak | jest, `thanks`/`beta` wykluczone |
| sitemap.xml | brak | jest, 3 URL-e |
| Search Console | plik weryfikacyjny jest | trzeba wysłać sitemapę |

Drugie przejście, blog:

| Rzecz | Stan |
|---|---|
| `/blog/` + 7 wpisów | 5 comparison, 1 how-to, 1 guide (patrz `SECTIONS` w `_build.py`) |
| Generator | `blog/_build.py` - nowy wpis = nowy słownik w `POSTS` |
| Keywordy | `blog/_keywords.py` - autouzupełnianie Google + Bing, patrz sekcja 1b |
| Design | `css/blog.css` + `js/blog.js`, light i dark, ta sama typografia co strona |
| Chrome | `css/chrome.css` - **jedno** źródło nav, stopki, theme toggle'a i modala |
| Schema na wpis | BlogPosting + BreadcrumbList + FAQPage |
| Linkowanie wewnętrzne | Blog w nav i w stopce, cztery linki z sekcji Pricing |
| Ceny konkurentów | zweryfikowane VII 2026, `price-ledger` na homepage poprawiony |

### Zasada, która wynikła z realnego buga

Modal pobierania rozjeżdżał się na blogu, bo reguły `.gate-*` i wygląd
`.modal__submit` istniały **tylko** w inline `<style>` w `index.html`.
`thanks.html` miał chrome skopiowany "1:1" z komentarzem, że to kopia.

Stąd `css/chrome.css` i kolejność ładowania na **każdej** stronie:

```
style.css  ->  chrome.css  ->  CSS strony
```

Regułę chrome'u (nav, stopka, theme toggle, modal) dopisujesz **tam**, nigdy
w inline. Inaczej blog znowu się rozjedzie.

Dwie pułapki, które już raz ugryzły:
- `section` w `style.css` ma `padding: 120px 0`. Każdy nowy `<section>` na
  blogu potrzebuje `padding: 0`, inaczej odstępy eksplodują.
- Nie pisz w komentarzu CSS ścieżki z gwiazdką i slashem. To zamyka komentarz
  przedwcześnie i parser zjada pierwszą regułę pod nim. Zjadło override akcentu
  i cały blog zrobił się turkusowy.

Nie zrobione, bo to decyzja produktowa (patrz sekcja 3):
H1 i nagłówki na stronie głównej nadal nie zawierają ani słowa "meeting",
ani "transcription".

### Co blokuje ruch

1. ~~**Jedna strona = jedno URL na wszystko.**~~ Ruszone: jest blog i cztery
   strony pod frazy z realną intencją zakupową. Rytm to teraz dwie strony
   miesięcznie, kolejność z sekcji 2.

2. **H1 nie zawiera kategorii.** "Every conversation, organized. Nothing leaves
   your Mac." brzmi dobrze i nie mówi Google'owi ani użytkownikowi, co to jest.
   Człowiek szukający "local meeting transcription mac" nie widzi dopasowania.

3. **Nazwa marki koliduje.** `thoughtsformac.com` to appka "Thoughts" na Maca:
   menubar, notatki, lokalnie, własny klucz Claude/OpenAI, pay-what-you-want.
   Prawie identyczne pozycjonowanie i prawie identyczna nazwa. Do tego "thoughts"
   i "notes" to najbardziej generyczne słowa w tej kategorii. Konsekwencja:
   brandowe zapytania będą się rozjeżdżać. Zawsze wychodź z "TNN" jako skrótem
   i dopinaj deskryptor ("Thoughts Not Notes - private meeting transcription").

---

## 1b. Jak szukać keywordów bez Ahrefsa

`python3 blog/_keywords.py` uderza w autouzupełnianie Google i Binga: seedy plus
modyfikatory plus alfabet. Podpowiedź istnieje tylko wtedy, gdy ludzie tak
wpisują, więc to realny sygnał popytu. Ostatni przebieg: 948 zapytań, 5453
unikalne frazy, 4974 trafione tematycznie.

Czego to **nie** daje: absolutnego wolumenu. Kolumna to liczba silników
(2 = mocny sygnał, 1 = słaby) i liczba trafień, nie searche/miesiąc.

Trudność oceniaj osobno i ręcznie: **wygoogluj frazę i zobacz, kto rankuje.**
- thin affiliate blogi, małe apki, forum, Reddit → wchodzimy
- ściana blogów finansowanych SaaS-ów, każdy z własnym listicle → odpuszczamy

Po realny wolumen, darmowo: Bing Webmaster Tools (keyword research) i własny
Search Console, gdy strony zbiorą wyświetlenia. GSC jest najlepszym narzędziem
keywordowym, jakie masz, bo pokazuje frazy, na które **już prawie** rankujesz.

### Czego nie pozycjonujemy, świadomie

`record a zoom meeting without anyone knowing` (19 trafień) i
`record teams meeting without anyone knowing` (6) mają realny wolumen. Nie
piszemy pod nagrywanie ludzi bez ich wiedzy. Ten sam popyt łapie uczciwie post
o zgodzie na nagrywanie, i ustawia TNN po właściwej stronie zamiast kojarzyć go
z ukrytym nagrywaniem. Ta fraza jest nadal wolna w backlogu jako `reference`.

### Odkrycie z SERP-ów, warte zapamiętania

W klastrze lokalnym realnymi sąsiadami w wynikach **nie są** Otter ani Granola,
ale małe apki: Whisper Notes, VoiceScriber, Inscribe, Viska, Buzz, VoiceInk.
Te SERP-y są słabe, więc to najtańsze wejście. Napisane porównania celują wyżej,
niż trzeba, i to jest dobra wiadomość, nie zła.

---

## 2. Mapa słów kluczowych

Kolejność = priorytet. Nie zaczynaj od góry kategorii, bo tam stoją Otter,
Fireflies i 200 artykułów afiliacyjnych.

### A. Alternatywy (NAJWYŻSZY priorytet)
Najwyższa intencja zakupowa, najniższa trudność, najlepsze pod ads.
Jedna strona na jednego konkurenta.

```
granola alternative           NAPISANE  /blog/granola-alternative/
otter.ai alternative          NAPISANE  /blog/otter-ai-alternative/
fireflies alternative         NAPISANE  /blog/fireflies-alternative/
tldv alternative              NAPISANE  /blog/tldv-alternative/
best offline transcription    NAPISANE  /blog/offline-transcription-apps-mac/
ai note taker no bot          NAPISANE  /blog/ai-notetaker-without-bot/
zoom without premium          NAPISANE  /blog/record-zoom-meeting-without-premium/

fathom alternative                      jamie alternative
meetily alternative                     speech to text mac
meeting recording consent               1 on 1 meeting notes template
```

Wzór strony (już zaszyty w czterech napisanych): callout z krótką odpowiedzią,
co konkurent robi dobrze, gdzie boli (subskrypcja / chmura / bot), tabela
porównawcza z datą weryfikacji cen, sekcja **gdzie konkurent nadal wygrywa**,
CTA, trzy pytania FAQ.

Ta sekcja "gdzie konkurent wygrywa" nie jest grzecznościowa. Robi trzy rzeczy:
buduje wiarygodność u czytelnika, który zna oba narzędzia; odsiewa ludzi, dla
których TNN nie zadziała (mniej pobrań, ale lepsze wywiady); i chroni przed tym,
że taka strona wróci po dwóch latach jako zarzut. Nie wycinaj jej.

Nowy wpis:

```
1. sprawdź ceny konkurenta na jego stronie (nie w cudzym artykule)
2. dopisz słownik do POSTS w blog/_build.py
3. python3 blog/_build.py
4. wklej wypisane <url> do sitemap.xml
5. jeśli wpis dotyczy konkurenta z price-ledger na homepage, upewnij się,
   że liczby się zgadzają w obu miejscach
```

### B. Bez bota (drugi priorytet)
Duży, niedoobsłużony klaster. Ludzie tego szukają wprost.

```
meeting recorder without bot         ai notetaker without bot
record zoom meeting without bot      transcribe google meet without bot
teams meeting notes without bot      ai meeting notes no bot in participant list
meeting transcription no bot joining
```

### C. Lokalnie / prywatnie / offline (rdzeń produktu)
```
local meeting transcription mac      offline meeting transcription
on-device meeting transcription      private ai meeting notes
meeting notes app that doesn't upload audio
gdpr compliant meeting transcription no cloud meeting recorder
record meetings locally mac
```
Target: strona główna + osobna strona `/private-meeting-transcription`.

### D. Bez subskrypcji
```
meeting transcription one time payment
ai meeting notes no subscription      lifetime license meeting transcription
free meeting transcription mac        (uwaga: "free" ściąga niepłacących,
                                       ale w becie to dokładnie nasz target)
```

### E. Claude / MCP (mała skala, zero konkurencji, nasze plemię)
Najlepszy stosunek wysiłku do konwersji. Ci ludzie kupują od razu.
```
claude mcp meeting notes             mcp server meeting transcripts
claude desktop meeting context       give claude context from my meetings
meeting notes markdown obsidian      ai memory from meetings
```
Do tego dystrybucja, nie SEO: rejestry serwerów MCP, awesome-mcp listy,
r/ClaudeAI. To jest darmowy kanał, który mamy niewykorzystany.

### F. How-to (górna część leja, blog, najniższy priorytet)
```
how to record a meeting on mac with audio
how to record system audio on mac       how to transcribe a meeting for free
whisper transcription on mac            meeting notes template markdown
```

### Czego NIE atakować
`ai meeting notes`, `meeting transcription software`, `ai notetaker`,
`best transcription app`. Head terms, CPC 6-15 USD, SERP zajęty przez
listicle SaaS-ów z budżetem. Wejdziemy tam za rok przez markę, nie teraz.

---

## 3. Copy na stronie: co zmienić (decyzja Dominika)

H1 to najmocniejszy sygnał na stronie i dziś nie robi nic dla wyszukiwania.
Trzy warianty, od najbardziej zachowawczego:

- **C (rekomendacja)** - zostaw pierwszą linię, druga bierze słowa kluczowe:
  `Every conversation, organized.` / `Meeting transcription that never leaves your Mac.`
- **B** - krócej i wprost: `Private meeting notes.` / `Nothing leaves your Mac.`
- **A** - najbardziej pod SEO, najmniej poetycko:
  `Every meeting, transcribed on your Mac.` / `Nothing leaves it.`

Poza H1, tanie wygrane w treści:
- H2 sekcji feature'ów: zamiast "Built around how you actually work" wpleść
  "meeting" i "Mac" w co najmniej dwa H3.
- Dodać do FAQ trzy pytania, które są realnymi zapytaniami:
  "Does it work without internet?", "Can I transcribe Zoom without a bot?",
  "Is it a Granola alternative?". Każde nowe FAQ **musi** trafić też do
  JSON-LD w `<head>`, inaczej rich result się wykrzaczy.
- ~~Sekcja `price-ledger` nie linkuje do niczego.~~ Zrobione: pod nią są cztery
  linki do wpisów, z anchor textem dokładnie pod frazę.

---

## 4. Mini system: co sprawdzać i kiedy

### Przy każdym deployu (5 minut)
- [ ] `<title>` i description nadal opisują to, co na stronie
- [ ] jeśli zmieniłem FAQ na stronie, zmieniłem też JSON-LD
- [ ] jeśli dodałem stronę, dopisałem ją do `sitemap.xml`
- [ ] CTA działa: klik -> modal -> mail -> `/thanks.html?dl=1` -> DMG leci
- [ ] og:image się renderuje (walidator LinkedIn Post Inspector)

### Raz w tygodniu (15 minut), trzy liczby
1. **Search Console -> Performance -> Queries.** Nie patrz na pozycję, patrz
   na *jakie zapytania w ogóle się pojawiły*. Każde nowe zapytanie z
   wyświetleniami i zerem klików to gotowy temat na stronę.
2. **GA4: `download_intent_desktop` -> `generate_lead`.** To jest przepuszczalność
   bramki mailowej. Jeśli poniżej ~50%, bramka kosztuje więcej niż wartość maili.
3. **`file_download` w ujęciu tygodniowym** - jedyna liczba, która się liczy.

### Raz w miesiącu (godzina)
- Ile nowych stron opublikowanych (target: 2/miesiąc, wszystkie z sekcji A/B)
- Ile wzmianek/linków z zewnątrz (szukaj `"thoughtsnotnotes"` w Google)
- Czy jesteśmy na: Product Hunt, alternativeto.net, MacUpdate, rejestrach MCP,
  awesome-mcp. To darmowe linki i darmowy ruch, każdy odhaczany raz.
- Re-check: `site:thoughtsnotnotes.com` w Google - czy wszystko jest w indeksie

### Do zrobienia raz, teraz
- [ ] Search Console: wysłać `sitemap.xml`
- [ ] Search Console: dodać wariant z `www` i bez, wybrać jeden jako kanoniczny
- [ ] Bing Webmaster Tools (import z GSC, 2 minuty, ChatGPT/Copilot ciągną z Bing)
- [ ] GA4 -> oznaczyć `file_download` i `generate_lead` jako *key events*
- [ ] PageSpeed Insights na `/` - 148 KB HTML plus Google Fonts blokujące render

---

## 5. Ads

### Uczciwa matematyka, zanim wydasz złotówkę
Produkt 49 USD jednorazowo. CPC na frazach typu "otter alternative" to 3-9 USD.
Przy 5% klików kończących się pobraniem i 20% pobrań kończących się zakupem
wychodzi 1% konwersji, czyli CAC 300-900 USD na produkcie za 49. Google Search
na szerokich frazach po prostu się nie spina. Dlatego:

**Nie odpalamy** kampanii na head terms ani broad match. Nigdy.

**Odpalamy, mały budżet, exact match:**
1. **Brand defense.** Fraza `thoughts not notes`, `tnn app mac`. Groszowe CPC,
   chroni przed `thoughtsformac` i przed tym, że konkurent podbije nasz brand.
   To pierwsza kampania, jaką w ogóle warto włączyć.
2. **Alternatywy, exact match**, po jednej grupie na konkurenta, kierowane na
   dedykowaną stronę z sekcji A. Mały wolumen, ale intencja maksymalna.
3. **"Without bot" / "offline"**, exact match, na stronę z sekcji B/C.

Budżet startowy 10-20 USD/dzień, bid strategy: maksymalizacja konwersji
z celem na `file_download`, nie na kliki.

### Czego brakuje w plumbingu (to zrób PRZED wydawaniem)
- [ ] Google Ads conversion tag / import konwersji z GA4 (dziś nie ma niczego,
      więc każda kampania byłaby ślepa)
- [ ] powiązanie GA4 z Google Ads
- [ ] audience do remarketingu: odwiedził `/` i nie dotarł do `/thanks.html`
- [ ] dedykowany landing pod ads: jedno CTA, bez nawigacji, bez sekcji pricing
      z przekreśloną ceną (przekreślone 49 USD przy "free" myli w płatnym ruchu)
- [ ] **rozstrzygnąć bramkę mailową.** W ruchu organicznym da się obronić.
      W płatnym płacisz za klik i tracisz połowę ludzi na formularzu przed
      pobraniem. Rekomendacja na płatny ruch: pobranie od razu, mail zbierany
      na `/thanks.html` po starcie downloadu.

### Kanały, które przy 49 USD bija Google Ads
Kolejność po stosunku wysiłku do efektu:
1. **Darmowe listingi**: Product Hunt, alternativeto.net (wpisać się jako
   alternatywa dla Granoli/Ottera - to jednocześnie link i ruch z intencją),
   MacUpdate, rejestry MCP, awesome-mcp.
2. **Reddit**: r/macapps, r/ClaudeAI, r/MacOS, r/productivity. Organicznie,
   nie reklamą. Reddit ads też są tanie, ale posty działają lepiej.
3. **Hacker News** - jeden Show HN, dobrze przygotowany.
4. **LinkedIn Dominika** - już działa, posty są w `tnn-marketing/linkedin/POSTY.md`.

---

## 6. Kolejność robót

**Ten tydzień**
1. Deploy całości: meta, og:image, JSON-LD, robots, sitemap, `/blog/` z czterema
   wpisami, linki z homepage, poprawione ceny w `price-ledger`
2. Search Console: wysłać sitemapę, potem "Request indexing" na `/blog/` i na
   każdym z czterech wpisów osobno. Bez tego nowe URL-e czekają tygodniami
3. Bing Webmaster Tools (import z GSC)
4. Wybrać wariant H1 na homepage i wdrożyć (sekcja 3)
5. Darmowe listingi: alternativeto.net (wpisać się jako alternatywa dla
   Granoli i Ottera, linkując do odpowiednich wpisów), rejestry MCP

**Następne dwa tygodnie**
6. Wpiąć konwersje do Google Ads, potem włączyć tylko brand defense
7. Rozesłać wpisy tam, gdzie leży ruch: r/macapps, r/ClaudeAI, LinkedIn.
   `offline-transcription-apps-mac` jest najlepszy na r/macapps, bo nie jest
   sprzedażowy i wprost mówi, kiedy wybrać Buzza
8. Kolejne wpisy z backlogu w sekcji 2, wg tego co pokaże GSC

**Potem, rytm**
9. Dwie strony miesięcznie z sekcji A/B, kolejność wg tego, co pokaże GSC
10. Ads rozszerzać tylko o frazy, które już dowiozły `file_download` organicznie
11. Raz na kwartał: przejść ceny konkurentów w czterech wpisach i w
    `price-ledger`. Nieaktualna cena w porównaniu to najłatwiejszy sposób
    stracenia wiarygodności
