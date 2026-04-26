#!/usr/bin/env python3
"""
Add Umami analytics snippet to every HTML page's <head>.
Run from project root: python3 add-umami.py
"""
import pathlib

UMAMI = '  <script defer src="https://cloud.umami.is/script.js" data-website-id="983c91be-28ac-4280-b541-aa45730b0d7e"></script>\n'

html_files = list(pathlib.Path(".").rglob("*.html"))
html_files = [f for f in html_files if "node_modules" not in str(f) and ".git" not in str(f)]

added = []
skipped = []

for f in sorted(html_files):
    src = f.read_text()
    if "umami.is" in src:
        skipped.append(str(f))
        continue
    if "</head>" not in src:
        skipped.append(str(f) + " (no </head>)")
        continue
    src = src.replace("</head>", UMAMI + "</head>", 1)
    f.write_text(src)
    added.append(str(f))

print(f"Added to {len(added)} files:")
for f in added:
    print(f"  {f}")

print(f"\nSkipped {len(skipped)} files:")
for f in skipped:
    print(f"  {f}")

print(f"\nTotal HTML files processed: {len(html_files)}")
