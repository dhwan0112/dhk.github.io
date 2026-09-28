"""Build the shell scripting guide pages from fragments in .build/pages/<lang>/<name>.html.

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

BRAND = "Shell"
NAV = {
    "ko": [
        ("시작", [("index", "00", "개요"), ("basics", "01", "첫 스크립트")]),
        ("문법", [("control", "02", "조건과 반복"), ("functions", "03", "함수와 인자"),
                ("robust", "04", "안전한 스크립트")]),
        ("텍스트 처리", [("text", "05", "grep · sed · awk"), ("extract", "06", "출력 파일에서 값 뽑기")]),
        ("작업 제출", [("batch", "07", "PBS · Slurm 작업 스크립트"), ("arrays", "08", "작업 배열과 파라미터 스윕")]),
        ("참고", [("cheatsheet", "09", "치트시트")]),
    ],
    "en": [
        ("Start", [("index", "00", "Overview"), ("basics", "01", "Your first script")]),
        ("Syntax", [("control", "02", "Conditions and loops"), ("functions", "03", "Functions and arguments"),
                    ("robust", "04", "Writing safer scripts")]),
        ("Text processing", [("text", "05", "grep · sed · awk"), ("extract", "06", "Pulling numbers from outputs")]),
        ("Job submission", [("batch", "07", "PBS · Slurm job scripts"), ("arrays", "08", "Job arrays and parameter sweeps")]),
        ("Reference", [("cheatsheet", "09", "Cheat sheet")]),
    ],
}
TEXT = {
    "ko": {"suffix": "셸 스크립팅 가이드", "brand": "스크립팅 가이드 · bash",
           "prev": "← 이전", "next": "다음 →", "top": "처음으로 ↑", "toc": "이 페이지에서 다루는 내용"},
    "en": {"suffix": "Shell Scripting Guide", "brand": "Scripting guide · bash",
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
           f'    <div class="brand-title">{BRAND}</div>',
           f'    <div class="brand-subtitle">{TEXT[lang]["brand"]}</div>',
           '  </a>', '', '  <nav>']
    for title, items in NAV[lang]:
        out += ['    <div class="nav-section">',
                f'      <div class="nav-section-title">{title}</div>',
                '      <ul class="nav-list">']
        for page, num, label in items:
            out.append(f'        <li><a href="{page}.html"><span class="nav-num">{num}</span>{label}</a></li>')
        out += ['      </ul>', '    </div>', '']
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
