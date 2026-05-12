#!/usr/bin/env python3
import pathlib, re

f = pathlib.Path("formats/british-parliamentary/index.html")
src = f.read_text()

NEW_SECTIONS = """  <h2>How British Parliamentary debate works</h2>
  <p>British Parliamentary (BP) debate is a four-team format used at university competitions worldwide, including the World Universities Debating Championship (WUDC). Four teams of two speakers compete simultaneously in each round: Opening Government (OG), Opening Opposition (OO), Closing Government (CG), and Closing Opposition (CO). Each team is ranked first through fourth — only one team wins each round.</p>
  <p>BP is the dominant format at university debating circuits in the UK, Ireland, Australia, Europe, Southeast Asia, and Africa. It is also used at high school level with shorter speech times (5 minutes instead of 7).</p>

  <h2>The four team roles</h2>
  <p>Each of the four teams has a distinct role in the round:</p>
  <ul>
    <li><strong>Opening Government (OG)</strong> — sets the debate by defining the motion and presenting the first government case. The Prime Minister speaks first.</li>
    <li><strong>Opening Opposition (OO)</strong> — challenges the government definition and case, presenting the first opposition arguments.</li>
    <li><strong>Closing Government (CG)</strong> — must extend the debate with a new government argument (the extension) while supporting OG. Cannot simply repeat OG's case.</li>
    <li><strong>Closing Opposition (CO)</strong> — must similarly extend with new opposition material. The Opposition Whip gives the final speech of the round.</li>
  </ul>
  <p>The closing teams face a strategic challenge: they must differentiate from the opening teams to earn a first or second place finish, but cannot directly contradict their bench partners.</p>

  <h2>Points of Information in BP</h2>
  <p>Points of Information (POIs) are brief interjections offered during speeches. In BP, POIs may be offered between the 1-minute and 6-minute marks of each 7-minute speech (or 0:30 to 4:30 in high school BP with 5-minute speeches). The first and last minute of each speech are protected.</p>
  <p>To offer a POI, a debater stands and says "Point of information" or "On that point." The speaker may accept or decline. Accepted POIs should last no more than 15 seconds. Speakers are expected to accept 1-2 POIs per speech — accepting none is considered evasive.</p>
  <p>DebateClock displays an automatic amber POI badge on the debater display that appears and disappears at the correct times for both university BP (7-minute speeches) and high school BP (5-minute speeches).</p>

  <h2>How to judge British Parliamentary debate</h2>
  <p>BP judges rank all four teams from first to fourth. The judging criteria are matter (content and arguments), manner (delivery and style), and method (structure and strategy).</p>
  <p>Key judging considerations:</p>
  <ul>
    <li>Closing teams must bring a genuine extension — new material that advances the bench's case, not a summary of opening arguments</li>
    <li>The team that best defines and wins the key clash of the debate typically ranks highly</li>
    <li>POI quantity and quality factor into manner scores — speakers who avoid all POIs or whose POIs are irrelevant lose manner points</li>
    <li>There is no prep time in BP — speeches run consecutively with no time between them for preparation</li>
    <li>Always defer to the official tournament director for any timing disputes</li>
  </ul>

  <h2>BP University vs BP High School</h2>
  <p>The two variants of British Parliamentary differ primarily in speech length:</p>
  <ul>
    <li><strong>BP University (WUDC standard)</strong> — 7-minute speeches, POI window minutes 1-6</li>
    <li><strong>BP High School</strong> — 5-minute speeches, POI window 0:30 to 4:30</li>
  </ul>
  <p>DebateClock has separate presets for both variants. The <a href="/formats/british-parliamentary-high-school/">BP High School format guide</a> covers the high school variant in detail.</p>

  <h2>British Parliamentary vs other formats</h2>
  <ul>
    <li><strong>BP vs World Schools (WSDC)</strong> — Both use POIs but WSDC has 2 teams of 3 speakers with reply speeches. BP has 4 teams of 2 speakers with no reply speeches. <a href="/blog/wsdc-vs-british-parliamentary/">Full comparison →</a></li>
    <li><strong>BP vs Asian Parliamentary</strong> — Asian Parliamentary has 2 teams of 3 with reply speeches. BP has 4 teams of 2 with no replies. <a href="/blog/asian-parliamentary-vs-wsdc/">Asian Parli vs WSDC →</a></li>
    <li><strong>BP vs Lincoln-Douglas</strong> — LD is 1v1 with philosophical frameworks and prep pools. BP is 4-team with POIs and no prep time. <a href="/blog/lincoln-douglas-vs-world-schools/">LD vs World Schools →</a></li>
  </ul>\n"""

# Insert before Related guides
src = src.replace(
    '  <h2>Related guides</h2>',
    NEW_SECTIONS + '  <h2>Related guides</h2>'
)

# Add FAQ entries
NEW_FAQS = """    <details><summary>What is British Parliamentary debate?</summary>
      <div>British Parliamentary (BP) debate is a four-team format where Opening Government, Opening Opposition, Closing Government, and Closing Opposition each give one speech. All four teams compete simultaneously and are ranked first through fourth. It is the format used at the World Universities Debating Championship (WUDC).</div>
    </details>
    <details><summary>What are the BP debate speech times?</summary>
      <div>In university BP (WUDC standard), each of the 8 speeches is 7 minutes with a POI window from minute 1 to minute 6. In high school BP, speeches are 5 minutes with a POI window from 0:30 to 4:30. There is no prep time in BP — speeches run consecutively.</div>
    </details>
    <details><summary>How many teams compete in a BP round?</summary>
      <div>Four teams of two speakers compete in each BP round: Opening Government, Opening Opposition, Closing Government, and Closing Opposition. Each team is ranked 1st through 4th — only one team wins, and one team comes last.</div>
    </details>
    <details><summary>What is an extension in BP debate?</summary>
      <div>An extension is the unique contribution a closing team makes to advance their bench's case. Closing teams cannot simply repeat opening arguments — they must introduce new material that extends the debate. A strong extension is the primary factor that separates closing teams from their opening bench partners in the adjudicators' ranking.</div>
    </details>
    <details><summary>Is there prep time in British Parliamentary debate?</summary>
      <div>No. There is no in-round prep time in BP. Speakers receive their motion at the start of the round and have 15 minutes of preparation before the round begins. Once the round starts, speeches run consecutively with no additional preparation time between them.</div>
    </details>\n"""

if 'What is British Parliamentary debate?' not in src:
    faq_div = src.find('class="faq"')
    if faq_div > 0:
        insert_pos = src.find('>', faq_div) + 1
        src = src[:insert_pos] + '\n' + NEW_FAQS + src[insert_pos:]
        print("ok: 5 new FAQs added")

# Update meta description
desc = re.search(r'<meta name="description" content="[^"]*">', src)
if desc:
    src = src.replace(desc.group(), '<meta name="description" content="British Parliamentary debate format guide. Four-team structure, 7-minute speeches, POI rules, closing half strategy, and free BP timer for university and high school BP.">')
    print("ok: meta description updated")

# Update title
old_title = src[src.find('<title>'):src.find('</title>')+8]
if 'British Parliamentary' in old_title:
    src = src.replace(old_title, '<title>British Parliamentary (BP) Debate Format: Rules, Speech Times & Free Timer</title>')
    print("ok: title updated")

f.write_text(src)
print(f"ok: BP format page expanded — {src.count('<h2>')} h2 sections, {src.count('<details>')} FAQ entries")
print(f"File size: {len(src):,} chars")
