#!/usr/bin/env python3
import pathlib, re

f = pathlib.Path("index.html")
src = f.read_text()

# Replace the entire formats section
OLD = re.search(r'<section class="formats">.*?</section>', src, re.DOTALL).group()

NEW = """<section class="formats">
    <div class="formats-header">
      <h2 style="font-size:20px;font-weight:700;color:#E8EAF0;margin:0 0 4px;">All supported formats</h2>
      <p style="font-size:14px;color:#8B90A0;margin:0;">Click any format to see the speech order and open the timer.</p>
    </div>
    <div class="formats-region-label">&#127482;&#127480; US Formats</div>
    <div class="format-grid">
      <a href="/timer/lincoln-douglas/" class="format-card">
        <h3>Lincoln-Douglas</h3>
        <p>1v1 &middot; 7 speeches</p>
        <div class="prep">4 min prep per debater</div>
      </a>
      <a href="/timer/policy-debate/" class="format-card">
        <h3>Policy (CX)</h3>
        <p>2v2 &middot; 12 speeches</p>
        <div class="prep">8 min prep per team</div>
      </a>
      <a href="/timer/public-forum/" class="format-card">
        <h3>Public Forum</h3>
        <p>2v2 &middot; 11 speeches</p>
        <div class="prep">3 min prep per team</div>
      </a>
      <a href="/timer/parliamentary/" class="format-card">
        <h3>Parliamentary</h3>
        <p>2v2 &middot; 6 speeches</p>
        <div class="prep no-prep">No prep &middot; POI windows</div>
      </a>
    </div>
    <div class="formats-region-label" style="margin-top:20px;">&#127758; International Formats</div>
    <div class="format-grid">
      <a href="/timer/world-schools/" class="format-card">
        <h3>World Schools (WSDC)</h3>
        <p>3v3 &middot; 8 speeches</p>
        <div class="prep no-prep">No prep &middot; POI min 1&ndash;7</div>
      </a>
      <a href="/timer/british-parliamentary/" class="format-card">
        <h3>British Parliamentary</h3>
        <p>4 teams &middot; 8 speeches</p>
        <div class="prep no-prep">No prep &middot; POI min 1&ndash;6</div>
      </a>
      <a href="/timer/asian-parliamentary/" class="format-card">
        <h3>Asian Parliamentary</h3>
        <p>3v3 &middot; 8 speeches</p>
        <div class="prep no-prep">No prep &middot; POI min 1&ndash;6</div>
      </a>
      <a href="/timer/canadian-parliamentary/" class="format-card">
        <h3>Canadian Parli (CUSID)</h3>
        <p>2v2 &middot; 8 speeches</p>
        <div class="prep no-prep">No prep &middot; POI min 1&ndash;6</div>
      </a>
    </div>
    <div class="formats-region-label" style="margin-top:20px;">&#127908; Speech Events</div>
    <div class="format-grid">
      <a href="/practice/motion/" class="format-card">
        <h3>Extemp / Impromptu</h3>
        <p>Individual &middot; Timed prep</p>
        <div class="prep">Motion timer + prep room clock</div>
      </a>
    </div>
  </section>"""

src = src.replace(OLD, NEW)

# Add region label + no-prep CSS before existing .format-card .prep
src = src.replace(
    ".format-card .prep {",
    ".formats-header { margin-bottom: 20px; }\n  .formats-region-label { font-size: 11px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #5B6175; margin-bottom: 10px; }\n  .format-card .prep.no-prep { color: #F59E0B; }\n  .format-card .prep {",
    1
)

f.write_text(src)
print("ok: 9 format cards with region labels")
