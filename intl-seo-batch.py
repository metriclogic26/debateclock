#!/usr/bin/env python3
"""
International circuit SEO batch:
1. /blog/asian-parliamentary-vs-wsdc/ — comparison post
2. /blog/asian-parliamentary-debate-rules/ — rules explainer
3. /timer/world-schools/ — country-specific content
4. /timer/asian-parliamentary/ — country-specific content
5. /formats/asian-parliamentary/ — WSDC comparison table
6. More WSDC/Asian Parli motions in generator

Run from project root: python3 intl-seo-batch.py
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
        <a href="/practice/motion/">Motion timer <span class="tag">New</span></a>
        <a href="/practice/motions/">Motion generator <span class="tag">New</span></a>
        <a href="/practice/extemp/">Extemp prep room <span class="tag">New</span></a>
        <a href="/practice/round-logger/">Round logger <span class="tag">New</span></a>
        <a href="/practice/flow/">Flow timer <span class="tag">New</span></a>
        <a href="/practice/tournament/">Tournament schedule <span class="tag">New</span></a>
        <div class="nav-dropdown-section">Resources</div>
        <a href="/blog/">Blog &amp; guides</a>
        <a href="/formats/lincoln-douglas/">Format guides</a>
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
      <h4>Competition</h4>
      <a href="/app/">Two-device timer</a>
      <a href="/setup/judge-paradigm/">Tabroom paradigm setup</a>
      <a href="/timer/lincoln-douglas/">Lincoln-Douglas</a>
      <a href="/timer/policy-debate/">Policy (CX)</a>
      <a href="/timer/public-forum/">Public Forum</a>
      <a href="/timer/world-schools/">World Schools (WSDC)</a>
      <a href="/timer/british-parliamentary/">British Parliamentary</a>
    </div>
    <div class="footer-col">
      <h4>Practice Tools</h4>
      <a href="/practice/motion/">Motion timer</a>
      <a href="/practice/motions/">Motion generator</a>
      <a href="/practice/extemp/">Extemp prep room</a>
      <a href="/practice/round-logger/">Round logger</a>
      <a href="/practice/flow/">Flow timer</a>
      <a href="/practice/tournament/">Tournament schedule</a>
    </div>
    <div class="footer-col">
      <h4>Guides &amp; Blog</h4>
      <a href="/blog/">All guides</a>
      <a href="/formats/lincoln-douglas/">LD format guide</a>
      <a href="/formats/public-forum/">PF format guide</a>
      <a href="/formats/world-schools/">WSDC format guide</a>
      <a href="/formats/british-parliamentary/">BP format guide</a>
      <a href="/formats/asian-parliamentary/">Asian Parli guide</a>
      <a href="/blog/wsdc-vs-british-parliamentary/">WSDC vs BP</a>
    </div>
  </div>
  <div class="footer-row">
    <div><a href="/" style="display:inline-flex;align-items:center;gap:8px;color:var(--muted);text-decoration:none;"><span style="width:12px;height:12px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);"></span>DebateClock</a><span style="margin-left:12px;">free browser debate timer</span></div>
    <a href="https://tally.so/r/QKAMOX" target="_blank" rel="noopener" class="feedback-btn">&#9733; Give feedback</a>
  </div>
</footer>"""

HEAD_CSS = """  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
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
  </style>"""

# ══════════════════════════════════════════════════════════════════════════════
# 1. Blog: Asian Parliamentary vs WSDC
# ══════════════════════════════════════════════════════════════════════════════

ASIAN_VS_WSDC = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Asian Parliamentary vs World Schools (WSDC): Which Format Should You Run?</title>
<meta name="description" content="Comparing Asian Parliamentary and World Schools (WSDC) debate formats. Team size, speech length, POI rules, reply speeches, and which suits your school or tournament.">
<link rel="canonical" href="https://www.debateclock.org/blog/asian-parliamentary-vs-wsdc/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"Asian Parliamentary vs World Schools (WSDC): Which Format Should You Run?","url":"https://www.debateclock.org/blog/asian-parliamentary-vs-wsdc/"}}
</script>
{HEAD_CSS}
</head>
<body>
{NAV}
<div class="content-wrap">
  <div style="font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#5B6175;margin-bottom:12px;">Blog</div>
  <h1>Asian Parliamentary vs World Schools (WSDC): which format should you run?</h1>
  <p>Asian Parliamentary and World Schools (WSDC) are the two dominant international debate formats across Asia, Africa, and Australasia. Both use three-on-three team structures, Points of Information, and reply speeches. But they differ in speech length, POI windows, motion style, and competitive culture. This guide explains the key differences to help coaches, tournament directors, and debaters decide which format fits their context.</p>

  <h2>Quick comparison</h2>
  <table class="compare-table">
    <thead><tr><th>Feature</th><th>Asian Parliamentary</th><th>World Schools (WSDC)</th></tr></thead>
    <tbody>
      <tr><td>Teams per round</td><td>2 (Government vs Opposition)</td><td>2 (Proposition vs Opposition)</td></tr>
      <tr><td>Speakers per team</td><td>3</td><td>3</td></tr>
      <tr><td>Constructive speech length</td><td>7 minutes</td><td>8 minutes</td></tr>
      <tr><td>Reply speech length</td><td>4 minutes</td><td>4 minutes</td></tr>
      <tr><td>Total speeches</td><td>8</td><td>8</td></tr>
      <tr><td>POI window</td><td>Minutes 1&ndash;6</td><td>Minutes 1&ndash;7</td></tr>
      <tr><td>Prep time</td><td>None in-round</td><td>None in-round</td></tr>
      <tr><td>Motion style</td><td>Typically impromptu</td><td>Prepared + impromptu mix</td></tr>
      <tr><td>Who gives reply</td><td>1st or 2nd speaker only</td><td>1st or 2nd speaker only</td></tr>
      <tr><td>Reply order</td><td>Opposition first, Government last</td><td>Opposition first, Proposition last</td></tr>
    </tbody>
  </table>

  <h2>How similar are they?</h2>
  <p>Asian Parliamentary and WSDC are structurally very similar — more so than either is to British Parliamentary or Lincoln-Douglas. Both use the same number of speakers, the same number of speeches, and the same reply speech convention. A debater who competes in one format can adapt to the other within a single practice session.</p>
  <p>The most significant differences are speech length (7 minutes vs 8 minutes) and motion style. These differences affect preparation strategy and the depth of argumentation expected in each speech.</p>

  <h2>Speech length — 7 vs 8 minutes</h2>
  <p>The one-minute difference between Asian Parliamentary (7 minutes) and WSDC (8 minutes) is more significant than it appears. An 8-minute speech allows time for a full case construction, engagement with POIs, and a structured summary. A 7-minute speech requires tighter argumentation — every point must be made efficiently.</p>
  <p>For novice debaters, 7-minute speeches are generally more accessible. Filling 8 minutes with substantive content is a higher bar for speakers who are still developing their argumentation skills.</p>

  <h2>POI windows — minutes 1&ndash;6 vs 1&ndash;7</h2>
  <p>In Asian Parliamentary, POIs may be offered between the 1-minute and 6-minute marks of each constructive speech. In WSDC, the window extends to the 7-minute mark. This means WSDC gives the opposing team one extra minute in which to interrupt — the final minute of each speech is protected in WSDC but not in the last two minutes of a 7-minute Asian Parli speech.</p>
  <p>DebateClock handles both correctly. The POI badge appears and disappears automatically at the right times for each format on the debater display.</p>

  <h2>Motion style</h2>
  <p>Asian Parliamentary tournaments typically use impromptu motions — debaters receive the motion and have a short preparation period (usually 30 minutes to 1 hour) before the round. This rewards broad general knowledge and the ability to construct arguments quickly.</p>
  <p>WSDC tournaments use a mix of prepared motions (announced weeks in advance) and impromptu motions. The prepared/impromptu ratio varies by tournament. Prepared motions allow deeper research and more sophisticated case construction, and reward debaters who invest time in topic preparation.</p>
  <p>For school programs, prepared motions (WSDC-style) allow better curriculum integration. Students can research the topic as part of class and develop well-evidenced cases. Impromptu-only formats (Asian Parliamentary-style) develop faster thinking but may disadvantage less experienced teams who haven't yet built strong general knowledge.</p>

  <h2>Which format is more widely used internationally?</h2>
  <p>Both formats have strong international circuits. Asian Parliamentary is dominant across Southeast Asia, South Asia, and Australasia — Singapore, Malaysia, the Philippines, Indonesia, Thailand, Australia, New Zealand, India, and Sri Lanka all have active Asian Parliamentary circuits.</p>
  <p>WSDC has a broader geographic spread — it is the format used at the World Schools Debating Championships, which includes national teams from across Africa, Europe, the Americas, and Asia. African nations including Kenya, South Africa, Nigeria, and Ghana compete primarily in WSDC-style tournaments.</p>

  <h2>Which is better for beginners?</h2>
  <p>Both formats are reasonably accessible for beginners because the team structure is familiar (two teams, three speakers each) and the reply speech provides a clear role for the team's strongest speaker. Asian Parliamentary's slightly shorter speeches make it marginally more accessible for first-time debaters.</p>
  <p>WSDC prepared motions can be an advantage for beginners — knowing the topic in advance reduces the anxiety of having to construct arguments on the spot, and allows coaches to prepare students thoroughly before competition.</p>

  <div class="cta-box">
    <h3>Free timers for both formats</h3>
    <p>Automatic POI signal, correct speech order, two-device sync. No signup.</p>
    <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;">
      <a class="btn" href="/app/?format=AsianParli">Asian Parli timer &rarr;</a>
      <a class="btn" style="background:#3B82F6;color:#fff;" href="/app/?format=WSDC">WSDC timer &rarr;</a>
    </div>
  </div>

  <h2>Frequently asked questions</h2>
  <div class="faq">
    <details><summary>Can the same debaters compete in both formats?</summary><div>Yes. The structural similarities between Asian Parliamentary and WSDC make it straightforward for debaters to compete in both. The main adjustments are speech length (7 vs 8 minutes) and motion preparation style.</div></details>
    <details><summary>Which format is used at the World Schools Championships?</summary><div>The World Schools Debating Championships (WSDC) uses the World Schools format with a mix of prepared and impromptu motions.</div></details>
    <details><summary>Is Australasian Parliamentary the same as Asian Parliamentary?</summary><div>Australasian Parliamentary and Asian Parliamentary use the same basic structure — 3 speakers per team, 7-minute speeches, reply speeches — with some minor variations in terminology and tournament rules depending on the specific circuit.</div></details>
    <details><summary>Which timer should I use for Asian Parliamentary debate?</summary><div>DebateClock has a dedicated Asian Parliamentary preset with the correct speech order, 7-minute speech times, POI window at minutes 1&ndash;6, and automatic POI signal. <a href="/app/?format=AsianParli">Open the Asian Parliamentary timer</a>.</div></details>
  </div>

  <h2>Related guides</h2>
  <ul>
    <li><a href="/formats/asian-parliamentary/">Asian Parliamentary complete format guide</a></li>
    <li><a href="/formats/world-schools/">World Schools (WSDC) complete format guide</a></li>
    <li><a href="/blog/wsdc-vs-british-parliamentary/">WSDC vs British Parliamentary</a></li>
    <li><a href="/timer/asian-parliamentary/">Asian Parliamentary timer</a></li>
    <li><a href="/timer/world-schools/">World Schools timer</a></li>
  </ul>
</div>
{DISCLAIMER}
{FOOTER}
</body>
</html>"""

# ══════════════════════════════════════════════════════════════════════════════
# 2. Blog: Asian Parliamentary debate rules
# ══════════════════════════════════════════════════════════════════════════════

ASIAN_RULES = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Asian Parliamentary Debate Rules: Complete Guide</title>
<meta name="description" content="Complete guide to Asian Parliamentary debate rules. Speech order, POI rules, reply speeches, timing, and how to run an Asian Parliamentary round.">
<link rel="canonical" href="https://www.debateclock.org/blog/asian-parliamentary-debate-rules/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"Asian Parliamentary Debate Rules: Complete Guide","url":"https://www.debateclock.org/blog/asian-parliamentary-debate-rules/"}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{{"@type":"Question","name":"How long are speeches in Asian Parliamentary debate?","acceptedAnswer":{{"@type":"Answer","text":"Constructive speeches are 7 minutes each. Reply speeches are 4 minutes each. There are 6 constructives and 2 reply speeches per round."}}}},
{{"@type":"Question","name":"When can POIs be offered in Asian Parliamentary?","acceptedAnswer":{{"@type":"Answer","text":"POIs may be offered between the 1-minute and 6-minute marks of each constructive speech. The first and last minute are protected."}}}},
{{"@type":"Question","name":"Who gives the reply speech in Asian Parliamentary?","acceptedAnswer":{{"@type":"Answer","text":"The reply speech is given by either the 1st or 2nd speaker — not the 3rd speaker. The Opposition gives their reply before the Government."}}}}
]}}
</script>
{HEAD_CSS}
</head>
<body>
{NAV}
<div class="content-wrap">
  <div style="font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#5B6175;margin-bottom:12px;">Guide</div>
  <h1>Asian Parliamentary debate rules: complete guide</h1>
  <p>Asian Parliamentary is a three-on-three debate format used at competitions across Southeast Asia, South Asia, and Australasia. This guide covers the complete rules — speech order, timing, POI rules, reply speeches, and how to run a round correctly.</p>

  <div class="cta-box">
    <h3>Free Asian Parliamentary timer</h3>
    <p>All rules preloaded — 7-minute speeches, automatic POI signal, reply speech order. No signup.</p>
    <a class="btn" href="/app/?format=AsianParli">Open Asian Parli timer &rarr;</a>
  </div>

  <h2>Basic structure</h2>
  <p>Asian Parliamentary debate involves two teams of three speakers — the Government (also called Proposition) and the Opposition. Each speaker gives one constructive speech. After all six constructives, one speaker from each team gives a reply speech. The Opposition reply comes before the Government reply, giving the Government the last word.</p>

  <h2>Speech order and timing</h2>
  <table class="compare-table">
    <thead><tr><th>#</th><th>Speech</th><th>Speaker</th><th>Time</th><th>POI Window</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>Prime Minister</td><td>Gov Speaker 1</td><td>7:00</td><td style="color:#F59E0B;">1:00 &ndash; 6:00</td></tr>
      <tr><td>2</td><td>Leader of Opposition</td><td>Opp Speaker 1</td><td>7:00</td><td style="color:#F59E0B;">1:00 &ndash; 6:00</td></tr>
      <tr><td>3</td><td>Deputy Prime Minister</td><td>Gov Speaker 2</td><td>7:00</td><td style="color:#F59E0B;">1:00 &ndash; 6:00</td></tr>
      <tr><td>4</td><td>Deputy Leader of Opposition</td><td>Opp Speaker 2</td><td>7:00</td><td style="color:#F59E0B;">1:00 &ndash; 6:00</td></tr>
      <tr><td>5</td><td>Government Whip</td><td>Gov Speaker 3</td><td>7:00</td><td style="color:#F59E0B;">1:00 &ndash; 6:00</td></tr>
      <tr><td>6</td><td>Opposition Whip</td><td>Opp Speaker 3</td><td>7:00</td><td style="color:#F59E0B;">1:00 &ndash; 6:00</td></tr>
      <tr><td>7</td><td>Opposition Reply</td><td>Opp Speaker 1 or 2</td><td>4:00</td><td style="color:#5B6175;">None</td></tr>
      <tr><td>8</td><td>Government Reply</td><td>Gov Speaker 1 or 2</td><td>4:00</td><td style="color:#5B6175;">None</td></tr>
    </tbody>
  </table>

  <h2>Points of Information (POI) rules</h2>
  <p>POIs are a core feature of Asian Parliamentary debate. During each 7-minute constructive speech, the opposing team may offer POIs between the 1-minute and 6-minute marks. The first minute and the last minute of each speech are protected — no POIs may be offered during these times.</p>

  <h3>How to offer a POI</h3>
  <p>To offer a POI, a debater stands up and says "Point of information," "On that point," or simply "POI." The speaker then decides whether to accept or decline. If the speaker accepts, the debater asking the POI has approximately 15 seconds to make their interjection. The speaker's clock continues running during the POI.</p>

  <h3>POI etiquette</h3>
  <p>Speakers are generally expected to accept 1 to 2 POIs per speech. Accepting zero POIs is considered evasive and may be noted by adjudicators. Offering too many POIs can be seen as disruptive. POIs should be genuine questions or brief rebuttals — not speeches in themselves.</p>

  <h3>POI window on DebateClock</h3>
  <p>DebateClock displays an amber POI badge on the debater display that appears automatically at 1:00 and disappears at 6:00 of each constructive speech. Both the speaker and the adjudicator can see at a glance whether the POI window is open without checking a watch.</p>

  <h2>Reply speeches</h2>
  <p>Each team gives one reply speech at the end of the round. The reply speech is given by either the 1st or 2nd speaker — the 3rd speaker (Whip) may not give the reply. The Opposition reply comes before the Government reply, giving the Government team the last word in the round.</p>
  <p>The reply speech is a biased adjudication of the round — the speaker summarises why their team won the debate without introducing new arguments. Reply speeches are 4 minutes each and have no POI window.</p>

  <h2>Preparation and motions</h2>
  <p>Asian Parliamentary rounds typically use impromptu motions. Teams receive the motion and are given a preparation period — usually 30 minutes to 1 hour — before the round begins. During preparation, teams may use notes and discuss strategy, but may not receive outside assistance once the round has started.</p>
  <p>Some tournaments use prepared motions announced in advance. The rules for each tournament should be confirmed with the tournament director.</p>

  <h2>Timing and bells</h2>
  <p>The standard bell schedule for Asian Parliamentary is:</p>
  <ul>
    <li><strong>1:00</strong> — single bell (POI window opens)</li>
    <li><strong>6:00</strong> — single bell (POI window closes)</li>
    <li><strong>7:00</strong> — double bell (speech time ends)</li>
  </ul>
  <p>For reply speeches: single bell at 3:00, double bell at 4:00. DebateClock plays these bells automatically at the correct times.</p>

  <h2>Adjudication</h2>
  <p>Asian Parliamentary rounds are typically adjudicated by a panel of one to three judges. The adjudicators evaluate matter (content and arguments), manner (delivery and style), and method (structure and strategy). The team that wins the majority of adjudicator votes wins the round.</p>
  <p>DebateClock is an informational timing aid. Always defer to the tournament director and official adjudication panel for any disputes about timing or procedure.</p>

  <h2>Frequently asked questions</h2>
  <div class="faq">
    <details><summary>How long are Asian Parliamentary speeches?</summary><div>Constructive speeches are 7 minutes each. Reply speeches are 4 minutes each. There are 6 constructive speeches and 2 reply speeches per round.</div></details>
    <details><summary>When can POIs be offered?</summary><div>Between the 1-minute and 6-minute marks of each constructive speech. The first and last minute are protected. Reply speeches have no POI window.</div></details>
    <details><summary>Who can give the reply speech?</summary><div>Only the 1st or 2nd speaker may give the reply speech. The 3rd speaker (Whip) cannot give a reply. The Opposition replies before the Government.</div></details>
    <details><summary>Is there prep time during the round?</summary><div>No. There is no in-round prep pool in Asian Parliamentary. Teams prepare before the round during the preparation period. Speeches run back-to-back without additional preparation time between them.</div></details>
    <details><summary>Can new arguments be introduced in the reply speech?</summary><div>No. The reply speech is a summary and adjudication of the round. New arguments introduced in a reply speech are generally penalised by adjudicators.</div></details>
  </div>

  <h2>Related guides</h2>
  <ul>
    <li><a href="/formats/asian-parliamentary/">Asian Parliamentary format guide</a></li>
    <li><a href="/blog/asian-parliamentary-vs-wsdc/">Asian Parliamentary vs World Schools (WSDC)</a></li>
    <li><a href="/timer/asian-parliamentary/">Asian Parliamentary timer</a></li>
    <li><a href="/formats/world-schools/">World Schools (WSDC) format guide</a></li>
  </ul>
</div>
{DISCLAIMER}
{FOOTER}
</body>
</html>"""

# ══════════════════════════════════════════════════════════════════════════════
# 3. Add country-specific content to WSDC timer page
# ══════════════════════════════════════════════════════════════════════════════

f = pathlib.Path("timer/world-schools/index.html")
src = f.read_text()

WSDC_COUNTRY = """  <h2>WSDC timer for national and regional championships</h2>
  <p>DebateClock is used by judges and coaches at World Schools-format tournaments across multiple countries and regions. The timer preloads the correct WSDC speech order, bell schedule, and POI window automatically — no manual setup required.</p>
  <ul>
    <li><strong>Southeast Asia</strong> — tournaments in the Philippines, Malaysia, Singapore, Indonesia, Thailand, and Vietnam that use World Schools format</li>
    <li><strong>South Asia</strong> — competitions in India, Sri Lanka, Bangladesh, and Pakistan</li>
    <li><strong>Africa</strong> — tournaments in Kenya, South Africa, Nigeria, Ghana, and Uganda that follow WSDC rules</li>
    <li><strong>Australasia</strong> — Australian and New Zealand school and university competitions using World Schools format</li>
    <li><strong>Europe</strong> — international tournaments and practice rounds using WSDC format</li>
  </ul>
  <p>If your tournament uses the standard World Schools format — 8-minute speeches, POI window 1&ndash;7 minutes, reply speeches, no in-round prep — DebateClock is ready to use immediately.</p>\n"""

src = src.replace(
    "  <h2>Used across international debate circuits</h2>",
    WSDC_COUNTRY + "  <h2>Used across international debate circuits</h2>"
)
f.write_text(src)
print("ok: WSDC timer — country content added")

# ══════════════════════════════════════════════════════════════════════════════
# 4. Add country content to Asian Parli timer page
# ══════════════════════════════════════════════════════════════════════════════

f = pathlib.Path("timer/asian-parliamentary/index.html")
src = f.read_text()

ASIAN_COUNTRY = """  <h2>Asian Parliamentary timer for regional tournaments</h2>
  <p>DebateClock supports the standard Asian Parliamentary format used at competitions across Asia and Australasia. Select Asian Parliamentary from the format picker and the correct speech order, timing, and POI window load instantly.</p>
  <ul>
    <li><strong>Southeast Asia</strong> — tournaments in Singapore, Malaysia, the Philippines, Indonesia, Thailand, Vietnam, and Myanmar</li>
    <li><strong>South Asia</strong> — competitions in India, Sri Lanka, Bangladesh, and Pakistan using Asian Parliamentary format</li>
    <li><strong>Australia and New Zealand</strong> — Australasian Parliamentary competitions at secondary and tertiary level</li>
    <li><strong>Practice rounds</strong> — school and university practice sessions anywhere the format is used</li>
  </ul>
  <p>The timer includes the correct POI window (minutes 1&ndash;6), automatic bell schedule, and opposition reply before government reply — exactly as the format requires.</p>\n"""

src = src.replace(
    "  <h2>Used across Asia and Australasia</h2>",
    ASIAN_COUNTRY + "  <h2>Used across Asia and Australasia</h2>"
)
f.write_text(src)
print("ok: Asian Parli timer — country content added")

# ══════════════════════════════════════════════════════════════════════════════
# 5. Add comparison table to Asian Parli format page
# ══════════════════════════════════════════════════════════════════════════════

f = pathlib.Path("formats/asian-parliamentary/index.html")
src = f.read_text()

COMPARE_SECTION = """  <h2>How Asian Parliamentary compares to World Schools</h2>
  <p>Asian Parliamentary and World Schools are structurally similar — both use three speakers per team and reply speeches. The main differences are speech length, POI window, and motion style.</p>
  <table class="compare-table">
    <thead><tr><th>Feature</th><th>Asian Parliamentary</th><th>World Schools (WSDC)</th></tr></thead>
    <tbody>
      <tr><td>Speech length</td><td>7 minutes</td><td>8 minutes</td></tr>
      <tr><td>POI window</td><td>Minutes 1&ndash;6</td><td>Minutes 1&ndash;7</td></tr>
      <tr><td>Reply speeches</td><td>Yes (4 minutes)</td><td>Yes (4 minutes)</td></tr>
      <tr><td>Motion style</td><td>Typically impromptu</td><td>Prepared + impromptu</td></tr>
      <tr><td>Prep time in round</td><td>None</td><td>None</td></tr>
    </tbody>
  </table>
  <p>See the full comparison: <a href="/blog/asian-parliamentary-vs-wsdc/">Asian Parliamentary vs World Schools</a>.</p>\n"""

src = src.replace(
    "  <h2>Frequently asked questions</h2>",
    COMPARE_SECTION + "  <h2>Frequently asked questions</h2>"
)
f.write_text(src)
print("ok: Asian Parli format page — WSDC comparison table added")

# ══════════════════════════════════════════════════════════════════════════════
# 6. Add more WSDC and Asian Parli motions to motion generator
# ══════════════════════════════════════════════════════════════════════════════

f = pathlib.Path("practice/motions/index.html")
src = f.read_text()

NEW_MOTIONS = """
  {t:"This house believes that urbanisation does more good than harm.",f:"WSDC",topic:"Social",level:"Novice"},
  {t:"This house would give greater powers to regional governments.",f:"WSDC",topic:"Politics",level:"Novice"},
  {t:"This house believes that developed nations should pay for climate adaptation in developing nations.",f:"WSDC",topic:"Environment",level:"Varsity"},
  {t:"This house would ban the use of natural resources as a tool of foreign policy.",f:"WSDC",topic:"International",level:"Varsity"},
  {t:"This house believes that international institutions have failed to address global inequality.",f:"WSDC",topic:"International",level:"Varsity"},
  {t:"This house would make environmental education compulsory in schools.",f:"WSDC",topic:"Environment",level:"Novice"},
  {t:"This house believes that technological innovation is the best solution to poverty.",f:"WSDC",topic:"Economics",level:"Novice"},
  {t:"This house would establish an international court for environmental crimes.",f:"WSDC",topic:"Environment",level:"Varsity"},
  {t:"This house believes that cities are better places to live than rural areas.",f:"WSDC",topic:"Social",level:"Novice"},
  {t:"This house would prioritise economic development over environmental protection in developing nations.",f:"WSDC",topic:"Economics",level:"Varsity"},
  {t:"This house believes that the rise of China is good for the world.",f:"WSDC",topic:"International",level:"Varsity"},
  {t:"This house would ban the use of fossil fuels in public transport.",f:"WSDC",topic:"Environment",level:"Novice"},
  {t:"This house believes that democracy requires a free press.",f:"WSDC",topic:"Politics",level:"Novice"},
  {t:"This house would make financial education compulsory in schools.",f:"WSDC",topic:"Social",level:"Novice"},
  {t:"This house believes that international trade does more good than harm.",f:"WSDC",topic:"Economics",level:"Novice"},
  {t:"This house believes that urbanisation does more harm than good.",f:"AsianParli",topic:"Social",level:"Novice"},
  {t:"This house would increase taxes on large corporations.",f:"AsianParli",topic:"Economics",level:"Novice"},
  {t:"This house believes that social entrepreneurship is more effective than government in solving social problems.",f:"AsianParli",topic:"Economics",level:"Varsity"},
  {t:"This house would implement a four-day school week.",f:"AsianParli",topic:"Social",level:"Novice"},
  {t:"This house believes that ASEAN has failed to deliver on its promises.",f:"AsianParli",topic:"International",level:"Varsity"},
  {t:"This house would prioritise regional trade agreements over global trade agreements.",f:"AsianParli",topic:"Economics",level:"Varsity"},
  {t:"This house believes that technology has made young people less resilient.",f:"AsianParli",topic:"Science",level:"Novice"},
  {t:"This house would establish a regional human rights court for Asia.",f:"AsianParli",topic:"International",level:"Varsity"},
  {t:"This house believes that economic growth is incompatible with environmental sustainability.",f:"AsianParli",topic:"Environment",level:"Varsity"},
  {t:"This house would make civic education compulsory in schools.",f:"AsianParli",topic:"Social",level:"Novice"},
  {t:"This house believes that foreign investment does more good than harm in developing economies.",f:"AsianParli",topic:"Economics",level:"Varsity"},
  {t:"This house would cap the salaries of executives at publicly listed companies.",f:"AsianParli",topic:"Economics",level:"Varsity"},
  {t:"This house believes that online learning will replace traditional education.",f:"AsianParli",topic:"Science",level:"Novice"},
  {t:"This house would make public transport free.",f:"AsianParli",topic:"Social",level:"Novice"},
  {t:"This house believes that developing nations should prioritise economic growth over environmental protection.",f:"AsianParli",topic:"Economics",level:"Varsity"},"""

# Insert before the closing of the MOTIONS array
src = src.replace(
    "];\n\nlet pool",
    NEW_MOTIONS + "\n];\n\nlet pool"
)
f.write_text(src)
new_count = src.count("{t:")
print(f"ok: motion generator — {new_count} total motions")

# ══════════════════════════════════════════════════════════════════════════════
# 7. Write blog pages
# ══════════════════════════════════════════════════════════════════════════════

pages = [
    ("blog/asian-parliamentary-vs-wsdc/index.html", ASIAN_VS_WSDC),
    ("blog/asian-parliamentary-debate-rules/index.html", ASIAN_RULES),
]
for path, content in pages:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print(f"ok: {path}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. Update blog dashboard with new posts
# ══════════════════════════════════════════════════════════════════════════════

f = pathlib.Path("blog/index.html")
src = f.read_text()

NEW_BLOG_CARDS = """    <a href="/blog/asian-parliamentary-vs-wsdc/" class="blog-card">
      <span class="blog-card-tag tag-blog">Blog</span>
      <h3>Asian Parliamentary vs World Schools: which format should you run?</h3>
      <p>Speech length, POI windows, motion style, and regional usage — a full comparison for coaches and tournament directors.</p>
      <span class="read-more">Read post &rarr;</span>
    </a>
    <a href="/blog/asian-parliamentary-debate-rules/" class="blog-card">
      <span class="blog-card-tag tag-guide">Guide</span>
      <h3>Asian Parliamentary debate rules: complete guide</h3>
      <p>Speech order, POI rules, reply speeches, timing, and how to run an Asian Parliamentary round correctly.</p>
      <span class="read-more">Read post &rarr;</span>
    </a>"""

if 'asian-parliamentary-vs-wsdc' not in src:
    src = src.replace(
        '    <a href="/blog/lincoln-douglas-vs-public-forum/" class="blog-card">',
        NEW_BLOG_CARDS + '\n    <a href="/blog/lincoln-douglas-vs-public-forum/" class="blog-card">'
    )
    f.write_text(src)
    print("ok: blog dashboard updated with 2 new posts")

# ══════════════════════════════════════════════════════════════════════════════
# 9. Update sitemap
# ══════════════════════════════════════════════════════════════════════════════

sm = pathlib.Path("sitemap.xml").read_text()
new_urls = [
    "https://www.debateclock.org/blog/asian-parliamentary-vs-wsdc/",
    "https://www.debateclock.org/blog/asian-parliamentary-debate-rules/",
]
for url in new_urls:
    if url not in sm:
        sm = sm.replace('</urlset>',
            f'  <url><loc>{url}</loc><lastmod>2026-04-24</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
pathlib.Path("sitemap.xml").write_text(sm)
print(f"ok: sitemap — {sm.count('<url>')} URLs")
print("done.")
