#!/usr/bin/env python3
"""Assemble a self-contained study-guide HTML from the shared template chrome
+ authored content, so the design system (CSS/JS) stays byte-identical to
`_template.html` and only the content differs.

A guide "content module" is a python file that defines:
    TITLE   : str   (page <title> and hero)
    DIGEST  : dict  (the #sg-digest JSON payload)
    LAYOUT  : str   (the full <div class="layout"> ... </div> block: nav + main)

Usage:
    python3 build_guide.py <content_module.py> <out.html>
The chrome is lifted from ../_template.html at the two stable anchors.
"""
import sys, os, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "_template.html")

DIGEST_ANCHOR = '<script type="application/json" id="sg-digest">'
FOOTER_ANCHOR = '<script>\n// ---- generate a quiz'


def load_module(path):
    spec = importlib.util.spec_from_file_location("guide_content", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(content_path: str) -> str:
    tpl = open(TEMPLATE, encoding="utf-8").read()
    d_idx = tpl.index(DIGEST_ANCHOR)
    f_idx = tpl.index(FOOTER_ANCHOR)
    head = tpl[:d_idx]
    footer = tpl[f_idx:]

    mod = load_module(content_path)
    title = mod.TITLE
    head = head.replace("{{Title}} — Study Guide", f"{title} — Study Guide")

    digest_block = (
        DIGEST_ANCHOR + "\n" + json.dumps(mod.DIGEST, ensure_ascii=False, indent=2) + "\n</script>"
    )
    out = head + digest_block + "\n\n" + mod.LAYOUT.strip() + "\n\n" + footer
    return out


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    html = build(sys.argv[1])
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(html)
    # quick sanity: single <body> tag, layout present, digest parses
    assert html.count("<body ") == 1 and html.count("</body>") == 1, "expected exactly one body element"
    assert '<div class="layout">' in html, "missing layout block"
    import re as _re
    _dig = _re.search(r'<script type="application/json" id="sg-digest">\s*(\{.*?\})\s*</script>', html, _re.S)
    assert _dig, "missing sg-digest"
    json.loads(_dig.group(1))  # raises if the digest isn't valid JSON
    print(f"OK wrote {sys.argv[2]}  ({len(html):,} bytes)")
