#!/usr/bin/env python3
"""Fail if the licence page could show a placeholder. Run before merging to main.

Passes when legal/eula/index.html has no "[" placeholder and no <angle
placeholder> in its visible text. A draft page (built while the text had
placeholders) carries none of the draft text, so it passes and says so.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "legal" / "eula" / "index.html"


def problems(page: str) -> list[str]:
    body = page.split("<!-- CONTENT -->", 1)[1] if "<!-- CONTENT -->" in page else page
    visible = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", body, flags=re.S)
    found = [visible[m.start():m.start() + 50] for m in re.finditer(r"\[", visible)]
    found += re.findall(r"&lt;[A-Za-z][A-Za-z ]*&gt;", visible)
    return found


def main() -> int:
    if not PAGE.exists():
        print("legal/eula/index.html is not built.")
        return 0
    page = PAGE.read_text(encoding="utf-8")
    found = problems(page)
    if found:
        print(f"legal/eula/index.html still shows {len(found)} placeholder(s), first: {found[0]!r}", file=sys.stderr)
        return 1
    print("legal/eula/index.html: no placeholders" + (" (draft notice only)" if 'content="draft"' in page else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
