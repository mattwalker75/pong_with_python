"""Ball class for the Pong game."""
import arcade
import random
import math
from game.settings import settings
from game.visual_effects import GlowEffect, MotionTrail


class Ball(arcade.SpriteCircle):
    """Ball sprite with physics."""

    def __init__(self, x: float, y: float):
        """Initialize ball.

        Args:
            x: Initial x position
            y: Initial y position
        """
        super().__init__(settings.ball_radius, settings.ball_color)
        self.center_x = x
        self.center_y = y

        # Velocity
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = settings.ball_initial_speed

        # Boundaries
        self.min_y = settings.ball_radius
        self.max_y = settings.screen_height - settings.ball_radius

        # Motion trail effect
        self.motion_trail = MotionTrail(max_length=settings.motion_blur_length)

    def launch(self, direction: int = 0) -> None:
        """Launch the ball in a random direction.

        Args:
            direction: -1 for left, 1 for right, 0 for random
        """
        if direction == 0:
            direction = random.choice([-1, 1])

        # Random angle between -45 and 45 degrees
        angle = random.uniform(-math.pi / 4, math.pi / 4)

        self.velocity_x = direction * self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)

    def update(self) -> None:
        """Update ball position."""
        self.center_x += self.velocity_x
        self.center_y += self.velocity_y

        # Update motion trail
        self.motion_trail.update(self.center_x, self.center_y)

        # Bounce off top and bottom walls
        if self.center_y <= self.min_y:
            self.center_y = self.min_y
            self.velocity_y = abs(self.velocity_y)
        elif self.center_y >= self.max_y:
            self.center_y = self.max_y
            self.velocity_y = -abs(self.velocity_y)

    def bounce_off_paddle(self, paddle_center_y: float, paddle_height: float) -> None:
        """Bounce the ball off a paddle with angle adjustment.

        Args:
            paddle_center_y: Y position of paddle center
            paddle_height: Height of the paddle
        """
        # Calculate current speed
        current_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)

        # If ball has no velocity, give it some initial velocity
        if current_speed == 0:
            current_speed = self.speed
            self.velocity_x = -self.speed if self.center_x > 640 else self.speed

        # Reverse horizontal direction
        self.velocity_x = -self.velocity_x

        # Calculate where ball hit paddle (normalized to -1 to 1)
        hit_position = (self.center_y - paddle_center_y) / (paddle_height / 2)
        hit_position = max(-1.0, min(1.0, hit_position))

        # Adjust angle based on hit position (max 60 degrees)
        max_angle = math.pi / 3
        angle = hit_position * max_angle

        # Calculate new velocity maintaining speed
        direction = 1 if self.velocity_x > 0 else -1

        self.velocity_x = direction * current_speed * math.cos(angle)
        self.velocity_y = current_speed * math.sin(angle)

        # Increase speed slightly
        self.speed = min(
            self.speed + settings.ball_speed_increase,
            settings.ball_max_speed
        )

        # Apply new speed
        speed_multiplier = self.speed / current_speed
        self.velocity_x *= speed_multiplier
        self.velocity_y *= speed_multiplier

    def reset(self, x: float, y: float) -> None:
        """Reset ball to initial state.

        Args:
            x: X position to reset to
            y: Y position to reset to
        """
        self.center_x = x
        self.center_y = y
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = settings.ball_initial_speed
        self.motion_trail.clear()

    def is_out_of_bounds_left(self) -> bool:
        """Check if ball went past left boundary."""
        return self.center_x < 0

    def is_out_of_bounds_right(self) -> bool:
        """Check if ball went past right boundary."""
        return self.center_x > settings.screen_width

    def draw(self) -> None:
        """Draw the ball with motion trail and glow effect."""
        # Draw motion trail first (behind the ball)
        self.motion_trail.draw(
            settings.ball_radius,
            settings.synthwave_ball_core,
            settings.synthwave_ball_glow
        )

        # Draw ball with radial glow
        GlowEffect.draw_radial_glow(
            self.center_x,
            self.center_y,
            settings.ball_radius,
            settings.synthwave_ball_core,
            settings.synthwave_ball_glow,
            intensity=1.5
        )
