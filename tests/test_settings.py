"""Unit tests for Settings."""
import pytest
from game.settings import GameSettings, update_difficulty_preset, settings


def test_default_settings():
    """Test default settings are correct."""
    s = GameSettings()

    assert s.screen_width == 1280
    assert s.screen_height == 720
    assert s.winning_score == 10
    assert s.difficulty_preset == "Normal"
    assert s.audio_enabled is True


def test_settings_validation():
    """Test settings validation."""
    s = GameSettings()

    s.master_volume = 0.5
    assert s.master_volume == 0.5

    with pytest.raises(Exception):
        s.master_volume = 1.5


def test_difficulty_preset_easy():
    """Test Easy difficulty preset."""
    update_difficulty_preset("Easy")

    assert settings.difficulty_preset == "Easy"
    assert settings.ai_initial_speed_multiplier == 0.5
    assert settings.ai_max_speed_multiplier == 0.9


def test_difficulty_preset_normal():
    """Test Normal difficulty preset."""
    update_difficulty_preset("Normal")

    assert settings.difficulty_preset == "Normal"
    assert settings.ai_initial_speed_multiplier == 0.7
    assert settings.ai_max_speed_multiplier == 1.2


def test_difficulty_preset_hard():
    """Test Hard difficulty preset."""
    update_difficulty_preset("Hard")

    assert settings.difficulty_preset == "Hard"
    assert settings.ai_initial_speed_multiplier == 0.9
    assert settings.ai_max_speed_multiplier == 1.5


def test_custom_settings():
    """Test custom settings values."""
    s = GameSettings(
        screen_width=1920,
        screen_height=1080,
        winning_score=15,
        audio_enabled=False
    )

    assert s.screen_width == 1920
    assert s.screen_height == 1080
    assert s.winning_score == 15
    assert s.audio_enabled is False


def test_paddle_settings():
    """Test paddle settings."""
    s = GameSettings()

    assert s.paddle_width == 20
    assert s.paddle_height == 120
    assert s.paddle_speed == 6.0


def test_ball_settings():
    """Test ball settings."""
    s = GameSettings()

    assert s.ball_radius == 10
    assert s.ball_initial_speed == 5.0
    assert s.ball_max_speed == 12.0


def test_color_settings():
    """Test color settings are RGB tuples."""
    s = GameSettings()

    assert len(s.background_color) == 3
    assert len(s.paddle_color) == 3
    assert len(s.ball_color) == 3

    assert all(0 <= c <= 255 for c in s.background_color)
    assert all(0 <= c <= 255 for c in s.paddle_color)
    assert all(0 <= c <= 255 for c in s.ball_color)
