#!/usr/bin/env python3
import pathlib, re

f = pathlib.Path("formats/parliamentary/index.html")
src = f.read_text()

NEW_SECTIONS = """  <h2>How Parliamentary debate works</h2>
  <p>Parliamentary debate (also called APDA — American Parliamentary Debate Association format) is a two-on-two team format used primarily at US college and university tournaments. The Government team proposes and defends a case; the Opposition team argues against it. Unlike Policy debate, Parliamentary debate uses no prepared evidence — debaters must construct arguments from general knowledge and logic on the spot.</p>
  <p>Parliamentary debate is fast-paced and rewards quick thinking, broad knowledge, and strong argumentation skills. Motions are typically announced 15-20 minutes before the round, giving teams minimal time to prepare their cases.</p>

  <h2>Government vs Opposition roles</h2>
  <p>The Government team has the right to define the motion — they choose how to interpret the resolution and what specific case to defend. The Prime Minister opens the debate with the Government's definition and case. The Opposition team must respond to the Government's interpretation, though they can challenge an unreasonable definition.</p>
  <ul>
    <li><strong>Prime Minister (PM)</strong> — opens for Government, sets the definition and case</li>
    <li><strong>Leader of Opposition (LO)</strong> — responds to the PM, presents Opposition case</li>
    <li><strong>Member of Government (MG)</strong> — extends Government case, responds to Opposition</li>
    <li><strong>Member of Opposition (MO)</strong> — extends Opposition case, responds to Government</li>
    <li><strong>Leader of Opposition Rebuttal (LOR)</strong> — Opposition summary and rebuttal</li>
    <li><strong>Prime Minister Rebuttal (PMR)</strong> — Government final summary, no new arguments</li>
  </ul>

  <h2>Points of Information in Parliamentary debate</h2>
  <p>Points of Information (POIs) are offered during the four main constructive speeches. During each constructive, the opposing team may stand and offer a POI between the 1-minute and 6-minute marks. The first and last minute of each constructive are protected.</p>
  <p>To offer a POI, a debater stands and says "Point of information" or "On that point." The speaker may accept or decline. Accepted POIs should last no more than 15 seconds. Speakers are generally expected to accept 1-2 POIs per speech.</p>
  <p>POIs are not offered during rebuttal speeches (LOR and PMR).</p>

  <h2>No evidence rule</h2>
  <p>Parliamentary debate prohibits the use of prepared evidence. Debaters may not read from notes containing pre-written arguments, cards, or research. All arguments must be constructed from general knowledge, logic, and examples developed during the preparation period. This distinguishes Parliamentary from Policy debate, which relies heavily on evidence files.</p>
  <p>Debaters may use notes to track arguments made during the round (flowing) but may not read from pre-prepared material.</p>

  <h2>How to judge Parliamentary debate</h2>
  <p>Parliamentary judges evaluate the quality of argumentation, logical consistency, and persuasiveness. Since no evidence is used, judges focus on the strength of reasoning and examples rather than source quality.</p>
  <ul>
    <li>Each team has 8 minutes of shared prep time — track cumulative usage across the round</li>
    <li>The PMR may not introduce new arguments — it is a summary and extension of previous Government arguments</li>
    <li>Government has the right to define the motion — but an unreasonable or squirrelly definition can be challenged</li>
    <li>POIs are offered during constructives only, not during rebuttals</li>
    <li>Always defer to the official tournament director for any timing disputes</li>
  </ul>

  <h2>Parliamentary vs other formats</h2>
  <ul>
    <li><strong>Parliamentary vs Policy:</strong> Both are 2v2 team formats but Policy uses prepared evidence and longer speeches. Parliamentary uses no evidence and rewards impromptu argumentation.</li>
    <li><strong>Parliamentary vs British Parliamentary:</strong> APDA has 2 teams of 2 with rebuttal speeches. BP has 4 teams of 2 with no rebuttals. APDA has prep time; BP does not.</li>
    <li><strong>Parliamentary vs World Schools:</strong> Both have POIs and no prepared evidence in constructives. WSDC uses 3-person teams with reply speeches; APDA uses 2-person teams with separate rebuttal speeches.</li>
  </ul>\n"""

src = src.replace('  <h2>Frequently asked questions</h2>', NEW_SECTIONS + '  <h2>Frequently asked questions</h2>')

NEW_FAQS = """    <details><summary>What is APDA debate?</summary>
      <div>APDA (American Parliamentary Debate Association) is the governing body for parliamentary debate at US colleges and universities. The format uses two teams of two speakers, no prepared evidence, Points of Information during constructive speeches, and 8 minutes of prep time per team. Motions are announced 15-20 minutes before the round.</div>
    </details>
    <details><summary>What are the speech times in Parliamentary debate?</summary>
      <div>Prime Minister Constructive: 7 minutes. Leader of Opposition Constructive: 8 minutes. Member of Government: 8 minutes. Member of Opposition: 8 minutes. Leader of Opposition Rebuttal: 4 minutes. Prime Minister Rebuttal: 5 minutes. Each team also has 8 minutes of shared prep time.</div>
    </details>
    <details><summary>Is evidence allowed in Parliamentary debate?</summary>
      <div>No. Parliamentary debate prohibits prepared evidence. All arguments must be constructed from general knowledge and logic during the preparation period. Debaters may flow (take notes on) arguments made during the round but cannot read from pre-prepared cards or research.</div>
    </details>
    <details><summary>What is prep time in Parliamentary debate?</summary>
      <div>Each team has 8 minutes of shared prep time to use freely across the round. Teams typically use prep time before their constructive speeches to organize their arguments. DebateClock tracks each team's cumulative prep pool automatically.</div>
    </details>
    <details><summary>What is the PMR in Parliamentary debate?</summary>
      <div>The Prime Minister Rebuttal (PMR) is the final speech of a Parliamentary round. It is given by the Prime Minister and serves as a summary of the Government's case and a response to Opposition arguments. The PMR may not introduce new arguments — it must extend and crystallize arguments already made in the round.</div>
    </details>\n"""

if 'What is APDA debate?' not in src:
    faq_div = src.find('class="faq"')
    if faq_div > 0:
        insert_pos = src.find('>', faq_div) + 1
        src = src[:insert_pos] + '\n' + NEW_FAQS + src[insert_pos:]
        print("ok: Parliamentary FAQs added")

desc = re.search(r'<meta name="description" content="[^"]*">', src)
if desc:
    src = src.replace(desc.group(), '<meta name="description" content="Parliamentary (APDA) debate format guide. Speech times, POI rules, no-evidence rule, Government vs Opposition roles, and free Parliamentary timer with prep pool tracking.">')
    print("ok: meta description updated")

old_title = src[src.find('<title>'):src.find('</title>')+8]
if 'Parliamentary' in old_title:
    src = src.replace(old_title, '<title>Parliamentary (APDA) Debate Format: Speech Times, Rules & Free Timer</title>')
    print("ok: title updated")

f.write_text(src)
print(f"ok: Parliamentary format page — {src.count('<h2>')} h2s, {src.count('<details>')} FAQs, {len(src):,} chars")
