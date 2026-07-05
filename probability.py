import random

BOWLING_FOUR_PENALTY = 0.0006
BOWLING_SIX_PENALTY = 0.0003
BATTING_WICKET_REDUCTION = 0.002
BATTING_DOT_REDUCTION = 0.01
BOWLING_DOT_BOOST = 0.0008
DEATH_FOUR_BATTING_BOOST = 0.009
DEATH_FOUR_BOWLING_PENALTY = 0.0002
DEATH_SIX_BATTING_BOOST = 0.006
DEATH_SIX_BOWLING_PENALTY = 0.0001
DEATH_WICKET_BOWLING_BOOST = 0.006
DEATH_DOT_REDUCTION = 0.05
DEATH_DOT_BOWLING_OFFSET = 0.0002
RUN_RESIDUAL = 0.3
RUN_WEIGHTS = (60, 30, 10)


def calculate_effective_bowling(bowling_skill, up_value, fatigue_rate, overs_bowled):
    return bowling_skill + up_value - (fatigue_rate * overs_bowled)


def calculate_ball_probabilities(striker_batting, effective_bowling, over_num, total_overs, coefficients):
    four_coeff, six_coeff, wicket_coeff, dot_ball_coeff, batsman_four_boost, batsman_six_boost, bowler_wicket_boost = coefficients
    p4 = four_coeff + striker_batting * batsman_four_boost - effective_bowling * BOWLING_FOUR_PENALTY
    p6 = six_coeff + striker_batting * batsman_six_boost - effective_bowling * BOWLING_SIX_PENALTY
    pw = wicket_coeff - striker_batting * BATTING_WICKET_REDUCTION + effective_bowling * bowler_wicket_boost
    pdot = dot_ball_coeff - striker_batting * BATTING_DOT_REDUCTION + effective_bowling * BOWLING_DOT_BOOST

    if over_num >= total_overs - 4:
        p4 += striker_batting * DEATH_FOUR_BATTING_BOOST - effective_bowling * DEATH_FOUR_BOWLING_PENALTY
        p6 += striker_batting * DEATH_SIX_BATTING_BOOST - effective_bowling * DEATH_SIX_BOWLING_PENALTY
        pw += effective_bowling * DEATH_WICKET_BOWLING_BOOST
        pdot -= DEATH_DOT_REDUCTION - effective_bowling * DEATH_DOT_BOWLING_OFFSET

    total = p4 + p6 + pw + pdot + RUN_RESIDUAL
    return p4 / total, p6 / total, pw / total, pdot / total


def determine_ball_outcome(p4, p6, pw, pdot):
    outcome = random.random()

    if outcome < pw:
        return "wicket", 0
    if outcome < pw + p6:
        return "six", 6
    if outcome < pw + p6 + p4:
        return "four", 4
    if outcome < pw + p6 + p4 + pdot:
        return "dot", 0
    return "runs", random.choices((1, 2, 3), weights=RUN_WEIGHTS, k=1)[0]
