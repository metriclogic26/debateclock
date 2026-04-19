#!/usr/bin/env python3
"""
Sprint 2: App UX polish
1. Prep display shows "used | remaining" on judge controller
2. Quick-set prep buttons [3m][5m][8m][10m]
3. Deliberation timer (post-round 5-min countdown + RFD stopwatch)

Run from project root:
    python3 sprint2-ux.py
"""
import pathlib

f = pathlib.Path("app/index.html")
src = f.read_text()
orig = src

# ─── 1. CSS — add styles ─────────────────────────────────────────────────────

CSS_NEW = """
  /* -- PREP USED LINE -- */
  .prep-side-used {
    font-family: 'DM Mono', monospace;
    font-size: 11px; color: var(--muted-2);
    font-variant-numeric: tabular-nums;
    min-height: 14px;
  }
  .prep-side.active .prep-side-used { color: var(--muted); }

  /* -- QUICK-SET PREP BUTTONS -- */
  .prep-quick-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
    margin-bottom: 12px;
  }
  .prep-quick-btn {
    background: var(--bg3);
    border: 1px solid var(--border);
    color: var(--muted);
    border-radius: 6px;
    padding: 5px 2px;
    font-family: 'DM Mono', monospace;
    font-size: 11px; font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
  }
  .prep-quick-btn:hover:not(:disabled) { border-color: var(--border-strong); color: var(--text); }
  .prep-quick-btn:disabled { opacity: 0.3; cursor: not-allowed; }

  /* -- DELIBERATION TIMER -- */
  .delib-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 18px;
  }
  .delib-card h3 {
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--muted-2);
    margin-bottom: 12px;
  }
  .delib-controls {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
    margin-bottom: 10px;
  }
  .delib-clock {
    font-family: 'DM Mono', monospace;
    font-size: 28px; font-weight: 500;
    color: var(--text);
    font-variant-numeric: tabular-nums;
    text-align: center;
    min-height: 36px;
    letter-spacing: -0.02em;
  }
  .delib-clock.running { color: var(--accent); }
  .delib-clock.done    { color: var(--muted); }
"""

CSS_ANCHOR = "  .footer-note {"
if CSS_ANCHOR in src:
    src = src.replace(CSS_ANCHOR, CSS_NEW + "  .footer-note {")
    print("ok: CSS added (used line, quick buttons, delib card)")
else:
    print("miss: CSS anchor .footer-note not found")


# ─── 2. HTML — add "used" line to AFF prep side ──────────────────────────────

OLD_AFF_CLOCK = '<div class="prep-side-clock mono" id="prepAffClock">0:00</div>\n            <div class="prep-side-bar">'
NEW_AFF_CLOCK = '<div class="prep-side-clock mono" id="prepAffClock">0:00</div>\n            <div class="prep-side-used" id="prepAffUsed"></div>\n            <div class="prep-side-bar">'

if OLD_AFF_CLOCK in src:
    src = src.replace(OLD_AFF_CLOCK, NEW_AFF_CLOCK)
    print("ok: AFF prep used element added")
else:
    print("miss: AFF prep clock anchor")


# ─── 3. HTML — add "used" line to NEG prep side ──────────────────────────────

OLD_NEG_CLOCK = '<div class="prep-side-clock mono" id="prepNegClock">0:00</div>\n            <div class="prep-side-bar">'
NEW_NEG_CLOCK = '<div class="prep-side-clock mono" id="prepNegClock">0:00</div>\n            <div class="prep-side-used" id="prepNegUsed"></div>\n            <div class="prep-side-bar">'

if OLD_NEG_CLOCK in src:
    src = src.replace(OLD_NEG_CLOCK, NEW_NEG_CLOCK)
    print("ok: NEG prep used element added")
else:
    print("miss: NEG prep clock anchor")


# ─── 4. HTML — quick-set buttons after prep card h3 ──────────────────────────

OLD_PREP_H3 = """          <h3>
          Prep Time Pool
          <button class="prep-reset" id="prepResetBtn">reset</button>
        </h3>
        <div class="prep-sides">"""

NEW_PREP_H3 = """          <h3>
          Prep Time Pool
          <button class="prep-reset" id="prepResetBtn">reset</button>
        </h3>
        <div class="prep-quick-row" id="prepQuickRow">
          <button class="prep-quick-btn" data-mins="3">3m</button>
          <button class="prep-quick-btn" data-mins="5">5m</button>
          <button class="prep-quick-btn" data-mins="8">8m</button>
          <button class="prep-quick-btn" data-mins="10">10m</button>
        </div>
        <div class="prep-sides">"""

if OLD_PREP_H3 in src:
    src = src.replace(OLD_PREP_H3, NEW_PREP_H3)
    print("ok: quick-set buttons added to prep card")
else:
    print("miss: prep card h3 anchor")


# ─── 5. HTML — deliberation card after QR card ───────────────────────────────

OLD_FOOTER_NOTE = '      <div class="footer-note">no signup \u00b7 nothing stored \u00b7 rooms are ephemeral</div>'
NEW_FOOTER_NOTE = """      <div class="delib-card" id="deliberationCard">
        <h3>Post-Round</h3>
        <div class="delib-controls">
          <button class="ctrl-btn" id="deliberationBtn">\u23f1 Deliberation</button>
          <button class="ctrl-btn" id="rfdBtn">\u23f1 RFD</button>
        </div>
        <div class="delib-clock" id="deliberationClock"></div>
      </div>

      <div class="footer-note">no signup \u00b7 nothing stored \u00b7 rooms are ephemeral</div>"""

if OLD_FOOTER_NOTE in src:
    src = src.replace(OLD_FOOTER_NOTE, NEW_FOOTER_NOTE)
    print("ok: deliberation card added")
else:
    print("miss: footer-note anchor for delib card")


# ─── 6. JS — update prep render to show used/remaining ───────────────────────

OLD_PREP_RENDER = """    clock.textContent = formatClock(rem, false);
    const p = tot > 0 ? Math.max(0, Math.min(100, (rem / tot) * 100)) : 0;
    bar.style.width = p + '%';"""

NEW_PREP_RENDER = """    clock.textContent = formatClock(rem, false);
    const usedEl = document.getElementById(side === 'aff' ? 'prepAffUsed' : 'prepNegUsed');
    if (usedEl) {
      if (tot > 0) {
        const usedMs = tot - rem;
        usedEl.textContent = formatClock(usedMs, false) + ' used';
      } else {
        usedEl.textContent = '';
      }
    }
    const p = tot > 0 ? Math.max(0, Math.min(100, (rem / tot) * 100)) : 0;
    bar.style.width = p + '%';"""

if OLD_PREP_RENDER in src:
    src = src.replace(OLD_PREP_RENDER, NEW_PREP_RENDER)
    print("ok: prep render updated with used display")
else:
    print("miss: prep render anchor")


# ─── 7. JS — quick-set buttons handler + deliberation timer ──────────────────

OLD_PREP_RESET_HANDLER = """document.getElementById('prepResetBtn').addEventListener('click', () => {
  if (confirm('Reset prep pool for both sides?')) act(resetPrep);
});"""

NEW_PREP_RESET_HANDLER = """document.getElementById('prepResetBtn').addEventListener('click', () => {
  if (confirm('Reset prep pool for both sides?')) act(resetPrep);
});

// Quick-set prep buttons
document.getElementById('prepQuickRow').addEventListener('click', (e) => {
  const btn = e.target.closest('[data-mins]');
  if (!btn) return;
  const mins = parseInt(btn.dataset.mins, 10);
  const ms = mins * 60 * 1000;
  if (!confirm('Set prep pool to ' + mins + ' min per side and reset usage?')) return;
  state = {
    ...state,
    prepPoolTotalMs: { aff: ms, neg: ms },
    prepConsumedMs: { aff: 0, neg: 0 },
    activePrepSide: null,
    prepStartedAt: null,
  };
  broadcast(); render();
});

// Deliberation timer (local only, not synced to display)
let delib = { mode: null, running: false, startedAt: null, elapsed: 0 };
const DELIB_DURATION = 5 * 60 * 1000; // 5 minutes

function deliberationElapsed() {
  if (!delib.running || !delib.startedAt) return delib.elapsed;
  return delib.elapsed + (Date.now() - delib.startedAt);
}

function renderDelib() {
  const clockEl = document.getElementById('deliberationClock');
  const dBtn = document.getElementById('deliberationBtn');
  const rBtn = document.getElementById('rfdBtn');
  if (!clockEl) return;

  if (!delib.mode) {
    clockEl.textContent = '';
    clockEl.className = 'delib-clock';
    dBtn.textContent = '\u23f1 Deliberation';
    rBtn.textContent = '\u23f1 RFD';
    return;
  }

  const elapsed = deliberationElapsed();

  if (delib.mode === 'delib') {
    const rem = Math.max(0, DELIB_DURATION - elapsed);
    clockEl.textContent = formatClock(rem, false);
    clockEl.className = 'delib-clock' + (rem === 0 ? ' done' : delib.running ? ' running' : '');
    dBtn.textContent = delib.running ? '\u23f8 Pause' : (rem === 0 ? '\u21ba Restart' : '\u25b6 Resume');
    rBtn.textContent = '\u23f1 RFD';
    if (rem === 0 && delib.running) {
      delib.running = false;
      delib.elapsed = DELIB_DURATION;
      delib.startedAt = null;
    }
  } else {
    clockEl.textContent = formatClock(elapsed, false);
    clockEl.className = 'delib-clock' + (delib.running ? ' running' : '');
    rBtn.textContent = delib.running ? '\u23f8 Pause' : '\u25b6 Resume';
    dBtn.textContent = '\u23f1 Deliberation';
  }
}

document.getElementById('deliberationBtn').addEventListener('click', () => {
  if (delib.mode === 'delib') {
    if (delib.running) {
      delib.elapsed = deliberationElapsed();
      delib.running = false;
      delib.startedAt = null;
    } else if (delib.elapsed >= DELIB_DURATION) {
      delib = { mode: 'delib', running: true, startedAt: Date.now(), elapsed: 0 };
    } else {
      delib.running = true;
      delib.startedAt = Date.now();
    }
  } else {
    delib = { mode: 'delib', running: true, startedAt: Date.now(), elapsed: 0 };
  }
  renderDelib();
});

document.getElementById('rfdBtn').addEventListener('click', () => {
  if (delib.mode === 'rfd') {
    if (delib.running) {
      delib.elapsed = deliberationElapsed();
      delib.running = false;
      delib.startedAt = null;
    } else {
      delib.running = true;
      delib.startedAt = Date.now();
    }
  } else {
    delib = { mode: 'rfd', running: true, startedAt: Date.now(), elapsed: 0 };
  }
  renderDelib();
});"""

if OLD_PREP_RESET_HANDLER in src:
    src = src.replace(OLD_PREP_RESET_HANDLER, NEW_PREP_RESET_HANDLER)
    print("ok: quick-set + deliberation timer JS added")
else:
    print("miss: prepResetBtn handler anchor")


# ─── 8. JS — hook renderDelib into RAF tick ──────────────────────────────────

OLD_TICK = """function tick(t) {
  if (t - lastRenderTime > 100) {
    lastRenderTime = t;
    render();
  }
  requestAnimationFrame(tick);
}"""

NEW_TICK = """function tick(t) {
  if (t - lastRenderTime > 100) {
    lastRenderTime = t;
    render();
    renderDelib();
  }
  requestAnimationFrame(tick);
}"""

if OLD_TICK in src:
    src = src.replace(OLD_TICK, NEW_TICK)
    print("ok: renderDelib hooked into RAF tick")
else:
    print("miss: tick function anchor")


# ─── 9. JS — disable quick-set buttons when no prep format ───────────────────

OLD_QUICK_ROW_RENDER = "  document.getElementById('vanishBtn').classList.toggle('active', state.vanishAtZero);"
NEW_QUICK_ROW_RENDER = """  // Disable quick-set buttons for no-prep formats
  const hasAnyPrep = state.prepPoolTotalMs.aff > 0 || state.prepPoolTotalMs.neg > 0 ||
    (FORMATS[state.format] && FORMATS[state.format].prepPoolSeconds.aff > 0);
  document.querySelectorAll('.prep-quick-btn').forEach(b => b.disabled = false);

  document.getElementById('vanishBtn').classList.toggle('active', state.vanishAtZero);"""

if OLD_QUICK_ROW_RENDER in src:
    src = src.replace(OLD_QUICK_ROW_RENDER, NEW_QUICK_ROW_RENDER)
    print("ok: quick-set button state wired into render")
else:
    print("miss: vanishBtn render anchor")


# ─── Write ───────────────────────────────────────────────────────────────────

if src != orig:
    f.write_text(src)
    print("\nok: app/index.html written")
else:
    print("\nWARN: no changes made — check misses above")

print("done.")
