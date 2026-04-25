#!/usr/bin/env python3
import pathlib, re

f = pathlib.Path("index.html")
src = f.read_text()

# ── 1. Add descriptive text after hero ────────────────────────────────────────
HERO_DESC = """  <section class="about-section" style="max-width:720px;margin:0 auto;padding:0 24px 48px;text-align:center;">
    <p style="font-size:16px;color:#8B90A0;line-height:1.75;margin-bottom:16px;">
      DebateClock is a free, browser-based debate timer with real-time two-device sync.
      The judge controls the timer on their phone. The debater sees a full-screen countdown
      on their laptop or tablet. No signup, no install — just open the link and start timing.
    </p>
    <p style="font-size:15px;color:#5B6175;line-height:1.75;">
      Most debate timers treat prep time as a per-speech countdown that resets each speech.
      DebateClock correctly implements a shared prep time pool — a bank of time each side
      draws from freely across the entire round, carrying the remaining balance forward
      between speeches automatically.
    </p>
  </section>\n"""

# Insert after the hero section
src = src.replace(
    '  <!-- HOW IT WORKS',
    HERO_DESC + '  <!-- HOW IT WORKS'
)

# ── 2. Add format section descriptions ───────────────────────────────────────
US_DESC = """    <p style="font-size:14px;color:#8B90A0;line-height:1.7;margin-bottom:20px;">
      Lincoln-Douglas, Policy (CX), and Public Forum are the three main NSDA competitive
      debate formats used at US high school and college tournaments. Each uses a shared
      prep time pool — LD gives 4 minutes per debater, Policy gives 8 minutes per team,
      and PF gives 3 minutes per team. DebateClock tracks each pool cumulatively across
      the round.
    </p>\n"""

INTL_DESC = """    <p style="font-size:14px;color:#8B90A0;line-height:1.7;margin-bottom:20px;">
      World Schools (WSDC) and British Parliamentary are the dominant international debate
      formats. Both use Points of Information — brief interjections during speeches — with
      automatic POI window signals. DebateClock shows a visual POI indicator on the debater
      display at the correct time for each format.
    </p>\n"""

PRACTICE_DESC = """    <p style="font-size:14px;color:#8B90A0;line-height:1.7;margin-bottom:20px;">
      Practice tools for coaches and debaters. Time individual speeches with a prep
      countdown, manage an extemp prep room with up to 10 simultaneous student countdowns,
      log actual vs allowed speech times, run structured work-break intervals, and keep
      your entire tournament schedule on countdown all day.
    </p>\n"""

src = src.replace(
    '    <div class="formats-region-label">&#127482;&#127480; US Formats</div>',
    US_DESC + '    <div class="formats-region-label">&#127482;&#127480; US Formats</div>'
)
src = src.replace(
    '    <div class="formats-region-label" style="margin-top:20px;">&#127758; International Formats</div>',
    INTL_DESC + '    <div class="formats-region-label" style="margin-top:20px;">&#127758; International Formats</div>'
)
src = src.replace(
    '    <div class="formats-region-label" style="margin-top:20px;">&#127908; Practice Tools</div>',
    PRACTICE_DESC + '    <div class="formats-region-label" style="margin-top:20px;">&#127908; Practice Tools</div>'
)

# ── 3. Add FAQ section before footer ─────────────────────────────────────────
FAQ_HTML = """
<section style="max-width:720px;margin:0 auto;padding:48px 24px;">
  <h2 style="font-size:22px;font-weight:700;color:#E8EAF0;margin-bottom:24px;">Frequently asked questions</h2>
  <div style="display:flex;flex-direction:column;gap:10px;">
    <details style="background:#111318;border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:14px 18px;">
      <summary style="font-size:14px;font-weight:600;color:#E8EAF0;cursor:pointer;list-style:none;">What is DebateClock?</summary>
      <p style="font-size:14px;color:#8B90A0;line-height:1.7;margin-top:10px;">DebateClock is a free browser-based debate timer with real-time two-device sync. The judge controls the timer on their phone while the debater sees a full-screen countdown on their own device. It supports 9 debate formats including Lincoln-Douglas, Policy, Public Forum, World Schools, and British Parliamentary.</p>
    </details>
    <details style="background:#111318;border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:14px 18px;">
      <summary style="font-size:14px;font-weight:600;color:#E8EAF0;cursor:pointer;list-style:none;">Which debate formats does DebateClock support?</summary>
      <p style="font-size:14px;color:#8B90A0;line-height:1.7;margin-top:10px;">DebateClock supports Lincoln-Douglas (LD), Policy (CX), Public Forum (PF), Parliamentary (APDA), World Schools (WSDC), British Parliamentary University (WUDC), British Parliamentary High School, Asian Parliamentary, and Canadian Parliamentary (CUSID). Each format has the correct speech order, prep pool, and POI windows preloaded.</p>
    </details>
    <details style="background:#111318;border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:14px 18px;">
      <summary style="font-size:14px;font-weight:600;color:#E8EAF0;cursor:pointer;list-style:none;">How does the shared prep time pool work?</summary>
      <p style="font-size:14px;color:#8B90A0;line-height:1.7;margin-top:10px;">The prep time pool is a shared bank of time that each side draws from freely across the entire round. Unlike most timer apps that reset prep time for each speech, DebateClock tracks the pool cumulatively — time used before one speech is subtracted from the total, and the remaining balance carries forward to the next prep call automatically.</p>
    </details>
    <details style="background:#111318;border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:14px 18px;">
      <summary style="font-size:14px;font-weight:600;color:#E8EAF0;cursor:pointer;list-style:none;">Does DebateClock work on mobile?</summary>
      <p style="font-size:14px;color:#8B90A0;line-height:1.7;margin-top:10px;">Yes. DebateClock works on most phones, tablets, and laptops with a modern browser. No app download or installation is required. The judge controller is optimised for mobile use, and the debater display works on any screen size.</p>
    </details>
    <details style="background:#111318;border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:14px 18px;">
      <summary style="font-size:14px;font-weight:600;color:#E8EAF0;cursor:pointer;list-style:none;">How does two-device sync work?</summary>
      <p style="font-size:14px;color:#8B90A0;line-height:1.7;margin-top:10px;">The judge opens the timer on their phone at debateclock.org/app. A QR code and room link appear automatically. The debater scans the QR code or opens the link on their laptop — a full-screen countdown appears immediately and stays in sync with the judge's controller in real time.</p>
    </details>
    <details style="background:#111318;border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:14px 18px;">
      <summary style="font-size:14px;font-weight:600;color:#E8EAF0;cursor:pointer;list-style:none;">Is DebateClock free?</summary>
      <p style="font-size:14px;color:#8B90A0;line-height:1.7;margin-top:10px;">Yes. DebateClock is completely free with no signup required. All features including two-device sync, all 9 formats, practice tools, and the motion generator are available at no cost.</p>
    </details>
  </div>
</section>

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"What is DebateClock?","acceptedAnswer":{"@type":"Answer","text":"DebateClock is a free browser-based debate timer with real-time two-device sync. It supports 9 debate formats including Lincoln-Douglas, Policy, Public Forum, World Schools, and British Parliamentary."}},
{"@type":"Question","name":"Which debate formats does DebateClock support?","acceptedAnswer":{"@type":"Answer","text":"DebateClock supports Lincoln-Douglas (LD), Policy (CX), Public Forum (PF), Parliamentary (APDA), World Schools (WSDC), British Parliamentary University, British Parliamentary High School, Asian Parliamentary, and Canadian Parliamentary (CUSID)."}},
{"@type":"Question","name":"How does the shared prep time pool work?","acceptedAnswer":{"@type":"Answer","text":"The prep time pool is a shared bank of time that each side draws from freely across the entire round. Time used before one speech is subtracted from the total, and the remaining balance carries forward automatically."}},
{"@type":"Question","name":"Does DebateClock work on mobile?","acceptedAnswer":{"@type":"Answer","text":"Yes. DebateClock works on most phones, tablets, and laptops with a modern browser. No app download or installation is required."}},
{"@type":"Question","name":"How does two-device sync work?","acceptedAnswer":{"@type":"Answer","text":"The judge opens the timer on their phone. A QR code appears. The debater scans it and a full-screen countdown appears on their device, synced in real time with the judge."}},
{"@type":"Question","name":"Is DebateClock free?","acceptedAnswer":{"@type":"Answer","text":"Yes. DebateClock is completely free with no signup required. All features are available at no cost."}}
]}
</script>"""

src = src.replace(
    '<div class="site-disclaimer">',
    FAQ_HTML + '\n<div class="site-disclaimer">'
)

# ── 4. Add SoftwareApplication schema ────────────────────────────────────────
APP_SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"SoftwareApplication","name":"DebateClock","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","description":"Free browser-based debate timer with real-time two-device sync. Supports 9 formats including LD, Policy, PF, WSDC, and BP. Shared prep time pool, POI windows, motion generator.","url":"https://www.debateclock.org/","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"featureList":["Two-device real-time sync","9 debate formats","Shared prep time pool","POI window indicator","Motion generator","Practice tools"]}
</script>\n"""

src = src.replace('<link rel="canonical"', APP_SCHEMA + '<link rel="canonical"')

f.write_text(src)
print("ok: hero description added")
print("ok: US/International/Practice format descriptions added")
print("ok: FAQ section with schema added")
print("ok: SoftwareApplication schema added")
print(f"Total file size: {len(src):,} chars")
