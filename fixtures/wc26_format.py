"""
WC '26 Format - World Cup style tournament.

Tournament structure:
1. All teams divided into 4 groups (A, B, C, D) fairly by strength
2. Single round-robin within each group
3. Top 2 teams from each group qualify for Super 8
4. Super 8 separation:
   - Group P: A1, B2, C2, D1
   - Group Q: A2, B1, C1, D2
5. Round-robin in Super 8 groups
6. Top 2 from each Super 8 group qualify for semis
7. Semis: P1 vs Q2 and Q1 vs P2
8. Finals: Winners of both semis
"""

import random
from match_simulator import simulate_match
import database
from config_manager import reset_advanced_profile
from teams_helper import divide_teams_into_balanced_groups, calculate_team_strength


def create_round_robin_fixtures(teams):
    """Create round-robin fixtures where each team plays every other team once."""
    fixtures = []
    n = len(teams)
    
    # Each team plays every other team once
    for i in range(n):
        for j in range(n):
            if i > j:
                fixtures.append((teams[i], teams[j]))
    
    # Shuffle to randomize order
    random.shuffle(fixtures)
    return fixtures


def get_team_nrr(team_name):
    """Calculate NRR for a team from database statistics."""
    teams_db = database.load_teams()
    if team_name in teams_db:
        return database.compute_nrr_for_team_entry(teams_db[team_name])
    return 0.0


def get_stage_nrr(team_name, snapshot):
    """
    Calculate NRR for a team since a snapshot point.
    
    This computes NRR only from matches played after the snapshot,
    useful for stage-specific NRR (e.g., Super Eight only).
    
    Args:
        team_name: Name of the team
        snapshot: Dict mapping team names to their stats at snapshot time
    
    Returns:
        NRR computed from matches since snapshot
    """
    current = database.get_team_stats(team_name)
    snap = snapshot.get(team_name, {"runs_scored": 0, "runs_conceded": 0, "balls_faced": 0, "balls_bowled": 0})
    
    # Calculate delta (stats since snapshot)
    runs_scored = current["runs_scored"] - snap.get("runs_scored", 0)
    runs_conceded = current["runs_conceded"] - snap.get("runs_conceded", 0)
    balls_faced = current["balls_faced"] - snap.get("balls_faced", 0)
    balls_bowled = current["balls_bowled"] - snap.get("balls_bowled", 0)
    
    return database.compute_nrr(runs_scored, runs_conceded, balls_faced, balls_bowled)


def print_group_table(group_name, standings, nrr_override=None):
    """
    Print a nicely formatted group standings table.
    
    Args:
        group_name: Name of the group
        standings: List of (team, stats) tuples
        nrr_override: Optional dict mapping team names to NRR values.
                      If provided, uses these instead of database NRR.
    """
    print(f"\n{'='*70}")
    print(f"GROUP {group_name} STANDINGS")
    print(f"{'='*70}")
    print(f"{'Pos':<4} {'Team':<8} {'Pts':<6} {'W':<3} {'L':<3} {'T':<3} {'NRR':<8}")
    print("-" * 70)
    
    for idx, (team, stats) in enumerate(standings, 1):
        # Use override NRR if provided, otherwise get from database
        if nrr_override is not None and team in nrr_override:
            nrr = nrr_override[team]
        else:
            nrr = get_team_nrr(team)
        print(f"{idx:<4} {team:<8} {stats['points']:<6} {stats['wins']:<3} {stats['losses']:<3} {stats['ties']:<3} {nrr:>7.3f}")
    
    print("=" * 70)


def simulate_wc26_format(selected_teams, playoff_ball_by_ball=False):
    """
    Simulate a league with WC '26 format.
    
    Args:
        selected_teams: List of teams participating
        playoff_ball_by_ball: Whether to show ball-by-ball for playoff matches
    
    Returns:
        Champion team name
    """
    print(f"\n{'='*70}")
    print(f"League Format: World Cup '26 ({len(selected_teams)} teams)")
    
    # if len(selected_teams) != 8:
    #     raise ValueError("WC '26 format requires exactly 8 teams (divisible into 4 groups of 2)")
    
    # if len(selected_teams) % 4 != 0:
    #     raise ValueError(f"WC '26 format requires teams divisible by 4 for group stage")
    
    print(f"{'='*70}\n")
    
    # ========== GROUP STAGE ==========
    print("DIVIDING TEAMS INTO GROUPS (Balanced by Strength)...\n")
    
    groups_list = divide_teams_into_balanced_groups(selected_teams, num_groups=4)
    group_names = ['A', 'B', 'C', 'D']
    groups = {}
    
    # Display group assignments
    for group_idx, (group_name, teams_in_group) in enumerate(zip(group_names, groups_list)):
        groups[group_name] = {
            'teams': teams_in_group,
            'standings': {team: {'points': 0, 'wins': 0, 'losses': 0, 'ties': 0, 'nrr': 0.0} for team in teams_in_group}
        }
        
        print(f"Group {group_name}: {', '.join(teams_in_group)}")
    
    print("\n" + "=" * 70)
    print("GROUP STAGE - ROUND ROBIN")
    print("=" * 70)
    
    match_counter = 1
    total_group_matches = (len(selected_teams) // 4) * (len(selected_teams) // 4 - 1) * 4  # matches per group
    
    # Play group stage matches
    for group_name in group_names:
        print(f"\n--- GROUP {group_name} ---")
        group_teams = groups[group_name]['teams']
        fixtures = create_round_robin_fixtures(group_teams)
        
        for team_a, team_b in fixtures:
            print(f"[Match {match_counter}/{total_group_matches}] {team_a} vs {team_b}: ", end="")
            winner = simulate_match(team_a, team_b, False)
            match_counter += 1
            
            # Update standings
            if winner == "TIE":
                groups[group_name]['standings'][team_a]['points'] += 1
                groups[group_name]['standings'][team_b]['points'] += 1
                groups[group_name]['standings'][team_a]['ties'] += 1
                groups[group_name]['standings'][team_b]['ties'] += 1
            else:
                groups[group_name]['standings'][winner]['points'] += 2
                groups[group_name]['standings'][winner]['wins'] += 1
                loser = team_b if winner == team_a else team_a
                groups[group_name]['standings'][loser]['losses'] += 1
        
        # Display group standings after all matches for this group
        print(f"\n" + "="*70)
        print(f"GROUP {group_name} MATCHES COMPLETED")
        print("="*70)
        
        # Sort by points and NRR (from database)
        standings = sorted(
            groups[group_name]['standings'].items(),
            key=lambda x: (-x[1]['points'], -get_team_nrr(x[0]))
        )
        
        print_group_table(group_name, standings)
        
        # Update standings with sorted order for qualification
        groups[group_name]['qualified'] = [standings[0][0], standings[1][0]]
        print(f"Qualified from Group {group_name}: {standings[0][0]} (1st), {standings[1][0]} (2nd)\n")
        
        # Wait for user to continue
        input(f"Press Enter to continue to next group...")
    
    # Print final group stage summary
    print("\n" + "=" * 70)
    print("GROUP STAGE RESULTS SUMMARY")
    print("=" * 70)
    
    group_qualified = {}
    for group_name in group_names:
        # Recalculate sorted standings for display
        standings = sorted(
            groups[group_name]['standings'].items(),
            key=lambda x: (-x[1]['points'], -get_team_nrr(x[0]))
        )
        group_qualified[group_name] = [standings[0][0], standings[1][0]]
        print(f"Group {group_name}: {group_qualified[group_name][0]} (1st), {group_qualified[group_name][1]} (2nd)")
    
    # ========== SUPER 8 STAGE ==========
    print("\n" + "=" * 70)
    print("SUPER 8 STAGE")
    print("=" * 70)
    
    # Create Super 8 groups based on qualification
    # Group P: A1, B2, C2, D1
    # Group Q: A2, B1, C1, D2
    group_p_teams = [
        group_qualified['A'][0],  # A1
        group_qualified['B'][1],  # B2
        group_qualified['C'][1],  # C2
        group_qualified['D'][0],  # D1
    ]
    
    group_q_teams = [
        group_qualified['A'][1],  # A2
        group_qualified['B'][0],  # B1
        group_qualified['C'][0],  # C1
        group_qualified['D'][1],  # D2
    ]
    
    print(f"\nGroup P: {', '.join(group_p_teams)}")
    print(f"Group Q: {', '.join(group_q_teams)}")
    
    # Snapshot team stats before Super 8 starts (for stage-specific NRR calculation)
    super8_all_teams = group_p_teams + group_q_teams
    super8_stats_snapshot = {team: database.get_team_stats(team) for team in super8_all_teams}
    
    # Wait before starting Super 8
    input("\nPress Enter to start SUPER 8 GROUP P matches...")
    
    # Initialize Super 8 standings
    super8_groups = {
        'P': {
            'teams': group_p_teams,
            'standings': {team: {'points': 0, 'wins': 0, 'losses': 0, 'ties': 0, 'nrr': 0.0} for team in group_p_teams}
        },
        'Q': {
            'teams': group_q_teams,
            'standings': {team: {'points': 0, 'wins': 0, 'losses': 0, 'ties': 0, 'nrr': 0.0} for team in group_q_teams}
        }
    }
    
    # Play Super 8 matches
    match_counter = 1
    total_super8_matches = 6 * 2  # 6 matches per group, 2 groups
    
    for super8_group_name in ['P', 'Q']:
        print(f"\n--- GROUP {super8_group_name} ---")
        super8_teams = super8_groups[super8_group_name]['teams']
        fixtures = create_round_robin_fixtures(super8_teams)
        
        for team_a, team_b in fixtures:
            print(f"[Match {match_counter}/{total_super8_matches}] {team_a} vs {team_b}: ", end="")
            winner = simulate_match(team_a, team_b, False)
            match_counter += 1
            
            # Update standings
            if winner == "TIE":
                super8_groups[super8_group_name]['standings'][team_a]['points'] += 1
                super8_groups[super8_group_name]['standings'][team_b]['points'] += 1
                super8_groups[super8_group_name]['standings'][team_a]['ties'] += 1
                super8_groups[super8_group_name]['standings'][team_b]['ties'] += 1
            else:
                super8_groups[super8_group_name]['standings'][winner]['points'] += 2
                super8_groups[super8_group_name]['standings'][winner]['wins'] += 1
                loser = team_b if winner == team_a else team_a
                super8_groups[super8_group_name]['standings'][loser]['losses'] += 1
        
        # Display Super 8 group standings after all matches
        print(f"\n" + "="*70)
        print(f"SUPER 8 GROUP {super8_group_name} MATCHES COMPLETED")
        print("="*70)
        
        # Compute stage-specific NRR for each team in this Super 8 group
        super8_nrr = {team: get_stage_nrr(team, super8_stats_snapshot) 
                      for team in super8_groups[super8_group_name]['teams']}
        
        # Sort by points and Super 8-specific NRR (not overall tournament NRR)
        standings = sorted(
            super8_groups[super8_group_name]['standings'].items(),
            key=lambda x: (-x[1]['points'], -super8_nrr[x[0]])
        )
        
        print_group_table(super8_group_name, standings, nrr_override=super8_nrr)
        
        # Get top 2 teams
        qualified_from_super8 = [standings[0][0], standings[1][0]]
        print(f"Qualified from Group {super8_group_name}: {qualified_from_super8[0]} (1st), {qualified_from_super8[1]} (2nd)\n")
        
        # Wait before next Super 8 group or before semis
        if super8_group_name == 'P':
            input("Press Enter to continue to SUPER 8 GROUP Q...")
        else:
            input("Press Enter to continue to SEMI-FINALS...")
    
    # Print Super 8 standings summary
    print("\n" + "=" * 70)
    print("SUPER 8 RESULTS")
    print("=" * 70)
    
    super8_qualified = {}
    
    for super8_group_name in ['P', 'Q']:
        # Compute stage-specific NRR for sorting
        super8_nrr = {team: get_stage_nrr(team, super8_stats_snapshot) 
                      for team in super8_groups[super8_group_name]['teams']}
        
        # Sort by points and Super 8-specific NRR
        standings = sorted(
            super8_groups[super8_group_name]['standings'].items(),
            key=lambda x: (-x[1]['points'], -super8_nrr[x[0]])
        )
        
        # Get top 2 teams
        super8_qualified[super8_group_name] = [standings[0][0], standings[1][0]]
        print(f"Group {super8_group_name} Qualifiers: {super8_qualified[super8_group_name][0]} (1st), {super8_qualified[super8_group_name][1]} (2nd)")
    
    # ========== KNOCKOUT STAGES ==========
    print("\n" + "=" * 70)
    print("SEMI-FINALS")
    print("=" * 70)
    
    p1 = super8_qualified['P'][0]
    p2 = super8_qualified['P'][1]
    q1 = super8_qualified['Q'][0]
    q2 = super8_qualified['Q'][1]
    
    print(f"\nSemi-Final 1: {p1} (P1) vs {q2} (Q2)")
    input("Press Enter to simulate Semi-Final 1...")
    semi1_winner = simulate_match(p1, q2, playoff_ball_by_ball)
    
    print(f"\nSemi-Final 2: {q1} (Q1) vs {p2} (P2)")
    input("Press Enter to simulate Semi-Final 2...")
    semi2_winner = simulate_match(q1, p2, playoff_ball_by_ball)
    
    # ========== FINAL ==========
    print("\n" + "=" * 70)
    print("FINAL")
    print("=" * 70)
    
    print(f"\n{semi1_winner} vs {semi2_winner}")
    input("Press Enter to simulate the Final...")
    champion = simulate_match(semi1_winner, semi2_winner, playoff_ball_by_ball)
    
    # ========== RESULTS ==========
    print(f"\n{'='*70}")
    print(f"TOURNAMENT CHAMPION: {champion}")
    print(f"{'='*70}\n")
    
    # Reset advanced coefficients to balanced after tournament ends
    try:
        reset_advanced_profile()
        print("Game coefficients reset to Balanced defaults")
    except Exception as e:
        print(f"Could not reset coefficients: {e}")
    
    return champion
