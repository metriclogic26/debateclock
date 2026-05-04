#!/usr/bin/env python3
import pathlib

f = pathlib.Path("formats/lincoln-douglas/index.html")
src = f.read_text()

NEW_SECTIONS = """  <h2>Value and criterion framework</h2>
  <p>Lincoln-Douglas debate is a values-based format. Each debater presents a philosophical framework consisting of two components: a <strong>value</strong> (a broad ideal such as justice, liberty, or human dignity) and a <strong>criterion</strong> (a standard for measuring whether the value is achieved). The affirmative defends the resolution by arguing their value and criterion better upholds the resolution. The negative argues against.</p>
  <p>The value criterion framework is what distinguishes LD from Policy debate. Where Policy focuses on evidence and plan implementation, LD focuses on philosophical argumentation. A judge evaluates which debater better upholds their value premise through their criterion, and which criterion better measures the value at stake in the resolution.</p>
  <p>Common values in LD include: justice, morality, human dignity, societal welfare, autonomy, and democracy. Common criteria include: maximizing utility, upholding rights, social contract theory, and categorical imperatives.</p>

  <h2>How to flow a Lincoln-Douglas round</h2>
  <p>Flowing is the process of taking structured notes during a debate round. LD judges and debaters typically use a sheet divided into columns — one column per speech. Arguments are tracked across columns to show how each point was extended, dropped, or refuted as the round progressed.</p>
  <p>A standard LD flow sheet has 7 columns for the 7 speeches: AC, CX, NC, CX, 1AR, NR, 2AR. Arguments made in the AC are tracked left to right. If the negative doesn't respond to an argument in the NC, it is considered "dropped" and the affirmative can extend it in the 1AR as conceded ground.</p>
  <p>DebateClock's <a href="/practice/flow/">flow timer</a> helps debaters practice structured work and review intervals. The <a href="/practice/round-logger/">round logger</a> tracks actual vs allowed speech times across a full round.</p>

  <h2>Judging Lincoln-Douglas debate</h2>
  <p>LD judges evaluate three main areas: the framework debate (which value and criterion should govern the round), the substantive arguments (which debater better upholds their framework), and overall presentation and logical consistency.</p>
  <p>A judge's decision typically follows this process: first, determine which framework wins — if the affirmative's criterion is accepted, do the affirmative's arguments meet it? If the negative's framework wins, does the negative successfully negate the resolution under that framework?</p>
  <p>Practical judging notes:</p>
  <ul>
    <li>Track prep time carefully — each debater has exactly 4 minutes to use freely across the round</li>
    <li>The 1AR is the most time-pressured speech — 4 minutes to answer a 7-minute NC</li>
    <li>Dropped arguments in the NR that were clearly extended in the 1AR carry significant weight</li>
    <li>Always defer to official tournament rules for any timing disputes</li>
  </ul>

  <h2>LD resolution structure</h2>
  <p>Lincoln-Douglas resolutions are value statements, typically in the form "Resolved: [value claim]." Unlike Policy resolutions which propose a specific plan, LD resolutions assert a philosophical position for debaters to affirm or negate.</p>
  <p>The National Speech and Debate Association (NSDA) releases new LD resolutions every two months. Resolutions typically address ethical dilemmas, political philosophy, or competing social values. Examples of resolution structures include:</p>
  <ul>
    <li>Comparative value judgments: "X is preferable to Y"</li>
    <li>Obligation statements: "Governments ought to..."</li>
    <li>Evaluative claims: "X is morally justified"</li>
  </ul>
  <p>Practice debating resolutions with the <a href="/practice/motions/">LD motion generator</a> — 150+ real motions filtered by format, topic, and difficulty level.</p>

  <h2>Lincoln-Douglas vs other formats</h2>
  <p>LD is one of three major NSDA formats alongside Policy and Public Forum. The key differences:</p>
  <ul>
    <li><strong>LD vs Policy:</strong> LD is one-on-one with philosophical frameworks. Policy is two-on-two with plan-based advocacy and large evidence files. <a href="/blog/lincoln-douglas-vs-policy/">Full comparison →</a></li>
    <li><strong>LD vs Public Forum:</strong> Both are individual-accessible formats, but PF uses two-person teams and focuses on current events rather than philosophical values. <a href="/blog/lincoln-douglas-vs-public-forum/">Full comparison →</a></li>
    <li><strong>LD vs World Schools:</strong> WSDC uses three-person teams and Points of Information. LD has no POI system and is strictly one-on-one. <a href="/blog/lincoln-douglas-vs-world-schools/">Full comparison →</a></li>
  </ul>\n"""

# Insert before Related guides
src = src.replace(
    '  <h2>Related guides</h2>',
    NEW_SECTIONS + '  <h2>Related guides</h2>'
)

# Add more FAQ entries targeting GSC queries
NEW_FAQS = """    <details><summary>What is the LD debate format?</summary>
      <div>Lincoln-Douglas (LD) debate is a one-on-one competitive debate format. One debater takes the affirmative position and defends a resolution; the other takes the negative position and argues against it. LD uses a value and criterion framework to evaluate philosophical claims. Each debater has 4 minutes of shared prep time to use freely across the round.</div>
    </details>
    <details><summary>What are LD debate speech times?</summary>
      <div>Affirmative Constructive: 6 minutes. Negative Cross-Examination: 3 minutes. Negative Constructive: 7 minutes. Affirmative Cross-Examination: 3 minutes. First Affirmative Rebuttal (1AR): 4 minutes. Negative Rebuttal: 6 minutes. Second Affirmative Rebuttal (2AR): 3 minutes. Each debater also has 4 minutes of prep time.</div>
    </details>
    <details><summary>What is the 1AR in Lincoln-Douglas debate?</summary>
      <div>The First Affirmative Rebuttal (1AR) is widely considered the hardest speech in LD. The affirmative has only 4 minutes to respond to the negative's 7-minute constructive. Skilled 1AR debaters prioritize the most important arguments rather than trying to answer everything, and extend their strongest affirmative offense.</div>
    </details>
    <details><summary>How long is a Lincoln-Douglas debate round?</summary>
      <div>A full LD round lasts approximately 35-40 minutes including prep time usage. The 7 speeches total 32 minutes of speaking time (6+3+7+3+4+6+3). Each debater has up to 4 minutes of prep time, making the maximum round length around 40 minutes.</div>
    </details>
    <details><summary>What is prep time in LD debate?</summary>
      <div>Prep time is a pool of time each debater uses between speeches to prepare their next speech. In LD, each debater gets 4 minutes of prep time to use freely across the entire round — not per speech. Once used, prep time does not replenish. DebateClock tracks each debater's cumulative prep pool automatically.</div>
    </details>\n"""

if 'What is the LD debate format?' not in src:
    src = src.replace(
        '    <details><summary>What are the speech times in Lincoln-Douglas debate?</summary>',
        NEW_FAQS + '    <details><summary>What are the speech times in Lincoln-Douglas debate?</summary>'
    )
    print("ok: 5 new FAQs added")

f.write_text(src)
print(f"ok: LD format page expanded — {src.count('<h2>')} h2 sections, {src.count('<details>')} FAQ entries")
print(f"File size: {len(src):,} chars")
