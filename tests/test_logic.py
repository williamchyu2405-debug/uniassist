"""Pure-logic tests for the study engine — no API, no network, isolated DB.

Run:  /Library/Developer/CommandLineTools/usr/bin/python3 -m unittest tests/test_logic.py -v
      (or: python3 tests/test_logic.py)

Importing `main` runs init_db() at module load, so we point DATA_DIR at a fresh
temp dir first — the real data/study.db is never touched.
"""
import os
import tempfile
import unittest

os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="uniassist_test_")

import sqlite3  # noqa: E402
import sys      # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main     # noqa: E402


def _mem_db():
    """In-memory DB with just the columns the tested functions read."""
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript(
        """
        CREATE TABLE quiz_questions (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT, topic TEXT, difficulty TEXT, related_topics TEXT);
        CREATE TABLE flashcards (user_id INT, topic TEXT, related_topics TEXT);
        CREATE TABLE quiz_attempts (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT, question_id INT, topic TEXT, is_correct INT, attempted_at TEXT);
        """
    )
    return db


def _seed(db, topic, results, difficulty="medium", user_id=1):
    """results = list of 0/1 in chronological order (oldest first)."""
    for i, c in enumerate(results):
        qid = db.execute(
            "INSERT INTO quiz_questions (user_id, topic, difficulty) VALUES (?,?,?)",
            (user_id, topic, difficulty),
        ).lastrowid
        db.execute(
            "INSERT INTO quiz_attempts (user_id, question_id, topic, is_correct, attempted_at) VALUES (?,?,?,?,?)",
            (user_id, qid, topic, c, f"2026-01-{i + 1:02d} 00:00:00"),
        )
    db.commit()


class TestSM2(unittest.TestCase):
    def test_first_correct_interval_1(self):
        interval, ease, count, nxt = main.sm2_schedule(2.5, 1, 0, True)
        self.assertEqual(interval, 1)
        self.assertEqual(count, 1)
        self.assertTrue(nxt)  # ISO date string

    def test_second_correct_interval_6(self):
        interval, ease, count, _ = main.sm2_schedule(2.5, 1, 1, True)
        self.assertEqual(interval, 6)
        self.assertEqual(count, 2)

    def test_wrong_resets_and_penalises_ease(self):
        interval, ease, count, _ = main.sm2_schedule(2.5, 20, 5, False)
        self.assertEqual(interval, 1)
        self.assertEqual(count, 0)
        self.assertLess(ease, 2.5)

    def test_ease_never_below_floor(self):
        _, ease, _, _ = main.sm2_schedule(1.3, 1, 0, False)
        self.assertGreaterEqual(ease, 1.3)


class TestAdaptiveTargets(unittest.TestCase):
    def test_hot_streak_pushes_harder(self):
        db = _mem_db()
        _seed(db, "Cardio", [1, 1, 1, 1, 1], "medium")
        t = main.adaptive_targets(db, 1)
        self.assertGreater(list(t.values())[0], 1)   # above medium (rank 1)

    def test_cold_streak_eases_off(self):
        db = _mem_db()
        _seed(db, "Renal", [0, 0, 0, 0, 0], "medium")
        t = main.adaptive_targets(db, 1)
        self.assertLess(list(t.values())[0], 1)      # below medium

    def test_insufficient_history_defaults_medium(self):
        db = _mem_db()
        _seed(db, "New", [1], "medium")
        t = main.adaptive_targets(db, 1)
        self.assertEqual(list(t.values())[0], 1)     # < min history → medium

    def test_target_clamped_to_max_rank(self):
        db = _mem_db()
        _seed(db, "Top", [1, 1, 1, 1, 1], "daredevil")
        t = main.adaptive_targets(db, 1)
        self.assertLessEqual(list(t.values())[0], 3)  # clamp [0,3]


class TestTopicAccuracy(unittest.TestCase):
    def test_aggregates_not_order_dependent_average(self):
        # 2 correct of 4 → 0.5, computed from raw counts (the #11 fix)
        db = _mem_db()
        _seed(db, "Cardio", [1, 1, 0, 0])
        acc = main.topic_accuracy(db, 1)
        self.assertTrue(any(abs(v - 0.5) < 1e-9 for v in acc.values()),
                        f"expected a 0.5 accuracy, got {acc}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
