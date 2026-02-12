"""
top_players.py

Compute top 10 players for various categories using the simulator database.

Categories:
- Most runs
- Most wickets
- Highest Score
- Most fours
- Most sixes
- Highest Strike Rate
- Best Bowling (by best_bowling field: wickets desc, runs asc)
- Best Economy (aggregated from match files' bowling stats)

The script prefers `database/match_stats_player_stats.json` (user-provided name),
then falls back to `database/player_stats.json`. For economy it aggregates
bowling `runs` and `balls` from files under `database/match_stats/`.

Usage:
    python top_players.py --print
    python top_players.py --output database/top_players_summary.json

"""
import os
import json
import argparse
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

DEFAULT_SOURCES = [
    os.path.join("database", "match_stats_player_stats.json"),
    os.path.join("database", "player_stats.json"),
]
MATCH_DIR = os.path.join("database", "match_stats")


def load_json_if_exists(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def aggregate_bowling_from_matches(match_dir):
    """Aggregate bowling runs and balls per bowler from match JSON files.
    Returns dict: name -> {"runs_conceded": int, "balls_bowled": int}
    """
    agg = defaultdict(lambda: {"runs_conceded": 0, "balls_bowled": 0})
    if not os.path.isdir(match_dir):
        return agg

    for fn in os.listdir(match_dir):
        path = os.path.join(match_dir, fn)
        if not fn.lower().endswith(".json"):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        # Each match file has keys: 'meta' and team names mapping to {"batting": [...], "bowling": {...}}
        for key, val in data.items():
            if key == "meta":
                continue
            team_section = val
            bowling = team_section.get("bowling") or {}
            # bowling is expected to be dict bowler_name -> {"overs":..., "balls":..., "runs":..., "wickets":...}
            for bowler, st in bowling.items():
                runs = st.get("runs", 0)
                balls = st.get("balls", 0)
                agg[bowler]["runs_conceded"] += runs
                agg[bowler]["balls_bowled"] += balls
    return agg


def top_n_by_numeric(mapping, key_fn, n=10, reverse=True):
    items = []
    for name, entry in mapping.items():
        try:
            val = key_fn(entry)
        except Exception:
            val = None
        items.append((name, entry, val))
    # Filter out None values
    items = [t for t in items if t[2] is not None]
    items_sorted = sorted(items, key=lambda t: t[2], reverse=reverse)
    return items_sorted[:n]


def compute_categories(players, match_bowling_agg):
    results = {}

    # Most runs (Orange Cap)
    results["most_runs"] = [
        {"name": name, "runs": entry.get("runs", 0), "matches": entry.get("matches", 0)}
        for name, entry, _ in top_n_by_numeric(players, lambda e: e.get("runs", 0), 10, True)
    ]

    # Most wickets (Purple Cap)
    results["most_wickets"] = [
        {"name": name, "wickets": entry.get("wickets", 0), "matches": entry.get("matches", 0)}
        for name, entry, _ in top_n_by_numeric(players, lambda e: e.get("wickets", 0), 10, True)
    ]

    # Least wickets - exclude those with 0 wickets
    def least_wickets_key(e):
        w = e.get("wickets", 0)
        if w == 0:
            return None
        return w
    results["least_wickets"] = [
        {"name": name, "wickets": entry.get("wickets", 0), "matches": entry.get("matches", 0)}
        for name, entry, _ in top_n_by_numeric(players, least_wickets_key, 10, False)
    ]

    # Highest score
    results["highest_score"] = [
        {"name": name, "highest_score": entry.get("highest_score", 0), "balls": entry.get("balls_in_highest_score", 0)}
        for name, entry, _ in top_n_by_numeric(players, lambda e: e.get("highest_score", 0), 10, True)
    ]

    # Most fours
    results["most_fours"] = [
        {"name": name, "fours": entry.get("fours", 0)}
        for name, entry, _ in top_n_by_numeric(players, lambda e: e.get("fours", 0), 10, True)
    ]

    # Most sixes
    results["most_sixes"] = [
        {"name": name, "sixes": entry.get("sixes", 0)}
        for name, entry, _ in top_n_by_numeric(players, lambda e: e.get("sixes", 0), 10, True)
    ]

    # Highest Strike Rate (runs/balls_faced * 100) - require runs >= 250
    def sr(e):
        runs = e.get("runs", 0)
        balls = e.get("balls_faced", 0)
        if runs < 100 or balls <= 0:
            return None
        return (runs / balls) * 100

    results["highest_strike_rate"] = [
        {"name": name, "strike_rate": round(val, 2), "runs": entry.get("runs", 0), "balls_faced": entry.get("balls_faced", 0)}
        for name, entry, val in top_n_by_numeric(players, sr, 10, True)
    ]

    # Lowest Strike Rate - require runs >= 250
    results["lowest_strike_rate"] = [
        {"name": name, "strike_rate": round(val, 2), "runs": entry.get("runs", 0), "balls_faced": entry.get("balls_faced", 0)}
        for name, entry, val in top_n_by_numeric(players, sr, 10, False)
    ]

    # Best Bowling (from best_bowling field)
    def best_bowling_key(e):
        bb = e.get("best_bowling") or {}
        w = bb.get("wickets", 0)
        r = bb.get("runs", 9999)
        # sort by wickets desc, runs asc -> numeric key: (w, -r) but top_n_by_numeric only supports numeric
        # We'll return a tuple-like but we can map to a composite number: w*100000 - r
        return w * 100000 - r

    top_bb = top_n_by_numeric(players, best_bowling_key, 10, True)
    results["best_bowling"] = []
    for name, entry, val in top_bb:
        bb = entry.get("best_bowling") or {"wickets": 0, "runs": None}
        results["best_bowling"].append({"name": name, "wickets": bb.get("wickets", 0), "runs": bb.get("runs")})

    # Best Economy - compute from match_aggregated bowling stats (runs_conceded, balls_bowled)
    econ_list = []
    for bowler, stats in match_bowling_agg.items():
        balls = stats.get("balls_bowled", 0)
        runs = stats.get("runs_conceded", 0)
        if balls <= 0:
            continue
        overs = balls / 6.0
        econ = runs / overs if overs > 0 else None
        if econ is None:
            continue
        econ_list.append((bowler, {"runs_conceded": runs, "balls_bowled": balls, "economy": round(econ, 3)}, econ))

    # sort by economy ascending (lower is better)
    econ_list_sorted = sorted(econ_list, key=lambda t: t[2])[:10]
    results["best_economy"] = [
        {"name": name, "economy": info["economy"], "runs_conceded": info["runs_conceded"], "balls_bowled": info["balls_bowled"]}
        for name, info, _ in econ_list_sorted
    ]

    # Worst Economy - highest economy rate
    econ_list_worst = sorted(econ_list, key=lambda t: t[2], reverse=True)[:10]
    results["worst_economy"] = [
        {"name": name, "economy": info["economy"], "runs_conceded": info["runs_conceded"], "balls_bowled": info["balls_bowled"]}
        for name, info, _ in econ_list_worst
    ]

    # Best Bowling Average (Season-long) - aggregate from matches
    bowling_season_list = []
    for bowler, stats in match_bowling_agg.items():
        total_runs = stats.get("runs_conceded", 0)
        if bowler in players:
            player_wickets = players[bowler].get("wickets", 0)
            if player_wickets > 0:
                avg = total_runs / player_wickets
                bowling_season_list.append((bowler, {"wickets": player_wickets, "runs": total_runs, "bowling_average": round(avg, 2)}, avg))
    
    # Sort by bowling average ascending (lower is better)
    bowling_avg_sorted = sorted(bowling_season_list, key=lambda t: t[2])[:10]
    results["best_bowling_average"] = [
        {"name": name, "bowling_average": info["bowling_average"], "wickets": info["wickets"], "runs": info["runs"]}
        for name, info, _ in bowling_avg_sorted
    ]

    # Worst Bowling Average (Season-long) - highest average
    bowling_avg_worst = sorted(bowling_season_list, key=lambda t: t[2], reverse=True)[:10]
    results["worst_bowling_average"] = [
        {"name": name, "bowling_average": info["bowling_average"], "wickets": info["wickets"], "runs": info["runs"]}
        for name, info, _ in bowling_avg_worst
    ]

    # Best Batting Average (min 300 runs) - runs / dismissals (outs)
    batting_avg_list = []
    for player, stats in players.items():
        runs = stats.get("runs", 0)
        if runs < 200:  # Skip if less than 200 runs
            continue
        outs = stats.get("outs", 0)
        not_outs = stats.get("not_outs", 0)
        matches = stats.get("matches", 0)
        
        # Batting average = runs / dismissals (only count players with at least 1 dismissal)
        if outs > 0:
            avg = runs / outs
            batting_avg_list.append((player, {"batting_average": round(avg, 2), "runs": runs, "outs": outs, "not_outs": not_outs}, avg))
    
    # Sort by batting average descending (higher is better)
    batting_avg_sorted = sorted(batting_avg_list, key=lambda t: t[2], reverse=True)[:10]
    results["best_batting_average"] = [
        {"name": name, "batting_average": info["batting_average"], "runs": info["runs"], "outs": info["outs"], "not_outs": info["not_outs"]}
        for name, info, _ in batting_avg_sorted
    ]

    # Worst Batting Average (min 300 runs) - lowest average
    batting_avg_worst = sorted(batting_avg_list, key=lambda t: t[2])[:10]
    results["worst_batting_average"] = [
        {"name": name, "batting_average": info["batting_average"], "runs": info["runs"], "outs": info["outs"], "not_outs": info["not_outs"]}
        for name, info, _ in batting_avg_worst
    ]

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="Player stats JSON file (preferred)", default=None)
    parser.add_argument("--match-dir", help="Match stats directory to aggregate bowling (default database/match_stats)", default=MATCH_DIR)
    parser.add_argument("--output", help="Output JSON path (optional)", default=None)
    parser.add_argument("--print", dest="print_out", action="store_true", help="Print results to console")
    args = parser.parse_args()

    # Determine source
    players = None
    if args.source:
        players = load_json_if_exists(args.source)
        if players is None:
            print(f"Source file {args.source} not found or invalid.")
    else:
        for p in DEFAULT_SOURCES:
            players = load_json_if_exists(p)
            if players is not None:
                break

    if players is None:
        print("No player stats JSON found. Exiting.")
        return 1

    match_bowling_agg = aggregate_bowling_from_matches(args.match_dir)

    results = compute_categories(players, match_bowling_agg)

    # Display results using Rich library
    console = Console()
    
    for cat, items in results.items():
        # Create a table for each category
        title = cat.upper().replace('_', ' ')
        
        # Determine table columns based on category
        if cat == "most_runs":
            table = Table(title=f"🟠 {title} (ORANGE CAP)", show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Runs", style="yellow", justify="right")
            table.add_column("Matches", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), str(it.get('runs', 0)), str(it.get('matches', 0)))
                
        elif cat == "most_wickets":
            table = Table(title=f"🟣 {title} (PURPLE CAP)", show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Wickets", style="red", justify="right")
            table.add_column("Matches", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), str(it.get('wickets', 0)), str(it.get('matches', 0)))
                
        elif cat == "least_wickets":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Wickets", justify="right")
            table.add_column("Matches", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), str(it.get('wickets', 0)), str(it.get('matches', 0)))
                
        elif cat == "highest_score":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Score", style="yellow", justify="right")
            table.add_column("Balls", justify="right")
            table.add_column("SR", justify="right")
            
            for i, it in enumerate(items, 1):
                score = it.get('highest_score', 0)
                balls = it.get('balls', 0)
                sr = f"{(score / balls) * 100:.2f}" if balls > 0 else "0.00"
                table.add_row(str(i), it.get("name", "Unknown"), str(score), str(balls), sr)
                
        elif cat == "most_fours":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Fours", style="blue", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), str(it.get('fours', 0)))
                
        elif cat == "most_sixes":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Sixes", style="red", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), str(it.get('sixes', 0)))
                
        elif cat == "highest_strike_rate":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("SR", style="yellow", justify="right")
            table.add_column("Runs", justify="right")
            table.add_column("Balls", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), f"{it.get('strike_rate', 0):.2f}", 
                             str(it.get('runs', 0)), str(it.get('balls_faced', 0)))
                
        elif cat == "lowest_strike_rate":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("SR", justify="right")
            table.add_column("Runs", justify="right")
            table.add_column("Balls", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), f"{it.get('strike_rate', 0):.2f}", 
                             str(it.get('runs', 0)), str(it.get('balls_faced', 0)))
                
        elif cat == "best_bowling":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Figures", style="red", justify="right")
            
            for i, it in enumerate(items, 1):
                wickets = it.get('wickets', 0)
                runs = it.get('runs', 'N/A')
                table.add_row(str(i), it.get("name", "Unknown"), f"{wickets}W/{runs}R")
                
        elif cat == "best_economy":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Economy", style="green", justify="right")
            table.add_column("Runs", justify="right")
            table.add_column("Balls", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), f"{it.get('economy', 0):.3f}", 
                             str(it.get('runs_conceded', 0)), str(it.get('balls_bowled', 0)))
                
        elif cat == "worst_economy":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Economy", style="red", justify="right")
            table.add_column("Runs", justify="right")
            table.add_column("Balls", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), f"{it.get('economy', 0):.3f}", 
                             str(it.get('runs_conceded', 0)), str(it.get('balls_bowled', 0)))
                
        elif cat == "best_bowling_average":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Average", style="green", justify="right")
            table.add_column("Wickets", justify="right")
            table.add_column("Runs", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), f"{it.get('bowling_average', 0):.2f}", 
                             str(it.get('wickets', 0)), str(it.get('runs', 0)))
                
        elif cat == "worst_bowling_average":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Average", style="red", justify="right")
            table.add_column("Wickets", justify="right")
            table.add_column("Runs", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), f"{it.get('bowling_average', 0):.2f}", 
                             str(it.get('wickets', 0)), str(it.get('runs', 0)))
                
        elif cat == "best_batting_average":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Average", style="yellow", justify="right")
            table.add_column("Runs", justify="right")
            table.add_column("Outs", justify="right")
            table.add_column("Not Outs", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), f"{it.get('batting_average', 0):.2f}", 
                             str(it.get('runs', 0)), str(it.get('outs', 0)), str(it.get('not_outs', 0)))
                
        elif cat == "worst_batting_average":
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="cyan", width=6)
            table.add_column("Player", style="green", width=30)
            table.add_column("Average", justify="right")
            table.add_column("Runs", justify="right")
            table.add_column("Outs", justify="right")
            table.add_column("Not Outs", justify="right")
            
            for i, it in enumerate(items, 1):
                table.add_row(str(i), it.get("name", "Unknown"), f"{it.get('batting_average', 0):.2f}", 
                             str(it.get('runs', 0)), str(it.get('outs', 0)), str(it.get('not_outs', 0)))
        else:
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Data", style="white")
            for i, it in enumerate(items, 1):
                table.add_row(str(it))
        
        if not items:
            console.print(Panel(f"[yellow]No data available for {title}[/yellow]"))
        else:
            console.print(table)
        console.print()  # Add spacing between tables

    if args.output:
        outp = args.output
    else:
        outp = os.path.join("database", "top_players_summary.json")

    try:
        with open(outp, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        console.print(f"\n[green]✅ Results written to: {outp}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to write output file: {e}[/red]")

    return 0


if __name__ == "__main__":
    main()
