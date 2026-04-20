#!/usr/bin/env python3
import pathlib

fixes = [
    ("timer/world-schools/index.html",
     "Works on any phone, tablet, or laptop \u00b7 Used in 70+ countries",
     "Works on most phones, tablets, and laptops with a modern browser"),

    ("formats/world-schools/index.html",
     "World Schools Debating Championships (WSDC) is a three-on-three international debate format used in over 70 countries.",
     "World Schools Debating Championships (WSDC) is a three-on-three international debate format competed across dozens of countries worldwide."),

    ("setup/judge-paradigm/index.html",
     "This means: the link never expires, never requires renewal, and works even if you haven't opened the app yet when the debater clicks it. When you open the app on your phone, your room is already waiting with any debaters who joined from the link.",
     "This means: the link is persistent and deterministic \u2014 the same name always generates the same room code. When you open the app on your phone, any debaters who joined from the link will be in the same room."),

    ("formats/lincoln-douglas/index.html",
     "It is the most popular individual debate event in US high school competition",
     "It is one of the most widely competed individual debate events in US high school competition"),

    ("formats/public-forum/index.html",
     "It is the most popular team debate event in US high school competition.",
     "It is one of the most widely competed team debate events in US high school competition."),

    ("blog/debate-timer-prep-time/index.html",
     "The remaining time is always visible and carries forward automatically.",
     "The remaining time is visible throughout the round and carries forward automatically."),

    ("timer/world-schools/index.html",
     "No signup, works on any device.",
     "No signup required."),
]

for path, old, new in fixes:
    f = pathlib.Path(path)
    if not f.exists():
        print(f"skip (missing): {path}")
        continue
    src = f.read_text()
    if old in src:
        f.write_text(src.replace(old, new, 1))
        print(f"ok: {path}")
    else:
        print(f"miss: {path[:40]} -- {old[:50]}")

print("done.")
