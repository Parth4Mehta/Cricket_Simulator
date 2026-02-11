# CricSim - Cricket League Simulator

A Python-based cricket league simulator that uses player statistics to simulate realistic T20 matches and full league seasons with playoffs.

**⚡ Quick Start:** `python main.py` (Python 3.7+ only, no dependencies!)

**→ [See QUICKSTART.md for 2-minute setup guide](QUICKSTART.md)**

## Features

✨ **Dynamic Match Simulation**
- Ball-by-ball cricket simulation based on player batting/bowling statistics
- Realistic game mechanics with configurable difficulty levels
- Support for individual match viewing or full league simulation

🏆 **League Management**
- Double round-robin league format (each team plays every other team twice)
- Automatic points table generation with NRR calculations
- Full playoff system (Qualifier 1, Eliminator, Qualifier 2, Final)
- Team selection - choose which teams compete in the league

⚙️ **Customization**
- Three difficulty profiles: Conservative, Balanced, Aggressive
- Configurable game coefficients via `config.json`
- Playoff format adapts to number of teams (2, 3, or 4+ teams)

📊 **Statistics Tracking**
- Player statistics (runs, wickets, strike rates, economy)
- Team statistics (wins, losses, points, NRR)
- Orange Cap (top run-scorer) and Purple Cap (top wicket-taker) tracking
- Persistent database across sessions

## Installation

### Prerequisites
- **Python 3.7 or higher**
- pip (Python package manager)

Check your Python version:
```bash
python --version
# or
python3 --version
```

### Option 1: Simple Installation (Recommended for Users)

```bash
git clone <repository-url>
cd CricSim
python main.py
```

That's it! Core functionality works with Python standard library only.

### Option 2: With Enhanced Console Output

For prettier tables and colored output, install optional dependencies:

```bash
pip install -r requirements.txt
python main.py
```

Or install with extras:
```bash
pip install -e ".[rich]"
```

### Option 3: Development Installation

For contributors:
```bash
git clone <repository-url>
cd CricSim
pip install -e ".[dev,rich]"
```

## Dependencies

**Required:** None! Only uses Python standard library.

**Optional:**
- `rich>=10.0.0` - For beautiful formatted console tables (automatic fallback to plain text if not installed)

| Feature | With Rich | Without Rich |
|---------|-----------|--------------|
| Functionality | ✅ Full | ✅ Full |
| Tables | Beautiful colored tables | Plain text tables |
| Performance | No difference | No difference |
## Compatibility

✅ Python 3.7, 3.8, 3.9, 3.10, 3.11+  
✅ Windows, macOS, Linux  
✅ No version clashes - uses only Python standard library by default  
✅ Optional `rich` library won't conflict with other projects
## Usage

### Quick Start

```bash
python main.py
```

This launches an interactive menu where you can:
1. Simulate a full league season
2. Simulate individual matches
3. View player and team statistics
4. Clear the database
5. Configure game difficulty

### Direct Usage

Simulate a league with team selection:
```bash
python league_simulator.py
```

Simulate a single match:
```bash
python match_simulator.py
```

## Configuration

Edit `config.json` to customize game difficulty:

```json
{
  "difficulty_profiles": {
    "balanced": {
      "four_coeff": 0.02,
      "six_coeff": 0.01,
      "wicket_coeff": 0.013,
      ...
    }
  }
}
```

- **four_coeff**: Probability multiplier for hitting fours
- **six_coeff**: Probability multiplier for hitting sixes
- **wicket_coeff**: Probability multiplier for getting out
- **dot_ball_coeff**: Probability of scoring no runs

## Project Structure

```
CricSim/
├── main.py                 # Entry point with interactive menu
├── match_simulator.py      # Core match simulation engine
├── league_simulator.py     # League and playoff management
├── teams.py               # Team and player definitions
├── database.py            # Statistics persistence
├── config.py              # Configuration management
├── config.json            # Difficulty profiles & settings
├── .gitignore
└── database/              # Generated statistics files
    ├── player_stats.json
    ├── team_stats.json
    └── match_stats/       # Individual match records
```

## Teams

Default teams (8 IPL teams):
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

Easily extend by adding teams to `teams.py`.

## Game Mechanics

**Match Simulation:**
- 20 overs per innings (120 balls)
- Strike rotation on odd runs
- Best 5 bowlers rotate in the second innings
- Enhanced entertainment factor in final 4 overs (more boundaries & wickets)

**Points System:**
- Win: 2 points
- Loss: 0 points
- Tie: 1 point each

**Player Ratings (0-10 scale):**
- Batting: Player's ability to score runs and hit boundaries
- Bowling: Player's ability to take wickets and defend runs

## Example Workflow

```
$ python main.py

=== MAIN MENU ===
1. Simulate a League
2. Simulate a Match
...

Select an option: 1

=== Team Selection ===
[Shows all teams]

Select teams or 'all': all

=== Choose Game Difficulty ===
1. Conservative
2. Balanced (Default)
3. Aggressive

Select: 2

[League simulation begins with 90 matches total]
```

## Development

To add new features or teams:

1. **New teams**: Edit `teams.py` and add Team class
2. **New difficulty profiles**: Edit `config.json`
3. **Game logic changes**: Modify `match_simulator.py` (be careful!)

## Database

Statistics are stored in `database/` directory:
- `player_stats.json`: Cumulative player statistics
- `team_stats.json`: Team standings and performance
- `match_stats/`: Individual match records with detailed statistics

Clear with `main.py` menu option 4 or directly delete the `database/` directory.

## License

[Your License Here]

## Contributing

Contributions are welcome! Please ensure:
- Game logic remains balanced
- Code follows PEP 8 style guide
- New features include documentation
