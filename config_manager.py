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


def save_config(config):
    """Save configuration to config.json"""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        raise Exception(f"Failed to save config.json: {e}")


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


def update_advanced_profile(coefficients):
    """Update the advanced profile with custom coefficients"""
    config = load_config()
    if "advanced" not in config.get("difficulty_profiles", {}):
        raise ValueError("Advanced profile not found in config")
    
    config["difficulty_profiles"]["advanced"].update(coefficients)
    save_config(config)


def reset_advanced_profile():
    """Reset advanced profile to balanced defaults"""
    config = load_config()
    balanced = config.get("difficulty_profiles", {}).get("balanced", {})
    
    if "advanced" not in config.get("difficulty_profiles", {}):
        raise ValueError("Advanced profile not found in config")
    
    # Copy balanced profile coefficients to advanced
    coeff_keys = ["four_coeff", "six_coeff", "wicket_coeff", "dot_ball_coeff", 
                  "batsman_six_boost", "batsman_four_boost", "bowler_wicket_boost"]
    
    for key in coeff_keys:
        if key in balanced:
            config["difficulty_profiles"]["advanced"][key] = balanced[key]
    
    save_config(config)
    return config.get("game_settings", {})


def get_bowler_fatigue_settings():
    """Get bowler fatigue settings from game_settings"""
    settings = get_game_settings()
    return settings.get("bowler_fatigue", {"up_value": 0.3, "fatigue_rate": 0.2})
