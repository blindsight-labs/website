#!/usr/bin/env python3
"""Build the Blindsight platform legal pages under platform/legal/.

    python3 scripts/build-platform-legal.py SOURCE_DIR [--effective "19 November 2026"]

SOURCE_DIR holds EULA-1.0.md and final/{DPA,SUBPROCESSORS,PRIVACY-NOTICE}.md
(the platform repository, plans/eula-review-2026-11-18). The page frame
(styles, nav, footer, theme) comes from privacy-policy/index.html so the legal
pages cannot drift from the site.

The EULA is pinned by hash in the desktop app and the platform. The build stops
unless the source file has the pinned sha256, writes that exact file next to the
page (platform/legal/eula/EULA-1.0.md) and checks the copy byte for byte.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRAME = ROOT / "privacy-policy" / "index.html"
OUT = ROOT / "platform" / "legal"
EULA_SHA256 = "2006c54f53548282ff652423ef2a1590d43fa6dcadde87e8bf954ad2e704f2a7"

DOCS = [
    # slug, source file (relative), page title, short description, effective date (None: use --effective)
    ("eula", "EULA-1.0.md", "Endpoint Licence Agreement",
     "The licence agreement for the Blindsight desktop software and hosted service.", "18 November 2026"),
    ("dpa", "final/DPA.md", "Data Processing Agreement",
     "How Blindsight processes personal data on behalf of its customers.", None),
    ("subprocessors", "final/SUBPROCESSORS.md", "Sub-processors",
     "The providers Blindsight uses to process customer data.", None),
    ("privacy", "final/PRIVACY-NOTICE.md", "Privacy Notice",
     "How Blindsight handles personal data on the platform, as controller.", None),
]

LINK_MAP = {
    "https://blindsight.io/platform/legal/eula": "/platform/legal/eula/",
    "https://blindsight.io/platform/legal/dpa": "/platform/legal/dpa/",
    "https://blindsight.io/platform/legal/subprocessors": "/platform/legal/subprocessors/",
    "https://blindsight.io/platform/legal/privacy": "/platform/legal/privacy/",
    "https://blindsight.io/privacy": "/privacy-policy/",
}
WEBSITE_PRIVACY = "/privacy-policy/"

EXTRA_CSS = """
    /* ── PLATFORM LEGAL ── */
    .pp-container { max-width: 860px; }
    .pl-scope {
      font-size: 14px; line-height: 1.7; color: var(--text-intro);
      border: 1px solid var(--border); border-left: 3px solid var(--purple);
      padding: 14px 18px; margin: 0 0 40px; border-radius: 2px;
    }
    .pl-scope a { color: var(--purple); border-bottom: 1px solid rgba(109,40,217,0.3); text-decoration: none; }
    .pl-scope a:hover { border-color: var(--purple); }
    .pl-doc .pp-section p, .pl-doc .pp-section li, .pl-doc td, .pl-doc th { color: var(--text-intro); }
    .pl-doc p { font-size: 14px; line-height: 1.8; color: var(--text-intro); margin-bottom: 14px; overflow-wrap: anywhere; }
    .pl-doc p .ln { display: block; padding-left: 2.2em; text-indent: -2.2em; }
    .pl-doc p .ln:first-child { padding-left: 0; text-indent: 0; }
    .pl-doc h2 { font-family: var(--display); font-size: 20px; font-weight: 700; letter-spacing: -0.02em; margin: 40px 0 16px; color: var(--text); }
    .pl-doc h3 { font-family: var(--display); font-size: 16px; font-weight: 700; margin: 28px 0 10px; color: var(--text-heading-sub); }
    .pl-doc h2.clause { font-size: 17px; margin-top: 36px; }
    .pl-doc ul { list-style: none; margin: 0 0 16px; padding: 0; }
    .pl-doc ul li { font-size: 14px; line-height: 1.8; color: var(--text-intro); padding-left: 20px; position: relative; margin-bottom: 8px; overflow-wrap: anywhere; }
    .pl-doc ul li::before { content: ''; position: absolute; left: 0; top: 10px; width: 6px; height: 6px; border: 1px solid var(--purple); border-radius: 1px; }
    .pl-doc ol { margin: 0 0 16px 22px; padding: 0; }
    .pl-doc ol li { font-size: 14px; line-height: 1.8; color: var(--text-intro); margin-bottom: 8px; }
    .pl-doc strong { color: var(--text-strong); font-weight: 600; }
    .pl-doc a { color: var(--purple); text-decoration: none; border-bottom: 1px solid rgba(109,40,217,0.3); }
    .pl-doc a:hover { border-color: var(--purple); }
    .pl-doc code { font-family: var(--mono); font-size: 12.5px; }
    .pl-doc hr { border: 0; height: 1px; background: var(--divider); margin: 40px 0; }
    .pl-doc pre.pl-notice { font-family: var(--mono); font-size: 11.5px; line-height: 1.6; color: var(--text-intro); white-space: pre-wrap; overflow-wrap: anywhere; border: 1px solid var(--border); padding: 14px 16px; margin: 0 0 24px; }
    .pl-tablewrap { overflow-x: auto; margin: 0 0 24px; border: 1px solid var(--border); }
    .pl-doc table { border-collapse: collapse; width: 100%; min-width: 640px; font-size: 12.5px; line-height: 1.6; }
    .pl-doc th, .pl-doc td { text-align: left; vertical-align: top; padding: 8px 10px; border-bottom: 1px solid var(--divider); }
    .pl-doc th { font-family: var(--mono); font-size: 10px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-strong); }
    .pl-index { list-style: none; margin: 0; padding: 0; }
    .pl-index li { border-top: 1px solid var(--divider); }
    .pl-index li:last-child { border-bottom: 1px solid var(--divider); }
    .pl-doc .pl-index li { padding-left: 0; margin-bottom: 0; }
    .pl-doc .pl-index li::before { display: none; }
    .pl-index a { display: block; padding: 20px 4px; text-decoration: none; border: 0; }
    .pl-index a:hover .pl-name { color: var(--purple); }
    .pl-name { display: block; font-family: var(--display); font-size: 18px; font-weight: 700; color: var(--text); letter-spacing: -0.02em; }
    .pl-desc { display: block; font-size: 14px; line-height: 1.6; color: var(--text-intro); margin-top: 4px; }
    .pl-meta { display: block; font-family: var(--mono); font-size: 11px; color: var(--text-updated); margin-top: 6px; letter-spacing: 0.04em; }
    .pl-raw { font-family: var(--mono); font-size: 11px; letter-spacing: 0.04em; margin: 0 0 32px; color: var(--text-updated); }
    .pl-raw a { color: var(--purple); }
    .pl-skip { position: absolute; left: -999px; }
    .pl-skip:focus { left: 8px; top: 8px; z-index: 300; background: var(--bg); color: var(--text); padding: 8px 12px; }
    @media print {
      :root, [data-theme="dark"], [data-theme="light"] {
        --bg: #fff; --text: #000; --text-mid: #222; --text-dim: #444; --text-body: #111; --text-intro: #111;
        --text-heading-sub: #000; --text-strong: #000; --text-updated: #333; --border: #bbb; --divider: #bbb; --purple: #000;
      }
      body { background: #fff; color: #000; font-size: 11pt; }
      nav, .mobile-menu, footer, .pl-raw, .pl-skip { display: none !important; }
      .pp-container { max-width: none; padding: 0; }
      .pl-scope { border: 1px solid #000; border-left: 3px solid #000; }
      .pl-doc p, .pl-doc ul li, .pl-doc ol li, .pl-doc td, .pl-doc th { font-size: 10.5pt; color: #000; }
      .pl-doc a, .pl-scope a { color: #000; border: 0; text-decoration: underline; }
      .pl-doc h2, .pl-doc h3 { break-after: avoid; }
      .pl-doc p, .pl-doc li, .pl-doc tr { break-inside: avoid; }
      .pl-tablewrap { overflow: visible; border: 0; }
      .pl-doc pre.pl-notice { font-size: 8.5pt; color: #000; border: 1px solid #888; }
      .pl-doc table { min-width: 0; font-size: 9pt; }
      .pl-doc th, .pl-doc td { border: 1px solid #888; }
      .pl-print-url { display: block !important; }
    }
    .pl-print-url { display: none; font-family: var(--mono); font-size: 10pt; margin-bottom: 16px; }
"""


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)

    def url(m: re.Match) -> str:
        u = m.group(1)
        trail = ""
        while u and u[-1] in ".,;:":
            trail = u[-1] + trail
            u = u[:-1]
        href = LINK_MAP.get(u, u)
        return f'<a href="{href}">{u}</a>{trail}'

    s = re.sub(r"(https://[^\s<)]+)", url, s)
    s = re.sub(r"(?<![\w/>@.-])([A-Za-z0-9._-]+@[A-Za-z0-9.-]+[A-Za-z0-9])", r'<a href="mailto:\1">\1</a>', s)
    return s


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def render(md: str) -> str:
    lines = md.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
        elif ln.startswith("# "):
            i += 1  # the page title is its own heading
        elif ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:])}</h3>")
            i += 1
        elif ln.startswith("## "):
            out.append(f"<h2>{inline(ln[3:])}</h2>")
            i += 1
        elif re.fullmatch(r"-{3,}", ln.strip()):
            out.append("<hr>")
            i += 1
        elif ln.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i])
                i += 1
            head, sep, rows = cells(block[0]), block[1], [cells(r) for r in block[2:]]
            assert re.fullmatch(r"[|\s:-]+", sep), f"not a table separator: {sep[:40]}"
            for r in rows:
                assert len(r) == len(head), f"table row has {len(r)} cells, header {len(head)}: {r[0][:40]}"
            t = "<div class=\"pl-tablewrap\" tabindex=\"0\" role=\"region\" aria-label=\"Table\"><table>\n<thead><tr>"
            t += "".join(f'<th scope="col">{inline(c)}</th>' for c in head) + "</tr></thead>\n<tbody>\n"
            for r in rows:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>\n"
            out.append(t + "</tbody></table></div>")
        elif re.match(r"- ", ln):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:])
                i += 1
            out.append("<ul>\n" + "\n".join(f"<li>{inline(x)}</li>" for x in items) + "\n</ul>")
        elif re.match(r"\d+\. ", ln):
            items = []
            while i < len(lines) and re.match(r"\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i]))
                i += 1
            out.append("<ol>\n" + "\n".join(f"<li>{inline(x)}</li>" for x in items) + "\n</ol>")
        else:
            block = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||- |\d+\. |-{3,}$)", lines[i]):
                block.append(lines[i])
                i += 1
            m = re.fullmatch(r"\*\*(\d+\. [^*]+)\*\*", block[0]) if len(block) == 1 else None
            if m:
                out.append(f'<h2 class="clause">{html.escape(m.group(1))}</h2>')
            else:
                out.append("<p>" + "".join(f'<span class="ln">{inline(x)}</span>' for x in block) + "</p>")
    return "\n".join(out)


def page(frame: str, *, title: str, desc: str, slug: str, content: str) -> str:
    head, rest = frame.split("<!-- CONTENT -->", 1)
    foot = rest.split("<!-- FOOTER -->", 1)[1]
    canon = f"https://blindsight.io/platform/legal/{slug}".rstrip("/")
    head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}{'' if 'platform' in title else ' | Blindsight platform'}</title>", head, count=1)
    head = re.sub(r'<meta name="description"[^>]*/>', f'<meta name="description" content="{html.escape(desc)}" />', head, count=1)
    head = head.replace("https://www.blindsight.io/privacy-policy", canon)
    head = head.replace('href="../assets/', 'href="/assets/').replace('src="../assets/', 'src="/assets/')
    head = head.replace("</style>", EXTRA_CSS + "  </style>", 1)
    head = head.replace("<body>", '<body>\n<a class="pl-skip" href="#main">Skip to the document</a>', 1)
    # the nav and mobile menu are in the frame head part (before CONTENT); keep them as they are
    foot = foot.replace('<li><a href="/privacy-policy/">Privacy</a></li>',
                        '<li><a href="/privacy-policy/">Privacy</a></li>\n    <li><a href="/platform/legal/">Platform legal</a></li>', 1)
    assert "/platform/legal/" in foot
    return head + "<!-- CONTENT -->\n" + content + "\n<!-- FOOTER -->" + foot


def scope_line() -> str:
    return (
        '<p class="pl-scope">This document covers the Blindsight platform (the console, the desktop apps and the APIs). '
        f'The blindsight.io website has its own <a href="{WEBSITE_PRIVACY}">privacy policy</a>.</p>'
    )


CC = {
    "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/legalcode",
    "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/legalcode",
    "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/legalcode",
    "CC0": "https://creativecommons.org/publicdomain/zero/1.0/legalcode",
    "Apache-2.0": "http://www.apache.org/licenses/LICENSE-2.0",
    "AFL-3.0": "https://opensource.org/license/afl-3-0-php",
}
CONVERTED = "Converted to a token-classification format and relabelled to person, organisation, place and date; entity classes mapped; some sentences case-changed or had names swapped."
# name, creator, licence key, source url, what Blindsight changed. Each licence key, source URL and
# creator surname must appear in the NOTICE text (checked in third_party_rows), so nothing here is invented.
BASE = ("distilbert-base-multilingual-cased (base model)", "Sanh et al.", "Apache-2.0",
        "https://huggingface.co/distilbert/distilbert-base-multilingual-cased",
        "Weights fine-tuned by Blindsight for token classification (names, organisations, places and dates), then converted to ONNX with reduced numeric precision (FP16 or INT8).")
ROWS = [
    ("Universal NER v1 (treebanks English-EWT, Portuguese-Bosque, Chinese-GSD, Chinese-GSDSimp)", "Mayhew et al.", "CC BY-SA 4.0", "https://www.universalner.org", CONVERTED),
    ("Europeana Newspapers NER corpora", "Europeana Newspapers Project", "CC0", "https://github.com/EuropeanaNewspapers/ner-corpora", CONVERTED),
    ("ANERcorp, CAMeL Lab train/test splits", "Benajiba, Rosso and Benedi Ruiz; Obeid et al.", "CC BY-SA 4.0", "https://camel.abudhabi.nyu.edu/anercorp/", CONVERTED),
    ("AQMAR Arabic Wikipedia Named Entity Corpus", "Mohit, Schneider, Bhowmick, Oflazer and Smith", "CC BY-SA 3.0", "https://www.cs.cmu.edu/~ark/ArabicNER/", CONVERTED + " CC BY-SA 3.0 section 4(b) permits an adaptation to be distributed under a later version of the licence with the same licence elements, here CC BY-SA 4.0."),
    ("GermEval 2014 NER shared task data", "Benikova, Biemann, Reznicek", "CC BY 4.0", "https://sites.google.com/site/germeval2014ner/", CONVERTED),
    ("WikiNER and wikigold", "Nothman, Ringland, Radford, Murphy, Curran; Balasuriya et al.", "CC BY 4.0", "https://doi.org/10.6084/m9.figshare.5462500", CONVERTED),
    ("MultiCoNER v2", "Fetahu, Chen, Kar, Rokhlenko, Malmasi", "CC BY 4.0", "https://multiconer.github.io", CONVERTED),
    ("LUMII AiLab FullStack, Latvian named entities", "LUMII AiLab", "CC BY-SA 4.0", "https://github.com/LUMII-AILab/FullStack", CONVERTED),
    ("Wikidata name labels", "Wikidata", "CC0", "https://www.wikidata.org", "Used to fill synthetic sentences."),
]


def licence_link(key: str) -> str:
    return f'<a href="{CC[key]}">{html.escape(key)}</a>'


def third_party_rows(notice: str) -> str:
    """Table rows. Every licence, source URL and creator name used must occur in the NOTICE text."""
    out = []
    for name, creator, lic, url, change in [BASE] + ROWS:
        assert url in notice, f"source url not in the NOTICE: {url}"
        assert lic.replace("Apache-2.0", "Apache") in notice or lic in notice, lic
        first = re.split(r"[,;]| and ", creator)[0].split()[-1] if "et al" not in creator else creator.split()[0]
        assert first in notice, f"creator not in the NOTICE: {creator}"
        out.append(
            f"<tr><td>{html.escape(name)}</td><td>{html.escape(creator)}</td><td>{licence_link(lic)}</td>"
            f'<td><a href="{url}">{html.escape(url)}</a></td><td>{html.escape(change)}</td></tr>'
        )
    return "\n".join(out)


def third_party_content(notices: Path, effective: str, public_name: str | None) -> str:
    n8 = (notices / "int8" / "NOTICE.txt").read_text(encoding="utf-8")
    n16 = (notices / "fp16" / "NOTICE.txt").read_text(encoding="utf-8")
    orgs = (notices / "int8" / "NOTICE-orgs-v1.txt").read_text(encoding="utf-8")
    assert orgs == (notices / "fp16" / "NOTICE-orgs-v1.txt").read_text(encoding="utf-8")
    block = re.compile(r"^Modification statement \(this variant: [^\n]*\)\n(?:  [^\n]*\n)+", re.M)
    m8, m16 = block.search(n8), block.search(n16)
    assert m8 and m16 and n8.replace(m8.group(0), "") == n16.replace(m16.group(0), ""), "the two notices differ outside the modification statement"
    for t in (n8, n16, orgs):
        assert "\r" not in t and "—" not in t and "–" not in t, "CR or dash in a notice"
    # The product name stays out of the page until the trademark check is done.
    first_line = "Mosaic v2, the Blindsight name model (model id mosaic-v2)\n"
    assert n8.startswith(first_line)
    assert n8.count("Mosaic") == 2 and n16.count("Mosaic") == 2 and "Mosaic" not in orgs
    if public_name is None:
        repl = lambda t: t.replace(first_line, "The Blindsight on-device names model\n", 1).replace("from the Mosaic v2 weights", "from the weights")
        shown8, shown16 = repl(n8), repl(n16)
        model = "the on-device names model"
        assert "Mosaic" not in shown8 + shown16
    else:
        shown8, shown16, model = n8, n16, public_name
    rows = third_party_rows(n8)
    org_row = (
        "<tr><td>Organisation name list (orgs-v1.json)</td><td>Wikidata</td><td>" + licence_link("CC0") + '</td><td><a href="https://www.wikidata.org">https://www.wikidata.org</a></td>'
        "<td>Labels and identifiers only, no Wikipedia text. A separate file, not covered by the CC BY-SA 4.0 grant for the model files.</td></tr>"
    )
    davlan_row = (
        "<tr><td>Davlan/distilbert-base-multilingual-cased-ner-hrl (earlier name model, versions 1 and 2-fp16 only)</td>"
        "<td>Davlan (the model card names no copyright holder)</td><td>" + licence_link("AFL-3.0") + '</td>'
        '<td><a href="https://huggingface.co/Davlan/distilbert-base-multilingual-cased-ner-hrl">https://huggingface.co/Davlan/distilbert-base-multilingual-cased-ner-hrl</a></td>'
        "<td>Converted to ONNX; the Apple silicon file is quantised to int8 and the file for every other device is converted to fp16. Weights otherwise unmodified.</td></tr>"
    )
    own_row = (
        f"<tr><td>Weights of {html.escape(model)} (versions 4 and 4-fp16)</td><td>Blindsight Technologies AG</td><td>{licence_link('CC BY-SA 4.0')}</td>"
        "<td>Downloaded by the desktop app after installation; not inside the installers.</td>"
        "<td>Fine-tuned from the base model; converted to ONNX; INT8 (dynamic, per channel) on Apple silicon, FP16 on all other devices. The tokenizer file is the tokenizer of the base model.</td></tr>"
    )
    esc = html.escape
    return (
        '<main id="main" class="pp-container pl-doc">\n  <div class="pp-tag">// Platform legal</div>\n'
        '  <h1 class="pp-title">Blindsight third-party licences</h1>\n'
        f'  <div class="pp-updated">Applies to {esc(model)} versions 4 and 4-fp16 &middot; Updated {esc(effective)}</div>\n'
        '  <p class="pl-print-url">blindsight.io/platform/legal/third-party</p>\n'
        f"  {scope_line()}\n"
        '  <div class="pp-section">\n'
        "<h2>1. What this page lists</h2>\n"
        f"<p>The models, tokenizer and datasets behind {esc(model)}, with their creators, licences, sources and the changes Blindsight made. The model files are downloaded by the desktop app after installation. The weights and the tokenizer file are licensed under CC BY-SA 4.0; the base model and the datasets keep the licences named below. The libraries and programs inside the installers are listed in the licence notices supplied with the software.</p>\n"
        "<h2>2. Models, tokenizer and datasets</h2>\n"
        '<div class="pl-tablewrap" tabindex="0" role="region" aria-label="Models, tokenizer and datasets"><table>\n'
        "<thead><tr><th scope=\"col\">Name</th><th scope=\"col\">Creator</th><th scope=\"col\">Licence</th><th scope=\"col\">Source</th><th scope=\"col\">What Blindsight changed</th></tr></thead>\n<tbody>\n"
        + own_row + "\n" + rows + "\n" + org_row + "\n" + davlan_row +
        "\n</tbody></table></div>\n"
        "<p>Blindsight also generated sentences by script from its own templates and lists, and had a language model write synthetic sentences with the names filled in by script. These are Blindsight's own material. No data from any Blindsight customer was used.</p>\n"
        "<h2>3. Full notice shipped with the model files</h2>\n"
        "<p>This is the notice that comes with the INT8 model files, followed by the one change that differs in the FP16 files. It includes the Apache License 2.0 text for the base model.</p>\n"
        f'<pre class="pl-notice">{esc(shown8)}</pre>\n'
        "<h3>Modification statement in the FP16 notice</h3>\n"
        f'<pre class="pl-notice">{esc(block.search(shown16).group(0))}</pre>\n'
        "<h3>Organisation list notice</h3>\n"
        f'<pre class="pl-notice">{esc(orgs)}</pre>\n'
        "  </div>\n</main>\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path)
    ap.add_argument("--effective", required=True, help="effective date of the three documents that take effect on publication, e.g. '19 December 2026'")
    ap.add_argument("--notices", type=Path, required=True, help="the Mosaic v2 artifacts directory holding int8/ and fp16/ with NOTICE.txt and NOTICE-orgs-v1.txt")
    ap.add_argument("--product-name", help="use this product name for the names model instead of 'the on-device names model' (only after the trademark check)")
    a = ap.parse_args()

    eula_path = a.source / "EULA-1.0.md"
    eula_bytes = eula_path.read_bytes()
    if sha(eula_bytes) != EULA_SHA256:
        print(f"EULA source hash is {sha(eula_bytes)}, expected {EULA_SHA256}. Not building.", file=sys.stderr)
        return 1

    frame = FRAME.read_text(encoding="utf-8")
    index_items = []
    for slug, src, title, desc, eff in DOCS:
        raw = (a.source / src).read_bytes()
        md = raw.decode("utf-8")
        assert "\r" not in md and "—" not in md and "–" not in md, f"{src}: CR or dash character"
        m = re.search(r"^Version (\d+\.\d+)[.,]", md, re.M)
        assert m, f"{src}: no version line"
        version = m.group(1)
        effective = eff or a.effective
        body_md = md
        if slug != "eula":
            # the page shows the version and the scope line itself, above; drop the document's two identical lines
            body_md = re.sub(r"^Version [^\n]*\n\n", "", body_md, count=1, flags=re.M)
            body_md = re.sub(r"^This (document|list|notice) covers the Blindsight platform[^\n]*\n\n", "", body_md, count=1, flags=re.M)
        body = render(body_md)
        raw_link = ""
        if slug == "eula":
            raw_link = '<p class="pl-raw">Plain text of this version, exactly as signed off: <a href="/platform/legal/eula/EULA-1.0.md">EULA-1.0.md</a></p>\n'
        content = (
            f'<main id="main" class="pp-container pl-doc">\n  <div class="pp-tag">// Platform legal</div>\n'
            f'  <h1 class="pp-title">{html.escape("Blindsight " + title)}</h1>\n'
            f'  <div class="pp-updated">Version {version} &middot; Effective {html.escape(effective)}</div>\n'
            f'  <p class="pl-print-url">blindsight.io/platform/legal/{slug}</p>\n'
            f"  {scope_line()}\n  {raw_link}"
            f'  <div class="pp-section">\n{body}\n  </div>\n</main>\n'
        )
        d = OUT / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(frame, title="Blindsight " + title, desc=desc, slug=slug + "/", content=content), encoding="utf-8")
        if slug == "eula":
            shutil.copyfile(eula_path, d / "EULA-1.0.md")
            assert sha((d / "EULA-1.0.md").read_bytes()) == EULA_SHA256
        index_items.append((slug, title, desc, version, effective))
        print(f"{slug}: version {version}, effective {effective}, {len(body)} bytes of html")

    tp = third_party_content(a.notices, a.effective, a.product_name)
    d = OUT / "third-party"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(page(frame, title="Blindsight third-party licences", desc="Models, tokenizer and datasets behind the Blindsight on-device names model, with creators, licences, sources and changes.", slug="third-party/", content=tp), encoding="utf-8")
    print("third-party written")

    li = "\n".join(
        f'    <li><a href="/platform/legal/{s}/"><span class="pl-name">{html.escape(t)}</span>'
        f'<span class="pl-desc">{html.escape(d)}</span><span class="pl-meta">Version {v} &middot; Effective {html.escape(e)}</span></a></li>'
        for s, t, d, v, e in index_items
    ) + (
        '\n    <li><a href="/platform/legal/third-party/"><span class="pl-name">Third-party licences</span>'
        '<span class="pl-desc">Models, tokenizer and datasets behind the on-device names model, with creators, licences, sources and changes.</span>'
        f'<span class="pl-meta">Updated {html.escape(a.effective)}</span></a></li>'
    )
    content = (
        '<main id="main" class="pp-container pl-doc">\n  <div class="pp-tag">// Platform legal</div>\n'
        '  <h1 class="pp-title">Blindsight platform legal documents</h1>\n'
        '  <div class="pp-updated">Console, desktop apps and APIs</div>\n'
        f"  {scope_line().replace('This document covers', 'These documents cover')}\n"
        f'  <ul class="pl-index">\n{li}\n  </ul>\n</main>\n'
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(
        page(frame, title="Blindsight platform legal documents", desc="The licence agreement, data processing agreement, sub-processor list and privacy notice for the Blindsight platform.", slug="", content=content),
        encoding="utf-8",
    )
    print("index written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
