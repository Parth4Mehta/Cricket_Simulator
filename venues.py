"""
venues.py

Real grounds and their usual T20 pitch type, plus each team's home ground.

Pitch types (effects live in config.json -> game_settings.pitches):
  flat     - batting-friendly: more boundaries, fewer wickets
  green    - helps pace bowlers
  turning  - helps spin bowlers
  balanced - no adjustment
"""
import random

VENUES = {
    "Wankhede Stadium, Mumbai": "flat",
    "M. Chinnaswamy Stadium, Bengaluru": "flat",
    "Rajiv Gandhi Intl. Stadium, Hyderabad": "flat",
    "Arun Jaitley Stadium, Delhi": "flat",
    "Saurashtra Cricket Association Stadium, Rajkot": "flat",
    "Eden Park, Auckland": "flat",
    "Gaddafi Stadium, Lahore": "flat",
    "Grand Prairie Stadium, Dallas": "flat",
    "MA Chidambaram Stadium, Chennai": "turning",
    "Ekana Cricket Stadium, Lucknow": "turning",
    "Feroz Shah Kotla, Delhi": "turning",
    "Sharjah Cricket Stadium": "turning",
    "Shere Bangla National Stadium, Mirpur": "turning",
    "Tribhuvan University Ground, Kirtipur": "turning",
    "Al Amerat Cricket Ground, Muscat": "turning",
    "R. Premadasa Stadium, Colombo": "turning",
    "Maharaja Yadavindra Singh Stadium, Mullanpur": "green",
    "PCA Stadium, Mohali": "green",
    "Perth Stadium": "green",
    "Lord's, London": "green",
    "Malahide Cricket Club Ground, Dublin": "green",
    "VRA Cricket Ground, Amstelveen": "green",
    "The Grange, Edinburgh": "green",
    "The Wanderers Stadium, Johannesburg": "green",
    "Sawai Mansingh Stadium, Jaipur": "balanced",
    "Eden Gardens, Kolkata": "balanced",
    "Narendra Modi Stadium, Ahmedabad": "balanced",
    "MCA Stadium, Pune": "balanced",
    "Maple Leaf Cricket Club, King City": "balanced",
    "Wanderers Cricket Ground, Windhoek": "balanced",
    "Amini Park, Port Moresby": "balanced",
    "Lugogo Cricket Oval, Kampala": "balanced",
    "Kensington Oval, Barbados": "balanced",
}

HOME_VENUES = {
    "MI": "Wankhede Stadium, Mumbai",
    "CSK": "MA Chidambaram Stadium, Chennai",
    "SRH": "Rajiv Gandhi Intl. Stadium, Hyderabad",
    "RCB": "M. Chinnaswamy Stadium, Bengaluru",
    "RR": "Sawai Mansingh Stadium, Jaipur",
    "PBKS": "Maharaja Yadavindra Singh Stadium, Mullanpur",
    "LSG": "Ekana Cricket Stadium, Lucknow",
    "KKR": "Eden Gardens, Kolkata",
    "GT": "Narendra Modi Stadium, Ahmedabad",
    "DC": "Arun Jaitley Stadium, Delhi",
    "MI16": "Wankhede Stadium, Mumbai",
    "RCB16": "M. Chinnaswamy Stadium, Bengaluru",
    "SRH16": "Rajiv Gandhi Intl. Stadium, Hyderabad",
    "KKR16": "Eden Gardens, Kolkata",
    "DD16": "Feroz Shah Kotla, Delhi",
    "KXIP16": "PCA Stadium, Mohali",
    "GL16": "Saurashtra Cricket Association Stadium, Rajkot",
    "RPS16": "MCA Stadium, Pune",
    "AFG": "Sharjah Cricket Stadium",
    "AUS": "Perth Stadium",
    "BAN": "Shere Bangla National Stadium, Mirpur",
    "CAN": "Maple Leaf Cricket Club, King City",
    "ENG": "Lord's, London",
    "IND": "Narendra Modi Stadium, Ahmedabad",
    "IRE": "Malahide Cricket Club Ground, Dublin",
    "NAM": "Wanderers Cricket Ground, Windhoek",
    "NEP": "Tribhuvan University Ground, Kirtipur",
    "NED": "VRA Cricket Ground, Amstelveen",
    "NZL": "Eden Park, Auckland",
    "OMN": "Al Amerat Cricket Ground, Muscat",
    "PAK": "Gaddafi Stadium, Lahore",
    "PNG": "Amini Park, Port Moresby",
    "SCO": "The Grange, Edinburgh",
    "RSA": "The Wanderers Stadium, Johannesburg",
    "SRL": "R. Premadasa Stadium, Colombo",
    "UGA": "Lugogo Cricket Oval, Kampala",
    "USA": "Grand Prairie Stadium, Dallas",
    "WI": "Kensington Oval, Barbados",
}


def get_home_venue(team_name):
    """Home ground of a team, or None if it has none."""
    return HOME_VENUES.get(team_name)


def random_venue():
    """A random ground, used for neutral matches (World Cup stages, knockouts)."""
    return random.choice(sorted(VENUES))


def get_pitch(venue):
    """Pitch type of a ground: flat, green, turning or balanced."""
    return VENUES[venue]
