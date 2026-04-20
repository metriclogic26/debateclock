#!/usr/bin/env python3
"""
Generates 5 SEO content pages:
1. /formats/lincoln-douglas/
2. /formats/public-forum/
3. /formats/world-schools/
4. /formats/british-parliamentary/
5. /blog/tournament-day-setup/

Run from project root: python3 seo-content-batch.py
"""
import pathlib

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
      <h4>US Formats</h4>
      <a href="/timer/lincoln-douglas/">Lincoln-Douglas</a>
      <a href="/timer/policy-debate/">Policy (CX)</a>
      <a href="/timer/public-forum/">Public Forum</a>
      <a href="/timer/parliamentary/">Parliamentary</a>
    </div>
    <div class="footer-col">
      <h4>International</h4>
      <a href="/timer/world-schools/">World Schools (WSDC)</a>
      <a href="/timer/british-parliamentary/">British Parliamentary</a>
      <a href="/timer/asian-parliamentary/">Asian Parliamentary</a>
      <a href="/timer/canadian-parliamentary/">Canadian (CUSID)</a>
    </div>
    <div class="footer-col">
      <h4>Practice Tools</h4>
      <a href="/practice/motion/">Motion timer</a>
      <a href="/practice/extemp/">Extemp prep room</a>
      <a href="/practice/round-logger/">Round logger</a>
      <a href="/practice/flow/">Flow timer</a>
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
    .content-wrap ul { margin: 0 0 16px 20px; }
    .content-wrap ul li { font-size: 15px; color: var(--muted, #8B90A0); line-height: 1.75; margin-bottom: 6px; }
    .content-wrap strong { color: #E8EAF0; }
    .speech-table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }
    .speech-table th { font-size: 10px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #5B6175; padding: 8px 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .speech-table td { padding: 10px 12px; color: #E8EAF0; border-bottom: 1px solid rgba(255,255,255,0.04); font-family: 'DM Mono', monospace; font-size: 13px; }
    .speech-table td:first-child { font-family: 'DM Sans', sans-serif; font-size: 14px; }
    .side-aff { background: rgba(34,197,94,0.12); color: #22C55E; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 600; }
    .side-neg { background: rgba(239,68,68,0.12); color: #EF4444; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 600; }
    .side-cx  { background: rgba(245,158,11,0.12); color: #F59E0B; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 600; }
    .cta-box { background: #111318; border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 28px; margin: 36px 0; text-align: center; }
    .cta-box h3 { font-size: 18px; margin-bottom: 8px; }
    .cta-box p { margin-bottom: 20px; }
    .cta-box a { display: inline-block; background: #22C55E; color: #04140a; font-weight: 700; padding: 12px 28px; border-radius: 10px; text-decoration: none; font-size: 15px; }
    .faq details { background: #111318; border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 14px 18px; margin-bottom: 8px; }
    .faq summary { font-size: 14px; font-weight: 600; color: #E8EAF0; cursor: pointer; list-style: none; }
    .faq summary::after { content: ' +'; color: #5B6175; }
    .faq details[open] summary::after { content: ' -'; }
    .faq details div { font-size: 14px; color: #8B90A0; line-height: 1.7; margin-top: 10px; }
  </style>"""

# ── PAGE 1: Lincoln-Douglas ───────────────────────────────────────────────────
LD_SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"Lincoln-Douglas Debate Format: Complete Guide","description":"Complete guide to Lincoln-Douglas debate format. Speech order, prep time rules, and how to time an LD round.","url":"https://debateclock.org/formats/lincoln-douglas/"}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"How long are speeches in Lincoln-Douglas debate?","acceptedAnswer":{"@type":"Answer","text":"The Affirmative Constructive is 6 minutes, Negative Constructive is 7 minutes, 1AR is 4 minutes, Negative Rebuttal is 6 minutes, and 2AR is 3 minutes. Cross-examinations are 3 minutes each."}},
{"@type":"Question","name":"How much prep time do debaters get in LD?","acceptedAnswer":{"@type":"Answer","text":"Each debater gets 4 minutes of prep time total, distributed freely across the round."}},
{"@type":"Question","name":"What order do speeches go in Lincoln-Douglas debate?","acceptedAnswer":{"@type":"Answer","text":"AC (6 min), Neg CX (3 min), NC (7 min), Aff CX (3 min), 1AR (4 min), NR (6 min), 2AR (3 min)."}}
]}</script>"""

LD = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lincoln-Douglas Debate Format: Speech Order, Prep Time & Rules</title>
<meta name="description" content="Complete guide to Lincoln-Douglas debate. Full speech order, prep time rules, cross-examination structure, and a free LD timer with shared prep pool.">
<link rel="canonical" href="https://debateclock.org/formats/lincoln-douglas/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
{LD_SCHEMA}
{HEAD_COMMON}
</head>
<body>
{NAV}
<div class="content-wrap">
  <div style="font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#5B6175;margin-bottom:12px;">Format Guide</div>
  <h1>Lincoln-Douglas debate: speech order, prep time &amp; rules</h1>
  <p>Lincoln-Douglas (LD) is a one-on-one debate format focused on values and philosophy. It is the most popular individual debate event in US high school competition, governed by the National Speech and Debate Association (NSDA). This guide covers the complete speech order, prep time rules, and how to time an LD round.</p>

  <div class="cta-box">
    <h3>Free LD Timer</h3>
    <p>Shared prep pool, two-device sync, all 7 speeches preloaded. No signup.</p>
    <a href="/timer/lincoln-douglas/">Open LD timer &rarr;</a>
  </div>

  <h2>Lincoln-Douglas speech order</h2>
  <table class="speech-table">
    <thead><tr><th>#</th><th>Speech</th><th>Side</th><th>Time</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>Affirmative Constructive (AC)</td><td><span class="side-aff">AFF</span></td><td>6:00</td></tr>
      <tr><td>2</td><td>Negative Cross-Examination of Aff</td><td><span class="side-cx">CX</span></td><td>3:00</td></tr>
      <tr><td>3</td><td>Negative Constructive (NC)</td><td><span class="side-neg">NEG</span></td><td>7:00</td></tr>
      <tr><td>4</td><td>Affirmative Cross-Examination of Neg</td><td><span class="side-cx">CX</span></td><td>3:00</td></tr>
      <tr><td>5</td><td>1st Affirmative Rebuttal (1AR)</td><td><span class="side-aff">AFF</span></td><td>4:00</td></tr>
      <tr><td>6</td><td>Negative Rebuttal (NR)</td><td><span class="side-neg">NEG</span></td><td>6:00</td></tr>
      <tr><td>7</td><td>2nd Affirmative Rebuttal (2AR)</td><td><span class="side-aff">AFF</span></td><td>3:00</td></tr>
    </tbody>
  </table>
  <p><strong>Prep time:</strong> 4 minutes per debater, distributed freely across the round. Each debater draws from their own pool and may use it before any of their speeches.</p>

  <h2>How prep time works in LD</h2>
  <p>Prep time in Lincoln-Douglas is a shared pool — each debater has 4 minutes total and can use it in any combination before any of their speeches. There is no per-speech limit. A debater might use 3 minutes before the NC and 1 minute before the NR, or all 4 minutes in a single block.</p>
  <p>The judge tracks prep time separately for each debater. When a debater calls for prep, the judge starts the clock. When the debater indicates they are ready, prep stops and the remaining time is noted.</p>
  <p>DebateClock handles this automatically — the prep pool for each side counts down independently and saves state between speeches.</p>

  <h2>Cross-examination rules</h2>
  <p>Cross-examination periods are 3 minutes each. During CX, the questioner asks questions and the respondent answers. Neither debater may use prep time during cross-examination. Cross-examination is not a speech — it does not count toward either debater's speaking time.</p>

  <h2>The 1AR challenge</h2>
  <p>The 1st Affirmative Rebuttal (1AR) is widely considered the hardest speech in LD. The affirmative has only 4 minutes to respond to the 7-minute NC plus the 6-minute NR, a combined 13 minutes of negative material. Efficient line-by-line refutation and strategic prioritization are essential.</p>

  <h2>Frequently asked questions</h2>
  <div class="faq">
    <details><summary>How long are speeches in LD debate?</summary><div>AC: 6 min, NC: 7 min, 1AR: 4 min, NR: 6 min, 2AR: 3 min. CX periods are 3 min each.</div></details>
    <details><summary>How much prep time in LD?</summary><div>4 minutes per debater, used freely across the round in any combination.</div></details>
    <details><summary>Can you use prep time during cross-examination?</summary><div>No. Prep time may only be used before a debater's own speeches, not during cross-examination.</div></details>
    <details><summary>What happens if prep time runs out?</summary><div>The debater must begin their speech immediately when called. Running out of prep time is a competitive disadvantage, not a rule violation.</div></details>
    <details><summary>How is LD different from Policy debate?</summary><div>LD is one-on-one (Policy is 2v2), has fewer and shorter speeches, and focuses on philosophical values rather than policy advocacy. LD prep pools are 4 min per debater vs 8 min per team in Policy.</div></details>
  </div>
</div>
{DISCLAIMER}
{FOOTER}
</body>
</html>"""

# ── PAGE 2: Public Forum ──────────────────────────────────────────────────────
PF_SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"Public Forum Debate Format: Complete Guide","description":"Complete guide to Public Forum debate format. Full speech order, crossfire structure, prep time rules, and a free PF timer.","url":"https://debateclock.org/formats/public-forum/"}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"How long are speeches in Public Forum debate?","acceptedAnswer":{"@type":"Answer","text":"Constructive speeches are 4 minutes each, Summary speeches are 3 minutes each, and Final Focus speeches are 2 minutes each. Crossfire periods are 3 minutes each."}},
{"@type":"Question","name":"How much prep time in Public Forum?","acceptedAnswer":{"@type":"Answer","text":"Each team gets 3 minutes of prep time total, distributed freely across the round."}},
{"@type":"Question","name":"What is Grand Crossfire in PF?","acceptedAnswer":{"@type":"Answer","text":"Grand Crossfire is a 3-minute period after the Summary speeches where all four debaters participate simultaneously."}}
]}</script>"""

PF = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Public Forum Debate Format: Speech Order, Crossfire & Prep Time</title>
<meta name="description" content="Complete guide to Public Forum debate. Full speech order, crossfire structure, prep time rules, and a free PF timer with shared prep pool.">
<link rel="canonical" href="https://debateclock.org/formats/public-forum/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
{PF_SCHEMA}
{HEAD_COMMON}
</head>
<body>
{NAV}
<div class="content-wrap">
  <div style="font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#5B6175;margin-bottom:12px;">Format Guide</div>
  <h1>Public Forum debate: speech order, crossfire &amp; prep time</h1>
  <p>Public Forum (PF) is a two-on-two debate format focused on current events and policy. It is the most popular team debate event in US high school competition. This guide covers the complete speech order, crossfire structure, prep time rules, and how to time a PF round.</p>

  <div class="cta-box">
    <h3>Free PF Timer</h3>
    <p>Shared prep pool per team, two-device sync, all 11 speeches preloaded. No signup.</p>
    <a href="/timer/public-forum/">Open PF timer &rarr;</a>
  </div>

  <h2>Public Forum speech order</h2>
  <table class="speech-table">
    <thead><tr><th>#</th><th>Speech</th><th>Side</th><th>Time</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>1st Speaker — Team A (Pro)</td><td><span class="side-aff">PRO</span></td><td>4:00</td></tr>
      <tr><td>2</td><td>1st Speaker — Team B (Con)</td><td><span class="side-neg">CON</span></td><td>4:00</td></tr>
      <tr><td>3</td><td>Crossfire #1 (1st speakers)</td><td><span class="side-cx">CX</span></td><td>3:00</td></tr>
      <tr><td>4</td><td>2nd Speaker — Team A (Pro)</td><td><span class="side-aff">PRO</span></td><td>4:00</td></tr>
      <tr><td>5</td><td>2nd Speaker — Team B (Con)</td><td><span class="side-neg">CON</span></td><td>4:00</td></tr>
      <tr><td>6</td><td>Crossfire #2 (2nd speakers)</td><td><span class="side-cx">CX</span></td><td>3:00</td></tr>
      <tr><td>7</td><td>Summary — Team A</td><td><span class="side-aff">PRO</span></td><td>3:00</td></tr>
      <tr><td>8</td><td>Summary — Team B</td><td><span class="side-neg">CON</span></td><td>3:00</td></tr>
      <tr><td>9</td><td>Grand Crossfire (all 4 speakers)</td><td><span class="side-cx">CX</span></td><td>3:00</td></tr>
      <tr><td>10</td><td>Final Focus — Team A</td><td><span class="side-aff">PRO</span></td><td>2:00</td></tr>
      <tr><td>11</td><td>Final Focus — Team B</td><td><span class="side-neg">CON</span></td><td>2:00</td></tr>
    </tbody>
  </table>
  <p><strong>Prep time:</strong> 3 minutes per team, distributed freely. Each team shares one pool across both speakers.</p>

  <h2>How crossfire works in PF</h2>
  <p>Public Forum has three crossfire periods. The first two crossfires are between the two first speakers and two second speakers respectively — they question each other directly. Grand Crossfire involves all four debaters and is less structured, with any debater able to ask or answer questions.</p>
  <p>During crossfire, both speakers stand and engage directly. The judge times the 3-minute period but does not intervene in the questioning structure.</p>

  <h2>Prep time rules in PF</h2>
  <p>Each team has 3 minutes of prep time shared between both partners. Prep may be called before either speaker's speech — the 1st speaker might use 1 minute before their constructive and the 2nd speaker uses the remaining 2 minutes before their constructive, or any other combination.</p>
  <p>Prep time cannot be used during crossfire periods. The judge tracks each team's remaining prep separately.</p>

  <h2>Frequently asked questions</h2>
  <div class="faq">
    <details><summary>How long are PF speeches?</summary><div>Constructives: 4 min each. Summaries: 3 min each. Final Focus: 2 min each. Crossfires: 3 min each.</div></details>
    <details><summary>How much prep time does each team get?</summary><div>3 minutes per team, shared between both partners and used freely across the round.</div></details>
    <details><summary>What is Grand Crossfire?</summary><div>A 3-minute period after both Summary speeches where all four debaters participate simultaneously. Any debater can ask or answer questions.</div></details>
    <details><summary>Can prep time be used during crossfire?</summary><div>No. Prep time may only be used before a team's own speeches.</div></details>
    <details><summary>What is the difference between Summary and Final Focus?</summary><div>Summary is 3 minutes and should crystallize the key arguments. Final Focus is 2 minutes and is the last speech — it should focus only on the 1-2 most important voters the judge should use to decide the round.</div></details>
  </div>
</div>
{DISCLAIMER}
{FOOTER}
</body>
</html>"""

# ── PAGE 3: World Schools ─────────────────────────────────────────────────────
WSDC_SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"World Schools Debate Format (WSDC): Complete Guide","description":"Complete guide to World Schools debate format. Speech order, POI rules, reply speech structure, and a free WSDC timer.","url":"https://debateclock.org/formats/world-schools/"}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"How long are speeches in World Schools debate?","acceptedAnswer":{"@type":"Answer","text":"Main speeches are 8 minutes each. Reply speeches are 4 minutes each."}},
{"@type":"Question","name":"When can POIs be offered in World Schools debate?","acceptedAnswer":{"@type":"Answer","text":"POIs can be offered between the 1-minute and 7-minute marks of each 8-minute main speech. The first and last minute are protected time."}},
{"@type":"Question","name":"Who gives the reply speech in WSDC?","acceptedAnswer":{"@type":"Answer","text":"The reply speech is given by either the 1st or 2nd speaker of each team — not the 3rd speaker. The Opposition gives their reply before the Proposition."}}
]}</script>"""

WSDC = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>World Schools Debate Format (WSDC): Speech Order, POI Rules & Timer</title>
<meta name="description" content="Complete guide to World Schools debate (WSDC). Speech order, POI window rules, reply speech structure, and a free WSDC timer with automatic POI signal.">
<link rel="canonical" href="https://debateclock.org/formats/world-schools/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
{WSDC_SCHEMA}
{HEAD_COMMON}
</head>
<body>
{NAV}
<div class="content-wrap">
  <div style="font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#5B6175;margin-bottom:12px;">Format Guide</div>
  <h1>World Schools debate (WSDC): speech order, POI rules &amp; timer</h1>
  <p>World Schools Debating Championships (WSDC) is a three-on-three international debate format used in over 70 countries. It combines prepared and impromptu motions, structured Points of Information (POIs), and a unique reply speech system. This guide covers the complete speech order, POI rules, and how to time a WSDC round.</p>

  <div class="cta-box">
    <h3>Free WSDC Timer</h3>
    <p>Automatic POI window signal, all 8 speeches preloaded, two-device sync. No signup.</p>
    <a href="/timer/world-schools/">Open WSDC timer &rarr;</a>
  </div>

  <h2>World Schools speech order</h2>
  <table class="speech-table">
    <thead><tr><th>#</th><th>Speech</th><th>Side</th><th>Time</th><th>POI Window</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>1st Proposition</td><td><span class="side-aff">PROP</span></td><td>8:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 7:00</td></tr>
      <tr><td>2</td><td>1st Opposition</td><td><span class="side-neg">OPP</span></td><td>8:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 7:00</td></tr>
      <tr><td>3</td><td>2nd Proposition</td><td><span class="side-aff">PROP</span></td><td>8:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 7:00</td></tr>
      <tr><td>4</td><td>2nd Opposition</td><td><span class="side-neg">OPP</span></td><td>8:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 7:00</td></tr>
      <tr><td>5</td><td>3rd Proposition</td><td><span class="side-aff">PROP</span></td><td>8:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 7:00</td></tr>
      <tr><td>6</td><td>3rd Opposition</td><td><span class="side-neg">OPP</span></td><td>8:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 7:00</td></tr>
      <tr><td>7</td><td>Opposition Reply</td><td><span class="side-neg">OPP</span></td><td>4:00</td><td style="color:#5B6175;font-family:'DM Mono',monospace;">None</td></tr>
      <tr><td>8</td><td>Proposition Reply</td><td><span class="side-aff">PROP</span></td><td>4:00</td><td style="color:#5B6175;font-family:'DM Mono',monospace;">None</td></tr>
    </tbody>
  </table>
  <p><strong>No prep pool.</strong> Speeches run back-to-back. The Opposition reply is delivered before the Proposition reply.</p>

  <h2>Points of Information (POIs)</h2>
  <p>POIs are one of the defining features of World Schools debate. During each 8-minute main speech, the opposing team may offer POIs between the 1-minute and 7-minute marks — the first and last minute are protected time.</p>
  <p>To offer a POI, a debater stands and says "Point of information" or "On that point." The speaker may accept or decline. A speaker who accepts a POI allows the opposing debater to ask a brief question or make a short interjection (maximum 15 seconds). The speaker's clock continues running during an accepted POI.</p>
  <p>Good speakers accept 1-2 POIs per speech. Accepting too few is considered evasive. DebateClock shows an amber POI badge on the debater display that appears at 1:00 and disappears at 7:00, signaling when POIs may be offered.</p>

  <h2>Reply speeches</h2>
  <p>Reply speeches are 4 minutes each and are delivered by either the 1st or 2nd speaker — not the 3rd speaker. The reply speech is a biased adjudication of the round: the speaker summarizes why their team won without introducing new arguments. The Opposition replies first, then the Proposition has the last word.</p>

  <h2>Frequently asked questions</h2>
  <div class="faq">
    <details><summary>How long are WSDC speeches?</summary><div>Main speeches: 8 minutes each. Reply speeches: 4 minutes each. There are 6 main speeches and 2 reply speeches per round.</div></details>
    <details><summary>When is the POI window open?</summary><div>Between 1:00 and 7:00 of each 8-minute main speech. The first and last minute are protected. Reply speeches have no POI window.</div></details>
    <details><summary>Who can give the reply speech?</summary><div>Only the 1st or 2nd speaker of each team. The 3rd speaker cannot give a reply speech. The Opposition replies first, then the Proposition.</div></details>
    <details><summary>Is there prep time in WSDC?</summary><div>No in-round prep pool. For prepared motions, teams receive the motion in advance. For impromptu motions, teams typically receive 1 hour of preparation before the round.</div></details>
    <details><summary>How many POIs should a speaker accept?</summary><div>The general guideline is 1-2 POIs per speech. Accepting zero POIs is seen as evasive; accepting too many disrupts the speech flow.</div></details>
  </div>
</div>
{DISCLAIMER}
{FOOTER}
</body>
</html>"""

# ── PAGE 4: British Parliamentary ────────────────────────────────────────────
BP_SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"British Parliamentary Debate Format: Complete Guide","description":"Complete guide to British Parliamentary debate format (WUDC). Four teams, speech order, POI rules, and a free BP timer.","url":"https://debateclock.org/formats/british-parliamentary/"}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"How many teams are in British Parliamentary debate?","acceptedAnswer":{"@type":"Answer","text":"Four teams compete in each BP round: Opening Government (OG), Opening Opposition (OO), Closing Government (CG), and Closing Opposition (CO). Each team has two speakers."}},
{"@type":"Question","name":"How long are speeches in British Parliamentary debate?","acceptedAnswer":{"@type":"Answer","text":"All speeches are 7 minutes at university level (WUDC). High school BP uses 5-minute speeches."}},
{"@type":"Question","name":"When can POIs be offered in BP debate?","acceptedAnswer":{"@type":"Answer","text":"POIs can be offered between the 1-minute and 6-minute marks of each 7-minute speech. The first and last minute are protected."}}
]}</script>"""

BP = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>British Parliamentary Debate Format (BP/WUDC): Complete Guide</title>
<meta name="description" content="Complete guide to British Parliamentary debate (WUDC). Four-team format, speech order, POI rules, and a free BP timer with automatic POI signal.">
<link rel="canonical" href="https://debateclock.org/formats/british-parliamentary/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
{BP_SCHEMA}
{HEAD_COMMON}
</head>
<body>
{NAV}
<div class="content-wrap">
  <div style="font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#5B6175;margin-bottom:12px;">Format Guide</div>
  <h1>British Parliamentary debate (BP/WUDC): format guide</h1>
  <p>British Parliamentary (BP) is the dominant debate format at universities worldwide, used at the World Universities Debating Championship (WUDC). Four teams of two speakers compete simultaneously in each round. This guide covers the team structure, speech order, POI rules, and how to time a BP round.</p>

  <div class="cta-box">
    <h3>Free BP Timer</h3>
    <p>Automatic POI signal, all 8 speeches preloaded, university and high school variants. No signup.</p>
    <a href="/timer/british-parliamentary/">Open BP timer &rarr;</a>
  </div>

  <h2>The four-team structure</h2>
  <p>BP is unique in having four teams compete simultaneously. The teams are Opening Government (OG), Opening Opposition (OO), Closing Government (CG), and Closing Opposition (CO). OG and CG are on the government side; OO and CO are on the opposition side. Crucially, the two government teams and two opposition teams are competing against each other as well — all four teams are ranked 1st through 4th at the end of the round.</p>

  <h2>British Parliamentary speech order</h2>
  <table class="speech-table">
    <thead><tr><th>#</th><th>Speech</th><th>Team</th><th>Time</th><th>POI Window</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>Prime Minister</td><td><span class="side-aff">OG</span></td><td>7:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 6:00</td></tr>
      <tr><td>2</td><td>Leader of Opposition</td><td><span class="side-neg">OO</span></td><td>7:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 6:00</td></tr>
      <tr><td>3</td><td>Deputy Prime Minister</td><td><span class="side-aff">OG</span></td><td>7:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 6:00</td></tr>
      <tr><td>4</td><td>Deputy Leader of Opposition</td><td><span class="side-neg">OO</span></td><td>7:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 6:00</td></tr>
      <tr><td>5</td><td>Member for Government (CG)</td><td><span class="side-aff">CG</span></td><td>7:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 6:00</td></tr>
      <tr><td>6</td><td>Member for Opposition (CO)</td><td><span class="side-neg">CO</span></td><td>7:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 6:00</td></tr>
      <tr><td>7</td><td>Government Whip (CG)</td><td><span class="side-aff">CG</span></td><td>7:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 6:00</td></tr>
      <tr><td>8</td><td>Opposition Whip (CO)</td><td><span class="side-neg">CO</span></td><td>7:00</td><td style="color:#F59E0B;font-family:'DM Mono',monospace;">1:00 – 6:00</td></tr>
    </tbody>
  </table>
  <p><strong>No prep pool.</strong> All 8 speeches are 7 minutes at university level. High school BP uses 5-minute speeches with POI window 0:30–4:30.</p>

  <h2>POI rules in BP</h2>
  <p>POIs follow the same principle as WSDC — stand, offer "Point of information," speaker accepts or declines. In BP the window is minutes 1–6 of each 7-minute speech (first and last minute protected). Speakers typically accept 1-2 POIs per speech.</p>

  <h2>The closing half challenge</h2>
  <p>The closing teams (CG and CO) face a unique challenge: they must extend the debate rather than repeat opening arguments. A closing team that simply repeats OG or OO material will be ranked 3rd or 4th. The Member speech must introduce a new and distinct argument that adds to the overall case for their side.</p>

  <h2>Frequently asked questions</h2>
  <div class="faq">
    <details><summary>How many teams are in a BP round?</summary><div>Four teams: Opening Government (OG), Opening Opposition (OO), Closing Government (CG), and Closing Opposition (CO). Each team has two speakers.</div></details>
    <details><summary>How are teams ranked in BP?</summary><div>All four teams are ranked 1st through 4th. Being on the government side does not mean you are competing only against the opposition — all four teams are ranked against each other.</div></details>
    <details><summary>How long are BP speeches?</summary><div>7 minutes at university level (WUDC). High school BP typically uses 5-minute speeches.</div></details>
    <details><summary>What is the POI window in BP?</summary><div>Minutes 1–6 of each 7-minute speech. The first and last minute are protected time.</div></details>
    <details><summary>Does BP have prep time?</summary><div>No in-round prep pool. Teams typically receive the motion 15 minutes before the round starts.</div></details>
  </div>
</div>
{DISCLAIMER}
{FOOTER}
</body>
</html>"""

# ── PAGE 5: Blog — Tournament day setup ──────────────────────────────────────
BLOG = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>How to Set Up a Debate Timer for Tournament Day | DebateClock</title>
<meta name="description" content="Step-by-step guide to setting up DebateClock for tournament day. Judge setup, debater display, Tabroom paradigm link, and what to do when Wi-Fi fails.">
<link rel="canonical" href="https://debateclock.org/blog/tournament-day-setup/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"HowTo","name":"How to Set Up a Debate Timer for Tournament Day","description":"Step-by-step guide to setting up DebateClock for a debate tournament.","totalTime":"PT5M","step":[
{{"@type":"HowToStep","position":1,"name":"Open the timer on your phone","text":"Go to debateclock.org/app on your phone. A room code is generated instantly."}},
{{"@type":"HowToStep","position":2,"name":"Share the display link with the debater","text":"Show the QR code or copy the display link. The debater opens it on their laptop or tablet."}},
{{"@type":"HowToStep","position":3,"name":"Select your format","text":"Tap the format pill in the top bar and select your format. The correct speech order and prep pool load automatically."}},
{{"@type":"HowToStep","position":4,"name":"Start timing","text":"Tap Start when the first speech begins. The prep pool tracks automatically across all speeches."}}
]}}</script>
{HEAD_COMMON}
</head>
<body>
{NAV}
<div class="content-wrap">
  <div style="font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#5B6175;margin-bottom:12px;">Guide</div>
  <h1>How to set up a debate timer for tournament day</h1>
  <p>Setting up DebateClock takes under 2 minutes. This guide covers everything from opening the timer before your first round to what to do if Wi-Fi drops mid-speech.</p>

  <h2>Before the tournament — 2 minutes of setup</h2>
  <p>The best time to set up DebateClock is the night before or in the car on the way to the tournament, not in the tab bay 30 seconds before your round.</p>
  <ul>
    <li><strong>Judges:</strong> Add your paradigm link to Tabroom. Your link is <code style="font-family:'DM Mono',monospace;color:#3B82F6;">debateclock.org/j/your-name</code>. Paste it at the top of your paradigm. Debaters will click it before every round. See the <a href="/setup/judge-paradigm/">full setup guide</a>.</li>
    <li><strong>Coaches:</strong> Bookmark <a href="/practice/tournament/">debateclock.org/practice/tournament/</a> and add the day's round schedule the night before.</li>
    <li><strong>Debaters:</strong> Bookmark <a href="/app/">debateclock.org/app/</a> on your phone and test that the display link opens on your laptop.</li>
  </ul>

  <h2>Step-by-step: judge setup for a round</h2>
  <table class="speech-table">
    <thead><tr><th>Step</th><th>Action</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>Open debateclock.org/app on your phone. Room code appears instantly — no signup.</td></tr>
      <tr><td>2</td><td>Tap the format pill (top left) and select your format. Speech order and prep pool load automatically.</td></tr>
      <tr><td>3</td><td>Show the QR code to the debater or copy the display link. They open it on their laptop.</td></tr>
      <tr><td>4</td><td>Both screens should show the same format and "waiting to start." Tap Start when the first speech begins.</td></tr>
      <tr><td>5</td><td>Prep time: tap "Start Prep — Aff" or "Start Prep — Neg" when a debater calls prep. It stops automatically when you tap again.</td></tr>
    </tbody>
  </table>

  <h2>What to do when Wi-Fi fails</h2>
  <p>Tournament venues often have unreliable Wi-Fi. DebateClock handles this gracefully:</p>
  <ul>
    <li>The timer continues running on both devices even if the connection drops — it uses the local clock, not a server.</li>
    <li>When Wi-Fi reconnects, both devices automatically re-sync.</li>
    <li>If sync fails entirely, the judge's phone is the authoritative timer. The debater display is supplementary.</li>
    <li>You can also use DebateClock in single-device mode — the judge controller works fully standalone without a debater display connected.</li>
  </ul>

  <h2>Format-specific tips</h2>
  <h3>Lincoln-Douglas</h3>
  <p>LD prep pools are per-debater (4 min each). Tap "Start Prep — Aff" when the Aff calls prep, "Start Prep — Neg" when Neg calls prep. The pools are independent and each saves state between uses.</p>

  <h3>Policy (CX)</h3>
  <p>Policy has 8-minute speeches and 8-minute prep pools per team. With 12 speeches and frequent prep calls, keeping the prep pool accurate is the most important job. DebateClock tracks this automatically.</p>

  <h3>Public Forum</h3>
  <p>PF has 3-minute prep pools per team. The pools are smaller but used more frequently. Grand Crossfire is the 9th speech — tap the row in the speech list to jump to it.</p>

  <h3>WSDC / BP</h3>
  <p>No prep pool — speeches run back-to-back. The POI badge appears automatically on the debater display at the correct time. No manual intervention needed.</p>

  <h2>The Tabroom paradigm link — your best tool</h2>
  <p>The single highest-leverage thing a judge can do is add their paradigm link to Tabroom. Debaters read paradigms in the tab bay before rounds. When your link is there, debaters click it, open the display on their laptop, and the timer is already running when you walk in. No QR code scanning, no room code sharing, no setup time.</p>
  <p>Your permanent link: <code style="font-family:'DM Mono',monospace;color:#3B82F6;">debateclock.org/j/your-name</code></p>
  <p><a href="/setup/judge-paradigm/">Full Tabroom setup guide &rarr;</a></p>

  <h2>Frequently asked questions</h2>
  <div class="faq">
    <details><summary>Does DebateClock work without internet?</summary><div>The timer itself works without internet once the page loads. Two-device sync requires a connection, but the judge controller works fully standalone. The page loads from cache on repeat visits.</div></details>
    <details><summary>What if the debater's laptop can't open the display link?</summary><div>The judge controller works as a standalone timer — the debater display is supplementary. The judge can show their phone screen to the debater if needed, or the debater can open the display on their phone instead.</div></details>
    <details><summary>Can multiple debaters join the same room?</summary><div>Yes — any number of devices can open the display link. Multiple debaters can watch the countdown on their own devices simultaneously.</div></details>
    <details><summary>How do I switch formats mid-tournament?</summary><div>Tap the format pill in the top bar, select the new format, and confirm. The round resets with the new speech order and prep pool.</div></details>
  </div>
</div>
{DISCLAIMER}
{FOOTER}
</body>
</html>"""

# ── Write all files ───────────────────────────────────────────────────────────
pages = [
    ("formats/lincoln-douglas/index.html", LD),
    ("formats/public-forum/index.html", PF),
    ("formats/world-schools/index.html", WSDC),
    ("formats/british-parliamentary/index.html", BP),
    ("blog/tournament-day-setup/index.html", BLOG),
]

for path, content in pages:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print(f"ok: {path}")

# Update sitemap
sm = pathlib.Path("sitemap.xml").read_text()
new_urls = [
    "https://debateclock.org/formats/lincoln-douglas/",
    "https://debateclock.org/formats/public-forum/",
    "https://debateclock.org/formats/world-schools/",
    "https://debateclock.org/formats/british-parliamentary/",
    "https://debateclock.org/blog/tournament-day-setup/",
]
for url in new_urls:
    if url not in sm:
        sm = sm.replace('</urlset>',
            f'  <url><loc>{url}</loc><lastmod>2026-04-19</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
pathlib.Path("sitemap.xml").write_text(sm)
print(f"ok: sitemap updated — {sm.count('<url>')} URLs total")
print("done.")
