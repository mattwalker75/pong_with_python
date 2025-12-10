"""Unit tests for Ball class."""
import pytest
import math
from game.ball import Ball
from game.settings import settings


@pytest.fixture
def ball():
    """Create a test ball."""
    return Ball(640, 360)


def test_ball_initialization(ball):
    """Test ball is initialized correctly."""
    assert ball.center_x == 640
    assert ball.center_y == 360
    assert ball.velocity_x == 0.0
    assert ball.velocity_y == 0.0
    assert ball.speed == settings.ball_initial_speed


def test_ball_launch_right():
    """Test ball launches to the right."""
    ball = Ball(640, 360)
    ball.launch(direction=1)

    assert ball.velocity_x > 0
    assert ball.velocity_x != 0 or ball.velocity_y != 0


def test_ball_launch_left():
    """Test ball launches to the left."""
    ball = Ball(640, 360)
    ball.launch(direction=-1)

    assert ball.velocity_x < 0
    assert ball.velocity_x != 0 or ball.velocity_y != 0


def test_ball_launch_random():
    """Test ball launches in random direction."""
    ball = Ball(640, 360)
    ball.launch(direction=0)

    assert ball.velocity_x != 0 or ball.velocity_y != 0


def test_ball_update_position():
    """Test ball position updates correctly."""
    ball = Ball(640, 360)
    ball.velocity_x = 5.0
    ball.velocity_y = 3.0

    initial_x = ball.center_x
    initial_y = ball.center_y

    ball.update()

    assert ball.center_x == initial_x + 5.0
    assert ball.center_y == initial_y + 3.0


def test_ball_bounce_top_wall():
    """Test ball bounces off top wall."""
    ball = Ball(640, settings.screen_height - 5)
    ball.velocity_x = 5.0
    ball.velocity_y = 5.0

    ball.update()

    assert ball.velocity_y < 0


def test_ball_bounce_bottom_wall():
    """Test ball bounces off bottom wall."""
    ball = Ball(640, 5)
    ball.velocity_x = 5.0
    ball.velocity_y = -5.0

    ball.update()

    assert ball.velocity_y > 0


def test_ball_bounce_off_paddle():
    """Test ball bounces off paddle correctly."""
    ball = Ball(640, 360)
    ball.velocity_x = 5.0
    ball.velocity_y = 0.0

    initial_speed = math.sqrt(ball.velocity_x**2 + ball.velocity_y**2)
    ball.bounce_off_paddle(360, 120)

    assert ball.velocity_x < 0
    new_speed = math.sqrt(ball.velocity_x**2 + ball.velocity_y**2)
    assert new_speed >= initial_speed


def test_ball_bounce_angle_variation():
    """Test ball bounce angle varies with hit position."""
    ball1 = Ball(640, 360)
    ball1.velocity_x = 5.0
    ball1.velocity_y = 0.0
    ball1.bounce_off_paddle(300, 120)

    ball2 = Ball(640, 360)
    ball2.velocity_x = 5.0
    ball2.velocity_y = 0.0
    ball2.bounce_off_paddle(360, 120)

    assert ball1.velocity_y != ball2.velocity_y


def test_ball_speed_increase_on_bounce():
    """Test ball speed increases after paddle bounce."""
    ball = Ball(640, 360)
    ball.launch(direction=1)

    initial_speed = ball.speed
    ball.bounce_off_paddle(360, 120)

    assert ball.speed > initial_speed


def test_ball_max_speed_limit():
    """Test ball speed is capped at maximum."""
    ball = Ball(640, 360)
    ball.speed = settings.ball_max_speed

    for _ in range(10):
        ball.bounce_off_paddle(360, 120)

    assert ball.speed <= settings.ball_max_speed


def test_ball_out_of_bounds_left():
    """Test ball detects left boundary."""
    ball = Ball(-10, 360)
    assert ball.is_out_of_bounds_left()


def test_ball_out_of_bounds_right():
    """Test ball detects right boundary."""
    ball = Ball(settings.screen_width + 10, 360)
    assert ball.is_out_of_bounds_right()


def test_ball_reset():
    """Test ball reset functionality."""
    ball = Ball(640, 360)
    ball.launch(direction=1)
    ball.update()

    ball.reset(640, 360)

    assert ball.center_x == 640
    assert ball.center_y == 360
    assert ball.velocity_x == 0.0
    assert ball.velocity_y == 0.0
    assert ball.speed == settings.ball_initial_speed
