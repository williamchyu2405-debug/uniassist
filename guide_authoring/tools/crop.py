#!/usr/bin/env python3
"""Crop figures from a PDF per a spec JSON. Usage: crop.py <pdf> <spec.json> <outdir>
spec: [{"page":N,"box":[l,t,r,b] fractions,"out":"name","fmt":"jpg|png","scale":4.0,"maxw":1500}]
"""
import sys, json, os
import pypdfium2 as pdfium
from PIL import Image

pdf_path, spec_path, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(outdir, exist_ok=True)
spec = json.load(open(spec_path))
doc = pdfium.PdfDocument(pdf_path)
cache = {}
def render(page, scale):
    k = (page, scale)
    if k not in cache:
        cache[k] = doc[page-1].render(scale=scale).to_pil()
    return cache[k]

for c in spec:
    im = render(c["page"], c.get("scale", 4.0))
    W, H = im.size
    l, t, r, b = c["box"]
    crop = im.crop((int(l*W), int(t*H), int(r*W), int(b*H)))
    maxw = c.get("maxw", 1500)
    if crop.width > maxw:
        crop = crop.resize((maxw, int(crop.height*maxw/crop.width)), Image.LANCZOS)
    fmt = c.get("fmt", "jpg")
    out = os.path.join(outdir, c["out"] + ("." + ("jpg" if fmt == "jpg" else "png")))
    if fmt == "jpg":
        crop.convert("RGB").save(out, "JPEG", quality=88, optimize=True)
    else:
        crop.save(out, "PNG", optimize=True)
    print(f'{c["out"]:10s} {crop.size} {os.path.getsize(out)//1024}KB {fmt}')
