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
   finished self-contained `.html`, drops it into `static/guides/` (+ `static/guides/private/`
   and `docs/` as appropriate), and **ALWAYS updates the gallery** — see next.

**Always update the gallery (standing rule).** Making or updating a guide is not done until
the gallery reflects it. Update the manifests so the entry (title, week, ISO date, blurb) is
present and current:
- `docs/guides.json` — the **public** GitHub Pages copy (drives the live `/guides` page).
- `static/guides/guides.json` — in-app public manifest; `static/guides/guides.local.json` —
  in-app **private** manifest (gitignored) for guides that shouldn't be published.
- Reinstall the guide file to `docs/` (public) and/or `static/guides/private/` (private).
If only a guide's *content* changed (same filename), the manifest entry already points to it —
still verify the blurb/date are accurate.

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
2. **Then go deeper — EXPLAIN, don't list.** This is the point of the guide, not an
   optional extra. A guide that only decodes slides into tables/bullets is a glorified
   list and has failed. On top of full coverage, weave in the **mechanism**, the ***why***,
   analogies and connections so the concept is genuinely understood at uni level, and say
   **what it means / what goes wrong** in practice. Concretely:
   - **Every `§` section carries at least one Reasoning box** (`box why`) — the mechanism /
     form-follows-function behind that section's facts — **and a Clinical box** (`box clin`)
     wherever a real-world or clinical consequence plausibly exists (it almost always does).
     Sparse boxes = under-delivered; the *reasoning + clinical emphasis is the house
     signature*.
   - Prefer **explanatory prose** that states the fact **and then its why/consequence** over
     a bare bullet. Tables/lists are for the source facts; the understanding lives around them.
   - For every structure ask *why is it shaped/placed like this?* (Reasoning) and *what
     happens when it fails?* (Clinical) — answer both.
3. **Grounded, never invented.** Added depth must be correct and must never contradict the
   material. **Every Plate is a real figure from the material** — no fabricated diagrams.
4. **Decode, don't transcribe.** Rewrite slide content into plain, precise language a
   sharp tutor would use. Define every piece of jargon on first use.
5. **Reference every useful diagram to teach — don't just show it.** Every diagram/figure
   in the material that helps explain a concept becomes a numbered Plate with a Label Key
   decoding *every* labelled part — **and the surrounding prose must point to it by name**
   ("as **Plate 2.1** shows…", "trace the arrow in **Plate 1.3**…") so the figure does
   real explanatory work. If a diagram is worth including, it's worth referring to in the
   explanation. Never leave a Plate stranded with no text that uses it. Each **Label Key**
   entry gives the part's **function and why it matters** — not just a name.
6. **No filler questions in the guide.** Do **not** embed easy in-guide MCQs or "check
   yourself" widgets — they waste time. Real self-testing is done by **generating a quiz from
   the guide** (the `#sg-digest` → MedVault, see below), where *you* pick the difficulty. Keep
   the guide itself for teaching, figures and recall.
7. **Worked examples for anything quantitative.** Numbers, formulae or calculations get a
   full **step-by-step worked example** (`.worked`) — show every step and its reasoning,
   not just the result.
8. **Self-contained + on-brand.** One `.html` file, the exact design system below, images
   base64-embedded, no external assets except Google Fonts.

---

## Inputs

- **Screenshots** of slides and/or a **PDF** of the deck/module.
- Per guide: **unit code**, **week number**, **topic/lecture title**, institution.
- If ordering matters, a note on slide sequence. Otherwise infer it from the material.

## Output & filing

- Filename: descriptive, e.g. `respiratory_anatomy_pt1.html` or
  `<topic>_<unit>_wk<NN>.html`.
- Save into `static/guides/`, then append one entry to `static/guides/guides.json`
  (and `docs/guides.json` for the public copy): `{ file, unit, subject, title, week, date (ISO), blurb, accent }`.
- It appears at **`/guides`** automatically, newest first. **Two live hosts, both auto-updating
  on `git push origin main`** (deploy only when Will asks — see the workflow memory):
  - **Railway app** — `medvault.up.railway.app/guides` serves the in-app gallery from
    `static/guides/`, with the working **quiz features** (the zero-API "Quiz" button seeded from
    `guide_quizzes.json`, and the Generate-quiz button — both need the backend). Rebuilds ~30–60 s
    after a push. *(Railway is alive — an earlier note here that said otherwise was wrong.)*
  - **GitHub Pages** — the static public copy from the `docs/` bundle, ~1 min after a push that
    touches `docs/`. No backend, so the quiz buttons don't function there.
  Keep `static/guides/` and `docs/` (and their `guides.json`) in sync so both hosts match.

---

## Design system (do not alter)

Copied from the guides; the template already carries the full CSS.

- **Palette:** paper `#F7F5F0`, ink `#1C2321`, muted `#55605C`; accents deep-teal `#0E7C7B`,
  oxblood `#8C2B2B`, ochre/`nerve` `#B08512`.
- **Type (Google Fonts):** Newsreader (display serif — titles), IBM Plex Sans (body),
  IBM Plex Mono (labels, `§` codes, tags).
- **Feel:** clean clinical atlas — generous whitespace, mono micro-labels, serif headings,
  `§` section codes, figure "plates" with label keys, flowing callout margin-notes.
- **Unified style system (2026-09, baked into `_template.html` — new guides inherit it, nothing to wire):**
  - **Reading themes** — Ivory / Sepia / Slate swatches in the sidebar (`.rc`), persisted in `localStorage`.
  - **Collapsible sidebar** — "Hide sidebar" (`.navtoggle`) + reopen tab (`.navreopen`), persisted.
  - **Frameless plates** — the diagram floats on a soft-shadowed white mount with a quiet caption line (no dark box/title bar); click-to-enlarge lightbox stays.
  - **Active-recall checklists** — the `<b>` key terms in each `.recall` item auto-become tap-to-reveal cloze blanks with a progress bar (`sg-recall-js` — no per-guide wiring; just write the checklist normally).
  - **Flowing callouts** — `.box why/mnem/clin/active` render as margin-notes (slim accent rule + soft wash), NOT hard-bordered filled boxes.
  - **Subtle paper texture** on the background; **optional Predict beat** (`.predict` — a guess-before-you-read block with a Reveal button; use early in a section where it adds punch).
  - These are delivered via scoped `body.sg-up` override blocks (`sg-style-upgrade`/`-theme-css`/`-nav-css`/`-callout-css` + `sg-predict-css`) already in the template. To retro-fit an OLD guide, inject the same blocks (`/tmp/apply_upgrade.py`, `apply_callouts.py`).
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
   one-line `lede`, and a `.meta` row (Covers / Figures / Recall).
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
| **Plate label — depth** | Each `<dt>/<dd>` = the part's **function + why it matters**, not just its name. |
| **Reasoning** box (`box why`, teal) | The *why* / mechanism — **your main tool for going deeper** than the slide. |
| **Worked example** `.worked` | Step-by-step quantitative solution; use `<span class="eq">` for formulae. |
| **Memory hook** box (`box mnem`, ochre) | A mnemonic or trick to lock it in. |
| **Clinical / real-world** box (`box clin`, oxblood) | Why it matters beyond the diagram. |
| **Clean list** `ul.clean` / `ol.clean` | Feature lists / ordered steps. |
| **Comparison table** `tbl-wrap > table` | Side-by-side contrasts (e.g. A vs B). |
| **Recall checklist** `.recall` | End-of-section rapid revision. |
| **Study digest** `<script id="sg-digest">` | Compact JSON distillation of the guide (see below). Keep in sync with content. |
| **Generate-quiz button** `#genquiz` | Feeds the digest into MedVault to spin up a quiz (see below). |
| Inline: `<strong>`, `<em>`, `<mark>` | Bold key terms; italic for nuance; `<mark>` for the one must-know phrase. |

---

## Quiz generation & the embedded digest

Every guide carries a compact, base64-free **study digest** so a study generator can make
quizzes/flashcards from it **without** wading through the 2–3 MB rendered HTML — that's the
token saving.

**The digest** — a JSON block near the top of the file:
```html
<script type="application/json" id="sg-digest">
{ "unit": "...", "week": N, "title": "...", "subject": "...", "source": "...",
  "sections": [ { "code": "§0", "title": "...",
                  "key_points": ["atomic fact", "..."],
                  "self_tests": [ {"q": "...", "a": "..."} ] } ] }
</script>
```
- Keep it **in sync** with the guide: one section object per `§` section, `key_points` as
  short atomic facts, every self-test mirrored as `{q, a}`. It's plain, generator-agnostic
  text — portable to any quiz tool.

**The button** — `#genquiz` in the hero reads the digest, flattens it to text and POSTs it to
MedVault's `/api/import-web` (same origin), creating a *material* you can then quiz from.
- Works when the guide is served from MedVault (i.e. the `/guides` gallery). It asks for the
  access code on click (or reads `?ac=` from the URL) and never hardcodes it.
- Guides are **publicly shared**, so friends see the button but can't use it without the code
  — it fails gracefully. The digest is the portable fallback if you paste into another tool.

---

## Quiz questions — make them genuinely hard

The hand-authored bank (`guide_quizzes.json`, one entry per guide keyed by its filename) is what the
`/guides` **"Quiz"** button serves. Its job is to make you **think about the content**, not spot the
answer from surface cues. Write every MCQ so a sharp student who *hasn't studied* still can't guess
it. Kill these tells:

1. **No give-away in the correct option.** Never append a clarifying parenthetical, textbook tag or
   extra qualifier that sits only on the right answer — put that depth in the **`explanation`**, never
   the option text. ✗ `Anchor the sarcomere to the sarcolemma (lateral force transfer)` — the bracket
   flags it.
2. **Parallel options.** All four match in length, grammatical form, specificity and tone. The correct
   answer must **not** be the longest, most detailed, most hedged or only "complete-sounding" one —
   that's the #1 tell ("the thorough answer is usually right"). If the right answer is rich and the
   wrong ones terse, level them all.
3. **Plausible, same-domain distractors that differ by a small, real detail.** Build each distractor
   from a *neighbouring true fact* — swap the protein / location / mechanism / direction for an
   adjacent correct one (dystrophin ↔ titin ↔ nebulin ↔ myosin), so ruling it out requires knowing the
   distinction. **Ban** obviously-wrong, extreme or absolute distractors ("there is no ATP", "calcium
   is excessive") — they're free eliminations.
4. **Force discrimination.** Favour "which is the **most** correct / best", cause-vs-consequence,
   correct ordering, or two options both partly true where one is more precise. Include deliberate
   **traps** where a common misconception is the tempting wrong answer.
5. **Even answer spread.** Distribute the correct letter roughly evenly across A/B/C/D within a bank —
   never let a fixed position (or "the most elaborate option") be a reliable signal.
6. **Reasoning over recognition.** Prefer "what happens if… / why…" and applied scenarios, so the stem
   can't be pattern-matched to a memorised phrase sitting in one option.

**Worked fixes** (the two real tells that prompted this rule):

- ✗ *Dystrophin's role is to:* `Anchor the sarcomere to the sarcolemma (lateral force transfer)` ·
  `Sit at the M-line stabilising myosin` · `Catalyse ATP hydrolysis` · `Align actin at the Z disc` —
  the bracket **and** the extra length give it away.
  ✓ *Dystrophin anchors the sarcomere to the sarcolemma — this transfer of force is:* `Lateral` ·
  `Longitudinal` · `Rotational` · `Radial`; **or** make all four "anchoring" options
  (dystrophin = to sarcolemma / titin = Z-disc to M-line / nebulin = along actin / a Z-disc tether) so
  you must actually know which protein does which. Move "lateral force transfer" into the explanation.
- ✗ *At a long sarcomere tension falls because:* `too little filament overlap for cross-bridges`
  (correct, and the only mechanistic option) · `thin filaments collide` · `there is no ATP` ·
  `calcium is excessive` — the wrong ones are eliminable extremes.
  ✓ *At a long sarcomere tension falls because:* `too few myosin heads can reach actin to form
  cross-bridges` · `the thin filaments overlap and block each other` · `the thick filament jams
  against the Z discs` · `titin is stretched past its elastic limit` — all four are plausible
  length–tension mechanisms; only the first is right (the next two describe the *short*-sarcomere end).

Difficulty tiers still apply (`easy`/`medium`/`hard`/`daredevil`) — harder tiers lean on niche detail
and on discriminating near-identical options, **not** on longer stems. ~25–30 questions per bank.

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
- [ ] Every Plate is a real figure from the material and has a Label Key giving each part's **function + why it matters**.
- [ ] Added depth is correct, grounded, and lives in the coloured boxes.
- [ ] **Reasoning + clinical emphasis delivered:** every `§` section has ≥1 Reasoning box and a Clinical box wherever one plausibly applies; the guide *explains* (mechanism + consequence) rather than just listing facts.
- [ ] **Gallery updated:** entry present/current in `docs/guides.json` (+ `static/guides/guides.json` / `.local.json`); guide reinstalled to `docs/` and/or `static/guides/private/`.
- [ ] **No** easy/filler MCQs embedded in the guide — self-testing is left to the generated quiz.
- [ ] **Quiz-bank questions pose real effort** (see *Quiz questions*): parallel options, no give-away parenthetical or over-long correct answer, plausible same-domain distractors (no eliminable extremes), some traps / "which is MORE right", even A/B/C/D spread.
- [ ] Any quantitative content has a **step-by-step worked example**.
- [ ] `#sg-digest` is present and in sync (one object per section; every self-test mirrored as `{q,a}`).
- [ ] Each major section ends with a recall checklist.
- [ ] Nav links, `§` codes and `id`s all match; the file renders self-contained.
- [ ] Saved to `static/guides/` and added to `guides.json` (correct unit accent, ISO date).
