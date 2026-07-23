# MedVault — Claude Code Project Context

## What this is
Medical/science study web app for university modules. Features: quiz generation, flashcards, slides, knowledge graph, dashboard, web clipper for SCORM content.

## Stack
- **Backend**: FastAPI + SQLite, served on Railway
- **Frontend**: Vanilla JS + Tailwind CSS, static files served by FastAPI
- **AI**: Anthropic API (Claude) for all generation
- **Deploy**: `git push origin main` → Railway auto-deploys (no manual step)

## Key URLs
- Production: `https://medvault.up.railway.app`
- Source content: `ilearn.mq.edu.au` (Moodle SCORM player — Articulate Rise modules)

## Security / Secrets
- Access code: `WILLCHI` (gates the whole app)
- `ANTHROPIC_API_KEY` lives in `.env` — never commit, never expose in code
- `.env` is in `.gitignore`

## Model constants (in main.py)
```python
MODEL = "claude-sonnet-4-6"       # quiz, slides — needs quality
HAIKU = "claude-haiku-4-5-20251001"  # flashcards — speed/cost
```

## Key files
| File | Purpose |
|------|---------|
| `main.py` | FastAPI app, all API routes, AI prompt logic |
| `static/app.js` | All frontend JS — quiz, flashcards, slides, graph, dashboard |
| `static/index.html` | Single-page app shell; asset URLs use `?v=__ASSET_VER__` |
| `static/style.css` | Custom CSS on top of Tailwind |
| `static/bookmarklet.html` | Three bookmarklets: Send to MedVault, Send to Claude, Diagnose Page |

## Important implementation details

### Cache busting
`index.html` asset URLs use `?v=__ASSET_VER__` placeholder. The root route `/` in `main.py` reads `index.html`, replaces the placeholder with an mtime-based version string, and serves with `Cache-Control: no-cache`. **Never hardcode version strings** — they're injected at runtime.

### Content cap
`GEN_CONTENT_CHARS = 50000` — raised from 24000 to handle full multi-lesson SCORM modules (~30-42k chars). Don't lower this.

### Quiz grounding guard
After AI generation, a post-processing step checks each question's anchor terms against the source text and drops questions with no match. This prevents off-syllabus hallucination. The guard is in `generate_quiz()` in `main.py`.

### Difficulty levels
`easy / medium / hard / mixed / daredevil` — Hard and Dare Devil are aimed at mining niche details from the actual source text, NOT board-exam external knowledge. Dare Devil badge uses `😈`.

### SM-2 spaced repetition
Flashcard scheduling uses the SM-2 algorithm. Don't replace with a simpler system.

## SCORM / Web clipper architecture
The SCORM player at ilearn is a nested iframe structure:
- Outer Moodle → `loadSCO.php` → `blank.html` (Articulate Rise shell)
- Rise re-renders `blank.html` on every lesson navigation — DOM nodes go stale immediately
- Lesson navigation uses in-page hash routes (`<a href="#/lessons/…">`) — `preventDefault()` on these blocks switching
- **Bookmarklet fix**: re-queries live DOM nodes by name before each click (not cached), only blocks `isNavLink()` anchors
- Re-drag bookmarklets from `bookmarklet.html` after any code change — the JS is baked in at drag time

## Dashboard
- Performance chart: per-material quiz accuracy (not topic — materials are the unit)
- Activity chart: 7-day rolling heatmap
- Mistakes to Review: retake quiz from wrong answers, cleared when answered correctly
- Upcoming Exams card: **removed** (was dead/useless)

## Knowledge graph
- Camera system with zoom (scroll), pan (drag), recenter (double-click)
- Physics: `BASE_REPULSION=5200`, `SPRING_LEN=150`, `DAMPING=0.88`, `MAX_V=18`
- Soft quadratic MIN_GAP push (not constant shove — prevents jitter)

## Slide templates
`title`, `bullets`, `compare`, `diagram`, `stat`, `keyterms`, `takeaway` — AI picks based on section shape. Require variety across a deck.

## Russian module (Languages → Russian)
- **Zero-API**: static 5-phase curriculum (`RU_CURRICULUM` in `app.js`) + a hand-authored seed deck (`RUSSIAN_SEED` in `main.py`). No AI calls anywhere in this module.
- **Spaced repetition** reuses the shared `sm2_schedule()` — the in-app "Drill" tab replaces external Anki. Tables: `russian_vocab` (SM-2 columns mirror `flashcards`), `russian_review_log`, `russian_progress`.
- **Endpoints**: `/api/russian/vocab` (GET lazy-seeds on first call · POST add · DELETE), `/api/russian/drills`, `/api/russian/vocab/{id}/result` (clone of `/api/flashcards/{id}/result`), `/api/russian/stats`, `/api/russian/progress`.
- **Audio** is browser TTS with a `ru-RU` voice (`ruSpeakText` in `app.js`) — free, but silent if the OS has no Russian voice installed.
- Phases: 0 Cyrillic alphabet (interactive grid) · 1 survival · 2 travel · 3 conversation · 4 maintain (checklist, no drill cards).

## Deploy checklist
1. `git add <files>` (specific files, not `-A`)
2. `git commit -m "..."`
3. `git push origin main`
4. Wait ~30s for Railway to rebuild
5. Hard-refresh browser (Cmd+Shift+R) to bust cache
6. Re-drag bookmarklets if `bookmarklet.html` changed
