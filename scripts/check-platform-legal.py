#!/usr/bin/env python3
"""Check platform/legal/: pinned EULA text, internal links, no dashes, version lines.

    python3 scripts/check-platform-legal.py [--base URL]

Without --base it checks the files in this repository. With --base
(for example https://blindsight.io) it fetches the live pages and the EULA copy.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EULA_SHA256 = "2006c54f53548282ff652423ef2a1590d43fa6dcadde87e8bf954ad2e704f2a7"
PAGES = ["", "eula/", "dpa/", "subprocessors/", "privacy/"]


def get(base: str | None, path: str) -> bytes:
    if base:
        with urllib.request.urlopen(base.rstrip("/") + "/platform/legal/" + path) as r:
            assert r.status == 200, (path, r.status)
            return r.read()
    p = ROOT / "platform" / "legal" / path
    return (p / "index.html" if p.is_dir() or path.endswith("/") or path == "" else p).read_bytes()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base")
    a = ap.parse_args()
    bad: list[str] = []
    eula = get(a.base, "eula/EULA-1.0.md")
    if hashlib.sha256(eula).hexdigest() != EULA_SHA256:
        bad.append("EULA-1.0.md does not have the pinned sha256")
    for p in PAGES:
        t = get(a.base, p).decode("utf-8")
        name = p or "index"
        if "—" in t or "–" in t:
            bad.append(f"{name}: dash character")
        if not re.search(r"Version \d+\.\d+ &middot; Effective|Version \d+\.\d+", t):
            bad.append(f"{name}: no version")
        if "covers the Blindsight platform" not in t and "cover the Blindsight platform" not in t:
            bad.append(f"{name}: no scope line")
        if "/privacy-policy/" not in t:
            bad.append(f"{name}: no link to the website privacy notice")
        if not a.base:
            for h in set(re.findall(r'(?:href|src)="(/[^"#]*)"', t)):
                q = ROOT / h.lstrip("/")
                if h != "/" and not (q.is_file() or (q / "index.html").is_file()):
                    bad.append(f"{name}: broken link {h}")
    for b in bad:
        print("FAIL", b, file=sys.stderr)
    print("ok" if not bad else f"{len(bad)} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
