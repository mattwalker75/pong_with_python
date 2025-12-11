# Pong - Arcade Edition

A modern, feature-rich implementation of the classic Pong game built with Python and the Arcade library. Features smooth graphics, adaptive AI difficulty, single and two-player modes, and a polished user interface.

Using AI to help develop a fun Pong game that is fully written in Python.

## Features

- **Single Player Mode**: Play against an AI opponent with adaptive difficulty that increases over time
- **Two Player Mode**: Classic head-to-head gameplay on the same keyboard
- **Modern Graphics**: Neon arcade aesthetic with smooth animations running at 120 FPS
- **Adaptive AI**: AI difficulty gradually increases based on game duration
- **Retro Sound Effects**: Classic Pong "ping" sounds for paddle hits, wall bounces, and scoring
- **Background Music**: Looping 80s-style arcade music during gameplay
- **Audio Controls**: Toggle audio on/off in settings menu
- **Pause Menu**: Pause anytime with ESC key
- **Settings Menu**: Configure difficulty, audio, fullscreen, and view controls
- **Fullscreen Support**: Toggle fullscreen mode with F11

## Requirements

- Python 3.10 or higher
- Arcade 3.3.3 or higher
- See [requirements.txt](requirements.txt) for Python package dependencies

**Note**: This game has been updated to be compatible with Arcade 3.3.3, which includes significant API changes from earlier versions.

## Installation

### Quick Install (macOS/Linux)

For a one-command installation, run the provided script:

```bash
./INSTALL.sh
```

This will:
- Check Python version
- Install PortAudio (macOS with Homebrew)
- Create virtual environment
- Install all Python dependencies
- Generate audio files

Then skip to [Running the Game](#running-the-game).

### Manual Installation

#### 1. Install Python

Ensure you have Python 3.10 or higher installed:

```bash
python --version
```

If you need to install Python, download it from [python.org](https://www.python.org/downloads/).

#### 2. Clone or Download the Repository

```bash
git clone <repository-url>
cd pong_with_python
```

#### 3. Create a Virtual Environment (Recommended)

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

#### 4. Install System Dependencies (macOS)

On macOS, you need to install the PortAudio library for audio support:

```bash
brew install portaudio
```

**Note**: On Linux, install portaudio19-dev: `sudo apt-get install portaudio19-dev`
On Windows, the PyAudio wheel usually includes portaudio.

#### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 6. Generate Audio Files (First Time Only)

The game includes retro sound effects and background music. Generate them once:

```bash
python setup_audio.py
```

This creates:
- Classic "ping" sound effects for paddle and wall hits
- Scoring sound effects
- Looping 80s-style arcade background music

**Note**: Audio files are generated programmatically and total ~1.3 MB. You only need to run this once.

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

**Issue**: Sound effects or music not playing

**Solution**:
1. Make sure you've generated the audio files:
   ```bash
   python setup_audio.py
   ```
2. Verify audio files exist in `src/assets/sounds/`:
   - `paddle_hit.wav`
   - `wall_hit.wav`
   - `score.wav`
   - `game_start.wav`
   - `game_over.wav`
   - `background_music.wav`
3. Check that audio is enabled in Settings menu
4. Verify system volume is not muted
5. Check `audio_enabled` setting in `src/game/settings.py`
6. For detailed troubleshooting, see [docs/AUDIO_TROUBLESHOOTING.md](docs/AUDIO_TROUBLESHOOTING.md)

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

## Documentation

Additional documentation is available in the `docs/` directory:

- **[AUDIO_README.md](docs/AUDIO_README.md)** - Audio system documentation and API reference
- **[AUDIO_TROUBLESHOOTING.md](docs/AUDIO_TROUBLESHOOTING.md)** - Audio troubleshooting guide
- **[ARCADE_3.3_MIGRATION.md](docs/ARCADE_3.3_MIGRATION.md)** - Arcade 3.3.3 migration guide

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

