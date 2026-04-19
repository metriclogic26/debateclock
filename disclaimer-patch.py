#!/usr/bin/env python3
"""
Disclaimer patch — adds legal footer to app pages and site.css disclaimer bar.

Run from project root:
    python3 disclaimer-patch.py
"""
import pathlib

# ─── 1. app/index.html — replace footer-note with disclaimer ─────────────────

f = pathlib.Path("app/index.html")
src = f.read_text()

OLD_FOOTER = '      <div class="footer-note">no signup · nothing stored · rooms are ephemeral</div>'
NEW_FOOTER = '''      <div class="footer-note">
        no signup · nothing stored · rooms are ephemeral<br>
        <span style="font-size:10px;">Informational timing aid only. Not affiliated with NSDA, WUDC, WSDC, CUSID, or Tabroom. Always defer to the tournament director for timing disputes. <a href="/terms/" style="color:var(--muted);text-decoration:underline;">Terms &amp; Privacy</a></span>
      </div>'''

if OLD_FOOTER in src:
    src = src.replace(OLD_FOOTER, NEW_FOOTER)
    f.write_text(src)
    print("ok: app/index.html disclaimer added")
else:
    print("miss: app/index.html footer-note not found — check manually")


# ─── 2. app/display.html — add disclaimer to watermark ───────────────────────

df = pathlib.Path("app/display.html")
dsrc = df.read_text()

OLD_WATERMARK = '  <div class="watermark">debateclock.org</div>'
NEW_WATERMARK = '  <div class="watermark">debateclock.org · informational timing aid only</div>'

if OLD_WATERMARK in dsrc:
    dsrc = dsrc.replace(OLD_WATERMARK, NEW_WATERMARK)
    df.write_text(dsrc)
    print("ok: app/display.html watermark updated")
else:
    print("miss: display.html watermark not found")


# ─── 3. assets/site.css — add disclaimer bar style ───────────────────────────

cf = pathlib.Path("assets/site.css")
if cf.exists():
    csrc = cf.read_text()
    if '.site-disclaimer' not in csrc:
        csrc += """
/* ── DISCLAIMER BAR ─────────────────────────────────────── */
.site-disclaimer {
  background: var(--bg2, #111318);
  border-top: 1px solid var(--border, rgba(255,255,255,0.07));
  padding: 12px 20px;
  text-align: center;
  font-size: 11px;
  color: var(--muted-2, #5B6175);
  line-height: 1.6;
  font-family: 'DM Mono', monospace;
}
.site-disclaimer a { color: var(--muted, #8B90A0); }
.site-disclaimer a:hover { color: var(--text, #E8EAF0); }
"""
        cf.write_text(csrc)
        print("ok: assets/site.css disclaimer bar style added")
    else:
        print("skip: disclaimer style already in site.css")
else:
    print("skip: assets/site.css not found")


# ─── 4. Add disclaimer bar to all SEO pages ──────────────────────────────────

DISCLAIMER_HTML = '''
<div class="site-disclaimer">
  Informational timing aid only &middot; Not affiliated with NSDA, WUDC, WSDC, CUSID, or Tabroom &middot; Always defer to the tournament director for timing disputes &middot; <a href="/terms/">Terms &amp; Privacy</a>
</div>
'''

seo_pages = list(pathlib.Path("timer").rglob("index.html")) + \
            list(pathlib.Path("blog").rglob("index.html")) + \
            list(pathlib.Path("alternative").rglob("index.html")) + \
            list(pathlib.Path("setup").rglob("index.html"))

patched = 0
for page in seo_pages:
    psrc = page.read_text()
    if 'site-disclaimer' not in psrc and '</footer>' in psrc:
        psrc = psrc.replace('</footer>', DISCLAIMER_HTML + '</footer>')
        page.write_text(psrc)
        patched += 1

print(f"ok: {patched} SEO pages — disclaimer bar added above footer closing tag")


# ─── 5. Update sitemap to include /terms/ ────────────────────────────────────

sm = pathlib.Path("sitemap.xml")
smtxt = sm.read_text()
if '/terms/' not in smtxt:
    smtxt = smtxt.replace('</urlset>',
        '  <url><loc>https://debateclock.org/terms/</loc><lastmod>2026-04-19</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>\n</urlset>')
    sm.write_text(smtxt)
    print("ok: sitemap.xml — /terms/ added,", smtxt.count("<url>"), "total URLs")
else:
    print("skip: /terms/ already in sitemap")

print("\ndone.")
