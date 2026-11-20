from collections import Counter

import pytest

from match_simulator import generate_bowling_order
from models import ROLES, STYLES, Player
from teams import BOWLING_ORDERS, get_bowler_ranking, get_player, get_teams

TEAMS = get_teams()


@pytest.mark.parametrize("team_name", TEAMS.keys())
def test_team_has_valid_squad(team_name):
    players = TEAMS[team_name]
    assert len(players) == 11
    assert len({p.name for p in players}) == 11, "duplicate player names"
    for p in players:
        assert 0 <= p.batting <= 10, p.name
        assert 0 <= p.bowling <= 10, p.name
        assert p.role in ROLES, p.name
        assert p.style in STYLES, p.name


def test_player_names_unique_across_squads():
    names = [p.name for squad in TEAMS.values() for p in squad]
    assert len(names) == len(set(names))
    assert get_player("J Bumrah").style == "pace"
    assert get_player("Nobody") is None


@pytest.mark.parametrize("team_name", TEAMS.keys())
def test_pure_batters_do_not_bowl(team_name):
    """A player labelled 'bat' getting overs means the label or the order is wrong."""
    order = generate_bowling_order(TEAMS[team_name], BOWLING_ORDERS.get(team_name))
    batters = sorted({p.name for p in order if p.role == "bat"})
    assert not batters, f"{team_name}: batters in bowling order: {batters}"


@pytest.mark.parametrize("team_name, order", BOWLING_ORDERS.items())
def test_bowling_order_is_legal(team_name, order):
    assert team_name in TEAMS, f"bowling order for unknown team {team_name}"
    assert len(order) == 20
    assert set(order) <= set("ABCDEFGHIJK")
    over_limit = {k: v for k, v in Counter(order).items() if v > 4}
    assert not over_limit, f"bowlers over 4 overs: {over_limit}"
    back_to_back = [i + 1 for i, (a, b) in enumerate(zip(order, order[1:])) if a == b]
    assert not back_to_back, f"same bowler in consecutive overs at over(s) {back_to_back}"


def test_bowler_ranking_sorts_by_skill_then_name():
    team = [Player(n, 5, b, "bowl", "pace") for n, b in [("Zed", 7), ("Amy", 7), ("Bob", 9), ("Cat", 1)]]
    ranking = get_bowler_ranking(team)
    assert [ranking[k].name for k in "ABCD"] == ["Bob", "Amy", "Zed", "Cat"]


@pytest.mark.parametrize("custom", [None, "CDCDEABEABEABEABDCDC"])
def test_generate_bowling_order_returns_20_overs(custom):
    team = TEAMS["MI"]
    order = generate_bowling_order(team, custom)
    assert len(order) == 20
    assert all(p in team for p in order)
