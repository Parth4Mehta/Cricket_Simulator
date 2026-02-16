"""
Fixtures package - Contains different tournament format implementations.
Each module represents a different tournament structure (format).
"""

from .double_round_robin_playoff import simulate_double_round_robin_playoff

# Available tournament formats
TOURNAMENT_FORMATS = {
    "1": {
        "name": "Double Round-Robin + Playoffs",
        "description": "Each team plays every other team twice (home & away), followed by playoffs",
        "function": simulate_double_round_robin_playoff,
    },
    # Future formats will be added here:
    # "2": {
    #     "name": "Group Stage + Playoffs",
    #     "description": "Teams divided into groups, followed by cross-over playoffs",
    #     "function": simulate_group_stage_playoff,
    # },
    # "3": {
    #     "name": "Single Elimination",
    #     "description": "Direct knockout tournament - one loss and you're out",
    #     "function": simulate_knockout,
    # },
}


def get_available_formats():
    """Return list of available tournament formats."""
    return TOURNAMENT_FORMATS


def get_format_function(format_id):
    """Get the simulator function for a specific format."""
    if format_id not in TOURNAMENT_FORMATS:
        raise ValueError(f"Unknown format: {format_id}")
    return TOURNAMENT_FORMATS[format_id]["function"]
