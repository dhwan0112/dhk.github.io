"""Assemble ORCA guide pages from body fragments in .build/pages/<lang>/<name>.html.

Each fragment starts with a front-matter block:
    <!--
    title: ...
    eyebrow: ...
    h1: ...
    lede: ...
    prev: file.html | Title
    next: file.html | Title
    -->
The <head> and sidebar are copied from frequencies.html of the same language, so
nav changes made there carry over.
"""
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SUFFIX = {"ko": "ORCA 사용자 가이드", "en": "ORCA User Guide"}
LABEL = {"ko": ("← 이전", "다음 →"), "en": ("← previous", "next →")}


def meta_and_body(path):
    s = open(path, encoding="utf-8").read()
    m = re.match(r"\s*<!--(.*?)-->\s*", s, re.S)
    meta = {}
    for line in m.group(1).strip().splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, s[m.end():]


def build(lang, frag):
    name = os.path.splitext(os.path.basename(frag))[0]
    meta, body = meta_and_body(frag)
    tpl = open(os.path.join(ROOT, lang, "frequencies.html"), encoding="utf-8").read()
    head_side = tpl[:tpl.index('    <main class="main">')]
    head_side = re.sub(r"<title>.*?</title>",
                       f"<title>{meta['title']} · {SUFFIX[lang]}</title>", head_side)
    head_side = re.sub(r'(<meta name="description" content=")[^"]*(")',
                       lambda m: m.group(1) + re.sub(r"<[^>]+>", "", meta["lede"]) + m.group(2),
                       head_side)
    head_side = head_side.replace('href="frequencies.html" class="active"',
                                  f'href="{name}.html" class="active"')
    other = "en" if lang == "ko" else "ko"
    head_side = head_side.replace(f'href="../{other}/frequencies.html"',
                                  f'href="../{other}/{name}.html"')

    nav = []
    for cls, key, lab in (("prev", "prev", LABEL[lang][0]), ("next", "next", LABEL[lang][1])):
        if meta.get(key):
            href, _, t = (x.strip() for x in meta[key].partition("|"))
            nav.append(f'        <a class="{cls}" href="{href}">\n'
                       f'          <div class="page-nav-label">{lab}</div>\n'
                       f'          <div class="page-nav-title">{t}</div>\n        </a>')

    html = (head_side
            + '    <main class="main">\n      <header class="page-header">\n'
            + f'        <div class="page-eyebrow">{meta["eyebrow"]}</div>\n'
            + f'        <h1 class="page-title">{meta["h1"]}</h1>\n'
            + f'        <p class="page-lede">{meta["lede"]}</p>\n      </header>\n\n'
            + '      <article class="content">\n' + body.rstrip() + '\n      </article>\n\n'
            + '      <nav class="page-nav">\n' + "\n".join(nav) + '\n      </nav>\n'
            + '    </main>\n  </div>\n  <script src="../assets/js/main.js"></script>\n</body>\n</html>\n')
    out = os.path.join(ROOT, lang, f"{name}.html")
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", os.path.relpath(out, ROOT))


for lang in ("ko", "en"):
    for frag in sorted(glob.glob(os.path.join(HERE, "pages", lang, "*.html"))):
        build(lang, frag)
