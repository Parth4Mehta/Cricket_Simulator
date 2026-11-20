import os
import sqlite3

import pytest

import database
import historical
from db import connection
from match_simulator import simulate_match

CURRENT_TABLES = ("matches", "match_batting", "match_bowling", "players", "teams")


def test_ensure_db_is_idempotent():
    connection.ensure_db()
    connection.ensure_db()


def test_migration_adds_stage_column_to_old_matches_table():
    # A DB created before the `stage` column existed.
    os.makedirs(connection.DB_DIR, exist_ok=True)
    con = sqlite3.connect(connection.DB_PATH)
    con.execute("""CREATE TABLE matches (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT, team_a TEXT NOT NULL,
        team_b TEXT NOT NULL, timestamp_utc TEXT NOT NULL, winner TEXT,
        margin TEXT, a_score INTEGER, b_score INTEGER)""")
    con.execute("INSERT INTO matches (team_a, team_b, timestamp_utc) VALUES ('MI', 'CSK', 'x')")
    con.commit()
    con.close()

    connection.ensure_db()

    with connection.get_conn() as con:
        cols = [r[1] for r in con.execute("PRAGMA table_info(matches)")]
        stage = con.execute("SELECT stage FROM matches").fetchone()[0]
    assert "stage" in cols
    assert stage == "league"


def test_get_conn_rolls_back_on_error(rows):
    with pytest.raises(RuntimeError):
        with connection.get_conn() as con:
            con.execute("INSERT INTO teams (team_code) VALUES ('XYZ')")
            raise RuntimeError("boom")
    assert rows("SELECT * FROM teams WHERE team_code = 'XYZ'") == []


def test_compute_nrr():
    assert database.compute_nrr(100, 100, 0, 120) == 0.0
    assert database.compute_nrr(100, 100, 120, 0) == 0.0
    # 180 off 20 overs vs 120 off 20 overs -> 9.0 - 6.0
    assert database.compute_nrr(180, 120, 120, 120) == 3.0


def test_points_table_sorted_by_points_then_nrr():
    simulate_match("MI", "CSK")
    simulate_match("RCB", "KKR")
    simulate_match("MI", "RCB")
    table = database.get_points_table_sorted()
    keys = [(r["points"], r["nrr"]) for r in table]
    assert keys == sorted(keys, reverse=True)


def test_clear_database_empties_current_tables(rows):
    simulate_match("MI", "CSK")
    database.clear_database(silent=True)
    for t in CURRENT_TABLES:
        assert rows(f"SELECT COUNT(*) FROM {t}")[0][0] == 0, t


def test_archive_copies_season_and_keeps_current(rows):
    assert historical.archive_current_season() is None  # nothing to archive yet

    simulate_match("MI", "CSK")
    season_id = historical.archive_current_season(champion="MI")

    assert season_id is not None
    assert rows("SELECT COUNT(*) FROM historical_matches")[0][0] == 1
    assert rows("SELECT COUNT(*) FROM historical_match_batting")[0][0] > 0
    assert rows("SELECT COUNT(*) FROM matches")[0][0] == 1  # current untouched
    assert len(historical.list_seasons()) == 1

    historical.delete_season(season_id)
    assert rows("SELECT COUNT(*) FROM historical_matches")[0][0] == 0
