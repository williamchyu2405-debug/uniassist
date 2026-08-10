#!/usr/bin/env python3
"""
seed_on_boot.py — OPTIONAL zero-API data seeder for a fresh MedVault deployment.

WHY THIS EXISTS
    data/study.db is gitignored, so a git/Docker deploy starts with an EMPTY database.
    main.py auto-creates all tables on boot (init_db()), and it can rebuild every
    guide quiz from the git-tracked guide_quizzes.json with NO Anthropic API calls
    (see _ensure_guide_quiz in main.py). This script drives that flow programmatically
    so a brand-new host comes up already populated with:
        - one user profile (default username "william")
        - all 14 guide-quiz materials (152 hand-authored MCQs) ready for SRS/dashboard

    This is the recommended path when you do NOT want to upload your real study.db
    (e.g. to leave personal quiz history / uploaded course materials on your Mac).
    If you DO want your exact local state, skip this and just copy study.db onto the
    persistent volume instead (see RUNBOOK "Data migration — Option A").

HOW IT WORKS
    It imports main.py (which runs init_db() at import time), then calls the same
    internal helpers the app uses. It must run in the app's environment, with the
    SAME DATA_DIR as the server so it writes to the same study.db.

USAGE (run once, on the host, in the app dir, with DATA_DIR set as in production)
    DATA_DIR=/data python seed_on_boot.py               # user "william"
    DATA_DIR=/data python seed_on_boot.py --user alice   # custom username

    On Railway:  railway run python seed_on_boot.py        (from your local project, CLI linked)
                 — or open the service > ⋮ > "Run a command" and enter:  python seed_on_boot.py
                 (set DATA_DIR=/data as a service variable and mount the volume at /data first,
                  so it writes to the same study.db the server reads)

IDEMPOTENT: safe to run repeatedly. It won't duplicate the user or re-insert
questions that already exist (matched by stem), thanks to _ensure_guide_quiz.
"""
import argparse
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="Seed a fresh MedVault DB (zero-API).")
    ap.add_argument("--user", default="william", help="username to create/seed (default: william)")
    args = ap.parse_args()

    # Importing main runs init_db() and resolves DB_PATH from DATA_DIR.
    import main

    db = main.get_db()
    try:
        # Find-or-create the user profile.
        row = db.execute("SELECT id FROM users WHERE username = ?", (args.user,)).fetchone()
        if row:
            user_id = row["id"]
            print(f"User '{args.user}' already exists (id={user_id}).")
        else:
            cur = db.execute("INSERT INTO users (username) VALUES (?)", (args.user,))
            user_id = cur.lastrowid
            db.commit()
            print(f"Created user '{args.user}' (id={user_id}).")
            print("  NOTE: no password_hash set. Set a password via the app's /api/login")
            print("  flow (first login on an empty-hash account sets it), or register fresh.")

        # Rebuild all guide quizzes from guide_quizzes.json (zero-API).
        banks = main._load_guide_quizzes()
        if not banks:
            print("WARNING: guide_quizzes.json produced no quizzes — is it present next to main.py?")
        total_inserted = 0
        for key in banks:
            mid, inserted = main._ensure_guide_quiz(db, user_id, key)
            if mid is not None:
                total_inserted += inserted
                print(f"  seeded {key}: +{inserted} questions (material id={mid})")
        print(f"\nDone. Inserted {total_inserted} new question(s) across {len(banks)} guide(s).")
        print("The app is ready: log in, open the gallery, hit any guide's Quiz button.")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
