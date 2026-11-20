# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pip install -e ".[dev,rich]"            # dev setup (pytest, black, flake8, rich)
python main.py                          # run the interactive menu app
python -m pytest -v tests/              # run all tests (what the hooks and CI run)
python -m pytest -v tests/test_teams.py -k MI   # run a single test/param case
black *.py && flake8 *.py               # format / lint (top-level modules only)
python top_players.py --print           # standalone top-players report from the DB
python -m db.migrate_from_json          # one-shot import of legacy JSON stats into SQLite
git config core.hooksPath .githooks     # enable pre-commit/pre-push hooks (run pytest)
```

CI (`.github/workflows/tests.yml`) runs pytest on Python 3.11 on every push/PR. The pre-commit and pre-push hooks also run the full test suite, so commits are blocked when tests fail.

Tests (about 2s, run them after any change): `tests/conftest.py` points every test at a temporary SQLite DB and a temporary copy of `config.json`, seeds `random`, and replaces `input()`/`time.sleep` with no-ops, so the tests never touch real data. Files: `test_teams.py` (squads, bowling orders), `test_probability.py` (ball math valid for every profile and every real batter/bowler pairing), `test_match.py` (innings/match totals add up, chase stops at target, match saved to DB), `test_database.py` (schema, migration, rollback, NRR, clear, archive), `test_formats.py` (every format in `TOURNAMENT_FORMATS` runs end to end; a new format must be added to `FORMAT_CASES`).

## Architecture

Interactive terminal app with no web layer (`frontend/` holds only untracked build output). Flow: `main.py` menu → `league_simulator.py` (pick format and teams) → a tournament function in `fixtures/` → `match_simulator.simulate_match` → `database.py` persistence.

- **Ball model**: `probability.py` holds the per-ball math. `calculate_ball_probabilities` combines the 7 difficulty coefficients from the active `config.json` profile with the striker's batting rating and the bowler's *effective* bowling (`skill + up_value - fatigue_rate * overs_bowled`, settings under `game_settings.bowler_fatigue`). The death-overs boosts (last 4 overs) are hard-coded constants in `probability.py`. The `game_settings.final_4_excitement_multiplier` and `overs_in_final_4` keys in `config.json` are not read anywhere.
- **Difficulty profiles**: `config_manager.py` reads and writes `config.json`. The `advanced` profile gets overwritten by user input during Advanced Controls, and `reset_advanced_profile()` copies `balanced` back into it after a league ends. That is why `config.json` often shows up modified in git; check `git diff config.json` before committing it.
- **Teams and bowling orders** (`teams.py`): `get_teams()` maps a team code to a list of 11 `models.Player(name, batting, bowling)`, with ratings on a 0–10 scale. `BOWLING_ORDERS` maps a team code to a 20-character string with one letter per over. Letters come from `get_bowler_ranking()`: A = the highest bowling rating, B = the next, and so on, with ties broken by name. The `# A`/`# B` comments beside players record that ranking, so changing a bowling rating can silently change which player a letter points to. Teams without an entry use the default `"ABABCDECDECDECDEABAB"`. `tests/test_teams.py` enforces 20 overs, letters A–K only, and no bowler over 4 overs.
- **Tournament formats** (`fixtures/`): each format is a function `(selected_teams, playoff_ball_by_ball, league_ball_by_ball)` registered in the `TOURNAMENT_FORMATS` dict in `fixtures/__init__.py`. To add a format, write a module and register it there. `wc26_format.py` uses `teams_helper.divide_teams_into_balanced_groups` (strength-based grouping) and per-stage NRR snapshots. Formats pass `stage="playoff"` to `simulate_match` for knockout games.
- **Persistence**: SQLite at `database/cricsim.db` (gitignored). `db/connection.py` provides `get_conn()` (a context manager that commits on clean exit and rolls back on an exception) and `ensure_db()`, which applies `db/schema.sql` on each connect. `schema.sql` only uses `CREATE TABLE IF NOT EXISTS`, so **adding a column to an existing table requires an idempotent `ALTER` in `_apply_migrations()`**. `database.py` keeps the API of the old JSON storage (dict-shaped `load_players`/`save_players` etc.) on top of SQLite. The README's mention of `player_stats.json`/`team_stats.json` is out of date.
- **Current vs historical**: current-season tables (`players`, `teams`, `matches`, `match_batting`, `match_bowling`, `cumulative_teams`) hold in-progress stats. `historical.py` copies a finished season into `historical_*` tables (`archive_current_season`) and serves all-time and per-season queries and player cards. Archiving never clears the current tables; that happens only through `database.clear_database()`.
- **Output**: `match_simulator.py` and `top_players.py` import `rich` unconditionally, so in practice `rich` is required, even though the README calls it optional.
