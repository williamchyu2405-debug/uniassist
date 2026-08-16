#!/usr/bin/env python3
"""Extract per-page text + image bboxes, and render pages to PNG.
Usage: extract.py <pdf> <outdir> [scale] [first] [last]
Writes <outdir>/meta.json and <outdir>/pNNN.png (rendered pages).
"""
import sys, os, json
import pdfplumber
import pypdfium2 as pdfium

pdf_path = sys.argv[1]
outdir   = sys.argv[2]
scale    = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
first    = int(sys.argv[4]) if len(sys.argv) > 4 else 1
last     = int(sys.argv[5]) if len(sys.argv) > 5 else 0   # 0 = all
os.makedirs(outdir, exist_ok=True)

# --- text + image bboxes via pdfplumber ---
meta = []
with pdfplumber.open(pdf_path) as plumber:
    n = len(plumber.pages)
    lo, hi = first, (last or n)
    for i in range(lo-1, hi):
        page = plumber.pages[i]
        txt = page.extract_text() or ""
        imgs = [{"x0": round(im["x0"],1), "top": round(im["top"],1),
                 "x1": round(im["x1"],1), "bottom": round(im["bottom"],1),
                 "w": round(im["x1"]-im["x0"],1), "h": round(im["bottom"]-im["top"],1)}
                for im in page.images]
        meta.append({"page": i+1, "pw": round(page.width,1), "ph": round(page.height,1),
                     "n_img": len(imgs), "images": imgs, "text": txt})

# --- render pages via pdfium ---
doc = pdfium.PdfDocument(pdf_path)
lo, hi = first, (last or len(doc))
for i in range(lo-1, hi):
    pg = doc[i]
    pil = pg.render(scale=scale).to_pil()
    pil.save(os.path.join(outdir, f"p{i+1:03d}.png"))

json.dump(meta, open(os.path.join(outdir, "meta.json"), "w"), ensure_ascii=False)
print(f"OK pages {lo}-{hi} of {len(doc)}  scale={scale}  -> {outdir}")
print("sample text p"+str(lo)+":", (meta[0]["text"][:300].replace(chr(10),' | ')) if meta else "(none)")
print("img counts:", [(m["page"], m["n_img"]) for m in meta[:12]])
