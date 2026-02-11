# CricSim - Cricket League Simulator

A Python-based cricket league simulator that uses player statistics to simulate realistic T20 matches and full league seasons with playoffs.

**⚡ Run it now:** `python main.py` (Python 3.7+, no dependencies required!)

---

## Table of Contents
1. [Overview & Features](#overview--features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Project Structure](#project-structure)
6. [**QUICKSTART** (2-Minute Setup)](#-quickstart--2-minute-setup)
7. [**CONTRIBUTING** (Developer Guide)](#-contributing--developer-guide)

---

## Overview & Features

✨ **Dynamic Match Simulation**
- Ball-by-ball cricket simulation based on player batting/bowling statistics
- Realistic game mechanics with 4 configurable difficulty levels
- Support for individual match viewing or full league simulation

🏆 **League Management**
- Double round-robin format (each team plays every other team twice)
- Automatic points table with NRR calculations
- Full playoff system (Qualifier 1, Eliminator, Qualifier 2, Final)
- Team selection - choose which teams compete
- Playoff format auto-adapts (2, 3, or 4+ teams)

⚙️ **Customization**
- Four difficulty profiles: Conservative, Balanced, Aggressive, Advanced (Custom)
- Advanced Controls: Tweak individual game coefficients interactively
- Auto-reset to Balanced after league (advanced settings don't persist)

📊 **Statistics Tracking**
- Player stats: runs, wickets, strike rates, economy, batting average, out/not out
- Team stats: wins, losses, points, NRR
- Orange Cap (top run-scorer) and Purple Cap (top wicket-taker)
- Batting averages with min 300 runs threshold and accurate out/not out tracking
- Persistent database across sessions
- Top players summary across 15+ statistical categories

---

## Installation

### Prerequisites
- **Python 3.7 or higher**
- No other dependencies needed! (Rich library optional for prettier output)

Check version:
```bash
python --version
```

### Simple Installation (Recommended)

```bash
git clone <repository-url>
cd CricSim
python main.py
```

That's it! Works with Python standard library only.

### Optional: Enhanced Console Output

For beautiful colored tables:
```bash
pip install -r requirements.txt
python main.py
```

The app automatically uses Rich if available, falls back to plain text otherwise.

### Compatibility

✅ Python 3.7, 3.8, 3.9, 3.10, 3.11+  
✅ Windows, macOS, Linux  
✅ No version conflicts - standard library only by default  
✅ Optional Rich library won't interfere with other projects

---

## Usage

### Main Menu

```bash
python main.py
```

Interactive menu options:
1. **Simulate a League** - Full season with selected teams
2. **Simulate a Single Match** - Pick two teams and watch
3. **View Current Stats** - Points table & player stats
4. **View Full Player Stats** - Top players across all categories
5. **Clear Database & Start Fresh** - Reset all statistics
6. **Configure Game Difficulty** - Choose: Conservative, Balanced, Aggressive, or Advanced
7. **Exit**

### Direct Access

```bash
python league_simulator.py    # League with team selection
python match_simulator.py     # Single match direct
python top_players.py         # Show top players stats
```

## Configuration

Edit `config.json` to customize game difficulty:

```json
{
  "difficulty_profiles": {
    "balanced": {
      "four_coeff": 0.02,        // Probability of hitting 4
      "six_coeff": 0.01,         // Probability of hitting 6
      "wicket_coeff": 0.013,     // Probability of getting out
      "dot_ball_coeff": 0.45,    // Probability of dot ball
      "batsman_six_boost": 0.008,
      "batsman_four_boost": 0.016,
      "bowler_wicket_boost": 0.006
    }
  }
}
```

### Available Profiles

| Profile | Description |
|---------|-------------|
| Conservative | Fewer boundaries & wickets, defensive gameplay |
| Balanced | Default, well-rounded gameplay |
| Aggressive | More boundaries, offensive gameplay |
| Advanced | Custom coefficients (interactive tweaking) |

### Advanced Controls

Select "Advanced Controls" during difficulty configuration to interactively adjust all 7 coefficients:
- Shows default (Balanced) value for reference
- Shows current value
- Provides hints for each coefficient
- Updates are saved and used during league play
- **Automatically reset to Balanced after league ends**

---

## Project Structure

```
CricSim/
├── main.py                    # Entry point - interactive menu
├── match_simulator.py         # Core match simulation engine
├── league_simulator.py        # League & playoff management
├── teams.py                   # Team & player definitions
├── database.py                # Statistics persistence
├── config_manager.py          # Configuration management
├── config.json                # Difficulty profiles & settings
├── top_players.py             # Player statistics analysis
├── LICENSE
├── README.md                  # This file
├── requirements.txt           # Optional dependencies
├── .gitignore
└── database/                  # Generated (ignored in git)
    ├── player_stats.json
    ├── team_stats.json
    └── match_stats/           # Individual match records
```

---

## Teams

Default 10 IPL teams:
- Mumbai Indians (MI)
- Chennai Super Kings (CSK)
- Sunrisers Hyderabad (SRH)
- Royal Challengers Bangalore (RCB)
- Rajasthan Royals (RR)
- Punjab Kings (PBKS)
- Lucknow Super Giants (LSG)
- Gujarat Titans (GT)
- Delhi Capitals (DC)
- Kolkata Knight Riders (KKR)

Extend by editing `teams.py`.

---

## Game Mechanics

**Match Format:**
- 20 overs per innings (120 balls)
- Strike rotation on odd runs
- Best 5 bowlers rotate in second innings
- Enhanced entertainment in final 4 overs (more boundaries & wickets)

**Points System:**
- Win: 2 points
- Tie: 1 point each
- Loss: 0 points

**Player Ratings (0-10 scale):**
- Batting: Ability to score runs and hit boundaries
- Bowling: Ability to take wickets and defend

**Statistics Tracked:**
- Runs, balls faced, 4s, 6s, strike rate, highest score
- Out/Not Out (for accurate batting averages)
- Wickets, bowling figures, economy, bowling average
- Best bowling performance, best economy

---

## Database

Statistics are stored in `database/` directory:
- `player_stats.json`: Cumulative player statistics
- `team_stats.json`: Team standings and performance  
- `match_stats/`: Individual match records with detailed statistics

Clear with menu option 5 or directly delete the `database/` directory.

---

---

# 👨‍💻 CONTRIBUTING (Developer Guide)

Thanks for interest in contributing! Follow this guide to set up your dev environment.

## Development Setup

### 1. Clone & Create Virtual Environment

```bash
git clone <repository-url>
cd CricSim
python -m venv venv

# Activate venv:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -e ".[dev,rich]"
```

### 2. Code Style

We follow **PEP 8**. Format code with black:

```bash
black *.py
```

Verify with flake8:
```bash
flake8 *.py
```

### 3. Testing

Run interactive tests:
```bash
python main.py    # Test all functionality
```

### 4. Making Changes

⚠️ **Important Guidelines:**

- **Core logic** (`match_simulator.py`): Be careful with probability calculations
- **Game balance**: Use `config.json` to adjust difficulty, not hardcoded values
- **Backwards compatibility**: Don't break existing functionality
- **Database format**: Keep player_stats.json schema consistent

### 5. Areas for Contribution

- ✅ New teams in `teams.py`
- ✅ New difficulty profiles in `config.json`
- ✅ Enhanced statistics in `top_players.py`
- ✅ Documentation improvements
- ✅ Bug fixes with detailed reports
- ✅ Performance optimizations
- ✅ UI/UX enhancements

### 6. Code Guidelines

- Keep functions focused (<50 lines when possible)
- Add docstrings to new functions
- Handle exceptions gracefully
- Test manually: `python main.py`
- Update README if adding features

### 7. Submitting Changes

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python main.py

# Commit with clear message
git commit -am "Add feature: Description of what you added"

# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### PR Checklist

- [ ] Code follows PEP 8
- [ ] Changes tested with `python main.py`
- [ ] No breaking changes to existing functionality
- [ ] Database schema not altered
- [ ] README updated if relevant
- [ ] Clear commit message

## Questions?

Open a GitHub issue for discussions or questions!

---

## License

[Your License Here]

## Summary

- **Easy to use**: No setup, just `python main.py`
- **Highly customizable**: 4 difficulty levels + advanced controls
- **Well-documented**: Code is commented, README is comprehensive
- **Extensible**: Add teams, profiles, and statistics easily
- **Contribution-friendly**: Clear guidelines and areas for contribution

Enjoy CricSim! 🏏
