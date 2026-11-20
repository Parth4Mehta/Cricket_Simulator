"""Shared test setup.

Every test runs against a throwaway SQLite DB and a copy of config.json,
with seeded randomness and no blocking input()/sleep(). Real user data in
database/cricsim.db and config.json is never touched.
"""
import builtins
import os
import random
import shutil
import sys
import time

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config_manager  # noqa: E402
import db.connection as connection  # noqa: E402


@pytest.fixture(autouse=True)
def isolated_env(tmp_path, monkeypatch):
    db_dir = tmp_path / "database"
    monkeypatch.setattr(connection, "DB_DIR", str(db_dir))
    monkeypatch.setattr(connection, "DB_PATH", str(db_dir / "cricsim.db"))

    cfg = tmp_path / "config.json"
    shutil.copy(os.path.join(ROOT, "config.json"), cfg)
    monkeypatch.setattr(config_manager, "CONFIG_FILE", str(cfg))

    monkeypatch.setattr(builtins, "input", lambda *a, **k: "")
    monkeypatch.setattr(time, "sleep", lambda *a, **k: None)

    random.seed(1234)
    yield tmp_path


@pytest.fixture
def rows():
    """Run a SELECT against the test DB and return the rows."""
    def _rows(sql, params=()):
        with connection.get_conn() as con:
            return con.execute(sql, params).fetchall()
    return _rows
