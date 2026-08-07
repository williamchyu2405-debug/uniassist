#!/usr/bin/env python3
"""Periodic, safe backup of MedVault's SQLite DB (data/study.db).

Run by the com.uniassist.dbbackup LaunchAgent (every ~6h) and manually anytime.

Safety design (learned from a Jul-2026 wipe):
  * Consistent snapshot via SQLite's online-backup API (safe while the app runs).
  * REFUSES to snapshot a suspiciously-empty DB (0 materials) when history exists,
    so a reset/wipe can never overwrite your good backups — history freezes until
    the DB is healthy again.
  * Skips duplicates (no change in materials since the newest backup).
  * Keeps the most recent KEEP snapshots.

Backups land in data/backups/study-YYYYMMDD-HHMMSS.db (data/ is gitignored).
"""
import sqlite3, os, glob, datetime, sys

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB     = os.path.join(ROOT, "data", "study.db")
BAKDIR = os.path.join(ROOT, "data", "backups")
KEEP   = 40  # ~10 days at 6h; healthy snapshots only (wiped states are skipped)


def signature(path):
    """A light fingerprint of study content: (materials, total content chars)."""
    try:
        c = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        n = c.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
        chars = c.execute("SELECT COALESCE(SUM(LENGTH(content)),0) FROM materials").fetchone()[0]
        c.close()
        return (n, chars)
    except Exception:
        return None


def main():
    if not os.path.exists(DB):
        print("no DB at", DB); return 0
    os.makedirs(BAKDIR, exist_ok=True)
    existing = sorted(glob.glob(os.path.join(BAKDIR, "study-*.db")))

    sig = signature(DB)
    if sig is None:
        print("cannot read DB (locked/corrupt?) — skipping this run"); return 0

    # Guard: never let a wiped/empty DB overwrite good history.
    if sig[0] == 0 and existing:
        print(f"skip: DB has 0 materials; preserving {len(existing)} prior backup(s)"); return 0

    # Dedup: skip if nothing changed since the newest backup.
    if existing and signature(existing[-1]) == sig:
        print(f"skip: no change since {os.path.basename(existing[-1])} (materials={sig[0]})"); return 0

    ts  = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = os.path.join(BAKDIR, f"study-{ts}.db")
    src = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    out = sqlite3.connect(dst)
    with out:
        src.backup(out)
    out.close(); src.close()
    print(f"backup -> {dst}  (materials={sig[0]}, {sig[1]} chars)")

    # Retention: keep the newest KEEP snapshots.
    backups = sorted(glob.glob(os.path.join(BAKDIR, "study-*.db")))
    for old in backups[:-KEEP]:
        try:
            os.remove(old); print("pruned", os.path.basename(old))
        except OSError as e:
            print("prune failed:", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
