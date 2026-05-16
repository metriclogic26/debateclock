#!/usr/bin/env python3
import pathlib, re

# ══════════════════════════════════════════════════════════════════════════════
# 1. EXPAND CANADIAN PARLIAMENTARY FORMAT PAGE
# ══════════════════════════════════════════════════════════════════════════════

f = pathlib.Path("formats/canadian-parliamentary/index.html")
src = f.read_text()

CUSID_SECTIONS = """  <h2>How Canadian Parliamentary debate works</h2>
  <p>Canadian Parliamentary debate (CUSID — Canadian University Society for Intercollegiate Debate) is the dominant format at Canadian university debate competitions. It is closely related to British Parliamentary and Asian Parliamentary, using 7-minute speeches with Points of Information, but with a distinct two-team structure and speech order.</p>
  <p>Two teams of two speakers compete: the Government (Proposition) and the Opposition. Each speaker gives one constructive speech, followed by rebuttal speeches from the leaders. The format rewards both substantive argumentation and quick thinking under POI pressure.</p>

  <h2>Government vs Opposition roles</h2>
  <ul>
    <li><strong>Prime Minister (PM)</strong> — opens for Government, defines the motion and presents the case</li>
    <li><strong>Leader of Opposition (LO)</strong> — responds to the PM, presents Opposition case</li>
    <li><strong>Member of Government (MG)</strong> — extends the Government case</li>
    <li><strong>Member of Opposition (MO)</strong> — extends the Opposition case</li>
    <li><strong>Leader of Opposition Rebuttal</strong> — Opposition summary, no new arguments</li>
    <li><strong>Prime Minister Rebuttal</strong> — Government final summary, no new arguments</li>
  </ul>

  <h2>Points of Information in CUSID</h2>
  <p>POIs may be offered between the 1-minute and 6-minute marks of each 7-minute constructive speech. The first and last minute are protected. POIs are not offered during rebuttal speeches.</p>
  <p>DebateClock shows the automatic POI window badge on the debater display — appearing at 1:00 and disappearing at 6:00 of each constructive speech.</p>

  <h2>How to judge Canadian Parliamentary debate</h2>
  <p>CUSID judges evaluate matter (content), manner (delivery), and method (structure). Key judging notes:</p>
  <ul>
    <li>Each team has 8 minutes of shared prep time — track cumulative usage</li>
    <li>Rebuttal speeches may not introduce new arguments</li>
    <li>POI quality and acceptance rate factor into manner scoring</li>
    <li>Government has the right to define the motion — Opposition can challenge squirrelly definitions</li>
    <li>Always defer to the official tournament director for any timing disputes</li>
  </ul>

  <h2>Canadian Parliamentary vs British Parliamentary</h2>
  <p>CUSID and BP share speech times (7 minutes) and POI windows (minutes 1-6) but differ in structure:</p>
  <ul>
    <li><strong>CUSID</strong> — 2 teams of 2 speakers, rebuttal speeches, 8 minutes prep time per team</li>
    <li><strong>BP</strong> — 4 teams of 2 speakers, no rebuttal speeches, no prep time</li>
  </ul>
  <p>A debater familiar with BP can adapt to CUSID quickly — the POI rules and speech length are identical, but the team structure and rebuttal speeches require adjustment.</p>

  <h2>Canadian Parliamentary vs American Parliamentary (APDA)</h2>
  <p>Both formats use two teams of two speakers with rebuttal speeches and prep time, but differ in speech times:</p>
  <ul>
    <li><strong>CUSID</strong> — 7-minute constructives, POI window 1-6</li>
    <li><strong>APDA</strong> — constructives range from 7-8 minutes, no evidence rule</li>
  </ul>\n"""

src = src.replace('  <h2>Frequently asked questions</h2>', CUSID_SECTIONS + '  <h2>Frequently asked questions</h2>')

CUSID_FAQS = """    <details><summary>What is Canadian Parliamentary debate (CUSID)?</summary>
      <div>Canadian Parliamentary debate (CUSID) is the dominant format at Canadian university tournaments. Two teams of two speakers compete across six speeches — four constructives and two rebuttals. It uses 7-minute speeches with Points of Information (minutes 1-6) and 8 minutes of prep time per team.</div>
    </details>
    <details><summary>What are the speech times in Canadian Parliamentary debate?</summary>
      <div>Each of the four constructive speeches is 7 minutes. Rebuttal speeches are typically 5 minutes each. POIs may be offered between the 1-minute and 6-minute marks of constructives. Each team has 8 minutes of shared prep time.</div>
    </details>
    <details><summary>How is CUSID different from British Parliamentary?</summary>
      <div>Both use 7-minute speeches and POIs (minutes 1-6), but CUSID has 2 teams of 2 speakers with rebuttal speeches and prep time. BP has 4 teams of 2 speakers with no rebuttal speeches and no prep time.</div>
    </details>
    <details><summary>Is there prep time in Canadian Parliamentary debate?</summary>
      <div>Yes. Each team has 8 minutes of shared prep time to use freely across the round. DebateClock tracks each team's cumulative prep pool automatically.</div>
    </details>
    <details><summary>What is the POI window in Canadian Parliamentary debate?</summary>
      <div>POIs may be offered between the 1-minute and 6-minute marks of each 7-minute constructive speech. The first and last minute are protected. POIs are not offered during rebuttal speeches.</div>
    </details>\n"""

if 'What is Canadian Parliamentary debate' not in src:
    faq_div = src.find('class="faq"')
    if faq_div > 0:
        insert_pos = src.find('>', faq_div) + 1
        src = src[:insert_pos] + '\n' + CUSID_FAQS + src[insert_pos:]
        print("ok: CUSID FAQs added")

desc = re.search(r'<meta name="description" content="[^"]*">', src)
if desc:
    src = src.replace(desc.group(), '<meta name="description" content="Canadian Parliamentary (CUSID) debate format guide. Speech times, POI rules, Government vs Opposition roles, and free CUSID timer with prep pool tracking.">')
    print("ok: CUSID meta description updated")

old_title = src[src.find('<title>'):src.find('</title>')+8]
if 'Canadian' in old_title:
    src = src.replace(old_title, '<title>Canadian Parliamentary (CUSID) Debate Format: Speech Times, Rules & Free Timer</title>')
    print("ok: CUSID title updated")

f.write_text(src)
print(f"ok: CUSID format page — {src.count('<h2>')} h2s, {src.count('<details>')} FAQs, {len(src):,} chars")

# ══════════════════════════════════════════════════════════════════════════════
# 2. ADD INTERNAL LINKS TO LD FORMAT PAGE from other format pages
# ══════════════════════════════════════════════════════════════════════════════

pages_to_update = [
    "formats/policy-debate/index.html",
    "formats/public-forum/index.html",
    "formats/world-schools/index.html",
    "formats/british-parliamentary/index.html",
    "blog/lincoln-douglas-vs-policy/index.html",
    "blog/lincoln-douglas-vs-public-forum/index.html",
    "blog/lincoln-douglas-vs-world-schools/index.html",
]

LD_LINK = '<a href="/formats/lincoln-douglas/">Lincoln-Douglas format guide</a>'
updated = 0

for path in pages_to_update:
    f = pathlib.Path(path)
    if not f.exists():
        continue
    content = f.read_text()
    # Check if LD format link already present
    if '/formats/lincoln-douglas/' in content:
        continue
    # Add LD format link in Related guides section
    if '<h2>Related guides</h2>' in content:
        content = content.replace(
            '<h2>Related guides</h2>',
            f'<h2>Related guides</h2>\n  <p>See also: {LD_LINK} — complete speech order, prep pool rules, and judging guide.</p>'
        )
        f.write_text(content)
        updated += 1

print(f"ok: internal links to LD format page added to {updated} pages")
print("done.")
