# database.py
import json
import os
from datetime import datetime

DB_DIR = "database"
MATCH_DIR = os.path.join(DB_DIR, "match_stats")
PLAYER_FILE = os.path.join(DB_DIR, "player_stats.json")
TEAM_FILE = os.path.join(DB_DIR, "team_stats.json")
CUMULATIVE_FILE = os.path.join(DB_DIR, "cumulative_stats.json")


def ensure_dirs():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    if not os.path.exists(MATCH_DIR):
        os.makedirs(MATCH_DIR)


def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return default
    return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_players():
    ensure_dirs()
    return load_json(PLAYER_FILE, {})


def save_players(players):
    ensure_dirs()
    save_json(PLAYER_FILE, players)


def load_teams():
    ensure_dirs()
    return load_json(TEAM_FILE, {})


def save_teams(teams):
    ensure_dirs()
    save_json(TEAM_FILE, teams)



def save_match_file(teamA_name, teamB_name, A_bat, A_bowl, B_bat, B_bowl, teamA_objs=None, teamB_objs=None, result=None, A_score=None, B_score=None):
    """Save match JSON including batsmen names and optional result.

    teamA_objs / teamB_objs: lists of player objects (optional). If provided,
    each batting entry will include a `name` field.
    result: optional dict describing match result (winner, margin, etc.).
    """
    ensure_dirs()
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{teamA_name}_vs_{teamB_name}_{ts}.json"
    path = os.path.join(MATCH_DIR, filename)

    def attach_names(bat_list, objs):
        if not isinstance(bat_list, list):
            return bat_list
        out = []
        for i, st in enumerate(bat_list):
            entry = dict(st) if isinstance(st, dict) else {"value": st}
            if objs and i < len(objs):
                try:
                    entry["name"] = objs[i].name
                except Exception:
                    entry["name"] = None
            out.append(entry)
        return out

    A_bat_named = attach_names(A_bat, teamA_objs)
    B_bat_named = attach_names(B_bat, teamB_objs)
    
    # Filter bowling stats to only include bowlers who actually bowled
    A_bowl_filtered = {name: stats for name, stats in A_bowl.items() if stats.get("balls", 0) > 0}
    B_bowl_filtered = {name: stats for name, stats in B_bowl.items() if stats.get("balls", 0) > 0}

    data = {
        "meta": {
            "teamA": teamA_name,
            "teamB": teamB_name,
            "timestamp_utc": ts,
        },
        teamA_name: {"batting": A_bat_named, "bowling": A_bowl_filtered},
        teamB_name: {"batting": B_bat_named, "bowling": B_bowl_filtered},
    }

    if isinstance(result, dict):
        data["result"] = result
    else:
        # if scores provided but no result dict, synthesize basic result
        if A_score is not None and B_score is not None:
            if A_score > B_score:
                margin = f"{A_score - B_score} runs"
                winner = teamA_name
            elif B_score > A_score:
                # unknown wickets info here; provide runs-based fallback
                margin = f"{B_score - A_score} runs"
                winner = teamB_name
            else:
                winner = "TIE"
                margin = ""
            data["result"] = {"winner": winner, "by": margin, "A_score": A_score, "B_score": B_score}

    save_json(path, data)
    return path

def update_players_from_match(team_name, batting_team, batting_stats, bowling_stats):
    players = load_players()

    # Batting updates
    for i, player in enumerate(batting_team):
        name = player.name
        st = batting_stats[i]
        if name not in players:
            players[name] = {
                "team": team_name,
                "runs": 0,
                "balls_faced": 0,
                "fours": 0,
                "sixes": 0,
                "matches": 0,
                "outs": 0,
                "not_outs": 0,
                "highest_score": 0,
                "wickets": 0,
                "balls_bowled": 0,
                "best_bowling": {"wickets": 0, "runs": 999},
            }
        p = players[name]
        runs = st.get("runs", 0)
        balls = st.get("balls", 0)
        fours = st.get("4s", 0)
        sixes = st.get("6s", 0)
        dismissal = st.get("dismissal", "not out").strip().lower()

        p["runs"] += runs
        p["balls_faced"] += balls
        p["fours"] += fours
        p["sixes"] += sixes
        p["matches"] += 1
        
        # Track out/not out
        if dismissal == "not out":
            p["not_outs"] += 1
        else:
            p["outs"] += 1
        
        if runs > p["highest_score"]:
            p["highest_score"] = runs

    # Bowling updates
    for bowler_name, st in bowling_stats.items():
        if bowler_name not in players:
            players[bowler_name] = {
                "team": team_name,
                "runs": 0,
                "balls_faced": 0,
                "fours": 0,
                "sixes": 0,
                "matches": 0,
                "outs": 0,
                "not_outs": 0,
                "highest_score": 0,
                "wickets": 0,
                "balls_bowled": 0,
                "best_bowling": {"wickets": 0, "runs": 999},
            }

        p = players[bowler_name]
        w = st.get("wickets", 0)
        balls_bowled = st.get("balls", 0)
        runs_conceded = st.get("runs", 0)

        p["wickets"] += w
        p["balls_bowled"] += balls_bowled
        bb = p["best_bowling"]
        if w > bb.get("wickets", 0) or (w == bb.get("wickets", 0) and runs_conceded < bb.get("runs", 999)):
            p["best_bowling"] = {"wickets": w, "runs": runs_conceded}

    save_players(players)

def update_team_from_match(teamA_name, teamB_name, A_score, B_score, A_overs_batted_balls, B_overs_batted_balls, winner):
    teams = load_teams()

    def ensure(team):
        if team not in teams:
            teams[team] = {
                "played": 0,
                "won": 0,
                "lost": 0,
                "tied": 0,
                "points": 0,
                "runs_scored": 0,
                "runs_conceded": 0,
                "balls_faced": 0,
                "balls_bowled": 0,
            }

    ensure(teamA_name)
    ensure(teamB_name)

    tA = teams[teamA_name]
    tB = teams[teamB_name]

    tA["played"] += 1
    tB["played"] += 1

    tA["runs_scored"] += A_score
    tA["runs_conceded"] += B_score
    tA["balls_faced"] += A_overs_batted_balls
    tA["balls_bowled"] += B_overs_batted_balls

    tB["runs_scored"] += B_score
    tB["runs_conceded"] += A_score
    tB["balls_faced"] += B_overs_batted_balls
    tB["balls_bowled"] += A_overs_batted_balls

    if winner == teamA_name:
        tA["won"] += 1
        tA["points"] += 2
        tB["lost"] += 1
    elif winner == teamB_name:
        tB["won"] += 1
        tB["points"] += 2
        tA["lost"] += 1
    else:  # tie
        tA["tied"] += 1
        tB["tied"] += 1
        tA["points"] += 1
        tB["points"] += 1

    save_teams(teams)


def get_orange_purple(top_n=10):
    players = load_players()
    runs_sorted = sorted(players.items(), key=lambda x: x[1].get("runs", 0), reverse=True)
    wkts_sorted = sorted(players.items(), key=lambda x: x[1].get("wickets", 0), reverse=True)
    return runs_sorted[:top_n], wkts_sorted[:top_n]


def compute_nrr_for_team_entry(entry):
    bf = entry.get("balls_faced", 0)
    bb = entry.get("balls_bowled", 0)
    if bf == 0 or bb == 0:
        return 0.0
    rs = entry.get("runs_scored", 0) / (bf / 6.0)
    rc = entry.get("runs_conceded", 0) / (bb / 6.0)
    return round(rs - rc, 3)


def compute_nrr(runs_scored, runs_conceded, balls_faced, balls_bowled):
    """
    Compute NRR from raw stats.
    
    Args:
        runs_scored: Total runs scored
        runs_conceded: Total runs conceded
        balls_faced: Total balls faced while batting
        balls_bowled: Total balls bowled while bowling
    
    Returns:
        Net Run Rate as float
    """
    if balls_faced == 0 or balls_bowled == 0:
        return 0.0
    rs = runs_scored / (balls_faced / 6.0)
    rc = runs_conceded / (balls_bowled / 6.0)
    return round(rs - rc, 3)


def get_team_stats(team_name):
    """
    Get current statistics for a team from database.
    
    Returns dict with runs_scored, runs_conceded, balls_faced, balls_bowled
    or a zero-initialized dict if team not found.
    """
    teams = load_teams()
    if team_name in teams:
        entry = teams[team_name]
        return {
            "runs_scored": entry.get("runs_scored", 0),
            "runs_conceded": entry.get("runs_conceded", 0),
            "balls_faced": entry.get("balls_faced", 0),
            "balls_bowled": entry.get("balls_bowled", 0),
        }
    return {
        "runs_scored": 0,
        "runs_conceded": 0,
        "balls_faced": 0,
        "balls_bowled": 0,
    }


def get_points_table_sorted():
    teams = load_teams()
    table = []
    for team, entry in teams.items():
        nrr = compute_nrr_for_team_entry(entry)
        row = {
            "team": team,
            "played": entry.get("played", 0),
            "won": entry.get("won", 0),
            "lost": entry.get("lost", 0),
            "tied": entry.get("tied", 0),
            "points": entry.get("points", 0),
            "nrr": nrr,
            "runs_scored": entry.get("runs_scored", 0),
            "runs_conceded": entry.get("runs_conceded", 0),
        }
        table.append(row)

    table_sorted = sorted(table, key=lambda r: (r["points"], r["nrr"]), reverse=True)
    return table_sorted


def clear_database():
    import shutil
    import time
    
    if not os.path.exists(DB_DIR):
        ensure_dirs()
        return
    
    try:
        # Try standard removal first
        shutil.rmtree(DB_DIR)
    except PermissionError:
        # If permission error, try manual removal approach
        try:
            def handle_remove_error(func, path, exc):
                """Handle removal errors, especially on Windows."""
                import stat
                if not os.access(path, os.W_OK):
                    os.chmod(path, stat.S_IWUSR | stat.S_IREAD)
                    func(path)
                else:
                    raise
            
            shutil.rmtree(DB_DIR, onerror=handle_remove_error)
        except Exception as e:
            # Last resort: remove files manually
            try:
                for root, dirs, files in os.walk(DB_DIR, topdown=False):
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        try:
                            os.remove(filepath)
                        except Exception:
                            pass
                    for dirname in dirs:
                        dirpath = os.path.join(root, dirname)
                        try:
                            os.rmdir(dirpath)
                        except Exception:
                            pass
                # Try to remove main directory
                try:
                    os.rmdir(DB_DIR)
                except Exception:
                    pass
            except Exception as final_err:
                print(f"Warning: Could not fully clear database ({final_err}). Clearing files instead...")
    
    print("Database cleared.")
    ensure_dirs()


def print_caps_and_table():
    try:
        from rich.console import Console
        from rich.table import Table
        from rich import box
        console = Console()
    except:
        console = None
    
    runs_sorted, wkts_sorted = get_orange_purple(10)
    
    if console:
        # Orange Cap Table
        orange_table = Table(title="🧡 ORANGE CAP (Top Run Scorers)", box=box.DOUBLE, style="bold orange1")
        orange_table.add_column("#", justify="right", style="yellow")
        orange_table.add_column("Player", style="cyan")
        orange_table.add_column("Runs", justify="right", style="bold green")
        
        for idx, (name, data) in enumerate(runs_sorted, 1):
            runs = data.get('runs', 0)
            orange_table.add_row(str(idx), name, f"{runs}")
        
        console.print()
        console.print(orange_table)
        
        # Purple Cap Table
        purple_table = Table(title="💜 PURPLE CAP (Top Wicket Takers)", box=box.DOUBLE, style="bold magenta")
        purple_table.add_column("#", justify="right", style="yellow")
        purple_table.add_column("Player", style="cyan")
        purple_table.add_column("Wickets", justify="right", style="bold red")
        
        for idx, (name, data) in enumerate(wkts_sorted, 1):
            wkts = data.get('wickets', 0)
            purple_table.add_row(str(idx), name, f"{wkts}")
        
        console.print(purple_table)
        
        # Points Table
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
                f"{r['nrr']:>7.3f}"
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


def save_cumulative_stats(stats):
    ensure_dirs()
    save_json(CUMULATIVE_FILE, stats)

def load_cumulative_stats():
    ensure_dirs()
    return load_json(CUMULATIVE_FILE, {})

def print_season_points_table(season_points_dict, season_number):
    """Print season-specific points table"""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich import box
        console = Console()
    except:
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
                str(stats["points"])
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
    """Update cumulative stats after each season"""
    cumulative = load_cumulative_stats()
    current_teams = load_teams()
    
    for team, stats in current_teams.items():
        if team not in cumulative:
            cumulative[team] = {"played": 0, "won": 0, "lost": 0, "tied": 0, "points": 0}
        
        cumulative[team]["played"] += stats.get("played", 0)
        cumulative[team]["won"] += stats.get("won", 0)
        cumulative[team]["lost"] += stats.get("lost", 0)
        cumulative[team]["tied"] += stats.get("tied", 0)
        cumulative[team]["points"] += stats.get("points", 0)
    
    save_cumulative_stats(cumulative)

def print_full_points_table():
    """Print cumulative points table across all seasons"""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich import box
        console = Console()
    except:
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
                str(stats["points"])
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
