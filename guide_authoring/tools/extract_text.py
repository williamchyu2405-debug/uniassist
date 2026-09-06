#!/usr/bin/env python3
"""Extract clean, readable source text from a study-guide HTML file.

Study guides embed base64 images and lots of chrome; this strips those and
returns the visible teaching text (with rough section breaks preserved) so it
can be used as the source material for authoring a fresh quiz bank.

Usage:  python3 extract_text.py <guide.html>   # prints text to stdout
"""
import re, sys, html, os

GUIDE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "static", "guides")


def extract(path: str) -> str:
    with open(path, encoding="utf-8", errors="ignore") as f:
        doc = f.read()
    # Drop scripts, styles, and base64 image payloads first (they dwarf the text).
    doc = re.sub(r"<script.*?</script>", " ", doc, flags=re.S | re.I)
    doc = re.sub(r"<style.*?</style>", " ", doc, flags=re.S | re.I)
    doc = re.sub(r"data:image/[^\"')]+", "", doc)
    # Turn block-level tags into newlines so section structure survives.
    doc = re.sub(r"</(p|div|section|li|h[1-6]|tr|table|figcaption|blockquote)>", "\n", doc, flags=re.I)
    doc = re.sub(r"<br\s*/?>", "\n", doc, flags=re.I)
    doc = re.sub(r"<h[1-6][^>]*>", "\n\n## ", doc, flags=re.I)
    doc = re.sub(r"<[^>]+>", " ", doc)
    doc = html.unescape(doc)
    # Collapse whitespace, keep paragraph breaks.
    doc = re.sub(r"[ \t]+", " ", doc)
    doc = re.sub(r"\n[ \t]+", "\n", doc)
    doc = re.sub(r"\n{3,}", "\n\n", doc)
    return doc.strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    arg = sys.argv[1]
    path = arg if os.path.isfile(arg) else os.path.join(GUIDE_DIR, arg)
    print(extract(path))
