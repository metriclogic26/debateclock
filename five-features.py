#!/usr/bin/env python3
"""
5 patches:
1. Tournament schedule — CSV import
2. App — Download QR as PNG
3. Debater display — heartbeat sync indicator
4. App + Display — stop at 00:00 toggle
5. Debater display — bigger speech label

Run from project root: python3 five-features.py
"""
import pathlib, re

# ══════════════════════════════════════════════════════════════════════════════
# 1. TOURNAMENT SCHEDULE — CSV IMPORT
# ══════════════════════════════════════════════════════════════════════════════
f = pathlib.Path("practice/tournament/index.html")
src = f.read_text()

CSV_BTN_CSS = """
  .csv-row { margin-top: 12px; display: flex; align-items: center; gap: 10px; }
  .csv-label { font-size: 12px; color: #5B6175; }
  .csv-btn { background: #0A0C0F; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 8px 14px; font-family: 'DM Sans', sans-serif; font-size: 12px; color: #8B90A0; cursor: pointer; transition: all .15s; }
  .csv-btn:hover { border-color: rgba(255,255,255,0.25); color: #E8EAF0; }
  #csvFileInput { display: none; }
"""

src = src.replace("  .add-card {", CSV_BTN_CSS + "\n  .add-card {")

CSV_HTML = """
    <!-- CSV Import -->
    <div class="csv-row">
      <span class="csv-label">Import from spreadsheet:</span>
      <button class="csv-btn" onclick="document.getElementById('csvFileInput').click()">&#8679; Import CSV</button>
      <input type="file" id="csvFileInput" accept=".csv" onchange="importCSV(this)">
      <a class="csv-btn" href="/practice/tournament/sample.csv" download style="text-decoration:none;">&#8681; Sample CSV</a>
    </div>"""

src = src.replace("    <!-- ROUND LIST -->", CSV_HTML + "\n\n  <!-- ROUND LIST -->")

CSV_JS = """
function importCSV(input) {
  var file = input.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function(e) {
    var lines = e.target.result.split(/\\r?\\n/).filter(function(l){ return l.trim(); });
    var added = 0;
    lines.forEach(function(line, idx) {
      if (idx === 0 && line.toLowerCase().includes('name')) return; // skip header
      var parts = line.split(',');
      if (parts.length < 2) return;
      var name = parts[0].trim().replace(/^"|"$/g,'');
      var timeStr = parts[1].trim().replace(/^"|"$/g,'');
      // parse time: "8:00 AM", "14:30", "2:30 PM"
      var m = timeStr.match(/(\\d+):(\\d+)\\s*(AM|PM)?/i);
      if (!m) return;
      var h = parseInt(m[1]);
      var min = parseInt(m[2]);
      var ampm = (m[3]||'').toUpperCase();
      if (ampm === 'PM' && h < 12) h += 12;
      if (ampm === 'AM' && h === 12) h = 0;
      var ms = (h * 3600 + min * 60) * 1000;
      rounds.push({ id: Date.now() + Math.random(), name: name || 'Round', timeMs: ms });
      added++;
    });
    rounds.sort(function(a,b){ return a.timeMs - b.timeMs; });
    save();
    renderList();
    updateCountdowns();
    alert('Imported ' + added + ' round' + (added===1?'':'s') + '.');
  };
  reader.readAsText(file);
  input.value = '';
}"""

src = src.replace("function addRound()", CSV_JS + "\n\nfunction addRound()")
f.write_text(src)
print("ok: 1. CSV import added to tournament schedule")

# Write sample CSV
sample = pathlib.Path("practice/tournament/sample.csv")
sample.write_text("Name,Time\nRound 1,8:00 AM\nRound 2,10:00 AM\nLunch,12:00 PM\nRound 3,1:30 PM\nRound 4,3:30 PM\nAwards,5:00 PM\n")
print("ok: 1. sample.csv written")

# ══════════════════════════════════════════════════════════════════════════════
# 2. APP — DOWNLOAD QR AS PNG
# ══════════════════════════════════════════════════════════════════════════════
f = pathlib.Path("app/index.html")
src = f.read_text()

# Add download button next to QR
src = src.replace(
    '<div class="qr-canvas" id="qrCanvas"></div>',
    '<div class="qr-canvas" id="qrCanvas" title="Click to download QR code" onclick="downloadQR()" style="cursor:pointer;" title="Click to download"></div>\n        <div style="font-size:10px;color:#5B6175;text-align:center;margin-top:4px;cursor:pointer;" onclick="downloadQR()">&#8681; Download QR</div>'
)

QR_DOWNLOAD_JS = """
function downloadQR() {
  var img = document.querySelector('#qrCanvas img');
  if (!img) return;
  var a = document.createElement('a');
  a.href = img.src;
  a.download = 'debateclock-room-' + (currentRoom || 'qr') + '.png';
  a.click();
}"""

src = src.replace("let isEchoing = false;", "let isEchoing = false;\n" + QR_DOWNLOAD_JS)
f.write_text(src)
print("ok: 2. QR download added to app")

# ══════════════════════════════════════════════════════════════════════════════
# 3. DEBATER DISPLAY — HEARTBEAT SYNC INDICATOR
# ══════════════════════════════════════════════════════════════════════════════
f = pathlib.Path("app/display.html")
src = f.read_text()

# Add heartbeat CSS
HEARTBEAT_CSS = """
  .sync-dot { width: 7px; height: 7px; border-radius: 50%; background: #22C55E; display: inline-block; margin-right: 5px; animation: hb-pulse 2s ease-in-out infinite; }
  .sync-dot.offline { background: #EF4444; animation: none; }
  .sync-bar { position: fixed; top: 0; left: 0; right: 0; padding: 6px 14px; background: rgba(10,12,15,0.85); backdrop-filter: blur(8px); display: flex; align-items: center; font-size: 11px; color: #5B6175; font-family: 'DM Mono', monospace; z-index: 50; }
  @keyframes hb-pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.85)} }
"""
src = src.replace("  @keyframes flash-clock", HEARTBEAT_CSS + "\n  @keyframes flash-clock")

# Add sync bar to body
src = src.replace(
    '<div class="speech-label"',
    '<div class="sync-bar"><span class="sync-dot" id="syncDot"></span><span id="syncLabel">Connecting&hellip;</span></div>\n  <div class="speech-label"'
)

# Update sync dot on connection state changes
src = src.replace(
    "document.getElementById('roomLabel').textContent = `ROOM ${room}`;",
    "document.getElementById('roomLabel').textContent = `ROOM ${room}`;\n  document.getElementById('syncLabel').textContent = 'Connecting\u2026';"
)

# Mark online when state received
src = src.replace(
    "onState(newState) {\n      state = newState;\n      render();",
    """onState(newState) {
      state = newState;
      render();
      var dot = document.getElementById('syncDot');
      var lbl = document.getElementById('syncLabel');
      if (dot) { dot.className = 'sync-dot'; lbl.textContent = 'Synced \u00b7 debateclock.org'; }"""
)

# Mark offline on disconnect
src = src.replace(
    "onClose() {",
    """onClose() {
      var dot = document.getElementById('syncDot');
      var lbl = document.getElementById('syncLabel');
      if (dot) { dot.className = 'sync-dot offline'; lbl.textContent = 'Reconnecting\u2026'; }"""
)

f.write_text(src)
print("ok: 3. Heartbeat sync indicator added to debater display")

# ══════════════════════════════════════════════════════════════════════════════
# 4. APP — STOP AT 00:00 TOGGLE
# ══════════════════════════════════════════════════════════════════════════════
f = pathlib.Path("app/index.html")
src = f.read_text()

TOGGLE_CSS = """
  .stop-toggle { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #8B90A0; margin-top: 8px; }
  .toggle-switch { position: relative; width: 32px; height: 18px; flex-shrink: 0; }
  .toggle-switch input { opacity: 0; width: 0; height: 0; }
  .toggle-slider { position: absolute; inset: 0; background: #1E232D; border-radius: 18px; cursor: pointer; transition: background .2s; }
  .toggle-slider::before { content:''; position: absolute; width: 12px; height: 12px; left: 3px; top: 3px; background: #5B6175; border-radius: 50%; transition: transform .2s, background .2s; }
  .toggle-switch input:checked + .toggle-slider { background: rgba(34,197,94,0.25); }
  .toggle-switch input:checked + .toggle-slider::before { transform: translateX(14px); background: #22C55E; }
"""
src = src.replace("  .stop-toggle {", "  /* already added */\n  .stop-toggle-skip {")  # guard
if "toggle-switch" not in src:
    src = src.replace("  @keyframes flash-red", TOGGLE_CSS + "\n  @keyframes flash-red")

# Add toggle HTML below the preview clock area
TOGGLE_HTML = """        <div class="stop-toggle">
          <label class="toggle-switch">
            <input type="checkbox" id="stopAtZeroToggle" onchange="syncToggle()" />
            <span class="toggle-slider"></span>
          </label>
          <span>Stop timer at 0:00</span>
        </div>"""

# Insert after prep cards section before speech list
src = src.replace(
    '<div class="speech-list" id="speechList">',
    TOGGLE_HTML + '\n      <div class="speech-list" id="speechList">'
)

TOGGLE_JS = """
var stopAtZero = false;
function syncToggle() {
  stopAtZero = document.getElementById('stopAtZeroToggle').checked;
  localStorage.setItem('dc_stop_at_zero', stopAtZero ? '1' : '0');
}
// Load preference
(function() {
  stopAtZero = localStorage.getItem('dc_stop_at_zero') === '1';
  var el = document.getElementById('stopAtZeroToggle');
  if (el) el.checked = stopAtZero;
})();
"""
src = src.replace("let isEchoing = false;", "let isEchoing = false;\n" + TOGGLE_JS)

# Broadcast stopAtZero in state
src = src.replace(
    "sock.send({ type: 'state', state: getState() });",
    "var st = getState(); st.stopAtZero = stopAtZero; sock.send({ type: 'state', state: st });"
)

f.write_text(src)
print("ok: 4. Stop at 00:00 toggle added to app")

# Apply stop-at-zero on display side
f = pathlib.Path("app/display.html")
src = f.read_text()

src = src.replace(
    "state = newState;\n      render();",
    "state = newState;\n      if (newState.stopAtZero && newState.speechPhase === 'overtime') { /* freeze display at 0:00 */ }\n      render();"
)

# In render, if stopAtZero and overtime, show 0:00
src = src.replace(
    "document.getElementById('clock').textContent = fmt(rem);",
    "var displayRem = (state && state.stopAtZero && rem < 0) ? 0 : rem;\n  document.getElementById('clock').textContent = fmt(displayRem);"
)

f.write_text(src)
print("ok: 4. Stop at 00:00 applied on debater display")

# ══════════════════════════════════════════════════════════════════════════════
# 5. DEBATER DISPLAY — BIGGER SPEECH LABEL
# ══════════════════════════════════════════════════════════════════════════════
f = pathlib.Path("app/display.html")
src = f.read_text()

# Make speech label much more prominent
src = src.replace(
    "  .speech-label {",
    "  .speech-label { font-size: 22px !important; font-weight: 600; letter-spacing: 0.02em; color: #E8EAF0 !important; margin-bottom: 16px; text-align: center; padding: 0 16px; /* override below */ display: block; }\n  .speech-label-ORIG {"
)

# Fix the mobile override too
src = src.replace(
    ".speech-label { font-size: 16px; margin-bottom: 10px; }",
    ".speech-label { font-size: 18px !important; margin-bottom: 10px; }"
)

f.write_text(src)
print("ok: 5. Speech label made more prominent on debater display")

print("\ndone. Run: git add -A && git commit -m 'Features: CSV import, QR download, heartbeat, stop at zero, bigger speech label' && git push")
