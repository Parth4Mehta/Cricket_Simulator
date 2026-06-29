"""
historical.py

Historical archive layer.

Functions for archiving a completed season into the historical_* tables
and for reading historical data back in multiple shapes:
- list of archived seasons
- per-season points table
- per-season top-N players (any of the 15 categories)
- all-time aggregate points table (across all archived seasons)
- all-time aggregate top-N players
- per-player career card (current season OR historical all-time OR historical specific season)

The current-season tables (`players`, `teams`, `matches`, etc.) are NEVER
touched here. The end-of-league archive flow copies data OUT of the current
tables INTO the historical_* tables. The user explicitly clears current
state via the existing clear_database() function when they want to start
a new season.
"""
from datetime import datetime

from db.connection import get_conn
import database


# ===========================================================================
# Archive flow
# ===========================================================================

def _next_season_name(con):
    """Auto-generate the next season name as 'Season N'."""
    row = con.execute("SELECT COALESCE(MAX(season_id), 0) FROM seasons").fetchone()
    return f"Season {row[0] + 1}"


def archive_current_season(champion=None):
    """Copy the contents of the current-season tables into historical_*.

    Returns the new season_id, or None if there is nothing to archive
    (no current matches).

    Does NOT clear the current tables. The user clears via menu option 5
    when they're ready to start a new league.

    Args:
        champion: name of the team that won the final, if any.
    """
    with get_conn() as con:
        current_match_count = con.execute("SELECT COUNT(*) FROM matches").fetchone()[0]
        if current_match_count == 0:
            return None

        team_count = con.execute("SELECT COUNT(*) FROM teams").fetchone()[0]
        name = _next_season_name(con)
        archived_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        cur = con.execute(
            """
            INSERT INTO seasons (name, archived_at, champion, num_matches, num_teams)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, archived_at, champion, current_match_count, team_count),
        )
        season_id = cur.lastrowid

        # Copy matches and remember the new historical_match_id mapping.
        match_id_map = {}
        rows = con.execute(
            "SELECT match_id, team_a, team_b, timestamp_utc, winner, margin, "
            "a_score, b_score, stage FROM matches"
        ).fetchall()
        for r in rows:
            cur = con.execute(
                """
                INSERT INTO historical_matches
                (season_id, team_a, team_b, timestamp_utc, winner, margin,
                 a_score, b_score, stage)
                VALUES (?,?,?,?,?,?,?,?,?)
                """,
                (
                    season_id,
                    r["team_a"], r["team_b"], r["timestamp_utc"],
                    r["winner"], r["margin"],
                    r["a_score"], r["b_score"], r["stage"],
                ),
            )
            match_id_map[r["match_id"]] = cur.lastrowid

        # Copy batting rows.
        bat_rows = con.execute(
            "SELECT match_id, team, position, player_name, runs, balls, "
            "fours, sixes, dismissal FROM match_batting"
        ).fetchall()
        for b in bat_rows:
            new_match_id = match_id_map.get(b["match_id"])
            if new_match_id is None:
                continue
            con.execute(
                """
                INSERT INTO historical_match_batting
                (historical_match_id, team, position, player_name,
                 runs, balls, fours, sixes, dismissal)
                VALUES (?,?,?,?,?,?,?,?,?)
                """,
                (
                    new_match_id, b["team"], b["position"], b["player_name"],
                    b["runs"], b["balls"], b["fours"], b["sixes"], b["dismissal"],
                ),
            )

        # Copy bowling rows.
        bowl_rows = con.execute(
            "SELECT match_id, team, player_name, overs, balls, runs, wickets "
            "FROM match_bowling"
        ).fetchall()
        for b in bowl_rows:
            new_match_id = match_id_map.get(b["match_id"])
            if new_match_id is None:
                continue
            con.execute(
                """
                INSERT INTO historical_match_bowling
                (historical_match_id, team, player_name, overs, balls, runs, wickets)
                VALUES (?,?,?,?,?,?,?)
                """,
                (
                    new_match_id, b["team"], b["player_name"],
                    b["overs"], b["balls"], b["runs"], b["wickets"],
                ),
            )

        # Snapshot final team standings (sorted by points DESC then NRR DESC).
        pts_table = database.get_points_table_sorted()
        for pos, row in enumerate(pts_table, 1):
            team_row = con.execute(
                "SELECT * FROM teams WHERE team_code = ?", (row["team"],)
            ).fetchone()
            if team_row is None:
                continue
            con.execute(
                """
                INSERT INTO historical_team_standings
                (season_id, team_code, final_position, played, won, lost, tied,
                 points, runs_scored, runs_conceded, balls_faced, balls_bowled, nrr)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    season_id, row["team"], pos,
                    team_row["played"], team_row["won"], team_row["lost"], team_row["tied"],
                    team_row["points"], team_row["runs_scored"], team_row["runs_conceded"],
                    team_row["balls_faced"], team_row["balls_bowled"], row["nrr"],
                ),
            )

    return season_id


# ===========================================================================
# Destructive operations (clearing historical data)
# ===========================================================================

def clear_all_historical():
    """Wipe ALL archived seasons and reset the season_id counter.

    Resets so the next archived season becomes 'Season 1' again.
    """
    with get_conn() as con:
        for t in (
            "historical_match_batting",
            "historical_match_bowling",
            "historical_matches",
            "historical_team_standings",
            "seasons",
        ):
            con.execute(f"DELETE FROM {t}")
        con.execute(
            "DELETE FROM sqlite_sequence WHERE name IN ('seasons', 'historical_matches')"
        )


def delete_season(season_id):
    """Delete one archived season (and all its matches/standings/cards).

    Returns True if a row was actually deleted, False if season_id was unknown.
    Explicit child-table deletes are used (belt-and-suspenders) so this works
    even if foreign keys aren't enforced on a given connection.
    """
    with get_conn() as con:
        match_ids = [
            r[0]
            for r in con.execute(
                "SELECT historical_match_id FROM historical_matches WHERE season_id = ?",
                (season_id,),
            ).fetchall()
        ]
        if match_ids:
            placeholders = ",".join("?" * len(match_ids))
            con.execute(
                f"DELETE FROM historical_match_batting WHERE historical_match_id IN ({placeholders})",
                match_ids,
            )
            con.execute(
                f"DELETE FROM historical_match_bowling WHERE historical_match_id IN ({placeholders})",
                match_ids,
            )
        con.execute(
            "DELETE FROM historical_matches WHERE season_id = ?", (season_id,)
        )
        con.execute(
            "DELETE FROM historical_team_standings WHERE season_id = ?", (season_id,)
        )
        cur = con.execute("DELETE FROM seasons WHERE season_id = ?", (season_id,))
        return cur.rowcount > 0


# ===========================================================================
# Season metadata
# ===========================================================================

def list_seasons():
    """Return the list of archived seasons, most recent first."""
    with get_conn() as con:
        rows = con.execute(
            "SELECT season_id, name, archived_at, champion, num_matches, num_teams "
            "FROM seasons ORDER BY season_id DESC"
        ).fetchall()
    return [dict(r) for r in rows]


# ===========================================================================
# Historical points tables
# ===========================================================================

def get_historical_points_table_season(season_id):
    """Final points table for one archived season."""
    with get_conn() as con:
        rows = con.execute(
            """
            SELECT team_code, final_position, played, won, lost, tied, points,
                   runs_scored, runs_conceded, balls_faced, balls_bowled, nrr
            FROM historical_team_standings
            WHERE season_id = ?
            ORDER BY final_position
            """,
            (season_id,),
        ).fetchall()
    return [
        {
            "team": r["team_code"],
            "position": r["final_position"],
            "played": r["played"],
            "won": r["won"],
            "lost": r["lost"],
            "tied": r["tied"],
            "points": r["points"],
            "nrr": r["nrr"],
            "runs_scored": r["runs_scored"],
            "runs_conceded": r["runs_conceded"],
        }
        for r in rows
    ]


def get_historical_points_table_all_time():
    """Aggregate standings across all archived seasons.

    Sums played/W/L/T/points/runs across every season.
    NRR is recomputed from the total runs/balls.
    """
    with get_conn() as con:
        rows = con.execute(
            """
            SELECT
                team_code,
                SUM(played)        AS played,
                SUM(won)           AS won,
                SUM(lost)          AS lost,
                SUM(tied)          AS tied,
                SUM(points)        AS points,
                SUM(runs_scored)   AS runs_scored,
                SUM(runs_conceded) AS runs_conceded,
                SUM(balls_faced)   AS balls_faced,
                SUM(balls_bowled)  AS balls_bowled,
                COUNT(*)           AS seasons_played
            FROM historical_team_standings
            GROUP BY team_code
            """
        ).fetchall()
    table = []
    for r in rows:
        nrr = database.compute_nrr(
            r["runs_scored"], r["runs_conceded"],
            r["balls_faced"], r["balls_bowled"],
        )
        table.append({
            "team": r["team_code"],
            "played": r["played"],
            "won": r["won"],
            "lost": r["lost"],
            "tied": r["tied"],
            "points": r["points"],
            "nrr": nrr,
            "runs_scored": r["runs_scored"],
            "runs_conceded": r["runs_conceded"],
            "seasons_played": r["seasons_played"],
        })
    return sorted(table, key=lambda r: (r["points"], r["nrr"]), reverse=True)


# ===========================================================================
# Historical aggregate -> reuse top_players.compute_categories
# ===========================================================================

def _build_player_aggregates(season_id=None):
    """Build (players_dict, bowling_agg_dict) shaped like the JSON-era
    aggregates that top_players.compute_categories expects.

    If season_id is None: aggregate across ALL archived seasons.
    If season_id is given: aggregate only matches in that season.
    """
    batting_filter = ""
    bowling_filter = ""
    params = ()
    if season_id is not None:
        batting_filter = (
            "WHERE historical_match_id IN ("
            "SELECT historical_match_id FROM historical_matches WHERE season_id = ?)"
        )
        bowling_filter = batting_filter
        params = (season_id,)

    with get_conn() as con:
        # Batting aggregates per player
        bat_rows = con.execute(
            f"""
            SELECT
                player_name,
                SUM(runs)  AS runs,
                SUM(balls) AS balls_faced,
                SUM(fours) AS fours,
                SUM(sixes) AS sixes,
                COUNT(*)   AS innings,
                SUM(CASE WHEN LOWER(TRIM(COALESCE(dismissal,'not out'))) != 'not out' THEN 1 ELSE 0 END) AS outs,
                SUM(CASE WHEN LOWER(TRIM(COALESCE(dismissal,'not out'))) = 'not out' THEN 1 ELSE 0 END) AS not_outs,
                MAX(runs)  AS highest_score
            FROM historical_match_batting
            {batting_filter}
            GROUP BY player_name
            HAVING player_name IS NOT NULL
            """,
            params,
        ).fetchall()

        # Bowling aggregates per player
        bowl_rows = con.execute(
            f"""
            SELECT
                player_name,
                SUM(wickets) AS wickets,
                SUM(balls)   AS balls_bowled,
                SUM(runs)    AS runs_conceded
            FROM historical_match_bowling
            {bowling_filter}
            GROUP BY player_name
            """,
            params,
        ).fetchall()

        # Best-bowling per player: pick the row that maximizes wickets,
        # then minimizes runs. Encode (wickets*100000 - runs) as a single key.
        bb_rows = con.execute(
            f"""
            WITH ranked AS (
                SELECT
                    player_name, wickets, runs,
                    ROW_NUMBER() OVER (
                        PARTITION BY player_name
                        ORDER BY wickets DESC, runs ASC
                    ) AS rk
                FROM historical_match_bowling
                {bowling_filter}
            )
            SELECT player_name, wickets, runs FROM ranked WHERE rk = 1
            """,
            params,
        ).fetchall()

        # Match count per player (used for the "matches" field in tables).
        # A player's matches = distinct historical_match_ids where they appear
        # in either batting or bowling.
        match_count_rows = con.execute(
            f"""
            SELECT player_name, COUNT(DISTINCT historical_match_id) AS matches FROM (
                SELECT player_name, historical_match_id FROM historical_match_batting {batting_filter}
                UNION
                SELECT player_name, historical_match_id FROM historical_match_bowling {bowling_filter}
            )
            GROUP BY player_name
            HAVING player_name IS NOT NULL
            """,
            params + params,
        ).fetchall()

    players = {}
    for r in bat_rows:
        players[r["player_name"]] = {
            "runs": r["runs"] or 0,
            "balls_faced": r["balls_faced"] or 0,
            "fours": r["fours"] or 0,
            "sixes": r["sixes"] or 0,
            "outs": r["outs"] or 0,
            "not_outs": r["not_outs"] or 0,
            "highest_score": r["highest_score"] or 0,
            "matches": 0,  # filled in below
            "wickets": 0,
            "balls_bowled": 0,
            "best_bowling": {"wickets": 0, "runs": 999},
        }
    for r in bowl_rows:
        name = r["player_name"]
        if name not in players:
            players[name] = {
                "runs": 0, "balls_faced": 0, "fours": 0, "sixes": 0,
                "outs": 0, "not_outs": 0, "highest_score": 0,
                "matches": 0,
                "best_bowling": {"wickets": 0, "runs": 999},
            }
        players[name]["wickets"] = r["wickets"] or 0
        players[name]["balls_bowled"] = r["balls_bowled"] or 0
    for r in bb_rows:
        name = r["player_name"]
        if name in players:
            players[name]["best_bowling"] = {
                "wickets": r["wickets"] or 0,
                "runs": r["runs"] if r["runs"] is not None else 999,
            }
    for r in match_count_rows:
        name = r["player_name"]
        if name in players:
            players[name]["matches"] = r["matches"]

    # Bowling aggregate for the economy / bowling-average categories
    bowling_agg = {}
    for r in bowl_rows:
        bowling_agg[r["player_name"]] = {
            "runs_conceded": r["runs_conceded"] or 0,
            "balls_bowled": r["balls_bowled"] or 0,
        }

    return players, bowling_agg


def get_historical_top_players(season_id=None):
    """Return the same 15-category dict that top_players.compute_categories
    returns, but built from historical tables.
    """
    from top_players import compute_categories
    players, bowling_agg = _build_player_aggregates(season_id=season_id)
    return compute_categories(players, bowling_agg)


def get_historical_orange_purple(top_n=10, season_id=None):
    """Top run-scorers and top wicket-takers from historical data."""
    players, _ = _build_player_aggregates(season_id=season_id)
    runs_sorted = sorted(players.items(), key=lambda x: x[1].get("runs", 0), reverse=True)[:top_n]
    wkts_sorted = sorted(players.items(), key=lambda x: x[1].get("wickets", 0), reverse=True)[:top_n]
    return runs_sorted, wkts_sorted


# ===========================================================================
# Per-player full card
# ===========================================================================

def _strike_rate(runs, balls):
    if balls <= 0:
        return None
    return round(runs * 100.0 / balls, 2)


def _bat_average(runs, outs):
    if outs <= 0:
        return None
    return round(runs / outs, 2)


def _economy(runs, balls):
    if balls <= 0:
        return None
    overs = balls / 6.0
    return round(runs / overs, 2)


def _bowl_average(runs, wickets):
    if wickets <= 0:
        return None
    return round(runs / wickets, 2)


def _format_overs(balls):
    return f"{balls // 6}.{balls % 6}"


def get_player_card_current(name):
    """Full per-player card from CURRENT season tables.

    Returns a dict with batting + bowling derived stats, or None if the
    player is not in the current players table.
    """
    with get_conn() as con:
        row = con.execute(
            "SELECT * FROM players WHERE name = ?", (name,)
        ).fetchone()
    if row is None:
        return None
    bat = {
        "matches": row["matches"],
        "runs": row["runs"],
        "balls_faced": row["balls_faced"],
        "fours": row["fours"],
        "sixes": row["sixes"],
        "highest_score": row["highest_score"],
        "outs": row["outs"],
        "not_outs": row["not_outs"],
        "strike_rate": _strike_rate(row["runs"], row["balls_faced"]),
        "average": _bat_average(row["runs"], row["outs"]),
    }
    bowl = {
        "wickets": row["wickets"],
        "balls_bowled": row["balls_bowled"],
        "overs": _format_overs(row["balls_bowled"]),
        # We don't track runs_conceded per player in the aggregate; pull from
        # match_bowling for an honest figure.
        "runs_conceded": None,
        "economy": None,
        "average": None,
        "best_bowling": {
            "wickets": row["best_bowling_wickets"],
            "runs": row["best_bowling_runs"] if row["best_bowling_runs"] != 999 else None,
        },
    }
    with get_conn() as con:
        rc = con.execute(
            "SELECT SUM(runs) AS rc, SUM(balls) AS b "
            "FROM match_bowling WHERE player_name = ?",
            (name,),
        ).fetchone()
    if rc and rc["b"]:
        bowl["runs_conceded"] = rc["rc"] or 0
        bowl["economy"] = _economy(rc["rc"] or 0, rc["b"] or 0)
        bowl["average"] = _bowl_average(rc["rc"] or 0, row["wickets"])
    return {
        "name": name,
        "team": row["team"],
        "source": "current",
        "batting": bat,
        "bowling": bowl,
    }


def get_player_card_historical(name, season_id=None):
    """Full per-player card from HISTORICAL tables.

    If season_id is None: aggregate across all archived seasons.
    If season_id is given: scoped to that season.

    Returns None if the player has no historical rows in scope.
    """
    where_match = ""
    params_match = (name,)
    if season_id is not None:
        where_match = (
            "AND historical_match_id IN ("
            "SELECT historical_match_id FROM historical_matches WHERE season_id = ?)"
        )
        params_match = (name, season_id)

    with get_conn() as con:
        bat = con.execute(
            f"""
            SELECT
                SUM(runs)  AS runs,
                SUM(balls) AS balls_faced,
                SUM(fours) AS fours,
                SUM(sixes) AS sixes,
                COUNT(*)   AS innings,
                SUM(CASE WHEN LOWER(TRIM(COALESCE(dismissal,'not out'))) != 'not out' THEN 1 ELSE 0 END) AS outs,
                SUM(CASE WHEN LOWER(TRIM(COALESCE(dismissal,'not out'))) = 'not out' THEN 1 ELSE 0 END) AS not_outs,
                MAX(runs)  AS highest_score
            FROM historical_match_batting
            WHERE player_name = ? {where_match}
            """,
            params_match,
        ).fetchone()

        bowl = con.execute(
            f"""
            SELECT
                SUM(wickets) AS wickets,
                SUM(balls)   AS balls_bowled,
                SUM(runs)    AS runs_conceded
            FROM historical_match_bowling
            WHERE player_name = ? {where_match}
            """,
            params_match,
        ).fetchone()

        bb = con.execute(
            f"""
            SELECT wickets, runs FROM historical_match_bowling
            WHERE player_name = ? {where_match}
            ORDER BY wickets DESC, runs ASC
            LIMIT 1
            """,
            params_match,
        ).fetchone()

        # Distinct matches across batting + bowling
        match_count = con.execute(
            f"""
            SELECT COUNT(DISTINCT historical_match_id) AS m FROM (
                SELECT historical_match_id FROM historical_match_batting
                WHERE player_name = ? {where_match}
                UNION
                SELECT historical_match_id FROM historical_match_bowling
                WHERE player_name = ? {where_match}
            )
            """,
            params_match + params_match,
        ).fetchone()

        team_row = con.execute(
            f"""
            SELECT team FROM historical_match_batting
            WHERE player_name = ? {where_match}
            ORDER BY historical_match_id DESC LIMIT 1
            """,
            params_match,
        ).fetchone()

    if (not bat or not bat["innings"]) and (not bowl or not bowl["balls_bowled"]):
        return None

    bat_card = {
        "matches": match_count["m"] if match_count else 0,
        "innings": bat["innings"] or 0,
        "runs": bat["runs"] or 0,
        "balls_faced": bat["balls_faced"] or 0,
        "fours": bat["fours"] or 0,
        "sixes": bat["sixes"] or 0,
        "highest_score": bat["highest_score"] or 0,
        "outs": bat["outs"] or 0,
        "not_outs": bat["not_outs"] or 0,
        "strike_rate": _strike_rate(bat["runs"] or 0, bat["balls_faced"] or 0),
        "average": _bat_average(bat["runs"] or 0, bat["outs"] or 0),
    }
    bowl_card = {
        "wickets": bowl["wickets"] or 0,
        "balls_bowled": bowl["balls_bowled"] or 0,
        "overs": _format_overs(bowl["balls_bowled"] or 0),
        "runs_conceded": bowl["runs_conceded"] or 0,
        "economy": _economy(bowl["runs_conceded"] or 0, bowl["balls_bowled"] or 0),
        "average": _bowl_average(bowl["runs_conceded"] or 0, bowl["wickets"] or 0),
        "best_bowling": {
            "wickets": bb["wickets"] if bb else 0,
            "runs": bb["runs"] if bb else None,
        },
    }
    return {
        "name": name,
        "team": team_row["team"] if team_row else None,
        "source": "historical" if season_id is None else f"historical:season_{season_id}",
        "batting": bat_card,
        "bowling": bowl_card,
    }


# ===========================================================================
# Pretty printing for the menu
# ===========================================================================

def _try_rich():
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich import box
        return Console, Table, Panel, box
    except Exception:
        return None


def print_player_card(card):
    """Render a player card in the same style as the existing menus."""
    if card is None:
        print("\nPlayer not found in this view.\n")
        return

    rich = _try_rich()

    def _fmt(v, suffix=""):
        if v is None:
            return "-"
        return f"{v}{suffix}"

    if not rich:
        bat = card["batting"]
        bowl = card["bowling"]
        print(f"\n=== {card['name']}  ({card.get('team') or '-'})  [source: {card['source']}] ===")
        print(" BATTING")
        print(f"   matches  : {_fmt(bat.get('matches'))}")
        print(f"   innings  : {_fmt(bat.get('innings', bat.get('matches')))}")
        print(f"   runs     : {_fmt(bat['runs'])}")
        print(f"   balls    : {_fmt(bat['balls_faced'])}")
        print(f"   SR       : {_fmt(bat['strike_rate'])}")
        print(f"   average  : {_fmt(bat['average'])}")
        print(f"   4s/6s    : {bat['fours']}/{bat['sixes']}")
        print(f"   HS       : {bat['highest_score']}")
        print(f"   outs/NO  : {bat['outs']}/{bat['not_outs']}")
        print(" BOWLING")
        print(f"   overs    : {bowl['overs']}")
        print(f"   wickets  : {bowl['wickets']}")
        print(f"   runs     : {_fmt(bowl['runs_conceded'])}")
        print(f"   economy  : {_fmt(bowl['economy'])}")
        print(f"   average  : {_fmt(bowl['average'])}")
        bb = bowl['best_bowling']
        bb_str = f"{bb['wickets']}/{bb['runs']}" if bb['runs'] is not None else "-"
        print(f"   best     : {bb_str}")
        print()
        return

    Console, Table, Panel, box = rich
    console = Console()
    title = f"🏏 {card['name']}  ({card.get('team') or '-'})  [{card['source']}]"
    console.print()
    console.print(Panel(title, border_style="cyan", box=box.DOUBLE_EDGE))

    bat = card["batting"]
    bat_table = Table(title="BATTING", box=box.ROUNDED, header_style="bold magenta")
    bat_table.add_column("Stat", style="cyan")
    bat_table.add_column("Value", justify="right", style="yellow")
    bat_table.add_row("Matches", _fmt(bat.get('matches')))
    bat_table.add_row("Innings", _fmt(bat.get('innings', bat.get('matches'))))
    bat_table.add_row("Runs", _fmt(bat['runs']))
    bat_table.add_row("Balls Faced", _fmt(bat['balls_faced']))
    bat_table.add_row("Strike Rate", _fmt(bat['strike_rate']))
    bat_table.add_row("Average", _fmt(bat['average']))
    bat_table.add_row("4s / 6s", f"{bat['fours']} / {bat['sixes']}")
    bat_table.add_row("Highest Score", str(bat['highest_score']))
    bat_table.add_row("Outs / Not Outs", f"{bat['outs']} / {bat['not_outs']}")
    console.print(bat_table)

    bowl = card["bowling"]
    bowl_table = Table(title="BOWLING", box=box.ROUNDED, header_style="bold magenta")
    bowl_table.add_column("Stat", style="cyan")
    bowl_table.add_column("Value", justify="right", style="yellow")
    bowl_table.add_row("Overs", bowl["overs"])
    bowl_table.add_row("Wickets", str(bowl["wickets"]))
    bowl_table.add_row("Runs Conceded", _fmt(bowl["runs_conceded"]))
    bowl_table.add_row("Economy", _fmt(bowl["economy"]))
    bowl_table.add_row("Average", _fmt(bowl["average"]))
    bb = bowl["best_bowling"]
    bb_str = f"{bb['wickets']}/{bb['runs']}" if bb["runs"] is not None else "-"
    bowl_table.add_row("Best Bowling", bb_str)
    console.print(bowl_table)
    console.print()


def print_seasons_list():
    seasons = list_seasons()
    if not seasons:
        print("\nNo archived seasons yet.\n")
        return
    rich = _try_rich()
    if rich:
        Console, Table, Panel, box = rich
        console = Console()
        table = Table(title="📚 ARCHIVED SEASONS", box=box.HEAVY_HEAD)
        table.add_column("ID", justify="right", style="yellow")
        table.add_column("Name", style="cyan")
        table.add_column("Archived At", style="white")
        table.add_column("Champion", style="green")
        table.add_column("Matches", justify="right")
        table.add_column("Teams", justify="right")
        for s in seasons:
            table.add_row(
                str(s["season_id"]),
                s["name"],
                s["archived_at"],
                s["champion"] or "-",
                str(s["num_matches"]),
                str(s["num_teams"]),
            )
        console.print()
        console.print(table)
        console.print()
    else:
        print("\n=== ARCHIVED SEASONS ===")
        for s in seasons:
            print(f"  {s['season_id']:>3}  {s['name']:15}  {s['archived_at']}  champion={s['champion']}  matches={s['num_matches']}")


def print_historical_points_table_all_time():
    table = get_historical_points_table_all_time()
    if not table:
        print("\nNo archived seasons yet.\n")
        return
    rich = _try_rich()
    if rich:
        Console, Table, Panel, box = rich
        console = Console()
        t = Table(title="🏆 ALL-TIME POINTS TABLE (across archived seasons)",
                  box=box.HEAVY_HEAD, style="bold white on blue")
        t.add_column("#", justify="center", style="yellow")
        t.add_column("Team", style="bold cyan")
        t.add_column("S", justify="right", style="white")
        t.add_column("P", justify="right", style="white")
        t.add_column("W", justify="right", style="green")
        t.add_column("L", justify="right", style="red")
        t.add_column("T", justify="right", style="yellow")
        t.add_column("Pts", justify="right", style="bold white")
        t.add_column("NRR", justify="right", style="cyan")
        for idx, r in enumerate(table, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx:2d}."
            t.add_row(medal, r["team"], str(r["seasons_played"]),
                       str(r["played"]), str(r["won"]), str(r["lost"]),
                       str(r["tied"]), str(r["points"]),
                       f"{r['nrr']:>7.3f}")
        console.print()
        console.print(t)
        console.print()
    else:
        print("\n=== ALL-TIME POINTS TABLE ===")
        print(f"{'Team':8} {'S':>3} {'P':>3} {'W':>3} {'L':>3} {'T':>3} {'Pts':>4} {'NRR':>7}")
        for r in table:
            print(f"{r['team']:8} {r['seasons_played']:>3} {r['played']:>3} "
                  f"{r['won']:>3} {r['lost']:>3} {r['tied']:>3} "
                  f"{r['points']:>4} {r['nrr']:>7.3f}")


def print_historical_points_table_season(season_id):
    table = get_historical_points_table_season(season_id)
    if not table:
        print(f"\nNo data for season_id={season_id}.\n")
        return
    rich = _try_rich()
    if rich:
        Console, Table, Panel, box = rich
        console = Console()
        t = Table(title=f"🏆 SEASON {season_id} FINAL POINTS TABLE",
                  box=box.HEAVY_HEAD, style="bold white on blue")
        t.add_column("Pos", justify="center", style="yellow")
        t.add_column("Team", style="bold cyan")
        t.add_column("P", justify="right", style="white")
        t.add_column("W", justify="right", style="green")
        t.add_column("L", justify="right", style="red")
        t.add_column("T", justify="right", style="yellow")
        t.add_column("Pts", justify="right", style="bold white")
        t.add_column("NRR", justify="right", style="cyan")
        for r in table:
            t.add_row(str(r["position"]), r["team"],
                       str(r["played"]), str(r["won"]), str(r["lost"]),
                       str(r["tied"]), str(r["points"]),
                       f"{r['nrr']:>7.3f}")
        console.print()
        console.print(t)
        console.print()
    else:
        print(f"\n=== SEASON {season_id} POINTS TABLE ===")
        for r in table:
            print(f"  {r['position']:>2}  {r['team']:8}  P={r['played']:>2} "
                  f"W={r['won']:>2} L={r['lost']:>2} T={r['tied']:>2} "
                  f"Pts={r['points']:>3} NRR={r['nrr']:>7.3f}")
