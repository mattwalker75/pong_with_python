"""AI controller for single-player mode."""
import random
from game.paddle import Paddle
from game.ball import Ball
from game.settings import settings


class AIController:
    """Controls AI paddle with adaptive difficulty."""

    def __init__(self, paddle: Paddle):
        """Initialize AI controller.

        Args:
            paddle: The paddle to control
        """
        self.paddle = paddle
        self.elapsed_time = 0.0

        # Difficulty parameters (start at initial values)
        self.speed_multiplier = settings.ai_initial_speed_multiplier
        self.accuracy = settings.ai_initial_accuracy

        # Reaction delay simulation
        self.reaction_time = 0.1
        self.last_update = 0.0

    def update(self, ball: Ball, delta_time: float) -> None:
        """Update AI paddle movement.

        Args:
            ball: The game ball
            delta_time: Time since last update
        """
        self.elapsed_time += delta_time
        self.last_update += delta_time

        # Increase difficulty over time
        self._update_difficulty()

        # Only update decision at intervals (simulates reaction time)
        if self.last_update >= self.reaction_time:
            self.last_update = 0.0
            self._make_decision(ball)

    def _update_difficulty(self) -> None:
        """Gradually increase AI difficulty."""
        intervals_passed = int(
            self.elapsed_time / settings.ai_difficulty_increase_interval
        )

        # Calculate new speed multiplier
        new_speed = (
            settings.ai_initial_speed_multiplier +
            (intervals_passed * settings.ai_speed_increase_rate)
        )
        self.speed_multiplier = min(new_speed, settings.ai_max_speed_multiplier)

        # Calculate new accuracy
        new_accuracy = (
            settings.ai_initial_accuracy +
            (intervals_passed * settings.ai_accuracy_increase_rate)
        )
        self.accuracy = min(new_accuracy, settings.ai_max_accuracy)

        # Update paddle max speed
        self.paddle.max_speed = settings.paddle_speed * self.speed_multiplier

    def _make_decision(self, ball: Ball) -> None:
        """Decide paddle movement based on ball position.

        Args:
            ball: The game ball
        """
        # Only react if ball is moving toward AI paddle
        if self.paddle.side == "right" and ball.velocity_x < 0:
            # Ball moving away, return to center
            self._move_to_center()
            return
        elif self.paddle.side == "left" and ball.velocity_x > 0:
            # Ball moving away, return to center
            self._move_to_center()
            return

        # Predict where ball will be
        target_y = self._predict_ball_position(ball)

        # Apply accuracy (add random error)
        if random.random() > self.accuracy:
            error_range = settings.paddle_height * 0.5
            target_y += random.uniform(-error_range, error_range)

        # Move toward target
        dead_zone = 10  # Don't move if already close
        if abs(self.paddle.center_y - target_y) > dead_zone:
            if self.paddle.center_y < target_y:
                self.paddle.move_up()
            else:
                self.paddle.move_down()
        else:
            self.paddle.stop()

    def _predict_ball_position(self, ball: Ball) -> float:
        """Predict where the ball will intersect with paddle's x position.

        Args:
            ball: The game ball

        Returns:
            Predicted y position
        """
        # Simple linear prediction (doesn't account for wall bounces)
        if ball.velocity_x == 0:
            return ball.center_y

        # Calculate time until ball reaches paddle x position
        paddle_x = self.paddle.center_x
        time_to_reach = abs((paddle_x - ball.center_x) / ball.velocity_x)

        # Predict y position
        predicted_y = ball.center_y + (ball.velocity_y * time_to_reach)

        # Account for wall bounces (simple approximation)
        while predicted_y < ball.min_y or predicted_y > ball.max_y:
            if predicted_y < ball.min_y:
                predicted_y = ball.min_y + (ball.min_y - predicted_y)
            elif predicted_y > ball.max_y:
                predicted_y = ball.max_y - (predicted_y - ball.max_y)

        return predicted_y

    def _move_to_center(self) -> None:
        """Move paddle toward vertical center of screen."""
        center_y = settings.screen_height / 2
        dead_zone = 20

        if abs(self.paddle.center_y - center_y) > dead_zone:
            if self.paddle.center_y < center_y:
                self.paddle.move_up()
            else:
                self.paddle.move_down()
        else:
            self.paddle.stop()

    def reset(self) -> None:
        """Reset AI difficulty to initial values."""
        self.elapsed_time = 0.0
        self.last_update = 0.0
        self.speed_multiplier = settings.ai_initial_speed_multiplier
        self.accuracy = settings.ai_initial_accuracy
        self.paddle.max_speed = settings.paddle_speed * self.speed_multiplier
