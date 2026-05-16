#!/usr/bin/env python3
import pathlib

# 1. Fix formats/lincoln-douglas title tag
f = pathlib.Path("formats/lincoln-douglas/index.html")
src = f.read_text()

# Update title to match "ld time format", "ld round structure" queries
old_title = src[src.find('<title>'):src.find('</title>')+8]
if 'Lincoln-Douglas' in old_title:
    src = src.replace(old_title, '<title>Lincoln-Douglas (LD) Debate Format: Speech Times, Round Structure & Free Timer</title>')
    print("ok: LD format page title updated")

# Update meta description
import re
desc_match = re.search(r'<meta name="description" content="[^"]*">', src)
if desc_match:
    src = src.replace(desc_match.group(), '<meta name="description" content="Lincoln-Douglas debate format guide. LD speech times, round structure, 4-minute prep pool, and free LD timer. Complete one-on-one format reference for debaters and judges.">')
    print("ok: LD format page description updated")

f.write_text(src)

# 2. Fix timer/lincoln-douglas description to target "ld debate timer" better
f = pathlib.Path("timer/lincoln-douglas/index.html")
src = f.read_text()
desc_match = re.search(r'<meta name="description" content="[^"]*">', src)
if desc_match:
    src = src.replace(desc_match.group(), '<meta name="description" content="Free LD debate timer with shared 4-minute prep pool. All 7 Lincoln-Douglas speeches preloaded, two-device sync, works on iPhone. No signup.">')
    print("ok: LD timer page description updated")
f.write_text(src)

# 3. Add FAQ entries targeting high-impression queries to LD format page
f = pathlib.Path("formats/lincoln-douglas/index.html")
src = f.read_text()

NEW_FAQS = """    <details><summary>What are the speech times in Lincoln-Douglas debate?</summary>
      <div>Lincoln-Douglas uses 7 speeches: Affirmative Constructive (6 min), Negative Cross-Examination (3 min), Negative Constructive (7 min), Affirmative Cross-Examination (3 min), First Affirmative Rebuttal (4 min), Negative Rebuttal (6 min), Second Affirmative Rebuttal (3 min). Each debater also has 4 minutes of prep time to use freely across the round.</div>
    </details>
    <details><summary>What is the LD debate round structure?</summary>
      <div>An LD round has 7 timed speeches plus prep time. The Affirmative speaks first and last. The Negative has the longest constructive speech at 7 minutes. Cross-examination periods follow the first two constructive speeches. Both debaters have a shared prep pool of 4 minutes each to use between speeches.</div>
    </details>
    <details><summary>How do you judge a Lincoln-Douglas debate?</summary>
      <div>LD judges evaluate the philosophical framework each debater presents, then assess which side better upheld their value and criterion throughout the round. Judges track prep time usage, speech times, and cross-examination. DebateClock handles timing automatically — select LD from the format picker and all 7 speeches load with correct times and the 4-minute prep pool.</div>
    </details>"""

if 'What are the speech times in Lincoln-Douglas' not in src:
    # Find the FAQ section and add entries
    if '<div class="faq">' in src:
        src = src.replace('<div class="faq">', '<div class="faq">\n' + NEW_FAQS)
        print("ok: LD format page FAQs added")
    elif 'class="faq"' in src:
        idx = src.find('class="faq"')
        insert_pos = src.find('>', idx) + 1
        src = src[:insert_pos] + '\n' + NEW_FAQS + src[insert_pos:]
        print("ok: LD format page FAQs added (alt method)")

f.write_text(src)

print("done.")
