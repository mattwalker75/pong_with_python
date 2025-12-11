# Quick Start Guide

## Installation (5 minutes)

### Step 1: Activate Virtual Environment

If you haven't created the virtual environment yet:

```bash
python -m venv pong_venv
```

Then activate it:

**macOS/Linux:**
```bash
source pong_venv/bin/activate
```

**Windows:**
```bash
pong_venv\Scripts\activate
```

You should see `(pong_venv)` in your terminal prompt.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `arcade` - Game engine and graphics
- `pytest` - Testing framework
- `pytest-cov` - Code coverage reporting
- `pydantic` - Settings validation

### Step 3: Run the Game

```bash
python src/main.py
```

That's it! The game should launch in a new window.

## First Time Playing

### Main Menu
- Use **Arrow Keys** or **Mouse** to navigate
- Press **Enter** or **Click** to select
- Choose "Single Player" to play against AI
- Choose "Two Players" for local multiplayer

### During Gameplay

**Default Controls (Single Player):**
- **Up Arrow** - Move Up
- **Down Arrow** - Move Down

**Default Controls (Two Player):**

Player 1 (Left Paddle):
- **W** - Move Up
- **S** - Move Down

Player 2 (Right Paddle):
- **Up Arrow** - Move Up
- **Down Arrow** - Move Down

**Other Controls:**
- **ESC** - Pause/Resume
- **F11** - Toggle Fullscreen

**Want different controls?**
Go to Settings → Configure Controls to customize your key bindings!

### Game Objective
- Prevent the ball from passing your paddle
- First to 10 points wins
- Ball speed increases as the game progresses
- In single player, AI difficulty increases over time

## Customization

### In-Game Settings

The easiest way to customize the game is through the Settings menu:

1. From the main menu, select **SETTINGS**
2. Configure:
   - **Difficulty** - AI difficulty (Easy/Normal/Hard)
   - **Audio** - Toggle sound on/off
   - **Fullscreen** - Toggle fullscreen mode
   - **Configure Controls** - Remap keyboard controls

All settings are automatically saved to `game_config.cfg` and loaded on next startup.

### Advanced Code Settings

For advanced customization, edit `src/game/settings.py`:

```python
# Easy changes
winning_score = 15              # Change points to win
paddle_speed = 8.0              # Faster paddles
ball_max_speed = 15.0           # Faster ball
```

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage report:

```bash
pytest --cov=src --cov-report=html
```

Then open `htmlcov/index.html` in your browser to see detailed coverage.

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'arcade'"

**Solution:** You forgot to install dependencies. Run:
```bash
pip install -r requirements.txt
```

### Problem: "python: command not found"

**Solution:** Try `python3` instead:
```bash
python3 src/main.py
```

### Problem: Virtual environment not activating

**Solution:**
- Make sure you're in the project directory
- On Windows, you might need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Problem: Game window is too large/small

**Solution:** Edit `src/game/settings.py`:
```python
screen_width = 1920   # Change to your preferred width
screen_height = 1080  # Change to your preferred height
```

## Next Steps

- Check out the full [README.md](README.md) for complete documentation
- Read [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details
- Explore the code in `src/game/` to understand how it works
- Run tests to see the code coverage
- Try modifying settings to customize your experience

## Have Fun!

Enjoy playing Pong! Try to beat the AI on Hard difficulty - it's quite challenging! 🎮
