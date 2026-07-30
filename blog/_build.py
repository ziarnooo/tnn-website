#!/usr/bin/env python3
"""
Blog generator for thoughtsnotnotes.com.

Every page on the blog shares the same chrome (nav, footer, download modals,
meta, JSON-LD), so it lives here once instead of being copy-pasted per file.

    python3 blog/_build.py

writes blog/index.html and blog/<slug>/index.html for every entry in POSTS,
then prints the <url> blocks to paste into sitemap.xml.

To add a post: append a dict to POSTS and re-run. Keep `body` as plain HTML -
the design comes from css/blog.css, so no inline styles are needed.

Two rules that are easy to break:
  1. Every FAQ entry ends up in the page's JSON-LD automatically, so a question
     in `faq` MUST be a question a reader can actually see on the page. Don't
     put schema-only questions there.
  2. Competitor pricing goes stale fast. `checked` is the date the numbers were
     last verified and is printed on the page. Re-verify before touching it.
"""

import os
import re
import html
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://thoughtsnotnotes.com"
BUILT = "2026-07-30"

# ============================================================
# SECTIONS
# Hub order and headings. A post's "type" must match a key here or the post
# will not appear on the hub. Default when "type" is omitted: comparison.
# ============================================================

SECTIONS = [
    ("comparison", "Comparisons",
     "Head to head against the tools people actually leave. Each one ends with where the other tool still wins."),
    ("howto", "How-to",
     "Concrete recording and transcription problems on a Mac, solved without a subscription."),
    ("guide", "Guides",
     "The wider picture: how the categories differ and which one you are actually shopping in."),
]

# ============================================================
# POSTS
# ============================================================

POSTS = [
    # ------------------------------------------------------------------
    {
        "slug": "record-zoom-meeting-without-premium",
        "type": "howto",
        "tag": "How-to",
        "title": "How to record a Zoom meeting without a paid plan",
        "seo_title": "Record a Zoom Meeting Without Premium (Mac, 2026) - TNN",
        "description": "Zoom's free plan limits recording and cuts group calls at 40 minutes. Here is what the free plan actually allows, and how to record and transcribe any meeting on a Mac without paying Zoom anything.",
        "date": "2026-07-30",
        "date_label": "30 July 2026",
        "read": "6 min read",
        "checked": "July 2026",
        "lede": "Most articles answering this question tell you to install a screen recorder and quietly capture the call. That advice skips the two things that actually matter: what Zoom's free plan really permits, and the fact that a recording is only useful if you can search it afterwards.",
        "table": {
            "headers": ["Approach", "Needs Zoom paid plan", "Needs host permission", "Get a transcript", "Works off Zoom too"],
            "rows": [
                ["Zoom local recording", "No, but host-only by default", "Yes, if you are not host", "No, audio file only", "No"],
                ["Zoom cloud recording", "Yes", "Yes, if you are not host", "Yes, on paid tiers", "No"],
                ["QuickTime screen recording", "No", "No", "No", "Yes"],
                ["Bot notetaker (Otter, Fireflies)", "No", "Bot must be admitted", "Yes", "Only supported apps"],
                ["TNN", "No", "No, captures your Mac's audio", "Yes, on-device", "Yes, anything audible"],
            ],
            "tnn_col": 4,
            "caption": "Zoom plan limits checked July 2026 against Zoom's published plan comparison. Zoom changes tiers often - verify before relying on this.",
        },
        "body": """
<div class="callout">
  <span class="callout__label">The short answer</span>
  <p>You do not need Zoom premium to record. You need something that captures the audio your own Mac plays, independently of Zoom. That also removes the 40-minute problem, because a local recorder does not care that Zoom ended the call.</p>
  <p>What you <em>do</em> need is to tell people you are recording. That is not a Zoom setting, it is your obligation, and no tool removes it.</p>
</div>

<h2>What Zoom's free plan actually gives you</h2>

<p>Two separate limits get confused constantly, so it is worth separating them.</p>

<p><strong>Recording.</strong> Zoom's free plan does include local recording, saved to your own disk from the desktop app. Cloud recording is a paid feature. The catch is not the plan, it is permission: by default only the host can record, and a participant needs the host to grant it. If you are the host of your own calls, free local recording works.</p>

<p><strong>The 40-minute cap.</strong> Group meetings on the free plan end after 40 minutes. This is the limit people actually hit, and it has nothing to do with recording. Your recording stops because the meeting stops.</p>

<p>So "record a Zoom meeting without premium" usually means one of three real problems: you are not the host and cannot get permission, you keep losing the second half of long calls, or you want a searchable transcript rather than a 400 MB video file you will never open.</p>

<h2>The advice you will find elsewhere, and why it is thin</h2>

<p>Search this question and you get screen recorders: QuickTime, and a long tail of affiliate-driven "recorder" products. QuickTime does work, it is already on your Mac, and it is free. On modern macOS you can capture the screen with system audio using the built-in screen recording tools.</p>

<p>But a screen recording gives you a video file. Three weeks later, when you need to know what you agreed to, you have a folder of hour-long videos and no way to search them. You have solved recording and not solved remembering, which was the actual job.</p>

<div class="note">
  <strong>The framing to be careful about:</strong> a lot of these articles are optimised for "record without permission" and treat invisibility as the feature. Whether a bot is visible or not, recording people who have not been told is a different question from which software you use, and in plenty of places it is a legal one. Say you are recording. It takes four seconds.
</div>

{{TABLE}}

<h2>The approach that solves the actual problem</h2>

<p>Capture the audio your Mac is already playing, transcribe it locally, and keep the result as text.</p>

<p>That is what TNN does. It does not join the Zoom call, so there is no host permission to request and nothing in the participant list. It records what your Mac can hear, which means it also covers the case Zoom cannot: the call moves to a phone on speaker, or half the meeting happens in the room after the call ends.</p>

<p>Because it is not tied to Zoom, the 40-minute cap becomes irrelevant to the recording. Zoom drops the call, you restart it, and TNN keeps writing to the same meeting.</p>

<p>Transcription runs on your Mac's Neural Engine using Whisper, so the audio never leaves the machine and there is no per-minute meter. Each meeting ends up as one plain Markdown file containing your live notes, the full transcript and an AI summary. Plain text is the point: it is searchable, greppable, indexable by Spotlight, and readable in ten years.</p>

<blockquote>A video of the meeting proves it happened. A transcript tells you what was decided.</blockquote>

<h2>Doing it, start to finish</h2>

<ol>
  <li>Install TNN and grant the screen and microphone permissions macOS asks for. The transcription model downloads once, about 600 MB, then everything runs offline.</li>
  <li>Connect your calendar so TNN knows which meeting is starting and names the file for you.</li>
  <li>At the top of the call, say you are recording for notes.</li>
  <li>Press record. Type rough fragments as you go - the AI fills in what you missed rather than replacing your judgement with a wall of summary.</li>
  <li>Afterwards, the meeting is a Markdown file in a folder you choose. If you connect Claude over MCP, you can ask it what you committed to across a whole month of calls, and it answers from the transcripts.</li>
</ol>

<h2>When you should just use Zoom's own recording</h2>

<ul>
  <li><strong>You need the video.</strong> Shared screens, slides, faces. TNN records audio and text only.</li>
  <li><strong>You need a recording of a meeting you did not attend.</strong> Nothing running on your laptop can capture a call you were not in. That is what a cloud bot is for.</li>
  <li><strong>Your organisation requires recordings in a central, auditable place.</strong> Local files are yours, which is exactly the wrong property for a compliance archive.</li>
  <li><strong>You are not on Apple Silicon.</strong> TNN needs macOS 13 or later on an Apple Silicon Mac.</li>
</ul>
""",
        "faq": [
            ("Can I record a Zoom meeting on the free plan?",
             "Yes. Zoom's free plan includes local recording from the desktop app, saved to your own disk. Cloud recording is a paid feature. The practical blocker is usually permission rather than price, because by default only the host can record and a participant has to be granted it. A tool that captures your Mac's own audio sidesteps that entirely."),
            ("How do I record a Zoom call longer than 40 minutes for free?",
             "The 40-minute cap ends the group meeting itself, so nothing that records inside Zoom can outlast it. A local recorder that captures your Mac's audio is not tied to the Zoom session, so when the call drops and you restart it, recording continues into the same set of notes."),
            ("Do I have to tell people I am recording?",
             "Yes, and treat that as the default regardless of the tool. Consent rules vary by country and by state, some places require everyone in the conversation to agree, and a recorder that is invisible to other participants does not change any of that. Say it at the top of the call."),
        ],
    },

    # ------------------------------------------------------------------
    {
        "slug": "granola-alternative",
        "type": "comparison",
        "tag": "Comparison",
        "title": "A Granola alternative that keeps the audio on your Mac",
        "seo_title": "Granola Alternative for Mac: Local, One-Time Payment - TNN",
        "description": "Granola is bot-free but cloud-based and billed monthly. TNN transcribes on your Mac, saves plain Markdown you own, and costs one payment. Honest comparison, including where Granola still wins.",
        "date": "2026-07-30",
        "date_label": "30 July 2026",
        "read": "7 min read",
        "checked": "July 2026",
        "lede": "Granola is the best-designed meeting notes app of the last two years, and it got one big thing right: no bot joins your call. So if you are looking for a Granola alternative, the reason usually is not the bot. It is where the audio goes, and how the bill arrives.",
        "table": {
            "competitor": "Granola",
            "rows": [
                ("Bot in the participant list", "No, captures device audio", "No, captures system audio"),
                ("Where transcription runs", "On Granola's servers", "On your Mac, on the Neural Engine"),
                ("Works with no internet", "No", "Yes, after the model downloads once"),
                ("Pricing", "Free tier, Business $14/user/mo, Enterprise $35/user/mo", "One payment, $49 planned. Free during beta"),
                ("Where notes live", "Granola's workspace, export available", "One Markdown file per meeting, in your folder"),
                ("AI notes run on", "Granola's AI, included in the price", "Your own Claude Pro or Max account"),
                ("Platforms", "macOS and Windows", "macOS 13+, Apple Silicon only"),
                ("Team workspace", "Yes, shared notes and folders", "No, single-user today"),
            ],
        },
        "body": """
<div class="callout">
  <span class="callout__label">The short answer</span>
  <p>If your problem with Granola is the monthly bill or the fact that your meeting audio is processed on someone else's servers, TNN solves both: everything runs on your Mac, and you pay once.</p>
  <p>If your problem is that you want a polished team workspace, or you are on Windows, stay with Granola. We are not going to pretend otherwise.</p>
</div>

<h2>What Granola actually got right</h2>

<p>Two things, and both are worth naming before we compare anything.</p>

<p>First, <strong>no bot</strong>. Granola captures the audio your computer plays instead of dialling into the call as a participant. Nobody sees a "Notetaker" in the attendee list, nobody has to admit a bot from the waiting room, and nobody asks what that account is. Once you have worked this way, going back to a bot-based tool feels absurd.</p>

<p>Second, <strong>the notes model</strong>. You type rough fragments during the meeting, the AI fills in what you missed. That is the correct interaction. Tools that give you a wall of AI summary with no input from you produce notes that read like nobody was in the room.</p>

<p>TNN works the same way on both counts. That is not a coincidence, and it means the honest comparison is about the two things underneath.</p>

<h2>Difference one: where the audio goes</h2>

<p>Granola sends your meeting audio to its servers to transcribe and summarise it. That is a normal, well-run SaaS arrangement, and for most meetings it is fine.</p>

<p>It stops being fine in specific situations, and if you are reading this you probably already know which one is yours: a client under an NDA that names third-party processors. A candidate interview. A salary conversation. A conversation about an incident that has not been disclosed yet. A legal or health context. A security review that asks you to enumerate every subprocessor that touches customer voices.</p>

<p>TNN transcribes on your Mac. Whisper runs on the Neural Engine, the audio never leaves the machine, and there is no server to enumerate because we do not run one. Turn off your wifi and transcription still works.</p>

{{TABLE}}

<h2>Difference two: how you pay</h2>

<p>Granola's paid tier is $14 per user per month at the time of writing, which is $168 a year, every year, for as long as you want your notes to work. The free tier gives you unlimited meetings but only the most recent 30 days are accessible; older notes stay stored and come back when you upgrade.</p>

<p>TNN is a one-time payment, $49 planned after the beta, and free while the beta runs. There is no subscription for transcription, ever, because transcription costs us nothing per meeting: it happens on your hardware.</p>

<blockquote>The pricing difference is not really about $168 versus $49. It is about what happens to two years of meeting notes if you stop paying.</blockquote>

<h2>Difference three: the files are yours</h2>

<p>This is the part people underestimate until they need it.</p>

<p>Every TNN meeting is one plain Markdown file in a folder you choose, <code>~/Documents/TNN</code> by default. Your live notes, the full transcript and the AI summary sit in that one file. Delete the app tomorrow and you still have every meeting, readable in any text editor, greppable from the terminal, indexable by Spotlight, syncable to whatever you already use.</p>

<p>Which leads to the thing TNN does that no bot-free competitor does yet: because your meetings are already plain files, <strong>Claude can work with the whole archive</strong>. TNN ships an MCP server, so Claude can list your meetings, read notes and transcripts, run your saved skills, and write results back into the meeting file. Setup is one click in Settings.</p>

<p>In practice that means you can ask "what did we promise this client across our last four calls" and get an answer built from actual transcripts, rather than from what you happened to remember to write down. The AI notes run on your own Claude Pro or Max subscription, so there are no API keys and no AI fees on top from us.</p>

<h2>Where Granola is still the better choice</h2>

<p>Genuinely, not as a formality:</p>

<ul>
  <li><strong>You are on Windows.</strong> TNN is macOS 13 or later, Apple Silicon only. Granola ships both.</li>
  <li><strong>You need a team workspace.</strong> Shared notes, shared folders, teammates reading each other's meetings. TNN is single-user today.</li>
  <li><strong>You want the AI included and zero setup.</strong> Granola's summaries work out of the box. TNN's AI notes need your own Claude Pro or Max.</li>
  <li><strong>You want a mature product.</strong> Granola has years of polish. TNN is in beta and you will find rough edges.</li>
</ul>

<div class="note">
  <strong>One more limitation worth stating up front:</strong> TNN records audio only. No video, no shareable clips with timestamps. If your workflow depends on sending a 90-second video snippet to a colleague, neither TNN nor Granola is your tool.
</div>

<h2>How to try it in about five minutes</h2>

<p>Download, grant the screen and microphone permissions macOS asks for, connect your calendar so TNN knows which meeting is starting, and press record on your next call. The transcription model downloads once, roughly 600 MB, and after that you are offline-capable.</p>

<p>If you want the Claude side, open Settings and enable the MCP server. Then ask Claude about your last meeting and watch which files it reads.</p>
""",
        "faq": [
            ("Is TNN a drop-in replacement for Granola?",
             "For the core loop, yes: rough notes during the call, AI-enhanced summary after, no bot in the participant list. What is missing is the team workspace, Windows support, and Granola's years of polish. What you gain is on-device transcription, plain Markdown files you own, and one payment instead of a subscription."),
            ("Can I import my existing Granola notes?",
             "Not automatically. Granola lets you export, and TNN meetings are plain Markdown files in a folder, so exported notes can be dropped in and they will be readable. There is no one-click migration today."),
            ("Does TNN work without internet like Granola does not?",
             "Yes, once the transcription model has downloaded. Recording, transcription, live notes, dictation and your archive all work with wifi off. Only the optional AI notes need a connection, because they run through your own Claude account."),
        ],
    },

    # ------------------------------------------------------------------
    {
        "slug": "otter-ai-alternative",
        "type": "comparison",
        "tag": "Comparison",
        "title": "An Otter.ai alternative with no bot and no minute limits",
        "seo_title": "Otter.ai Alternative for Mac: No Bot, No Minute Caps - TNN",
        "description": "Otter.ai sends a bot into your call, caps your monthly minutes and bills every month. TNN records and transcribes on your Mac with no bot, no caps and one payment. Full comparison.",
        "date": "2026-07-30",
        "date_label": "30 July 2026",
        "read": "7 min read",
        "checked": "July 2026",
        "lede": "Otter.ai is the tool most people meet first, which means it is also the tool most people are looking to leave. Two complaints come up again and again: something visibly joins the meeting, and there is a meter running on how much you can transcribe.",
        "table": {
            "competitor": "Otter.ai",
            "rows": [
                ("Bot in the participant list", "Yes, joins Zoom, Teams and Meet", "No, captures system audio"),
                ("Monthly transcription limit", "Pro: 1,200 min/mo, 90 min per conversation", "None, it runs on your hardware"),
                ("Where transcription runs", "Otter's cloud", "On your Mac, on the Neural Engine"),
                ("Pricing", "Pro $16.99/mo, or $8.33/mo billed annually. Business $30/mo, or $19.99 annually", "One payment, $49 planned. Free during beta"),
                ("Where notes live", "Otter's cloud workspace", "One Markdown file per meeting, in your folder"),
                ("Works with no internet", "No", "Yes, after the model downloads once"),
                ("Platforms", "Web, Windows, macOS, iOS, Android", "macOS 13+, Apple Silicon only"),
                ("Team features", "Shared workspace, live captions, integrations", "No, single-user today"),
            ],
        },
        "body": """
<div class="callout">
  <span class="callout__label">The short answer</span>
  <p>Switch if the bot is a problem, if you keep hitting the minute cap, or if you would rather your meeting audio never left your laptop.</p>
  <p>Do not switch if you need Otter's shared team workspace, live captions across platforms, or anything that has to work on Windows, web or a phone.</p>
</div>

<h2>The bot is the thing people actually hate</h2>

<p>Otter works by joining your meeting. It appears in Zoom, Google Meet and Microsoft Teams as a participant, records from inside the call, and produces a transcript from there.</p>

<p>That design has consequences you feel every week. Someone has to let it in from the waiting room. External guests see an account they do not recognise and ask about it. A client on a sensitive call notices a recorder in the attendee list and the temperature of the conversation changes. If the bot fails to join, you have no recording at all and you find out afterwards.</p>

<p>TNN never joins anything. It captures the audio your Mac is already playing, so there is nothing in the participant list, no meeting link to hand over, no waiting room, and nothing for the other side to notice. It works identically on Zoom, Meet, Teams, a Slack huddle, a phone call on speaker, or two people talking in a room. If your Mac can hear it, TNN can transcribe it.</p>

<div class="note">
  <strong>Recording without a bot is not recording without consent.</strong> An invisible recorder does not change your legal or ethical obligations, and in plenty of places it does not change the law either. Tell people you are recording. TNN removes the awkward bot, not the conversation.
</div>

<h2>The meter is the other thing</h2>

<p>On Otter's Pro plan you get 1,200 transcription minutes a month, a 90-minute ceiling on any single conversation, and 10 file imports a month. Twenty hours sounds generous until you have a week of workshops, or one three-hour planning session that gets cut off at ninety minutes.</p>

<p>Business lifts the meeting transcription limit and raises the per-conversation cap to four hours, at $30 per user per month billed monthly or $19.99 billed annually.</p>

<p>TNN has no minute limit, and the reason is structural rather than generous: transcription runs on your Neural Engine, so a minute of audio costs us nothing. There is no meter to build.</p>

{{TABLE}}

<h2>What happens to the audio</h2>

<p>Otter uploads and processes your meetings in its cloud. That is a normal SaaS arrangement and for a lot of meetings it is genuinely fine.</p>

<p>It is not fine when the meeting is a candidate interview, a compensation conversation, an unannounced incident, a client under an NDA that enumerates subprocessors, or anything a security questionnaire will ask about later. In those cases the honest answer to "where does the audio go" needs to be "nowhere".</p>

<p>With TNN that is the actual answer. Recording and transcription happen entirely on your Mac. There is no server, so there is nothing to breach, subpoena or add to a subprocessor list. The one online step is optional: AI-written notes run through <em>your own</em> Claude account, and you can see exactly which files Claude reads.</p>

<h2>What you get that Otter does not have at all</h2>

<p>Every TNN meeting is one plain Markdown file: your live notes, the transcript and the AI summary together, in a folder you choose. Delete the app and the files remain, readable in any editor.</p>

<p>Because they are plain files, TNN can expose them to Claude over MCP. Claude lists your meetings, reads notes and transcripts, runs skills you have saved, and writes results back into the meeting file. Ask what you committed to across the last month of client calls and the answer comes from transcripts rather than memory. That runs on your own Claude Pro or Max subscription, so there is no API key and no AI surcharge from us.</p>

<blockquote>Otter gives you a searchable cloud archive. TNN gives you a folder your AI can reason over.</blockquote>

<h2>Where Otter is still the better choice</h2>

<ul>
  <li><strong>You are not on Apple Silicon.</strong> TNN needs macOS 13 or later on an Apple Silicon Mac. Otter runs on web, Windows, macOS, iOS and Android.</li>
  <li><strong>You need live captions.</strong> Otter's real-time captioning is a genuine accessibility feature and TNN does not match it.</li>
  <li><strong>You need a team workspace.</strong> Shared folders, teammates searching each other's meetings, permissions. TNN is single-user today.</li>
  <li><strong>You need to record meetings you are not in.</strong> A bot can sit in a call you skipped. Nothing local can.</li>
  <li><strong>You want a mature product.</strong> TNN is in beta. You will find rough edges.</li>
</ul>

<h2>Trying it</h2>

<p>Download, grant the screen and microphone permissions macOS asks for, connect your calendar so TNN knows which meeting is starting, and press record. The transcription model downloads once, about 600 MB, and runs on the Neural Engine after that. Language detection is automatic, including meetings that switch language mid-sentence.</p>
""",
        "faq": [
            ("Can I transcribe Zoom without a bot joining the call?",
             "Yes. TNN captures the audio playing on your Mac rather than joining as a participant, so nothing appears in the Zoom participant list. The same approach works for Google Meet, Microsoft Teams, Slack huddles, a phone call on speaker, or a conversation in the room."),
            ("Does TNN have a monthly transcription limit like Otter's 1,200 minutes?",
             "No. Transcription runs on your Mac's Neural Engine, so there is no per-minute cost to us and no meter. Meeting length is limited only by your disk space."),
            ("Is TNN cheaper than Otter.ai over time?",
             "Otter Pro is $16.99 per month, or $8.33 per month billed annually. TNN is a single payment, $49 planned after the beta and free while the beta runs. The saving compounds, but the more important difference is that your notes keep working when you stop paying, because they are plain files on your disk."),
        ],
    },

    # ------------------------------------------------------------------
    {
        "slug": "fireflies-alternative",
        "type": "comparison",
        "tag": "Comparison",
        "title": "A Fireflies.ai alternative with no bot and no AI credits",
        "seo_title": "Fireflies.ai Alternative for Mac: No Bot, No Credits - TNN",
        "description": "Fireflies sends a notetaker bot into your calls and meters AI features with credits. TNN transcribes on your Mac, has no bot and no credits, and costs one payment. Honest comparison.",
        "date": "2026-07-30",
        "date_label": "30 July 2026",
        "read": "6 min read",
        "checked": "July 2026",
        "lede": "Fireflies.ai is built for revenue teams: a bot joins every call, everything lands in a searchable team database, and it syncs to your CRM. If that is your job, it is a reasonable tool. If you just want your own meetings written down properly, you are paying for a lot of machinery you will never open.",
        "table": {
            "competitor": "Fireflies.ai",
            "rows": [
                ("Bot in the participant list", "Yes, Fred joins the call", "No, captures system audio"),
                ("AI feature metering", "Shared workspace credit pools, add-on bundles sold separately", "None"),
                ("Where transcription runs", "Fireflies' cloud", "On your Mac, on the Neural Engine"),
                ("Pricing", "Free tier. Pro $10/user/mo annually ($18 monthly), Business $19 ($29 monthly), Enterprise $39", "One payment, $49 planned. Free during beta"),
                ("Where notes live", "Fireflies' cloud workspace", "One Markdown file per meeting, in your folder"),
                ("CRM sync", "Yes, a core feature", "No"),
                ("Platforms", "Web and mobile, bot-based so platform-agnostic", "macOS 13+, Apple Silicon only"),
                ("Works with no internet", "No", "Yes, after the model downloads once"),
            ],
        },
        "body": """
<div class="callout">
  <span class="callout__label">The short answer</span>
  <p>Leave Fireflies if you do not need the CRM and the team database, and you would rather not have a bot in the attendee list or your audio in someone's cloud.</p>
  <p>Stay with Fireflies if your team's pipeline genuinely runs through it. Nothing local replaces CRM sync and cross-team conversation search.</p>
</div>

<h2>You are probably paying for the sales stack</h2>

<p>Fireflies' real product is the layer above the transcript: conversation intelligence across a whole team, CRM records updated from calls, coaching signals, AskFred answering questions over the workspace. That is valuable if you run a sales org.</p>

<p>If you are an individual, a founder, a PM or an engineer, you open roughly none of it. You wanted the meeting written down and the commitments captured, and you ended up with a bot in every call and a subscription tuned to a use case that is not yours.</p>

<h2>The credit model catches people out</h2>

<p>Every Fireflies plan includes unlimited transcription and unlimited AI summaries, which sounds like the end of the story. It is not. AI features draw on a one-time shared workspace credit pool rather than a monthly per-user allowance: 20 on Pro, 30 on Business, 50 on Enterprise, with add-on bundles sold separately. Teams that lean on summaries, action items and AskFred hit that wall and then budget for top-ups.</p>

<p>TNN has no credits and no AI surcharge, because the AI is not ours. Recording, transcription, live notes, dictation and your archive work with no account at all. AI-written notes and the Claude connection run on <em>your own</em> Claude Pro or Max subscription. There is nothing for us to meter.</p>

{{TABLE}}

<h2>No bot, and why that matters beyond etiquette</h2>

<p>Fireflies works by joining your meeting as a participant. Someone admits it, external guests see it, and if it fails to join you have no recording.</p>

<p>TNN captures the audio your Mac is already playing. Nothing joins, nothing appears in the participant list, and it works the same on Zoom, Meet, Teams, a Slack huddle, a phone call on speaker or a conversation across a table. There is no integration to break because there is no integration.</p>

<div class="note">
  <strong>Worth saying plainly:</strong> removing the bot removes the awkwardness, not the obligation. Tell people you are recording.
</div>

<h2>Where the audio goes, and where the notes end up</h2>

<p>Fireflies processes and stores your calls in its cloud. TNN transcribes on your Mac's Neural Engine and writes one plain Markdown file per meeting into a folder you choose. Your live notes, the transcript and the AI summary are in that one file. Delete the app and the files are still yours.</p>

<p>Then the part that is genuinely different: TNN ships an MCP server, so Claude can work with that folder directly. It lists your meetings, reads notes and transcripts, runs skills you have saved, and writes the result back into the meeting file. Fireflies gives you AskFred inside Fireflies. TNN gives your own Claude access to your own meeting history, and shows you exactly which files it read.</p>

<h2>Where Fireflies is still the better choice</h2>

<ul>
  <li><strong>You need CRM sync.</strong> Calls updating deal records is a real workflow and TNN does not do it.</li>
  <li><strong>You need a team-wide searchable archive.</strong> Everyone's calls in one place, with permissions. TNN is single-user today.</li>
  <li><strong>You need coaching and playbook tracking.</strong> That is Fireflies' core, not ours.</li>
  <li><strong>Your team is not all on Apple Silicon Macs.</strong> TNN needs macOS 13 or later on Apple Silicon. A bot does not care what you run.</li>
  <li><strong>You need calls recorded when you are not there.</strong> A bot can attend without you. Nothing local can.</li>
</ul>

<h2>Trying it</h2>

<p>Download, grant the macOS screen and microphone permissions, connect your calendar, press record on the next call. The model downloads once, roughly 600 MB, then runs offline. Language detection is automatic, including mid-sentence switches.</p>
""",
        "faq": [
            ("Does TNN join my meetings the way Fireflies does?",
             "No. TNN captures the audio playing on your Mac, so nothing joins the call and nothing appears in the participant list. There is no bot to admit and no integration that can fail to connect."),
            ("Are there AI credits or usage limits in TNN?",
             "No. Recording, transcription, live notes, dictation and your archive work with no account and no limits. AI-written notes run through your own Claude Pro or Max subscription, so there is nothing for us to meter and no add-on bundles to buy."),
            ("Can TNN sync meetings to a CRM like Fireflies does?",
             "Not directly. Meetings are plain Markdown files and Claude can read and write them over MCP, so a CRM workflow is buildable, but there is no built-in CRM integration. If CRM sync is central to your job, Fireflies is the better fit."),
        ],
    },

    # ------------------------------------------------------------------
    {
        "slug": "tldv-alternative",
        "type": "comparison",
        "tag": "Comparison",
        "title": "A tl;dv alternative for people who want notes, not video",
        "seo_title": "tl;dv Alternative for Mac: Local Transcription, One Payment - TNN",
        "description": "tl;dv is video-first: a bot joins, records video, and Business runs $59 per user per month. TNN is audio-only, runs on your Mac and costs one payment. Where each one wins.",
        "date": "2026-07-30",
        "date_label": "30 July 2026",
        "read": "6 min read",
        "checked": "July 2026",
        "lede": "tl;dv is a video product with a transcript attached. A bot joins your call, records audio and video, and you get clips you can share with timestamps. That is genuinely useful for some teams. It is also a lot of tool, and a lot of money, if what you needed was a good record of what was said.",
        "table": {
            "competitor": "tl;dv",
            "rows": [
                ("Bot in the participant list", "Yes, joins Zoom, Meet and Teams", "No, captures system audio"),
                ("Records video", "Yes, video plus synced transcript", "No, audio and text only"),
                ("Where recording is processed", "tl;dv's cloud", "On your Mac, on the Neural Engine"),
                ("Pricing", "Free tier (40 recordings/week, 3h per meeting). Pro $18/user/mo annually ($29 monthly), Business $59 annually ($98 monthly)", "One payment, $49 planned. Free during beta"),
                ("Where notes live", "tl;dv's cloud library", "One Markdown file per meeting, in your folder"),
                ("Shareable clips", "Yes, a core feature", "No"),
                ("Works with no internet", "No", "Yes, after the model downloads once"),
                ("Platforms", "Bot-based, platform-agnostic", "macOS 13+, Apple Silicon only"),
            ],
        },
        "body": """
<div class="callout">
  <span class="callout__label">The short answer</span>
  <p>If you have never actually sent someone a video clip of a meeting, you are paying for the wrong product. TNN gives you the transcript, the notes and the summary, locally, for one payment.</p>
  <p>If clips <em>are</em> the workflow, stay with tl;dv. TNN records no video at all and that is not on the roadmap.</p>
</div>

<h2>Video is the whole premise, and the whole cost</h2>

<p>tl;dv's bot joins your call and captures audio and video together, producing a synchronised transcript you can scrub through and clip from. Free covers a lot on paper, with limits of 40 recordings a week and three hours per meeting. Pro is $18 per user per month billed annually, $29 monthly. Business, which is where CRM sync, coaching and playbook tracking live, is $59 per user per month annually and $98 monthly.</p>

<p>Video is why the pricing looks like that. Storing and streaming recorded calls is expensive, and you are paying for it whether or not you ever open one.</p>

<p>So the first question is honest and slightly uncomfortable: in the last three months, how many meeting videos have you actually watched back or sent to someone? For a sales team running deal reviews, the answer is a real number. For most other people it is zero, and they are on a video plan because that is what the category sells.</p>

{{TABLE}}

<h2>What TNN does instead</h2>

<p>TNN records audio and turns it into text on your Mac. Whisper runs on the Neural Engine, so the audio never leaves the machine and there is no server involved. Each meeting becomes one plain Markdown file in a folder you choose: your live notes, the full transcript, and the AI summary together.</p>

<p>No bot joins, because TNN captures the audio your Mac is already playing. Nothing appears in the participant list, and it works the same on Zoom, Meet, Teams, a Slack huddle, a phone call on speaker, or a conversation in the room.</p>

<p>Then the part that is hard to get from a cloud video tool: because your meetings are plain files, TNN exposes them to Claude over MCP. Claude lists your meetings, reads the notes and transcripts, runs skills you have saved, and writes the result back into the meeting file, on your own Claude Pro or Max subscription. You can ask what changed in a project across two months of calls and get an answer assembled from transcripts.</p>

<blockquote>tl;dv optimises for rewatching the meeting. TNN optimises for never needing to.</blockquote>

<h2>The privacy difference is not abstract here</h2>

<p>A cloud tool that records video of your calls is holding a considerably more sensitive asset than one holding text. Faces, screen shares, whatever was visible in someone's browser or on someone's wall.</p>

<p>If your meetings include candidate interviews, compensation discussions, incidents that have not been disclosed, or clients whose NDA enumerates subprocessors, a local audio-to-text tool is a materially easier thing to defend. With TNN the answer to "where is the recording stored" is "on the laptop of the person who was in the meeting", and there is no subprocessor to add to anyone's list.</p>

<div class="note">
  <strong>Still your responsibility:</strong> no bot in the participant list does not mean no obligation to say you are recording. Say it.
</div>

<h2>Where tl;dv is clearly the better choice</h2>

<ul>
  <li><strong>You share clips.</strong> Timestamped video snippets sent to colleagues or customers. TNN cannot do this at all.</li>
  <li><strong>You need CRM sync, coaching or playbook tracking.</strong> That is what Business tier buys and TNN has no equivalent.</li>
  <li><strong>Your team is mixed-platform.</strong> A bot does not care what anyone runs. TNN needs macOS 13 or later on Apple Silicon.</li>
  <li><strong>You need calls recorded without you present.</strong> A bot can attend alone. Nothing local can.</li>
  <li><strong>You want a finished product.</strong> TNN is in beta.</li>
</ul>

<h2>Trying it</h2>

<p>Download, grant the screen and microphone permissions, connect your calendar so TNN knows which meeting is starting, press record. The transcription model downloads once, about 600 MB, and after that everything works offline. Language detection is automatic.</p>
""",
        "faq": [
            ("Does TNN record video like tl;dv?",
             "No. TNN records audio and produces text: your notes, the transcript and an AI summary in one Markdown file. There is no video capture and no shareable video clips. If clips are central to your workflow, tl;dv is the right tool."),
            ("Is TNN cheaper than tl;dv?",
             "tl;dv Pro is $18 per user per month billed annually and Business is $59. TNN is a single payment, $49 planned after the beta and free during it. There is no subscription for transcription because it runs on your own hardware."),
            ("Does a bot join the call with TNN?",
             "No. TNN captures the audio playing on your Mac, so nothing joins the meeting and nothing shows up in the participant list. It works on any meeting app, and on conversations that are not in a meeting app at all."),
        ],
    },

    # ------------------------------------------------------------------
    {
        "slug": "offline-transcription-apps-mac",
        "type": "comparison",
        "tag": "Comparison",
        "title": "Offline transcription on a Mac: which app is for which job",
        "seo_title": "Best Offline Transcription Apps for Mac (2026), Compared - TNN",
        "description": "MacWhisper, Buzz, superwhisper and TNN all run Whisper on your Mac, and they are built for three different jobs: dictation, file transcription, and live meetings. Pick by job, not by feature list.",
        "date": "2026-07-30",
        "date_label": "30 July 2026",
        "read": "6 min read",
        "checked": "July 2026",
        "lede": "Search for offline transcription on a Mac and you get a dozen apps that all describe themselves the same way: Whisper, on-device, private, fast. They are not competitors in any useful sense. They are built for three different jobs, and almost every bad recommendation comes from mixing them up.",
        "table": {
            "headers": ["App", "Built for", "Runs on-device", "Captures live meeting audio", "Platforms", "Price model"],
            "rows": [
                ["macOS built-in dictation", "Dictation", "Yes", "No", "macOS", "Included"],
                ["superwhisper", "Dictation, plus file and meeting transcription on paid tiers", "On Apple Silicon; Intel favours cloud models", "On paid tiers", "macOS, Windows, iOS", "Free tier plus paid"],
                ["MacWhisper", "Transcribing audio and video files you already have", "Yes", "Not its focus", "macOS", "Free tier plus paid"],
                ["Buzz", "File transcription, plus live mic transcription", "Yes", "Microphone, not system audio", "macOS, Windows, Linux", "Free, MIT open source"],
                ["TNN", "Live meetings: notes, transcript and summary in one file", "Yes, on the Neural Engine", "Yes, system audio, no bot", "macOS 13+, Apple Silicon", "One payment, $49 planned; free in beta"],
            ],
            "tnn_col": 5,
            "caption": "Capabilities checked July 2026. Buzz details confirmed from its MIT-licensed repository; superwhisper from its own site. Deliberately no exact prices for the paid apps here - they change often and a stale number is worse than none. Check each vendor before you buy.",
        },
        "body": """
<div class="callout">
  <span class="callout__label">The short answer</span>
  <p>Want to speak instead of type? That is dictation - superwhisper, or the dictation already built into macOS.</p>
  <p>Have a recording sitting on disk? That is file transcription - MacWhisper, or Buzz if you want free and open source.</p>
  <p>Want your meetings captured as they happen, with notes and a summary you can search later? That is a different job, and it is the one TNN is built for.</p>
</div>

<h2>Three jobs that look identical on a feature list</h2>

<p>Every app in this space says "Whisper, on-device, private". That tells you the engine, not the product. What separates them is where the audio comes from and what you get at the end.</p>

<h3>Job one: dictation</h3>

<p>You want to speak and have text appear where your cursor is. The audio source is your microphone, the output is a sentence, and speed matters more than anything.</p>

<p>macOS has this built in and it is genuinely decent. Apps like superwhisper exist because they are more accurate, work in any text field with a hotkey, and let you shape the output with prompts. superwhisper runs offline models well on Apple Silicon; on Intel Macs it leans on cloud models, which is worth knowing if privacy is the reason you are here.</p>

<p>TNN includes a quick dictation hotkey too, but if dictation is the <em>whole</em> job, a dedicated dictation app will beat it.</p>

<h3>Job two: transcribing files you already have</h3>

<p>You have an interview, a voice memo, a webinar recording. The audio source is a file, and you want text out with decent speaker handling.</p>

<p>MacWhisper is the well-known Mac answer, running Whisper locally over audio and video files. Buzz is the open-source one: MIT licensed, free, transcribes files offline with Whisper, and also does live microphone transcription. Buzz runs on macOS, Windows and Linux, which none of the Mac-only options do.</p>

<p>TNN transcribes existing audio files as well, so if that is an occasional task alongside meetings you are covered. If it is your <em>main</em> task, especially in bulk, a file-first tool is the better fit.</p>

<h3>Job three: live meetings</h3>

<p>This is the one the other categories cannot reach, and it is where most of the frustration in this search comes from.</p>

<p>A meeting is not a microphone and not a file. The audio you need is what your <em>Mac</em> is playing - the other people on the call - plus your own mic. You need it to start when the meeting starts, to know which meeting it was, and to end up as something you can find in three months.</p>

<p>A dictation app cannot do this, because it listens to you. A file transcriber cannot do this, because there is no file until afterwards. Buzz gets closer with live microphone transcription, but a microphone does not capture the person on the other end of Zoom.</p>

{{TABLE}}

<h2>What "on-device" is worth, and where it stops</h2>

<p>The honest case for local transcription is narrow and real. Your audio never becomes someone else's asset. There is no subprocessor to declare on a security questionnaire, no per-minute meter, and it keeps working on a plane. If your meetings include candidate interviews, compensation conversations, undisclosed incidents, or clients whose NDA enumerates processors, that matters more than any feature comparison.</p>

<p>What local processing does <em>not</em> buy you: a shared team archive, recordings of meetings you did not attend, or the polish of a company with a hundred engineers. Those are real trade-offs, not marketing asterisks.</p>

<blockquote>Bot-free and local are two different things, and the apps that blur them are usually only one of the two.</blockquote>

<h2>How TNN differs from the rest of this list</h2>

<p>TNN is the only one here whose unit of work is a meeting rather than a recording. It captures system audio so no bot joins the call, reads your calendar so it knows which meeting is starting, and writes one plain Markdown file per meeting containing your live notes, the transcript and an AI summary together.</p>

<p>The file format is the part that pays off later. Because meetings are plain text on your disk, TNN can expose them to Claude over MCP: Claude lists your meetings, reads notes and transcripts, runs skills you have saved, and writes results back into the meeting file. Ask what you promised a client across four calls and the answer comes from transcripts. That runs on your own Claude Pro or Max subscription, so there is no API key and no AI fee from us.</p>

<h2>Pick by this, not by the feature list</h2>

<ul>
  <li><strong>Mostly dictating</strong> - macOS dictation first, then superwhisper if you want better accuracy and hotkeys everywhere.</li>
  <li><strong>Mostly transcribing files</strong> - MacWhisper on Mac, or Buzz if you want free, open source, and cross-platform.</li>
  <li><strong>Mostly in meetings</strong> - TNN, or a cloud notetaker if you need a team workspace and do not mind the audio leaving your machine.</li>
  <li><strong>Not on Apple Silicon</strong> - Buzz. Most of this category, TNN included, is Apple Silicon first.</li>
</ul>
""",
        "faq": [
            ("What is the best offline transcription app for Mac?",
             "It depends which job you have. For dictation, macOS's built-in dictation or superwhisper. For transcribing files you already have, MacWhisper, or Buzz if you want free and open source. For live meetings captured as searchable notes, TNN. No single app is best at all three."),
            ("Is there a free offline transcription app for Mac?",
             "Yes. Buzz is MIT licensed and free, transcribes files offline with Whisper, and also does live microphone transcription across macOS, Windows and Linux. macOS also has dictation built in at no cost. TNN is free while its beta runs."),
            ("Do offline transcription apps work without internet?",
             "Once the model is downloaded, yes. TNN downloads its transcription model once, roughly 600 MB, and then records and transcribes with wifi off. Watch for hybrid apps: some run local models on Apple Silicon but fall back to cloud models on Intel Macs, which defeats the point if privacy is why you wanted local."),
        ],
    },

    # ------------------------------------------------------------------
    {
        "slug": "ai-notetaker-without-bot",
        "type": "guide",
        "tag": "Guide",
        "title": "AI notetakers without a bot: what that actually means",
        "seo_title": "AI Note Taker With No Bot: Bot-Free vs Local (2026) - TNN",
        "description": "Bot-free and private are not the same thing. Here is the two-axis map of AI notetakers - does a bot join, and where is the audio processed - with where every major tool sits.",
        "date": "2026-07-30",
        "date_label": "30 July 2026",
        "read": "5 min read",
        "checked": "July 2026",
        "lede": "No bot has become the headline feature of the whole category, and it has quietly stopped meaning much. Plenty of tools now capture your device's audio instead of dialling into the call, and then upload that audio to their servers anyway. If you went looking for a notetaker without a bot because you wanted the conversation to stay yours, the bot was never the thing to check.",
        "table": {
            "headers": ["Tool", "Bot joins the call", "Where audio is processed", "What you were probably looking for"],
            "rows": [
                ["Otter.ai", "Yes", "Vendor cloud", "Neither"],
                ["Fireflies.ai", "Yes", "Vendor cloud", "Neither"],
                ["tl;dv", "Yes", "Vendor cloud", "Neither"],
                ["Granola", "No, captures device audio", "Vendor cloud", "Bot-free"],
                ["Jamie", "No, captures device audio", "Vendor cloud", "Bot-free"],
                ["Meetily", "No, captures system audio", "On your machine", "Both"],
                ["TNN", "No, captures system audio", "On your Mac", "Both"],
            ],
            "tnn_col": 3,
            "caption": "Positioning checked July 2026 from each vendor's own description of how capture works. This is about architecture, not quality - several cloud tools here are excellent at their job.",
        },
        "body": """
<div class="callout">
  <span class="callout__label">The short answer</span>
  <p>There are two separate questions, and the marketing collapses them into one.</p>
  <p><strong>Does a bot join?</strong> That is about social friction: who sees a recorder in the participant list, who has to admit it, whether the client notices.</p>
  <p><strong>Where is the audio processed?</strong> That is about privacy: whether your conversation becomes a file on someone else's server.</p>
  <p>Most "no bot" tools solve the first and not the second.</p>
</div>

<h2>Why the bot became the headline</h2>

<p>For years every AI notetaker worked the same way: it dialled into your Zoom, Meet or Teams call as a participant, recorded from inside, and produced a transcript. Otter, Fireflies and tl;dv all still work this way.</p>

<p>The problems are social, and they show up weekly. Someone has to admit the bot from the waiting room. External guests see an account they do not recognise and ask what it is. A client on a sensitive call notices a recorder in the attendee list and the conversation changes temperature. And when the bot fails to join, you discover it afterwards, with no recording.</p>

<p>So a second generation built capture differently: listen to the audio the computer is already playing. Nothing joins, nothing appears in the list, and it works on any meeting app because there is no integration to break. Granola made this mainstream. Jamie works the same way. TNN works the same way.</p>

<p>This is a genuine improvement, and it is the reason "no bot" sells.</p>

<h2>The part that got lost</h2>

<p>Capturing device audio says nothing about what happens to that audio next.</p>

<p>A bot-free tool can still upload your recording, transcribe it in its cloud, summarise it with its own models, and store the result in its workspace. Architecturally, the audio is in the same place it would have been with a bot. You removed the recorder from the participant list, not from the internet.</p>

<p>For most meetings that is a perfectly reasonable trade. It stops being reasonable in specific situations, and if you searched for this you probably have one in mind: a candidate interview, a compensation conversation, an incident that has not been disclosed, a client under an NDA that enumerates third-party processors, a security review asking you to list every service that touches customer voices.</p>

<p>In those cases the question is not "does a bot join". It is "can I answer where the audio is stored with the word nowhere".</p>

{{TABLE}}

<h2>The two-axis map</h2>

<p>Read the table as a grid rather than a ranking.</p>

<ul>
  <li><strong>Bot plus cloud.</strong> Otter, Fireflies, tl;dv. Maximum reach: they can record a meeting you did not attend, run on any platform, and give a team one searchable archive. Maximum exposure too.</li>
  <li><strong>Bot-free plus cloud.</strong> Granola, Jamie. The social problem is solved and the product is usually excellent. The audio still leaves your machine.</li>
  <li><strong>Bot-free plus local.</strong> Meetily, TNN. Nothing joins the call and nothing leaves the laptop. The cost is real: no team workspace, no recording meetings you skipped, and a much smaller company behind it.</li>
</ul>

<blockquote>If the reason you typed "without bot" was privacy rather than etiquette, the second column is the one to read.</blockquote>

<h2>One thing no architecture fixes</h2>

<p>A recorder that other participants cannot see does not reduce your obligation to tell them. Consent rules vary by country and by state, and in several places everyone in the conversation has to agree. "Nothing appeared in the participant list" is not a defence.</p>

<p>Being invisible to Zoom is a convenience feature. Saying "I am recording this for notes" at the top of the call is the actual requirement, and it takes four seconds.</p>

<h2>Where TNN sits</h2>

<p>Bottom-right of that grid, deliberately. No bot joins, because TNN captures the audio your Mac plays. Transcription runs on the Neural Engine with Whisper, so the audio never leaves the machine and there is no server to enumerate. Each meeting becomes one plain Markdown file - your notes, the transcript, the AI summary - in a folder you choose.</p>

<p>Because the files are plain text, Claude can work with the whole archive over MCP, on your own Claude Pro or Max subscription. And the trade-offs are the ones listed above: macOS 13 or later on Apple Silicon, single-user, audio only, still in beta.</p>

<h2>Read the head-to-heads</h2>

<p>If you already have a tool in mind, the detailed version lives here:
<a href="/blog/granola-alternative/">vs Granola</a>,
<a href="/blog/otter-ai-alternative/">vs Otter.ai</a>,
<a href="/blog/fireflies-alternative/">vs Fireflies</a>,
<a href="/blog/tldv-alternative/">vs tl;dv</a>.
Each one ends with the cases where that tool is still the better choice.</p>
""",
        "faq": [
            ("What is the best AI note taker with no bot?",
             "It depends on why you want no bot. If it is about not having a recorder in the participant list, Granola and Jamie are strong and polished, though they still process audio in their cloud. If it is because you want the audio to stay on your machine, you need a tool that is both bot-free and local, which narrows it to options like Meetily and TNN."),
            ("Does bot-free mean my meeting is private?",
             "No, and this is the most common misunderstanding in the category. Bot-free describes how the audio is captured, not where it goes afterwards. Several bot-free tools upload the recording and transcribe it on their servers. If privacy is the goal, check where processing happens, not whether something appears in the attendee list."),
            ("Can an AI notetaker record without joining the meeting?",
             "Yes. Instead of dialling in as a participant, it captures the audio your computer is already playing. Nothing appears in the participant list, there is no waiting room to clear, and it works on any meeting app, including a phone call on speaker or a conversation in the room. It also means you have to be in the meeting yourself, since there is no bot to attend on your behalf."),
        ],
    },
]

# ============================================================
# TEMPLATE PIECES
# ============================================================

GTAG = "G-HP9XZCGX2S"

HEAD_SCRIPTS = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '%s');
  </script>

  <!-- MailerLite Universal (powers the mobile download modal) -->
  <script>
    (function(w,d,e,u,f,l,n){w[f]=w[f]||function(){(w[f].q=w[f].q||[])
    .push(arguments);},l=d.createElement(e),l.async=1,l.src=u,
    n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);})
    (window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');
    ml('account', '2363499');
  </script>""" % (GTAG, GTAG)

FONTS = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Ancizar+Serif:ital,wght@0,400;0,600;1,400;1,600&family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/chrome.css">
  <link rel="stylesheet" href="/css/blog.css">"""

NAV = """<header>
  <nav class="nav" id="nav">
    <a href="/" class="nav__logo">
      <img src="/assets/logo-dark.svg" alt="Thoughts Not Notes" class="nav__logo-img">
    </a>
    <div class="nav__right">
      <nav class="nav__links" aria-label="Main navigation">
        <a href="/#how-it-works" class="nav__link">How it works</a>
        <a href="/#features" class="nav__link">Features</a>
        <a href="/#pricing" class="nav__link">Pricing</a>
        <a href="/blog/" class="nav__link">Blog</a>
        <a href="/#faq" class="nav__link">FAQ</a>
      </nav>
      <button class="theme-toggle" data-theme-toggle aria-label="Toggle dark mode" type="button">
        <svg class="theme-toggle__icon theme-toggle__icon--moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
        <svg class="theme-toggle__icon theme-toggle__icon--sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="4"/>
          <line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/>
          <line x1="4.93" y1="4.93" x2="6.34" y2="6.34"/><line x1="17.66" y1="17.66" x2="19.07" y2="19.07"/>
          <line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/>
          <line x1="4.93" y1="19.07" x2="6.34" y2="17.66"/><line x1="17.66" y1="6.34" x2="19.07" y2="4.93"/>
        </svg>
      </button>
      <button class="btn btn--nav" data-modal-open><img src="/assets/icons/apple.svg" width="13" height="13" alt="" aria-hidden="true" class="btn-apple-icon"> Download for Mac</button>
    </div>
  </nav>
</header>"""

FOOTER = """<footer class="site-footer">
  <span>&copy; 2026 Thoughts Not Notes</span>
  <span>
    <a href="/blog/">Blog</a>
    &nbsp;&middot;&nbsp;
    <a href="/privacy.html">Privacy</a>
    &nbsp;&middot;&nbsp;
    <a href="/terms.html">Terms</a>
    &nbsp;&middot;&nbsp;
    <a href="https://thoughtsnotnotes.com">thoughtsnotnotes.com</a>
  </span>
</footer>"""

MODALS = """<!-- Mobile: collect the email, MailerLite mails the download link -->
<div id="mobile-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="mobile-modal-title">
  <div class="modal">
    <button class="modal__close" aria-label="Close" data-modal-close>&times;</button>
    <div class="modal__icon" aria-hidden="true">&#128187;</div>
    <h3 class="modal__title" id="mobile-modal-title">TNN is for Mac</h3>
    <p class="modal__sub">The app requires macOS 13 or later. Drop your email and we'll send the download link - open it on your Mac.</p>
    <div class="ml-embedded" data-form="GQaCbC"></div>
  </div>
</div>

<!-- Desktop: email gate, then /thanks.html starts the DMG download -->
<div id="gate-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="gate-modal-title">
  <div class="modal">
    <button class="modal__close" aria-label="Close" data-modal-close>&times;</button>
    <div class="modal__icon" aria-hidden="true">&#128075;</div>
    <h3 class="modal__title" id="gate-modal-title">One thing before you download</h3>
    <p class="modal__sub">TNN is free while we build it. The only thing we ask for is your email - so we can hear how it works for you and make it fit the way <em>you</em> work.</p>
    <form class="gate-form" id="gate-form">
      <input type="email" required placeholder="you@company.com" class="gate-input" id="gate-input" autocomplete="email">
      <button type="submit" class="modal__submit gate-submit">
        <img src="/assets/icons/apple.svg" width="15" height="15" alt="" aria-hidden="true" class="btn-apple-icon">
        Start the download
      </button>
    </form>
    <p class="gate-note">No spam, no newsletter - we'll only reach out about your feedback.</p>
  </div>
</div>"""

SCRIPTS = """<script src="/js/main.js?v=20260729" defer></script>
<script src="/js/blog.js?v=20260729" defer></script>"""

CTA = """<section class="blog-cta">
  <h2>Try it on your next meeting</h2>
  <p>Records and transcribes on your Mac. No bot in the call, no cloud, no subscription for transcription. Free while the beta runs.</p>
  <button class="btn btn--primary" data-modal-open>
    <img src="/assets/icons/apple.svg" width="15" height="15" alt="" aria-hidden="true" class="btn-apple-icon">
    Download for Mac
  </button>
  <div class="blog-cta__meta">
    <span>Free during beta</span>
    <span class="blog-cta__sep" aria-hidden="true">&middot;</span>
    <span>macOS 13+</span>
    <span class="blog-cta__sep" aria-hidden="true">&middot;</span>
    <span>Apple Silicon</span>
  </div>
</section>"""


# ============================================================
# RENDERERS
# ============================================================

def head(title, description, url, extra_ld=""):
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/svg+xml" href="/assets/logo-icon.svg">
  <link rel="apple-touch-icon" href="/assets/logo-icon.svg">

{scripts}

  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index,follow,max-image-preview:large">

  <meta property="og:site_name" content="Thoughts Not Notes">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{site}/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{site}/assets/og-image.png">

  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#171717" media="(prefers-color-scheme: dark)">

{fonts}
{ld}
</head>
<body>
""".format(
        scripts=HEAD_SCRIPTS,
        title=html.escape(title, quote=True),
        description=html.escape(description, quote=True),
        url=url,
        site=SITE,
        fonts=FONTS,
        ld=extra_ld,
    )


def ld_block(obj):
    return '\n  <script type="application/ld+json">\n' + \
        json.dumps(obj, indent=2, ensure_ascii=False) + "\n  </script>\n"


def render_table(spec, checked):
    """Two shapes are accepted.

    Head-to-head:  {"competitor": "Otter.ai", "rows": [(label, them, us), ...]}
    Wide:          {"headers": [...], "rows": [[...], ...], "tnn_col": 3}

    tnn_col is a 0-indexed column to highlight. Pass None for no highlight.
    An explicit "caption" overrides the default pricing disclaimer.
    """
    if "competitor" in spec:
        headers = ["&nbsp;", html.escape(spec["competitor"]), "TNN"]
        rows = [[label, a, b] for label, a, b in spec["rows"]]
        tnn_col = 2
        caption = spec.get(
            "caption",
            "%s pricing and limits checked %s against public pricing pages. "
            "Vendors change plans often - verify before you decide."
            % (html.escape(spec["competitor"]), checked),
        )
    else:
        headers = [html.escape(h) for h in spec["headers"]]
        rows = spec["rows"]
        tnn_col = spec.get("tnn_col")
        caption = spec.get("caption", "")

    def cell(tag, text, i):
        cls = ' class="col-tnn"' if tnn_col is not None and i == tnn_col else ""
        return "<%s%s>%s</%s>" % (tag, cls, text, tag)

    out = ['<div class="cmp">', "  <table>", "    <thead>", "      <tr>"]
    out += ["        " + cell("th", h, i) for i, h in enumerate(headers)]
    out += ["      </tr>", "    </thead>", "    <tbody>"]
    for row in rows:
        out.append("      <tr>")
        for i, val in enumerate(row):
            out.append("        " + cell("th" if i == 0 else "td", html.escape(str(val)), i))
        out.append("      </tr>")
    out += ["    </tbody>", "  </table>", "</div>"]
    if caption:
        out.append('<p class="cmp__caption">%s</p>' % caption)
    return "\n".join(out)


def render_faq(faq):
    items = []
    for q, a in faq:
        items.append(
            '        <details class="faq-q">\n'
            '          <summary>%s<span class="faq-q__chev" aria-hidden="true"></span></summary>\n'
            '          <p>%s</p>\n'
            '        </details>' % (html.escape(q), a)
        )
    return (
        '      <section class="article-faq">\n'
        '        <h2>Questions people ask</h2>\n'
        + "\n".join(items) + "\n"
        '      </section>'
    )


def render_related(current_slug):
    others = [p for p in POSTS if p["slug"] != current_slug][:4]
    items = []
    for p in others:
        items.append(
            '          <a class="related__item" href="/blog/%s/">\n'
            '            <span>%s</span>\n'
            '            <em>%s</em>\n'
            '          </a>' % (p["slug"], html.escape(p["title"]), p["read"])
        )
    return (
        '      <nav class="related" aria-label="More comparisons">\n'
        '        <p class="related__label">More comparisons</p>\n'
        '        <div class="related__list">\n'
        + "\n".join(items) + "\n"
        '        </div>\n'
        '      </nav>'
    )


def word_count(body):
    return len(re.sub(r"<[^>]+>", " ", body).split())


def render_post(p):
    url = "%s/blog/%s/" % (SITE, p["slug"])
    ld = ld_block({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": url + "#post",
                "headline": p["title"],
                "description": p["description"],
                "url": url,
                "mainEntityOfPage": url,
                "datePublished": p["date"],
                "dateModified": p["date"],
                "image": SITE + "/assets/og-image.png",
                "inLanguage": "en",
                "author": {"@type": "Organization", "name": "Thoughts Not Notes", "url": SITE + "/"},
                "publisher": {
                    "@type": "Organization",
                    "name": "Thoughts Not Notes",
                    "url": SITE + "/",
                    "logo": SITE + "/assets/logo-dark.svg",
                },
                "about": {"@type": "SoftwareApplication", "name": "Thoughts Not Notes",
                          "operatingSystem": "macOS 13.0 or later, Apple Silicon",
                          "applicationCategory": "BusinessApplication"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                    {"@type": "ListItem", "position": 3, "name": p["title"], "item": url},
                ],
            },
            {
                "@type": "FAQPage",
                "@id": url + "#faq",
                "mainEntity": [
                    {"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer",
                                        "text": re.sub(r"<[^>]+>", "", a)}}
                    for q, a in p["faq"]
                ],
            },
        ],
    })

    body = p["body"].strip()
    if "{{TABLE}}" not in body:
        raise SystemExit("post %r has no {{TABLE}} placeholder" % p["slug"])
    body = body.replace("{{TABLE}}", render_table(p["table"], p["checked"]))

    return (
        head(p["seo_title"], p["description"], url, ld)
        + NAV + "\n\n"
        + '<main class="blog-shell">\n'
        + '  <article class="blog-wrap">\n'
        + '    <nav class="crumbs" aria-label="Breadcrumb">\n'
        + '      <a href="/">Home</a><span class="crumbs__sep">/</span>'
        + '<a href="/blog/">Blog</a><span class="crumbs__sep">/</span>'
        + '<span>%s</span>\n' % html.escape(p["tag"])
        + '    </nav>\n'
        + '    <p class="eyebrow">%s</p>\n' % html.escape(p["tag"])
        + '    <h1 class="article__title">%s</h1>\n' % html.escape(p["title"])
        + '    <p class="article__meta"><span>%s</span><span class="crumbs__sep">&middot;</span>'
          '<span>%s</span><span class="crumbs__sep">&middot;</span>'
          '<span>Pricing checked %s</span></p>\n' % (p["date_label"], p["read"], p["checked"])
        + '    <p class="article__lede">%s</p>\n' % html.escape(p["lede"])
        + '    <div class="prose">\n' + body + "\n    </div>\n"
        + CTA + "\n"
        + render_faq(p["faq"]) + "\n"
        + render_related(p["slug"]) + "\n"
        + '  </article>\n</main>\n\n'
        + FOOTER + "\n\n" + MODALS + "\n\n" + SCRIPTS + "\n</body>\n</html>\n"
    )


def render_hub():
    url = SITE + "/blog/"
    ld = ld_block({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Blog",
                "@id": url + "#blog",
                "name": "Thoughts Not Notes Blog",
                "description": "Honest comparisons of meeting transcription tools, with a bias we state up front.",
                "url": url,
                "inLanguage": "en",
                "publisher": {"@type": "Organization", "name": "Thoughts Not Notes", "url": SITE + "/"},
                "blogPost": [
                    {"@type": "BlogPosting", "headline": p["title"],
                     "url": "%s/blog/%s/" % (SITE, p["slug"]),
                     "datePublished": p["date"], "description": p["description"]}
                    for p in POSTS
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": url},
                ],
            },
        ],
    })

    def card(p, wide=False):
        return (
            '        <a class="post-card%s" href="/blog/%s/">\n'
            '          <span class="post-card__tag">%s</span>\n'
            '          <h3 class="post-card__title">%s</h3>\n'
            '          <p class="post-card__sub">%s</p>\n'
            '          <p class="post-card__meta"><span>%s</span>'
            '<span class="crumbs__sep">&middot;</span><span>%s</span>'
            '<span class="post-card__arrow" aria-hidden="true">&rarr;</span></p>\n'
            '        </a>' % (
                ' post-card--wide' if wide else '', p["slug"],
                html.escape(p["tag"]), html.escape(p["title"]),
                html.escape(p["lede"].split(". ")[0] + "."), p["date_label"], p["read"],
            )
        )

    sections = []
    for key, heading, blurb in SECTIONS:
        group = [p for p in POSTS if p.get("type", "comparison") == key]
        if not group:
            continue
        cards = [card(p, wide=(i == 0 and len(group) % 2 == 1)) for i, p in enumerate(group)]
        sections.append(
            '      <section class="hub-section">\n'
            '        <h2 class="hub-section__title">%s</h2>\n'
            '        <p class="hub-section__blurb">%s</p>\n'
            '      </section>\n'
            '      <div class="hub-grid">\n%s\n      </div>'
            % (html.escape(heading), html.escape(blurb), "\n".join(cards))
        )

    return (
        head(
            "Blog - Meeting Transcription Tools, Compared Honestly | TNN",
            "Comparisons of Granola, Otter.ai, Fireflies and tl;dv against a local, on-device alternative - including where each competitor is still the better choice.",
            url, ld,
        )
        + NAV + "\n\n"
        + '<main class="blog-shell">\n'
        + '  <div class="blog-wrap blog-wrap--wide">\n'
        + '    <nav class="crumbs" aria-label="Breadcrumb">\n'
        + '      <a href="/">Home</a><span class="crumbs__sep">/</span><span>Blog</span>\n'
        + '    </nav>\n'
        + '    <header class="hub-head">\n'
        + '      <p class="eyebrow">Blog</p>\n'
        + '      <h1>Meeting tools, compared honestly</h1>\n'
        + '      <p>We build a meeting recorder, so we are not neutral and we are not going to '
          'pretend to be. What we can do is get the facts right, tell you plainly when a '
          'competitor is the better choice for you, and write the how-to guides we wanted '
          'when we started. Every comparison here ends with where the other tool wins.</p>\n'
        + '    </header>\n'
        + "\n".join(sections) + "\n"
        + CTA + "\n"
        + '  </div>\n</main>\n\n'
        + FOOTER + "\n\n" + MODALS + "\n\n" + SCRIPTS + "\n</body>\n</html>\n"
    )


# ============================================================
# WRITE
# ============================================================

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("  %-46s %5d words" % (path, word_count(content)))


if __name__ == "__main__":
    print("Building blog...")
    write("blog/index.html", render_hub())
    for post in POSTS:
        write("blog/%s/index.html" % post["slug"], render_post(post))

    print("\nsitemap.xml entries:")
    print("  <url><loc>%s/blog/</loc><lastmod>%s</lastmod>"
          "<changefreq>weekly</changefreq><priority>0.8</priority></url>" % (SITE, BUILT))
    for post in POSTS:
        print("  <url><loc>%s/blog/%s/</loc><lastmod>%s</lastmod>"
              "<changefreq>monthly</changefreq><priority>0.7</priority></url>"
              % (SITE, post["slug"], post["date"]))
