# Guide build tools

Small helper scripts for turning a lecture PDF into a study guide (see `../STUDY_GUIDE_SPEC.md`).
They need the project venv, which already has `pdfplumber` + `pypdfium2` + `Pillow`
(no poppler / PyMuPDF needed):

```bash
VP=../../venv/bin/python   # or /Users/will/uniassist/venv/bin/python
```

## The pipeline

1. **Extract** — per-page text + rendered page images.
   ```bash
   $VP extract.py "<lecture.pdf>" out        # writes out/meta.json + out/pNNN.png (scale 2.0)
   ```
   Read the text (via `meta.json`) to plan sections; view the `pNNN.png` renders to pick figures.

2. **Crop** — cut each figure out of its page, tight to the diagram + labels.
   Write a spec listing fractional crop boxes, then run:
   ```json
   [ {"page":8, "box":[0.03,0.15,0.98,0.93], "out":"fig_0_1", "fmt":"jpg"} ]
   ```
   ```bash
   $VP crop.py "<lecture.pdf>" crops.json figs   # renders at scale 4.0, writes figs/<out>.<fmt>
   ```
   Iterate the fractional `box` until the crop is tight with **no adjacent prose and no
   source/copyright text** (crop those out — usually bottom-right or a side column).

3. **Assemble** — splice the template head + scripts, inject the digest, body and base64 figures.
   ```bash
   $VP assemble.py "<Title>" digest.json body.html figs \
       ../../static/guides/<file>.html ../../docs/<file>.html
   ```
   Reference figures in `body.html` as `{{FIG:fig_0_1}}` — assemble injects the base64 data URI
   from `figs/`. The head CSS + the genquiz/sg-lightbox scripts come straight from
   `../_template.html`, so **the multi-MB base64 never has to pass through the model's context** —
   you only author the digest + body prose with figure placeholders.

## Then (per the spec)

- Add the manifest entry to **both** `static/guides/guides.json` and `docs/guides.json`.
- Add a `guide_quizzes.json` entry (~30 MCQs).
- Serve locally to check: `python3 -m http.server` in `static/guides/`.
- Commit locally; push (Railway auto-deploys) only when Will asks.
