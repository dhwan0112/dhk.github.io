"""Convert Quantum ESPRESSO guide Markdown sources into standalone HTML pages.

Mirrors the LAMMPS guide build: reuses the shared guide stylesheet and adds
KaTeX (math) and Prism (code highlighting) via CDN.

Source layout under SRC:
    intro/      8 introductory chapters + index.md
    examples/   4 runnable example walkthroughs

Output: dhk.github.io/guides/qe/*.html (flat; examples prefixed "ex-").
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
    ("index.html",                 "intro/index.md",               None,
        "실리콘 SCF 한 예제부터 시작해 pw.x 입력의 네임리스트 구조, 유사퍼텐셜, k점, 밴드·DOS까지 차근차근 풉니다."),
    ("01-getting-started.html",    "intro/01-getting-started.md",  "CHAPTER 01 · 시작",
        "설치 확인, pw.x 첫 실행, 가장 단순한 실리콘 SCF, 출력 파일 읽기."),
    ("02-input-structure.html",    "intro/02-input-structure.md",  "CHAPTER 02 · 시작",
        "pw.x 입력의 네임리스트(&control/&system/&electrons)와 카드(ATOMIC_*, K_POINTS, CELL_PARAMETERS) 구조."),
    ("03-pseudopotentials.html",   "intro/03-pseudopotentials.md", "CHAPTER 03 · 계산 준비",
        "유사퍼텐셜의 종류(NC/US/PAW), SSSP 라이브러리, ecutwfc·ecutrho 컷오프 선택."),
    ("04-kpoints.html",            "intro/04-kpoints.md",          "CHAPTER 04 · 계산 준비",
        "Monkhorst-Pack k점 격자, 자동/명시 K_POINTS, 수렴 점검과 금속의 주의점."),
    ("05-scf-convergence.html",    "intro/05-scf-convergence.md",  "CHAPTER 05 · 계산",
        "SCF 순환, mixing_beta·conv_thr, 금속의 smearing, 수렴이 안 될 때의 진단."),
    ("06-relax.html",              "intro/06-relax.md",            "CHAPTER 06 · 계산",
        "힘과 응력, relax·vc-relax, &ions/&cell, 최적화가 흔들릴 때의 대처."),
    ("07-bands-dos.html",          "intro/07-bands-dos.md",        "CHAPTER 07 · 결과",
        "scf→nscf→bands.x 밴드구조, dos.x 상태밀도, projwfc.x 투영 DOS와 후처리."),
    ("08-troubleshooting.html",    "intro/08-troubleshooting.md",  "CHAPTER 08 · 운영",
        "자주 나는 오류, 결과 의심 시 점검 순서, 병렬 실행(-nk)과 성능 감각, 좋은 운영 습관."),
    # === Examples: runnable walkthroughs ===
    ("ex-01-si-scf.html",          "examples/01-si-scf.md",        "예제 · E1",
        "실리콘 8원자 셀의 SCF 전체 에너지와 ecutwfc·k점 수렴을 실제로 돌려보는 첫 예제."),
    ("ex-02-si-bands.html",        "examples/02-si-bands.md",      "예제 · E2",
        "scf → nscf → bands.x 로 실리콘 밴드구조를, dos.x 로 상태밀도를 뽑는 완전한 워크플로."),
    ("ex-03-metal-smearing.html",  "examples/03-metal-smearing.md","예제 · E3",
        "금속 알루미늄을 smearing 으로 SCF 하고 페르미 준위와 상태밀도를 확인하는 예제."),
    ("ex-04-relax.html",           "examples/04-relax.md",         "예제 · E4",
        "힘·응력을 이용한 구조 최적화(relax/vc-relax)를 작은 계로 실제로 돌려보는 예제."),
]

# Sidebar nav grouping
NAV_SECTIONS = [
    ("입문 · 시작", [
        ("index.html",                 "00", "개요"),
        ("01-getting-started.html",    "01", "시작하기"),
        ("02-input-structure.html",    "02", "입력 파일 구조"),
    ]),
    ("입문 · 계산 준비", [
        ("03-pseudopotentials.html",   "03", "유사퍼텐셜"),
        ("04-kpoints.html",            "04", "k점 샘플링"),
    ]),
    ("입문 · 계산과 최적화", [
        ("05-scf-convergence.html",    "05", "SCF와 수렴"),
        ("06-relax.html",              "06", "구조 최적화"),
    ]),
    ("입문 · 결과와 운영", [
        ("07-bands-dos.html",          "07", "밴드와 DOS"),
        ("08-troubleshooting.html",    "08", "트러블슈팅"),
    ]),
    ("예제 · 따라 하기", [
        ("ex-01-si-scf.html",          "E1", "Si SCF"),
        ("ex-02-si-bands.html",        "E2", "Si 밴드 + DOS"),
        ("ex-03-metal-smearing.html",  "E3", "금속 smearing"),
        ("ex-04-relax.html",           "E4", "구조 최적화"),
    ]),
]


def render_sidebar(current: str) -> str:
    out = [
        '<aside class="sidebar">',
        '  <a href="../../" class="sidebar-back">← Donghwan KIM</a>',
        '  <a href="index.html" class="sidebar-brand">',
        '    <div class="brand-title">Quantum ESPRESSO</div>',
        '    <div class="brand-subtitle">한국어 입문 가이드</div>',
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
            f'<div class="page-nav-label">← 이전</div>'
            f'<div class="page-nav-title">{html_lib.escape(l)}</div></a>'
        )
    if 0 <= idx < len(flat) - 1:
        h, l = flat[idx + 1]
        next_html = (
            f'<a class="next" href="{h}">'
            f'<div class="page-nav-label">다음 →</div>'
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
    r"^##\s*목차\s*$\s*\{:[^}]*\}\s*\n\s*\n1\.\s*TOC\s*\n\{:toc\}\s*\n?",
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
            '<div class="toc-title">이 페이지에서 다룹니다</div>'
            f"{toc_inner}"
            "</div>\n"
        )
        body_html = toc_block + body_html

    body_html = restore_math(body_html, math)
    return body_html, toc_html


HEAD_TMPL = """<!DOCTYPE html>
<html lang="ko">
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
          <span class="hero-title-accent">한국어 입문 가이드</span>
        </h1>
        <p class="hero-tagline">{lede}</p>
        <div class="hero-meta">
          <span>대상 버전</span> 7.5 (2025) · <span>출발 예제</span> 실리콘(Si) · <span>주요 코드</span> pw.x · dos.x · projwfc.x
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
            page_title_full = "Quantum ESPRESSO 한국어 입문 가이드"
        else:
            short = title_raw.split(". ", 1)[-1] if ". " in title_raw else title_raw
            page_title_full = f"{short} · QE 가이드"

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
        print(f"wrote {out_name:<32}  ({len(body_html):>6} bytes body)")


if __name__ == "__main__":
    main()
