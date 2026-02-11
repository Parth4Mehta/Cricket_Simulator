import random
import time
from teams import get_teams
import database
from config_manager import get_profile, list_profiles, get_default_profile

# Global game coefficients - initialized with default profile
FOUR_COEFF = 0.02
SIX_COEFF = 0.01
WICKET_COEFF = 0.013
DOT_BALL_COEFF = 0.45
BATSMAN_SIX_BOOST = 0.008
BATSMAN_FOUR_BOOST = 0.016
BOWLER_WICKET_BOOST = 0.006


def load_profile(profile_name):
    """Load a difficulty profile and set global coefficients."""
    global FOUR_COEFF, SIX_COEFF, WICKET_COEFF, DOT_BALL_COEFF
    global BATSMAN_SIX_BOOST, BATSMAN_FOUR_BOOST, BOWLER_WICKET_BOOST
    
    try:
        profile = get_profile(profile_name)
        FOUR_COEFF = profile["four_coeff"]
        SIX_COEFF = profile["six_coeff"]
        WICKET_COEFF = profile["wicket_coeff"]
        DOT_BALL_COEFF = profile["dot_ball_coeff"]
        BATSMAN_SIX_BOOST = profile["batsman_six_boost"]
        BATSMAN_FOUR_BOOST = profile["batsman_four_boost"]
        BOWLER_WICKET_BOOST = profile["bowler_wicket_boost"]
        print(f"Loaded profile: {profile['label']}")
        return profile
    except Exception as e:
        print(f"Error loading profile: {e}")
        load_profile_default()


def load_profile_default():
    """Load the default difficulty profile."""
    profile = get_default_profile()
    load_profile(profile.get("label", "balanced").lower())


def choose_profile():
    """Prompt user to pick a difficulty profile."""
    print("\n=== Choose Game Difficulty ===")
    profiles = list_profiles()
    profile_list = list(profiles.items())
    
    for idx, (key, label) in enumerate(profile_list, 1):
        print(f"{idx}. {label}")
    
    while True:
        choice = input(f"Enter 1-{len(profile_list)} (default 1): ").strip() or "1"
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(profile_list):
                profile_key, _ = profile_list[idx]
                load_profile(profile_key)
                print()
                return
        except ValueError:
            pass
        print(f"Invalid choice. Enter 1-{len(profile_list)}")


def choose_profile_default():
    """Automatically load default profile without prompting."""
    load_profile_default()
def generate_bowling_order(best5):
    A, B, C, D, E = best5
    order = [A, B, A, B, C, D, E, C, D, E, C, D, E, C, D, E, A, B, A, B]
    return order  # 20 overs


def simulate_innings(batting_team, bowling_team, ball_by_ball=False, target=None, total_overs=20, team_name=None):
    best5 = sorted(bowling_team, key=lambda p: p.bowling, reverse=True)[:5]
    bowling_order = generate_bowling_order(best5)

    score = 0
    wickets = 0

    # striker and non-striker indices and next batsman to come
    striker_idx = 0
    non_striker_idx = 1 if len(batting_team) > 1 else 0
    next_batsman = 2

    batting_stats = [
        {"runs": 0, "balls": 0, "4s": 0, "6s": 0, "dismissal": "not out"}
        for _ in batting_team
    ]

    bowling_stats = {b.name: {"overs": 0, "balls": 0, "runs": 0, "wickets": 0}
                     for b in bowling_team}

    fall_of_wickets = []

    balls_bowled = 0
    def _print_over_summary(tokens, over_idx, bowler_obj, bowler_stats_obj, balls_bowled_local, striker_idx_local, non_striker_idx_local):
        # compute runs in over
        over_runs_local = 0
        for t in tokens:
            if t == '6':
                over_runs_local += 6
            elif t == '4':
                over_runs_local += 4
            elif t in ('.', 'W'):
                over_runs_local += 0
            else:
                try:
                    over_runs_local += int(t)
                except Exception:
                    pass
        # finish the current over line
        print()  # end the carriage-returned line
        # print(f"Over {over_idx+1}  |  {' '.join(tokens)}  | ({over_runs_local} runs)")
        # batsmen
        b1_idx = striker_idx_local
        b2_idx = non_striker_idx_local
        b1_name = batting_team[b1_idx].name
        b2_name = batting_team[b2_idx].name
        b1_runs = batting_stats[b1_idx]["runs"]
        b1_balls = batting_stats[b1_idx]["balls"]
        b2_runs = batting_stats[b2_idx]["runs"]
        b2_balls = batting_stats[b2_idx]["balls"]
        def _fmt_b(idx, name, runs, balls, next_idx):
            star = '*' if idx == next_idx else ''
            return f"{name} {runs}({balls}){star}"
        print("Batsmen:", _fmt_b(b1_idx, b1_name, b1_runs, b1_balls, non_striker_idx_local), "|", _fmt_b(b2_idx, b2_name, b2_runs, b2_balls, non_striker_idx_local))
        # bowler stats
        bowler_name = bowler_obj.name
        bb = bowler_stats_obj.get("balls", 0)
        bow_overs = bb // 6
        bow_rem = bb % 6
        bow_overs_str = f"{bow_overs}.{bow_rem}"
        bow_runs = bowler_stats_obj.get("runs", 0)
        bow_wk = bowler_stats_obj.get("wickets", 0)
        print(f"Bowler : {bowler_name} — {bow_overs_str}, {bow_runs}, {bow_wk}")
        print(f"Total: {score}/{wickets} in {balls_bowled_local//6}.{balls_bowled_local%6} overs")
        print()
        # runs required if chasing
        if target is not None:
            runs_needed = max(0, target - score)
            overs_completed = balls_bowled_local // 6
            balls_in_current_over = balls_bowled_local % 6
            overs_str = f"{overs_completed}.{balls_in_current_over}"
            remaining_overs = total_overs - (balls_bowled_local / 6)
            print(f"Runs required: {runs_needed} in {remaining_overs} overs")
            
    for bowler_idx, bowler in enumerate(bowling_order):
        bowler_stats = bowling_stats[bowler.name]

        over_num = bowler_idx  # 0-based
        per_over_tokens = []
        for ball_in_over in range(6):
            if wickets == 10:
                return score, wickets, batting_stats, bowling_stats, fall_of_wickets

            # current striker
            striker = batting_team[striker_idx]
            striker_stats = batting_stats[striker_idx]

            bowler_stats["balls"] += 1
            balls_bowled += 1

            p4 = FOUR_COEFF + striker.batting * BATSMAN_FOUR_BOOST
            p6 = SIX_COEFF + striker.batting * BATSMAN_SIX_BOOST
            pw = WICKET_COEFF - striker.batting * 0.002 + bowler.bowling * BOWLER_WICKET_BOOST #0.002 is good
            pdot = DOT_BALL_COEFF - striker.batting * 0.01

            #Make last 4 overs more exciting - increase chances of boundaries and wickets
            if over_num >= total_overs - 4:
                p4 += striker.batting * 0.009
                p6 += striker.batting * 0.006
                pw += bowler.bowling * 0.006
                pdot -= 0.05
            
            total = p4 + p6 + pw + pdot + 0.3
            p4 /= total
            p6 /= total
            pw /= total
            pdot /= total

            striker_stats["balls"] += 1
            outcome = random.random()

            if outcome < pw:
                # wicket: striker out
                wickets += 1
                bowler_stats["wickets"] += 1
                striker_stats["dismissal"] = f"c&b {bowler.name}"
                fall_of_wickets.append((score, striker_idx + 1))
                per_over_tokens.append('W')

                # new batsman comes to striker's end (if available)
                if next_batsman < len(batting_team):
                    striker_idx = next_batsman
                    next_batsman += 1
                else:
                    # all out
                    if ball_by_ball:
                        # print final over summary
                        _print_over_summary(per_over_tokens, over_num, bowler, bowler_stats, balls_bowled, striker_idx, non_striker_idx)
                    return score, wickets, batting_stats, bowling_stats, fall_of_wickets

            elif outcome < pw + p6:
                score += 6
                striker_stats["runs"] += 6
                striker_stats["6s"] += 1
                bowler_stats["runs"] += 6
                per_over_tokens.append('6')

            elif outcome < pw + p6 + p4:
                score += 4
                striker_stats["runs"] += 4
                striker_stats["4s"] += 1
                bowler_stats["runs"] += 4
                per_over_tokens.append('4')

            elif outcome < pw + p6 + p4 + pdot:
                # dot ball
                per_over_tokens.append('.')

            else:
                    run = random.choices([1, 2, 3], weights=[60, 30, 10], k=1)[0]
                    score += run
                    striker_stats["runs"] += run
                    bowler_stats["runs"] += run
                    per_over_tokens.append(str(run))

                    # change strike on odd runs
                    if run % 2 == 1:
                        striker_idx, non_striker_idx = non_striker_idx, striker_idx
            # print ball-by-ball token if enabled — update same over line
            if ball_by_ball:
                # for wicket, ensure token present
                if outcome < pw and not per_over_tokens:
                    per_over_tokens.append('W')
                # overwrite same line for current over
                print(f"Over {over_num+1}: {' '.join(per_over_tokens)}", end='\r', flush=True)
                time.sleep(0.7)
            # if chasing and reached target, end innings immediately
            if target is not None and score >= target:
                # ensure final over line printed properly
                if ball_by_ball:
                    _print_over_summary(per_over_tokens, over_num, bowler, bowler_stats, balls_bowled, striker_idx, non_striker_idx)
                return score, wickets, batting_stats, bowling_stats, fall_of_wickets
        # end of over: update overs and swap strike
        bowler_stats["overs"] = bowler_stats["balls"] // 6
        # print final over summary if ball_by_ball (ensure full over line)
        if ball_by_ball:
            _print_over_summary(per_over_tokens, over_num, bowler, bowler_stats, balls_bowled, striker_idx, non_striker_idx)
        striker_idx, non_striker_idx = non_striker_idx, striker_idx

    return score, wickets, batting_stats, bowling_stats, fall_of_wickets


def print_scorecard(team_name, batting_team, score, wickets, batting_stats, bowling_stats, fall):
    print(f"\n===== {team_name} Scorecard =====")
    print(f"{team_name}: {score}/{wickets}\n")

    print("### Batting")
    print(f"{'Player':20} {'R':>3} {'B':>3} {'4s':>3} {'6s':>3} {'SR':>6}   {'Dismissal'}")

    for i, s in enumerate(batting_stats):
        player_name = batting_team[i].name
        balls = s["balls"]
        sr = (s["runs"] / balls * 100) if balls > 0 else 0
        print(
            f"{i+1:<2}. {player_name:20} "
            f"{s['runs']:>3} {balls:>3} {s['4s']:>3} {s['6s']:>3} "
            f"{sr:>6.1f}   {s['dismissal']}"
        )

    # -------------------------
    # BOWLING TABLE
    # -------------------------
    print("\n### Bowling")
    print(f"{'Bowler':20} {'O':>3} {'R':>3} {'W':>3} {'Econ':>6}")

    sorted_bowlers = sorted(
        [b for b in bowling_stats.items() if b[1]["balls"] > 0],
        key=lambda x: x[1]["overs"],
        reverse=True
    )

    for bname, s in sorted_bowlers:
        overs = s["overs"]
        runs = s["runs"]
        wk = s["wickets"]
        econ = runs / overs if overs > 0 else 0
        print(f"{bname:20} {overs:>3} {runs:>3} {wk:>3} {econ:>6.2f}")

    print("\n### Fall of Wickets")
    for i, (runs, wicket_num) in enumerate(fall, 1):
        print(f"{i}. {runs}/{wicket_num}")

    # print which team won by how much:
    print("\n----------------------------------")


def simulate_match(teamA_name, teamB_name, ball_by_ball=False):
    # nicer centered header for the match
    header = f" MATCH: {teamA_name} vs {teamB_name} "
    line = "=" * max(0, (100 - len(header)) // 2)
    print(f"{line}{header}{line}")
    teams = get_teams()
    if teamA_name not in teams or teamB_name not in teams:
        raise ValueError("Team names not found in teams.py")

    A = teams[teamA_name]
    B = teams[teamB_name]

    # First innings
    A_score, A_wk, A_bat, A_bowl, A_fall = simulate_innings(A, B, ball_by_ball=ball_by_ball, team_name=teamA_name)
    print_scorecard(teamA_name, A, A_score, A_wk, A_bat, A_bowl, A_fall)

    if ball_by_ball:
        time.sleep(20)
    # Second innings (chase). target = A_score + 1
    target = A_score + 1
    B_score, B_wk, B_bat, B_bowl, B_fall = simulate_innings(B, A, ball_by_ball=ball_by_ball, target=target, team_name=teamB_name)
    print_scorecard(teamB_name, B, B_score, B_wk, B_bat, B_bowl, B_fall)

    if A_score > B_score:
        winner = teamA_name
    elif B_score > A_score:
        winner = teamB_name
    else:
        winner = "TIE"

    choice = "y"
    if choice != "n":
        # compute margin string for result
        if winner == teamA_name:
            margin = f"{A_score - B_score} runs" if A_score != B_score else ""
        elif winner == teamB_name:
            # wickets remaining is 10 - wickets lost by winner (B_wk)
            wickets_remaining = 10 - B_wk
            margin = f"{wickets_remaining} wickets" if wickets_remaining >= 0 else ""
        else:
            margin = ""

        result = {"winner": winner, "by": margin, "A_score": A_score, "B_score": B_score}

        path = database.save_match_file(teamA_name, teamB_name, A_bat, A_bowl, B_bat, B_bowl, teamA_objs=A, teamB_objs=B, result=result, A_score=A_score, B_score=B_score)
        database.update_players_from_match(teamA_name, A, A_bat, A_bowl)
        database.update_players_from_match(teamB_name, B, B_bat, B_bowl)

        A_balls_faced = sum(s.get("balls", 0) for s in A_bat)
        B_balls_faced = sum(s.get("balls", 0) for s in B_bat)

        # If the chasing team (B) finished the chase before 20 overs,
        # project how many runs they would have scored in a full 20.0 overs
        # using their current runs-per-ball rate and show that in the
        # concise match summary. Both teams are displayed with (20.0).
        display_A_score = A_score
        display_B_score = B_score
        total_balls = 20 * 6
        # target was set to A_score + 1 for the chase
        if B_score >= target and B_balls_faced < total_balls:
            if B_balls_faced > 0:
                runs_per_ball = B_score / B_balls_faced
                remaining_balls = total_balls - B_balls_faced
                projected_additional = runs_per_ball * remaining_balls
                projected_full = int(round(B_score + projected_additional))
                display_B_score = projected_full

        # concise match result lines
        print("\nMatch Result Summary:")
        print(f"{teamA_name}: {display_A_score}/{A_wk} (20.0)")
        print(f"{teamB_name}: {display_B_score}/{B_wk} (20.0)")
        # print winner and margin clearly
        if winner == "TIE":
            print("Result: Match tied")
        else:
            print(f"Result: {winner} won by {margin}")

        database.update_team_from_match(teamA_name, teamB_name, A_score, B_score, A_balls_faced, B_balls_faced, winner)

    return winner


if __name__ == "__main__":
    choose_profile()
    simulate_match("KKR", "MI", False)
    simulate_match("SRH", "MI", False)