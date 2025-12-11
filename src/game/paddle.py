"""Paddle class for the Pong game."""
import arcade
from typing import Literal
from game.settings import settings
from game.visual_effects import GlowEffect


class Paddle(arcade.SpriteSolidColor):
    """Paddle sprite with smooth movement physics."""

    def __init__(self, x: float, y: float, side: Literal["left", "right"]):
        """Initialize paddle.

        Args:
            x: Initial x position
            y: Initial y position
            side: Which side of the screen ("left" or "right")
        """
        super().__init__(
            settings.paddle_width,
            settings.paddle_height,
            settings.paddle_color
        )
        self.center_x = x
        self.center_y = y
        self.side = side

        # Movement state
        self.velocity_y = 0.0
        self.target_velocity = 0.0
        self.max_speed = settings.paddle_speed

        # Boundaries
        self.min_y = settings.paddle_height // 2
        self.max_y = settings.screen_height - (settings.paddle_height // 2)

    def move_up(self) -> None:
        """Set paddle to move upward."""
        self.target_velocity = self.max_speed

    def move_down(self) -> None:
        """Set paddle to move downward."""
        self.target_velocity = -self.max_speed

    def stop(self) -> None:
        """Stop paddle movement."""
        self.target_velocity = 0.0

    def update(self) -> None:
        """Update paddle position with smooth acceleration/deceleration."""
        # Apply acceleration toward target velocity
        if self.target_velocity > self.velocity_y:
            self.velocity_y += settings.paddle_acceleration
            if self.velocity_y > self.target_velocity:
                self.velocity_y = self.target_velocity
        elif self.target_velocity < self.velocity_y:
            self.velocity_y -= settings.paddle_acceleration
            if self.velocity_y < self.target_velocity:
                self.velocity_y = self.target_velocity

        # Apply friction when stopping
        if self.target_velocity == 0.0:
            self.velocity_y *= settings.paddle_friction
            if abs(self.velocity_y) < 0.1:
                self.velocity_y = 0.0

        # Update position
        self.center_y += self.velocity_y

        # Clamp to screen boundaries
        if self.center_y < self.min_y:
            self.center_y = self.min_y
            self.velocity_y = 0.0
        elif self.center_y > self.max_y:
            self.center_y = self.max_y
            self.velocity_y = 0.0

    def reset_position(self, y: float) -> None:
        """Reset paddle to initial position.

        Args:
            y: Y position to reset to
        """
        self.center_y = y
        self.velocity_y = 0.0
        self.target_velocity = 0.0

    def draw(self) -> None:
        """Draw the paddle with synthwave glow effect."""
        GlowEffect.draw_rectangular_glow(
            self.center_x,
            self.center_y,
            settings.paddle_width,
            settings.paddle_height,
            settings.synthwave_paddle_core,
            settings.synthwave_paddle_glow,
            intensity=1.2
        )
