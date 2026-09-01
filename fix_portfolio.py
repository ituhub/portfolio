#!/usr/bin/env python3
"""
fix_portfolio.py — run from inside your `portfolio` repo, next to index.html.

    python3 fix_portfolio.py

Does two things:
  1. Corrects every model-count reference   (MarketLens = 7, EnergyLens = 6)
  2. Inserts the two demo videos with poster frames

Safe to run twice — it skips anything already applied, and writes a
backup to index.html.bak before touching the file.
"""
import shutil
import sys
from pathlib import Path

SRC = Path("index.html")

# ---------------------------------------------------------------- replacements
COUNT_FIXES = [
    # meta description
    ("7-models neural ensembles, bitemporal pipelines",
     "7- and 6-model neural ensembles, bitemporal pipelines"),

    # hero stat — one number can't describe two different ensembles,
    # so this slot now carries an operational metric instead
    ('<div class="hero-stat"><div class="num">7</div><div class="label">Model Ensemble</div></div>',
     '<div class="hero-stat"><div class="num">12K<span>+</span></div><div class="label">Forecasts Scored</div></div>'),

    # MarketLens body copy
    # NOTE: if the real MarketLens count is 8 (as the demo video says),
    # change "7-model" to "8-model" below, and also change the
    # MarketLens pipeline step in index.html from 7-Model to 8-Model.
    ("It orchestrates an <strong>8-model neural ensemble</strong>",
     "It orchestrates a <strong>7-model neural ensemble</strong>"),

    # EnergyLens body copy
    ("an <strong>8-model neural ensemble</strong> for 24-hour-ahead price prediction",
     "a <strong>6-model neural ensemble</strong> for 24-hour-ahead price prediction"),

    # EnergyLens pipeline step  (MarketLens step already reads 7 — left alone)
    ('<div class="step-name">8-Model Ensemble</div>',
     '<div class="step-name">6-Model Ensemble</div>'),
]

# ---------------------------------------------------------------- video blocks
CSS = """
/* DEMO VIDEO */
.demo { margin: 0 0 40px; }
.demo video { width: 100%; display: block; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); background: #0D2137; }
.demo figcaption { font-size: 0.76rem; color: rgba(255,255,255,0.42); margin-top: 10px; text-align: center; }

"""
CSS_ANCHOR = "/* GCP PRACTICE */"

MLP_ANCHOR = ('<a href="https://marketlenspro.app" target="_blank" rel="noopener noreferrer" '
              'class="proj-link proj-live">&#9679; View Live &mdash; marketlenspro.app</a>\n    </div>')
MLP_VIDEO = """
    <figure class="demo">
      <video controls muted playsinline preload="none" poster="assets/marketlens-demo-poster.jpg">
        <source src="assets/marketlens-demo.mp4" type="video/mp4">
        <a href="assets/marketlens-demo.mp4">Download the demo (3&nbsp;MB)</a>
      </video>
      <figcaption>Product walkthrough &mdash; landing page, signal dashboard, quality gate and paper-trading engine (1:11)</figcaption>
    </figure>"""

EL_ANCHOR = ('class="proj-link proj-live">&#9679; View Live Dashboard</a>\n    </div>')
EL_VIDEO = """
    <figure class="demo">
      <video controls muted playsinline preload="none" poster="assets/energylens-demo-poster.jpg">
        <source src="assets/energylens-demo.mp4" type="video/mp4">
        <a href="assets/energylens-demo.mp4">Download the demo (3&nbsp;MB)</a>
      </video>
      <figcaption>Platform walkthrough &mdash; ingestion, feature pipeline, forecast, explainability and accuracy tracking (1:06)</figcaption>
    </figure>"""


def main():
    if not SRC.exists():
        sys.exit("index.html not found — run this from the root of the portfolio repo.")

    html = SRC.read_text(encoding="utf-8")
    shutil.copy(SRC, "index.html.bak")
    applied, skipped = [], []

    for old, new in COUNT_FIXES:
        if old in html:
            html = html.replace(old, new)
            applied.append(old[:58] + "...")
        elif new in html:
            skipped.append("already fixed: " + new[:48] + "...")
        else:
            skipped.append("NOT FOUND (check manually): " + old[:48] + "...")

    if ".demo video" not in html:
        html = html.replace(CSS_ANCHOR, CSS.lstrip("\n") + CSS_ANCHOR, 1)
        applied.append("video CSS")
    else:
        skipped.append("video CSS already present")

    for name, anchor, block in (("MarketLens video", MLP_ANCHOR, MLP_VIDEO),
                                ("EnergyLens video", EL_ANCHOR, EL_VIDEO)):
        if block.strip() in html:
            skipped.append(name + " already embedded")
        elif anchor in html:
            html = html.replace(anchor, anchor + block, 1)
            applied.append(name)
        else:
            skipped.append("anchor NOT FOUND for " + name)

    SRC.write_text(html, encoding="utf-8")

    print("applied:")
    for a in applied:
        print("   +", a)
    print("skipped:")
    for s in skipped:
        print("   -", s)
    print("\nbackup written to index.html.bak")
    print("still to do by hand: the MarketLens sentence listing all 8 architecture names")


if __name__ == "__main__":
    main()
