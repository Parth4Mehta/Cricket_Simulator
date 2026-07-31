"""
One-shot importer: read the existing JSON storage and load it into SQLite.

Run from the project root:

    python -m db.migrate_from_json

This script never deletes or modifies the JSON files. It only reads them
and inserts into the SQLite DB. Safe to run multiple times: existing
rows are replaced (no duplicates) and match files are de-duplicated by
(team_a, team_b, timestamp_utc).
"""
import json
import os
from glob import glob

from db.connection import DB_DIR, ensure_db, get_conn

PLAYER_FILE = os.path.join(DB_DIR, "player_stats.json")
TEAM_FILE = os.path.join(DB_DIR, "team_stats.json")
CUMULATIVE_FILE = os.path.join(DB_DIR, "cumulative_stats.json")
MATCH_DIR = os.path.join(DB_DIR, "match_stats")


def _load(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  warn: failed to read {path}: {e}")
        return default


def import_players(con):
    data = _load(PLAYER_FILE, {})
    n = 0
    for name, p in data.items():
        bb = p.get("best_bowling") or {}
        con.execute(
            """
            INSERT OR REPLACE INTO players
            (name, team, runs, balls_faced, fours, sixes, matches, outs, not_outs,
             highest_score, wickets, balls_bowled, best_bowling_wickets, best_bowling_runs)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                name,
                p.get("team"),
                p.get("runs", 0),
                p.get("balls_faced", 0),
                p.get("fours", 0),
                p.get("sixes", 0),
                p.get("matches", 0),
                p.get("outs", 0),
                p.get("not_outs", 0),
                p.get("highest_score", 0),
                p.get("wickets", 0),
                p.get("balls_bowled", 0),
                bb.get("wickets", 0),
                bb.get("runs", 999),
            ),
        )
        n += 1
    print(f"  players imported: {n}")


def import_teams(con):
    data = _load(TEAM_FILE, {})
    n = 0
    for code, t in data.items():
        con.execute(
            """
            INSERT OR REPLACE INTO teams
            (team_code, played, won, lost, tied, points,
             runs_scored, runs_conceded, balls_faced, balls_bowled)
            VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                code,
                t.get("played", 0),
                t.get("won", 0),
                t.get("lost", 0),
                t.get("tied", 0),
                t.get("points", 0),
                t.get("runs_scored", 0),
                t.get("runs_conceded", 0),
                t.get("balls_faced", 0),
                t.get("balls_bowled", 0),
            ),
        )
        n += 1
    print(f"  teams imported: {n}")


def import_cumulative(con):
    data = _load(CUMULATIVE_FILE, {})
    n = 0
    for code, t in data.items():
        con.execute(
            """
            INSERT OR REPLACE INTO cumulative_teams
            (team_code, played, won, lost, tied, points)
            VALUES (?,?,?,?,?,?)
            """,
            (
                code,
                t.get("played", 0),
                t.get("won", 0),
                t.get("lost", 0),
                t.get("tied", 0),
                t.get("points", 0),
            ),
        )
        n += 1
    print(f"  cumulative_teams imported: {n}")


def import_matches(con):
    if not os.path.isdir(MATCH_DIR):
        print("  no match_stats directory; skipping match import")
        return

    n_matches = 0
    n_batting = 0
    n_bowling = 0
    skipped = 0

    for path in sorted(glob(os.path.join(MATCH_DIR, "*.json"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                m = json.load(f)
        except Exception as e:
            print(f"  skip (bad json): {os.path.basename(path)} ({e})")
            skipped += 1
            continue

        meta = m.get("meta", {})
        team_a, team_b = meta.get("teamA"), meta.get("teamB")
        ts = meta.get("timestamp_utc", "")
        if not (team_a and team_b):
            skipped += 1
            continue

        existing = con.execute(
            "SELECT match_id FROM matches WHERE team_a=? AND team_b=? AND timestamp_utc=?",
            (team_a, team_b, ts),
        ).fetchone()
        if existing:
            continue

        res = m.get("result") or {}
        cur = con.execute(
            """
            INSERT INTO matches (team_a, team_b, timestamp_utc, winner, margin, a_score, b_score)
            VALUES (?,?,?,?,?,?,?)
            """,
            (
                team_a,
                team_b,
                ts,
                res.get("winner"),
                res.get("by", ""),
                res.get("A_score"),
                res.get("B_score"),
            ),
        )
        match_id = cur.lastrowid
        n_matches += 1

        for team in (team_a, team_b):
            section = m.get(team) or {}

            for i, b in enumerate(section.get("batting", []) or []):
                con.execute(
                    """
                    INSERT INTO match_batting
                    (match_id, team, position, player_name, runs, balls, fours, sixes, dismissal)
                    VALUES (?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        match_id,
                        team,
                        i,
                        b.get("name"),
                        b.get("runs", 0),
                        b.get("balls", 0),
                        b.get("4s", 0),
                        b.get("6s", 0),
                        b.get("dismissal", "not out"),
                    ),
                )
                n_batting += 1

            for bowler, bs in (section.get("bowling") or {}).items():
                con.execute(
                    """
                    INSERT INTO match_bowling
                    (match_id, team, player_name, overs, balls, runs, wickets)
                    VALUES (?,?,?,?,?,?,?)
                    """,
                    (
                        match_id,
                        team,
                        bowler,
                        bs.get("overs", 0),
                        bs.get("balls", 0),
                        bs.get("runs", 0),
                        bs.get("wickets", 0),
                    ),
                )
                n_bowling += 1

    print(f"  matches imported: {n_matches} (skipped: {skipped})")
    print(f"  match_batting rows: {n_batting}")
    print(f"  match_bowling rows: {n_bowling}")


def summarize(con):
    print("\n--- Summary ---")
    for table in (
        "teams",
        "players",
        "matches",
        "match_batting",
        "match_bowling",
        "cumulative_teams",
    ):
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:18} {n}")


def main():
    ensure_db()
    print("Migrating JSON -> SQLite ...")
    with get_conn() as con:
        import_players(con)
        import_teams(con)
        import_cumulative(con)
        import_matches(con)
        summarize(con)
    print("\nDone. DB file: database/cricsim.db")
    print("Original JSON files left untouched.")


if __name__ == "__main__":
    main()
