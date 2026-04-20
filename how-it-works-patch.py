#!/usr/bin/env python3
import pathlib, re

f = pathlib.Path("index.html")
src = f.read_text()

# CSS for the how-it-works section
HOW_CSS = """
  /* HOW IT WORKS */
  .how-section {
    max-width: 900px;
    margin: 0 auto 60px;
    padding: 0 24px;
  }
  .how-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.18em;
    text-transform: uppercase; color: #5B6175;
    text-align: center; margin-bottom: 12px;
  }
  .how-title {
    font-size: 22px; font-weight: 700; color: #E8EAF0;
    text-align: center; margin-bottom: 32px;
  }
  .how-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 14px;
    position: relative;
  }
  .how-card {
    background: #111318;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 24px 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    position: relative;
  }
  .how-num {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.25);
    display: flex; align-items: center; justify-content: center;
    font-family: 'DM Mono', monospace;
    font-size: 15px; font-weight: 600;
    color: #3B82F6;
  }
  .how-card h3 {
    font-size: 15px; font-weight: 600; color: #E8EAF0;
    margin: 0;
  }
  .how-card p {
    font-size: 13px; color: #8B90A0;
    line-height: 1.6; margin: 0;
  }
  .how-card .how-icon {
    font-size: 28px; margin-bottom: 2px;
  }
  /* arrow between cards */
  .how-arrow {
    position: absolute;
    top: 50%; transform: translateY(-50%);
    color: #3B3F4D;
    font-size: 18px;
    pointer-events: none;
    z-index: 1;
  }
  .how-arrow-1 { left: calc(33.33% - 10px); }
  .how-arrow-2 { left: calc(66.66% - 10px); }
  @media (max-width: 640px) {
    .how-grid { grid-template-columns: 1fr; }
    .how-arrow { display: none; }
  }
"""

HOW_HTML = """
  <!-- HOW IT WORKS -->
  <div class="how-section">
    <div class="how-label">How it works</div>
    <div class="how-title">Live in 30 seconds</div>
    <div class="how-grid">
      <span class="how-arrow how-arrow-1">&#8594;</span>
      <span class="how-arrow how-arrow-2">&#8594;</span>
      <div class="how-card">
        <div class="how-num">1</div>
        <div class="how-icon">&#9654;&#65039;</div>
        <h3>Judge opens the timer</h3>
        <p>Go to debateclock.org/app on your phone. A room code is generated instantly &mdash; no signup, no install.</p>
      </div>
      <div class="how-card">
        <div class="how-num">2</div>
        <div class="how-icon">&#128279;</div>
        <h3>Debater scans or taps the link</h3>
        <p>Share the QR code or link. The debater opens the display on their laptop or tablet &mdash; full-screen countdown appears immediately.</p>
      </div>
      <div class="how-card">
        <div class="how-num">3</div>
        <div class="how-icon">&#9201;</div>
        <h3>Start timing</h3>
        <p>Judge controls the timer from their phone. Both screens stay in sync in real time. Prep pool tracks automatically across all speeches.</p>
      </div>
    </div>
  </div>
"""

# Insert CSS before closing </style>
if 'how-section' not in src:
    src = src.replace('</style>', HOW_CSS + '\n  </style>', 1)
    print("ok: CSS added")
else:
    print("skip: CSS already present")

# Insert HTML after the demo section, before the formats section
if 'how-section' not in src or '<!-- HOW IT WORKS -->' not in src:
    src = src.replace(
        '<section class="formats">',
        HOW_HTML + '\n  <section class="formats">',
        1
    )
    print("ok: HTML inserted")
else:
    print("skip: HTML already present")

f.write_text(src)
print("done.")
