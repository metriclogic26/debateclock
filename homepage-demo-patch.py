#!/usr/bin/env python3
"""
Homepage demo patch — inserts an animated split-view demo widget into index.html.
Shows judge controller (left) + debater display (right) with live ticking clock.

Run from project root:
    python3 homepage-demo-patch.py
"""
import pathlib

f = pathlib.Path("index.html")
src = f.read_text()
orig = src

DEMO_CSS = """
  /* ─── HOMEPAGE DEMO ─────────────────────────────────────── */
  .demo-section {
    max-width: 960px;
    margin: 0 auto 60px;
    padding: 0 24px;
  }
  .demo-section-label {
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted-2, #5B6175);
    margin-bottom: 20px;
  }
  .demo-wrap {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.04), 0 32px 80px rgba(0,0,0,0.6);
    position: relative;
  }
  /* divider line */
  .demo-wrap::after {
    content: '';
    position: absolute;
    top: 0; bottom: 0;
    left: 50%;
    width: 1px;
    background: rgba(255,255,255,0.08);
    pointer-events: none;
    z-index: 2;
  }

  /* ── JUDGE SIDE ── */
  .demo-judge {
    background: #111318;
    padding: 22px 20px 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .demo-panel-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #5B6175;
    margin-bottom: 2px;
  }
  .demo-speech-name {
    font-size: 13px;
    font-weight: 600;
    color: #E8EAF0;
    margin-bottom: 2px;
  }
  .demo-speech-side {
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8B90A0;
  }
  .demo-judge-clock {
    font-family: 'DM Mono', monospace;
    font-size: 48px;
    font-weight: 500;
    letter-spacing: -0.03em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
    color: #22C55E;
    transition: color 0.4s;
  }
  .demo-judge-clock.warn { color: #F59E0B; }
  .demo-judge-clock.critical { color: #EF4444; }

  .demo-progress {
    height: 4px;
    background: #1E232D;
    border-radius: 999px;
    overflow: hidden;
  }
  .demo-progress-fill {
    height: 100%;
    background: #22C55E;
    border-radius: 999px;
    transition: width 1s linear, background 0.4s;
  }
  .demo-progress-fill.warn { background: #F59E0B; }
  .demo-progress-fill.critical { background: #EF4444; }

  .demo-btns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
  }
  .demo-btn {
    background: #181C23;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    color: #E8EAF0;
    padding: 9px 6px;
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    font-weight: 600;
    text-align: center;
    cursor: default;
  }
  .demo-btn.primary {
    background: #F59E0B;
    color: #1a1205;
    border-color: #F59E0B;
  }
  .demo-btn.active-aff {
    background: rgba(59,130,246,0.15);
    border-color: #3B82F6;
    color: #3B82F6;
  }

  /* prep pool */
  .demo-prep-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  .demo-prep-title {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #5B6175;
  }
  .demo-prep-sides {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  .demo-prep-side {
    background: #181C23;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px;
    padding: 10px;
  }
  .demo-prep-side.active-prep {
    border-color: #3B82F6;
    background: rgba(59,130,246,0.08);
  }
  .demo-prep-side-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8B90A0;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .demo-prep-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
  }
  .demo-prep-dot.aff { background: #22C55E; }
  .demo-prep-dot.neg { background: #EF4444; }
  .demo-prep-clock {
    font-family: 'DM Mono', monospace;
    font-size: 18px;
    font-weight: 500;
    color: #E8EAF0;
    font-variant-numeric: tabular-nums;
  }
  .demo-prep-used {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #5B6175;
    margin-top: 2px;
  }
  .demo-prep-bar {
    height: 3px;
    background: #1E232D;
    border-radius: 2px;
    overflow: hidden;
    margin-top: 6px;
  }
  .demo-prep-bar-fill {
    height: 100%;
    background: #3B82F6;
    border-radius: 2px;
    transition: width 1s linear;
  }

  /* ── DEBATER SIDE ── */
  .demo-debater {
    background: #0A0C0F;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 28px 20px;
    position: relative;
    min-height: 320px;
  }
  .demo-debater-label {
    position: absolute;
    top: 14px; left: 14px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #5B6175;
  }
  .demo-debater-speech {
    font-size: 13px;
    font-weight: 600;
    color: #E8EAF0;
    opacity: 0.7;
    text-align: center;
    margin-bottom: 6px;
  }
  .demo-debater-side {
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #22C55E;
    margin-bottom: 20px;
  }
  .demo-debater-side.warn { color: #F59E0B; }
  .demo-debater-side.critical { color: #EF4444; }

  .demo-big-clock {
    font-family: 'DM Mono', monospace;
    font-size: clamp(64px, 12vw, 96px);
    font-weight: 500;
    letter-spacing: -0.04em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
    color: #22C55E;
    transition: color 0.4s;
    text-align: center;
  }
  .demo-big-clock.warn { color: #F59E0B; }
  .demo-big-clock.critical { color: #EF4444; }

  .demo-poi-badge {
    margin-top: 16px;
    padding: 5px 14px;
    background: rgba(245,158,11,0.15);
    border: 1px solid rgba(245,158,11,0.35);
    border-radius: 999px;
    color: #F59E0B;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0;
    transition: opacity 0.4s;
  }
  .demo-poi-badge.visible { opacity: 1; }

  .demo-debater-prep {
    position: absolute;
    bottom: 14px;
    left: 14px; right: 14px;
    display: flex;
    justify-content: center;
    gap: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #5B6175;
  }
  .demo-debater-prep-side { display: flex; align-items: center; gap: 5px; }
  .demo-debater-prep-side.active { color: #3B82F6; }
  .demo-debater-prep-dot {
    width: 5px; height: 5px; border-radius: 50%;
  }
  .demo-debater-prep-dot.aff { background: #22C55E; }
  .demo-debater-prep-dot.neg { background: #EF4444; }
  .demo-debater-prep-side.active .demo-debater-prep-dot {
    background: #3B82F6;
    box-shadow: 0 0 6px #3B82F6;
  }

  .demo-watermark {
    position: absolute;
    bottom: 8px; right: 12px;
    font-size: 9px;
    color: rgba(255,255,255,0.1);
    font-family: 'DM Mono', monospace;
  }

  /* format row below demo */
  .demo-formats {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 14px;
    flex-wrap: wrap;
  }
  .demo-format-tag {
    background: #111318;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 4px 10px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #8B90A0;
    cursor: pointer;
    transition: border-color 0.15s, color 0.15s;
    user-select: none;
  }
  .demo-format-tag:hover,
  .demo-format-tag.active {
    border-color: #3B82F6;
    color: #E8EAF0;
  }

  @media (max-width: 640px) {
    .demo-wrap { grid-template-columns: 1fr; }
    .demo-wrap::after { display: none; }
    .demo-debater { min-height: 220px; }
    .demo-big-clock { font-size: 64px; }
  }
"""

DEMO_HTML = """
  <!-- HOMEPAGE DEMO -->
  <div class="demo-section">
    <div class="demo-section-label">Live demo — see how it works</div>
    <div class="demo-wrap">

      <!-- JUDGE SIDE -->
      <div class="demo-judge">
        <div>
          <div class="demo-panel-label">Judge · Controller</div>
        </div>
        <div>
          <div class="demo-speech-name" id="demoSpeechName">Affirmative Constructive (AC)</div>
          <div class="demo-speech-side" id="demoSpeechSide">Affirmative</div>
        </div>
        <div class="demo-judge-clock" id="demoJudgeClock">6:00</div>
        <div class="demo-progress">
          <div class="demo-progress-fill" id="demoProgressFill" style="width:100%"></div>
        </div>
        <div class="demo-btns">
          <div class="demo-btn" style="opacity:0.4;">◀</div>
          <div class="demo-btn primary" id="demoPauseBtn">⏸ Pause</div>
        </div>

        <div>
          <div class="demo-prep-header">
            <div class="demo-prep-title">Prep Time Pool</div>
          </div>
          <div class="demo-prep-sides">
            <div class="demo-prep-side active-prep" id="demoPrepAff">
              <div class="demo-prep-side-label"><span>AFF</span><span class="demo-prep-dot aff"></span></div>
              <div class="demo-prep-clock" id="demoPrepAffClock">4:00</div>
              <div class="demo-prep-used" id="demoPrepAffUsed">0:00 used</div>
              <div class="demo-prep-bar"><div class="demo-prep-bar-fill" id="demoPrepAffBar" style="width:100%"></div></div>
            </div>
            <div class="demo-prep-side" id="demoPrepNeg">
              <div class="demo-prep-side-label"><span>NEG</span><span class="demo-prep-dot neg"></span></div>
              <div class="demo-prep-clock" id="demoPrepNegClock">4:00</div>
              <div class="demo-prep-used" id="demoPrepNegUsed">0:00 used</div>
              <div class="demo-prep-bar"><div class="demo-prep-bar-fill" id="demoPrepNegBar" style="width:100%"></div></div>
            </div>
          </div>
        </div>
      </div>

      <!-- DEBATER SIDE -->
      <div class="demo-debater">
        <div class="demo-debater-label">Debater · Display</div>
        <div class="demo-debater-speech" id="demoDebaterSpeech">Affirmative Constructive (AC)</div>
        <div class="demo-debater-side" id="demoDebaterSide">AFFIRMATIVE</div>
        <div class="demo-big-clock" id="demoBigClock">6:00</div>
        <div class="demo-poi-badge" id="demoPoiBadge">POI Window</div>
        <div class="demo-debater-prep">
          <div class="demo-debater-prep-side aff" id="demoDebaterPrepAff">
            <span class="demo-debater-prep-dot aff"></span>
            AFF prep <span id="demoDebaterAffTime">4:00</span>
          </div>
          <div class="demo-debater-prep-side neg" id="demoDebaterPrepNeg">
            <span class="demo-debater-prep-dot neg"></span>
            NEG prep <span id="demoDebaterNegTime">4:00</span>
          </div>
        </div>
        <div class="demo-watermark">debateclock.org</div>
      </div>

    </div>

    <!-- Format selector -->
    <div class="demo-formats">
      <div class="demo-format-tag active" data-format="LD" onclick="demoSetFormat(this)">LD</div>
      <div class="demo-format-tag" data-format="Policy" onclick="demoSetFormat(this)">Policy</div>
      <div class="demo-format-tag" data-format="PF" onclick="demoSetFormat(this)">PF</div>
      <div class="demo-format-tag" data-format="WSDC" onclick="demoSetFormat(this)">WSDC</div>
      <div class="demo-format-tag" data-format="BP" onclick="demoSetFormat(this)">BP</div>
    </div>
  </div>

  <script>
  (function() {
    // ── Demo state ──────────────────────────────────────────────
    var FORMATS = {
      LD:     { speech: 'Affirmative Constructive (AC)', side: 'AFFIRMATIVE', duration: 360, prep: 240, hasPOI: false },
      Policy: { speech: '1st Aff Constructive (1AC)',   side: 'AFFIRMATIVE', duration: 480, prep: 480, hasPOI: false },
      PF:     { speech: '1st Speaker — Team A (Pro)',   side: 'TEAM A',      duration: 240, prep: 180, hasPOI: false },
      WSDC:   { speech: '1st Proposition',              side: 'PROPOSITION', duration: 480, prep: 0,   hasPOI: true,  poiStart: 60, poiEnd: 420 },
      BP:     { speech: 'Prime Minister (OG)',          side: 'OPENING GOV', duration: 420, prep: 0,   hasPOI: true,  poiStart: 60, poiEnd: 360 },
    };

    var currentFmt = 'LD';
    var startedAt = Date.now();
    var prepAffUsed = 0;
    var prepAffStartedAt = null;
    var animFrame;

    function fmt(ms) {
      ms = Math.max(0, ms);
      var s = Math.floor(ms / 1000);
      return Math.floor(s/60) + ':' + ('0' + (s%60)).slice(-2);
    }

    function tick() {
      var f = FORMATS[currentFmt];
      var elapsed = (Date.now() - startedAt) / 1000;
      var remaining = Math.max(0, f.duration - elapsed);
      var pct = remaining / f.duration * 100;

      // phase
      var phase = remaining > 60 ? 'go' : remaining > 30 ? 'warn' : 'critical';
      if (remaining === 0) phase = 'critical';

      // speech clock
      var clockStr = fmt(remaining * 1000);
      document.getElementById('demoJudgeClock').textContent = clockStr;
      document.getElementById('demoBigClock').textContent = clockStr;
      document.getElementById('demoJudgeClock').className = 'demo-judge-clock' + (phase !== 'go' ? ' ' + phase : '');
      document.getElementById('demoBigClock').className = 'demo-big-clock' + (phase !== 'go' ? ' ' + phase : '');
      document.getElementById('demoDebaterSide').className = 'demo-debater-side' + (phase !== 'go' ? ' ' + phase : '');

      // progress bar
      document.getElementById('demoProgressFill').style.width = pct + '%';
      document.getElementById('demoProgressFill').className = 'demo-progress-fill' + (phase !== 'go' ? ' ' + phase : '');

      // POI badge
      var poiVisible = false;
      if (f.hasPOI) {
        poiVisible = elapsed >= f.poiStart && elapsed <= f.poiEnd;
      }
      document.getElementById('demoPoiBadge').className = 'demo-poi-badge' + (poiVisible ? ' visible' : '');

      // prep pool — aff ticks for first 30s of demo, then stops; neg untouched
      var prepAffUsedMs = prepAffStartedAt ? prepAffUsed + (Date.now() - prepAffStartedAt) : prepAffUsed;
      prepAffUsedMs = Math.min(prepAffUsedMs, f.prep * 1000);
      var prepAffRem = Math.max(0, f.prep * 1000 - prepAffUsedMs);
      var affPct = f.prep > 0 ? prepAffRem / (f.prep * 1000) * 100 : 0;

      if (f.prep > 0) {
        document.getElementById('demoPrepAffClock').textContent = fmt(prepAffRem);
        document.getElementById('demoPrepAffUsed').textContent = fmt(prepAffUsedMs) + ' used';
        document.getElementById('demoPrepAffBar').style.width = affPct + '%';
        document.getElementById('demoPrepNegClock').textContent = fmt(f.prep * 1000);
        document.getElementById('demoPrepNegUsed').textContent = '0:00 used';
        document.getElementById('demoPrepNegBar').style.width = '100%';
        document.getElementById('demoDebaterAffTime').textContent = fmt(prepAffRem);
        document.getElementById('demoDebaterNegTime').textContent = fmt(f.prep * 1000);
        document.getElementById('demoPrepAff').style.display = '';
        document.getElementById('demoPrepNeg').style.display = '';
        document.getElementById('demoDebaterPrepAff').parentElement.style.display = '';
      } else {
        document.getElementById('demoPrepAff').style.display = 'none';
        document.getElementById('demoPrepNeg').style.display = 'none';
      }

      // loop after 75% of speech is done
      if (elapsed > f.duration * 0.75) {
        startedAt = Date.now();
        prepAffUsed = 0;
        prepAffStartedAt = f.prep > 0 ? Date.now() : null;
      }

      animFrame = requestAnimationFrame(tick);
    }

    window.demoSetFormat = function(el) {
      document.querySelectorAll('.demo-format-tag').forEach(function(t) { t.classList.remove('active'); });
      el.classList.add('active');
      currentFmt = el.dataset.format;
      var f = FORMATS[currentFmt];
      startedAt = Date.now();
      prepAffUsed = 0;
      prepAffStartedAt = f.prep > 0 ? Date.now() : null;
      document.getElementById('demoSpeechName').textContent = f.speech;
      document.getElementById('demoSpeechSide').textContent = f.side.charAt(0) + f.side.slice(1).toLowerCase();
      document.getElementById('demoDebaterSpeech').textContent = f.speech;
    };

    // Start demo — aff prep counts for LD
    prepAffStartedAt = Date.now();
    tick();
  })();
  </script>
"""

# Find the right insertion point — after hero section, before formats/features
# Look for the formats section or the gap section
INSERT_AFTER = [
    '<div class="formats"',
    '<section class="formats"',
    '<div class="gap"',
    '<section class="gap"',
    '<!-- features -->',
    '<!-- formats -->',
]

inserted = False
for anchor in INSERT_AFTER:
    if anchor in src:
        src = src.replace(anchor, DEMO_HTML + '\n  ' + anchor, 1)
        inserted = True
        print(f"ok: demo inserted before {anchor!r}")
        break

if not inserted:
    # Fallback — insert after closing </section> of hero or before </main>
    if '</main>' in src:
        src = src.replace('</main>', DEMO_HTML + '\n</main>', 1)
        inserted = True
        print("ok: demo inserted before </main>")
    elif '<footer' in src:
        src = src.replace('<footer', DEMO_HTML + '\n<footer', 1)
        inserted = True
        print("ok: demo inserted before <footer")

if not inserted:
    print("miss: could not find insertion point — check index.html structure manually")

# Insert CSS into <style> block
if 'demo-section' not in src and '/* ─── HOMEPAGE DEMO' not in src:
    if '</style>' in src:
        src = src.replace('</style>', DEMO_CSS + '\n</style>', 1)
        print("ok: demo CSS inserted")
    else:
        print("miss: no </style> found")
else:
    print("skip: demo CSS already present")

if src != orig:
    f.write_text(src)
    print("written.")
else:
    print("no changes — check misses above")
