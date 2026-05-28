#!/usr/bin/env python3
"""
CricSim - Cricket League Simulator
Main entry point for the application.
"""

import sys
from match_simulator import choose_profile, choose_profile_default, simulate_match, configure_ball_by_ball_timers
from league_simulator import simulate_league, select_teams
from database import print_caps_and_table, clear_database, get_points_table_sorted
from teams import get_teams


def print_banner():
    """Print application banner."""
    print("\n" + "="*70)
    print("       🏏 CRICSIM - Cricket League Simulator 🏏")
    print("="*70)
    print()


def show_main_menu():
    """Display the main menu and get user choice."""
    print("\n=== MAIN MENU ===")
    print("1. Simulate a League (Choose Tournament Format)")
    print("2. Simulate a Single Match")
    print("3. View Stats (Current or Historical)")
    print("4. View Full Player Stats (Top Players, Current or Historical)")
    print("5. Clear Database & Start Fresh")
    print("6. Configure Game Difficulty")
    print("7. Configure Ball-by-Ball Timers")
    print("8. Lookup Player by Name")
    print("9. Exit")
    print()

    choice = input("Select an option (1-9): ").strip()
    return choice


def menu_simulate_league():
    """Simulate a full league."""
    print("\n" + "="*70)
    print("LEAGUE SIMULATION")
    print("="*70)
    
    try:
        simulate_league()
    except KeyboardInterrupt:
        print("\n\nLeague simulation cancelled.")
    except Exception as e:
        print(f"\nError during league simulation: {e}")


def menu_simulate_match():
    """Simulate a single match."""
    print("\n" + "="*70)
    print("SINGLE MATCH SIMULATION")
    print("="*70)
    
    all_teams = list(get_teams().keys())
    
    print(f"\nAvailable teams ({len(all_teams)} total):")
    for idx, team in enumerate(all_teams, 1):
        print(f"{idx:2d}. {team}")
    
    print()
    try:
        team1_idx = int(input("Select team 1 (enter number): ")) - 1
        if not (0 <= team1_idx < len(all_teams)):
            print("Invalid selection!")
            return
        
        team2_idx = int(input("Select team 2 (enter number): ")) - 1
        if not (0 <= team2_idx < len(all_teams)):
            print("Invalid selection!")
            return
        
        if team1_idx == team2_idx:
            print("Teams must be different!")
            return
        
        team1 = all_teams[team1_idx]
        team2 = all_teams[team2_idx]
        
        ball_by_ball = input("Show ball-by-ball (y/n, default: n): ").strip().lower() == "y"
        
        simulate_match(team1, team2, ball_by_ball=ball_by_ball)
    except ValueError:
        print("Invalid input!")
    except KeyboardInterrupt:
        print("\n\nMatch simulation cancelled.")
    except Exception as e:
        print(f"Error during match simulation: {e}")


def _prompt_current_or_historical():
    """Ask the user which data source they want to view.

    Returns one of: 'current', 'hist_all', 'hist_season', or None if cancelled.
    For 'hist_season', also returns the chosen season_id.
    """
    print()
    print("View which data?")
    print("  1. Current season (working state)")
    print("  2. Historical: all-time aggregate (across all archived seasons)")
    print("  3. Historical: a specific archived season")
    choice = input("Select (1-3): ").strip()
    if choice == "1":
        return ("current", None)
    if choice == "2":
        return ("hist_all", None)
    if choice == "3":
        import historical
        seasons = historical.list_seasons()
        if not seasons:
            print("\nNo archived seasons yet. Falling back to current season.")
            return ("current", None)
        historical.print_seasons_list()
        sid = input("Enter season_id: ").strip()
        try:
            sid = int(sid)
        except ValueError:
            print("Invalid season_id.")
            return None
        if not any(s["season_id"] == sid for s in seasons):
            print(f"season_id {sid} not found.")
            return None
        return ("hist_season", sid)
    print("Invalid choice.")
    return None


def menu_view_stats():
    """View statistics — current or historical (points table + orange/purple cap)."""
    print("\n" + "=" * 70)
    print("STATISTICS")
    print("=" * 70)
    selection = _prompt_current_or_historical()
    if selection is None:
        return
    mode, season_id = selection

    try:
        if mode == "current":
            print_caps_and_table()
        elif mode == "hist_all":
            import historical
            historical.print_historical_points_table_all_time()
            _print_historical_caps(historical, season_id=None)
        elif mode == "hist_season":
            import historical
            historical.print_historical_points_table_season(season_id)
            _print_historical_caps(historical, season_id=season_id)
    except Exception as e:
        print(f"Error displaying stats: {e}")


def _print_historical_caps(historical, season_id):
    """Render orange/purple cap from historical data (uses the existing
    rendering helpers in database.py for consistency)."""
    from rich.console import Console
    from rich.table import Table
    from rich import box

    runs_sorted, wkts_sorted = historical.get_historical_orange_purple(10, season_id=season_id)
    console = Console()
    label = "ALL-TIME" if season_id is None else f"SEASON {season_id}"

    orange_table = Table(title=f"🧡 ORANGE CAP ({label})", box=box.DOUBLE, style="bold orange1")
    orange_table.add_column("#", justify="right", style="yellow")
    orange_table.add_column("Player", style="cyan")
    orange_table.add_column("Runs", justify="right", style="bold green")
    for idx, (name, data) in enumerate(runs_sorted, 1):
        orange_table.add_row(str(idx), name, str(data.get("runs", 0)))
    console.print()
    console.print(orange_table)

    purple_table = Table(title=f"💜 PURPLE CAP ({label})", box=box.DOUBLE, style="bold magenta")
    purple_table.add_column("#", justify="right", style="yellow")
    purple_table.add_column("Player", style="cyan")
    purple_table.add_column("Wickets", justify="right", style="bold red")
    for idx, (name, data) in enumerate(wkts_sorted, 1):
        purple_table.add_row(str(idx), name, str(data.get("wickets", 0)))
    console.print(purple_table)
    console.print()


def menu_view_full_stats():
    """View full player statistics across 15 categories — current or historical."""
    print("\n" + "=" * 70)
    print("FULL PLAYER STATISTICS")
    print("=" * 70)
    selection = _prompt_current_or_historical()
    if selection is None:
        return
    mode, season_id = selection

    try:
        if mode == "current":
            from top_players import main as top_players_main
            sys.argv = [sys.argv[0], "--print"]
            top_players_main()
        else:
            import historical
            results = historical.get_historical_top_players(
                season_id=None if mode == "hist_all" else season_id
            )
            # Reuse the existing display path in top_players.py by injecting results.
            _render_top_players_results(results, season_id=season_id)
    except KeyboardInterrupt:
        print("\n\nFull stats display cancelled.")
    except Exception as e:
        print(f"Error displaying full stats: {e}")
        import traceback
        traceback.print_exc()


def _render_top_players_results(results, season_id):
    """Render the 15-category results dict using the same table layouts
    as top_players.main(). Lifted into main.py so that historical results
    can be displayed without re-running the SQL-based loader.
    """
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
    label = "ALL-TIME" if season_id is None else f"SEASON {season_id}"

    for cat, items in results.items():
        title = f"{cat.upper().replace('_', ' ')}  ({label})"
        if not items:
            console.print(Panel(f"[yellow]No data for {title}[/yellow]"))
            console.print()
            continue
        sample = items[0]
        # Build a generic table from the keys present in the first item.
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Rank", style="cyan", width=6)
        cols = [k for k in sample.keys() if k != "name"]
        table.add_column("Player", style="green", width=30)
        for c in cols:
            table.add_column(c.replace("_", " ").title(), justify="right")
        for i, it in enumerate(items, 1):
            row = [str(i), it.get("name", "Unknown")]
            for c in cols:
                v = it.get(c)
                row.append("-" if v is None else str(v))
            table.add_row(*row)
        console.print(table)
        console.print()


def menu_lookup_player():
    """Look up a single player's full batting + bowling card."""
    print("\n" + "=" * 70)
    print("PLAYER LOOKUP")
    print("=" * 70)
    name = input("\nPlayer name (exact, case-sensitive): ").strip()
    if not name:
        print("No name entered.")
        return

    selection = _prompt_current_or_historical()
    if selection is None:
        return
    mode, season_id = selection

    import historical
    if mode == "current":
        card = historical.get_player_card_current(name)
    elif mode == "hist_all":
        card = historical.get_player_card_historical(name, season_id=None)
    else:
        card = historical.get_player_card_historical(name, season_id=season_id)

    historical.print_player_card(card)


def menu_clear_database():
    """Clear database and start fresh."""
    print("\n" + "="*70)
    print("CLEAR DATABASE")
    print("="*70)
    print("\nThis will delete all statistics and match records!")
    
    confirm = input("Are you sure? (yes/no): ").strip().lower()
    if confirm == "yes":
        clear_database()
        print("Database cleared successfully!")
    else:
        print("Operation cancelled.")


def menu_configure():
    """Configure game difficulty."""
    print("\n" + "="*70)
    print("GAME CONFIGURATION")
    print("="*70)
    print("\nChoose your game difficulty profile:")
    
    choose_profile()


def menu_configure_timers():
    """Configure ball-by-ball timers."""
    configure_ball_by_ball_timers()


def main():
    """Main application loop."""
    print_banner()
    print("Welcome to CricSim!")
    print("Load default difficulty (Balanced)...")
    choose_profile_default()
    
    while True:
        try:
            choice = show_main_menu()
            
            if choice == "1":
                menu_simulate_league()
            elif choice == "2":
                menu_simulate_match()
            elif choice == "3":
                menu_view_stats()
            elif choice == "4":
                menu_view_full_stats()
            elif choice == "5":
                menu_clear_database()
            elif choice == "6":
                menu_configure()
            elif choice == "7":
                menu_configure_timers()
            elif choice == "8":
                menu_lookup_player()
            elif choice == "9":
                print("\nThanks for using CricSim! Goodbye!\n")
                sys.exit(0)
            else:
                print("Invalid choice! Please select 1-9.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            confirm = input("Exit? (yes/no): ").strip().lower()
            if confirm == "yes":
                print("\nThanks for using CricSim! Goodbye!\n")
                sys.exit(0)
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Returning to main menu...\n")


if __name__ == "__main__":
    main()
