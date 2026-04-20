#!/usr/bin/env python3
import pathlib, re

# ── 1. Blog dashboard — add 3 new comparison posts ────────────────────────────
f = pathlib.Path("blog/index.html")
src = f.read_text()

NEW_CARDS = """    <a href="/blog/lincoln-douglas-vs-public-forum/" class="blog-card">
      <span class="blog-card-tag tag-blog">Blog</span>
      <h3>Lincoln-Douglas vs Public Forum: which format is right for you?</h3>
      <p>Team size, speech length, prep time, topic style, and which format suits different debaters.</p>
      <span class="read-more">Read post &rarr;</span>
    </a>
    <a href="/blog/lincoln-douglas-vs-policy/" class="blog-card">
      <span class="blog-card-tag tag-blog">Blog</span>
      <h3>Lincoln-Douglas vs Policy debate: key differences explained</h3>
      <p>Speech times, prep pools, team structure, topic style, and which format suits different competitive goals.</p>
      <span class="read-more">Read post &rarr;</span>
    </a>
    <a href="/blog/lincoln-douglas-vs-world-schools/" class="blog-card">
      <span class="blog-card-tag tag-blog">Blog</span>
      <h3>Lincoln-Douglas vs World Schools: US vs international formats</h3>
      <p>POIs vs cross-examination, team size, prep time, reply speeches — a full structural comparison.</p>
      <span class="read-more">Read post &rarr;</span>
    </a>"""

# Insert before the closing of the blog grid section
src = src.replace(
    '    <a href="/blog/judge-debater-sync/" class="blog-card">',
    NEW_CARDS + '\n    <a href="/blog/judge-debater-sync/" class="blog-card">'
)
f.write_text(src)
print("ok: blog dashboard — 3 new posts added")

# ── 2. Correct NAV (with motion generator) ────────────────────────────────────
CORRECT_NAV = """<nav class="site-nav">
  <a class="brand" href="/"><span class="brand-dot"></span>DebateClock</a>
  <div class="nav-links">
    <div class="nav-dropdown">
      <button class="nav-dropdown-trigger">Competition &#9662;</button>
      <div class="nav-dropdown-menu">
        <div class="nav-dropdown-section">Timer</div>
        <a href="/app/">Two-device timer <span class="tag">Live</span></a>
        <a href="/setup/judge-paradigm/">Tabroom paradigm setup</a>
        <div class="nav-dropdown-section">US Formats</div>
        <a href="/timer/lincoln-douglas/">Lincoln-Douglas</a>
        <a href="/timer/policy-debate/">Policy (CX)</a>
        <a href="/timer/public-forum/">Public Forum</a>
        <a href="/timer/parliamentary/">Parliamentary</a>
        <div class="nav-dropdown-section">International</div>
        <a href="/timer/world-schools/">World Schools (WSDC)</a>
        <a href="/timer/british-parliamentary/">British Parliamentary</a>
        <a href="/timer/asian-parliamentary/">Asian Parliamentary</a>
        <a href="/timer/canadian-parliamentary/">Canadian (CUSID)</a>
      </div>
    </div>
    <div class="nav-dropdown">
      <button class="nav-dropdown-trigger">Practice &#9662;</button>
      <div class="nav-dropdown-menu">
        <div class="nav-dropdown-section">Practice Tools</div>
        <a href="/practice/motion/">Motion timer <span class="tag">New</span></a>
        <a href="/practice/motions/">Motion generator <span class="tag">New</span></a>
        <a href="/practice/extemp/">Extemp prep room <span class="tag">New</span></a>
        <a href="/practice/round-logger/">Round logger <span class="tag">New</span></a>
        <a href="/practice/flow/">Flow timer <span class="tag">New</span></a>
        <a href="/practice/tournament/">Tournament schedule <span class="tag">New</span></a>
        <div class="nav-dropdown-section">Resources</div>
        <a href="/blog/">Blog &amp; guides</a>
        <a href="/formats/lincoln-douglas/">Format guides</a>
      </div>
    </div>
  </div>
  <a class="nav-cta" href="/app/">Open timer</a>
</nav>"""

CORRECT_FOOTER = """<footer class="site-footer">
  <div class="footer-cols">
    <div class="footer-col">
      <h4>Competition</h4>
      <a href="/app/">Two-device timer</a>
      <a href="/setup/judge-paradigm/">Tabroom paradigm setup</a>
      <a href="/timer/lincoln-douglas/">Lincoln-Douglas</a>
      <a href="/timer/policy-debate/">Policy (CX)</a>
      <a href="/timer/public-forum/">Public Forum</a>
      <a href="/timer/world-schools/">World Schools (WSDC)</a>
      <a href="/timer/british-parliamentary/">British Parliamentary</a>
    </div>
    <div class="footer-col">
      <h4>Practice Tools</h4>
      <a href="/practice/motion/">Motion timer</a>
      <a href="/practice/motions/">Motion generator</a>
      <a href="/practice/extemp/">Extemp prep room</a>
      <a href="/practice/round-logger/">Round logger</a>
      <a href="/practice/flow/">Flow timer</a>
      <a href="/practice/tournament/">Tournament schedule</a>
    </div>
    <div class="footer-col">
      <h4>Guides &amp; Blog</h4>
      <a href="/blog/">All guides</a>
      <a href="/formats/lincoln-douglas/">LD format guide</a>
      <a href="/formats/public-forum/">PF format guide</a>
      <a href="/formats/world-schools/">WSDC format guide</a>
      <a href="/formats/british-parliamentary/">BP format guide</a>
      <a href="/blog/debate-timer-prep-time/">Prep time explained</a>
      <a href="/blog/wsdc-vs-british-parliamentary/">WSDC vs BP</a>
      <a href="/blog/tournament-day-setup/">Tournament day setup</a>
    </div>
  </div>
  <div class="footer-row">
    <div><a href="/" style="display:inline-flex;align-items:center;gap:8px;color:var(--muted);text-decoration:none;"><span style="width:12px;height:12px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);"></span>DebateClock</a><span style="margin-left:12px;">free browser debate timer</span></div>
    <a href="https://tally.so/r/QKAMOX" target="_blank" rel="noopener" class="feedback-btn">&#9733; Give feedback</a>
  </div>
</footer>"""

# ── 3. Update nav + footer on ALL pages ───────────────────────────────────────
all_pages = list(pathlib.Path(".").rglob("index.html"))
all_pages = [p for p in all_pages if 'node_modules' not in str(p)]

nav_updated = footer_updated = 0
for page in all_pages:
    src = page.read_text()
    changed = False

    new_src = re.sub(r'<nav class="site-nav">.*?</nav>', CORRECT_NAV, src, flags=re.DOTALL, count=1)
    if new_src != src:
        src = new_src
        nav_updated += 1
        changed = True

    new_src = re.sub(r'<footer class="site-footer">.*?</footer>', CORRECT_FOOTER, src, flags=re.DOTALL, count=1)
    if new_src != src:
        src = new_src
        footer_updated += 1
        changed = True

    if changed:
        page.write_text(src)

print(f"ok: nav updated on {nav_updated} pages")
print(f"ok: footer updated on {footer_updated} pages")

# ── 4. Homepage — add motion generator tile ───────────────────────────────────
hp = pathlib.Path("index.html")
src = hp.read_text()

OLD_TILE = """      <a href="/practice/motion/" class="format-card">
        <h3>Motion Practice Timer</h3>
        <p>Individual &middot; All formats</p>
        <div class="prep">Prep countdown + speech timer</div>
      </a>"""

NEW_TILE = """      <a href="/practice/motion/" class="format-card">
        <h3>Motion Practice Timer</h3>
        <p>Individual &middot; All formats</p>
        <div class="prep">Prep countdown + speech timer</div>
      </a>
      <a href="/practice/motions/" class="format-card">
        <h3>Motion Generator</h3>
        <p>All formats &middot; 120+ motions</p>
        <div class="prep">Filter by topic &amp; level</div>
      </a>"""

if OLD_TILE in src:
    src = src.replace(OLD_TILE, NEW_TILE)
    hp.write_text(src)
    print("ok: homepage motion generator tile added")
else:
    print("skip: homepage tile already present or anchor not found")

# ── 5. Update sitemap lastmod ─────────────────────────────────────────────────
print(f"ok: all done")
