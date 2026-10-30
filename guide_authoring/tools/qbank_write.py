#!/usr/bin/env python3
"""Shared helpers for hand-authored gallery quiz banks.

A bank script defines KEY, META and a list Q built with q(...), then calls
write_bank(KEY, META, Q). Correct answers are rotated across A-D so no letter
dominates, every question is checked by qbank_lib.check_question, and the
entry is written straight into guide_quizzes.json (keys already present are
replaced in place).
"""
import os, sys, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from qbank_lib import check_bank, summarize  # noqa

BANK_PATH = os.path.join(HERE, "..", "..", "guide_quizzes.json")


def q(topic, diff, stem, opts, ans, expl):
    """One MCQ. `opts` are bare option texts; `ans` is the letter of the correct one."""
    return {"topic": topic, "difficulty": diff, "question": stem,
            "options": [f"{'ABCD'[i]}. {o}" for i, o in enumerate(opts)],
            "correct_answer": ans, "explanation": expl, "related": [topic]}


def rebalance(qs):
    """Move each correct option to a rotating position so A-D are evenly used."""
    for i, x in enumerate(qs):
        bodies = [re.sub(r"^[A-D]\. ", "", o) for o in x["options"]]
        ci = "ABCD".index(x["correct_answer"])
        ti = (i * 3 + 1) % 4
        bodies[ci], bodies[ti] = bodies[ti], bodies[ci]
        x["options"] = [f"{'ABCD'[k]}. {b}" for k, b in enumerate(bodies)]
        x["correct_answer"] = "ABCD"[ti]
    return qs


def write_bank(key, meta, questions):
    rebalance(questions)
    bad = check_bank(questions)
    print(f"{key}: {summarize(questions)}")
    if bad:
        print("VIOLATIONS:")
        for i, vs in bad.items():
            print(f"  [{i}] {questions[i].get('question', '')[:70]}")
            for v in vs:
                print(f"        - {v}")
        sys.exit(1)
    raw = open(BANK_PATH, encoding="utf-8").read()
    bank = json.loads(raw)
    bank[key] = dict(meta, questions=questions)
    out = json.dumps(bank, ensure_ascii=False, indent=1) + ("\n" if raw.endswith("\n") else "")
    open(BANK_PATH, "w", encoding="utf-8").write(out)
    print(f"wrote {key} ({len(questions)} questions; bank now {len(bank)} guides)")
