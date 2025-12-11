# Source Code Directory

This directory contains all source code for the Pong game.

## Structure

```
src/
├── main.py                    # Application entry point
├── assets/                    # Game assets
│   └── sounds/                # Audio files
│       ├── background_music.wav  # Background music loop
│       ├── game_over.wav      # Game over sound
│       ├── game_start.wav     # Game start sound
│       ├── paddle_hit.wav     # Paddle collision sound
│       ├── score.wav          # Score point sound
│       └── wall_hit.wav       # Wall bounce sound
└── game/                      # Game package
    ├── settings.py            # Configuration and settings management
    ├── pong_window.py         # Main game window and loop
    ├── paddle.py              # Paddle sprite and physics
    ├── ball.py                # Ball sprite and physics
    ├── ai_controller.py       # AI opponent logic
    ├── background_renderer.py # Synthwave background renderer
    ├── visual_effects.py      # Glow effects and motion trails
    ├── audio_manager.py       # Audio system (Arcade-based)
    ├── audio_manager_pyaudio.py # Audio system (PyAudio-based, alternative)
    ├── sound_generator.py     # Procedural sound effect generation
    ├── music_generator.py     # Procedural music generation
    └── ui/                    # User interface components
        ├── main_menu.py       # Main menu screen
        ├── pause_menu.py      # Pause/resume menu
        ├── settings_menu.py   # Settings configuration menu
        ├── controls_menu.py   # Control mapping configuration
        └── components/        # Reusable UI components
            └── button.py      # Button widget

```

## Core Components

### Entry Point
**`main.py`** - Creates the game window and launches the application.

### Audio Assets
**`assets/sounds/`** - Pre-generated audio files for game events:
- **background_music.wav** - Looping synthwave background music
- **game_over.wav** - Sound played when game ends
- **game_start.wav** - Sound played when game begins
- **paddle_hit.wav** - Sound for ball-paddle collisions
- **score.wav** - Sound when a player scores
- **wall_hit.wav** - Sound for ball-wall collisions

These files are procedurally generated using the sound/music generator modules and saved for consistent playback.

### Game Engine
**`pong_window.py`** - Main game view containing the game loop, collision detection, scoring, and state management. Handles both single-player and two-player modes.

### Game Objects
- **`paddle.py`** - Paddle sprite with smooth acceleration/deceleration physics and boundary constraints
- **`ball.py`** - Ball sprite with velocity-based physics, wall bouncing, and motion trail effects
- **`ai_controller.py`** - AI opponent with reaction delays and difficulty scaling

### Visual Systems
- **`background_renderer.py`** - Synthwave-themed background with gradient sky, starfield, city skyline, and perspective grid
- **`visual_effects.py`** - Glow effects (radial and rectangular) and motion blur trail system

### Configuration
**`settings.py`** - Centralized configuration using Pydantic for type-safe settings:
- Screen dimensions and colors
- Game physics parameters
- AI difficulty settings
- Control mappings
- Audio preferences
- Synthwave visual theme colors
- Save/load configuration to JSON

### Audio System
- **`audio_manager.py`** - Primary audio manager using Arcade's audio system
- **`audio_manager_pyaudio.py`** - Alternative audio manager using PyAudio (for systems where Arcade audio fails)
- **`sound_generator.py`** - Generates procedural sound effects (paddle hits, wall bounces, scoring)
- **`music_generator.py`** - Generates procedural background music

### User Interface

#### Menus
- **`ui/main_menu.py`** - Main menu with synthwave styling (Single Player, Two Player, Settings, Quit)
- **`ui/pause_menu.py`** - In-game pause menu (Resume, Settings, Main Menu)
- **`ui/settings_menu.py`** - Settings configuration (Difficulty, Audio, Fullscreen, Controls)
- **`ui/controls_menu.py`** - Custom control mapping interface with conflict detection

#### Components
- **`ui/components/button.py`** - Reusable button widget with neon glow effects and hover states

## Key Features

### Game Mechanics
- Smooth paddle physics with acceleration/friction
- Ball speed increases on paddle hits
- AI difficulty scales over time
- Configurable winning score
- Single and two-player modes

### Visual Theme
- Synthwave/cyberpunk aesthetic
- Neon glow effects on all game objects
- Motion blur trail on ball
- Procedurally generated city skyline
- Perspective grid floor
- Gradient sky with starfield

### Configuration
- Customizable controls for both players
- Difficulty presets (Easy, Normal, Hard)
- Audio toggle
- Fullscreen support
- Persistent configuration via JSON file

### Audio
- Procedurally generated sound effects
- Background music generation
- Fallback audio system for compatibility

## Development Notes

- Built with Python Arcade 3.3.3
- Uses Pydantic for configuration management
- Type hints throughout for better IDE support
- Modular design with separated concerns
- All visual effects use arcade.draw API with XYWH specifications
