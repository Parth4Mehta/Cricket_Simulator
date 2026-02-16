"""
Double Round-Robin + Playoffs fixture format.

Each team plays every other team twice (home and away),
followed by a 4-team playoff system.
"""

import random
from match_simulator import simulate_match
import database
from config_manager import reset_advanced_profile


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


def simulate_double_round_robin_playoff(selected_teams, playoff_ball_by_ball=False):
    """
    Simulate a league with double round-robin format + playoffs.
    
    Args:
        selected_teams: List of teams participating
        playoff_ball_by_ball: Whether to show ball-by-ball for playoff matches
    
    Returns:
        Champion team name
    """
    print(f"\n{'='*60}")
    print(f"League Format: Double Round-Robin ({len(selected_teams)} teams)")
    
    # Create double round-robin fixtures
    fixtures = create_double_round_robin_fixtures(selected_teams)
    
    print(f"Total Matches: {len(fixtures)}")
    print(f"{'='*60}\n")

    # Initialize points table
    points_in_this_season = {t: 0 for t in selected_teams}

    # Play league stage matches
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
    
    # Get standings sorted by points and NRR (already calculated in database)
    table = database.get_points_table_sorted()
    
    # Filter to only selected teams
    table_filtered = [row for row in table if row['team'] in selected_teams]
    
    if len(table_filtered) >= 4:
        teams_for_playoffs = table_filtered[:4]
    elif len(table_filtered) >= 2:
        teams_for_playoffs = table_filtered[:3] if len(table_filtered) == 3 else table_filtered
    else:
        # Just 2 teams, go straight to final
        return simulate_match(selected_teams[0], selected_teams[1], playoff_ball_by_ball)
    
    playoff_teams = [row['team'] for row in teams_for_playoffs]
    
    print(f"\nTop {len(playoff_teams)} teams qualified:")
    for idx, row in enumerate(teams_for_playoffs, 1):
        print(f"{idx}. {row['team']} ({row['points']} pts, NRR: {row['nrr']:+.2f})")
    
    if len(playoff_teams) == 2:
        print("\n--- FINAL ---")
        input("Press Enter to simulate the final...")
        final_winner = simulate_match(playoff_teams[0], playoff_teams[1], playoff_ball_by_ball)
    elif len(playoff_teams) == 3:
        print("\n--- Eliminator ---")
        input("Press Enter to simulate eliminator (2nd vs 3rd)...")
        eliminator_winner = simulate_match(playoff_teams[1], playoff_teams[2], playoff_ball_by_ball)
        
        print("\n--- FINAL ---")
        input("Press Enter to simulate the final...")
        final_winner = simulate_match(playoff_teams[0], eliminator_winner, playoff_ball_by_ball)
    else:  # 4 teams
        print("\n--- Qualifier 1 (1st vs 2nd) ---")
        input("Press Enter to simulate Qualifier 1...")
        q1_winner = simulate_match(playoff_teams[0], playoff_teams[1], playoff_ball_by_ball)
        q1_loser = playoff_teams[1] if q1_winner == playoff_teams[0] else playoff_teams[0]
        
        print("\n--- Eliminator (3rd vs 4th) ---")
        input("Press Enter to simulate Eliminator...")
        eliminator_winner = simulate_match(playoff_teams[2], playoff_teams[3], playoff_ball_by_ball)
        
        print("\n--- Qualifier 2 (Loser Q1 vs Winner Eliminator) ---")
        input("Press Enter to simulate Qualifier 2...")
        q2_winner = simulate_match(q1_loser, eliminator_winner, playoff_ball_by_ball)
        
        print("\n--- FINAL ---")
        input("Press Enter to simulate the final...")
        final_winner = simulate_match(q1_winner, q2_winner, playoff_ball_by_ball)
    
    print(f"\n{'='*60}")
    print(f"🏆 LEAGUE CHAMPION: {final_winner} 🏆")
    print(f"{'='*60}\n")
    
    # Reset advanced coefficients to balanced after league ends
    try:
        reset_advanced_profile()
        print("✅ Game coefficients reset to Balanced defaults")
    except Exception as e:
        print(f"⚠️  Could not reset coefficients: {e}")
    
    return final_winner
