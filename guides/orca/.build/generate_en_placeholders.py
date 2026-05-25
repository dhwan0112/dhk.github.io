"""Generate English placeholder pages for the ORCA guide chapters whose
English translation is not yet written. Each placeholder shares the same
sidebar/layout as the fully translated pages and points to the Korean
version of the same chapter, so the KO/EN toggle stays functional while
the translation is in progress."""

from __future__ import annotations
from pathlib import Path

DST = Path(__file__).resolve().parent.parent / "en"
DST.mkdir(parents=True, exist_ok=True)

# (filename, eyebrow, english title, english lede, ko filename)
PAGES = [
    ("input-structure.html",       "CHAPTER 02 · GETTING STARTED", "Input file structure",
        "Keyword lines, %-blocks and coordinate input — the syntax of an ORCA input file on a single page."),
    ("keywords.html",              "CHAPTER 03 · GETTING STARTED", "Keywords",
        "A short dictionary of the most common method, basis, and convergence keywords you will encounter."),
    ("single-point.html",          "CHAPTER 04 · COMMON CALCULATIONS", "Single point energy",
        "Energy and wavefunction at a fixed geometry — the most basic ORCA job."),
    ("geometry-optimization.html", "CHAPTER 05 · COMMON CALCULATIONS", "Geometry optimisation",
        "Constraints, choice of coordinate system, and one-/two-dimensional potential-surface scans."),
    ("frequencies.html",           "CHAPTER 06 · COMMON CALCULATIONS", "Frequencies · Thermochemistry",
        "Analytical vs numerical frequencies, and Gibbs free energy from the output."),
    ("transition-states.html",     "CHAPTER 07 · COMMON CALCULATIONS", "Transition states · NEB",
        "NEB-TS, ScanTS, and other strategies for locating activation barriers."),
    ("excited-states.html",        "CHAPTER 08 · COMMON CALCULATIONS", "Excited states · TD-DFT",
        "UV-Vis absorption spectra and the basics of fluorescence calculations."),
    ("solvation.html",             "CHAPTER 09 · COMMON CALCULATIONS", "Solvation",
        "Practical use of implicit-solvent models such as CPCM and SMD."),
    ("coupled-cluster.html",       "CHAPTER 10 · METHODS & MODELS", "DLPNO-CCSD(T)",
        "The gold-standard correlation method, now affordable for large molecules."),
    ("basis-sets.html",            "CHAPTER 11 · METHODS & MODELS", "Basis sets",
        "When to reach for def2, cc-pVnZ, SARC, and friends."),
    ("dft-functionals.html",       "CHAPTER 12 · METHODS & MODELS", "DFT functionals",
        "Beyond B3LYP — r²SCAN, ωB97X-V and other modern choices."),
    ("tips.html",                  "CHAPTER 13 · OPERATIONS",       "Tips &amp; troubleshooting",
        "SCF convergence failure, out-of-memory errors and other day-to-day traps."),
]

# Flat sequence for prev/next nav (must match the sidebar order)
FLAT = [
    ("index.html",                 "Overview"),
    ("getting-started.html",       "Getting started"),
    ("input-structure.html",       "Input file structure"),
    ("keywords.html",              "Keywords"),
    ("single-point.html",          "Single point energy"),
    ("geometry-optimization.html", "Geometry optimisation"),
    ("frequencies.html",           "Frequencies"),
    ("transition-states.html",     "Transition states · NEB"),
    ("excited-states.html",        "Excited states · TD-DFT"),
    ("solvation.html",             "Solvation"),
    ("coupled-cluster.html",       "DLPNO-CCSD(T)"),
    ("basis-sets.html",            "Basis sets"),
    ("dft-functionals.html",       "DFT functionals"),
    ("tips.html",                  "Tips · Troubleshooting"),
]

SIDEBAR = """<aside class="sidebar">
  <a href="../../../" class="sidebar-back">← Donghwan KIM</a>
  <div class="sidebar-lang">
    <a href="../ko/{filename}">KO</a>
    <a href="{filename}" class="active">EN</a>
  </div>
  <a href="index.html" class="sidebar-brand">
    <div class="brand-title">ORCA</div>
    <div class="brand-subtitle">User Guide · v6.0</div>
  </a>

  <nav>
    <div class="nav-section">
      <div class="nav-section-title">Getting Started</div>
      <ul class="nav-list">
        <li><a href="index.html"><span class="nav-num">00</span>Overview</a></li>
        <li><a href="getting-started.html"><span class="nav-num">01</span>Getting started</a></li>
        <li><a href="input-structure.html"><span class="nav-num">02</span>Input file structure</a></li>
        <li><a href="keywords.html"><span class="nav-num">03</span>Keywords</a></li>
      </ul>
    </div>

    <div class="nav-section">
      <div class="nav-section-title">Common Calculations</div>
      <ul class="nav-list">
        <li><a href="single-point.html"><span class="nav-num">04</span>Single point energy</a></li>
        <li><a href="geometry-optimization.html"><span class="nav-num">05</span>Geometry optimisation</a></li>
        <li><a href="frequencies.html"><span class="nav-num">06</span>Frequencies</a></li>
        <li><a href="transition-states.html"><span class="nav-num">07</span>Transition states · NEB</a></li>
        <li><a href="excited-states.html"><span class="nav-num">08</span>Excited states · TD-DFT</a></li>
        <li><a href="solvation.html"><span class="nav-num">09</span>Solvation</a></li>
      </ul>
    </div>

    <div class="nav-section">
      <div class="nav-section-title">Methods &amp; Models</div>
      <ul class="nav-list">
        <li><a href="coupled-cluster.html"><span class="nav-num">10</span>DLPNO-CCSD(T)</a></li>
        <li><a href="basis-sets.html"><span class="nav-num">11</span>Basis sets</a></li>
        <li><a href="dft-functionals.html"><span class="nav-num">12</span>DFT functionals</a></li>
      </ul>
    </div>

    <div class="nav-section">
      <div class="nav-section-title">Operations</div>
      <ul class="nav-list">
        <li><a href="tips.html"><span class="nav-num">13</span>Tips · Troubleshooting</a></li>
      </ul>
    </div>
  </nav>
</aside>"""


def render_page_nav(filename: str) -> str:
    idx = next((i for i, (f, _) in enumerate(FLAT) if f == filename), -1)
    prev_html = next_html = ""
    if idx > 0:
        f, l = FLAT[idx - 1]
        prev_html = (
            f'<a class="prev" href="{f}">'
            f'<div class="page-nav-label">← previous</div>'
            f'<div class="page-nav-title">{l}</div></a>'
        )
    if 0 <= idx < len(FLAT) - 1:
        f, l = FLAT[idx + 1]
        next_html = (
            f'<a class="next" href="{f}">'
            f'<div class="page-nav-label">next →</div>'
            f'<div class="page-nav-title">{l}</div></a>'
        )
    if not (prev_html or next_html):
        return ""
    return f'<nav class="page-nav">{prev_html}{next_html}</nav>'


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title_plain} · ORCA User Guide</title>
  <meta name="description" content="{lede_plain}" />
  <link rel="icon" type="image/x-icon" href="../../../favicon.ico" />
  <link rel="stylesheet" href="../assets/css/style.css" />
</head>
<body>
  <button class="mobile-nav-toggle">MENU</button>
  <div class="layout">
{sidebar}

    <main class="main">
      <header class="page-header">
        <div class="page-eyebrow">{eyebrow}</div>
        <h1 class="page-title">{title_html}</h1>
        <p class="page-lede">{lede}</p>
      </header>

      <article class="content">
        <div class="note">
          <div class="note-title">Translation in progress</div>
          <p>
            The English version of this chapter is being written. In the meantime, the
            corresponding Korean chapter is fully available — please follow the link below
            or use the <strong>KO</strong> toggle in the top-left of the sidebar.
          </p>
          <p>
            → <a href="../ko/{filename}">Read this chapter in Korean (한국어)</a>
          </p>
        </div>

        <p>
          If you would like to be notified when the English translation lands, please open
          an issue at
          <a href="https://github.com/dhwan0112/dhk.github.io/issues">dhwan0112/dhk.github.io</a>.
        </p>
      </article>

{page_nav}
    </main>
  </div>
  <script src="../assets/js/main.js"></script>
</body>
</html>
"""


def html_strip(text: str) -> str:
    import re
    return re.sub(r"&[a-z]+;", lambda m: {"&amp;": "&", "&lt;": "<", "&gt;": ">"}.get(m.group(0), m.group(0)), text)


def main():
    for filename, eyebrow, title, lede in PAGES:
        title_plain = html_strip(title)
        lede_plain = html_strip(lede)
        out = TEMPLATE.format(
            title_plain=title_plain,
            lede_plain=lede_plain,
            sidebar=SIDEBAR.format(filename=filename),
            eyebrow=eyebrow,
            title_html=title,
            lede=lede,
            page_nav=render_page_nav(filename),
            filename=filename,
        )
        (DST / filename).write_text(out, encoding="utf-8")
        print(f"wrote en/{filename}")


if __name__ == "__main__":
    main()
