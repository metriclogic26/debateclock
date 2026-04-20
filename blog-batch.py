#!/usr/bin/env python3
"""
Generates 2 blog posts + adds cross-links to format guide pages.

Run from project root: python3 blog-batch.py
"""
import pathlib, re

NAV = """<nav class="site-nav">
  <a class="brand" href="/"><span class="brand-dot"></span>DebateClock</a>
  <div class="nav-links">
    <div class="nav-dropdown">
      <button class="nav-dropdown-trigger">Competition &#9662;</button>
      <div class="nav-dropdown-menu">
        <div class="nav-dropdown-section">Timer</div>
        <a href="/app/">Two-device timer <span class="tag">Live</span></a>
        <a href="/setup/judge-paradigm/">Tabroom paradigm setup</a>
        <div class="nav-dropdown-section">US Formats</div>
        <a href="/timer/lincoln-douglas/">Lincoln-Douglas</a>
        <a href="/timer/policy-debate/">Policy (CX)</a>
        <a href="/timer/public-forum/">Public Forum</a>
        <a href="/timer/parliamentary/">Parliamentary</a>
        <div class="nav-dropdown-section">International</div>
        <a href="/timer/world-schools/">World Schools (WSDC)</a>
        <a href="/timer/british-parliamentary/">British Parliamentary</a>
        <a href="/timer/asian-parliamentary/">Asian Parliamentary</a>
        <a href="/timer/canadian-parliamentary/">Canadian (CUSID)</a>
      </div>
    </div>
    <div class="nav-dropdown">
      <button class="nav-dropdown-trigger">Practice &#9662;</button>
      <div class="nav-dropdown-menu">
        <div class="nav-dropdown-section">Practice Tools</div>
        <a href="/practice/motion/">Motion practice timer <span class="tag">New</span></a>
        <a href="/practice/extemp/">Extemp prep room clock <span class="tag">New</span></a>
        <a href="/practice/round-logger/">Round logger <span class="tag">New</span></a>
        <a href="/practice/flow/">Flow timer <span class="tag">New</span></a>
        <a href="/practice/tournament/">Tournament schedule <span class="tag">New</span></a>
      </div>
    </div>
  </div>
  <a class="nav-cta" href="/app/">Open timer</a>
</nav>"""

DISCLAIMER = """<div class="site-disclaimer">
  Informational timing aid only &middot; Not affiliated with NSDA, WUDC, WSDC, CUSID, or Tabroom &middot; Always defer to the tournament director for timing disputes &middot; <a href="/terms/">Terms &amp; Privacy</a>
</div>"""

FOOTER = """<footer class="site-footer">
  <div class="footer-cols">
    <div class="footer-col">
      <h4>Format Guides</h4>
      <a href="/formats/lincoln-douglas/">Lincoln-Douglas guide</a>
      <a href="/formats/public-forum/">Public Forum guide</a>
      <a href="/formats/world-schools/">World Schools guide</a>
      <a href="/formats/british-parliamentary/">British Parliamentary guide</a>
    </div>
    <div class="footer-col">
      <h4>Timers</h4>
      <a href="/timer/lincoln-douglas/">LD timer</a>
      <a href="/timer/public-forum/">PF timer</a>
      <a href="/timer/world-schools/">WSDC timer</a>
      <a href="/timer/british-parliamentary/">BP timer</a>
    </div>
    <div class="footer-col">
      <h4>Practice</h4>
      <a href="/practice/motion/">Motion timer</a>
      <a href="/practice/round-logger/">Round logger</a>
      <a href="/practice/tournament/">Tournament schedule</a>
    </div>
  </div>
  <div class="footer-row">
    <div><a href="/" style="display:inline-flex;align-items:center;gap:8px;color:var(--muted);text-decoration:none;"><span style="width:12px;height:12px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);"></span>DebateClock</a><span style="margin-left:12px;">free browser debate timer</span></div>
    <a href="https://tally.so/r/QKAMOX" target="_blank" rel="noopener" class="feedback-btn">&#9733; Give feedback</a>
  </div>
</footer>"""

HEAD_COMMON = """  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/site.css">
  <style>
    .content-wrap { max-width: 760px; margin: 0 auto; padding: 40px 24px 80px; }
    .content-wrap h1 { font-size: 32px; font-weight: 700; margin-bottom: 12px; line-height: 1.2; }
    .content-wrap h2 { font-size: 20px; font-weight: 700; margin: 36px 0 12px; }
    .content-wrap h3 { font-size: 16px; font-weight: 600; margin: 24px 0 8px; }
    .content-wrap p { font-size: 15px; color: var(--muted, #8B90A0); line-height: 1.75; margin-bottom: 16px; }
    .content-wrap ul, .content-wrap ol { margin: 0 0 16px 20px; }
    .content-wrap li { font-size: 15px; color: var(--muted, #8B90A0); line-height: 1.75; margin-bottom: 6px; }
    .content-wrap strong { color: #E8EAF0; }
    .content-wrap a { color: #3B82F6; }
    .cta-box { background: #111318; border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 28px; margin: 36px 0; text-align: center; }
    .cta-box h3 { font-size: 18px; margin-bottom: 8px; color: #E8EAF0; }
    .cta-box p { margin-bottom: 20px; }
    .cta-box a.btn { display: inline-block; background: #22C55E; color: #04140a; font-weight: 700; padding: 12px 28px; border-radius: 10px; text-decoration: none; font-size: 15px; }
    .faq details { background: #111318; border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 14px 18px; margin-bottom: 8px; }
    .faq summary { font-size: 14px; font-weight: 600; color: #E8EAF0; cursor: pointer; list-style: none; }
    .faq summary::after { content: ' +'; color: #5B6175; }
    .faq details[open] summary::after { content: ' -'; }
    .faq details div { font-size: 14px; color: #8B90A0; line-height: 1.7; margin-top: 10px; }
    .compare-table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }
    .compare-table th { font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #5B6175; padding: 10px 14px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .compare-table td { padding: 12px 14px; color: #E8EAF0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 14px; line-height: 1.5; }
    .compare-table td:first-child { font-weight: 600; color: #8B90A0; font-size: 13px; }
    .badge-green { background: rgba(34,197,94,0.12); color: #22C55E; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
    .badge-blue  { background: rgba(59,130,246,0.12); color: #3B82F6; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
    .prep-demo { background: #0A0C0F; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px 24px; margin: 20px 0; font-family: 'DM Mono', monospace; font-size: 13px; }
    .prep-demo .row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .prep-demo .row:last-child { border-bottom: none; }
    .prep-demo .event { color: #8B90A0; }
    .prep-demo .pool { color: #22C55E; }
    .prep-demo .pool.used { color: #F59E0B; }
  </style>"""

# ── BLOG 1: Prep time pool explainer ─────────────────────────────────────────
PREP_BLOG = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shared Prep Time Pool in Debate: How It Works | DebateClock</title>
<meta name="description" content="What is a shared prep time pool in debate? How prep time works in LD, Policy, and Public Forum — and how to track it accurately during a round.">
<link rel="canonical" href="https://debateclock.org/blog/debate-timer-prep-time/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"Shared Prep Time Pool in Debate: How It Works","description":"What is a shared prep time pool in debate? How prep time works in LD, Policy, and Public Forum.","url":"https://debateclock.org/blog/debate-timer-prep-time/"}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{{"@type":"Question","name":"What is a prep time pool in debate?","acceptedAnswer":{{"@type":"Answer","text":"A prep time pool is a shared bank of time that a debater or team can draw from before any of their speeches. Unlike a per-speech countdown, the pool is shared across the entire round."}}}},
{{"@type":"Question","name":"How much prep time do debaters get in LD?","acceptedAnswer":{{"@type":"Answer","text":"Each debater gets 4 minutes of prep time in Lincoln-Douglas debate, distributed freely across the round."}}}},
{{"@type":"Question","name":"How much prep time do teams get in Policy debate?","acceptedAnswer":{{"@type":"Answer","text":"Each team gets 8 minutes of prep time in Policy debate, shared between both partners."}}}}
]}}
</script>
{HEAD_COMMON}
</head>
<body>
{NAV}
<div class="content-wrap">
  <div style="font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#5B6175;margin-bottom:12px;">Blog</div>
  <h1>Shared prep time pool in debate: how it works</h1>
  <p>Prep time is one of the most misunderstood timing elements in competitive debate. Most mobile timer apps handle it incorrectly — they treat it as a per-speech countdown rather than a shared pool. This guide explains exactly how prep time works in LD, Policy, and Public Forum, and why the shared pool model matters.</p>

  <h2>What is a prep time pool?</h2>
  <p>A prep time pool is a shared bank of time that a debater or team draws from before any of their speeches. The pool is not reset between speeches — it is consumed cumulatively across the entire round. Once it runs out, it is gone.</p>
  <p>This is fundamentally different from a per-speech timer. A per-speech timer gives a debater, say, 2 minutes before each speech independently. A pool gives them 4 minutes total to use however they choose across all their speeches.</p>

  <h2>Prep time rules by format</h2>
  <table class="compare-table">
    <thead><tr><th>Format</th><th>Pool size</th><th>Shared between</th></tr></thead>
    <tbody>
      <tr><td>Lincoln-Douglas</td><td>4 minutes</td><td>Each debater has their own pool</td></tr>
      <tr><td>Policy (CX)</td><td>8 minutes</td><td>Both partners on a team share one pool</td></tr>
      <tr><td>Public Forum</td><td>3 minutes</td><td>Both partners on a team share one pool</td></tr>
      <tr><td>Parliamentary / WSDC / BP</td><td>None</td><td>No prep pool — speeches run back-to-back</td></tr>
    </tbody>
  </table>

  <h2>How prep time is used in practice</h2>
  <p>When a debater or team wants to use prep time, they call "prep" and the judge starts their pool clock. When they are ready to speak, they say "ready" and the judge stops the clock. The remaining time is noted and carries forward to their next prep call.</p>
  <p>In LD, each debater manages their own pool independently. In Policy and PF, the two partners share a single pool — either partner can call prep, and the time counts against the shared pool regardless of which partner uses it.</p>

  <h3>Example: LD round prep usage</h3>
  <div class="prep-demo">
    <div class="row"><span class="event">Before 1AR</span><span class="pool">Aff uses 2:30 &rarr; 1:30 remaining</span></div>
    <div class="row"><span class="event">Before 2AR</span><span class="pool used">Aff uses 1:30 &rarr; 0:00 remaining</span></div>
    <div class="row"><span class="event">Neg before NR</span><span class="pool">Neg uses 3:45 &rarr; 0:15 remaining</span></div>
    <div class="row"><span class="event">Neg pool exhausted</span><span class="pool used">Neg must speak immediately when called</span></div>
  </div>

  <h2>Why most timer apps get this wrong</h2>
  <p>Most mobile debate timer apps treat prep time as a simple countdown that resets each speech. When a debater calls prep, the app starts a 4-minute countdown. When they stop it, the app records nothing — the next time they call prep, they get another 4 minutes.</p>
  <p>This is incorrect. In a real round, a debater who uses 3 minutes before the 1AR has only 1 minute left for the rest of the round. An app that resets the countdown each time will give them 4 full minutes before the 2AR, which is wrong.</p>
  <p>DebateClock uses a proper shared pool model — the pool counts down cumulatively and the remaining time carries forward exactly as the rules require.</p>

  <h2>Tracking prep time as a judge</h2>
  <p>As a judge, your job is to track each debater's (or team's) remaining prep accurately. Here is the correct procedure:</p>
  <ol>
    <li>When a debater calls prep, note the time on your timer and start their pool clock.</li>
    <li>When they say ready, stop the pool clock and note the remaining time.</li>
    <li>Never let a debater use more prep than they have remaining. If they are out, they must begin immediately.</li>
    <li>In Policy and PF, both partners share the pool — track one number per team, not per speaker.</li>
  </ol>
  <p>DebateClock automates all of this. The pool for each side counts down when you tap "Start Prep" and stops when you tap again. The remaining time is always visible and carries forward automatically.</p>

  <div class="cta-box">
    <h3>Free timer with shared prep pool</h3>
    <p>LD, Policy, PF — all formats with correct prep pool logic. Two-device sync. No signup.</p>
    <a class="btn" href="/app/">Open timer &rarr;</a>
  </div>

  <h2>Frequently asked questions</h2>
  <div class="faq">
    <details><summary>What happens when prep time runs out?</summary><div>The debater must begin their speech immediately when called. Running out of prep time is a competitive disadvantage but not a rule violation — the judge simply cannot grant any additional prep.</div></details>
    <details><summary>Can prep time be used during cross-examination?</summary><div>No. Prep time may only be used before a debater's own speeches, not during cross-examination or while the opposing team is speaking.</div></details>
    <details><summary>In Policy, can one partner use all the prep time?</summary><div>Yes. Both partners share a single 8-minute pool, and either partner can use any portion of it. The pool does not split 4 minutes per partner.</div></details>
    <details><summary>What if a debater calls prep but then doesn't use it?</summary><div>The judge should stop the clock as soon as the debater says they are ready, and record only the time actually used. Brief hesitation before a speech should not be charged as prep unless the debater explicitly calls for it.</div></details>
    <details><summary>Does prep time carry over between rounds?</summary><div>No. Prep time resets at the start of each round. Each new round gives every debater or team a fresh pool.</div></details>
  </div>
</div>
{DISCLAIMER}
{FOOTER}
</body>
</html>"""

# ── BLOG 2: WSDC vs BP comparison ────────────────────────────────────────────
WSDCBP_BLOG = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WSDC vs British Parliamentary: Which Format Should Your School Run?</title>
<meta name="description" content="Comparing World Schools (WSDC) and British Parliamentary (BP) debate formats. Team size, speech length, POI rules, difficulty level, and which is better for your school.">
<link rel="canonical" href="https://debateclock.org/blog/wsdc-vs-british-parliamentary/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"WSDC vs British Parliamentary: Which Format Should Your School Run?","description":"Comparing World Schools and British Parliamentary debate formats for schools and coaches.","url":"https://debateclock.org/blog/wsdc-vs-british-parliamentary/"}}
</script>
{HEAD_COMMON}
</head>
<body>
{NAV}
<div class="content-wrap">
  <div style="font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#5B6175;margin-bottom:12px;">Blog</div>
  <h1>WSDC vs British Parliamentary: which format should your school run?</h1>
  <p>If you are starting a debate program outside the US, the two most common international formats you will encounter are World Schools Debating Championships (WSDC) style and British Parliamentary (BP). Both are three-on-three and four-team formats respectively, both use Points of Information, and both are debated in English globally. But they have significant differences that affect which is better suited for your school, circuit, or competition goals.</p>

  <h2>Quick comparison</h2>
  <table class="compare-table">
    <thead><tr><th>Feature</th><th>World Schools (WSDC)</th><th>British Parliamentary (BP)</th></tr></thead>
    <tbody>
      <tr><td>Teams per round</td><td>2 (Proposition vs Opposition)</td><td>4 (OG, OO, CG, CO)</td></tr>
      <tr><td>Speakers per team</td><td>3</td><td>2</td></tr>
      <tr><td>Speech length</td><td>8 min (main), 4 min (reply)</td><td>7 min (university), 5 min (high school)</td></tr>
      <tr><td>Speeches per round</td><td>8</td><td>8</td></tr>
      <tr><td>POI window</td><td>Minutes 1&ndash;7 of main speeches</td><td>Minutes 1&ndash;6 of speeches</td></tr>
      <tr><td>Reply speech</td><td>Yes &mdash; 1st or 2nd speaker only</td><td>No reply speeches</td></tr>
      <tr><td>Prep time</td><td>None in-round</td><td>None in-round</td></tr>
      <tr><td>Motions</td><td>Prepared + impromptu</td><td>Typically impromptu (15 min prep)</td></tr>
      <tr><td>Ranking</td><td>Win/loss per team</td><td>1st/2nd/3rd/4th per team</td></tr>
      <tr><td>Used at</td><td>National teams, school competitions</td><td>University circuits, school competitions</td></tr>
    </tbody>
  </table>

  <h2>Team structure: 2 teams vs 4 teams</h2>
  <p>The most fundamental difference is team structure. WSDC is a two-team format — Proposition vs Opposition — which mirrors traditional competitive debate. BP has four teams competing simultaneously in every round, with two government teams and two opposition teams all ranked against each other.</p>
  <p>For schools, the two-team structure of WSDC is generally easier to manage. You need 6 speakers per round (3 per team) and the outcome is a clear win or loss. BP requires 8 speakers per round (2 per team × 4 teams) and the ranking system is more complex to explain to beginners.</p>
  <p>BP's four-team format also creates a unique strategic challenge: closing teams must extend the debate rather than repeat their opening half, which requires more advanced debating skills. This makes BP harder to teach to novices.</p>

  <h2>Speech length and structure</h2>
  <p>WSDC main speeches are 8 minutes — longer than BP's 7 minutes at university level or 5 minutes at high school level. WSDC also includes reply speeches (4 minutes each), which BP does not have. Reply speeches are a biased summary of the round and require a different skill set from constructive speeches.</p>
  <p>For beginners, shorter speeches are easier to fill. BP high school (5-minute speeches) is often more accessible for new debaters than WSDC's 8-minute requirement.</p>

  <h2>Points of Information</h2>
  <p>Both formats use POIs, but with slightly different windows. WSDC protects the first and last minute of each 8-minute speech (POI window: 1:00–7:00). BP protects the first and last minute of each 7-minute speech (POI window: 1:00–6:00).</p>
  <p>In practice, POI culture differs between the formats. WSDC tends toward more formal, substantive POIs. BP POIs are often shorter and more frequent. Neither format requires debaters to accept POIs, but accepting too few is considered poor style in both.</p>

  <h2>Prepared vs impromptu motions</h2>
  <p>WSDC tournaments use a mix of prepared motions (announced weeks in advance) and impromptu motions (announced 1 hour before the round). The prepared/impromptu split varies by tournament.</p>
  <p>BP rounds are almost always impromptu — teams receive the motion 15 minutes before the round and must construct their case from scratch. This rewards breadth of knowledge and fast thinking over deep topic research.</p>
  <p>For school programs, prepared motions (WSDC-style) allow more curriculum integration and deeper research skills development. BP's impromptu nature is better for developing quick thinking and general knowledge.</p>

  <h2>Which is better for beginners?</h2>
  <p><strong>WSDC is generally better for beginners</strong> because:</p>
  <ul>
    <li>Two-team format is easier to understand (win or lose, not 4-way ranking)</li>
    <li>Prepared motions allow research and preparation</li>
    <li>Reply speeches teach summarization as a distinct skill</li>
    <li>3 speakers per team means more speaking time distributed across the team</li>
  </ul>
  <p><strong>BP is better when:</strong></p>
  <ul>
    <li>You have a large number of debaters and need to run many rooms simultaneously</li>
    <li>You want to participate in university-level circuits</li>
    <li>Your debaters already have WSDC experience and want a new challenge</li>
    <li>You prioritize impromptu thinking and general knowledge over research</li>
  </ul>

  <h2>Which format does DebateClock support?</h2>
  <p>Both. DebateClock has separate presets for WSDC, BP University (7-min), and BP High School (5-min), each with the correct POI window and speech order. The POI badge appears automatically on the debater display at the correct time for each format.</p>

  <div class="cta-box">
    <h3>Free WSDC and BP timers</h3>
    <p>Automatic POI signal, correct speech order, two-device sync. No signup.</p>
    <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;">
      <a class="btn" href="/timer/world-schools/">WSDC timer &rarr;</a>
      <a class="btn" style="background:#3B82F6;color:#fff;" href="/timer/british-parliamentary/">BP timer &rarr;</a>
    </div>
  </div>

  <h2>Related format guides</h2>
  <ul>
    <li><a href="/formats/world-schools/">World Schools (WSDC) complete format guide</a></li>
    <li><a href="/formats/british-parliamentary/">British Parliamentary complete format guide</a></li>
    <li><a href="/timer/asian-parliamentary/">Asian Parliamentary timer</a></li>
    <li><a href="/timer/canadian-parliamentary/">Canadian Parliamentary (CUSID) timer</a></li>
  </ul>

  <h2>Frequently asked questions</h2>
  <div class="faq">
    <details><summary>Can the same debaters compete in both WSDC and BP?</summary><div>Yes. The skills transfer well between formats. Many competitive debaters compete in both. The main adjustment is the team structure (2-team vs 4-team) and the absence of reply speeches in BP.</div></details>
    <details><summary>Which format is used at the World Schools championship?</summary><div>WSDC uses the World Schools format — 3 speakers per team, 8-minute speeches, reply speeches, and a mix of prepared and impromptu motions.</div></details>
    <details><summary>Which format is used at WUDC?</summary><div>The World Universities Debating Championship (WUDC) uses British Parliamentary format — 4 teams of 2 speakers, 7-minute speeches, no reply speeches.</div></details>
    <details><summary>Is Asian Parliamentary similar to WSDC or BP?</summary><div>Asian Parliamentary is closer to WSDC in structure (2 teams, 3 speakers each) but uses 7-minute speeches and has no reply speeches in the traditional format. See the <a href="/timer/asian-parliamentary/">Asian Parliamentary timer</a>.</div></details>
  </div>
</div>
{DISCLAIMER}
{FOOTER}
</body>
</html>"""

# ── Write blog posts ──────────────────────────────────────────────────────────
pages = [
    ("blog/debate-timer-prep-time/index.html", PREP_BLOG),
    ("blog/wsdc-vs-british-parliamentary/index.html", WSDCBP_BLOG),
]

for path, content in pages:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print(f"ok: {path}")

# ── Add cross-links to format guide pages ─────────────────────────────────────
RELATED = {
    "formats/lincoln-douglas/index.html": """  <h2>Related guides</h2>
  <ul>
    <li><a href="/formats/public-forum/">Public Forum format guide</a></li>
    <li><a href="/blog/debate-timer-prep-time/">How shared prep time pools work</a></li>
    <li><a href="/blog/tournament-day-setup/">How to set up a debate timer for tournament day</a></li>
    <li><a href="/timer/policy-debate/">Policy (CX) timer</a></li>
  </ul>""",
    "formats/public-forum/index.html": """  <h2>Related guides</h2>
  <ul>
    <li><a href="/formats/lincoln-douglas/">Lincoln-Douglas format guide</a></li>
    <li><a href="/blog/debate-timer-prep-time/">How shared prep time pools work</a></li>
    <li><a href="/blog/tournament-day-setup/">How to set up a debate timer for tournament day</a></li>
    <li><a href="/timer/policy-debate/">Policy (CX) timer</a></li>
  </ul>""",
    "formats/world-schools/index.html": """  <h2>Related guides</h2>
  <ul>
    <li><a href="/formats/british-parliamentary/">British Parliamentary format guide</a></li>
    <li><a href="/blog/wsdc-vs-british-parliamentary/">WSDC vs BP: which should your school run?</a></li>
    <li><a href="/timer/asian-parliamentary/">Asian Parliamentary timer</a></li>
    <li><a href="/blog/tournament-day-setup/">How to set up a debate timer for tournament day</a></li>
  </ul>""",
    "formats/british-parliamentary/index.html": """  <h2>Related guides</h2>
  <ul>
    <li><a href="/formats/world-schools/">World Schools (WSDC) format guide</a></li>
    <li><a href="/blog/wsdc-vs-british-parliamentary/">WSDC vs BP: which should your school run?</a></li>
    <li><a href="/timer/asian-parliamentary/">Asian Parliamentary timer</a></li>
    <li><a href="/timer/canadian-parliamentary/">Canadian Parliamentary (CUSID) timer</a></li>
  </ul>""",
}

for path, related_html in RELATED.items():
    f = pathlib.Path(path)
    if not f.exists():
        print(f"skip (missing): {path}")
        continue
    src = f.read_text()
    if 'Related guides' not in src:
        src = src.replace(
            '  <h2>Frequently asked questions</h2>',
            related_html + '\n\n  <h2>Frequently asked questions</h2>',
            1
        )
        f.write_text(src)
        print(f"ok cross-links: {path}")
    else:
        print(f"skip (already has links): {path}")

# ── Update sitemap ────────────────────────────────────────────────────────────
sm = pathlib.Path("sitemap.xml").read_text()
new_urls = [
    "https://debateclock.org/blog/wsdc-vs-british-parliamentary/",
]
for url in new_urls:
    if url not in sm:
        sm = sm.replace('</urlset>',
            f'  <url><loc>{url}</loc><lastmod>2026-04-19</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
# prep-time blog already exists in sitemap — just update it
pathlib.Path("sitemap.xml").write_text(sm)
print(f"ok: sitemap — {sm.count('<url>')} URLs")
print("done.")
