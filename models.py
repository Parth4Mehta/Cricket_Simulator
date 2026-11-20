from dataclasses import dataclass

ROLES = ("bat", "bowl", "ar")
STYLES = ("pace", "spin")


@dataclass
class Player:
    name: str
    batting: float
    bowling: float
    role: str  # "bat", "bowl" or "ar" (all-rounder)
    style: str  # bowling style: "pace" or "spin" (part-time style for batters)
