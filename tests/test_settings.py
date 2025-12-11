"""Unit tests for Settings."""
import pytest
import arcade
import json
import tempfile
from pathlib import Path
from game.settings import (
    GameSettings,
    update_difficulty_preset,
    settings,
    ControlMapping,
    save_settings,
    load_settings
)


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


# Control Configuration Tests

def test_control_mapping_default():
    """Test default ControlMapping creation."""
    control = ControlMapping(up=arcade.key.UP, down=arcade.key.DOWN)

    assert control.up == arcade.key.UP
    assert control.down == arcade.key.DOWN


def test_control_mapping_custom():
    """Test custom ControlMapping creation."""
    control = ControlMapping(up=arcade.key.W, down=arcade.key.S)

    assert control.up == arcade.key.W
    assert control.down == arcade.key.S


def test_default_single_player_controls():
    """Test default single player controls."""
    s = GameSettings()

    assert s.single_player_controls.up == arcade.key.UP
    assert s.single_player_controls.down == arcade.key.DOWN


def test_default_two_player_controls():
    """Test default two player controls."""
    s = GameSettings()

    # Player 1 defaults
    assert s.two_player_p1_controls.up == arcade.key.W
    assert s.two_player_p1_controls.down == arcade.key.S

    # Player 2 defaults
    assert s.two_player_p2_controls.up == arcade.key.UP
    assert s.two_player_p2_controls.down == arcade.key.DOWN


def test_custom_single_player_controls():
    """Test setting custom single player controls."""
    s = GameSettings()
    s.single_player_controls = ControlMapping(up=arcade.key.I, down=arcade.key.K)

    assert s.single_player_controls.up == arcade.key.I
    assert s.single_player_controls.down == arcade.key.K


def test_custom_two_player_controls():
    """Test setting custom two player controls."""
    s = GameSettings()

    # Customize P1 controls
    s.two_player_p1_controls = ControlMapping(up=arcade.key.Q, down=arcade.key.A)
    assert s.two_player_p1_controls.up == arcade.key.Q
    assert s.two_player_p1_controls.down == arcade.key.A

    # Customize P2 controls
    s.two_player_p2_controls = ControlMapping(up=arcade.key.O, down=arcade.key.L)
    assert s.two_player_p2_controls.up == arcade.key.O
    assert s.two_player_p2_controls.down == arcade.key.L


def test_save_and_load_settings():
    """Test saving and loading settings from config file."""
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cfg', delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        # Modify global settings
        original_single_up = settings.single_player_controls.up
        original_p1_up = settings.two_player_p1_controls.up
        original_difficulty = settings.difficulty_preset

        settings.single_player_controls = ControlMapping(up=arcade.key.I, down=arcade.key.K)
        settings.two_player_p1_controls = ControlMapping(up=arcade.key.Q, down=arcade.key.A)
        settings.two_player_p2_controls = ControlMapping(up=arcade.key.O, down=arcade.key.L)
        settings.difficulty_preset = "Hard"
        settings.audio_enabled = False

        # Save settings
        save_settings(tmp_path)

        # Verify file exists
        assert tmp_path.exists()

        # Verify file contents
        with open(tmp_path, 'r') as f:
            config_data = json.load(f)

        assert config_data["controls"]["single_player"]["up"] == arcade.key.I
        assert config_data["controls"]["single_player"]["down"] == arcade.key.K
        assert config_data["controls"]["two_player_p1"]["up"] == arcade.key.Q
        assert config_data["controls"]["two_player_p1"]["down"] == arcade.key.A
        assert config_data["controls"]["two_player_p2"]["up"] == arcade.key.O
        assert config_data["controls"]["two_player_p2"]["down"] == arcade.key.L
        assert config_data["gameplay"]["difficulty_preset"] == "Hard"
        assert config_data["audio"]["enabled"] is False

        # Reset settings to defaults
        settings.single_player_controls = ControlMapping(up=arcade.key.UP, down=arcade.key.DOWN)
        settings.two_player_p1_controls = ControlMapping(up=arcade.key.W, down=arcade.key.S)
        settings.audio_enabled = True

        # Load settings
        load_result = load_settings(tmp_path)
        assert load_result is True

        # Verify loaded settings
        assert settings.single_player_controls.up == arcade.key.I
        assert settings.single_player_controls.down == arcade.key.K
        assert settings.two_player_p1_controls.up == arcade.key.Q
        assert settings.two_player_p1_controls.down == arcade.key.A
        assert settings.two_player_p2_controls.up == arcade.key.O
        assert settings.two_player_p2_controls.down == arcade.key.L
        assert settings.difficulty_preset == "Hard"
        assert settings.audio_enabled is False

        # Restore original settings
        settings.single_player_controls = ControlMapping(up=original_single_up, down=arcade.key.DOWN)
        settings.two_player_p1_controls = ControlMapping(up=original_p1_up, down=arcade.key.S)
        update_difficulty_preset(original_difficulty)
        settings.audio_enabled = True

    finally:
        # Clean up temp file
        if tmp_path.exists():
            tmp_path.unlink()


def test_load_settings_missing_file():
    """Test loading settings from non-existent file."""
    # Try to load from a file that doesn't exist
    non_existent = Path("/tmp/definitely_does_not_exist_12345.cfg")
    result = load_settings(non_existent)

    assert result is False


def test_save_settings_config_structure():
    """Test the structure of saved config file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cfg', delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        save_settings(tmp_path)

        with open(tmp_path, 'r') as f:
            config_data = json.load(f)

        # Check top-level structure
        assert "controls" in config_data
        assert "display" in config_data
        assert "gameplay" in config_data
        assert "audio" in config_data

        # Check controls structure
        assert "single_player" in config_data["controls"]
        assert "two_player_p1" in config_data["controls"]
        assert "two_player_p2" in config_data["controls"]

        # Check each control has up and down
        for control_type in ["single_player", "two_player_p1", "two_player_p2"]:
            assert "up" in config_data["controls"][control_type]
            assert "down" in config_data["controls"][control_type]

    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def test_control_mapping_validation():
    """Test ControlMapping validates assignments."""
    control = ControlMapping(up=arcade.key.W, down=arcade.key.S)

    # Should be able to reassign
    control.up = arcade.key.UP
    assert control.up == arcade.key.UP

    control.down = arcade.key.DOWN
    assert control.down == arcade.key.DOWN
