#!/usr/bin/env python3
"""Assemble the regenerated per-guide fragments into guide_quizzes.json.

- Reads every guide_authoring/regen/*.html.json fragment.
- Validates every question (anti-giveaway + structural rules).
- Backs up the existing guide_quizzes.json, then writes the merged bank.

Refuses to write if any fragment has a validation violation, or (unless --partial)
if any gallery key in the current bank is missing a fragment — so a full deploy
can't accidentally drop a gallery.

Usage:
  python3 assemble_bank.py            # dry-run: report coverage + violations
  python3 assemble_bank.py --write    # back up + write guide_quizzes.json
  python3 assemble_bank.py --write --partial   # allow missing galleries
"""
import os, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
REGEN = os.path.join(HERE, "..", "regen")
BANK = os.path.join(ROOT, "guide_quizzes.json")
sys.path.insert(0, HERE)
from qbank_lib import check_bank, summarize  # noqa


def load_fragments() -> dict:
    frags = {}
    for fn in sorted(os.listdir(REGEN)):
        if fn.endswith(".html.json"):
            key = fn[:-5]  # drop ".json" -> "<name>.html"
            with open(os.path.join(REGEN, fn), encoding="utf-8") as f:
                frags[key] = json.load(f)
    return frags


def main():
    write = "--write" in sys.argv
    partial = "--partial" in sys.argv
    current = json.load(open(BANK, encoding="utf-8"))
    frags = load_fragments()

    missing = [k for k in current if k not in frags]
    extra = [k for k in frags if k not in current]

    print(f"Current bank: {len(current)} galleries")
    print(f"Fragments:    {len(frags)} galleries")
    if missing:
        print(f"\n⬜ MISSING fragments ({len(missing)}):")
        for k in missing:
            print(f"   - {k}")
    if extra:
        print(f"\n➕ NEW galleries not in old bank ({len(extra)}): {extra}")

    total_q = 0
    any_bad = False
    print("\nPer-fragment validation:")
    for key, frag in frags.items():
        qs = frag.get("questions") or []
        total_q += len(qs)
        bad = check_bank(qs)
        flag = "❌" if bad else "✅"
        print(f"  {flag} {key}: {summarize(qs)}")
        if bad:
            any_bad = True
            for i, vs in bad.items():
                print(f"        [{i}] {qs[i].get('question','')[:55]}: {vs}")
    print(f"\nTotal questions across fragments: {total_q}")

    if not write:
        print("\n(dry run — pass --write to back up and write guide_quizzes.json)")
        return 0 if not any_bad else 1

    if any_bad:
        print("\nRefusing to write: validation violations above.")
        return 1
    if missing and not partial:
        print("\nRefusing to write: galleries missing fragments (use --partial to override).")
        return 1

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = f"{BANK}.bak-{ts}"
    os.rename(BANK, backup)
    print(f"\nBacked up old bank -> {backup}")
    # Preserve any galleries that (in --partial mode) don't yet have a fragment.
    merged = dict(current)
    merged.update(frags)
    with open(BANK, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=1)
    print(f"Wrote {BANK}: {len(merged)} galleries, "
          f"{sum(len(v.get('questions') or []) for v in merged.values())} questions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
