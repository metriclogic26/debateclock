#!/usr/bin/env python3
import pathlib

f = pathlib.Path("practice/tournament/index.html")
src = f.read_text()

# Replace the number input for minutes with a full 60-option select
OLD = """      <input type="number" id="roundMin" class="time-input"
        placeholder="00" min="0" max="59" value="0"
        style="width:76px;padding:12px 8px;font-size:16px;font-weight:600;text-align:center;">"""

# Build all 60 options
options = "\n".join(
    f'        <option value="{i}">{str(i).zfill(2)}</option>'
    for i in range(60)
)

NEW = f"""      <select class="time-input" id="roundMin"
        style="width:80px;padding:12px 8px;font-size:16px;font-weight:600;text-align:center;">
{options}
      </select>"""

if OLD in src:
    src = src.replace(OLD, NEW)
    print("ok: minutes replaced with 60-option select")
else:
    print("miss: minutes input not found")

# Fix addRound to use parseInt on select value
src = src.replace(
    "  var m = parseInt(document.getElementById('roundMin').value) || 0;",
    "  var m = parseInt(document.getElementById('roundMin').value);"
)

# Fix setDefaultTime to set nearest 5-min mark
src = src.replace(
    "  document.getElementById('roundMin').value = 0;",
    "  document.getElementById('roundMin').value = 0; // default to :00"
)

f.write_text(src)
print("done.")
