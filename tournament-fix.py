#!/usr/bin/env python3
import pathlib, re

f = pathlib.Path("practice/tournament/index.html")
src = f.read_text()

# Find and replace the entire add-card inner content
OLD = re.search(r'<div class="add-card">.*?</div>\s*<!-- ROUND LIST -->', src, re.DOTALL).group()

NEW = '''<div class="add-card">
    <div class="add-card-title">Add a round or event</div>

    <!-- Row 1: Name -->
    <div style="margin-bottom:10px;">
      <input class="round-name-input" type="text" id="roundName"
        placeholder="Round 1, Lunch, Awards…"
        style="width:100%;box-sizing:border-box;font-size:15px;padding:12px 14px;">
    </div>

    <!-- Row 2: Time selects -->
    <div style="display:flex;gap:8px;align-items:center;margin-bottom:10px;flex-wrap:wrap;">
      <select class="time-input" id="roundHour"
        style="width:70px;padding:12px 8px;font-size:16px;font-weight:600;text-align:center;">
        <option value="1">1</option><option value="2">2</option><option value="3">3</option>
        <option value="4">4</option><option value="5">5</option><option value="6">6</option>
        <option value="7">7</option><option value="8">8</option><option value="9">9</option>
        <option value="10">10</option><option value="11">11</option><option value="12">12</option>
      </select>
      <span style="color:#5B6175;font-size:22px;font-weight:700;">:</span>
      <select class="time-input" id="roundMin"
        style="width:80px;padding:12px 8px;font-size:16px;font-weight:600;text-align:center;">
        <option value="00">00</option><option value="05">05</option><option value="10">10</option>
        <option value="15">15</option><option value="20">20</option><option value="25">25</option>
        <option value="30">30</option><option value="35">35</option><option value="40">40</option>
        <option value="45">45</option><option value="50">50</option><option value="55">55</option>
        <option value="custom">other…</option>
      </select>
      <select class="time-input" id="roundAmPm"
        style="width:76px;padding:12px 8px;font-size:16px;font-weight:600;text-align:center;">
        <option value="AM">AM</option>
        <option value="PM" selected>PM</option>
      </select>
      <input type="number" id="customMinInput" class="time-input"
        placeholder="min" min="0" max="59"
        style="width:80px;padding:12px 8px;font-size:16px;display:none;text-align:center;">
    </div>

    <!-- Row 3: Add button -->
    <button class="add-btn" onclick="addRound()"
      style="width:100%;padding:14px;font-size:15px;border-radius:10px;">
      + Add to schedule
    </button>

    <!-- Quick presets -->
    <div class="quick-presets" style="margin-top:12px;">
      <span style="font-size:10px;color:#5B6175;letter-spacing:.1em;text-transform:uppercase;margin-right:4px;">Quick:</span>
      <button class="quick-btn" onclick="quickAdd('Round 1')">Round 1</button>
      <button class="quick-btn" onclick="quickAdd('Round 2')">Round 2</button>
      <button class="quick-btn" onclick="quickAdd('Round 3')">Round 3</button>
      <button class="quick-btn" onclick="quickAdd('Round 4')">Round 4</button>
      <button class="quick-btn" onclick="quickAdd('Lunch')">Lunch</button>
      <button class="quick-btn" onclick="quickAdd('Awards')">Awards</button>
    </div>
  </div>

  <!-- ROUND LIST -->'''

src = src.replace(OLD, NEW)

# Make sure customMinInput shows/hides correctly
if "roundMin').addEventListener" not in src:
    src = src.replace(
        "document.getElementById('roundName').addEventListener('keydown'",
        """document.getElementById('roundMin').addEventListener('change', function() {
  var custom = document.getElementById('customMinInput');
  custom.style.display = this.value === 'custom' ? 'inline-block' : 'none';
  if (this.value === 'custom') custom.focus();
});

document.getElementById('roundName').addEventListener('keydown'"""
    )

# Fix addRound to handle custom min
if "mSel === 'custom'" not in src:
    src = src.replace(
        "  var h = parseInt(document.getElementById('roundHour').value);",
        """  var h = parseInt(document.getElementById('roundHour').value);"""
    )
    src = src.replace(
        "  var m = document.getElementById('roundMin').value;",
        "  var mSel = document.getElementById('roundMin').value;\n  var m = mSel === 'custom' ? (parseInt(document.getElementById('customMinInput').value) || 0) : parseInt(mSel);"
    )
    src = src.replace(
        "  var ms = (h24 * 3600 + parseInt(m) * 60) * 1000;",
        "  var ms = (h24 * 3600 + m * 60) * 1000;"
    )

f.write_text(src)
print("ok: add form rewritten")
