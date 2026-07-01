"""Convert LAMMPS guide Markdown sources into ORCA-style standalone HTML pages.

Source layout under SRC:
    intro/      8 introductory chapters + index.md (LAMMPS itself)
    cu/         8 applied chapters + index.md (Cu surface adsorption)

Output: dhk.github.io/guides/lammps/*.html (flat, prefix "cu-" for applied
series). Reuses the ORCA guide style sheet and adds KaTeX (math) and Prism
(code highlighting) via CDN.
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
    # === Intro series ===
    ("index.html",                "intro/index.md",              None,
        "Lennard-Jones 액체 한 예제부터 시작해 LAMMPS 입력 스크립트의 4단계 구조와 자주 쓰는 명령을 차근차근 풉니다."),
    ("01-getting-started.html",   "intro/01-getting-started.md", "CHAPTER 01 · 시작",
        "LAMMPS 설치, 첫 명령, Lennard-Jones 액체 예제, 출력 파일의 의미."),
    ("02-input-structure.html",   "intro/02-input-structure.md", "CHAPTER 02 · 시작",
        "공식 매뉴얼이 정의하는 입력 스크립트의 4단계 구조와 각 단계의 핵심 명령."),
    ("03-units-atomstyle.html",   "intro/03-units-atomstyle.md", "CHAPTER 03 · 시뮬레이션 만들기",
        "단위계(lj/real/metal …) 선택과 atom_style 의 의미, 그리고 둘이 함께 결정하는 입력의 톤."),
    ("04-system.html",            "intro/04-system.md",          "CHAPTER 04 · 시뮬레이션 만들기",
        "박스와 원자를 만드는 세 가지 방법: read_data, read_restart, lattice + create_atoms."),
    ("05-forcefield.html",        "intro/05-forcefield.md",      "CHAPTER 05 · 시뮬레이션 만들기",
        "pair_style 개관, 결합 상호작용, kspace_style. 입력에서 가장 흔히 헷갈리는 부분 정리."),
    ("06-fix-run.html",           "intro/06-fix-run.md",         "CHAPTER 06 · 시뮬레이션 만들기",
        "velocity, timestep, fix(NVE/NVT/NPT/Langevin), minimize, run — 시뮬레이션을 돌리는 마지막 한 묶음."),
    ("07-output.html",            "intro/07-output.md",          "CHAPTER 07 · 결과 보기",
        "thermo, dump, compute, fix ave/*, restart 그리고 OVITO/VMD 등 후처리 도구."),
    ("08-troubleshooting.html",   "intro/08-troubleshooting.md", "CHAPTER 08 · 운영",
        "자주 발생하는 오류, 결과 의심 시 점검 순서, 병렬 실행과 성능 진단, 좋은 운영 습관."),
    # === Examples: runnable walkthroughs ===
    ("ex-01-lj-basic.html",       "examples/01-lj-basic.md",      "예제 · E1",
        "외부 파일 없이 LJ 액체 4000개를 NVE로 250 step 돌리는 가장 단순한 첫 실행."),
    ("ex-02-lj-demo.html",        "examples/02-lj-demo.md",       "예제 · E2",
        "LJ 액체를 최소화 → NVT → NPT → 생성으로 돌리고 RDF·MSD를 측정하는 완전한 워크플로."),
    ("ex-03-cu-slab.html",        "examples/03-cu-slab.md",       "예제 · E3",
        "EAM으로 Cu(100) 슬랩+진공을 만들고 z 밀도 프로파일을 뽑는 금속 표면 예제."),
    ("ex-04-cu-adsorption.html",  "examples/04-cu-adsorption.md", "예제 · E4",
        "Cu 표면 벤젠-에탄올 경쟁 흡착 응용 프로토콜의 입력 구성과 5단계 실행 흐름."),
    # === Applied: Cu surface adsorption ===
    ("cu-overview.html",          "cu/index.md",                 "APPLIED · OVERVIEW",
        "응용 시리즈 진입 — Cu(100)/Cu(111) 표면 위 벤젠-에탄올 경쟁 흡착 프로토콜 개요."),
    ("cu-01-system.html",         "cu/01-overview.md",           "APPLIED · CHAPTER 01",
        "벤젠과 에탄올의 화학적 배경, 슬랩 셀 기하, 표면 흡착 메커니즘."),
    ("cu-02-data-files.html",     "cu/02-data-files.md",         "APPLIED · CHAPTER 02",
        "opls.data 와 trappe.data 의 구조와 차이, 원자 종류 매핑."),
    ("cu-03-force-fields.html",   "cu/03-force-fields.md",       "APPLIED · CHAPTER 03",
        "OPLS-AA 와 TraPPE-UA 가 분자 거동에 미치는 영향 비교."),
    ("cu-04-electrostatics.html", "cu/04-electrostatics.md",     "APPLIED · CHAPTER 04",
        "PPPM 과 MSM 의 알고리즘 차이, 슬랩 계의 정전기 보정."),
    ("cu-05-protocol.html",       "cu/05-protocol.md",           "APPLIED · CHAPTER 05",
        "소프트 완화 → 최소화 → 가열 → 평형화 → 생성 동역학의 5단계 프로토콜."),
    ("cu-06-frameworks.html",     "cu/06-frameworks.md",         "APPLIED · CHAPTER 06",
        "힘장 × 정전기 조합 네 가지의 비교와 선택 기준."),
    ("cu-07-analysis.html",       "cu/07-analysis.md",           "APPLIED · CHAPTER 07",
        "RDF, 밀도 프로파일, 잉여 표면 흡착, 계면 장력의 정량 분석."),
    ("cu-08-troubleshooting.html","cu/08-troubleshooting.md",    "APPLIED · CHAPTER 08",
        "응용 시리즈에서 자주 마주치는 오류와 화학적 진단."),
]

# Sidebar nav grouping
NAV_SECTIONS = [
    ("입문 · 시작", [
        ("index.html",                "00", "개요"),
        ("01-getting-started.html",   "01", "시작하기"),
        ("02-input-structure.html",   "02", "입력 스크립트 구조"),
    ]),
    ("입문 · 시뮬레이션 만들기", [
        ("03-units-atomstyle.html",   "03", "단위계와 atom_style"),
        ("04-system.html",            "04", "시스템 정의"),
        ("05-forcefield.html",        "05", "상호작용 모델"),
        ("06-fix-run.html",           "06", "셋업과 실행"),
    ]),
    ("입문 · 결과와 운영", [
        ("07-output.html",            "07", "출력과 분석"),
        ("08-troubleshooting.html",   "08", "트러블슈팅"),
    ]),
    ("예제 · 따라 하기", [
        ("ex-01-lj-basic.html",       "E1", "LJ 액체 (NVE)"),
        ("ex-02-lj-demo.html",        "E2", "LJ 5단계 + RDF·MSD"),
        ("ex-03-cu-slab.html",        "E3", "Cu(100) 슬랩"),
        ("ex-04-cu-adsorption.html",  "E4", "Cu 벤젠-에탄올 흡착"),
    ]),
    ("응용 · Cu 표면 흡착", [
        ("cu-overview.html",          "A0", "개요"),
        ("cu-01-system.html",         "A1", "시스템 개요"),
        ("cu-02-data-files.html",     "A2", "데이터 파일"),
        ("cu-03-force-fields.html",   "A3", "힘장 비교"),
        ("cu-04-electrostatics.html", "A4", "정전기 방법"),
        ("cu-05-protocol.html",       "A5", "5단계 프로토콜"),
        ("cu-06-frameworks.html",     "A6", "4가지 프레임워크"),
        ("cu-07-analysis.html",       "A7", "분석 방법"),
        ("cu-08-troubleshooting.html","A8", "응용 트러블슈팅"),
    ]),
]


def render_sidebar(current: str) -> str:
    out = [
        '<aside class="sidebar">',
        '  <a href="../../" class="sidebar-back">← Donghwan KIM</a>',
        '  <a href="index.html" class="sidebar-brand">',
        '    <div class="brand-title">LAMMPS</div>',
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
            body = text[end + 4 :].lstrip("\n")
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


# just-the-docs source links → our flat filenames
LINK_FIX_MAP = {
    "docs/01-overview":      "cu-01-system.html",
    "docs/02-data-files":    "cu-02-data-files.html",
    "docs/03-force-fields":  "cu-03-force-fields.html",
    "docs/04-electrostatics":"cu-04-electrostatics.html",
    "docs/05-protocol":      "cu-05-protocol.html",
    "docs/06-frameworks":    "cu-06-frameworks.html",
    "docs/07-analysis":      "cu-07-analysis.html",
    "docs/08-troubleshooting":"cu-08-troubleshooting.html",
}


def fix_links(text: str) -> str:
    for src, dst in LINK_FIX_MAP.items():
        text = text.replace(f'href="{src}"', f'href="{dst}"')
    return text


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
    body_html = fix_links(body_html)
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
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
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
          <em>LAMMPS</em><br />
          <span class="hero-title-accent">한국어 입문 가이드</span>
        </h1>
        <p class="hero-tagline">{lede}</p>
        <div class="hero-meta">
          <span>대상 버전</span> 22 Jul 2024 이상 · <span>출발 예제</span> Lennard-Jones 액체 · <span>응용 시리즈</span> Cu 표면 흡착
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
            page_title_full = "LAMMPS 한국어 입문 가이드"
        elif out_name == "cu-overview.html":
            page_title_full = "응용 · Cu 표면 흡착 시리즈 개요 · LAMMPS 가이드"
        else:
            short = title_raw.split(". ", 1)[-1] if ". " in title_raw else title_raw
            page_title_full = f"{short} · LAMMPS 가이드"

        body_html, _toc = convert_body(body)

        if out_name == "index.html":
            header_html = HERO_TMPL.format(lede=html_lib.escape(lede))
        else:
            # for the cu series, the cu-overview hero stays page-header
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
