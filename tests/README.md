# Tests Directory

This directory contains the unit test suite for the Pong game. All tests use pytest.

## Test Files

### `conftest.py`
Pytest configuration and shared fixtures used across all test files.

### `test_paddle.py`
Tests for the Paddle class:
- Initialization
- Movement (up/down/stop)
- Physics (acceleration, friction, boundaries)
- Position updates

### `test_ball.py`
Tests for the Ball class:
- Initialization
- Launch mechanics (left/right/random)
- Wall bouncing (top/bottom)
- Speed increases on paddle hits
- Boundary detection (out of bounds)
- Reset functionality

### `test_ai.py`
Tests for the AI Controller:
- Initialization
- Paddle tracking and positioning
- Reaction time delays
- Difficulty scaling over time
- Movement decisions

### `test_game_state.py`
Tests for the game logic and state management:
- Game setup (single/two player modes)
- Scoring system
- Ball reset after scoring
- Win conditions
- Game mode switching

### `test_settings.py`
Tests for configuration management:
- Default settings initialization
- Settings validation
- Difficulty presets (Easy/Normal/Hard)
- Control mapping configuration
- Save/load configuration persistence

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/game

# Run specific test file
pytest tests/test_paddle.py

# Run verbose
pytest -v
```

## Test Coverage

The test suite covers:
- Core game mechanics (ball physics, paddle movement)
- AI behavior and difficulty scaling
- Configuration persistence
- Game state transitions
- Input validation
