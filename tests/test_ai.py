"""Unit tests for AI Controller."""
import pytest
from game.ai_controller import AIController
from game.paddle import Paddle
from game.ball import Ball
from game.settings import settings


@pytest.fixture
def ai_paddle():
    """Create a test AI paddle."""
    return Paddle(settings.screen_width - 50, settings.screen_height / 2, "right")


@pytest.fixture
def ai_controller(ai_paddle):
    """Create a test AI controller."""
    return AIController(ai_paddle)


@pytest.fixture
def ball():
    """Create a test ball."""
    return Ball(settings.screen_width / 2, settings.screen_height / 2)


def test_ai_initialization(ai_controller):
    """Test AI controller is initialized correctly."""
    assert ai_controller.elapsed_time == 0.0
    assert ai_controller.speed_multiplier == settings.ai_initial_speed_multiplier
    assert ai_controller.accuracy == settings.ai_initial_accuracy


def test_ai_tracks_ball_moving_toward_paddle(ai_controller, ball):
    """Test AI tracks ball moving toward it."""
    ball.center_x = settings.screen_width / 2
    ball.center_y = 100
    ball.velocity_x = 5.0
    ball.velocity_y = 0.0

    ai_controller.paddle.center_y = 500

    ai_controller.update(ball, 0.2)

    assert ai_controller.paddle.target_velocity != 0


def test_ai_returns_to_center_when_ball_moving_away(ai_controller, ball):
    """Test AI returns to center when ball moves away."""
    ball.center_x = settings.screen_width / 2
    ball.center_y = settings.screen_height / 2
    ball.velocity_x = -5.0

    ai_controller.paddle.center_y = 100

    ai_controller.update(ball, 0.2)

    assert ai_controller.paddle.target_velocity != 0


def test_ai_difficulty_increases_over_time(ai_controller, ball):
    """Test AI difficulty increases over time."""
    initial_speed = ai_controller.speed_multiplier
    initial_accuracy = ai_controller.accuracy

    for _ in range(20):
        ai_controller.update(ball, settings.ai_difficulty_increase_interval)

    assert ai_controller.speed_multiplier > initial_speed
    assert ai_controller.accuracy > initial_accuracy


def test_ai_difficulty_capped_at_maximum(ai_controller, ball):
    """Test AI difficulty doesn't exceed maximum."""
    for _ in range(100):
        ai_controller.update(ball, settings.ai_difficulty_increase_interval)

    assert ai_controller.speed_multiplier <= settings.ai_max_speed_multiplier
    assert ai_controller.accuracy <= settings.ai_max_accuracy


def test_ai_reset():
    """Test AI reset functionality."""
    paddle = Paddle(settings.screen_width - 50, settings.screen_height / 2, "right")
    ai = AIController(paddle)
    ball = Ball(settings.screen_width / 2, settings.screen_height / 2)

    for _ in range(10):
        ai.update(ball, settings.ai_difficulty_increase_interval)

    ai.reset()

    assert ai.elapsed_time == 0.0
    assert ai.speed_multiplier == settings.ai_initial_speed_multiplier
    assert ai.accuracy == settings.ai_initial_accuracy


def test_ai_prediction_accuracy(ai_controller, ball):
    """Test AI can predict ball position."""
    ball.center_x = 200
    ball.center_y = 360
    ball.velocity_x = 5.0
    ball.velocity_y = 3.0

    predicted_y = ai_controller._predict_ball_position(ball)

    assert isinstance(predicted_y, float)
    assert ball.min_y <= predicted_y <= ball.max_y


def test_ai_reaction_time_delay(ai_controller, ball):
    """Test AI has reaction time delay."""
    ball.velocity_x = 5.0
    ball.center_y = 100

    ai_controller.paddle.center_y = 500

    initial_velocity = ai_controller.paddle.target_velocity
    ai_controller.update(ball, 0.05)

    assert ai_controller.paddle.target_velocity == initial_velocity
