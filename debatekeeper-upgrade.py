#!/usr/bin/env python3
import pathlib

f = pathlib.Path("alternative/debatekeeper/index.html")
src = f.read_text()

# 1. Upgrade the comparison table to cover all formats
OLD_TABLE_START = '<h2>Feature comparison</h2>\n  <table class="compare-table">'
OLD_TABLE_END = '</table>'

# Find and replace the entire table
import re
table_match = re.search(r'<h2>Feature comparison</h2>.*?</table>', src, re.DOTALL)
if table_match:
    NEW_TABLE = """<h2>Feature comparison</h2>
  <p>This table is based on Debatekeeper's public documentation and GitHub repository. Last verified April 2026.</p>
  <table class="compare-table">
    <thead>
      <tr>
        <th>Feature</th>
        <th>DebateClock</th>
        <th>Debatekeeper</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Platform</td><td>Any browser (iPhone, Android, laptop, tablet)</td><td>Android only</td></tr>
      <tr><td>iPhone / iOS support</td><td>&#10003; Yes</td><td>&#10007; No</td></tr>
      <tr><td>No install required</td><td>&#10003; Yes — open link in browser</td><td>&#10007; Requires APK install</td></tr>
      <tr><td>Lincoln-Douglas (LD)</td><td>&#10003; Full prep pool support</td><td>&#10007; Not supported</td></tr>
      <tr><td>Policy (CX)</td><td>&#10003; Full prep pool support</td><td>&#10007; Not supported</td></tr>
      <tr><td>Public Forum (PF)</td><td>&#10003; Full prep pool support</td><td>&#10007; Not supported</td></tr>
      <tr><td>Parliamentary (APDA)</td><td>&#10003; Yes</td><td>&#10003; Yes</td></tr>
      <tr><td>British Parliamentary (University)</td><td>&#10003; Yes</td><td>&#10003; Yes</td></tr>
      <tr><td>British Parliamentary (High School)</td><td>&#10003; Yes — 5 min speeches, correct POI window</td><td>&#10007; Not supported per documentation</td></tr>
      <tr><td>World Schools (WSDC)</td><td>&#10003; Automatic POI signal min 1&ndash;7</td><td>&#10003; Yes</td></tr>
      <tr><td>Asian Parliamentary</td><td>&#10003; Automatic POI signal min 1&ndash;6</td><td>&#10003; Yes</td></tr>
      <tr><td>Canadian Parliamentary (CUSID)</td><td>&#10003; Yes</td><td>&#10003; Yes</td></tr>
      <tr><td>Shared prep time pool (LD/Policy/PF)</td><td>&#10003; Cumulative pool, carries forward</td><td>&#10007; Not supported</td></tr>
      <tr><td>Two-device sync (judge + debater display)</td><td>&#10003; Real-time, any two devices</td><td>&#10007; Single device only</td></tr>
      <tr><td>POI window signal on debater display</td><td>&#10003; Automatic amber badge</td><td>&#10007; No debater display</td></tr>
      <tr><td>Debater display (full-screen countdown)</td><td>&#10003; Separate screen, read-only</td><td>&#10007; No</td></tr>
      <tr><td>QR code room join</td><td>&#10003; Yes</td><td>&#10007; No</td></tr>
      <tr><td>No signup or account required</td><td>&#10003; Yes</td><td>&#10003; Yes</td></tr>
      <tr><td>Free</td><td>&#10003; Yes</td><td>&#10003; Yes</td></tr>
      <tr><td>Custom format builder</td><td>Coming soon</td><td>&#10003; XML format files</td></tr>
      <tr><td>Offline operation</td><td>Partial (timer works, sync needs connection)</td><td>&#10003; Fully offline</td></tr>
      <tr><td>Motion generator</td><td>&#10003; 150+ real motions, filter by format</td><td>&#10007; No</td></tr>
      <tr><td>Practice tools</td><td>&#10003; Extemp prep room, round logger, flow timer</td><td>&#10007; No</td></tr>
    </tbody>
  </table>"""
    src = src.replace(table_match.group(), NEW_TABLE)
    print("ok: comparison table upgraded")
else:
    print("miss: table not found")

# 2. Add BP High School section after "two issues" section
BPHS_SECTION = """
  <h2>British Parliamentary High School — a third gap</h2>
  <p>Beyond iOS and US formats, there is a third format Debatekeeper explicitly does not support: British Parliamentary High School. BP High School uses 5-minute speeches and a different POI window (0:30&ndash;4:30) compared to the standard 7-minute university format. Debatekeeper's documentation notes this variant is not supported.</p>
  <p>DebateClock has a dedicated BP High School preset with the correct 5-minute speech times and POI window, loaded automatically when you select the format.</p>
  <p><a href="/formats/british-parliamentary-high-school/">BP High School format guide &rarr;</a></p>"""

src = src.replace(
    '  <h2>Feature comparison</h2>',
    BPHS_SECTION + '\n\n  <h2>Feature comparison</h2>'
)
print("ok: BP High School section added")

# 3. Add HowTo schema in head
HOWTO_SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HowTo","name":"How to switch from Debatekeeper to DebateClock","totalTime":"PT1M","step":[
{"@type":"HowToStep","position":1,"name":"Open DebateClock on your phone","text":"Go to debateclock.org/app in your browser. No download or install required."},
{"@type":"HowToStep","position":2,"name":"Select your format","text":"Tap the format pill in the top bar and select your debate format. Speech order and prep pool load automatically."},
{"@type":"HowToStep","position":3,"name":"Share the display link","text":"Tap COPY or show the QR code to the debater. They open it on their device for a full-screen countdown."},
{"@type":"HowToStep","position":4,"name":"Start timing","text":"Tap Start when the first speech begins. The prep pool tracks automatically."}
]}
</script>\n"""

src = src.replace('</head>', HOWTO_SCHEMA + '</head>')
print("ok: HowTo schema added")

# 4. Add more FAQ entries
NEW_FAQS = """    <details class="faq-item">
      <summary>Does DebateClock support BP High School (5-minute speeches)?</summary>
      <div>Yes. DebateClock has a dedicated BP High School preset with 5-minute speeches and the correct POI window (0:30&ndash;4:30). Debatekeeper's documentation states this variant is not supported.</div>
    </details>
    <details class="faq-item">
      <summary>Can I use DebateClock offline?</summary>
      <div>The timer itself continues running without an internet connection once the page has loaded. Two-device sync requires a connection to stay in sync. If Wi-Fi drops during a round, the judge controller continues timing and re-syncs automatically when the connection returns. For fully offline use without any sync, use the judge controller as a standalone timer.</div>
    </details>
    <details class="faq-item">
      <summary>Does DebateClock work on Android?</summary>
      <div>Yes. DebateClock works in most modern browsers on Android — Chrome, Firefox, and Samsung Internet all work. No APK download required, just open the link.</div>
    </details>
    <details class="faq-item">
      <summary>How does the two-device sync work?</summary>
      <div>The judge opens the timer on their phone. A QR code and room link appear automatically. The debater scans the QR or opens the link on their laptop — a full-screen countdown appears and stays in sync with the judge in real time. The debater display is read-only.</div>
    </details>"""

src = src.replace(
    '  <h2>Frequently asked questions</h2>\n  <div class="faq">',
    '  <h2>Frequently asked questions</h2>\n  <div class="faq">\n' + NEW_FAQS
)
print("ok: 4 new FAQ entries added")

# 5. Fix remaining "any phone" absolute claim
src = src.replace(
    'Full prep pool support for LD, Policy, and PF. Works on any phone, tablet, or laptop.',
    'Full prep pool support for LD, Policy, and PF. Works on most phones, tablets, and laptops with a modern browser.'
)
print("ok: absolute claim softened")

f.write_text(src)
print("done.")
