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
    
    print("\nEnter team numbers (comma-separated) or 'all' for all teams:")
    print("Example: 1,2,3,4,5,6 or all")
    
    choice = input("Your choice (default: all): ").strip().lower()
    
    if not choice or choice == "all":
        return all_teams
    
    try:
        selections = [int(x.strip()) for x in choice.split(",")]
        selected_teams = []
        for sel in selections:
            if 1 <= sel <= len(all_teams):
                selected_teams.append(all_teams[sel - 1])
        
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
    
    # Ask user if they want ball-by-ball for playoffs
    print("\n" + "="*60)
    print("Playoff Configuration")
    print("="*60)
    playoff_ball_by_ball_choice = input("Do you want ball-by-ball simulation for playoff matches? (y/n, default: n): ").strip().lower()
    playoff_ball_by_ball = (playoff_ball_by_ball_choice == "y")
    
    # Get the appropriate format function and run it
    format_function = get_format_function(format_id)
    champion = format_function(selected_teams, playoff_ball_by_ball)
    
    return champion


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
