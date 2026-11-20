"""Arrow-key menu mode of LiveCaptain.

Uses a fake menu to check what is offered, and the real questionary driven by
simulated key presses to check the integration (default pre-selected, arrows
move, disabled bowlers are skipped, menus erase themselves)."""
import random
import types

import pytest

import match_simulator as m
from captain import AUTO, LiveCaptain
from teams import get_teams

TEAM = "MI"
DOWN, ENTER = "\x1b[B", "\r"


class FakeMenu:
    """Stands in for questionary: records each select() and returns scripted picks."""

    def __init__(self, picks):
        self.picks, self.calls = list(picks), []

    @staticmethod
    def Choice(title, value, disabled=None):
        return types.SimpleNamespace(title=title, value=value, disabled=disabled)

    def select(self, message, choices, default, **kwargs):
        self.calls.append(types.SimpleNamespace(message=message, choices=choices, default=default, kwargs=kwargs))
        pick = self.picks.pop(0) if self.picks else default.value  # no script = press Enter
        return types.SimpleNamespace(unsafe_ask=lambda: pick)


def _bowler_args(lineup):
    ranking = m.get_bowler_ranking(lineup)
    allowed = [p for p in lineup if p.name != "J Bumrah"]  # Bumrah bowled the last over
    left = {p.name: 4 for p in lineup}
    left["J Bumrah"] = 2
    return ranking, allowed, ranking["C"], left


def test_bowler_menu_offers_ratings_overs_and_greys_out_unavailable():
    lineup = get_teams()[TEAM]
    ranking, allowed, default, left = _bowler_args(lineup)
    menu = FakeMenu([])
    cap = LiveCaptain(menu=menu)

    assert cap.choose_bowler(TEAM, 6, ranking, allowed, default, left, "MI 50/1") is default

    call = menu.calls[0]
    titles = [c.title for c in call.choices]
    assert call.kwargs["erase_when_done"] is True
    assert "Over 7 | MI 50/1" in call.message
    assert call.default.title.startswith("D Chahar") and "<- default" in call.default.title
    bumrah = next(c for c in call.choices if c.title.startswith("J Bumrah"))
    assert bumrah.disabled == "bowled last over, 2 left"
    assert any("bowling  8.5  4 overs left" in t for t in titles)  # Boult: rating + overs
    assert not any(t.startswith("S Rohit") for t in titles)        # rated under 5: hidden
    assert titles[-1].startswith(">> auto")


def test_menu_picks_and_auto():
    lineup = get_teams()[TEAM]
    ranking, allowed, default, left = _bowler_args(lineup)

    menu = FakeMenu([1])  # second entry = T Boult
    assert LiveCaptain(menu=menu).choose_bowler(TEAM, 0, ranking, allowed, default, left, "").name == "T Boult"

    cap = LiveCaptain(menu=FakeMenu([AUTO]))
    assert cap.choose_bowler(TEAM, 0, ranking, allowed, default, left, "") is default
    assert cap.auto  # rest of the innings is automatic: no more menus
    assert cap.choose_next_batter(TEAM, lineup, [2, 3], "") == 2

    menu = FakeMenu([10, 8])  # opener 1 = #11; opener 2 = index 8 in the remaining list (#9)
    assert LiveCaptain(menu=menu).choose_openers(TEAM, lineup) == (10, 8)
    assert "opener 1: J Bumrah" in menu.calls[1].message
    assert "batting  1.0" in menu.calls[0].choices[10].title

    menu = FakeMenu([1])  # picks are menu positions: position 1 = candidate 4
    assert LiveCaptain(menu=menu).choose_next_batter(TEAM, lineup, [3, 4, 5, 6], "out") == 4
    assert "WICKET!" in menu.calls[0].message and "<- default" in menu.calls[0].default.title

    assert LiveCaptain(menu=FakeMenu([1])).choose_toss(TEAM) == "BOWL"
    assert LiveCaptain(menu=FakeMenu([2])).choose_toss(TEAM) is None  # random
    assert not any(c.title.startswith(">> auto") for c in FakeMenu([]).calls)


def test_match_with_menus_keeping_defaults_matches_automatic_play():
    teams = get_teams()
    random.seed(4)
    auto = m.simulate_innings(teams["MI"], teams["CSK"], team_name="MI", bowling_team_name="CSK")
    teams = get_teams()
    random.seed(4)
    live = m.simulate_innings(teams["MI"], teams["CSK"], team_name="MI", bowling_team_name="CSK",
                              captain=LiveCaptain(menu=FakeMenu([])))
    assert live == auto


# ----- real questionary, simulated key presses -------------------------------
questionary = pytest.importorskip("questionary")
from prompt_toolkit.input import create_pipe_input  # noqa: E402
from prompt_toolkit.output import DummyOutput  # noqa: E402


def _keyboard_menu(pipe):
    """questionary, but reading keys from `pipe` and drawing nowhere."""
    def select(*args, **kwargs):
        return questionary.select(*args, input=pipe, output=DummyOutput(), **kwargs)
    return types.SimpleNamespace(Choice=questionary.Choice, select=select)


def test_real_menu_enter_keeps_default_and_arrows_skip_disabled():
    lineup = get_teams()[TEAM]
    ranking, allowed, default, left = _bowler_args(lineup)

    with create_pipe_input() as pipe:
        cap = LiveCaptain(menu=_keyboard_menu(pipe))
        pipe.send_text(ENTER)
        assert cap.choose_bowler(TEAM, 0, ranking, allowed, default, left, "") is default

    with create_pipe_input() as pipe:  # default is #3 D Chahar; down once = #4 A Ghazanfar
        cap = LiveCaptain(menu=_keyboard_menu(pipe))
        pipe.send_text(DOWN + ENTER)
        assert cap.choose_bowler(TEAM, 0, ranking, allowed, default, left, "").name == "A Ghazanfar"

    # default = Boult (#2); Bumrah (#1, disabled) is above it. Up from Boult wraps past
    # Bumrah to the auto item at the bottom, so the disabled bowler can't be picked.
    with create_pipe_input() as pipe:
        cap = LiveCaptain(menu=_keyboard_menu(pipe))
        pipe.send_text("\x1b[A" + ENTER)
        assert cap.choose_bowler(TEAM, 0, ranking, allowed, ranking["B"], left, "") is ranking["B"]
        assert cap.auto
