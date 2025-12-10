"""Unit tests for game state and logic."""
import pytest
import arcade
from game.pong_window import PongGameView
from game.settings import settings


@pytest.fixture
def window():
    """Create a window for testing."""
    window = arcade.Window(800, 600, "Test")
    yield window
    window.close()


@pytest.fixture
def single_player_game(window):
    """Create a single player game view."""
    game = PongGameView("single")
    game.setup()
    return game


@pytest.fixture
def two_player_game(window):
    """Create a two player game view."""
    game = PongGameView("two_player")
    game.setup()
    return game


def test_game_initialization_single_player(single_player_game):
    """Test single player game initializes correctly."""
    assert single_player_game.game_mode == "single"
    assert single_player_game.score_left == 0
    assert single_player_game.score_right == 0
    assert single_player_game.paddle_left is not None
    assert single_player_game.paddle_right is not None
    assert single_player_game.ball is not None
    assert single_player_game.ai_controller is not None
    assert not single_player_game.paused
    assert not single_player_game.game_over


def test_game_initialization_two_player(two_player_game):
    """Test two player game initializes correctly."""
    assert two_player_game.game_mode == "two_player"
    assert two_player_game.ai_controller is None


def test_scoring_left_side(single_player_game):
    """Test scoring on left side."""
    single_player_game.ball.center_x = settings.screen_width + 100

    single_player_game._check_scoring()

    assert single_player_game.score_left == 1
    assert single_player_game.score_right == 0


def test_scoring_right_side(single_player_game):
    """Test scoring on right side."""
    single_player_game.ball.center_x = -100

    single_player_game._check_scoring()

    assert single_player_game.score_left == 0
    assert single_player_game.score_right == 1


def test_win_condition_player_left(single_player_game):
    """Test win condition for left player."""
    single_player_game.score_left = settings.winning_score

    single_player_game._check_win_condition()

    assert single_player_game.game_over is True
    assert single_player_game.winner == "Player 1"


def test_win_condition_player_right_single(single_player_game):
    """Test win condition for AI in single player."""
    single_player_game.score_right = settings.winning_score

    single_player_game._check_win_condition()

    assert single_player_game.game_over is True
    assert single_player_game.winner == "AI"


def test_win_condition_player_right_two_player(two_player_game):
    """Test win condition for player 2 in two player."""
    two_player_game.score_right = settings.winning_score

    two_player_game._check_win_condition()

    assert two_player_game.game_over is True
    assert two_player_game.winner == "Player 2"


def test_pause_toggle(single_player_game):
    """Test pause toggle functionality."""
    assert not single_player_game.paused

    single_player_game._toggle_pause()
    assert single_player_game.paused

    single_player_game._toggle_pause()
    assert not single_player_game.paused


def test_game_over_prevents_pause(single_player_game):
    """Test pause doesn't work when game is over."""
    single_player_game.game_over = True

    single_player_game._toggle_pause()

    assert not single_player_game.paused


def test_ball_reset(single_player_game):
    """Test ball reset after scoring."""
    initial_x = single_player_game.ball.center_x
    initial_y = single_player_game.ball.center_y

    single_player_game.ball.center_x = 1000
    single_player_game.ball.center_y = 500

    single_player_game._reset_ball()

    assert single_player_game.ball.center_x == initial_x
    assert single_player_game.ball.center_y == initial_y
    assert single_player_game.ball.velocity_x == 0.0
    assert single_player_game.ball.velocity_y == 0.0
