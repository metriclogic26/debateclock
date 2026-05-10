#!/usr/bin/env python3
import pathlib

f = pathlib.Path("formats/policy-debate/index.html")
src = f.read_text()

NEW_SECTIONS = """  <h2>How Policy debate works</h2>
  <p>Policy debate (also called CX or Cross-Examination debate) is a two-on-two team format where one team defends a policy proposal (the affirmative) and the other team argues against it (the negative). The affirmative team reads a prepared case advocating for a specific plan within the year's resolution. The negative team runs a variety of strategies to defeat the case.</p>
  <p>Unlike Lincoln-Douglas debate, which focuses on philosophical values, Policy debate centers on evidence-based advocacy. Teams prepare large evidence files throughout the year and read cards (cited evidence) rapidly during speeches. Fast delivery — known as spreading — is common at competitive levels, allowing debaters to cover more arguments per speech.</p>

  <h2>Evidence and case construction</h2>
  <p>Policy debate relies heavily on evidence. Teams cut cards — excerpts from academic papers, news articles, and government documents — and organize them into files. A typical Policy debater carries hundreds of cards to a tournament, organized by argument type.</p>
  <p>The affirmative case typically includes:</p>
  <ul>
    <li><strong>Inherency</strong> — why the problem exists under the status quo</li>
    <li><strong>Harms/Significance</strong> — the scale of the problem</li>
    <li><strong>Solvency</strong> — how the plan fixes the problem</li>
  </ul>
  <p>The negative runs responses such as disadvantages (the plan causes harm), counterplans (an alternative to the affirmative plan), and kritiks (challenges to the affirmative's assumptions or framework).</p>

  <h2>The negative block — the key strategic moment</h2>
  <p>The negative block consists of two consecutive negative speeches: the 2NC (8 minutes) and the 1NR (5 minutes), totaling 13 minutes of negative speech time with only the 1AR (5 minutes) in between. This is the negative's primary opportunity to extend their strongest arguments and collapse the debate to the issues most likely to win.</p>
  <p>The 2AC must answer everything in the 1NC. The 1AR — at only 5 minutes — must respond to the entire negative block. The 1AR is widely considered the hardest speech in Policy debate for this reason.</p>

  <h2>How to judge Policy debate</h2>
  <p>Policy judges evaluate which team wins the flow — the structured tracking of arguments across all speeches. A dropped argument (one the opposing team never responded to) is typically conceded. Judges track whether arguments were extended, answered, or dropped across the round.</p>
  <p>Practical judging notes for Policy:</p>
  <ul>
    <li>Each team has 8 minutes of prep time — track cumulative usage, not per-speech</li>
    <li>Cross-examination is 3 minutes after the 1AC, 1NC, 2AC, and 2NC</li>
    <li>The negative block (2NC + 1NR) is the strategic center of the round</li>
    <li>Always defer to official tournament rules for any timing disputes</li>
  </ul>

  <h2>Policy vs Lincoln-Douglas vs Public Forum</h2>
  <p>Policy is the most evidence-intensive and team-oriented of the three major NSDA formats:</p>
  <ul>
    <li><strong>Policy vs LD:</strong> Policy is 2v2 with plan advocacy and large evidence files. LD is 1v1 with philosophical frameworks. Policy rounds are typically faster-paced with more evidence. <a href="/blog/lincoln-douglas-vs-policy/">Full comparison →</a></li>
    <li><strong>Policy vs PF:</strong> Both are team formats but PF uses shorter speeches, focuses on current events, and has crossfire instead of cross-examination. Policy allows more complex argumentation.</li>
    <li><strong>Policy vs World Schools:</strong> WSDC uses 3-person teams with Points of Information. Policy has no POI system and is strictly evidence-based.</li>
  </ul>

  <h2>Policy debate topics and resolutions</h2>
  <p>The National Speech and Debate Association (NSDA) releases one Policy resolution per year. Unlike LD (which changes every two months) or PF (which changes monthly), Policy teams research and debate the same resolution for the entire academic year. This allows for deep specialization and highly developed argumentation on both sides.</p>
  <p>Policy resolutions typically propose a policy action by the US federal government, such as "The United States federal government should substantially increase its funding and/or regulation of..." Topics cover areas like energy policy, foreign policy, criminal justice, and economic policy.</p>\n"""

# Insert before Related guides
src = src.replace(
    '  <h2>Related guides</h2>',
    NEW_SECTIONS + '  <h2>Related guides</h2>'
)

# Add FAQ entries
NEW_FAQS = """    <details><summary>What is CX debate?</summary>
      <div>CX debate (Cross-Examination debate) is another name for Policy debate. The name comes from the cross-examination periods — 3-minute question-and-answer sessions after each constructive speech where the opposing team questions the speaker. Policy/CX is a two-on-two team format focused on evidence-based advocacy for a policy plan.</div>
    </details>
    <details><summary>What are Policy debate speech times?</summary>
      <div>First Affirmative Constructive (1AC): 8 minutes. Negative Cross-Examination: 3 minutes. First Negative Constructive (1NC): 8 minutes. Affirmative Cross-Examination: 3 minutes. Second Affirmative Constructive (2AC): 8 minutes. Negative Cross-Examination: 3 minutes. Second Negative Constructive (2NC): 8 minutes. Affirmative Cross-Examination: 3 minutes. First Negative Rebuttal (1NR): 5 minutes. First Affirmative Rebuttal (1AR): 5 minutes. Second Negative Rebuttal (2NR): 5 minutes. Second Affirmative Rebuttal (2AR): 3 minutes. Each team also has 8 minutes of shared prep time.</div>
    </details>
    <details><summary>How long is a Policy debate round?</summary>
      <div>A full Policy round lasts approximately 90 minutes including prep time. The 12 speeches total 68 minutes of speaking time, plus up to 16 minutes of prep time (8 per team), plus time between speeches.</div>
    </details>
    <details><summary>What is spreading in Policy debate?</summary>
      <div>Spreading is the technique of speaking very quickly to read more evidence and arguments per speech. At competitive levels, Policy debaters can speak at 300-400 words per minute. Spreading allows teams to make more arguments than the opponent can answer in the allotted time. It is a legal but contested technique — some judges prefer slower, clearer delivery.</div>
    </details>
    <details><summary>What is prep time in Policy debate?</summary>
      <div>Each team in Policy debate has 8 minutes of shared prep time to use freely across the round. Teams use prep time between speeches to organize their flow, prepare responses, and select which cards to read. DebateClock tracks each team's cumulative prep pool automatically — the remaining balance carries forward between speeches.</div>
    </details>\n"""

if 'What is CX debate?' not in src:
    # Find FAQ section and insert
    faq_div = src.find('class="faq"')
    if faq_div > 0:
        insert_pos = src.find('>', faq_div) + 1
        src = src[:insert_pos] + '\n' + NEW_FAQS + src[insert_pos:]
        print("ok: 5 new FAQs added")

# Update meta description
import re
desc = re.search(r'<meta name="description" content="[^"]*">', src)
if desc:
    src = src.replace(desc.group(), '<meta name="description" content="Policy (CX) debate format guide. Speech times, prep pool rules, negative block strategy, evidence and flowing. Free Policy debate timer with 8-minute prep pool tracking.">')
    print("ok: meta description updated")

# Update title
src = src.replace(
    '<title>Policy Debate Format: Speech Order, CX Rules & Prep Pool | DebateClock</title>',
    '<title>Policy (CX) Debate Format: Speech Times, Rules & Free Timer | DebateClock</title>'
)

f.write_text(src)
print(f"ok: Policy format page expanded — {src.count('<h2>')} h2 sections, {src.count('<details>')} FAQ entries")
print(f"File size: {len(src):,} chars")
