"""
league_simulator.py

Module to handle league simulation with different tournament formats.
"""

from teams import get_teams
from database import clear_database
import database
from fixtures import get_available_formats, get_format_function


def select_tournament_format():
    """
    Allow user to select a tournament format.
    
    Returns:
        format_id (str): The ID of selected format
    """
    formats = get_available_formats()
    
    print("\n" + "="*70)
    print("SELECT TOURNAMENT FORMAT")
    print("="*70)
    
    format_list = sorted(formats.items(), key=lambda x: x[0])
    
    for format_id, format_info in format_list:
        print(f"\nOption {format_id}: {format_info['name']}")
        print(f"  Description: {format_info['description']}")
    
    print("\n" + "-"*70)
    while True:
        choice = input("Select tournament format (enter option number): ").strip()
        if choice in formats:
            selected_format = formats[choice]
            print(f"\n✓ Selected: {selected_format['name']}")
            return choice
        else:
            print(f"Invalid choice! Please enter one of: {', '.join(sorted(formats.keys()))}")


def select_teams():
    """Allow user to select which teams participate in the league."""
    all_teams = list(get_teams().keys())
    
    print("\n=== Team Selection ===")
    print(f"Available teams ({len(all_teams)} total):")
    for idx, team in enumerate(all_teams, 1):
        print(f"{idx:2d}. {team}")
    
    print("\nEnter team numbers using:")
    print("  - Comma-separated: 1,2,3,4,5,6")
    print("  - Range notation: 4-8 (includes both 4 and 8)")
    print("  - Mixed: 1-3,5,7-9")
    print("  - Or 'all' for all teams")
    
    choice = input("Your choice (default: all): ").strip().lower()
    
    if not choice or choice == "all":
        return all_teams
    
    try:
        selections = []
        
        # Split by comma first
        parts = choice.split(",")
        
        for part in parts:
            part = part.strip()
            
            # Check if it's a range (contains hyphen)
            if "-" in part:
                range_parts = part.split("-")
                if len(range_parts) == 2:
                    start = int(range_parts[0].strip())
                    end = int(range_parts[1].strip())
                    
                    if start > end:
                        start, end = end, start
                    
                    # Add all numbers in range (inclusive)
                    for num in range(start, end + 1):
                        if 1 <= num <= len(all_teams):
                            selections.append(num)
                else:
                    print(f"ERROR: Invalid range format '{part}'")
                    return select_teams()
            else:
                # Single number
                num = int(part)
                if 1 <= num <= len(all_teams):
                    selections.append(num)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_selections = []
        for sel in selections:
            if sel not in seen:
                unique_selections.append(sel)
                seen.add(sel)
        
        selected_teams = [all_teams[sel - 1] for sel in unique_selections]
        
        if len(selected_teams) < 2:
            print("ERROR: Need at least 2 teams!")
            return select_teams()
        
        print(f"\nSelected {len(selected_teams)} teams: {', '.join(selected_teams)}")
        return selected_teams
    except ValueError:
        print("ERROR: Invalid input!")
        return select_teams()


def simulate_league(format_id=None, selected_teams=None):
    """
    Simulate a full league with the specified tournament format.
    
    Args:
        format_id (str, optional): Tournament format ID. If None, user will be prompted.
        selected_teams (list, optional): Teams to participate. If None, user will select.
    
    Returns:
        champion (str): Name of the champion team
    """
    # Get tournament format from user if not provided
    if format_id is None:
        format_id = select_tournament_format()
    
    # Select teams or use provided list
    if selected_teams is None:
        selected_teams = select_teams()
    
    # Ask user if they want ball-by-ball for league matches
    print("\n" + "="*60)
    print("Simulation Configuration")
    print("="*60)
    league_ball_by_ball_choice = input("Do you want ball-by-ball simulation for league matches? (y/n, default: n): ").strip().lower()
    league_ball_by_ball = (league_ball_by_ball_choice == "y")
    
    # Ask user if they want ball-by-ball for playoffs
    playoff_ball_by_ball_choice = input("Do you want ball-by-ball simulation for playoff matches? (y/n, default: n): ").strip().lower()
    playoff_ball_by_ball = (playoff_ball_by_ball_choice == "y")
    
    # Get the appropriate format function and run it
    format_function = get_format_function(format_id)
    champion = format_function(selected_teams, playoff_ball_by_ball, league_ball_by_ball)

    # Offer to archive into the historical database.
    _prompt_archive(champion)

    return champion


def _prompt_archive(champion):
    """Ask the user whether to archive the just-completed season into the
    historical database. Safe to skip; the user can also clear via menu 5
    without archiving if they don't want to keep this season.
    """
    print("\n" + "=" * 60)
    print("ARCHIVE THIS SEASON?")
    print("=" * 60)
    print("This will copy the current points table, all matches, and all")
    print("batting/bowling cards into the historical database as a new")
    print("season. The current data stays put (use menu option 5 to clear).")
    print()
    answer = input("Add this season to historical database? (y/n): ").strip().lower()
    if answer != "y":
        print("Skipped archiving.")
        return

    try:
        import historical
        season_id = historical.archive_current_season(champion=champion)
        if season_id is None:
            print("Nothing to archive (no current matches found).")
        else:
            print(f"\nArchived as season_id={season_id}. Champion: {champion or '-'}")
            # Auto-clear current season immediately on successful archive so
            # the user is ready to start a fresh league without going through
            # menu option 5 manually.
            database.clear_database(silent=True)
            print("Current season cleared.")
    except Exception as e:
        print(f"Archive failed: {e}")


if __name__ == "__main__":
    from match_simulator import choose_profile_default
    
    # Load default difficulty profile
    choose_profile_default()
    
    database.print_caps_and_table()
    clear_database()
    season_wins = {}
    
    # Simulate one season (change range to simulate multiple)
    for i in range(1):
        winner = simulate_league()
        print(f"Season {i+1} completed.")
        season_wins[winner] = season_wins.get(winner, 0) + 1
    
    print("\n" + "="*60)
    print("SEASON SUMMARY")
    print("="*60)
    print("Number of seasons won by each team:")
    for team, wins in sorted(season_wins.items(), key=lambda x: -x[1]):
        print(f"  {team}: {wins} season(s)")
    print("="*60)
