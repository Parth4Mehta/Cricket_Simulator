import random

import pytest

import database
from match_simulator import simulate_innings, simulate_match
from teams import get_teams

TEAMS = get_teams()
BAT, BOWL = "MI", "CSK"


def _check_innings(result, batting_team):
    score, wickets, bat_stats, bowl_stats, fall = result
    balls = sum(s["balls"] for s in bat_stats)

    assert 0 <= wickets <= 10
    assert len(fall) == wickets
    assert balls <= 120
    assert sum(s["runs"] for s in bat_stats) == score
    # No extras in this game: every run is off the bat and charged to a bowler.
    assert sum(b["runs"] for b in bowl_stats.values()) == score
    assert sum(b["balls"] for b in bowl_stats.values()) == balls
    assert sum(b["wickets"] for b in bowl_stats.values()) == wickets
    assert all(b["balls"] <= 24 for b in bowl_stats.values())
    assert len(bat_stats) == len(batting_team)
    return score, wickets, balls


@pytest.mark.parametrize("seed", range(10))
def test_first_innings_invariants(seed):
    random.seed(seed)
    result = simulate_innings(TEAMS[BAT], TEAMS[BOWL], team_name=BAT, bowling_team_name=BOWL)
    score, wickets, balls = _check_innings(result, TEAMS[BAT])
    assert balls == 120 or wickets == 10  # innings only ends early on all out


@pytest.mark.parametrize("seed", range(10))
def test_chase_stops_at_target(seed):
    random.seed(seed)
    target = 60
    result = simulate_innings(TEAMS[BAT], TEAMS[BOWL], target=target,
                              team_name=BAT, bowling_team_name=BOWL)
    score, wickets, balls = _check_innings(result, TEAMS[BAT])
    if score >= target:
        assert score <= target + 5  # stopped on the ball that got there
    else:
        assert balls == 120 or wickets == 10


def test_simulate_match_persists_one_consistent_result(rows):
    winner = simulate_match(BAT, BOWL)

    assert len(rows("SELECT * FROM matches")) == 1
    table = {r["team"]: r for r in database.get_points_table_sorted()}
    a, b = table[BAT], table[BOWL]
    assert a["played"] == b["played"] == 1
    assert a["points"] + b["points"] == 2

    if winner == "TIE":
        assert a["runs_scored"] == b["runs_scored"]
        assert a["tied"] == b["tied"] == 1
    else:
        loser = BOWL if winner == BAT else BAT
        assert winner in (BAT, BOWL)
        assert table[winner]["won"] == 1 and table[loser]["lost"] == 1
        assert table[winner]["runs_scored"] > table[loser]["runs_scored"]


def test_unknown_team_raises():
    with pytest.raises(ValueError):
        simulate_match("MI", "NOT_A_TEAM")


def test_scorecard_and_player_card_show_labels(capsys):
    import historical
    simulate_match(BAT, BOWL)
    out = capsys.readouterr().out
    assert "BOWL" in out and "pace" in out  # role + style columns rendered

    historical.print_player_card(historical.get_player_card_current("J Bumrah"))
    assert "BOWL · pace" in capsys.readouterr().out
