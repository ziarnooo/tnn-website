#!/usr/bin/env python3
"""Keyword discovery without Ahrefs.

Hits the Google and Bing autocomplete endpoints across seed phrases plus
modifier and alphabet expansions. A suggestion only exists if people actually
type it, so this is real demand signal - but it gives NO absolute volume.

    python3 blog/_keywords.py     # writes kw_raw.txt: engines, hits, phrase

Read the output as: 2 engines = strong signal, 1 = weak. Then judge difficulty
by searching the phrase and looking at WHO ranks. Thin app-marketing sites or
forums on page one means winnable; a wall of funded SaaS blogs means skip.

For real volume numbers, free: Bing Webmaster Tools keyword research, and your
own Search Console once pages have impressions. GSC is the best keyword tool
you own, because it shows queries you ALREADY nearly rank for.
"""

import json, urllib.parse, urllib.request, string, collections, sys
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"

def fetch(url, t=4):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=t) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        return ""

def google(q):
    raw = fetch("https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q=" + urllib.parse.quote(q))
    try: return json.loads(raw)[1]
    except Exception: return []

def bing(q):
    raw = fetch("https://api.bing.com/osjson.aspx?query=" + urllib.parse.quote(q))
    try: return json.loads(raw)[1]
    except Exception: return []

SEEDS = [
    "record meeting on mac", "record zoom meeting without", "record teams meeting",
    "record system audio mac", "how to record a meeting on mac",
    "transcribe meeting", "transcribe audio mac", "meeting transcription",
    "transcribe zoom meeting", "whisper mac", "local transcription",
    "offline transcription", "on device transcription", "speech to text mac",
    "ai meeting notes", "ai notetaker", "meeting notes app", "meeting summary ai",
    "meeting notes template", "meeting recorder without bot", "notetaker without bot",
    "private meeting notes", "is otter ai safe", "meeting recording consent",
    "claude mcp", "mcp server", "claude meeting notes", "obsidian meeting notes",
    "markdown meeting notes", "dictation mac", "voice to text mac",
    "1 on 1 meeting notes", "user interview notes", "how to take better meeting notes",
    "granola alternative", "otter alternative", "meeting notes without",
    "ai notes privacy", "transcribe interview", "meeting minutes ai",
]

MODS = ["", "how to ", "best ", "can i ", "free "]
TAILS = ["", " without bot", " mac", " offline", " free", " privacy", " locally", " app"]

qs = []
for s in SEEDS:
    for m in MODS:
        qs.append(m + s)
    for t in TAILS:
        if t: qs.append(s + t)
for s in SEEDS[:18]:
    for ch in string.ascii_lowercase:
        qs.append(s + " " + ch)
qs = list(dict.fromkeys(qs))
print("queries:", len(qs), file=sys.stderr)

seen = collections.Counter()
src = collections.defaultdict(set)

def work(q):
    res = []
    for name, fn in (("g", google), ("b", bing)):
        for s in fn(q):
            res.append((name, s.strip().lower()))
    return res

with ThreadPoolExecutor(max_workers=16) as ex:
    for i, res in enumerate(ex.map(work, qs)):
        for name, s in res:
            if 12 < len(s) < 78:
                seen[s] += 1
                src[s].add(name)
        if i % 100 == 0:
            print("  %d/%d  %d unique" % (i, len(qs), len(seen)), file=sys.stderr, flush=True)

rows = sorted(((len(src[k]), c, k) for k, c in seen.items()), reverse=True)
with open("kw_raw.txt", "w") as f:
    for e, c, k in rows:
        f.write("%d\t%d\t%s\n" % (e, c, k))
print("wrote kw_raw.txt:", len(rows), file=sys.stderr)
