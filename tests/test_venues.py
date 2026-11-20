import random

import pytest

import match_simulator as m
from config_manager import get_game_settings, get_pitch_settings
from probability import pitch_bowling_bonus
from teams import get_player, get_teams
from venues import HOME_VENUES, VENUES, get_home_venue, get_pitch, random_venue

PITCH_TYPES = {"flat", "green", "turning", "balanced"}
PITCH_KEYS = {"boundary_mult", "wicket_mult", "pace_bonus", "spin_bonus"}
TEAMS = get_teams()


def test_every_team_has_a_home_ground():
    assert set(HOME_VENUES) == set(TEAMS)
    assert set(HOME_VENUES.values()) <= set(VENUES)


def test_every_venue_has_a_configured_pitch():
    pitches = get_game_settings()["pitches"]
    assert set(pitches) == PITCH_TYPES
    assert set(VENUES.values()) <= PITCH_TYPES
    for name, settings in pitches.items():
        assert PITCH_KEYS <= set(settings), name


def test_lookups():
    assert get_pitch(get_home_venue("CSK")) == "turning"
    assert random_venue() in VENUES
    assert get_pitch_settings("not-a-pitch") == {k: (1.0 if "mult" in k else 0.0) for k in PITCH_KEYS}
    turning = get_pitch_settings("turning")
    assert pitch_bowling_bonus("spin", turning) > 0 > pitch_bowling_bonus("pace", turning)
    assert pitch_bowling_bonus("spin", None) == 0


def _innings_on(pitch_type, n=80):
    """Same seeds and matchups on each pitch, so only the pitch differs."""
    pitch = get_pitch_settings(pitch_type)
    codes = list(TEAMS)
    runs, wickets = 0, {"pace": 0, "spin": 0}
    for i in range(n):
        bat, bowl = random.Random(i).sample(codes, 2)
        random.seed(i)
        score, _, _, bowling, _ = m.simulate_innings(
            TEAMS[bat], TEAMS[bowl], team_name=bat, bowling_team_name=bowl, pitch=pitch)
        runs += score
        for name, s in bowling.items():
            wickets[get_player(name).style] += s["wickets"]
    return runs, wickets


def test_pitches_shift_results_the_right_way():
    base_runs, base_wk = _innings_on("balanced")
    flat_runs, _ = _innings_on("flat")
    _, green_wk = _innings_on("green")
    _, turning_wk = _innings_on("turning")

    assert flat_runs > base_runs
    assert green_wk["pace"] > base_wk["pace"] and green_wk["spin"] < base_wk["spin"]
    assert turning_wk["spin"] > base_wk["spin"] and turning_wk["pace"] < base_wk["pace"]


def test_match_records_venue_and_pitch(rows):
    m.simulate_match("MI", "CSK", venue=get_home_venue("CSK"))
    m.simulate_match("MI", "CSK")  # neutral: random ground
    (home, neutral) = rows("SELECT venue, pitch FROM matches ORDER BY match_id")
    assert tuple(home) == ("MA Chidambaram Stadium, Chennai", "turning")
    assert neutral["venue"] in VENUES and neutral["pitch"] == VENUES[neutral["venue"]]


def test_match_header_shows_venue(capsys):
    m.simulate_match("MI", "CSK", venue=get_home_venue("MI"))
    assert "Wankhede Stadium, Mumbai" in capsys.readouterr().out
