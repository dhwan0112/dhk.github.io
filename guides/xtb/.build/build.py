"""Build the xtb guide pages from fragments in .build/pages/<lang>/<name>.html.

Fragment front matter (HTML comment at the top):
    title, eyebrow, h1, lede   page header (omit h1 for pages that write their own hero)
    description                optional <meta name="description">; defaults to lede
The sidebar and prev/next links come from NAV below.
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NAV = {
    "ko": [
        ("시작", [("index", "00", "개요"), ("getting-started", "01", "설치와 실행")]),
        ("계산", [("calculations", "02", "단일점 · 최적화 · 진동수"), ("solvation", "03", "용매 모델")]),
        ("탐색", [("md", "04", "분자동역학 · 메타다이내믹스"), ("crest", "05", "CREST 컨포머 탐색")]),
        ("실전", [("workflow", "06", "예제: CREST에서 DFT까지")]),
    ],
    "en": [
        ("Start", [("index", "00", "Overview"), ("getting-started", "01", "Installing and running")]),
        ("Calculations", [("calculations", "02", "Single point · opt · freq"), ("solvation", "03", "Solvation")]),
        ("Sampling", [("md", "04", "MD · metadynamics"), ("crest", "05", "CREST conformer search")]),
        ("In practice", [("workflow", "06", "Example: CREST to DFT")]),
    ],
}
RELATED = {
    "ko": ("관련 가이드", "../../orca/ko/xtb.html", "ORCA 안에서 xTB 쓰기"),
    "en": ("Related", "../../orca/en/xtb.html", "xTB inside ORCA"),
}
TEXT = {
    "ko": {"suffix": "xtb 사용자 가이드", "brand": "사용자 가이드 · xtb 6.7 · CREST 3",
           "prev": "← 이전", "next": "다음 →", "top": "처음으로 ↑", "toc": "이 페이지에서 다루는 내용"},
    "en": {"suffix": "xtb User Guide", "brand": "User Guide · xtb 6.7 · CREST 3",
           "prev": "← previous", "next": "next →", "top": "back to top ↑", "toc": "On this page"},
}


def front_matter(path):
    s = open(path, encoding="utf-8").read()
    m = re.match(r"\s*<!--(.*?)-->\s*", s, re.S)
    meta = {}
    for line in m.group(1).strip().splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, s[m.end():]


def sidebar(lang, name):
    other = "en" if lang == "ko" else "ko"
    ko_cls = ' class="active"' if lang == "ko" else ""
    en_cls = ' class="active"' if lang == "en" else ""
    ko_href = f"{name}.html" if lang == "ko" else f"../ko/{name}.html"
    en_href = f"{name}.html" if lang == "en" else f"../en/{name}.html"
    out = ['<aside class="sidebar">',
           '  <a href="../../../" class="sidebar-back">← Donghwan KIM</a>',
           '  <div class="sidebar-lang">',
           f'    <a href="{ko_href}"{ko_cls}>KO</a>',
           f'    <a href="{en_href}"{en_cls}>EN</a>',
           '  </div>',
           '  <a href="index.html" class="sidebar-brand">',
           '    <div class="brand-title">xtb</div>',
           f'    <div class="brand-subtitle">{TEXT[lang]["brand"]}</div>',
           '  </a>', '', '  <nav>']
    for title, items in NAV[lang]:
        out += ['    <div class="nav-section">',
                f'      <div class="nav-section-title">{title}</div>',
                '      <ul class="nav-list">']
        for page, num, label in items:
            out.append(f'        <li><a href="{page}.html"><span class="nav-num">{num}</span>{label}</a></li>')
        out += ['      </ul>', '    </div>', '']
    title, href, label = RELATED[lang]
    out += ['    <div class="nav-section">',
            f'      <div class="nav-section-title">{title}</div>',
            '      <ul class="nav-list">',
            f'        <li><a href="{href}"><span class="nav-num">↗</span>{label}</a></li>',
            '      </ul>', '    </div>', '']
    out += ['  </nav>', '</aside>']
    return "\n".join(out)


def page_nav(lang, name):
    flat = [(p, lab) for _, items in NAV[lang] for p, _, lab in items]
    idx = [p for p, _ in flat].index(name)
    t = TEXT[lang]
    parts = []
    if idx > 0:
        p, lab = flat[idx - 1]
        parts.append(f'        <a class="prev" href="{p}.html">\n          <div class="page-nav-label">{t["prev"]}</div>\n'
                     f'          <div class="page-nav-title">{lab}</div>\n        </a>')
    if idx < len(flat) - 1:
        p, lab = flat[idx + 1]
        parts.append(f'        <a class="next" href="{p}.html">\n          <div class="page-nav-label">{t["next"]}</div>\n'
                     f'          <div class="page-nav-title">{lab}</div>\n        </a>')
    elif idx > 0:
        parts.append(f'        <a class="next" href="index.html">\n          <div class="page-nav-label">{t["top"]}</div>\n'
                     f'          <div class="page-nav-title">{flat[0][1]}</div>\n        </a>')
    return '      <nav class="page-nav">\n' + "\n".join(parts) + '\n      </nav>\n'


def build(lang, name):
    meta, body = front_matter(os.path.join(HERE, "pages", lang, f"{name}.html"))
    desc = meta.get("description") or re.sub(r"<[^>]+>", "", meta.get("lede", ""))
    title = meta["title"] if name != "index" else meta["title"]
    full_title = f"{title} · {TEXT[lang]['suffix']}" if name != "index" else title
    head = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{full_title}</title>
  <meta name="description" content="{html.escape(desc, quote=True)}" />
  <link rel="icon" type="image/x-icon" href="../../../images/icons/favicon.ico" />
  <script>try{{document.documentElement.setAttribute("data-theme",localStorage.getItem("theme")||"light")}}catch(e){{}}</script>
  <link rel="stylesheet" href="../assets/css/style.css" />
</head>
<body>
  <button class="mobile-nav-toggle">MENU</button>
  <div class="layout">
"""
    main = '    <main class="main">\n'
    if meta.get("h1"):
        main += ('      <header class="page-header">\n'
                 f'        <div class="page-eyebrow">{meta["eyebrow"]}</div>\n'
                 f'        <h1 class="page-title">{meta["h1"]}</h1>\n'
                 f'        <p class="page-lede">{meta["lede"]}</p>\n      </header>\n\n'
                 '      <article class="content">\n' + body.rstrip() + '\n      </article>\n\n')
    else:
        main += body.rstrip() + "\n\n"
    main += page_nav(lang, name) + '    </main>\n  </div>\n  <script src="../assets/js/main.js"></script>\n</body>\n</html>\n'
    os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
    out = os.path.join(ROOT, lang, f"{name}.html")
    open(out, "w", encoding="utf-8").write(head + sidebar(lang, name) + "\n\n" + main)
    print("wrote", os.path.relpath(out, ROOT))


for lang in NAV:
    for _, items in NAV[lang]:
        for page, _, _ in items:
            if os.path.exists(os.path.join(HERE, "pages", lang, f"{page}.html")):
                build(lang, page)
