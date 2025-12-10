"""Unit tests for Paddle class."""
import pytest
from game.paddle import Paddle
from game.settings import settings


@pytest.fixture
def paddle():
    """Create a test paddle."""
    return Paddle(100, 360, "left")


def test_paddle_initialization(paddle):
    """Test paddle is initialized correctly."""
    assert paddle.center_x == 100
    assert paddle.center_y == 360
    assert paddle.side == "left"
    assert paddle.velocity_y == 0.0
    assert paddle.target_velocity == 0.0


def test_paddle_move_up(paddle):
    """Test paddle moves up when commanded."""
    paddle.move_up()
    assert paddle.target_velocity == paddle.max_speed


def test_paddle_move_down(paddle):
    """Test paddle moves down when commanded."""
    paddle.move_down()
    assert paddle.target_velocity == -paddle.max_speed


def test_paddle_stop(paddle):
    """Test paddle stops when commanded."""
    paddle.move_up()
    paddle.stop()
    assert paddle.target_velocity == 0.0


def test_paddle_update_acceleration():
    """Test paddle accelerates smoothly."""
    paddle = Paddle(100, 360, "left")
    paddle.move_up()

    initial_velocity = paddle.velocity_y
    paddle.update()

    assert paddle.velocity_y > initial_velocity
    assert paddle.velocity_y <= paddle.target_velocity


def test_paddle_update_deceleration():
    """Test paddle decelerates with friction."""
    paddle = Paddle(100, 360, "left")
    paddle.velocity_y = 5.0
    paddle.stop()

    paddle.update()

    assert paddle.velocity_y < 5.0


def test_paddle_boundary_top():
    """Test paddle respects top boundary."""
    paddle = Paddle(100, settings.screen_height, "left")
    paddle.move_up()

    for _ in range(50):
        paddle.update()

    assert paddle.center_y <= settings.screen_height - (settings.paddle_height // 2)


def test_paddle_boundary_bottom():
    """Test paddle respects bottom boundary."""
    paddle = Paddle(100, 0, "left")
    paddle.move_down()

    for _ in range(50):
        paddle.update()

    assert paddle.center_y >= settings.paddle_height // 2


def test_paddle_reset_position():
    """Test paddle position reset."""
    paddle = Paddle(100, 360, "left")
    paddle.move_up()
    paddle.update()

    paddle.reset_position(500)

    assert paddle.center_y == 500
    assert paddle.velocity_y == 0.0
    assert paddle.target_velocity == 0.0


def test_paddle_continuous_movement():
    """Test paddle moves continuously when input is held."""
    paddle = Paddle(100, 360, "left")
    paddle.move_up()

    initial_y = paddle.center_y

    for _ in range(10):
        paddle.update()

    assert paddle.center_y > initial_y
