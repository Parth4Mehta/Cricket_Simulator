import pytest

from fixtures import TOURNAMENT_FORMATS
from teams_helper import divide_teams_into_balanced_groups

# Team list and expected match count per format. Add an entry when adding a format.
FORMAT_CASES = {
    # 4 teams: 4*3 league games + Q1, Eliminator, Q2, Final
    "Double Round-Robin + Playoffs": (["MI", "CSK", "RCB", "KKR"], 12 + 4),
    # 8 teams: 4 groups of 2 (4 games) + two Super 8 groups of 4 (12) + 2 semis + final
    "World Cup '26 Format": (["MI", "CSK", "RCB", "KKR", "SRH", "RR", "PBKS", "GT"], 4 + 12 + 3),
}


def test_every_format_has_a_test_case():
    names = {f["name"] for f in TOURNAMENT_FORMATS.values()}
    assert names == set(FORMAT_CASES), "add new formats to FORMAT_CASES"


@pytest.mark.parametrize("fmt", TOURNAMENT_FORMATS.values(), ids=lambda f: f["name"])
def test_format_runs_end_to_end(fmt, rows):
    teams, expected_matches = FORMAT_CASES[fmt["name"]]

    champion = fmt["function"](teams, playoff_ball_by_ball=False, league_ball_by_ball=False)

    assert champion in teams
    assert rows("SELECT COUNT(*) FROM matches")[0][0] == expected_matches
    assert rows("SELECT COUNT(*) FROM matches WHERE stage = 'playoff'")[0][0] > 0


@pytest.mark.parametrize("n_teams", [8, 12, 16])
def test_balanced_groups_cover_every_team_once(n_teams):
    from teams import get_teams
    teams = list(get_teams())[:n_teams]
    groups = divide_teams_into_balanced_groups(teams, num_groups=4)
    flat = [t for g in groups for t in g]
    assert sorted(flat) == sorted(teams)
    assert max(map(len, groups)) - min(map(len, groups)) <= 1
