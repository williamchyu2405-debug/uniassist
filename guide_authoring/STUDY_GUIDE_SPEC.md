# Study Guide — Master Spec & Instructions

The **set instructions** for turning a week's lecture into a study guide that matches
the "clinical atlas" style and holds a consistent, university-level standard — no matter
what material goes in. This is the recipe that recreates the deleted Claude project.

Companion file: **`_template.html`** — a ready-to-fill HTML skeleton whose styling is
copied byte-for-byte from a real guide. Fill its `{{PLACEHOLDERS}}`.

---

## How to run it each week

**Primary path — hand this + your material to Claude Code (recommended).**
1. Drop the week's **screenshots and/or PDF** into a folder (e.g. `~/Downloads/`).
2. Say: *"Make a study guide from these, following `guide_authoring/STUDY_GUIDE_SPEC.md`."*
   Give the **unit code, week, topic**, and slide order if it isn't obvious.
3. Claude Code reads the pages, **embeds your real figures as base64**, writes the
   finished self-contained `.html`, and (on request) drops it into `static/guides/` +
   adds the `guides.json` entry so it shows at `/guides`.

> Why Claude Code and not a browser chat: only a tool that can read your image/PDF files
> can emit the **real figures as base64**. A chat model can describe a pasted image but
> cannot reproduce its exact bytes. If you *do* recreate a claude.ai project from this
> spec, everything applies except the figures — you'd insert those separately.

---

## The house rules (non-negotiable)

These are what keep the quality constant regardless of the input.

1. **Completeness — omit NOTHING.** Every slide, figure, labelled diagram, definition,
   list, and self-test in the provided material must appear in the guide. The material is
   the **foundation you build on** — never drop, skip, or abbreviate its content.
2. **Then go deeper.** On top of full coverage, add the mechanism, the *why*, analogies,
   and connections so the concept is genuinely understood at uni level. Put this added
   depth in the coloured boxes (esp. **Reasoning**) so it's always distinguishable from
   the source content.
3. **Grounded, never invented.** Added depth must be correct and must never contradict the
   material. **Every Plate is a real figure from the material** — no fabricated diagrams.
4. **Decode, don't transcribe.** Rewrite slide content into plain, precise language a
   sharp tutor would use. Define every piece of jargon on first use.
5. **Reference every useful diagram to teach — don't just show it.** Every diagram/figure
   in the material that helps explain a concept becomes a numbered Plate with a Label Key
   decoding *every* labelled part — **and the surrounding prose must point to it by name**
   ("as **Plate 2.1** shows…", "trace the arrow in **Plate 1.3**…") so the figure does
   real explanatory work. If a diagram is worth including, it's worth referring to in the
   explanation. Never leave a Plate stranded with no text that uses it.
6. **Answer the self-tests.** Any quiz/self-check question in the material is reproduced
   and answered inline in a **Check yourself** box.
7. **Self-contained + on-brand.** One `.html` file, the exact design system below, images
   base64-embedded, no external assets except Google Fonts.

---

## Inputs

- **Screenshots** of slides and/or a **PDF** of the deck/module.
- Per guide: **unit code**, **week number**, **topic/lecture title**, institution.
- If ordering matters, a note on slide sequence. Otherwise infer it from the material.

## Output & filing

- Filename: descriptive, e.g. `respiratory_anatomy_pt1.html` or
  `<topic>_<unit>_wk<NN>.html`.
- Save into `static/guides/`, then append one entry to `static/guides/guides.json`:
  `{ file, unit, subject, title, week, date (ISO), blurb, accent }`.
- It appears at **`/guides`** automatically, newest first. (Public link:
  `https://medvault.up.railway.app/guides` — live after `git push`.)

---

## Design system (do not alter)

Copied from the guides; the template already carries the full CSS.

- **Palette:** paper `#F7F5F0`, ink `#1C2321`, muted `#55605C`; accents deep-teal `#0E7C7B`,
  oxblood `#8C2B2B`, ochre/`nerve` `#B08512`.
- **Type (Google Fonts):** Newsreader (display serif — titles), IBM Plex Sans (body),
  IBM Plex Mono (labels, `§` codes, tags).
- **Feel:** clean clinical atlas — generous whitespace, mono micro-labels, serif headings,
  `§` section codes, figure "plates" with label keys, colour-coded callout boxes.
- **Accent per unit** (keep one colour per unit so the gallery reads consistently):
  | Unit | accent |
  |------|--------|
  | MEDI2200 | `ochre` |
  | MHHS2402 | `oxblood` |
  | *(next new unit)* | `teal`, then cycle |

---

## Anatomy of a guide (page order)

1. **Sidebar nav** (`<details class="nav">`) — brand line, title, "How to use", then one
   link per section/subsection (subsections get `class="sub"`), ending in the recall link.
2. **Hero** — eyebrow (`UNIT · Week N · Lecture`), `h1.title` with an italic `.thin` span,
   one-line `lede`, and a `.meta` row (Covers / Figures / Self-tests).
3. **"How to use this guide"** legend — reusable; explains reference codes, Plates, Label
   Keys and the four tags. Leave as-is.
4. **Sections** `§0, §1, …` — one per lecture part/theme. Each: `sec-head` (`§` code +
   part label) → `sec-title` → one-line italic `sec-tag` → `divider` → `lead-note` → the
   content, assembled from the component kit below. Subsections are `§N.N`.
5. **Recall checklist** — closes each major section: the section's must-knows as ticks.
6. **Footer** — "Built from:" provenance line + a "what's next" `nextcard`.

---

## Component kit — when to use each

(Exact HTML for every one of these is in `_template.html`. This is the *when*.)

| Component | Use it for |
|-----------|-----------|
| **Section** `§N` | Each major part/theme of the lecture. |
| **Subsection** `h3.sub` `§N.N` | A distinct sub-topic; give it a nav entry + reference code. |
| **Sub-subheading** `h4.subsub` | A minor heading inside a subsection. |
| **Plate + Label Key** | Every figure. Plate = the real image + caption + source; Key = a `<dl>` decoding each labelled part. **This is the core unit — one per figure.** |
| **Reasoning** box (`box why`, teal) | The *why* / mechanism — **your main tool for going deeper** than the slide. |
| **Check yourself** box (`box active`, grey) | Reproduce and answer a self-test question from the material. |
| **Memory hook** box (`box mnem`, ochre) | A mnemonic or trick to lock it in. |
| **Clinical / real-world** box (`box clin`, oxblood) | Why it matters beyond the diagram. |
| **Clean list** `ul.clean` / `ol.clean` | Feature lists / ordered steps. |
| **Comparison table** `tbl-wrap > table` | Side-by-side contrasts (e.g. A vs B). |
| **Recall checklist** `.recall` | End-of-section rapid revision. |
| Inline: `<strong>`, `<em>`, `<mark>` | Bold key terms; italic for nuance; `<mark>` for the one must-know phrase. |

---

## Voice

- **Do:** decode every slide in plain language; always name the *why*; add a mnemonic where
  it helps; keep sentences tight; use the material's own figures **and cite each Plate in
  the prose** so the explanation walks the reader through the diagram.
- **Don't:** omit any source content; invent or redraw figures; contradict the lecture;
  pad with filler; assume knowledge without defining it.

---

## Pre-ship checklist

- [ ] **Every** slide, figure, list and self-test from the material is represented (nothing dropped).
- [ ] Every useful diagram from the material is included as a Plate — and **referenced by name in the prose** to explain the concept (no stranded figures).
- [ ] Every Plate is a real figure from the material and has a Label Key covering **each** labelled part.
- [ ] Added depth is correct, grounded, and lives in the coloured boxes.
- [ ] Every self-test question is reproduced and answered.
- [ ] Each major section ends with a recall checklist.
- [ ] Nav links, `§` codes and `id`s all match; the file renders self-contained.
- [ ] Saved to `static/guides/` and added to `guides.json` (correct unit accent, ISO date).
