#!/usr/bin/env python3
import pathlib

# Fix motions
f = pathlib.Path("practice/motions/index.html")
src = f.read_text()

src = src.replace(
    '{t:"This house believes that the rise of China is good for the world.",f:"WSDC",topic:"International",level:"Varsity"},',
    '{t:"This house believes that economic interdependence promotes peace.",f:"WSDC",topic:"International",level:"Varsity"},'
)
src = src.replace(
    '{t:"This house believes that ASEAN has failed to deliver on its promises.",f:"AsianParli",topic:"International",level:"Varsity"},',
    '{t:"This house believes that regional organisations are more effective than global ones.",f:"AsianParli",topic:"International",level:"Varsity"},'
)
src = src.replace(
    '{t:"This house believes that mass surveillance is justified in the fight against terrorism.",f:"WSDC",topic:"Politics",level:"Varsity"},',
    '{t:"This house believes that national security should take precedence over individual privacy.",f:"WSDC",topic:"Politics",level:"Varsity"},'
)
f.write_text(src)
print("ok: 3 sensitive motions replaced")

# Fix Debatekeeper alternative page
f = pathlib.Path("alternative/debatekeeper/index.html")
src = f.read_text()
src = src.replace(
    'works on any device (iPhone, Android, laptop, tablet)',
    'works on most devices with a modern browser (iPhone, Android, laptop, tablet)'
)
src = src.replace(
    'DebateClock runs in any browser — iPhone included',
    'DebateClock runs in most modern browsers — iPhone included'
)
f.write_text(src)
print("ok: debatekeeper page absolutes softened")

# Fix timer pages
timer_files = [
    "timer/lincoln-douglas/index.html",
    "timer/public-forum/index.html",
    "timer/world-schools/index.html",
    "timer/policy-debate/index.html",
    "timer/british-parliamentary/index.html",
    "timer/parliamentary/index.html",
    "timer/asian-parliamentary/index.html",
    "timer/canadian-parliamentary/index.html",
]
for path in timer_files:
    f = pathlib.Path(path)
    if not f.exists():
        continue
    src = f.read_text()
    src = src.replace("Opens in any browser.", "Works in most modern browsers.")
    src = src.replace("Works on any device.", "Works on most devices with a modern browser.")
    src = src.replace("works on any device", "works on most devices with a modern browser")
    src = src.replace("any browser", "most modern browsers")
    f.write_text(src)
print("ok: timer pages absolutes softened")
print("done.")
