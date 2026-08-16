#!/usr/bin/env python3
"""Assemble a final guide HTML from template head/scripts + digest + body + base64 figures.
Usage: assemble.py "<Title>" <digest.json> <body.html> <figs_dir> <out1> [out2 ...]
Figure placeholders in body: {{FIG:name}} -> data URI from <figs_dir>/name.(jpg|png)
"""
import sys, os, base64, re
# _template.html sits in guide_authoring/, one level up from this tools/ dir.
TEMPLATE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_template.html")

title, digest_path, body_path, figs_dir = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
out_paths = sys.argv[5:]

tpl = open(TEMPLATE, encoding="utf-8").read()
head = tpl[:tpl.index("</head>") + len("</head>")]
head = head.replace("<title>{{Title}} — Study Guide</title>", f"<title>{title} — Study Guide</title>")

m = tpl.index("// ---- generate a quiz from the embedded digest")
tail_start = tpl.rfind("<script>", 0, m)
tail_end = tpl.index("<!-- /sg-lightbox -->") + len("<!-- /sg-lightbox -->")
tail = tpl[tail_start:tail_end]

digest = open(digest_path, encoding="utf-8").read().strip()
body = open(body_path, encoding="utf-8").read().strip()
digest_block = '<script type="application/json" id="sg-digest">\n' + digest + '\n</script>'
final = head + "\n<body>\n" + digest_block + "\n\n" + body + "\n\n" + tail + "\n</body>\n</html>\n"

def repl(mm):
    name = mm.group(1)
    for ext, mime in (("jpg", "image/jpeg"), ("png", "image/png")):
        p = os.path.join(figs_dir, name + "." + ext)
        if os.path.exists(p):
            b = base64.b64encode(open(p, "rb").read()).decode()
            return f"data:{mime};base64,{b}"
    raise SystemExit("MISSING FIG: " + name)

n_before = len(re.findall(r"\{\{FIG:[a-z0-9_]+\}\}", final))
final = re.sub(r"\{\{FIG:([a-z0-9_]+)\}\}", repl, final)
leftover = re.findall(r"\{\{[^}]+\}\}", final)
if leftover:
    print("WARNING leftover placeholders:", set(leftover))
# validate digest JSON
import json
json.loads(digest)
print(f"figures embedded: {n_before}")
for op in out_paths:
    os.makedirs(os.path.dirname(op), exist_ok=True)
    open(op, "w", encoding="utf-8").write(final)
    print("wrote", op, f"{os.path.getsize(op)//1024}KB")
