#!/usr/bin/env python3
"""Shared helpers for authoring the guide quiz bank.

The point of this module is the *validator*: every regenerated question is run
through `check_question` so the two giveaways the bank suffered from can never
slip back in —
  1. the correct option being the uniquely longest / most detailed one, and
  2. a parenthetical clarifier on the correct option that the distractors lack.
It also enforces structural sanity (4 options, valid letter, no daredevil).
"""
import re

LETTERS = ["A", "B", "C", "D"]
# Longest option may exceed the shortest by at most this many words. The bank's
# old tell was a correct answer 3-6 words longer than the distractors.
MAX_WORD_SPREAD = 4
VALID_DIFF = {"easy", "medium", "hard"}


def option_body(o: str) -> str:
    """Strip a leading 'A. ' / 'B) ' / 'C: ' style label to get clean option text."""
    m = re.match(r"^\s*[A-Da-d]\s*[\.\)\:\-]\s*(.*)$", str(o))
    return (m.group(1) if m else str(o)).strip()


def _has_bracket(text: str) -> bool:
    return "(" in text and ")" in text


def check_question(q: dict) -> list:
    """Return a list of human-readable violation strings ([] == clean)."""
    v = []
    stem = (q.get("question") or "").strip()
    if not stem:
        v.append("empty stem")
    diff = (q.get("difficulty") or "").strip().lower()
    if diff not in VALID_DIFF:
        v.append(f"bad/absent difficulty {diff!r} (daredevil is removed)")
    opts = q.get("options") or []
    if len(opts) != 4:
        v.append(f"expected 4 options, got {len(opts)}")
        return v
    ca = (q.get("correct_answer") or "").strip().upper()[:1]
    if ca not in LETTERS:
        v.append(f"correct_answer {ca!r} not one of A-D")
        return v
    if not (q.get("explanation") or "").strip():
        v.append("empty explanation")
    # Explanation must not point back at "the material/source/text/notes".
    expl = (q.get("explanation") or "").lower()
    for bad in ("the material", "the source", "the text", "the notes", "the study",
                "the passage", "the module states", "as stated"):
        if bad in expl:
            v.append(f"explanation references source ({bad!r})")
            break

    bodies = [option_body(o) for o in opts]
    ci = LETTERS.index(ca)
    if len(set(b.lower() for b in bodies)) != 4:
        v.append("duplicate option text")

    # --- Giveaway 1: length tell ---
    wc = [len(b.split()) for b in bodies]
    spread = max(wc) - min(wc)
    if spread > MAX_WORD_SPREAD:
        v.append(f"option word spread {spread} > {MAX_WORD_SPREAD} ({wc})")
    if wc[ci] == max(wc) and wc.count(max(wc)) == 1 and spread >= 2:
        v.append(f"correct option is uniquely the longest ({wc[ci]}w vs {wc})")

    # --- Giveaway 2: bracket tell ---
    br = [_has_bracket(b) for b in bodies]
    if br[ci] and sum(br) < len(br):
        v.append("correct option has a parenthetical the distractors lack")

    return v


def check_bank(questions: list) -> dict:
    """Validate a whole question list; return {index: [violations]} for offenders."""
    out = {}
    for i, q in enumerate(questions):
        vs = check_question(q)
        if vs:
            out[i] = vs
    return out


def summarize(questions: list) -> str:
    diffs = {}
    for q in questions:
        diffs[q.get("difficulty", "?")] = diffs.get(q.get("difficulty", "?"), 0) + 1
    return f"{len(questions)} questions · difficulty {diffs}"


def emit(key: str, meta: dict, questions: list) -> int:
    """Validate a guide's questions and, if clean, write regen/<key>.json.
    Returns a process exit code (0 = written, 1 = violations)."""
    import os, json, sys
    bad = check_bank(questions)
    print(f"{key}: {summarize(questions)}")
    if bad:
        print("VIOLATIONS:")
        for i, vs in bad.items():
            print(f"  [{i}] {questions[i].get('question','')[:60]}")
            for v in vs:
                print(f"        - {v}")
        return 1
    print("All questions clean ✅")
    regen_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "regen")
    out = dict(meta, questions=questions)
    path = os.path.join(regen_dir, key + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote", path)
    return 0
