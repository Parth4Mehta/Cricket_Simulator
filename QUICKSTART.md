# Quick Start Guide

Get CricSim running in 2 minutes!

## Step 1: Clone Repository
```bash
git clone <repository-url>
cd CricSim
```

## Step 2: Run (No Installation Required!)
```bash
python main.py
```

That's it! 🎉

## First Run

You'll see:
```
======================================================================
       🏏 CRICSIM - Cricket League Simulator 🏏
======================================================================

Welcome to CricSim!
Load default difficulty (Balanced)...
Loaded profile: Balanced

=== MAIN MENU ===
1. Simulate a League (Double Round-Robin + Playoffs)
2. Simulate a Single Match
3. View Current Stats
4. Clear Database & Start Fresh
5. Configure Game Difficulty
6. Exit

Select an option (1-6):
```

## Try These

### Option 1: Quick Single Match
```
Select: 2
[Picks two teams and simulates a match]
```

### Option 2: Create a Full League
```
Select: 1
[Pick 4-8 teams]
[Simulates 24-56 matches + playoffs automatically]
```

### Option 3: Change Difficulty
```
Select: 5
[Choose: Conservative, Balanced, or Aggressive]
```

## Optional: Enhanced Output

For prettier console tables:
```bash
pip install rich
```

Then run normally - output will auto-upgrade to colored tables!

## Troubleshooting

**"ModuleNotFoundError"**
- Make sure you're in the `CricSim` directory: `cd CricSim`
- Python 3.7+: `python --version`

**"No module named 'rich'"**
- Not required! Install if you want: `pip install rich`
- Works fine without it (plain text output)

**"Port already in use"** (or similar network error)
- CricSim doesn't use network - this shouldn't happen
- Check if another Python process is running

**Stats not showing**
- Run a match or league first: `Select: 1` or `2`
- Stats populate after matches are played

## Next Steps

- **Customize Difficulty**: Edit `config.json`
- **Add Teams**: Edit `teams.py` and add a new team
- **View Code**: All Python files are well-commented
- **Contribute**: See `CONTRIBUTING.md`

## Need Help?

1. Check `README.md` for detailed docs
2. Read the code comments (well-documented!)
3. Open an issue on GitHub

Enjoy! 🏏
