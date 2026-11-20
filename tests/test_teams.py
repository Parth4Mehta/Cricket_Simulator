from collections import Counter

import pytest

from match_simulator import generate_bowling_order
from models import Player
from teams import BOWLING_ORDERS, get_bowler_ranking, get_teams

TEAMS = get_teams()


@pytest.mark.parametrize("team_name", TEAMS.keys())
def test_team_has_valid_squad(team_name):
    players = TEAMS[team_name]
    assert len(players) == 11
    assert len({p.name for p in players}) == 11, "duplicate player names"
    for p in players:
        assert 0 <= p.batting <= 10, p.name
        assert 0 <= p.bowling <= 10, p.name


@pytest.mark.parametrize("team_name, order", BOWLING_ORDERS.items())
def test_bowling_order_is_legal(team_name, order):
    assert team_name in TEAMS, f"bowling order for unknown team {team_name}"
    assert len(order) == 20
    assert set(order) <= set("ABCDEFGHIJK")
    over_limit = {k: v for k, v in Counter(order).items() if v > 4}
    assert not over_limit, f"bowlers over 4 overs: {over_limit}"


def test_bowler_ranking_sorts_by_skill_then_name():
    team = [Player("Zed", 5, 7), Player("Amy", 5, 7), Player("Bob", 5, 9), Player("Cat", 5, 1)]
    ranking = get_bowler_ranking(team)
    assert [ranking[k].name for k in "ABCD"] == ["Bob", "Amy", "Zed", "Cat"]


@pytest.mark.parametrize("custom", [None, "CDCDEABEABEABEABDCDC"])
def test_generate_bowling_order_returns_20_overs(custom):
    team = TEAMS["MI"]
    order = generate_bowling_order(team, custom)
    assert len(order) == 20
    assert all(p in team for p in order)
