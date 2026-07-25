"""Convert Quantum ESPRESSO guide Markdown sources into standalone HTML pages.

Mirrors the LAMMPS guide build: reuses the shared guide stylesheet and adds
KaTeX (math) and Prism (code highlighting) via CDN.

Source layout under SRC:
    index.md        landing page
    chapters/       18 concept chapters (01~18)
    ref/            4 reference pages (keywords / cards / errors / executables)
    examples/       13 runnable labs (E1~E13, bundle inputs under ../files/)

Output: dhk.github.io/guides/qe/*.html (flat; refs "ref-", examples "ex-").
"""

from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

import markdown
import yaml

SRC = Path(__file__).resolve().parent / "src"
DST = Path(__file__).resolve().parent.parent
DST.mkdir(parents=True, exist_ok=True)

# (output_filename, source_md_relpath, page_eyebrow, page_lede)
PAGES = [
    ("index.html", "index.md", None,
        "From a single silicon SCF to DFT+U on antiferromagnetic FeO: a step-by-step, fully test-run guide to first-principles calculations with pw.x."),
    # === Basics · Getting started ===
    ("01-getting-started.html", "chapters/01-getting-started.md", "CHAPTER 01 · BASICS · GETTING STARTED",
        "The minimum background for plane-wave DFT, choosing an install route (conda or source), verifying the install, and getting pseudopotentials."),
    ("02-input-structure.html", "chapters/02-input-structure.md", "CHAPTER 02 · BASICS · GETTING STARTED",
        "The two-layer pw.x input format: namelists (&CONTROL/&SYSTEM/&ELECTRONS) and cards, dissected on a minimal input."),
    ("03-units-coordinates.html", "chapters/03-units-coordinates.md", "CHAPTER 03 · BASICS · GETTING STARTED",
        "Rydberg atomic units, ibrav and celldm, the alat/crystal/angstrom coordinate conventions, and the classic traps."),
    # === Basics · Core concepts ===
    ("04-pseudopotentials.html", "chapters/04-pseudopotentials.md", "CHAPTER 04 · BASICS · CORE CONCEPTS",
        "NC vs US vs PAW pseudopotentials, choosing from PSlibrary and SSSP, and reading the cutoffs a file demands."),
    ("05-convergence.html", "chapters/05-convergence.md", "CHAPTER 05 · BASICS · CORE CONCEPTS",
        "The standard procedure for converging ecutwfc, ecutrho and the k-grid, with the usual misconceptions."),
    ("06-occupations.html", "chapters/06-occupations.md", "CHAPTER 06 · BASICS · CORE CONCEPTS",
        "Choosing occupations for insulators and metals, smearing types and degauss, with measured scans."),
    ("07-scf-control.html", "chapters/07-scf-control.md", "CHAPTER 07 · BASICS · CORE CONCEPTS",
        "How the SCF cycle works, mixing_beta, mixing_mode and diagonalization, and a diagnosis order for failures."),
    # === Basics · Calculation types ===
    ("08-scf-nscf.html", "chapters/08-scf-nscf.md", "CHAPTER 08 · BASICS · CALCULATION TYPES",
        "The division of labor between scf and nscf/bands runs, and how to read the output file."),
    ("09-relaxation.html", "chapters/09-relaxation.md", "CHAPTER 09 · BASICS · CALCULATION TYPES",
        "Forces and stress, relax and vc-relax, BFGS, &IONS and &CELL, convergence criteria, and the post-vc-relax rerun."),
    ("10-dos-bands.html", "chapters/10-dos-bands.md", "CHAPTER 10 · BASICS · CALCULATION TYPES",
        "The dos.x, projwfc.x and bands.x post-processing pipelines, reading gaps, and interpreting PDOS."),
    ("11-postprocessing.html", "chapters/11-postprocessing.md", "CHAPTER 11 · BASICS · CALCULATION TYPES",
        "pp.x and plot_num, extracting charge densities and potentials, cube files, and visualization tools."),
    # === Advanced · Magnetism and correlation ===
    ("12-magnetism.html", "chapters/12-magnetism.md", "CHAPTER 12 · ADVANCED · MAGNETISM",
        "nspin and starting_magnetization, setting up AFM order with atom labels, and measured runs on bcc Fe and FeO."),
    ("13-dft-plus-u.html", "chapters/13-dft-plus-u.md", "CHAPTER 13 · ADVANCED · MAGNETISM",
        "Self-interaction error and DFT+U, the v7.1+ HUBBARD card syntax, and why (and how) a gap opens in FeO."),
    ("14-hubbard-hp.html", "chapters/14-hubbard-hp.md", "CHAPTER 14 · ADVANCED · MAGNETISM",
        "Computing U from first principles with hp.x: the linear-response workflow and its convergence parameters."),
    # === Advanced · Applications and operations ===
    ("15-surfaces.html", "chapters/15-surfaces.md", "CHAPTER 15 · ADVANCED · APPLICATIONS",
        "Building slab models, dipole corrections, planar-averaged potentials, and the work function."),
    ("16-molecular-dynamics.html", "chapters/16-molecular-dynamics.md", "CHAPTER 16 · ADVANCED · APPLICATIONS",
        "Born-Oppenheimer MD, the SVR thermostat, and sampling training data for machine-learned potentials."),
    ("17-phonons-neb.html", "chapters/17-phonons-neb.md", "CHAPTER 17 · ADVANCED · APPLICATIONS",
        "The big picture of ph.x phonons and neb.x reaction paths: when you need them and where to start."),
    ("18-parallel-hpc.html", "chapters/18-parallel-hpc.md", "CHAPTER 18 · ADVANCED · APPLICATIONS",
        "The -nk/-nd/-ni parallelization levels, scaling intuition for small and large systems, and HPC habits."),
    # === Reference ===
    ("ref-keywords.html", "ref/ref-keywords.md", "REFERENCE · R1",
        "A lookup dictionary of the main input variables, namelist by namelist, from &CONTROL to &CELL."),
    ("ref-cards.html", "ref/ref-cards.md", "REFERENCE · R2",
        "Syntax and options for the pw.x cards: ATOMIC_*, K_POINTS, CELL_PARAMETERS and HUBBARD."),
    ("ref-errors.html", "ref/ref-errors.md", "REFERENCE · R3",
        "An error dictionary organized as symptom, cause, fix, plus the cases that fail without any error."),
    ("ref-executables.html", "ref/ref-executables.md", "REFERENCE · R4",
        "The executables of the QE suite with their input namelists, prerequisites and outputs."),
    # === Examples · Hands-on ===
    ("ex-01-si-scf.html", "examples/01-si-scf.md", "EXAMPLE · E1",
        "Run the simplest possible silicon SCF and read every block of the output."),
    ("ex-02-si-ibrav0.html", "examples/02-si-ibrav0.md", "EXAMPLE · E2",
        "Rewrite the same crystal with ibrav=0 and CELL_PARAMETERS and verify the two descriptions agree."),
    ("ex-03-convergence.html", "examples/03-convergence.md", "EXAMPLE · E3",
        "Automate cutoff, k-point and force convergence tests with shell scripts."),
    ("ex-04-o2-molecule.html", "examples/04-o2-molecule.md", "EXAMPLE · E4",
        "Compute the O2 triplet molecule with isolation corrections and a fixed spin state, then get the binding energy."),
    ("ex-05-al-metal.html", "examples/05-al-metal.md", "EXAMPLE · E5",
        "A smearing SCF on metallic fcc Al: the Fermi level, and measured evidence for choosing degauss."),
    ("ex-06-si-vcrelax.html", "examples/06-si-vcrelax.md", "EXAMPLE · E6",
        "Find the equilibrium lattice constant of silicon with a variable-cell relaxation."),
    ("ex-07-si-dos.html", "examples/07-si-dos.md", "EXAMPLE · E7",
        "The scf, nscf, dos.x and projwfc.x density-of-states pipeline, plus Löwdin charges."),
    ("ex-08-si-bands.html", "examples/08-si-bands.md", "EXAMPLE · E8",
        "Compute the silicon band structure along a high-symmetry path and read off the indirect gap."),
    ("ex-09-fe-bcc.html", "examples/09-fe-bcc.md", "EXAMPLE · E9",
        "A spin-polarized SCF for ferromagnetic bcc Fe and its magnetic moment."),
    ("ex-10-feo-afm.html", "examples/10-feo-afm.md", "EXAMPLE · E10",
        "Set up antiferromagnetic FeO and watch GGA wrongly predict a metal."),
    ("ex-11-feo-hubbard.html", "examples/11-feo-hubbard.md", "EXAMPLE · E11",
        "Turn on U with the HUBBARD card, measure the Hubbard splitting, and diagnose the famous metallic trap."),
    ("ex-12-feo-hp.html", "examples/12-feo-hp.md", "EXAMPLE · E12",
        "Compute U from first principles with hp.x linear response, no empirical parameters."),
    ("ex-13-slab-md.html", "examples/13-slab-md.md", "EXAMPLE · E13",
        "Slab generation, the work function, and Born-Oppenheimer MD as a starting point for ML training data."),
]

# Sidebar nav grouping
NAV_SECTIONS = [
    ("Basics · Getting started", [
        ("index.html",              "00", "Overview"),
        ("01-getting-started.html", "01", "Getting started"),
        ("02-input-structure.html", "02", "Input file structure"),
        ("03-units-coordinates.html", "03", "Units and coordinates"),
    ]),
    ("Basics · Core concepts", [
        ("04-pseudopotentials.html", "04", "Pseudopotentials"),
        ("05-convergence.html",      "05", "Cutoff and k-point convergence"),
        ("06-occupations.html",      "06", "Occupations and smearing"),
        ("07-scf-control.html",      "07", "Controlling SCF convergence"),
    ]),
    ("Basics · Calculation types", [
        ("08-scf-nscf.html",       "08", "SCF and NSCF"),
        ("09-relaxation.html",     "09", "Structure optimization"),
        ("10-dos-bands.html",      "10", "DOS and band structure"),
        ("11-postprocessing.html", "11", "Densities and potentials"),
    ]),
    ("Advanced · Magnetism and correlation", [
        ("12-magnetism.html",  "12", "Spin polarization and magnetism"),
        ("13-dft-plus-u.html", "13", "DFT+U and the HUBBARD card"),
        ("14-hubbard-hp.html", "14", "Computing U with hp.x"),
    ]),
    ("Advanced · Applications and operations", [
        ("15-surfaces.html",           "15", "Surfaces, slabs, work function"),
        ("16-molecular-dynamics.html", "16", "Molecular dynamics"),
        ("17-phonons-neb.html",        "17", "Phonons and reaction paths"),
        ("18-parallel-hpc.html",       "18", "Parallel execution and HPC"),
    ]),
    ("Reference", [
        ("ref-keywords.html",    "R1", "Keyword dictionary"),
        ("ref-cards.html",       "R2", "Card reference"),
        ("ref-errors.html",      "R3", "Error message dictionary"),
        ("ref-executables.html", "R4", "Executables"),
    ]),
    ("Examples · Hands-on", [
        ("ex-01-si-scf.html",       "E1",  "Si SCF"),
        ("ex-02-si-ibrav0.html",    "E2",  "Rewriting with ibrav=0"),
        ("ex-03-convergence.html",  "E3",  "Automating convergence tests"),
        ("ex-04-o2-molecule.html",  "E4",  "O₂ molecule (triplet)"),
        ("ex-05-al-metal.html",     "E5",  "fcc Al metal"),
        ("ex-06-si-vcrelax.html",   "E6",  "Si vc-relax"),
        ("ex-07-si-dos.html",       "E7",  "Si DOS and PDOS"),
        ("ex-08-si-bands.html",     "E8",  "Si band structure"),
        ("ex-09-fe-bcc.html",       "E9",  "Ferromagnetic bcc Fe"),
        ("ex-10-feo-afm.html",      "E10", "FeO AFM (where GGA fails)"),
        ("ex-11-feo-hubbard.html",  "E11", "FeO with DFT+U"),
        ("ex-12-feo-hp.html",       "E12", "Computing U with hp.x"),
        ("ex-13-slab-md.html",      "E13", "Slabs and AIMD"),
    ]),
]


def render_sidebar(current: str) -> str:
    out = [
        '<aside class="sidebar">',
        '  <a href="../../" class="sidebar-back">← Donghwan KIM</a>',
        '  <a href="index.html" class="sidebar-brand">',
        '    <div class="brand-title">Quantum ESPRESSO</div>',
        '    <div class="brand-subtitle">A Practical Guide</div>',
        '  </a>',
        '  <nav>',
    ]
    for section_title, items in NAV_SECTIONS:
        out.append('    <div class="nav-section">')
        out.append(f'      <div class="nav-section-title">{section_title}</div>')
        out.append('      <ul class="nav-list">')
        for href, num, label in items:
            active = ' class="active" aria-current="page"' if href == current else ''
            out.append(
                f'        <li><a href="{href}"{active}>'
                f'<span class="nav-num">{num}</span>{label}</a></li>'
            )
        out.append('      </ul>')
        out.append('    </div>')
    out.append('  </nav>')
    out.append('</aside>')
    return "\n".join(out)


def render_page_nav(current: str) -> str:
    flat = []
    for _, items in NAV_SECTIONS:
        for href, _num, label in items:
            flat.append((href, label))
    idx = next((i for i, (h, _) in enumerate(flat) if h == current), -1)
    prev_html = next_html = ""
    if idx > 0:
        h, l = flat[idx - 1]
        prev_html = (
            f'<a class="prev" href="{h}">'
            f'<div class="page-nav-label">← Previous</div>'
            f'<div class="page-nav-title">{html_lib.escape(l)}</div></a>'
        )
    if 0 <= idx < len(flat) - 1:
        h, l = flat[idx + 1]
        next_html = (
            f'<a class="next" href="{h}">'
            f'<div class="page-nav-label">Next →</div>'
            f'<div class="page-nav-title">{html_lib.escape(l)}</div></a>'
        )
    if not (prev_html or next_html):
        return ""
    return f'<nav class="page-nav">{prev_html}{next_html}</nav>'


def split_frontmatter(text: str):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = yaml.safe_load(text[3:end]) or {}
            body = text[end + 4:].lstrip("\n")
            return fm, body
    return {}, text


KRAMDOWN_TOC_BLOCK = re.compile(
    r"^##\s*(?:목차|Contents)\s*$\s*\{:[^}]*\}\s*\n\s*\n1\.\s*TOC\s*\n\{:toc\}\s*\n?",
    re.MULTILINE,
)
KRAMDOWN_ATTR_LINE = re.compile(r"^\{:[^}]*\}\s*$\n?", re.MULTILINE)
KRAMDOWN_ATTR_INLINE = re.compile(r"\s*\{:[^}]*\}\s*$", re.MULTILINE)
H1_LINE = re.compile(r"^#\s+[^\n]+\n", re.MULTILINE)


def stash_math(text: str):
    blocks = []

    def block_repl(m):
        blocks.append(m.group(0))
        return f"@@MATHBLOCK{len(blocks) - 1}@@"

    def inline_repl(m):
        blocks.append(m.group(0))
        return f"@@MATHINLINE{len(blocks) - 1}@@"

    text = re.sub(r"\$\$[\s\S]*?\$\$", block_repl, text)
    text = re.sub(r"(?<!\\)\$[^\$\n]+?\$", inline_repl, text)
    return text, blocks


def restore_math(html_out: str, blocks):
    for i, blk in enumerate(blocks):
        html_out = html_out.replace(f"@@MATHBLOCK{i}@@", blk)
        html_out = html_out.replace(f"@@MATHINLINE{i}@@", blk)
    return html_out


def convert_body(md_body: str) -> tuple[str, str]:
    had_toc_block = bool(KRAMDOWN_TOC_BLOCK.search(md_body))
    md_body = KRAMDOWN_TOC_BLOCK.sub("", md_body)
    md_body = KRAMDOWN_ATTR_LINE.sub("", md_body)
    md_body = KRAMDOWN_ATTR_INLINE.sub("", md_body)
    md_body = H1_LINE.sub("", md_body, count=1)

    md_body, math = stash_math(md_body)

    md = markdown.Markdown(
        extensions=["extra", "tables", "fenced_code", "toc", "sane_lists"],
        extension_configs={"toc": {"toc_depth": "2-3"}},
    )
    body_html = md.convert(md_body)
    toc_html = md.toc or ""

    if had_toc_block and toc_html:
        toc_inner = re.sub(
            r'<div class="toc">(.*)</div>\s*$', r"\1", toc_html, count=1, flags=re.DOTALL
        )
        toc_block = (
            '<div class="toc">'
            '<div class="toc-title">On this page</div>'
            f"{toc_inner}"
            "</div>\n"
        )
        body_html = toc_block + body_html

    body_html = restore_math(body_html, math)
    return body_html, toc_html


HEAD_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="icon" type="image/x-icon" href="../../favicon.ico" />
  <link rel="stylesheet" href="assets/css/style.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" />
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{
      delimiters: [
        {{left: '$$', right: '$$', display: true}},
        {{left: '$', right: '$', display: false}}
      ]
    }});"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" />
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-fortran.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
</head>
<body>
  <button class="mobile-nav-toggle">MENU</button>
  <div class="layout">
{sidebar}
    <main class="main">
{header}
      <article class="content">
{body}
      </article>
{page_nav}
    </main>
  </div>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""

HERO_TMPL = """      <section class="hero">
        <h1 class="hero-title">
          <em>Quantum ESPRESSO</em><br />
          <span class="hero-title-accent">A Practical Guide</span>
        </h1>
        <p class="hero-tagline">{lede}</p>
        <div class="hero-meta">
          <span>Target version</span> QE 7.5 · <span>First example</span> Si SCF · <span>Application arc</span> Fe–O oxides
        </div>
      </section>"""

PAGE_HEADER_TMPL = """      <header class="page-header">
        <div class="page-eyebrow">{eyebrow}</div>
        <h1 class="page-title">{title}</h1>
        <p class="page-lede">{lede}</p>
      </header>"""


def main():
    for out_name, src_rel, eyebrow, lede in PAGES:
        src_path = SRC / src_rel
        text = src_path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)

        title_raw = str(fm.get("title", "") or "").strip()
        if out_name == "index.html":
            page_title_full = "Quantum ESPRESSO: A Practical Guide"
        else:
            short = title_raw.split(". ", 1)[-1] if ". " in title_raw else title_raw
            page_title_full = f"{short} · QE Guide"

        body_html, _toc = convert_body(body)

        if out_name == "index.html":
            header_html = HERO_TMPL.format(lede=html_lib.escape(lede))
        else:
            short = title_raw.split(". ", 1)[-1] if ". " in title_raw else title_raw
            header_html = PAGE_HEADER_TMPL.format(
                eyebrow=html_lib.escape(eyebrow or ""),
                title=html_lib.escape(short or title_raw),
                lede=html_lib.escape(lede or ""),
            )

        html_out = HEAD_TMPL.format(
            title=html_lib.escape(page_title_full),
            description=html_lib.escape(lede or ""),
            sidebar=render_sidebar(out_name),
            header=header_html,
            body=body_html,
            page_nav=render_page_nav(out_name),
        )

        (DST / out_name).write_text(html_out, encoding="utf-8")
        print(f"wrote {out_name:<28}  ({len(body_html):>6} bytes body)")


if __name__ == "__main__":
    main()
