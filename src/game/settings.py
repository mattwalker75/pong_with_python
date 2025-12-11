"""Game settings and configuration."""
from typing import Literal
from pydantic import BaseModel, Field
import arcade
import json
from pathlib import Path


class ControlMapping(BaseModel):
    """Control mapping for a single player."""
    up: int = Field(description="Key code for moving up")
    down: int = Field(description="Key code for moving down")

    class Config:
        """Pydantic configuration."""
        validate_assignment = True


class GameSettings(BaseModel):
    """Game configuration settings."""

    # Control settings
    single_player_controls: ControlMapping = Field(
        default=ControlMapping(up=arcade.key.UP, down=arcade.key.DOWN),
        description="Controls for single player mode"
    )
    two_player_p1_controls: ControlMapping = Field(
        default=ControlMapping(up=arcade.key.W, down=arcade.key.S),
        description="Controls for player 1 in two player mode"
    )
    two_player_p2_controls: ControlMapping = Field(
        default=ControlMapping(up=arcade.key.UP, down=arcade.key.DOWN),
        description="Controls for player 2 in two player mode"
    )

    # Display settings
    screen_width: int = Field(default=1280, description="Screen width in pixels")
    screen_height: int = Field(default=720, description="Screen height in pixels")
    screen_title: str = Field(default="Pong - Arcade Edition", description="Window title")
    fullscreen: bool = Field(default=False, description="Fullscreen mode enabled")
    target_fps: int = Field(default=120, description="Target frames per second")

    # Gameplay settings
    winning_score: int = Field(default=10, description="Score needed to win")
    difficulty_preset: Literal["Easy", "Normal", "Hard"] = Field(
        default="Normal",
        description="AI difficulty preset"
    )

    # Audio settings
    audio_enabled: bool = Field(default=True, description="Sound effects enabled")
    master_volume: float = Field(default=0.7, ge=0.0, le=1.0, description="Master volume")

    # Paddle settings
    paddle_width: int = Field(default=20, description="Paddle width in pixels")
    paddle_height: int = Field(default=120, description="Paddle height in pixels")
    paddle_speed: float = Field(default=6.0, description="Paddle movement speed")
    paddle_acceleration: float = Field(default=0.8, description="Paddle acceleration factor")
    paddle_friction: float = Field(default=0.85, description="Paddle friction/deceleration")

    # Ball settings
    ball_radius: int = Field(default=10, description="Ball radius in pixels")
    ball_initial_speed: float = Field(default=5.0, description="Initial ball speed")
    ball_speed_increase: float = Field(default=0.05, description="Ball speed increase per bounce")
    ball_max_speed: float = Field(default=12.0, description="Maximum ball speed")

    # AI settings
    ai_initial_speed_multiplier: float = Field(
        default=0.7,
        description="AI paddle speed as fraction of player speed"
    )
    ai_max_speed_multiplier: float = Field(
        default=1.2,
        description="Maximum AI speed multiplier"
    )
    ai_initial_accuracy: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="AI prediction accuracy (0-1)"
    )
    ai_max_accuracy: float = Field(
        default=0.95,
        ge=0.0,
        le=1.0,
        description="Maximum AI accuracy"
    )
    ai_difficulty_increase_interval: float = Field(
        default=10.0,
        description="Seconds between difficulty increases"
    )
    ai_speed_increase_rate: float = Field(
        default=0.05,
        description="AI speed increase per interval"
    )
    ai_accuracy_increase_rate: float = Field(
        default=0.02,
        description="AI accuracy increase per interval"
    )

    # Visual settings
    background_color: tuple[int, int, int] = Field(
        default=(10, 10, 30),
        description="Background RGB color"
    )
    paddle_color: tuple[int, int, int] = Field(
        default=(0, 255, 255),
        description="Paddle RGB color (neon cyan)"
    )
    ball_color: tuple[int, int, int] = Field(
        default=(255, 50, 255),
        description="Ball RGB color (neon magenta)"
    )
    score_color: tuple[int, int, int] = Field(
        default=(200, 200, 255),
        description="Score text RGB color"
    )
    center_line_color: tuple[int, int, int] = Field(
        default=(50, 50, 100),
        description="Center line RGB color"
    )

    # Synthwave visual theme settings
    synthwave_sky_top: tuple[int, int, int] = Field(
        default=(10, 5, 40),
        description="Sky gradient top color (deep blue/purple)"
    )
    synthwave_sky_bottom: tuple[int, int, int] = Field(
        default=(60, 20, 80),
        description="Sky gradient bottom color (purple)"
    )
    synthwave_grid_color: tuple[int, int, int] = Field(
        default=(255, 20, 147),
        description="Perspective grid lines color (hot pink/magenta)"
    )
    synthwave_grid_glow: tuple[int, int, int] = Field(
        default=(255, 105, 180),
        description="Grid glow color (lighter pink)"
    )
    synthwave_city_base: tuple[int, int, int] = Field(
        default=(20, 20, 40),
        description="City building base color (dark)"
    )
    synthwave_city_windows_cyan: tuple[int, int, int] = Field(
        default=(0, 255, 255),
        description="City windows cyan accent"
    )
    synthwave_city_windows_pink: tuple[int, int, int] = Field(
        default=(255, 20, 147),
        description="City windows pink accent"
    )
    synthwave_city_windows_orange: tuple[int, int, int] = Field(
        default=(255, 140, 0),
        description="City windows orange accent"
    )
    synthwave_paddle_core: tuple[int, int, int] = Field(
        default=(255, 255, 240),
        description="Paddle core color (bright white/cream)"
    )
    synthwave_paddle_glow: tuple[int, int, int] = Field(
        default=(200, 200, 255),
        description="Paddle glow color (soft blue-white)"
    )
    synthwave_ball_core: tuple[int, int, int] = Field(
        default=(255, 255, 255),
        description="Ball core color (pure white)"
    )
    synthwave_ball_glow: tuple[int, int, int] = Field(
        default=(255, 200, 255),
        description="Ball glow color (pink-white)"
    )

    # Visual effect settings
    glow_intensity: float = Field(default=1.0, ge=0.0, le=2.0, description="Global glow intensity")
    motion_blur_enabled: bool = Field(default=True, description="Enable ball motion blur trail")
    motion_blur_length: int = Field(default=15, description="Number of trail segments")
    star_count: int = Field(default=100, description="Number of background stars")
    grid_perspective_depth: float = Field(default=0.8, description="Grid perspective depth factor")

    class Config:
        """Pydantic configuration."""
        validate_assignment = True


# Global settings instance
settings = GameSettings()


def update_difficulty_preset(preset: Literal["Easy", "Normal", "Hard"]) -> None:
    """Update AI difficulty based on preset."""
    global settings

    if preset == "Easy":
        settings.ai_initial_speed_multiplier = 0.5
        settings.ai_max_speed_multiplier = 0.9
        settings.ai_initial_accuracy = 0.5
        settings.ai_max_accuracy = 0.8
        settings.ai_difficulty_increase_interval = 15.0
    elif preset == "Normal":
        settings.ai_initial_speed_multiplier = 0.7
        settings.ai_max_speed_multiplier = 1.2
        settings.ai_initial_accuracy = 0.7
        settings.ai_max_accuracy = 0.95
        settings.ai_difficulty_increase_interval = 10.0
    elif preset == "Hard":
        settings.ai_initial_speed_multiplier = 0.9
        settings.ai_max_speed_multiplier = 1.5
        settings.ai_initial_accuracy = 0.85
        settings.ai_max_accuracy = 0.99
        settings.ai_difficulty_increase_interval = 8.0

    settings.difficulty_preset = preset


def save_settings(config_file: Path = None) -> None:
    """Save current settings to configuration file.

    Args:
        config_file: Path to config file (defaults to game_config.cfg in project root)
    """
    if config_file is None:
        config_file = Path(__file__).parent.parent.parent / "game_config.cfg"

    # Convert settings to dictionary
    config_data = {
        "controls": {
            "single_player": {
                "up": settings.single_player_controls.up,
                "down": settings.single_player_controls.down
            },
            "two_player_p1": {
                "up": settings.two_player_p1_controls.up,
                "down": settings.two_player_p1_controls.down
            },
            "two_player_p2": {
                "up": settings.two_player_p2_controls.up,
                "down": settings.two_player_p2_controls.down
            }
        },
        "display": {
            "fullscreen": settings.fullscreen
        },
        "gameplay": {
            "winning_score": settings.winning_score,
            "difficulty_preset": settings.difficulty_preset
        },
        "audio": {
            "enabled": settings.audio_enabled,
            "master_volume": settings.master_volume
        }
    }

    # Save to file
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)

    print(f"[CONFIG] Settings saved to {config_file}")


def load_settings(config_file: Path = None) -> bool:
    """Load settings from configuration file.

    Args:
        config_file: Path to config file (defaults to game_config.cfg in project root)

    Returns:
        True if settings were loaded, False if file doesn't exist
    """
    global settings

    if config_file is None:
        config_file = Path(__file__).parent.parent.parent / "game_config.cfg"

    if not config_file.exists():
        print(f"[CONFIG] No config file found at {config_file}, using defaults")
        return False

    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)

        # Load control settings
        if "controls" in config_data:
            if "single_player" in config_data["controls"]:
                settings.single_player_controls = ControlMapping(
                    up=config_data["controls"]["single_player"]["up"],
                    down=config_data["controls"]["single_player"]["down"]
                )
            if "two_player_p1" in config_data["controls"]:
                settings.two_player_p1_controls = ControlMapping(
                    up=config_data["controls"]["two_player_p1"]["up"],
                    down=config_data["controls"]["two_player_p1"]["down"]
                )
            if "two_player_p2" in config_data["controls"]:
                settings.two_player_p2_controls = ControlMapping(
                    up=config_data["controls"]["two_player_p2"]["up"],
                    down=config_data["controls"]["two_player_p2"]["down"]
                )

        # Load display settings
        if "display" in config_data:
            if "fullscreen" in config_data["display"]:
                settings.fullscreen = config_data["display"]["fullscreen"]

        # Load gameplay settings
        if "gameplay" in config_data:
            if "winning_score" in config_data["gameplay"]:
                settings.winning_score = config_data["gameplay"]["winning_score"]
            if "difficulty_preset" in config_data["gameplay"]:
                update_difficulty_preset(config_data["gameplay"]["difficulty_preset"])

        # Load audio settings
        if "audio" in config_data:
            if "enabled" in config_data["audio"]:
                settings.audio_enabled = config_data["audio"]["enabled"]
            if "master_volume" in config_data["audio"]:
                settings.master_volume = config_data["audio"]["master_volume"]

        print(f"[CONFIG] Settings loaded from {config_file}")
        return True

    except Exception as e:
        print(f"[CONFIG] Error loading config file: {e}")
        print(f"[CONFIG] Using default settings")
        return False


# Load settings on module import
load_settings()
