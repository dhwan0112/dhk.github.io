"""Convert LAMMPS guide Markdown sources into ORCA-style standalone HTML pages.

Reads /tmp/lammps-src/*.md (just-the-docs flavour) and writes the
dhk.github.io/guides/lammps/*.html sub-site that reuses the ORCA guide
style sheet. Math equations are protected via placeholders so kramdown
attribute lists, Markdown italics and KaTeX delimiters do not collide
during conversion.
"""

from __future__ import annotations

import html as html_lib
import re
import shutil
from pathlib import Path

import markdown
import yaml

SRC = Path("C:/Users/denny/AppData/Local/Temp/lammps-src")
DST = Path("C:/Users/denny/Desktop/GitHub Pages/dhk.github.io/guides/lammps")
DST.mkdir(parents=True, exist_ok=True)

# (output_filename, source_filename, page_eyebrow, page_lede)
PAGES = [
    ("index.html",            "index.md",              None,
        "Cu(100)/Cu(111) 표면 위 벤젠-에탄올 경쟁 흡착의 분자동역학 시뮬레이션 프로토콜과 입력 파일 모음."),
    ("01-overview.html",      "01-overview.md",        "CHAPTER 01 · 시작",
        "벤젠과 에탄올의 화학적 배경, 슬랩 셀 기하, 표면 흡착 메커니즘을 정리합니다."),
    ("02-data-files.html",    "02-data-files.md",      "CHAPTER 02 · 시작",
        "opls.data 와 trappe.data 의 구조와 차이, 원자 종류 매핑 방법."),
    ("03-force-fields.html",  "03-force-fields.md",    "CHAPTER 03 · 이론",
        "OPLS-AA 와 TraPPE-UA 가 분자 거동에 미치는 영향을 비교합니다."),
    ("04-electrostatics.html","04-electrostatics.md",  "CHAPTER 04 · 이론",
        "PPPM 과 MSM 의 알고리즘 차이, 슬랩 계에서의 정전기 보정."),
    ("05-protocol.html",      "05-protocol.md",        "CHAPTER 05 · 실전",
        "소프트 완화 → 최소화 → 가열 → 평형화 → 생성 동역학의 5단계 프로토콜."),
    ("06-frameworks.html",    "06-frameworks.md",      "CHAPTER 06 · 실전",
        "힘장 × 정전기 방법의 네 가지 조합을 비교하고 선택 기준을 제시합니다."),
    ("07-analysis.html",      "07-analysis.md",        "CHAPTER 07 · 분석",
        "RDF, 밀도 프로파일, 잉여 표면 흡착, 계면 장력의 정량 분석 절차."),
    ("08-troubleshooting.html","08-troubleshooting.md","CHAPTER 08 · 운영",
        "자주 발생하는 LAMMPS 오류와 화학적 근원, 진단 명령어 모음."),
]

# Sidebar nav grouping (matches ORCA guide structure)
NAV_SECTIONS = [
    ("시작", [
        ("index.html",            "00", "개요"),
        ("01-overview.html",      "01", "시스템 개요"),
        ("02-data-files.html",    "02", "데이터 파일"),
    ]),
    ("이론과 방법론", [
        ("03-force-fields.html",  "03", "힘장 비교"),
        ("04-electrostatics.html","04", "정전기 방법"),
    ]),
    ("실전 프로토콜", [
        ("05-protocol.html",      "05", "5단계 프로토콜"),
        ("06-frameworks.html",    "06", "4가지 프레임워크"),
    ]),
    ("분석과 운영", [
        ("07-analysis.html",      "07", "분석 방법"),
        ("08-troubleshooting.html","08","트러블슈팅"),
    ]),
]


def render_sidebar(current: str) -> str:
    out = [
        '<aside class="sidebar">',
        '  <a href="index.html" class="sidebar-brand">',
        '    <div class="brand-title">LAMMPS</div>',
        '    <div class="brand-subtitle">Cu 표면 흡착 가이드</div>',
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


def convert_body(md_body: str) -> tuple[str, str]:
    """Return (html_body, toc_inner_html). Prepends a styled TOC component
    when the source contained a kramdown {:toc} block."""
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
          <span class="hero-title-accent">Cu 표면 흡착 가이드</span>
        </h1>
        <p class="hero-tagline">{lede}</p>
        <div class="hero-meta">
          <span>대상</span> Cu(100) · Cu(111) · <span>힘장</span> OPLS-AA · TraPPE-UA · <span>정전기</span> PPPM · MSM
        </div>
      </section>"""

PAGE_HEADER_TMPL = """      <header class="page-header">
        <div class="page-eyebrow">{eyebrow}</div>
        <h1 class="page-title">{title}</h1>
        <p class="page-lede">{lede}</p>
      </header>"""


def main():
    for out_name, src_name, eyebrow, lede in PAGES:
        src_path = SRC / src_name
        text = src_path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)

        title_raw = fm.get("title", "") or ""
        title_clean = str(title_raw).strip()
        if out_name == "index.html":
            page_title_full = "LAMMPS Cu 표면 흡착 가이드 · 한국어"
        else:
            page_title_full = f"{title_clean} · LAMMPS Cu 표면 흡착 가이드"

        body_html, _toc = convert_body(body)

        if out_name == "index.html":
            header_html = HERO_TMPL.format(lede=html_lib.escape(lede))
        else:
            header_html = PAGE_HEADER_TMPL.format(
                eyebrow=html_lib.escape(eyebrow),
                title=html_lib.escape(title_clean.split(". ", 1)[-1] if ". " in title_clean else title_clean),
                lede=html_lib.escape(lede),
            )

        html_out = HEAD_TMPL.format(
            title=html_lib.escape(page_title_full),
            description=html_lib.escape(lede),
            sidebar=render_sidebar(out_name),
            header=header_html,
            body=body_html,
            page_nav=render_page_nav(out_name),
        )

        (DST / out_name).write_text(html_out, encoding="utf-8")
        print(f"wrote {out_name}  ({len(body_html):>6} bytes body)")


if __name__ == "__main__":
    main()
