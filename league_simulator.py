# league_simulator.py

from match_simulator import simulate_match
from teams import get_teams
from database import clear_database
import database
import random


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


def create_double_round_robin_fixtures(teams):
    """Create double round-robin fixtures: each team plays every other team twice."""
    fixtures = []
    n = len(teams)
    
    # Each team plays every other team twice (home and away)
    for i in range(n):
        for j in range(n):
            if i != j:
                fixtures.append((teams[i], teams[j]))
    
    # Shuffle to randomize order
    random.shuffle(fixtures)
    return fixtures


def simulate_league(selected_teams=None):
    """Simulate a full league with double round-robin format."""
    # Select teams or use provided list
    if selected_teams is None:
        selected_teams = select_teams()
    
    # Initialize points table
    points_in_this_season = {t: 0 for t in selected_teams}
    
    # Create double round-robin fixtures
    fixtures = create_double_round_robin_fixtures(selected_teams)
    
    print(f"\n{'='*60}")
    print(f"League Format: Double Round-Robin ({len(selected_teams)} teams)")
    print(f"Total Matches: {len(fixtures)}")
    print(f"{'='*60}\n")

    for idx, (A, B) in enumerate(fixtures, 1):
        print(f"[Match {idx}/{len(fixtures)}] ", end="")
        winner = simulate_match(A, B, False)
        if winner != "TIE":
            points_in_this_season[winner] = points_in_this_season.get(winner, 0) + 2
        else:
            points_in_this_season[A] = points_in_this_season.get(A, 0) + 1
            points_in_this_season[B] = points_in_this_season.get(B, 0) + 1
    
    print("\n" + "="*60)
    print("LEAGUE STAGE COMPLETED")
    print("="*60)
    
    database.print_caps_and_table()
    
    # Simulate Playoffs - Top 4 teams
    print("\n" + "="*60)
    print("PLAYOFFS")
    print("="*60)
    
    # Sort by points (desc) and then by team name for deterministic ordering
    top_teams = sorted(points_in_this_season.items(), key=lambda x: (-x[1], x[0]))
    
    if len(selected_teams) >= 4:
        teams_for_playoffs = top_teams[:4]
    elif len(selected_teams) == 3:
        teams_for_playoffs = top_teams[:3]
    else:
        # Just 2 teams, go straight to final
        return simulate_match(selected_teams[0], selected_teams[1], True)
    
    playoff_teams = [t[0] for t in teams_for_playoffs]
    
    print(f"\nTop {len(playoff_teams)} teams qualified:")
    for idx, team in enumerate(playoff_teams, 1):
        points = points_in_this_season[team]
        print(f"{idx}. {team} ({points} points)")
    
    if len(playoff_teams) == 2:
        print("\n--- FINAL ---")
        input("Press Enter to simulate the final...")
        final_winner = simulate_match(playoff_teams[0], playoff_teams[1], True)
    elif len(playoff_teams) == 3:
        print("\n--- Eliminator ---")
        input("Press Enter to simulate eliminator (2nd vs 3rd)...")
        eliminator_winner = simulate_match(playoff_teams[1], playoff_teams[2], True)
        
        print("\n--- FINAL ---")
        input("Press Enter to simulate the final...")
        final_winner = simulate_match(playoff_teams[0], eliminator_winner, True)
    else:  # 4 teams
        print("\n--- Qualifier 1 (1st vs 2nd) ---")
        input("Press Enter to simulate Qualifier 1...")
        q1_winner = simulate_match(playoff_teams[0], playoff_teams[1], True)
        q1_loser = playoff_teams[1] if q1_winner == playoff_teams[0] else playoff_teams[0]
        
        print("\n--- Eliminator (3rd vs 4th) ---")
        input("Press Enter to simulate Eliminator...")
        eliminator_winner = simulate_match(playoff_teams[2], playoff_teams[3], True)
        
        print("\n--- Qualifier 2 (Loser Q1 vs Winner Eliminator) ---")
        input("Press Enter to simulate Qualifier 2...")
        q2_winner = simulate_match(q1_loser, eliminator_winner, True)
        
        print("\n--- FINAL ---")
        input("Press Enter to simulate the final...")
        final_winner = simulate_match(q1_winner, q2_winner, True)
    
    print(f"\n{'='*60}")
    print(f"🏆 LEAGUE CHAMPION: {final_winner} 🏆")
    print(f"{'='*60}\n")
    
    return final_winner


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
