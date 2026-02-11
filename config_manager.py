"""
config.py

Load and manage game configuration including difficulty profiles.
"""
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def load_config():
    """Load configuration from config.json"""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"config.json not found at {CONFIG_FILE}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in config.json")


def get_profile(profile_name):
    """Get a difficulty profile by name"""
    config = load_config()
    profiles = config.get("difficulty_profiles", {})
    
    if profile_name not in profiles:
        raise ValueError(f"Profile '{profile_name}' not found. Available: {list(profiles.keys())}")
    
    return profiles[profile_name]


def get_default_profile():
    """Get the default difficulty profile"""
    config = load_config()
    default = config.get("default_profile", "balanced")
    return get_profile(default)


def list_profiles():
    """List all available difficulty profiles"""
    config = load_config()
    profiles = config.get("difficulty_profiles", {})
    return {name: profile.get("label", name) for name, profile in profiles.items()}


def get_game_settings():
    """Get general game settings"""
    config = load_config()
    return config.get("game_settings", {})
