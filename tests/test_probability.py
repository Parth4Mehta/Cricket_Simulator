import pytest

import probability
from config_manager import get_bowler_fatigue_settings, get_profile, list_profiles
from match_simulator import generate_bowling_order
from probability import (
    calculate_ball_probabilities,
    calculate_effective_bowling,
    determine_ball_outcome,
)
from teams import BOWLING_ORDERS, get_teams

COEFF_KEYS = ("four_coeff", "six_coeff", "wicket_coeff", "dot_ball_coeff",
              "batsman_four_boost", "batsman_six_boost", "bowler_wicket_boost")


def _coeffs(profile_name):
    p = get_profile(profile_name)
    return tuple(p[k] for k in COEFF_KEYS)


@pytest.fixture
def coeffs():
    return _coeffs("balanced")


def _real_extremes():
    """Strongest/weakest batter in any squad, and the effective-bowling range
    of bowlers who actually get overs (fresh vs. 3 overs of fatigue)."""
    teams = get_teams()
    fatigue = get_bowler_fatigue_settings()
    bats = [p.batting for t in teams.values() for p in t]
    used = [b.bowling for code, t in teams.items()
            for b in generate_bowling_order(t, BOWLING_ORDERS.get(code))]
    up, rate = fatigue.get("up_value", 0.3), fatigue.get("fatigue_rate", 0.2)
    return (min(bats), max(bats),
            min(used) + up - rate * 3, max(used) + up)


@pytest.mark.parametrize("profile", list(list_profiles()))
def test_every_profile_has_all_coefficients(profile):
    p = get_profile(profile)
    assert all(isinstance(p.get(k), (int, float)) for k in COEFF_KEYS), profile


@pytest.mark.parametrize("profile", list(list_profiles()))
def test_probabilities_valid_for_real_players(profile):
    """Every profile must give valid probabilities for every real batter/bowler
    pairing. Fails if a rating change pushes e.g. wicket chance below zero."""
    lo_bat, hi_bat, lo_bowl, hi_bowl = _real_extremes()
    coeffs = _coeffs(profile)
    for bat in (lo_bat, hi_bat):
        for bowl in (lo_bowl, hi_bowl):
            for over in (0, 19):
                probs = calculate_ball_probabilities(bat, bowl, over, 20, coeffs)
                assert all(0 <= p <= 1 for p in probs), (profile, bat, bowl, over, probs)
                assert sum(probs) < 1, (profile, bat, bowl, over, probs)


def test_probabilities_move_in_the_right_direction(coeffs):
    weak_bat = calculate_ball_probabilities(2, 5, 5, 20, coeffs)
    strong_bat = calculate_ball_probabilities(9, 5, 5, 20, coeffs)
    assert strong_bat[0] > weak_bat[0]  # more fours
    assert strong_bat[2] < weak_bat[2]  # fewer wickets

    weak_bowl = calculate_ball_probabilities(5, 2, 5, 20, coeffs)
    strong_bowl = calculate_ball_probabilities(5, 9, 5, 20, coeffs)
    assert strong_bowl[2] > weak_bowl[2]  # more wickets

    early = calculate_ball_probabilities(7, 5, 0, 20, coeffs)
    death = calculate_ball_probabilities(7, 5, 19, 20, coeffs)
    assert death[1] > early[1]  # more sixes at the death


def test_fatigue_reduces_effective_bowling():
    fresh = calculate_effective_bowling(8, 0.3, 0.2, 0)
    tired = calculate_effective_bowling(8, 0.3, 0.2, 3)
    assert tired < fresh


@pytest.mark.parametrize("roll, expected", [
    (0.05, "wicket"),  # < pw
    (0.15, "six"),     # < pw + p6
    (0.25, "four"),    # < pw + p6 + p4
    (0.45, "dot"),     # < pw + p6 + p4 + pdot
    (0.90, "runs"),
])
def test_determine_ball_outcome_thresholds(monkeypatch, roll, expected):
    monkeypatch.setattr(probability.random, "random", lambda: roll)
    outcome, runs = determine_ball_outcome(p4=0.1, p6=0.1, pw=0.1, pdot=0.3)
    assert outcome == expected
    assert runs == {"wicket": 0, "six": 6, "four": 4, "dot": 0}.get(outcome, runs)
    if outcome == "runs":
        assert runs in (1, 2, 3)
