"""Every module must import, and the interactive entry points must run.

The other tests call the simulation directly, so a broken menu (e.g. a syntax
error in main.py) would otherwise slip through.
"""
import builtins
import importlib
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODULES = sorted(
    {p.stem for p in ROOT.glob("*.py") if p.stem != "setup"}
    | {f"{pkg}.{p.stem}" for pkg in ("db", "fixtures") for p in (ROOT / pkg).glob("*.py") if p.stem != "__init__"}
)


@pytest.mark.parametrize("module", MODULES)
def test_module_imports(module):
    importlib.import_module(module)


def _answers(monkeypatch, answers):
    it = iter(answers)
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(it, ""))


def test_single_match_menu_plays_a_match(monkeypatch, rows):
    import main
    from teams import get_teams
    from venues import get_home_venue

    first, second = list(get_teams())[:2]
    # team 1, team 2, ball-by-ball no, venue = team 1's home, live choices no
    _answers(monkeypatch, ["1", "2", "n", "1", "n"])
    main.menu_simulate_match()

    played = rows("SELECT team_a, team_b, venue FROM matches")
    assert [tuple(r) for r in played] == [(first, second, get_home_venue(first))]


def test_league_menu_runs_a_league(monkeypatch, rows):
    import league_simulator

    # league ball-by-ball no, playoff ball-by-ball no, live choices no, archive no
    _answers(monkeypatch, ["n", "n", "n", "n"])
    champion = league_simulator.simulate_league(format_id="1", selected_teams=["MI", "CSK", "RCB"])

    assert champion in ("MI", "CSK", "RCB")
    assert rows("SELECT COUNT(*) FROM matches")[0][0] == 6 + 2  # 3x2 league games + eliminator + final
