#!/usr/bin/env python3
"""
scan_vocab.py — surface new vocabulary from your Chrome search history.

This is a LOCAL, read-only helper for the "update my word bank" flow. It does
NOT write anything or call any AI. It prints candidate words that:
  1. look like vocabulary lookups in your Chrome history, and
  2. aren't already in your Word Bank (seed list + saved words from the API).

Typical use (in a Claude Code session):
    python3 tools/scan_vocab.py --since 2026-07-11
Claude then writes definitions/examples for the printed words and POSTs them to
/api/wordbank. Nothing here touches the database directly.

Flags:
    --since YYYY-MM-DD   only searches on/after this date (default: last 30 days)
    --profile NAME       Chrome profile folder (default: Default)
    --api URL            Word Bank API base to dedupe against (optional)
    --token TOKEN        Bearer token for the API (optional; else X-User-Id)
    --user-id N          legacy auth fallback for --api
    --json               emit JSON instead of a plain list
"""
import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import sys
import tempfile
import shutil
import urllib.request

HISTORY = os.path.expanduser(
    "~/Library/Application Support/Google/Chrome/{profile}/History"
)

# A search term looks like a vocab lookup if it is short, or explicitly asks for
# a meaning/definition/synonym/pronunciation/etc.
VOCAB_HINT = re.compile(
    r"(meaning|definition|synonym|antonym|etymolog|pronounce|pronunciation|"
    r"\bdefine\b|in a sentence| vs |another word|word for)", re.I)


def is_candidate(term: str) -> bool:
    t = term.strip()
    if not t or "http" in t or "." in t or any(c.isdigit() for c in t):
        return False
    if VOCAB_HINT.search(t):
        return True
    # short, all-alphabetic phrase (<=2 words, >=4 chars) — likely a lone word lookup
    return len(t) >= 4 and t.replace(" ", "").isalpha() and t.count(" ") <= 1


def clean(term: str) -> str:
    """Strip the hint words so 'poignant meaning' -> 'poignant'."""
    t = VOCAB_HINT.sub("", term).strip()
    t = re.sub(r"\b(define|what does|mean|means)\b", "", t, flags=re.I).strip()
    return re.sub(r"\s+", " ", t).lower()


def read_history(profile: str, since: dt.date):
    path = HISTORY.format(profile=profile)
    if not os.path.exists(path):
        sys.exit(f"No Chrome history at {path}")
    # Copy first — Chrome keeps the live DB locked while running.
    tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False).name
    shutil.copy2(path, tmp)
    cutoff = int((since - dt.date(1601, 1, 1)).total_seconds() * 1_000_000)
    try:
        con = sqlite3.connect(f"file:{tmp}?mode=ro", uri=True)
        rows = con.execute(
            "SELECT DISTINCT k.term FROM keyword_search_terms k "
            "JOIN urls u ON k.url_id = u.id WHERE u.last_visit_time > ?",
            (cutoff,)).fetchall()
        con.close()
    finally:
        os.unlink(tmp)
    return [r[0] for r in rows]


def existing_words(api: str, token: str, user_id: str):
    """Words already saved via the API (lower-cased). Best-effort."""
    if not api:
        return set()
    req = urllib.request.Request(api.rstrip("/") + "/api/wordbank")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    elif user_id:
        req.add_header("X-User-Id", user_id)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
        return {w["word"].lower() for w in data.get("words", [])}
    except Exception as e:  # noqa: BLE001 — dedupe is best-effort
        print(f"# (couldn't reach API to dedupe: {e})", file=sys.stderr)
        return set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since")
    ap.add_argument("--profile", default="Default")
    ap.add_argument("--api")
    ap.add_argument("--token")
    ap.add_argument("--user-id")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    since = (dt.date.fromisoformat(a.since) if a.since
             else dt.date.today() - dt.timedelta(days=30))

    terms = read_history(a.profile, since)
    seen = existing_words(a.api, a.token, a.user_id)

    # Seed words shipped in the app so we don't re-suggest them. Kept in sync
    # loosely; the API dedupe above is the authoritative check.
    candidates = {}
    for t in terms:
        if not is_candidate(t):
            continue
        w = clean(t)
        if len(w) < 3 or w in seen or w in candidates:
            continue
        candidates[w] = t  # keep first raw form for reference

    out = sorted(candidates)
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        if not out:
            print("No new vocabulary candidates found.")
        for w in out:
            print(w)
    print(f"\n# {len(out)} new candidate(s) since {since}", file=sys.stderr)


if __name__ == "__main__":
    main()
