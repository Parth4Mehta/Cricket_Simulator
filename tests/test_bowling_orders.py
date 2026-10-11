from collections import Counter

import pytest

from teams import BOWLING_ORDERS


@pytest.mark.parametrize("team_name, bowling_order", BOWLING_ORDERS.items())
def test_bowling_order_respects_over_limits(team_name, bowling_order):
    assert len(bowling_order) == 20, team_name
    assert set(bowling_order) <= set("ABCDEFGHIJK"), team_name
    assert all(count <= 4 for count in Counter(bowling_order).values()), team_name