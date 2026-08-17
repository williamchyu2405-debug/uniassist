#!/usr/bin/env python3
"""Crop figures out of PNG screenshots. Usage: crop_png.py <spec.json> <outdir>
spec: [{"src":"path.png","box":[l,t,r,b] fractions,"out":"name","fmt":"jpg|png","maxw":1400}]"""
import sys, json, os
from PIL import Image
spec = json.load(open(sys.argv[1])); outdir = sys.argv[2]
os.makedirs(outdir, exist_ok=True)
cache = {}
for c in spec:
    if c["src"] not in cache: cache[c["src"]] = Image.open(c["src"])
    im = cache[c["src"]]; W, H = im.size
    l, t, r, b = c["box"]
    crop = im.crop((int(l*W), int(t*H), int(r*W), int(b*H)))
    maxw = c.get("maxw", 1400)
    if crop.width > maxw: crop = crop.resize((maxw, int(crop.height*maxw/crop.width)), Image.LANCZOS)
    fmt = c.get("fmt", "jpg"); out = os.path.join(outdir, c["out"] + ("." + ("jpg" if fmt=="jpg" else "png")))
    if fmt == "jpg": crop.convert("RGB").save(out, "JPEG", quality=88, optimize=True)
    else: crop.save(out, "PNG", optimize=True)
    print(f'{c["out"]:10s} {crop.size} {os.path.getsize(out)//1024}KB')
