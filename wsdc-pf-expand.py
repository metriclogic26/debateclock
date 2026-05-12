#!/usr/bin/env python3
import pathlib, re

# ══════════════════════════════════════════════════════════════════════════════
# WORLD SCHOOLS
# ══════════════════════════════════════════════════════════════════════════════

f = pathlib.Path("formats/world-schools/index.html")
src = f.read_text()

WSDC_SECTIONS = """  <h2>How World Schools debate works</h2>
  <p>World Schools Debating (WSDC) is a three-on-three international debate format used at national championships and the World Schools Debating Championships. Two teams of three speakers — Proposition and Opposition — compete across eight speeches including six constructives and two reply speeches. The format combines prepared and impromptu motions, Points of Information, and a unique reply speech system where the Opposition replies before the Proposition.</p>
  <p>World Schools is the dominant international format across Asia, Africa, Europe, and Australasia. Countries including Singapore, Kenya, South Africa, Australia, the Philippines, India, and over 50 others compete in WSDC-affiliated tournaments.</p>

  <h2>Prepared vs impromptu motions</h2>
  <p>WSDC tournaments use a mix of two motion types:</p>
  <ul>
    <li><strong>Prepared motions</strong> — announced weeks before the tournament, allowing deep research and case construction. Teams prepare evidence, arguments, and rebuttals in advance.</li>
    <li><strong>Impromptu motions</strong> — announced one hour before the round. Teams receive the motion and have 60 minutes to prepare their case with no outside assistance once the timer starts.</li>
  </ul>
  <p>The ratio of prepared to impromptu motions varies by tournament. Major international competitions like WSDC typically use a mix, with preliminary rounds often being impromptu and elimination rounds being prepared.</p>

  <h2>How to judge a World Schools round</h2>
  <p>WSDC judges evaluate matter (content and arguments), manner (delivery and presentation), and method (structure and strategy). Each criterion is weighted equally in most WSDC circuits.</p>
  <p>Practical judging notes:</p>
  <ul>
    <li>Track POI windows carefully — amber badge appears at 1:00 and disappears at 7:00 on the DebateClock debater display</li>
    <li>The Opposition reply is given before the Proposition reply — Opposition speaks seventh, Proposition speaks last</li>
    <li>Reply speeches cannot introduce new arguments — they are a biased summary of why the team won</li>
    <li>Only the 1st or 2nd speaker may give the reply — not the 3rd speaker</li>
    <li>There is no prep time during the round — speeches run consecutively</li>
    <li>Always defer to the official tournament director for any timing disputes</li>
  </ul>

  <h2>World Schools vs British Parliamentary</h2>
  <p>WSDC and BP are the two dominant international formats but differ significantly in structure:</p>
  <ul>
    <li>WSDC: 2 teams of 3 speakers, reply speeches, 8-minute speeches, POI window 1-7</li>
    <li>BP: 4 teams of 2 speakers, no reply speeches, 7-minute speeches, POI window 1-6</li>
  </ul>
  <p><a href="/blog/wsdc-vs-british-parliamentary/">Full WSDC vs BP comparison →</a></p>

  <h2>World Schools vs Asian Parliamentary</h2>
  <p>WSDC and Asian Parliamentary share the same basic structure (2 teams of 3, reply speeches) but differ in speech length and motion style:</p>
  <ul>
    <li>WSDC: 8-minute speeches, POI window 1-7, prepared + impromptu motions</li>
    <li>Asian Parli: 7-minute speeches, POI window 1-6, typically impromptu motions</li>
  </ul>
  <p><a href="/blog/asian-parliamentary-vs-wsdc/">Full Asian Parliamentary vs WSDC comparison →</a></p>\n"""

src = src.replace('  <h2>Related guides</h2>', WSDC_SECTIONS + '  <h2>Related guides</h2>')

WSDC_FAQS = """    <details><summary>What is World Schools debate?</summary>
      <div>World Schools Debating (WSDC) is a three-on-three international debate format. Two teams of three speakers compete across eight speeches — six constructives and two reply speeches. It uses Points of Information and a mix of prepared and impromptu motions. It is the format used at the World Schools Debating Championships.</div>
    </details>
    <details><summary>What are the speech times in World Schools debate?</summary>
      <div>Each of the six main constructive speeches is 8 minutes. Reply speeches are 4 minutes each. The POI window is open from minute 1 to minute 7 of each constructive speech. There is no prep time during the round.</div>
    </details>
    <details><summary>Who gives the reply speech in WSDC?</summary>
      <div>The reply speech is given by either the 1st or 2nd speaker — the 3rd speaker may not give a reply. The Opposition gives their reply before the Proposition, so the Proposition has the last word in the round.</div>
    </details>
    <details><summary>What is the difference between prepared and impromptu motions?</summary>
      <div>Prepared motions are announced weeks before the tournament, allowing teams to research and prepare cases in advance. Impromptu motions are announced one hour before the round, requiring teams to construct their case on the spot with no outside assistance.</div>
    </details>
    <details><summary>How many countries compete in World Schools debate?</summary>
      <div>Over 50 countries compete in WSDC-affiliated competitions globally, including Singapore, Kenya, South Africa, Australia, the Philippines, India, the UK, Ireland, and many others across Asia, Africa, Europe, and Australasia.</div>
    </details>\n"""

if 'What is World Schools debate?' not in src:
    faq_div = src.find('class="faq"')
    if faq_div > 0:
        insert_pos = src.find('>', faq_div) + 1
        src = src[:insert_pos] + '\n' + WSDC_FAQS + src[insert_pos:]
        print("ok: WSDC FAQs added")

desc = re.search(r'<meta name="description" content="[^"]*">', src)
if desc:
    src = src.replace(desc.group(), '<meta name="description" content="World Schools (WSDC) debate format guide. Speech times, POI rules, reply speeches, prepared vs impromptu motions, and free WSDC timer with automatic POI signal.">')
    print("ok: WSDC meta description updated")

old_title = src[src.find('<title>'):src.find('</title>')+8]
if 'World Schools' in old_title:
    src = src.replace(old_title, '<title>World Schools (WSDC) Debate Format: Speech Times, POI Rules & Free Timer</title>')
    print("ok: WSDC title updated")

f.write_text(src)
print(f"ok: WSDC format page — {src.count('<h2>')} h2s, {src.count('<details>')} FAQs, {len(src):,} chars")


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC FORUM
# ══════════════════════════════════════════════════════════════════════════════

f = pathlib.Path("formats/public-forum/index.html")
src = f.read_text()

PF_SECTIONS = """  <h2>How Public Forum debate works</h2>
  <p>Public Forum (PF) debate is a two-on-two team format focused on current events and policy. Two teams — Pro and Con — debate a resolution that changes monthly. PF is designed to be accessible to general audiences, emphasizing clear argumentation over technical jargon. It is one of the most popular NSDA formats at US high school tournaments.</p>
  <p>PF uses a unique structure with crossfire periods — open question-and-answer sessions where both speakers from opposing teams question each other simultaneously. The grand crossfire involves all four debaters.</p>

  <h2>PF topics and resolutions</h2>
  <p>Public Forum resolutions change monthly and focus on current events, policy debates, and international relations. Unlike Lincoln-Douglas (philosophical values) or Policy (year-long research), PF topics are released a month in advance and focus on real-world issues. Debaters research current news sources, government reports, and academic papers relevant to the monthly topic.</p>
  <p>The monthly topic rotation means PF debaters need to quickly adapt their research and argumentation style. Breadth of knowledge across many topic areas is valued over deep specialization in one area.</p>

  <h2>Crossfire in Public Forum</h2>
  <p>Public Forum has three crossfire periods that distinguish it from other formats:</p>
  <ul>
    <li><strong>Crossfire #1</strong> — 3 minutes between the two 1st speakers after their constructives</li>
    <li><strong>Crossfire #2</strong> — 3 minutes between the two 2nd speakers after their constructives</li>
    <li><strong>Grand Crossfire</strong> — 3 minutes with all four debaters after the summary speeches</li>
  </ul>
  <p>Crossfire is a simultaneous exchange — unlike cross-examination in Policy or LD where one team asks and the other answers, both PF speakers may ask and answer questions during crossfire. Strong crossfire performance can significantly influence judge decisions.</p>

  <h2>How to judge Public Forum debate</h2>
  <p>PF judges evaluate the flow (tracking of arguments across speeches), the quality of evidence, and the debaters' ability to clash directly with opposing arguments. PF judges often have less technical debate experience than LD or Policy judges — arguments should be clear and accessible.</p>
  <p>Practical judging notes:</p>
  <ul>
    <li>Each team has 3 minutes of shared prep time — track cumulative usage across the round</li>
    <li>The Final Focus (2 minutes each) is the last speech — judges often weight these heavily</li>
    <li>Crossfire exchanges are not flowed but can influence overall impression scores</li>
    <li>Summary speeches should crystallize the round to 1-2 key issues</li>
    <li>Always defer to the official tournament director for any timing disputes</li>
  </ul>

  <h2>Public Forum vs Lincoln-Douglas vs Policy</h2>
  <ul>
    <li><strong>PF vs LD:</strong> PF is 2v2 focused on current events with crossfire. LD is 1v1 focused on philosophical values with cross-examination. PF topics change monthly; LD topics change every two months. <a href="/blog/lincoln-douglas-vs-public-forum/">Full comparison →</a></li>
    <li><strong>PF vs Policy:</strong> Both are team formats but Policy uses year-long research, much longer speeches, and spreading. PF is faster to pick up for new debaters with shorter speeches and accessible topics.</li>
  </ul>\n"""

src = src.replace('  <h2>Related guides</h2>', PF_SECTIONS + '  <h2>Related guides</h2>')

PF_FAQS = """    <details><summary>What is Public Forum debate?</summary>
      <div>Public Forum (PF) debate is a two-on-two team format where Pro and Con teams debate a monthly current events resolution. It features unique crossfire periods — open question-and-answer exchanges between opposing speakers. PF is one of the most popular NSDA formats at US high school tournaments.</div>
    </details>
    <details><summary>What are the PF debate speech times?</summary>
      <div>Each team gives two 4-minute constructive speeches, one 3-minute summary speech, and one 2-minute final focus. There are three 3-minute crossfire periods. Each team also has 3 minutes of shared prep time to use freely across the round.</div>
    </details>
    <details><summary>What is grand crossfire in PF?</summary>
      <div>Grand crossfire is a 3-minute period after the summary speeches where all four debaters participate simultaneously. Unlike the earlier crossfires (which involve only the two speakers of the same position), grand crossfire involves both speakers from both teams questioning each other openly.</div>
    </details>
    <details><summary>How does prep time work in Public Forum?</summary>
      <div>Each team has 3 minutes of shared prep time to use freely across the entire round — not per speech. Once used, prep time does not replenish. DebateClock tracks each team's cumulative prep pool automatically, carrying the remaining balance forward between speeches.</div>
    </details>
    <details><summary>How often do PF topics change?</summary>
      <div>Public Forum topics change monthly. The NSDA releases a new resolution each month, requiring debaters to research fresh current events topics regularly. This contrasts with Policy (one topic per year) and Lincoln-Douglas (one topic per two months).</div>
    </details>\n"""

if 'What is Public Forum debate?' not in src:
    faq_div = src.find('class="faq"')
    if faq_div > 0:
        insert_pos = src.find('>', faq_div) + 1
        src = src[:insert_pos] + '\n' + PF_FAQS + src[insert_pos:]
        print("ok: PF FAQs added")

desc = re.search(r'<meta name="description" content="[^"]*">', src)
if desc:
    src = src.replace(desc.group(), '<meta name="description" content="Public Forum debate format guide. Speech times, crossfire rules, prep pool, monthly topics, and free PF timer with shared 3-minute prep pool tracking.">')
    print("ok: PF meta description updated")

old_title = src[src.find('<title>'):src.find('</title>')+8]
if 'Public Forum' in old_title:
    src = src.replace(old_title, '<title>Public Forum (PF) Debate Format: Speech Times, Crossfire Rules & Free Timer</title>')
    print("ok: PF title updated")

f.write_text(src)
print(f"ok: PF format page — {src.count('<h2>')} h2s, {src.count('<details>')} FAQs, {len(src):,} chars")
print("done.")
