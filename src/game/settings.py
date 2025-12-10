"""Game settings and configuration."""
from typing import Literal
from pydantic import BaseModel, Field


class GameSettings(BaseModel):
    """Game configuration settings."""

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
