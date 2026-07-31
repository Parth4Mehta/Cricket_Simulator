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
    print("5. Clear Database (Current Season or Historical)")
    print("6. Configure Game Settings")
    print("7. Lookup Player by Name")
    print("8. Exit")
    print()

    choice = input("Select an option (1-8): ").strip()
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
    """Clear database — branches into current-season vs historical."""
    print("\n" + "=" * 70)
    print("CLEAR DATABASE")
    print("=" * 70)
    print()
    print("What do you want to clear?")
    print("  1. Current season (working data: players, teams, matches)")
    print("  2. Historical database (archived seasons)")
    print("  3. Cancel")
    choice = input("Select (1-3): ").strip()

    if choice == "1":
        _clear_current_season()
    elif choice == "2":
        _clear_historical()
    else:
        print("Operation cancelled.")


def _clear_current_season():
    """Existing single yes/no confirm flow for the current season."""
    print("\nThis will delete the current season's statistics and match records.")
    confirm = input("Are you sure? (yes/no): ").strip().lower()
    if confirm == "yes":
        clear_database()
        print("Current season cleared successfully!")
    else:
        print("Operation cancelled.")


def _clear_historical():
    """Branch into 'all historical' vs 'a specific season', both with a
    strict 'type DELETE to confirm' prompt because this is irreversible."""
    import historical

    seasons = historical.list_seasons()
    if not seasons:
        print("\nNo archived seasons exist. Nothing to clear.")
        return

    print("\nWhat would you like to clear from the historical database?")
    print("  1. ALL historical seasons (wipes everything; season counter resets to 1)")
    print("  2. A specific archived season")
    print("  3. Cancel")
    sub = input("Select (1-3): ").strip()

    if sub == "1":
        _clear_all_historical(historical)
    elif sub == "2":
        _clear_one_historical_season(historical)
    else:
        print("Operation cancelled.")


def _clear_all_historical(historical):
    """Strict-confirm flow for nuking ALL archived seasons."""
    print("\n" + "!" * 70)
    print("WARNING: this will permanently delete ALL archived seasons,")
    print("all archived matches, all batting/bowling cards, and the")
    print("snapshotted final standings. This cannot be undone.")
    print("!" * 70)
    typed = input(
        "Type DELETE to confirm deletion of ALL historical seasons: "
    ).strip()
    if typed == "DELETE":
        historical.clear_all_historical()
        print("All historical data cleared. Next archived season will be 'Season 1'.")
    else:
        print("Confirmation text did not match. Operation cancelled.")


def _clear_one_historical_season(historical):
    """Strict-confirm flow for deleting a single archived season."""
    historical.print_seasons_list()
    sid_raw = input("Enter season_id to delete: ").strip()
    try:
        sid = int(sid_raw)
    except ValueError:
        print("Invalid season_id.")
        return

    seasons = historical.list_seasons()
    if not any(s["season_id"] == sid for s in seasons):
        print(f"season_id {sid} not found.")
        return

    typed = input(
        f"Type DELETE to confirm deletion of season {sid}: "
    ).strip()
    if typed != "DELETE":
        print("Confirmation text did not match. Operation cancelled.")
        return

    if historical.delete_season(sid):
        print(f"Season {sid} deleted.")
    else:
        print(f"Could not delete season {sid} (no rows affected).")


def menu_configure_settings():
    """Combined game-settings submenu (difficulty + ball-by-ball timers)."""
    print("\n" + "=" * 70)
    print("CONFIGURE GAME SETTINGS")
    print("=" * 70)
    print()
    print("Which setting do you want to configure?")
    print("  1. Game Difficulty")
    print("  2. Ball-by-Ball Timers")
    print("  3. Back to main menu")
    choice = input("Select (1-3): ").strip()

    if choice == "1":
        print("\nChoose your game difficulty profile:")
        choose_profile()
    elif choice == "2":
        configure_ball_by_ball_timers()
    elif choice == "3":
        return
    else:
        print("Invalid choice. Returning to main menu.")


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
                menu_configure_settings()
            elif choice == "7":
                menu_lookup_player()
            elif choice == "8":
                print("\nThanks for using CricSim! Goodbye!\n")
                sys.exit(0)
            else:
                print("Invalid choice! Please select 1-8.")
        
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
