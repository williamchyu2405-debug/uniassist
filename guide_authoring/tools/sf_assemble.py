#!/usr/bin/env python3
"""Assemble a PUBLIC slide-forward study guide (self-contained, base64 images)
from a content spec, reusing an existing guide's head-CSS + tail-scripts verbatim.

The design-system CSS and all the interactive scripts (lightbox, recall cloze,
theme, nav, predict, generate-quiz) are sliced straight out of the autonomic
pharmacology guide so every new build stays pixel-identical to the template and
automatically inherits fixes (e.g. the recall cue-detection fix).

Driver scripts import `build(spec, out_path)` and pass a spec dict. See
renal_w10_spec.py / renal_w11_spec.py for the content format.
"""
import os, io, json, base64
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TEMPLATE = os.path.join(ROOT, "static/guides/private/autonomic_pharmacology_medi2004_wk10_l19.html")

DIGEST_MARK = '<script type="application/json" id="sg-digest">'
TAIL_FIND = '// ---- generate a quiz from the embedded digest'
OLD_TITLE = '<title>Autonomic Pharmacology · MEDI2004 W10 L19 — Study Guide</title>'
OLD_COMMENT = '<!-- MEDI2004 W10 L19 — Autonomic pharmacology. Slide-forward deep-explain study guide. -->'


def _template_parts():
    t = open(TEMPLATE, encoding="utf-8").read()
    head = t[:t.index(DIGEST_MARK)]
    ti = t.index(TAIL_FIND)
    si = t.rfind('<script>', 0, ti)
    tail = t[si:]
    return head, tail


def _img_uri(workdir, slide_no, max_w=1700, quality=82):
    path = os.path.join(ROOT, workdir, f"p{slide_no:03d}.png")
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def _plate(workdir, n, cap, alt, oneline=False):
    uri = _img_uri(workdir, n)
    bar = f'<div class="plate-bar"><span class="pno">SLIDE {n}</span><span class="pcap">{cap}</span></div>'
    img = f'<img src="{uri}" alt="{alt}" loading="lazy">'
    if oneline:
        return f'<figure class="plate slide">{bar}{img}</figure>'
    return f'      <figure class="plate slide">\n        {bar}\n        {img}\n      </figure>'


def _block(workdir, b):
    kind = b[0]
    if kind == "plate":
        _, n, cap, alt = b
        return _plate(workdir, n, cap, alt)
    if kind == "grid":
        cells = "".join("        " + _plate(workdir, n, cap, alt, oneline=True) + "\n"
                        for (n, cap, alt) in b[1])
        return f'      <div class="slidegrid">\n{cells}      </div>'
    if kind == "exp":
        return f'      <p class="slideexp">{b[1]}</p>'
    if kind == "lead":
        return f'      <p class="lead-note">{b[1]}</p>'
    if kind == "box":
        _, bkind, lab, body = b
        return f'      <div class="box {bkind} slidenote"><span class="lab">{lab}</span><p>{body}</p></div>'
    raise ValueError("unknown block " + kind)


def _recall(rc, first=False):
    idattr = ' id="recall"' if first else ''
    items = "\n".join("          " + it for it in rc["items"])
    return (f'    <div class="recall"{idattr}>\n'
            f'      <div class="rhead"><span class="tag t-recall" style="padding:2px 8px">R</span> {rc["head"]}</div>\n'
            f'      <div class="rbody">\n        <ul>\n{items}\n        </ul>\n      </div>\n    </div>')


def _digest_json(spec):
    d = {
        "unit": spec["unit"], "week": spec["week"], "title": spec["title"],
        "subject": spec["subject"], "source": spec["source"], "sections": [],
    }
    for s in spec["sections"]:
        dg = s.get("digest")
        if not dg:
            continue
        d["sections"].append({
            "code": s["code"], "title": s["title"],
            "key_points": dg.get("key_points", []),
            "self_tests": dg.get("self_tests", []),
        })
    return json.dumps(d, ensure_ascii=False, indent=2)


def build(spec, out_path):
    head, tail = _template_parts()
    wd = spec["workdir"]

    new_title = f'<title>{spec["title"]} · {spec["unit"]} Wk{spec["week"]} — Study Guide</title>'
    new_comment = f'<!-- {spec["unit"]} Wk{spec["week"]} — {spec["title"]}. Slide-forward deep-explain study guide. -->'
    head = head.replace(OLD_TITLE, new_title).replace(OLD_COMMENT, new_comment)

    # nav
    nav_links = "\n".join(
        f'      <a href="#{s["id"]}"><span class="code">{s["code"].replace("§","§")}</span>{s["title"]}</a>'
        for s in spec["sections"])
    # masthead + hero + howto
    n_parts = len([s for s in spec["sections"] if s["code"].startswith("§") and s["code"] != "§0"])
    legend = (
        '      <div class="legend-grid">\n'
        '        <div class="legend-item"><span class="tag t-why">Why / mechanism</span><br>The step the slide draws but doesn\'t explain.</div>\n'
        '        <div class="legend-item"><span class="tag t-mnem">Exam hook</span><br>The discriminating fact or framework that earns the mark.</div>\n'
        '        <div class="legend-item"><span class="tag t-clin">Clinical</span><br>Where this shows up in a patient — and what goes wrong.</div>\n'
        '      </div>')

    mid = []
    mid.append(DIGEST_MARK + "\n" + _digest_json(spec) + "\n</script>\n")
    mid.append('<div class="layout">')
    mid.append('<button type="button" class="navreopen" title="Show sidebar">&#10095;</button>\n')
    mid.append('  <details class="nav" open>')
    mid.append('    <summary>Contents</summary>')
    mid.append('    <div class="navbody">')
    mid.append('      <div class="rc" role="group" aria-label="Reading theme">')
    mid.append('        <span class="rclab">Theme</span>')
    mid.append('        <button type="button" data-theme="ivory" title="Ivory" style="background:#FAF8F3"></button>')
    mid.append('        <button type="button" data-theme="sepia" title="Sepia" style="background:#F2E8D5"></button>')
    mid.append('        <button type="button" data-theme="slate" title="Slate" style="background:#ECEEF0"></button>')
    mid.append('      </div>')
    mid.append('      <button type="button" class="navtoggle">&#10094;&nbsp; Hide sidebar</button>')
    mid.append(f'      <div class="brand">{spec["brand"]}</div>')
    mid.append(f'      <div class="brandsub">{spec["brandsub"]}</div>')
    mid.append('      <a href="#howto">How to use this guide</a>')
    mid.append('      <div class="grp">Sections</div>')
    mid.append(nav_links)
    mid.append('      <a href="#recall" class="sub"><span class="code">R</span>Recall checklists</a>')
    mid.append('    </div>')
    mid.append('  </details>\n')
    mid.append('  <main class="content">')
    mid.append('  <div class="reading">\n')
    mid.append('    <header class="hero">')
    mid.append(f'      <div class="eyebrow">{spec["eyebrow"]}</div>')
    mid.append(f'      <h1 class="title">{spec["h1"]} <span class="thin">{spec["h1thin"]}</span></h1>')
    mid.append(f'      <p class="lede">{spec["lede"]}</p>')
    mid.append('      <div class="meta">')
    mid.append(f'        <span><b>Covers</b> {spec["n_slides"]} slides · {n_parts} parts</span>')
    mid.append('        <span><b>Figures</b> the lecture\'s own slides</span>')
    mid.append('        <span><b>Self-tests</b> interactive recall</span>')
    mid.append('        <span><button class="genquiz" id="genquiz" type="button">Generate quiz &rarr;</button></span>')
    mid.append('      </div>')
    mid.append('    </header>\n')
    mid.append('    <div class="howto" id="howto">')
    mid.append('      <h3>How to use this guide</h3>')
    mid.append(f'      <p style="margin-top:0;color:var(--ink-soft);font-size:15px">{spec["howto"]}</p>')
    mid.append(legend)
    mid.append('    </div>\n')

    first_recall = True
    for s in spec["sections"]:
        mid.append(f'    <!-- {s["code"]} {s["title"]} -->')
        mid.append(f'    <section id="{s["id"]}">')
        mid.append(f'      <div class="sec-head"><span class="sec-code">{s["code"]}</span><span class="sec-lo">{s["lo"]}</span></div>')
        mid.append(f'      <h2 class="sec-title">{s["title"]}</h2>')
        mid.append(f'      <p class="sec-tag">{s["tag"]}</p>')
        mid.append('      <hr class="divider">')
        if s.get("lead"):
            mid.append(f'      <p class="lead-note">{s["lead"]}</p>')
        for b in s["blocks"]:
            mid.append(_block(wd, b))
        mid.append('    </section>\n')
        if s.get("recall"):
            mid.append(_recall(s["recall"], first=first_recall))
            mid.append("")
            first_recall = False

    mid.append('    <div class="foot">')
    mid.append(f'      <p><b>Built from:</b> {spec["source"]}. Personal study aid: the lecture\'s own slides, each explained in depth.</p>')
    mid.append('      <div class="nextcard">')
    mid.append(f'        <b>All {spec["n_slides"]} content slides covered, in order.</b> Click any slide to enlarge; quote a code (e.g. §3) to go deeper, or hit <b>Generate quiz</b> (top) to spin one up from this guide.')
    mid.append('      </div>')
    mid.append('    </div>\n')
    mid.append('  </div>')
    mid.append('  </main>')
    mid.append('</div>\n')

    html_out = head + "\n".join(mid) + "\n" + tail
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    kb = os.path.getsize(out_path) / 1024
    print(f"wrote {out_path}  ({kb:.0f} KB)")
    return out_path
