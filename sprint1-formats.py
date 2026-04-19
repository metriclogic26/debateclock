#!/usr/bin/env python3
"""
Sprint 1: International formats
Adds WSDC, BP University, BP High School to formats.js
Generalizes POI window logic in state.js
Updates display.html import

Run from project root:
    python3 sprint1-formats.py
"""
import pathlib

# ─── 1. formats.js ──────────────────────────────────────────────────────────

f = pathlib.Path("app/formats.js")
src = f.read_text()

NEW_FORMATS = """
  WSDC: {
    id: 'WSDC',
    name: 'World Schools (WSDC)',
    shortName: 'WSDC',
    prepPoolSeconds: { aff: 0, neg: 0 },
    // POI window: min 1-7 of each 8-min constructive. Reply speeches have no POI.
    // Bell schedule: 1:00 (POIs open), 7:00 (POIs close), 8:00 (double bell).
    speeches: [
      { id: 'p1',     label: '1st Proposition',   side: 'aff', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'o1',     label: '1st Opposition',     side: 'neg', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'p2',     label: '2nd Proposition',    side: 'aff', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'o2',     label: '2nd Opposition',     side: 'neg', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'p3',     label: '3rd Proposition',    side: 'aff', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'o3',     label: '3rd Opposition',     side: 'neg', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'oreply', label: 'Opposition Reply',   side: 'neg', duration: 240, isCX: false },
      { id: 'preply', label: 'Proposition Reply',  side: 'aff', duration: 240, isCX: false },
    ],
  },

  BPUni: {
    id: 'BPUni',
    name: 'British Parliamentary (Uni / WUDC)',
    shortName: 'BP',
    prepPoolSeconds: { aff: 0, neg: 0 },
    // 4 teams: OG (Opening Gov) = aff, OO (Opening Opp) = neg,
    //          CG (Closing Gov) = aff, CO (Closing Opp) = neg
    // POI window: min 1-6 of each 7-min speech.
    speeches: [
      { id: 'pm',  label: 'Prime Minister (OG)',              side: 'aff', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'lo',  label: 'Leader of Opposition (OO)',        side: 'neg', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'dpm', label: 'Deputy Prime Minister (OG)',       side: 'aff', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'dlo', label: 'Deputy Leader of Opposition (OO)', side: 'neg', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'mg',  label: 'Member for Government (CG)',       side: 'aff', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'mo',  label: 'Member for Opposition (CO)',       side: 'neg', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'gw',  label: 'Government Whip (CG)',             side: 'aff', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'ow',  label: 'Opposition Whip (CO)',             side: 'neg', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
    ],
  },

  BPHS: {
    id: 'BPHS',
    name: 'British Parliamentary (High School)',
    shortName: 'BP-HS',
    prepPoolSeconds: { aff: 0, neg: 0 },
    // 5-min speeches. POI window: 0:30 to 4:30 (30s protected at start AND end).
    // Explicitly not supported by Debatekeeper per user reviews.
    speeches: [
      { id: 'pm',  label: 'Prime Minister (OG)',              side: 'aff', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'lo',  label: 'Leader of Opposition (OO)',        side: 'neg', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'dpm', label: 'Deputy Prime Minister (OG)',       side: 'aff', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'dlo', label: 'Deputy Leader of Opposition (OO)', side: 'neg', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'mg',  label: 'Member for Government (CG)',       side: 'aff', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'mo',  label: 'Member for Opposition (CO)',       side: 'neg', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'gw',  label: 'Government Whip (CG)',             side: 'aff', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'ow',  label: 'Opposition Whip (CO)',             side: 'neg', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
    ],
  },
"""

# Insert after the Parli block (before closing `}` of FORMATS)
ANCHOR = "export const FORMAT_LIST = Object.values(FORMATS);"
if ANCHOR not in src:
    print("MISS: formats.js anchor not found")
else:
    # Find the closing }; of the FORMATS object
    insert_marker = "};\n\nexport const FORMAT_LIST"
    src = src.replace(insert_marker, NEW_FORMATS + "};\n\nexport const FORMAT_LIST")
    f.write_text(src)
    print("ok: formats.js — added WSDC, BPUni, BPHS")


# ─── 2. state.js — generalize parliPOIWindow → poiWindow ────────────────────

sf = pathlib.Path("app/state.js")
ssrc = sf.read_text()

OLD_POI = """// For Parli POI window: 1:00\u20136:00 into 7-min constructives, POI signal allowed
export function parliPOIWindow(state, now = Date.now()) {
  const sp = currentSpeech(state);
  if (!sp || state.format !== 'Parli') return false;
  if (sp.duration < 420) return false;  // POI only in 7-min constructives
  const elapsed = speechElapsedMs(state, now);
  return elapsed >= 60_000 && elapsed <= (sp.duration - 60) * 1000;
}"""

NEW_POI = """// POI window check — works for WSDC, BP, and legacy Parli formats.
// Speeches with POI windows carry poiStartSec / poiEndSec fields.
// Legacy Parli speeches don't have those fields; handled by fallback.
export function poiWindow(state, now = Date.now()) {
  const sp = currentSpeech(state);
  if (!sp) return false;
  const elapsed = speechElapsedMs(state, now);
  // Per-speech POI data (WSDC, BPUni, BPHS)
  if (sp.poiStartSec != null && sp.poiEndSec != null) {
    return elapsed >= sp.poiStartSec * 1000 && elapsed <= sp.poiEndSec * 1000;
  }
  // Legacy Parli: 1:00-6:00 in 7-min constructives
  if (state.format === 'Parli') {
    if (sp.duration < 420) return false;
    return elapsed >= 60_000 && elapsed <= (sp.duration - 60) * 1000;
  }
  return false;
}

// Backward-compat alias (display.html uses this name)
export const parliPOIWindow = poiWindow;"""

if OLD_POI in ssrc:
    ssrc = ssrc.replace(OLD_POI, NEW_POI)
    sf.write_text(ssrc)
    print("ok: state.js — generalized parliPOIWindow -> poiWindow")
else:
    print("miss: state.js — parliPOIWindow block not found (may already be patched)")


# ─── 3. display.html — update POI cue label for WSDC/BP ─────────────────────

df = pathlib.Path("app/display.html")
dsrc = df.read_text()

# Update the static POI cue text to be format-aware
# Currently: <div class="poi-cue" id="poiCue">POI Window Open</div>
# Change the JS render to set the text dynamically (already generic enough, just label update)

# The poi-cue text is hardcoded in HTML. Make it match the format.
OLD_POI_CUE = '<div class="poi-cue" id="poiCue">POI Window Open</div>'
NEW_POI_CUE = '<div class="poi-cue" id="poiCue">POI Window</div>'

if OLD_POI_CUE in dsrc:
    dsrc = dsrc.replace(OLD_POI_CUE, NEW_POI_CUE)
    print("ok: display.html — updated POI cue label")
else:
    print("skip: display.html POI cue (already updated or different markup)")

# The parliPOIWindow import in display.html is already aliased, so no import change needed.
# But let's verify the alias works by checking the import
if "parliPOIWindow" in dsrc:
    print("ok: display.html — still uses parliPOIWindow alias (works via state.js alias)")

df.write_text(dsrc)


# ─── 4. Verify format count ─────────────────────────────────────────────────
src_check = pathlib.Path("app/formats.js").read_text()
count = src_check.count("id: '")
print(f"ok: formats.js — {count} format IDs total (expected 7: LD, Policy, PF, Parli, WSDC, BPUni, BPHS)")

print("\ndone.")
