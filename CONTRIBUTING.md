# Contributing to CricSim

Thanks for interest in contributing! Here's how to set up your development environment.

## Development Setup

### 1. Clone & Install

```bash
git clone <repository-url>
cd CricSim
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -e ".[dev,rich]"
```

### 2. Code Style

We follow PEP 8. Format code with black:

```bash
black *.py
```

Verify with flake8:
```bash
flake8 *.py
```

### 3. Testing

Run tests:
```bash
pytest
```

### 4. Making Changes

**Important: Do NOT change the core game logic lightly!**

- Core mechanics are in `match_simulator.py` - be careful with probability calculations
- Coefficients are in `config.json` - adjust here for balance, not in code
- New features should not break existing functionality

### 5. Submit Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -am "Add feature X"`
3. Verify everything works: `python main.py`
4. Push: `git push origin feature/your-feature`
5. Create a Pull Request

## Areas for Contribution

- **New Teams**: Add teams to `teams.py`
- **New Difficulty Profiles**: Edit `config.json`
- **Statistics Analysis**: Enhance `top_players.py`
- **Documentation**: Improve README or add examples
- **Bug Fixes**: Report issues with detailed reproduction steps
- **Performance**: Optimize simulation speed

## Code Guidelines

- Keep functions focused and under 50 lines when possible
- Add docstrings to new functions
- Handle exceptions gracefully
- Test your changes manually with `python main.py`
- Update README if adding features/config options

## Questions?

Open an issue for questions or discussions!
