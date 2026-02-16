"""
teams_helper.py

Helper functions for team operations like strength calculation and grouping.
"""

from teams import get_teams


def calculate_team_strength(team_name):
    """
    Calculate overall strength of a team based on player stats.
    
    Args:
        team_name (str): Name of the team
    
    Returns:
        float: Team strength index (average combined batting + bowling)
    """
    teams = get_teams()
    
    if team_name not in teams:
        raise ValueError(f"Team {team_name} not found")
    
    players = teams[team_name]
    total_strength = 0
    
    for player in players:
        # Combine batting and bowling score as team strength metric
        player_strength = (player.batting + player.bowling) / 2
        total_strength += player_strength
    
    return total_strength / len(players)


def get_all_team_strengths():
    """
    Get strength ratings for all teams.
    
    Returns:
        dict: Mapping of team_name -> strength_value, sorted by strength descending
    """
    teams = get_teams()
    strengths = {}
    
    for team_name in teams.keys():
        strengths[team_name] = calculate_team_strength(team_name)
    
    # Sort by strength descending
    return dict(sorted(strengths.items(), key=lambda x: -x[1]))


def divide_teams_into_balanced_groups(teams_list, num_groups=4):
    """
    Divide teams into balanced groups by strength.
    Uses a snake draft approach to ensure fair group distribution.
    
    Args:
        teams_list (list): List of team names
        num_groups (int): Number of groups to create (default: 4)
    
    Returns:
        list: List of lists, each containing teams for that group
    """
    # if len(teams_list) % num_groups != 0:
    #     raise ValueError(f"Cannot evenly divide {len(teams_list)} teams into {num_groups} groups")
    
    # Calculate strength for each team
    team_strengths = {team: calculate_team_strength(team) for team in teams_list}
    
    # Sort teams by strength (descending)
    sorted_teams = sorted(teams_list, key=lambda t: -team_strengths[t])
    
    # Initialize groups
    groups = [[] for _ in range(num_groups)]
    
    # Snake draft: alternate direction for each round
    for idx, team in enumerate(sorted_teams):
        group_idx = idx % num_groups
        # Direction for snake: if round is even, go forward; if odd, go backward
        round_num = idx // num_groups
        if round_num % 2 == 1:
            group_idx = num_groups - 1 - group_idx
        groups[group_idx].append(team)
    
    return groups
