"""
database.py

SQLite-backed persistence layer for CricSim.

Public API is preserved from the previous JSON-backed version so the rest
of the codebase does not change. All reads and writes now go through
SQLite via the helpers in db/connection.py.

Tables live in database/cricsim.db. Schema is in db/schema.sql.
"""
from datetime import datetime

from db.connection import ensure_db, get_conn


def _row_to_player_dict(row):
    """Convert a `players` row into the dict shape callers used to see."""
    return {
        "team": row["team"],
        "runs": row["runs"],
        "balls_faced": row["balls_faced"],
        "fours": row["fours"],
        "sixes": row["sixes"],
        "matches": row["matches"],
        "outs": row["outs"],
        "not_outs": row["not_outs"],
        "highest_score": row["highest_score"],
        "wickets": row["wickets"],
        "balls_bowled": row["balls_bowled"],
        "best_bowling": {
            "wickets": row["best_bowling_wickets"],
            "runs": row["best_bowling_runs"],
        },
    }


def _row_to_team_dict(row):
    """Convert a `teams` row into the dict shape callers used to see."""
    return {
        "played": row["played"],
        "won": row["won"],
        "lost": row["lost"],
        "tied": row["tied"],
        "points": row["points"],
        "runs_scored": row["runs_scored"],
        "runs_conceded": row["runs_conceded"],
        "balls_faced": row["balls_faced"],
        "balls_bowled": row["balls_bowled"],
    }


def load_players():
    with get_conn() as con:
        rows = con.execute("SELECT * FROM players").fetchall()
    return {r["name"]: _row_to_player_dict(r) for r in rows}


def save_players(players):
    """Replace the entire players table with the given dict.

    Kept for API compatibility; the runtime path uses update_players_from_match
    instead of full rewrites.
    """
    with get_conn() as con:
        con.execute("DELETE FROM players")
        for name, p in players.items():
            bb = p.get("best_bowling") or {}
            con.execute(
                """
                INSERT INTO players
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


def load_teams():
    with get_conn() as con:
        rows = con.execute("SELECT * FROM teams").fetchall()
    return {r["team_code"]: _row_to_team_dict(r) for r in rows}


def save_teams(teams):
    """Replace the entire teams table with the given dict."""
    with get_conn() as con:
        con.execute("DELETE FROM teams")
        for code, t in teams.items():
            con.execute(
                """
                INSERT INTO teams
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


def save_match_file(teamA_name, teamB_name, A_bat, A_bowl, B_bat, B_bowl,
                    teamA_objs=None, teamB_objs=None, result=None,
                    A_score=None, B_score=None, stage="league"):
    """Persist one match (header + batting + bowling) into SQLite.

    The function name is kept for API compatibility with the JSON era.
    Returns the new match_id (the previous JSON version returned a file
    path; no caller actually uses the return value).

    Args:
        stage: 'league' (default) or 'playoff'. Used to distinguish playoff
            knockouts from regular-season matches when archiving and when
            running historical queries.
    """
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    if not isinstance(result, dict):
        if A_score is not None and B_score is not None:
            if A_score > B_score:
                result = {"winner": teamA_name, "by": f"{A_score - B_score} runs",
                          "A_score": A_score, "B_score": B_score}
            elif B_score > A_score:
                result = {"winner": teamB_name, "by": f"{B_score - A_score} runs",
                          "A_score": A_score, "B_score": B_score}
            else:
                result = {"winner": "TIE", "by": "", "A_score": A_score, "B_score": B_score}
        else:
            result = {}

    def _attach_name(stat, objs, i):
        if not (objs and i < len(objs)):
            return None
        try:
            return objs[i].name
        except Exception:
            return None

    with get_conn() as con:
        cur = con.execute(
            """
            INSERT INTO matches
            (team_a, team_b, timestamp_utc, winner, margin, a_score, b_score, stage)
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (
                teamA_name,
                teamB_name,
                ts,
                result.get("winner"),
                result.get("by", ""),
                result.get("A_score"),
                result.get("B_score"),
                stage,
            ),
        )
        match_id = cur.lastrowid

        for team, bat_list, objs in (
            (teamA_name, A_bat, teamA_objs),
            (teamB_name, B_bat, teamB_objs),
        ):
            if not isinstance(bat_list, list):
                continue
            for i, st in enumerate(bat_list):
                if not isinstance(st, dict):
                    st = {"value": st}
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
                        _attach_name(st, objs, i),
                        st.get("runs", 0),
                        st.get("balls", 0),
                        st.get("4s", 0),
                        st.get("6s", 0),
                        st.get("dismissal", "not out"),
                    ),
                )

        for team, bowl_map in ((teamA_name, A_bowl), (teamB_name, B_bowl)):
            if not isinstance(bowl_map, dict):
                continue
            for bowler, st in bowl_map.items():
                if st.get("balls", 0) <= 0:
                    continue
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
                        st.get("overs", 0),
                        st.get("balls", 0),
                        st.get("runs", 0),
                        st.get("wickets", 0),
                    ),
                )

    return match_id


def update_players_from_match(team_name, batting_team, batting_stats, bowling_stats):
    """Increment aggregate player stats from a single match's batting and bowling.

    Mirrors the original JSON-era semantics:
    - `matches` is incremented only in the batting loop (once per player on
      the batting side).
    - The bowler's `team` field is set to the caller's `team_name`, even
      though those bowlers actually belong to the opposing side. This is
      preserved verbatim from the previous behavior.
    """
    with get_conn() as con:
        for i, player in enumerate(batting_team):
            name = player.name
            st = batting_stats[i]
            runs = st.get("runs", 0)
            balls = st.get("balls", 0)
            fours = st.get("4s", 0)
            sixes = st.get("6s", 0)
            dismissal = st.get("dismissal", "not out").strip().lower()

            con.execute(
                "INSERT OR IGNORE INTO players (name, team) VALUES (?, ?)",
                (name, team_name),
            )

            outs_delta, not_outs_delta = (0, 1) if dismissal == "not out" else (1, 0)

            con.execute(
                """
                UPDATE players SET
                    team          = COALESCE(team, ?),
                    runs          = runs + ?,
                    balls_faced   = balls_faced + ?,
                    fours         = fours + ?,
                    sixes         = sixes + ?,
                    matches       = matches + 1,
                    outs          = outs + ?,
                    not_outs      = not_outs + ?,
                    highest_score = CASE WHEN ? > highest_score THEN ? ELSE highest_score END
                WHERE name = ?
                """,
                (
                    team_name,
                    runs, balls, fours, sixes,
                    outs_delta, not_outs_delta,
                    runs, runs,
                    name,
                ),
            )

        for bowler_name, st in bowling_stats.items():
            w = st.get("wickets", 0)
            balls_bowled = st.get("balls", 0)
            runs_conceded = st.get("runs", 0)

            con.execute(
                "INSERT OR IGNORE INTO players (name, team) VALUES (?, ?)",
                (bowler_name, team_name),
            )

            con.execute(
                """
                UPDATE players SET
                    team         = COALESCE(team, ?),
                    wickets      = wickets + ?,
                    balls_bowled = balls_bowled + ?
                WHERE name = ?
                """,
                (team_name, w, balls_bowled, bowler_name),
            )

            con.execute(
                """
                UPDATE players SET
                    best_bowling_wickets = ?,
                    best_bowling_runs    = ?
                WHERE name = ?
                  AND (
                        ? > best_bowling_wickets
                        OR (? = best_bowling_wickets AND ? < best_bowling_runs)
                      )
                """,
                (w, runs_conceded, bowler_name, w, w, runs_conceded),
            )


def update_team_from_match(teamA_name, teamB_name, A_score, B_score,
                            A_overs_batted_balls, B_overs_batted_balls, winner):
    with get_conn() as con:
        for team in (teamA_name, teamB_name):
            con.execute("INSERT OR IGNORE INTO teams (team_code) VALUES (?)", (team,))

        con.execute(
            """
            UPDATE teams SET
                played        = played + 1,
                runs_scored   = runs_scored   + ?,
                runs_conceded = runs_conceded + ?,
                balls_faced   = balls_faced   + ?,
                balls_bowled  = balls_bowled  + ?
            WHERE team_code = ?
            """,
            (A_score, B_score, A_overs_batted_balls, B_overs_batted_balls, teamA_name),
        )
        con.execute(
            """
            UPDATE teams SET
                played        = played + 1,
                runs_scored   = runs_scored   + ?,
                runs_conceded = runs_conceded + ?,
                balls_faced   = balls_faced   + ?,
                balls_bowled  = balls_bowled  + ?
            WHERE team_code = ?
            """,
            (B_score, A_score, B_overs_batted_balls, A_overs_batted_balls, teamB_name),
        )

        if winner == teamA_name:
            con.execute("UPDATE teams SET won = won + 1, points = points + 2 WHERE team_code = ?", (teamA_name,))
            con.execute("UPDATE teams SET lost = lost + 1 WHERE team_code = ?", (teamB_name,))
        elif winner == teamB_name:
            con.execute("UPDATE teams SET won = won + 1, points = points + 2 WHERE team_code = ?", (teamB_name,))
            con.execute("UPDATE teams SET lost = lost + 1 WHERE team_code = ?", (teamA_name,))
        else:
            con.execute("UPDATE teams SET tied = tied + 1, points = points + 1 WHERE team_code = ?", (teamA_name,))
            con.execute("UPDATE teams SET tied = tied + 1, points = points + 1 WHERE team_code = ?", (teamB_name,))


def get_orange_purple(top_n=10):
    with get_conn() as con:
        runs_rows = con.execute(
            "SELECT * FROM players ORDER BY runs DESC LIMIT ?", (top_n,)
        ).fetchall()
        wkts_rows = con.execute(
            "SELECT * FROM players ORDER BY wickets DESC LIMIT ?", (top_n,)
        ).fetchall()
    runs_sorted = [(r["name"], _row_to_player_dict(r)) for r in runs_rows]
    wkts_sorted = [(r["name"], _row_to_player_dict(r)) for r in wkts_rows]
    return runs_sorted, wkts_sorted


def compute_nrr_for_team_entry(entry):
    bf = entry.get("balls_faced", 0)
    bb = entry.get("balls_bowled", 0)
    if bf == 0 or bb == 0:
        return 0.0
    rs = entry.get("runs_scored", 0) / (bf / 6.0)
    rc = entry.get("runs_conceded", 0) / (bb / 6.0)
    return round(rs - rc, 3)


def compute_nrr(runs_scored, runs_conceded, balls_faced, balls_bowled):
    """Compute NRR from raw stats.

    Returns 0.0 if either side has 0 balls.
    """
    if balls_faced == 0 or balls_bowled == 0:
        return 0.0
    rs = runs_scored / (balls_faced / 6.0)
    rc = runs_conceded / (balls_bowled / 6.0)
    return round(rs - rc, 3)


def get_team_stats(team_name):
    """Return per-team raw stats used for NRR snapshotting.

    Returns zero-initialized dict if team is missing.
    """
    with get_conn() as con:
        row = con.execute(
            "SELECT runs_scored, runs_conceded, balls_faced, balls_bowled "
            "FROM teams WHERE team_code = ?",
            (team_name,),
        ).fetchone()
    if not row:
        return {
            "runs_scored": 0,
            "runs_conceded": 0,
            "balls_faced": 0,
            "balls_bowled": 0,
        }
    return {
        "runs_scored": row["runs_scored"],
        "runs_conceded": row["runs_conceded"],
        "balls_faced": row["balls_faced"],
        "balls_bowled": row["balls_bowled"],
    }


def get_points_table_sorted():
    teams = load_teams()
    table = []
    for team, entry in teams.items():
        nrr = compute_nrr_for_team_entry(entry)
        table.append({
            "team": team,
            "played": entry.get("played", 0),
            "won": entry.get("won", 0),
            "lost": entry.get("lost", 0),
            "tied": entry.get("tied", 0),
            "points": entry.get("points", 0),
            "nrr": nrr,
            "runs_scored": entry.get("runs_scored", 0),
            "runs_conceded": entry.get("runs_conceded", 0),
        })
    return sorted(table, key=lambda r: (r["points"], r["nrr"]), reverse=True)


def clear_database(silent=False):
    """Wipe all rows from the SQLite tables. Keeps schema and the .db file.

    Args:
        silent: when True, suppress the success print so callers can render
            their own message (used by the post-archive auto-clear flow).
    """
    with get_conn() as con:
        for t in ("match_batting", "match_bowling", "matches",
                  "players", "teams", "cumulative_teams"):
            con.execute(f"DELETE FROM {t}")
        con.execute("DELETE FROM sqlite_sequence")
    if not silent:
        print("Database cleared.")


def print_caps_and_table():
    try:
        from rich.console import Console
        from rich.table import Table
        from rich import box
        console = Console()
    except Exception:
        console = None

    runs_sorted, wkts_sorted = get_orange_purple(10)

    if console:
        orange_table = Table(title="🧡 ORANGE CAP (Top Run Scorers)", box=box.DOUBLE, style="bold orange1")
        orange_table.add_column("#", justify="right", style="yellow")
        orange_table.add_column("Player", style="cyan")
        orange_table.add_column("Runs", justify="right", style="bold green")

        for idx, (name, data) in enumerate(runs_sorted, 1):
            runs = data.get('runs', 0)
            orange_table.add_row(str(idx), name, f"{runs}")

        console.print()
        console.print(orange_table)

        purple_table = Table(title="💜 PURPLE CAP (Top Wicket Takers)", box=box.DOUBLE, style="bold magenta")
        purple_table.add_column("#", justify="right", style="yellow")
        purple_table.add_column("Player", style="cyan")
        purple_table.add_column("Wickets", justify="right", style="bold red")

        for idx, (name, data) in enumerate(wkts_sorted, 1):
            wkts = data.get('wickets', 0)
            purple_table.add_row(str(idx), name, f"{wkts}")

        console.print(purple_table)

        table = get_points_table_sorted()
        points_table = Table(title="🏆 POINTS TABLE", box=box.HEAVY_HEAD, style="bold white on blue")
        points_table.add_column("#", justify="center", style="yellow")
        points_table.add_column("Team", style="bold cyan")
        points_table.add_column("P", justify="right", style="white")
        points_table.add_column("W", justify="right", style="green")
        points_table.add_column("L", justify="right", style="red")
        points_table.add_column("T", justify="right", style="yellow")
        points_table.add_column("Pts", justify="right", style="bold white")
        points_table.add_column("NRR", justify="right", style="cyan")

        for idx, r in enumerate(table, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx:2d}."
            points_table.add_row(
                medal,
                r['team'],
                str(r['played']),
                str(r['won']),
                str(r['lost']),
                str(r['tied']),
                str(r['points']),
                f"{r['nrr']:>7.3f}",
            )

        console.print(points_table)
        console.print()
    else:
        print("\n===== ORANGE CAP (Top Run Scorers) =====")
        for name, data in runs_sorted:
            print(f"{name:30} {data.get('runs',0)} runs")

        print("\n===== PURPLE CAP (Top Wicket Takers) =====")
        for name, data in wkts_sorted:
            print(f"{name:30} {data.get('wickets',0)} wickets")

        print("\n===== POINTS TABLE =====")
        table = get_points_table_sorted()
        print(f"{'Team':8} {'P':>3} {'W':>3} {'L':>3} {'T':>3} {'Pts':>4} {'NRR':>7}")
        for r in table:
            print(f"{r['team']:8} {r['played']:>3} {r['won']:>3} {r['lost']:>3} {r['tied']:>3} {r['points']:>4} {r['nrr']:>7.3f}")


def print_points_table():
    """Print only the points table (no orange/purple caps)."""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich import box
        console = Console()
    except Exception:
        console = None

    table = get_points_table_sorted()

    if console:
        points_table = Table(title="POINTS TABLE", box=box.HEAVY_HEAD, style="bold white on blue")
        points_table.add_column("#", justify="center", style="yellow")
        points_table.add_column("Team", style="bold cyan")
        points_table.add_column("P", justify="right", style="white")
        points_table.add_column("W", justify="right", style="green")
        points_table.add_column("L", justify="right", style="red")
        points_table.add_column("T", justify="right", style="yellow")
        points_table.add_column("Pts", justify="right", style="bold white")
        points_table.add_column("NRR", justify="right", style="cyan")

        for idx, r in enumerate(table, 1):
            points_table.add_row(
                str(idx),
                r['team'],
                str(r['played']),
                str(r['won']),
                str(r['lost']),
                str(r['tied']),
                str(r['points']),
                f"{r['nrr']:>7.3f}",
            )

        console.print(points_table)
        console.print()
    else:
        print("\n===== POINTS TABLE =====")
        print(f"{'Team':8} {'P':>3} {'W':>3} {'L':>3} {'T':>3} {'Pts':>4} {'NRR':>7}")
        for r in table:
            print(f"{r['team']:8} {r['played']:>3} {r['won']:>3} {r['lost']:>3} {r['tied']:>3} {r['points']:>4} {r['nrr']:>7.3f}")


def load_cumulative_stats():
    with get_conn() as con:
        rows = con.execute("SELECT * FROM cumulative_teams").fetchall()
    return {
        r["team_code"]: {
            "played": r["played"],
            "won": r["won"],
            "lost": r["lost"],
            "tied": r["tied"],
            "points": r["points"],
        }
        for r in rows
    }


def save_cumulative_stats(stats):
    with get_conn() as con:
        con.execute("DELETE FROM cumulative_teams")
        for code, t in stats.items():
            con.execute(
                """
                INSERT INTO cumulative_teams
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


def print_season_points_table(season_points_dict, season_number):
    """Print season-specific points table (unchanged from JSON era)."""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich import box
        console = Console()
    except Exception:
        console = None

    if console:
        season_table = Table(title=f"📊 SEASON {season_number} POINTS TABLE", box=box.HEAVY_HEAD, style="bold white on blue")
        season_table.add_column("#", justify="center", style="yellow")
        season_table.add_column("Team", style="bold cyan")
        season_table.add_column("P", justify="right", style="white")
        season_table.add_column("W", justify="right", style="green")
        season_table.add_column("L", justify="right", style="red")
        season_table.add_column("T", justify="right", style="yellow")
        season_table.add_column("Pts", justify="right", style="bold white")

        sorted_teams = sorted(season_points_dict.items(), key=lambda x: (-x[1]["points"], x[0]))
        for idx, (team, stats) in enumerate(sorted_teams, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx:2d}."
            season_table.add_row(
                medal,
                team,
                str(stats["played"]),
                str(stats["won"]),
                str(stats["lost"]),
                str(stats["tied"]),
                str(stats["points"]),
            )

        console.print()
        console.print(season_table)
        console.print()
    else:
        print(f"\n===== SEASON {season_number} POINTS TABLE =====")
        print(f"{'#':>3} {'Team':15} {'P':>3} {'W':>3} {'L':>3} {'T':>3} {'Pts':>4}")
        sorted_teams = sorted(season_points_dict.items(), key=lambda x: (-x[1]["points"], x[0]))
        for idx, (team, stats) in enumerate(sorted_teams, 1):
            print(f"{idx:>3} {team:15} {stats['played']:>3} {stats['won']:>3} {stats['lost']:>3} {stats['tied']:>3} {stats['points']:>4}")


def update_cumulative_stats():
    """Update cumulative_teams by adding current teams stats on top."""
    cumulative = load_cumulative_stats()
    current_teams = load_teams()

    for team, stats in current_teams.items():
        if team not in cumulative:
            cumulative[team] = {"played": 0, "won": 0, "lost": 0, "tied": 0, "points": 0}
        cumulative[team]["played"] += stats.get("played", 0)
        cumulative[team]["won"]    += stats.get("won", 0)
        cumulative[team]["lost"]   += stats.get("lost", 0)
        cumulative[team]["tied"]   += stats.get("tied", 0)
        cumulative[team]["points"] += stats.get("points", 0)

    save_cumulative_stats(cumulative)


def print_full_points_table():
    """Print cumulative points table across all seasons (unchanged from JSON era)."""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich import box
        console = Console()
    except Exception:
        console = None

    cumulative = load_cumulative_stats()

    if not cumulative:
        print("No cumulative stats yet")
        return

    if console:
        full_table = Table(title="📈 FULL POINTS TABLE (All Seasons)", box=box.HEAVY_HEAD, style="bold white on blue")
        full_table.add_column("#", justify="center", style="yellow")
        full_table.add_column("Team", style="bold cyan")
        full_table.add_column("P", justify="right", style="white")
        full_table.add_column("W", justify="right", style="green")
        full_table.add_column("L", justify="right", style="red")
        full_table.add_column("T", justify="right", style="yellow")
        full_table.add_column("Total Pts", justify="right", style="bold white")

        sorted_teams = sorted(cumulative.items(), key=lambda x: (-x[1]["points"], x[0]))
        for idx, (team, stats) in enumerate(sorted_teams, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx:2d}."
            full_table.add_row(
                medal,
                team,
                str(stats["played"]),
                str(stats["won"]),
                str(stats["lost"]),
                str(stats["tied"]),
                str(stats["points"]),
            )

        console.print()
        console.print(full_table)
        console.print()
    else:
        print("\n===== FULL POINTS TABLE (All Seasons) =====")
        print(f"{'#':>3} {'Team':15} {'P':>3} {'W':>3} {'L':>3} {'T':>3} {'Total Pts':>9}")
        sorted_teams = sorted(cumulative.items(), key=lambda x: (-x[1]["points"], x[0]))
        for idx, (team, stats) in enumerate(sorted_teams, 1):
            print(f"{idx:>3} {team:15} {stats['played']:>3} {stats['won']:>3} {stats['lost']:>3} {stats['tied']:>3} {stats['points']:>9}")
