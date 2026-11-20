import builtins
import random

import pytest

import match_simulator as m
from captain import LiveCaptain
from fixtures import TOURNAMENT_FORMATS
from teams import get_teams

BAT, BOWL = "MI", "CSK"


def scripted(answers):
    """input() replacement that returns the given answers, then Enter forever."""
    it = iter(answers)
    return lambda prompt="": next(it, "")


def _innings(captain=None, seed=5, target=None):
    teams = get_teams()
    random.seed(seed)
    batting = teams[BAT]
    result = m.simulate_innings(batting, teams[BOWL], team_name=BAT, bowling_team_name=BOWL,
                                target=target, captain=captain)
    return batting, result


@pytest.mark.parametrize("seed", range(5))
def test_keeping_every_default_matches_automatic_play(seed):
    """Enter on every prompt must give exactly the same innings as no captain."""
    _, auto = _innings(None, seed)
    _, live = _innings(LiveCaptain(input_fn=scripted([]), print_fn=lambda *a: None), seed)
    assert live == auto


def test_chosen_openers_bat_first():
    teams = get_teams()
    expected = [teams[BAT][10].name, teams[BAT][9].name]
    batting, (score, wickets, bat_stats, _, fall) = _innings(
        LiveCaptain(input_fn=scripted(["11 10"]), print_fn=lambda *a: None))
    assert [p.name for p in batting[:2]] == expected
    assert bat_stats[0]["balls"] > 0  # the chosen opener really faced the first ball
    assert sum(s["runs"] for s in bat_stats) == score
    assert [w for _, w in fall] == list(range(1, wickets + 1))  # FOW shows wicket numbers


class LastBatterCaptain(LiveCaptain):
    """Always sends in the last batter on the list."""
    def __init__(self):
        super().__init__(input_fn=scripted([]), print_fn=lambda *a: None)
        self.sent_in = []

    def choose_next_batter(self, team_name, lineup, candidates, situation):
        self.sent_in.append(lineup[candidates[-1]].name)
        return candidates[-1]


def test_chosen_next_batter_comes_in_and_stats_stay_aligned():
    cap = LastBatterCaptain()
    batting, (score, wickets, bat_stats, _, _) = _innings(cap, seed=2)
    assert wickets >= 1 and cap.sent_in
    assert batting[2].name == cap.sent_in[0]
    assert sum(s["runs"] for s in bat_stats) == score
    batted = [s for s in bat_stats if s["balls"] > 0 or s["dismissal"] != "not out"]
    assert bat_stats[:len(batted)] == batted  # everyone who batted is at the top, in order


class GreedyCaptain(LiveCaptain):
    """Tries to bowl the same bowler every over; records what the engine offered."""
    def __init__(self, favourite):
        super().__init__(input_fn=scripted([]), print_fn=lambda *a: None)
        self.favourite, self.offers = favourite, []

    def choose_bowler(self, team_name, over_num, ranking, allowed, default, overs_left, situation):
        self.offers.append(({p.name for p in allowed}, dict(overs_left)))
        return next(p for p in ranking.values() if p.name == self.favourite)


def test_bowling_rules_hold_whatever_the_captain_picks():
    cap = GreedyCaptain("A Noor")
    _, (_, _, _, bowl_stats, _) = _innings(cap, seed=1)
    assert all(s["balls"] <= 24 for s in bowl_stats.values())
    assert bowl_stats["A Noor"]["balls"] <= 24
    # who bowled each over = whose overs_left dropped between offers
    for (_, before), (allowed_next, after) in zip(cap.offers, cap.offers[1:]):
        bowled = next(n for n in before if after[n] == before[n] - 1)
        assert bowled not in allowed_next, "same bowler offered two overs in a row"


def test_prompt_parsing_rejects_bad_input_and_supports_auto():
    teams = get_teams()
    lineup = teams[BAT]
    out = []
    cap = LiveCaptain(input_fn=scripted(["x", "1 1", "12 1", "3 4"]), print_fn=out.append)
    assert cap.choose_openers(BAT, lineup) == (2, 3)
    assert sum("two different numbers" in str(o) for o in out) == 3

    ranking = m.get_bowler_ranking(lineup)
    allowed = [p for p in lineup if p.name != "J Bumrah"]
    default = ranking["B"]
    cap = LiveCaptain(input_fn=scripted(["auto"]), print_fn=lambda *a: None)
    assert cap.choose_bowler(BAT, 0, ranking, allowed, default, {p.name: 4 for p in lineup}, "") is default
    assert cap.auto
    cap = LiveCaptain(input_fn=scripted(["A", "c"]), print_fn=lambda *a: None)  # A = Bumrah, unavailable -> re-ask
    assert cap.choose_bowler(BAT, 0, ranking, allowed, default, {p.name: 4 for p in lineup}, "") is ranking["C"]


@pytest.mark.parametrize("answer, bats_first_is_winner", [("bowl", False), ("", True)])
def test_toss_winner_chooses(answer, bats_first_is_winner):
    cap = LiveCaptain(input_fn=scripted([answer]), print_fn=lambda *a: None)
    batting_first, _, winner, decision = m.coin_toss(BAT, BOWL, cap)
    assert (batting_first == winner) == bats_first_is_winner
    assert decision == ("BAT" if bats_first_is_winner else "BOWL")


@pytest.mark.parametrize("fmt", TOURNAMENT_FORMATS.values(), ids=lambda f: f["name"])
def test_formats_run_with_live_choices(monkeypatch, fmt, rows):
    prompts = []
    monkeypatch.setattr(builtins, "input", lambda p="": prompts.append(p) or "")
    teams = ["MI", "CSK", "RCB"] if fmt["name"].startswith("Double") else \
        ["MI", "CSK", "RCB", "KKR", "SRH", "RR", "PBKS", "GT"]
    champion = fmt["function"](teams, False, False, captain=LiveCaptain())
    assert champion in teams
    assert any("bowler" in p for p in prompts) and any("Openers" in p for p in prompts)
