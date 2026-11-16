#!/usr/bin/env python3
"""Build legal/eula/index.html from the licence text.

    python3 scripts/build-legal-eula.py TEXT.md --meta licence.json [--platform-meta current.json] [--require-final]

The text is the same file the Blindsight platform serves and the installers show.
While it still holds a placeholder (a "[" or an <angle placeholder>) the page is
built as a short "being finalised" notice that contains NONE of the draft text,
so a draft can never be published by merging this branch. With --require-final a
text that still has placeholders is an error (exit 1): use it in the release.

Styles and the page frame come from privacy-policy/index.html, so the two legal
pages cannot drift apart.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRAME = ROOT / "privacy-policy" / "index.html"
OUT = ROOT / "legal" / "eula" / "index.html"
ANGLE = re.compile(r"<[A-Za-z][A-Za-z ]*>")


def placeholders(text: str) -> list[str]:
    found = [line[m.start():m.start() + 60] for line in text.splitlines() for m in re.finditer(r"\[", line)]
    for line in text.splitlines():
        found.extend(ANGLE.findall(line))
    return found


def _inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return re.sub(r"(https://[^\s<)]+[^\s<).,;])", r'<a href="\1">\1</a>', s)


def body_from(text: str) -> str:
    out: list[str] = []
    for block in [b.strip() for b in text.strip().split("\n\n") if b.strip()]:
        if block.startswith("# "):
            continue  # the page title is its own heading
        lines = block.split("\n")
        m = re.match(r"\*\*(\d+\. [^*]+)\*\*(.*)", lines[0])
        if m and not m.group(2).strip() and len(lines) == 1:
            out.append(f'  </div>\n  <div class="pp-section">\n    <h2>{html.escape(m.group(1))}</h2>')
        elif m:
            out.append(f'  </div>\n  <div class="pp-section">\n    <h2>{html.escape(m.group(1))}</h2>\n    <p>{_inline(m.group(2).strip())}</p>')
        else:
            out.append("    <p>" + "<br>\n    ".join(_inline(x) for x in lines) + "</p>")
    body = "\n".join(out)
    return body.replace('  </div>\n  <div class="pp-section">', '<div class="pp-section">', 1) if body.startswith("  </div>") else '  <div class="pp-section">\n' + body


def text_hash(text: str) -> str:
    """Same normalisation as the platform and the installers: LF, one trailing newline."""
    return hashlib.sha256((text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n").encode("utf-8")).hexdigest()


def build(text: str, version: str, published: str, marked_final: bool = False) -> tuple[str, bool]:
    final = bool(marked_final) and not placeholders(text)
    frame = FRAME.read_text(encoding="utf-8")
    head, rest = frame.split("<!-- CONTENT -->", 1)
    foot = rest.split("<!-- FOOTER -->", 1)[1]
    head = re.sub(r"<title>.*?</title>", "<title>End-User Licence Agreement | Blindsight</title>", head, count=1)
    head = re.sub(r'<meta name="description"[^>]*/>', '<meta name="description" content="The Blindsight desktop end-user licence agreement." />', head, count=1)
    head = head.replace("https://www.blindsight.io/privacy-policy", "https://www.blindsight.io/legal/eula")
    head = head.replace('href="../assets/', 'href="../../assets/').replace('src="../assets/', 'src="../../assets/')
    if not final:
        head = head.replace("</head>", '  <meta name="robots" content="noindex, nofollow" />\n  <meta name="blindsight-licence-status" content="draft" />\n</head>', 1)
        content = (
            '<div class="pp-container">\n  <div class="pp-tag">// Legal</div>\n'
            '  <h1 class="pp-title">End-User Licence Agreement</h1>\n'
            '  <p class="pp-intro">This agreement is being finalised and is not published yet.</p>\n</div>\n'
        )
    else:
        content = (
            '<div class="pp-container">\n  <div class="pp-tag">// Legal</div>\n'
            '  <h1 class="pp-title">End-User Licence Agreement</h1>\n'
            f'  <div class="pp-updated">Version {html.escape(version)}, published {html.escape(published)}</div>\n'
            f'  <div class="pp-divider"></div>\n{body_from(text)}\n  </div>\n</div>\n'
        )
    foot = foot.replace('<li><a href="/privacy-policy/">Privacy</a></li>', '<li><a href="/privacy-policy/">Privacy</a></li>\n    <li><a href="/legal/eula/">Licence</a></li>', 1)
    foot = foot.replace('href="/antidote/"', 'href="/antidote/"')
    return head + "<!-- CONTENT -->\n" + content + "\n<!-- FOOTER -->" + foot, final


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text", type=Path)
    ap.add_argument("--meta", type=Path, required=True, help="licence.json: version, published_at, final")
    ap.add_argument("--platform-meta", type=Path, help="the platform's current.json, to compare the version")
    ap.add_argument("--require-final", action="store_true")
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)
    meta = json.loads(a.meta.read_text(encoding="utf-8"))
    if a.platform_meta:
        theirs = json.loads(a.platform_meta.read_text(encoding="utf-8"))
        if str(theirs.get("version")) != str(meta.get("version")):
            print(f"The licence version here ({meta.get('version')}) is not the platform's ({theirs.get('version')}).", file=sys.stderr)
            return 1
    text = a.text.read_text(encoding="utf-8")
    page, final = build(text, str(meta["version"]), str(meta["published_at"]), bool(meta.get("final")))
    print(f"licence {meta['version']} sha256 {text_hash(text)}")
    if a.require_final and not final:
        print("The licence text is not final (not marked final, or it still has placeholders); not building a final page.", file=sys.stderr)
        return 1
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(page, encoding="utf-8")
    print(f"wrote {a.out} ({'final' if final else 'draft: no licence text on the page'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
