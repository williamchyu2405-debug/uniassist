#!/usr/bin/env python3
"""One-off live-DB cleanup for sharing. Backs up first; prints before + after.
Run:  python3 db_admin.py            # inspect only (safe)
      python3 db_admin.py --clean    # backup + remove/wipe/clear, then re-inspect
"""
import sqlite3, os, sys, shutil, datetime

# Resolve DB the same way main.py does (DATA_DIR=/data on Railway -> /data/data/study.db)
_root = (os.getenv("DATA_DIR", "").strip() or ".")
DB = os.path.join(_root, "data", "study.db")
if not os.path.exists(DB):
    for c in ("/data/data/study.db", "data/study.db"):
        if os.path.exists(c):
            DB = c; break

REMOVE_IDS = [6, 9]    # William Yu + Harrison ("Sharreson") — confirmed against live DB
WIPE_IDS   = [7, 8]    # Martha (marthachriston1) + Fiona (fotinifioravantis) — confirmed

# every table that carries user_id (for full account removal)
USER_TABLES = ["materials","flashcards","quiz_questions","quiz_attempts","revision_slides",
  "exam_dates","mind_maps","chat_messages","flashcard_log","user_materials","sessions",
  "battle_participants","graph_hidden_nodes","graph_hidden_edges","graph_custom_edges",
  "writing_essays","writing_errors","writing_cards","writing_reviews","word_bank",
  "russian_vocab","russian_review_log","russian_progress"]
# activity/stats tables cleared for a WIPE (account + material access kept)
WIPE_TABLES = ["quiz_attempts","quiz_questions","flashcards","flashcard_log","revision_slides",
  "mind_maps","chat_messages","battle_participants","graph_hidden_nodes","graph_hidden_edges",
  "graph_custom_edges","writing_essays","writing_errors","writing_cards","writing_reviews",
  "word_bank","russian_review_log","russian_progress"]

def _has(d, t):
    return bool(d.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone())

def inspect(d):
    print("DB:", DB)
    print("USERS:")
    for r in d.execute("SELECT id, username, (password_hash IS NOT NULL AND password_hash!='') FROM users ORDER BY id"):
        qa = d.execute("SELECT COUNT(*) FROM quiz_attempts WHERE user_id=?", (r[0],)).fetchone()[0]
        print(f"  id={r[0]:<4} user={r[1]!r:<24} password={'YES' if r[2] else 'NONE'}  quiz_attempts={qa}")
    print("MATERIALS  (SHARED? = non-guide = Discover clutter):")
    for r in d.execute("SELECT id, filename, original_name, user_id, visibility FROM materials ORDER BY id"):
        kind = "GUIDE " if (r[1] or "").startswith("guide:") else "SHARED"
        print(f"  [{kind}] id={r[0]:<4} owner={r[3]!s:<4} vis={r[4]!r:<9} {(r[2] or r[1])!r}")

def clean(d):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = DB + f".bak-{ts}"; shutil.copy2(DB, bak); print("backup ->", bak)
    def rows(idlist):
        return [(r[0], r[1]) for r in d.execute("SELECT id, username FROM users") if r[0] in idlist]
    for uid, un in rows(REMOVE_IDS):
        for t in USER_TABLES:
            if _has(d, t): d.execute(f"DELETE FROM {t} WHERE user_id=?", (uid,))
        d.execute("DELETE FROM users WHERE id=?", (uid,))
        print(f"  REMOVED account {un!r} (id {uid}) + all data")
    for uid, un in rows(WIPE_IDS):
        for t in WIPE_TABLES:
            if _has(d, t): d.execute(f"DELETE FROM {t} WHERE user_id=?", (uid,))
        print(f"  WIPED stats for {un!r} (id {uid})")
    shared = [r[0] for r in d.execute("SELECT id FROM materials WHERE filename NOT LIKE 'guide:%'")]
    for mid in shared:
        for t in ["quiz_questions","quiz_attempts","flashcards","flashcard_log","revision_slides","mind_maps","user_materials"]:
            if _has(d, t): d.execute(f"DELETE FROM {t} WHERE material_id=?", (mid,))
        d.execute("DELETE FROM materials WHERE id=?", (mid,))
    print(f"  CLEARED {len(shared)} non-guide (Discover/shared) materials")
    d.commit(); print("committed.")

if __name__ == "__main__":
    d = sqlite3.connect(DB)
    print("=== BEFORE ==="); inspect(d)
    if "--clean" in sys.argv:
        print("\n=== CLEANING ==="); clean(d)
        print("\n=== AFTER ==="); inspect(d)
    else:
        print("\n(inspect only — pass --clean to apply)")
