# Quiz-bank regeneration — working notes

Goal: replace every gallery's questions in `guide_quizzes.json` with a fresh,
harder, **tell-free** set, then deploy (which auto-wipes old progress when a
guide's stem-set changes — see `_ensure_guide_quiz` in main.py).

## The two giveaways we are killing
1. **Length tell** — correct option being the uniquely longest / most detailed.
2. **Bracket tell** — a parenthetical clarifier only the correct option has.
Both are enforced mechanically by `tools/qbank_lib.py::check_question`:
- 4 options, valid A–D, non-empty stem/explanation, difficulty ∈ {easy,medium,hard}
- option word-spread ≤ 4; correct option never uniquely longest (when spread ≥ 2)
- correct option may not carry a lone parenthetical
- explanation must not reference "the material/source/text/notes/study/passage"
- **daredevil is removed** — reclassify any old daredevil question to `hard`.

## Per-guide workflow (no API spend — authored by hand here)
1. Dump the existing vetted facts + content:
   `python3 - <<'PY' ... bank[key] ... PY` (topic, stem, correct option, explanation)
2. Write `regen/<key_stem>.py`. It loads title/subject/unit/content from the
   current bank (so only questions change) and calls `emit(KEY, META, Q)`.
3. Run it; fix any reported violations; it writes `regen/<key>.html.json`.

Authoring discipline that avoids fix-cycles: keep all four options within ~2–3
words of each other, and if lengths differ make a **distractor** the longest.
Make distractors real traps (adjacent facts), not throwaways. Difficulty mix
target ≈ 15–20% easy / ~50% medium / ~30% hard (the approved "pilot mix").

## Status / assembly / deploy
- `python3 tools/assemble_bank.py --status`  → done vs missing, per-fragment validation
- `python3 tools/assemble_bank.py --write`   → backs up + writes guide_quizzes.json
  (refuses if any gallery is missing a fragment or any question violates a rule)

## Progress (39/39 done ✅ — all fragments authored & validating clean)
- MEDI2004 pharmacology: 7/7 ✅
- MEDI2200 cell biology: 6/6 ✅
- SOCI1010 (everyday life): 5/5 ✅
- MHHS2401 (upper/lower limb + bone/muscle physiology): 14/14 ✅
- MHHS2402 (respiratory + cardiovascular): 7/7 ✅
Total: 1253 questions across 39 galleries. `assemble_bank.py --status` shows
no missing fragments and no rule violations. NOT yet deployed — run
`python3 tools/assemble_bank.py --write` to back up + write guide_quizzes.json
(this re-seeds each guide's questions on next load, wiping old per-user progress).
