# Pong - Arcade Edition

A modern, feature-rich implementation of the classic Pong game built with Python and the Arcade library. Features smooth graphics, adaptive AI difficulty, single and two-player modes, and a polished user interface.

Using AI to help develop a fun Pong game that is fully written in Python.

## Features

- **Single Player Mode**: Play against an AI opponent with adaptive difficulty that increases over time
- **Two Player Mode**: Classic head-to-head gameplay on the same keyboard
- **Modern Graphics**: Neon arcade aesthetic with smooth animations running at 120 FPS
- **Adaptive AI**: AI difficulty gradually increases based on game duration
- **Sound Effects**: Audio feedback for bounces, scoring, and game events (toggleable)
- **Pause Menu**: Pause anytime with ESC key
- **Settings Menu**: Configure difficulty, audio, fullscreen, and view controls
- **Fullscreen Support**: Toggle fullscreen mode with F11

## Requirements

- Python 3.10 or higher
- Arcade 3.3.3 or higher
- See [requirements.txt](requirements.txt) for Python package dependencies

**Note**: This game has been updated to be compatible with Arcade 3.3.3, which includes significant API changes from earlier versions.

## Installation

### 1. Install Python

Ensure you have Python 3.10 or higher installed:

```bash
python --version
```

If you need to install Python, download it from [python.org](https://www.python.org/downloads/).

### 2. Clone or Download the Repository

```bash
git clone <repository-url>
cd pong_with_python
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv pong_venv
```

Activate the virtual environment:

**On macOS/Linux:**
```bash
source pong_venv/bin/activate
```

**On Windows:**
```bash
pong_venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Game

From the project root directory, run:

```bash
python src/main.py
```

## Controls

### Player 1 (Left Paddle)
- **W** - Move up
- **S** - Move down

### Player 2 (Right Paddle) - Two Player Mode Only
- **Up Arrow** - Move up
- **Down Arrow** - Move down

### General Controls
- **ESC** - Pause/Resume game
- **F11** - Toggle fullscreen
- **Enter** - Select menu option / Play again after game over
- **Arrow Keys** - Navigate menus

## Gameplay

### Single Player Mode
- Play against an adaptive AI opponent
- AI difficulty increases over time:
  - AI paddle speed gradually increases
  - Ball speed gradually increases
  - AI prediction accuracy improves
- First to reach 10 points wins (configurable in settings)

### Two Player Mode
- Classic head-to-head gameplay
- Both players control their paddles simultaneously
- First to reach 10 points wins

### Game Rules
- Ball bounces off paddles and top/bottom walls
- Hitting the ball with different parts of the paddle changes the angle
- Ball speed increases slightly with each paddle hit
- Missing the ball gives your opponent a point
- Game ends when a player reaches the winning score

## Configuration

The game can be configured by modifying the settings in [src/game/settings.py](src/game/settings.py).

### Common Settings

```python
# Display
screen_width = 1280          # Screen width in pixels
screen_height = 720          # Screen height in pixels
target_fps = 120             # Target frames per second

# Gameplay
winning_score = 10           # Score needed to win
difficulty_preset = "Normal" # AI difficulty: "Easy", "Normal", or "Hard"

# Audio
audio_enabled = True         # Enable/disable sound effects
master_volume = 0.7          # Volume level (0.0 to 1.0)

# Paddle
paddle_speed = 6.0           # Paddle movement speed

# Ball
ball_initial_speed = 5.0     # Starting ball speed
ball_max_speed = 12.0        # Maximum ball speed
```

## Testing

The project includes comprehensive unit tests with pytest.

### Running Tests

```bash
pytest
```

### Running Tests with Coverage

```bash
pytest --cov=src --cov-report=html
```

This generates an HTML coverage report in the `htmlcov/` directory.

### Test Files
- `tests/test_paddle.py` - Paddle movement and physics tests
- `tests/test_ball.py` - Ball physics and collision tests
- `tests/test_ai.py` - AI controller and difficulty tests
- `tests/test_settings.py` - Settings and configuration tests
- `tests/test_game_state.py` - Game state and logic tests

## Project Structure

```
pong_with_python/
├── src/
│   ├── main.py                    # Entry point
│   └── game/
│       ├── __init__.py
│       ├── pong_window.py         # Main game logic
│       ├── paddle.py              # Paddle class
│       ├── ball.py                # Ball class
│       ├── ai_controller.py       # AI logic
│       ├── settings.py            # Game settings
│       ├── audio_manager.py       # Sound effects
│       └── ui/
│           ├── main_menu.py       # Main menu
│           ├── pause_menu.py      # Pause menu
│           ├── settings_menu.py   # Settings menu
│           └── components/
│               └── button.py      # Button component
├── tests/                         # Unit tests
├── workflow/                      # AI development notes and documentation
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Troubleshooting

### Game Won't Start

**Issue**: Error when running `python src/main.py`

**Solution**:
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.10+)

### Arcade API Errors

**Issue**: `AttributeError: module 'arcade' has no attribute 'draw_rectangle_filled'`

**Solution**:
- This error indicates you're using an incompatible version of Arcade
- This game requires Arcade 3.3.3 or higher
- Upgrade Arcade: `pip install --upgrade arcade`
- If problems persist, recreate your virtual environment and reinstall dependencies

### Low Frame Rate

**Issue**: Game runs slowly or stutters

**Solution**:
- Close other applications to free up system resources
- Lower the target FPS in settings
- Ensure graphics drivers are up to date

### No Sound

**Issue**: Sound effects not playing

**Solution**:
- Check that audio is enabled in Settings menu
- Verify system volume is not muted
- Check `audio_enabled` setting in `src/game/settings.py`

### Window Size Issues

**Issue**: Game window is too large or small

**Solution**:
- Modify `screen_width` and `screen_height` in `src/game/settings.py`
- Try fullscreen mode with F11

## Uninstallation

### 1. Deactivate Virtual Environment

```bash
deactivate
```

### 2. Remove Project Directory

```bash
cd ..
rm -rf pong_with_python
```

**Note**: The `pong_venv/` directory (if created) and `workflow/` directory remain untouched during uninstallation. Remove these manually if desired.

## Development

### Adding New Features

1. Create or modify files in `src/game/`
2. Add corresponding tests in `tests/`
3. Run tests to ensure nothing breaks: `pytest`
4. Update documentation as needed

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Include docstrings for classes and functions
- Maintain test coverage above 80%

## Tools Used for Development

- **AI**
  - ChatGPT
  - Claude Code
- **Development Tools**
  - VSCode

## Credits

Built with Python and the [Arcade](https://api.arcade.academy/) library.

## License

This project is provided as-is for educational and entertainment purposes.

