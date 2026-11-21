"""Checks for the Fortran guide under fortran/ and its examples under examples/fortran/.

Usage:
  python3 tools/fortran_guide.py lint
  python3 tools/fortran_guide.py examples
  python3 tools/fortran_guide.py site SITE_DIR
  python3 tools/fortran_guide.py all [SITE_DIR]

lint      front matter, permalinks, fences and their markers, links, glossary terms.
examples  compiles every example with FC (default gfortran) and BASE_FLAGS, runs it,
          and compares the result with the sidecar files next to it.
site      checks a built site: every chapter page exists and every internal link
          on the guide pages resolves to a file.

Sidecar files next to examples/fortran/chNN/NAME.f90 (or NAME.f):
  NAME.out            expected standard output; the program must exit with status 0
  NAME.in             standard input for the run
  NAME.flags          extra compiler arguments, appended after the source file
  NAME.warning        one expected warning text per line; any other warning fails
  NAME.compile-error  text that must appear in the compiler output of a failed compile
  NAME.run-error      text that must appear in stderr of a run that exits non-zero

Exit status is 0 when every check passes and 1 otherwise.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "fortran"
IMAGES = GUIDE / "images"
EXAMPLES = ROOT / "examples" / "fortran"
GLOSSARY = ROOT / "docs" / "fortran-guide-glossary.md"
DECISIONS = ROOT / "docs" / "fortran-guide-decisions.md"

BASE_FLAGS = ["-std=f2018", "-Wall", "-Wextra"]
FRONT_MATTER_KEYS = {"title", "order", "permalink"}
FENCE_LANGUAGES = {"fortran", "sh", "text"}
SOURCE_SUFFIXES = (".f90", ".f")
SIDECAR_SUFFIXES = (".out", ".in", ".flags", ".warning", ".compile-error", ".run-error")
RUN_TIMEOUT_SECONDS = 20

CHAPTER_FILE = re.compile(r"^(?P<nn>\d\d)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
MARKER = re.compile(r"^<!-- (?P<kind>file|excerpt|output): (?P<path>ch(?P<nn>\d\d)/[A-Za-z0-9_-]+\.(?:f90|f|out)) -->$")
LOOSE_MARKER = re.compile(r"^<!--\s*(file|excerpt|output)\s*:")
FENCE = re.compile(r"^```(?P<lang>\S*)\s*$")
GUIDE_LINK = re.compile(r"\]\((?P<target>/fortran/[^)\s]*)\)")
IMAGE_LINK = re.compile(r"!\[[^\]]*\]\((?P<target>[^)\s]+)\)")
ENGINE_SYNTAX = re.compile(r"\{%|\{\{|\{:|<script", re.IGNORECASE)
INLINE_CODE = re.compile(r"`[^`]*`")
HREF = re.compile(r"""(?:href|src)="(?P<url>[^"#?]*)[^"]*\"""")
WARNING_LINE = re.compile(r"^Warning: (?P<text>.*)$", re.MULTILINE)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def note(self, message: str) -> None:
        self.notes.append(message)


@dataclass
class Fence:
    lang: str
    start: int
    lines: list[str]
    marker_kind: str | None
    marker_path: str | None


@dataclass
class Chapter:
    path: Path
    front: dict[str, str]
    body: list[str]
    body_start: int
    order: int = 0
    fences: list[Fence] = field(default_factory=list)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_front_matter(path: Path, report: Report) -> Chapter | None:
    lines = path.read_text(encoding="utf-8").split("\n")
    if not lines or lines[0] != "---":
        report.error(rel(path), "must start with a '---' front matter line")
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        report.error(rel(path), "front matter is not closed with '---'")
        return None
    front: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        key, sep, value = line.partition(":")
        if not sep:
            report.error(f"{rel(path)}:{number}", "front matter lines must be 'key: value'")
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        front[key.strip()] = value
    return Chapter(path=path, front=front, body=lines[end + 1:], body_start=end + 2)


def check_front_matter(chapter: Chapter, report: Report) -> None:
    where = rel(chapter.path)
    keys = set(chapter.front)
    if keys != FRONT_MATTER_KEYS:
        report.error(where, f"front matter keys must be exactly {sorted(FRONT_MATTER_KEYS)}, found {sorted(keys)}")
    order_text = chapter.front.get("order", "")
    if not order_text.isdigit():
        report.error(where, f"order must be a positive integer, found {order_text!r}")
        return
    chapter.order = int(order_text)
    permalink = chapter.front.get("permalink", "")
    name = chapter.path.name
    if name == "index.md":
        if chapter.order != 1:
            report.error(where, "index.md is the preface and must have order 1")
        if permalink != "/fortran/":
            report.error(where, f"index.md permalink must be /fortran/, found {permalink!r}")
        return
    match = CHAPTER_FILE.match(name)
    if not match:
        report.error(where, "chapter file names must look like NN-slug.md with a lowercase ASCII slug")
        return
    if int(match["nn"]) != chapter.order:
        report.error(where, f"file number {match['nn']} does not match order {chapter.order}")
    expected = f"/fortran/{chapter.path.stem}/"
    if permalink != expected:
        report.error(where, f"permalink must be {expected} (the address is fixed by the file name), found {permalink!r}")


def collect_fences(chapter: Chapter, report: Report) -> None:
    body = chapter.body
    index = 0
    pending: tuple[str, str, int] | None = None
    while index < len(body):
        line = body[index]
        number = chapter.body_start + index
        where = f"{rel(chapter.path)}:{number}"
        marker = MARKER.match(line)
        if marker:
            if pending:
                report.error(f"{rel(chapter.path)}:{pending[2]}", "marker is not followed by a fenced block")
            pending = (marker["kind"], marker["path"], number)
            if int(marker["nn"]) != chapter.order:
                report.error(where, f"marker points to ch{marker['nn']} but this chapter has order {chapter.order}; keep examples in examples/fortran/ch{chapter.order:02d}/")
            index += 1
            continue
        if LOOSE_MARKER.match(line):
            report.error(where, "malformed marker; write exactly '<!-- file: chNN/name.f90 -->', '<!-- excerpt: ... -->' or '<!-- output: chNN/name.out -->'")
        fence = FENCE.match(line)
        if not fence:
            if pending and line.strip():
                report.error(f"{rel(chapter.path)}:{pending[2]}", "marker must be on the line right before the fence")
                pending = None
            index += 1
            continue
        lang = fence["lang"]
        content: list[str] = []
        index += 1
        while index < len(body) and body[index].rstrip() != "```":
            content.append(body[index])
            index += 1
        if index >= len(body):
            report.error(where, "fenced block is not closed")
            return
        kind, path = (pending[0], pending[1]) if pending else (None, None)
        chapter.fences.append(Fence(lang=lang, start=number, lines=content, marker_kind=kind, marker_path=path))
        pending = None
        index += 1
    if pending:
        report.error(f"{rel(chapter.path)}:{pending[2]}", "marker is not followed by a fenced block")


def check_fences(chapter: Chapter, report: Report, referenced: set[str]) -> None:
    for fence in chapter.fences:
        where = f"{rel(chapter.path)}:{fence.start}"
        if fence.lang not in FENCE_LANGUAGES:
            report.error(where, f"fence language must be one of {sorted(FENCE_LANGUAGES)}, found {fence.lang!r}")
            continue
        if fence.lang == "fortran" and fence.marker_kind not in ("file", "excerpt"):
            report.error(where, "every fortran block needs '<!-- file: chNN/name.f90 -->' or '<!-- excerpt: chNN/name.f90 -->' on the line before it")
            continue
        if fence.lang == "sh" and fence.marker_kind:
            report.error(where, "sh blocks are commands, not examples; remove the marker")
            continue
        if fence.lang == "text" and fence.marker_kind not in (None, "output"):
            report.error(where, "a text block can only carry an output marker")
            continue
        if fence.lang == "fortran" and fence.marker_path.endswith(".out"):
            report.error(where, "a fortran block must point to a source file, not an .out file")
            continue
        if fence.lang == "text" and fence.marker_kind == "output" and not fence.marker_path.endswith(".out"):
            report.error(where, "an output marker must point to an .out file")
            continue
        if not fence.marker_kind:
            continue
        target = EXAMPLES / fence.marker_path
        if not target.is_file():
            report.error(where, f"{rel(target)} does not exist")
            continue
        file_lines = [line.rstrip() for line in target.read_text(encoding="utf-8").rstrip("\n").split("\n")]
        block = [line.rstrip() for line in fence.lines]
        while block and not block[-1].strip():
            block.pop()
        if fence.marker_kind in ("file", "output"):
            if block != file_lines:
                report.error(where, f"block differs from {rel(target)}; copy the file into the block or fix the file")
            if fence.marker_kind == "file":
                referenced.add(fence.marker_path)
        elif not contains_run(file_lines, block):
            report.error(where, f"excerpt is not a contiguous run of lines in {rel(target)}")


def contains_run(haystack: list[str], needle: list[str]) -> bool:
    if not needle:
        return False
    width = len(needle)
    return any(haystack[i:i + width] == needle for i in range(len(haystack) - width + 1))


def prose_lines(chapter: Chapter):
    fenced = set()
    for fence in chapter.fences:
        fenced.update(range(fence.start, fence.start + len(fence.lines) + 2))
    for offset, line in enumerate(chapter.body):
        number = chapter.body_start + offset
        if number not in fenced:
            yield number, line


def check_prose(chapter: Chapter, report: Report, permalinks: set[str], avoid: dict[str, str]) -> None:
    for number, line in prose_lines(chapter):
        where = f"{rel(chapter.path)}:{number}"
        if ENGINE_SYNTAX.search(line):
            report.error(where, "engine-specific syntax ({%, {{, {:, <script) is not allowed; the layout handles navigation")
        for match in GUIDE_LINK.finditer(line):
            target = match["target"]
            if target.startswith("/fortran/images/"):
                continue
            page = target.split("#", 1)[0]
            if page not in permalinks:
                report.error(where, f"link {target} does not match any chapter permalink")
        for match in IMAGE_LINK.finditer(line):
            target = match["target"]
            if not target.startswith("/fortran/images/"):
                report.error(where, f"images must live in /fortran/images/, found {target}")
            elif not (IMAGES / target.removeprefix("/fortran/images/")).is_file():
                report.error(where, f"image {target} does not exist")
        text = INLINE_CODE.sub("", line)
        for wrong, right in avoid.items():
            if wrong in text:
                report.error(where, f"glossary: write '{right}' instead of '{wrong}'")


def read_glossary(report: Report) -> dict[str, str]:
    if not GLOSSARY.is_file():
        report.error(rel(GLOSSARY), "glossary file is missing")
        return {}
    avoid: dict[str, str] = {}
    rows = [line for line in GLOSSARY.read_text(encoding="utf-8").split("\n") if line.startswith("|")]
    for line in rows[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 3:
            report.error(rel(GLOSSARY), f"row needs three columns: {line}")
            continue
        for wrong in filter(None, (term.strip() for term in cells[2].split(","))):
            avoid[wrong] = cells[1]
    return avoid


def load_chapters(report: Report) -> list[Chapter]:
    chapters = []
    for path in sorted(GUIDE.glob("*.md")):
        chapter = read_front_matter(path, report)
        if chapter:
            check_front_matter(chapter, report)
            chapters.append(chapter)
    if not chapters:
        report.error(rel(GUIDE), "no chapters found")
        return chapters
    orders = sorted(chapter.order for chapter in chapters)
    if orders != list(range(1, len(orders) + 1)):
        report.error(rel(GUIDE), f"orders must run 1..{len(orders)} without gaps or repeats, found {orders}")
    return chapters


def example_sources() -> list[Path]:
    return sorted(p for p in EXAMPLES.rglob("*") if p.is_file() and p.suffix in SOURCE_SUFFIXES)


def check_example_tree(report: Report, referenced: set[str]) -> None:
    for path in sorted(p for p in EXAMPLES.rglob("*") if p.is_file()):
        name = rel(path)
        if path.parent.parent != EXAMPLES or not re.fullmatch(r"ch\d\d", path.parent.name):
            report.error(name, "examples must sit directly in examples/fortran/chNN/")
            continue
        if path.suffix in SOURCE_SUFFIXES:
            key = path.relative_to(EXAMPLES).as_posix()
            if key not in referenced:
                report.error(name, "example is not shown in any chapter; add a '<!-- file: ... -->' block or delete it")
            continue
        if path.name.endswith(SIDECAR_SUFFIXES):
            stem = path.name
            for suffix in SIDECAR_SUFFIXES:
                if stem.endswith(suffix):
                    stem = stem[: -len(suffix)]
                    break
            if not any((path.parent / (stem + s)).is_file() for s in SOURCE_SUFFIXES):
                report.error(name, "sidecar has no matching .f90 or .f source")
            continue
        report.error(name, f"unexpected file; allowed are sources {SOURCE_SUFFIXES} and sidecars {SIDECAR_SUFFIXES}")


def lint(report: Report) -> None:
    chapters = load_chapters(report)
    avoid = read_glossary(report)
    permalinks = {chapter.front.get("permalink", "") for chapter in chapters}
    referenced: set[str] = set()
    for chapter in chapters:
        collect_fences(chapter, report)
        check_fences(chapter, report, referenced)
        check_prose(chapter, report, permalinks, avoid)
    check_example_tree(report, referenced)
    report.note(f"lint: {len(chapters)} chapters, {sum(len(c.fences) for c in chapters)} fenced blocks, {len(referenced)} example files shown")


def sidecar(source: Path, suffix: str) -> Path:
    return source.with_suffix(suffix)


def read_optional(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.is_file() else None


def run_examples(report: Report) -> None:
    compiler = os.environ.get("FC", "gfortran")
    if not shutil.which(compiler):
        report.error("examples", f"compiler {compiler!r} not found; nothing was checked")
        return
    version = subprocess.run([compiler, "--version"], capture_output=True, text=True).stdout.split("\n")[0]
    report.note(f"examples: {version}")
    decisions = read_optional(DECISIONS) or ""
    compiled = ran = expected_failures = 0
    sources = example_sources()
    if not sources:
        report.error("examples", "no example sources found")
        return
    for source in sources:
        key = source.relative_to(EXAMPLES).as_posix()
        extra = (read_optional(sidecar(source, ".flags")) or "").split()
        compile_error = read_optional(sidecar(source, ".compile-error"))
        warnings_expected = [w for w in (read_optional(sidecar(source, ".warning")) or "").split("\n") if w.strip()]
        expected_out = read_optional(sidecar(source, ".out"))
        run_error = read_optional(sidecar(source, ".run-error"))
        stdin_text = read_optional(sidecar(source, ".in"))
        with tempfile.TemporaryDirectory() as work:
            exe = Path(work) / "a.out"
            built = subprocess.run([compiler, *BASE_FLAGS, str(source), "-o", str(exe), *extra], capture_output=True, text=True, cwd=work)
            log = built.stdout + built.stderr
            if compile_error is not None:
                if built.returncode == 0:
                    report.error(key, "expected the compile to fail, but it succeeded")
                elif compile_error.strip() not in log:
                    report.error(key, f"compile failed without the expected text {compile_error.strip()!r}:\n{log}")
                else:
                    expected_failures += 1
                continue
            if built.returncode != 0:
                report.error(key, f"compile failed:\n{log}")
                continue
            compiled += 1
            seen = [m["text"] for m in WARNING_LINE.finditer(log)]
            unexpected = [w for w in seen if not any(e in w for e in warnings_expected)]
            missing = [e for e in warnings_expected if not any(e in w for w in seen)]
            for text in unexpected:
                report.error(key, f"unexpected warning: {text}")
            for text in missing:
                report.error(key, f".warning lists {text!r} but the compiler did not print it")
            if warnings_expected and key not in decisions:
                report.error(key, f"kept warnings must be explained in {rel(DECISIONS)}; mention {key} there")
            if expected_out is None and run_error is None:
                report.error(key, "add NAME.out (expected output) or NAME.run-error (expected runtime error)")
                continue
            try:
                result = subprocess.run([str(exe)], input=stdin_text or "", capture_output=True, text=True, cwd=work, timeout=RUN_TIMEOUT_SECONDS)
            except subprocess.TimeoutExpired:
                report.error(key, f"run did not finish within {RUN_TIMEOUT_SECONDS} s")
                continue
            ran += 1
            if run_error is not None:
                if result.returncode == 0:
                    report.error(key, "expected the run to fail, but it exited with status 0")
                elif run_error.strip() not in result.stderr:
                    report.error(key, f"run failed without the expected text {run_error.strip()!r}:\n{result.stderr}")
                continue
            if result.returncode != 0:
                report.error(key, f"run exited with status {result.returncode}:\n{result.stderr}")
            elif result.stdout != expected_out:
                report.error(key, f"output differs from {key.rsplit('.', 1)[0]}.out:\n--- expected\n{expected_out}--- got\n{result.stdout}")
    report.note(f"examples: {len(sources)} sources, {compiled} compiled, {ran} ran, {expected_failures} failed to compile as expected")


def check_site(site: Path, report: Report) -> None:
    chapters = load_chapters(Report())
    for chapter in chapters:
        page = site / chapter.front.get("permalink", "").strip("/") / "index.html"
        if not page.is_file():
            report.error(rel_site(site, page), "chapter page was not built")
    pages = sorted((site / "fortran").rglob("*.html")) + [site / "guides" / "index.html"]
    links = 0
    for page in pages:
        if not page.is_file():
            report.error(rel_site(site, page), "page is missing")
            continue
        html = page.read_text(encoding="utf-8")
        if "{%" in html or "{{" in html:
            report.error(rel_site(site, page), "unrendered Liquid in output")
        for match in HREF.finditer(html):
            url = match["url"]
            if not url.startswith("/") or url.startswith("//"):
                continue
            links += 1
            target = site / url.lstrip("/")
            if not (target.is_file() or (target / "index.html").is_file()):
                report.error(rel_site(site, page), f"internal link {url} does not resolve")
    report.note(f"site: {len(chapters)} chapters, {len(pages)} pages scanned, {links} internal links checked")


def rel_site(site: Path, path: Path) -> str:
    try:
        return path.relative_to(site).as_posix()
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Checks for the Fortran guide.")
    parser.add_argument("command", choices=["lint", "examples", "site", "all"])
    parser.add_argument("site", nargs="?", type=Path)
    args = parser.parse_args()
    report = Report()
    if args.command in ("lint", "all"):
        lint(report)
    if args.command in ("examples", "all"):
        run_examples(report)
    if args.command == "site" or (args.command == "all" and args.site):
        if not args.site:
            parser.error("site needs the built site directory")
        check_site(args.site.resolve(), report)
    for note in report.notes:
        print(note)
    for error in report.errors:
        print(f"ERROR {error}", file=sys.stderr)
    print(f"{len(report.errors)} error(s)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
