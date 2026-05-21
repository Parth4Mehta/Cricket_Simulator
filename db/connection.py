"""
Connection + schema bootstrap for the SQLite-backed CricSim DB.

Usage:
    from db.connection import get_conn, ensure_db

    ensure_db()  # creates database/cricsim.db and applies schema.sql

    with get_conn() as con:
        rows = con.execute("SELECT * FROM teams").fetchall()
"""
import os
import sqlite3
from contextlib import contextmanager

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(PROJECT_ROOT, "database")
DB_PATH = os.path.join(DB_DIR, "cricsim.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


def ensure_db():
    """Create the DB file (if missing) and apply schema.sql idempotently."""
    os.makedirs(DB_DIR, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.execute("PRAGMA journal_mode = WAL")
        with open(SCHEMA_PATH, "r") as f:
            con.executescript(f.read())
        con.commit()
    finally:
        con.close()


@contextmanager
def get_conn():
    """Context-managed connection.

    - Auto-commits on clean exit, rolls back on exception.
    - Foreign keys and Row factory enabled.
    """
    ensure_db()
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def db_path():
    return DB_PATH
