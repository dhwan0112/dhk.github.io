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
        "실리콘 SCF 한 예제부터 반강자성 FeO의 DFT+U까지, pw.x 중심의 제일원리 계산을 단계별로 풉니다."),
    # === 입문 · 시작 ===
    ("01-getting-started.html", "chapters/01-getting-started.md", "CHAPTER 01 · 입문 · 시작",
        "평면파 DFT의 큰 그림, 설치 경로 선택(conda/소스), 설치 검증, 유사퍼텐셜 확보."),
    ("02-input-structure.html", "chapters/02-input-structure.md", "CHAPTER 02 · 입문 · 시작",
        "pw.x 입력의 네임리스트(&CONTROL/&SYSTEM/&ELECTRONS)와 카드 문법, 최소 입력 해부."),
    ("03-units-coordinates.html", "chapters/03-units-coordinates.md", "CHAPTER 03 · 입문 · 시작",
        "Rydberg 원자단위, ibrav와 celldm, alat·crystal·angstrom 좌표 규약과 흔한 함정."),
    # === 입문 · 핵심 개념 ===
    ("04-pseudopotentials.html", "chapters/04-pseudopotentials.md", "CHAPTER 04 · 입문 · 핵심 개념",
        "NC/US/PAW 유사퍼텐셜의 차이, PSlibrary·SSSP에서 고르는 법, 파일이 요구하는 컷오프 읽기."),
    ("05-convergence.html", "chapters/05-convergence.md", "CHAPTER 05 · 입문 · 핵심 개념",
        "ecutwfc·ecutrho·k점 수렴 테스트의 표준 절차, 수렴 판단에서 흔한 오해."),
    ("06-occupations.html", "chapters/06-occupations.md", "CHAPTER 06 · 입문 · 핵심 개념",
        "절연체와 금속의 occupations 선택, smearing 종류와 degauss, 실측 스캔."),
    ("07-scf-control.html", "chapters/07-scf-control.md", "CHAPTER 07 · 입문 · 핵심 개념",
        "SCF 순환의 구조, mixing_beta·mixing_mode·diagonalization, 수렴 실패 진단 순서."),
    # === 입문 · 계산 종류 ===
    ("08-scf-nscf.html", "chapters/08-scf-nscf.md", "CHAPTER 08 · 입문 · 계산 종류",
        "자기일관(scf)과 비자기일관(nscf/bands) 계산의 역할 분담, 출력 파일 읽는 법."),
    ("09-relaxation.html", "chapters/09-relaxation.md", "CHAPTER 09 · 입문 · 계산 종류",
        "힘과 응력, relax/vc-relax, BFGS, &IONS·&CELL, 수렴 기준과 vc-relax 후 재계산."),
    ("10-dos-bands.html", "chapters/10-dos-bands.md", "CHAPTER 10 · 입문 · 계산 종류",
        "dos.x·projwfc.x·bands.x 후처리 파이프라인, 갭 읽기와 PDOS 해석."),
    ("11-postprocessing.html", "chapters/11-postprocessing.md", "CHAPTER 11 · 입문 · 계산 종류",
        "pp.x의 plot_num, 전하밀도·퍼텐셜 추출, 큐브 파일과 시각화 도구."),
    # === 심화 · 자성과 강상관 ===
    ("12-magnetism.html", "chapters/12-magnetism.md", "CHAPTER 12 · 심화 · 자성과 강상관",
        "nspin·starting_magnetization, FM/AFM 초기화 요령, bcc Fe와 FeO 실측."),
    ("13-dft-plus-u.html", "chapters/13-dft-plus-u.md", "CHAPTER 13 · 심화 · 자성과 강상관",
        "자기상호작용 오류와 DFT+U, v7.1+ HUBBARD 카드 문법, FeO에서 갭이 열리는 이유."),
    ("14-hubbard-hp.html", "chapters/14-hubbard-hp.md", "CHAPTER 14 · 심화 · 자성과 강상관",
        "선형 응답 이론으로 U를 제일원리 계산하는 hp.x 워크플로와 수렴 파라미터."),
    # === 심화 · 응용과 운영 ===
    ("15-surfaces.html", "chapters/15-surfaces.md", "CHAPTER 15 · 심화 · 응용과 운영",
        "슬랩 모델 만들기, 쌍극자 보정, 평면평균 퍼텐셜과 일함수."),
    ("16-molecular-dynamics.html", "chapters/16-molecular-dynamics.md", "CHAPTER 16 · 심화 · 응용과 운영",
        "Born-Oppenheimer MD, 온도조절(SVR), ML 퍼텐셜 학습 데이터 샘플링의 출발점."),
    ("17-phonons-neb.html", "chapters/17-phonons-neb.md", "CHAPTER 17 · 심화 · 응용과 운영",
        "ph.x 포논과 neb.x 반응 경로의 큰 그림 — 언제 필요하고 어디서 시작하는지."),
    ("18-parallel-hpc.html", "chapters/18-parallel-hpc.md", "CHAPTER 18 · 심화 · 응용과 운영",
        "-nk/-nd/-ni 병렬화 레벨, 작은 계와 큰 계의 스케일링 감각, HPC 운영 습관."),
    # === 레퍼런스 ===
    ("ref-keywords.html", "ref/ref-keywords.md", "레퍼런스 · R1",
        "네임리스트별 주요 변수를 찾아보는 사전. &CONTROL부터 &CELL까지."),
    ("ref-cards.html", "ref/ref-cards.md", "레퍼런스 · R2",
        "pw.x 카드(ATOMIC_*, K_POINTS, CELL_PARAMETERS, HUBBARD)의 문법과 옵션."),
    ("ref-errors.html", "ref/ref-errors.md", "레퍼런스 · R3",
        "증상 → 원인 → 해결 순서의 오류 사전과 '에러 없이 틀리는 경우' 점검표."),
    ("ref-executables.html", "ref/ref-executables.md", "레퍼런스 · R4",
        "QE 스위트 실행 파일 목록과 각각의 입력 네임리스트·입출력 요약."),
    # === 예제 · 따라 하기 ===
    ("ex-01-si-scf.html", "examples/01-si-scf.md", "예제 · E1",
        "가장 단순한 실리콘 SCF를 한 번 돌리고 출력의 모든 블록을 읽어보는 첫 예제."),
    ("ex-02-si-ibrav0.html", "examples/02-si-ibrav0.md", "예제 · E2",
        "같은 결정을 ibrav=0 + CELL_PARAMETERS로 다시 정의해 두 표현의 등가성을 확인합니다."),
    ("ex-03-convergence.html", "examples/03-convergence.md", "예제 · E3",
        "ecutwfc·k점·힘 수렴 테스트를 셸 스크립트로 자동화하는 표준 절차."),
    ("ex-04-o2-molecule.html", "examples/04-o2-molecule.md", "예제 · E4",
        "고립계 보정과 스핀 고정으로 O₂ 삼중항 분자를 계산하고 결합 에너지를 구합니다."),
    ("ex-05-al-metal.html", "examples/05-al-metal.md", "예제 · E5",
        "금속 fcc Al의 smearing SCF, 페르미 준위, degauss 선택의 실측 근거."),
    ("ex-06-si-vcrelax.html", "examples/06-si-vcrelax.md", "예제 · E6",
        "셀까지 함께 푸는 vc-relax로 실리콘 평형 격자상수를 찾습니다."),
    ("ex-07-si-dos.html", "examples/07-si-dos.md", "예제 · E7",
        "scf → nscf → dos.x → projwfc.x 상태밀도 파이프라인과 Löwdin 전하."),
    ("ex-08-si-bands.html", "examples/08-si-bands.md", "예제 · E8",
        "고대칭 경로를 따라 실리콘 밴드 구조를 계산하고 간접 갭을 읽습니다."),
    ("ex-09-fe-bcc.html", "examples/09-fe-bcc.md", "예제 · E9",
        "스핀 편극 SCF로 bcc Fe의 강자성 바닥상태와 자기모멘트를 계산합니다."),
    ("ex-10-feo-afm.html", "examples/10-feo-afm.md", "예제 · E10",
        "반강자성 FeO를 GGA로 계산하면 무엇이 틀리는지 직접 확인합니다."),
    ("ex-11-feo-hubbard.html", "examples/11-feo-hubbard.md", "예제 · E11",
        "HUBBARD 카드로 U를 켜 Hubbard 분리를 실측하고, 이상적 큐빅 셀의 유명한 함정까지 진단합니다."),
    ("ex-12-feo-hp.html", "examples/12-feo-hp.md", "예제 · E12",
        "경험 파라미터 없이 hp.x 선형 응답으로 U를 제일원리 계산합니다."),
    ("ex-13-slab-md.html", "examples/13-slab-md.md", "예제 · E13",
        "슬랩 생성과 일함수, 그리고 ML 퍼텐셜 학습 데이터 샘플링의 출발점인 BOMD."),
]

# Sidebar nav grouping (STRUCTURE.md 3절 그대로)
NAV_SECTIONS = [
    ("입문 · 시작", [
        ("index.html",              "00", "개요"),
        ("01-getting-started.html", "01", "시작하기"),
        ("02-input-structure.html", "02", "입력 파일 구조"),
        ("03-units-coordinates.html", "03", "단위계와 좌표계"),
    ]),
    ("입문 · 핵심 개념", [
        ("04-pseudopotentials.html", "04", "유사퍼텐셜"),
        ("05-convergence.html",      "05", "컷오프와 k-점 수렴"),
        ("06-occupations.html",      "06", "점유수와 smearing"),
        ("07-scf-control.html",      "07", "SCF 수렴 제어"),
    ]),
    ("입문 · 계산 종류", [
        ("08-scf-nscf.html",       "08", "SCF와 NSCF"),
        ("09-relaxation.html",     "09", "구조 최적화"),
        ("10-dos-bands.html",      "10", "상태밀도와 밴드"),
        ("11-postprocessing.html", "11", "전하밀도와 퍼텐셜"),
    ]),
    ("심화 · 자성과 강상관", [
        ("12-magnetism.html",  "12", "스핀 편극과 자성"),
        ("13-dft-plus-u.html", "13", "DFT+U와 HUBBARD 카드"),
        ("14-hubbard-hp.html", "14", "hp.x 로 U 계산하기"),
    ]),
    ("심화 · 응용과 운영", [
        ("15-surfaces.html",           "15", "표면·슬랩과 일함수"),
        ("16-molecular-dynamics.html", "16", "분자동역학"),
        ("17-phonons-neb.html",        "17", "포논과 반응 경로"),
        ("18-parallel-hpc.html",       "18", "병렬 실행과 HPC 운영"),
    ]),
    ("레퍼런스", [
        ("ref-keywords.html",    "R1", "키워드 사전"),
        ("ref-cards.html",       "R2", "카드 레퍼런스"),
        ("ref-errors.html",      "R3", "오류 메시지 사전"),
        ("ref-executables.html", "R4", "실행 파일 목록"),
    ]),
    ("예제 · 따라 하기", [
        ("ex-01-si-scf.html",       "E1",  "Si SCF"),
        ("ex-02-si-ibrav0.html",    "E2",  "ibrav=0 다시 쓰기"),
        ("ex-03-convergence.html",  "E3",  "수렴 테스트 자동화"),
        ("ex-04-o2-molecule.html",  "E4",  "O₂ 분자 (삼중항)"),
        ("ex-05-al-metal.html",     "E5",  "fcc Al 금속"),
        ("ex-06-si-vcrelax.html",   "E6",  "Si vc-relax"),
        ("ex-07-si-dos.html",       "E7",  "Si DOS·PDOS"),
        ("ex-08-si-bands.html",     "E8",  "Si 밴드 구조"),
        ("ex-09-fe-bcc.html",       "E9",  "bcc Fe 강자성"),
        ("ex-10-feo-afm.html",      "E10", "FeO AFM (GGA 실패)"),
        ("ex-11-feo-hubbard.html",  "E11", "FeO DFT+U"),
        ("ex-12-feo-hp.html",       "E12", "hp.x 로 U 계산"),
        ("ex-13-slab-md.html",      "E13", "슬랩과 AIMD"),
    ]),
]


def render_sidebar(current: str) -> str:
    out = [
        '<aside class="sidebar">',
        '  <a href="../../" class="sidebar-back">← Donghwan KIM</a>',
        '  <a href="index.html" class="sidebar-brand">',
        '    <div class="brand-title">Quantum ESPRESSO</div>',
        '    <div class="brand-subtitle">한국어 가이드</div>',
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
          <span class="hero-title-accent">한국어 가이드</span>
        </h1>
        <p class="hero-tagline">{lede}</p>
        <div class="hero-meta">
          <span>대상 버전</span> QE 7.5 · <span>출발 예제</span> Si SCF · <span>응용 시리즈</span> Fe–O 산화물
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
            page_title_full = "Quantum ESPRESSO 한국어 가이드"
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
        print(f"wrote {out_name:<28}  ({len(body_html):>6} bytes body)")


if __name__ == "__main__":
    main()
