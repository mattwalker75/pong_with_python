"""Main Pong game window and logic."""
import arcade
from typing import Literal, Optional
from game.settings import settings
from game.paddle import Paddle
from game.ball import Ball
from game.ai_controller import AIController
from game.audio_manager_pyaudio import PyAudioManager as AudioManager
from game.ui.pause_menu import PauseMenu
from game.background_renderer import BackgroundRenderer


class PongGameView(arcade.View):
    """Main Pong game view."""

    def __init__(self, game_mode: Literal["single", "two_player"]):
        """Initialize game view.

        Args:
            game_mode: "single" for single player, "two_player" for two players
        """
        super().__init__()
        self.game_mode = game_mode

        # Game objects
        self.paddle_left: Optional[Paddle] = None
        self.paddle_right: Optional[Paddle] = None
        self.ball: Optional[Ball] = None
        self.ai_controller: Optional[AIController] = None
        self.audio_manager: Optional[AudioManager] = None
        self.pause_menu: Optional[PauseMenu] = None
        self.background_renderer: Optional[BackgroundRenderer] = None

        # Game state
        self.score_left = 0
        self.score_right = 0
        self.paused = False
        self.game_over = False
        self.winner = ""

        # Input state
        self.keys_pressed = set()

    def setup(self) -> None:
        """Set up the game."""
        # Create paddles
        paddle_margin = 50
        center_y = settings.screen_height / 2

        self.paddle_left = Paddle(paddle_margin, center_y, "left")
        self.paddle_right = Paddle(
            settings.screen_width - paddle_margin,
            center_y,
            "right"
        )

        # Create ball
        self.ball = Ball(
            settings.screen_width / 2,
            settings.screen_height / 2
        )

        # Create AI controller if single player
        if self.game_mode == "single":
            self.ai_controller = AIController(self.paddle_right)

        # Create audio manager
        self.audio_manager = AudioManager()

        # Create pause menu
        self.pause_menu = PauseMenu()
        self.pause_menu.on_resume = self._resume_game
        self.pause_menu.on_quit = self._quit_to_menu

        # Create background renderer
        self.background_renderer = BackgroundRenderer(
            settings.screen_width,
            settings.screen_height
        )

        # Reset game state
        self.score_left = 0
        self.score_right = 0
        self.game_over = False
        self.winner = ""

        # Start the ball and background music
        self.audio_manager.play_game_start()
        self.audio_manager.play_background_music()
        self.ball.launch()

    def on_draw(self) -> None:
        """Draw the game."""
        self.clear()

        # Draw synthwave background
        self.background_renderer.draw()

        if not self.game_over:
            # Draw center line
            self._draw_center_line()

            # Draw game objects
            self.paddle_left.draw()
            self.paddle_right.draw()
            self.ball.draw()

            # Draw scores
            self._draw_scores()

            # Draw pause menu if paused
            if self.paused:
                self.pause_menu.draw()

        else:
            # Draw game over screen
            self._draw_game_over()

    def on_update(self, delta_time: float) -> None:
        """Update game state.

        Args:
            delta_time: Time since last update
        """
        if self.paused or self.game_over:
            return

        # Update ball
        self.ball.update()

        # Update paddles
        self._update_player_input()
        self.paddle_left.update()
        self.paddle_right.update()

        # Update AI
        if self.ai_controller:
            self.ai_controller.update(self.ball, delta_time)

        # Check collisions
        self._check_paddle_collisions()
        self._check_scoring()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle key presses.

        Args:
            key: Key that was pressed
            modifiers: Modifier keys held
        """
        # Check if pause menu handles the key
        if self.pause_menu.handle_key_press(key):
            return

        # Toggle pause
        if key == arcade.key.ESCAPE:
            self._toggle_pause()
            return

        # Toggle fullscreen
        if key == arcade.key.F11:
            settings.fullscreen = not settings.fullscreen
            self.window.set_fullscreen(settings.fullscreen)
            return

        # Game over - restart
        if self.game_over and key == arcade.key.ENTER:
            self.setup()
            return

        # Game over - back to menu
        if self.game_over and key == arcade.key.ESCAPE:
            self._quit_to_menu()
            return

        # Track key state
        self.keys_pressed.add(key)

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Handle key releases.

        Args:
            key: Key that was released
            modifiers: Modifier keys held
        """
        self.keys_pressed.discard(key)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        """Handle mouse motion.

        Args:
            x: Mouse x position
            y: Mouse y position
            dx: Change in x
            dy: Change in y
        """
        self.pause_menu.handle_mouse_motion(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Handle mouse clicks.

        Args:
            x: Mouse x position
            y: Mouse y position
            button: Mouse button pressed
            modifiers: Modifier keys held
        """
        self.pause_menu.handle_mouse_press(x, y)

    def on_hide_view(self) -> None:
        """Called when this view is hidden (e.g., switching to menu)."""
        if self.audio_manager:
            self.audio_manager.cleanup()

    def _update_player_input(self) -> None:
        """Update paddle movement based on input using configurable controls."""
        if self.game_mode == "single":
            # Single player mode - use single player controls for left paddle
            controls = settings.single_player_controls
            if controls.up in self.keys_pressed:
                self.paddle_left.move_up()
            elif controls.down in self.keys_pressed:
                self.paddle_left.move_down()
            else:
                self.paddle_left.stop()
        else:
            # Two player mode - use separate controls for each paddle
            p1_controls = settings.two_player_p1_controls
            p2_controls = settings.two_player_p2_controls

            # Player 1 (left paddle)
            if p1_controls.up in self.keys_pressed:
                self.paddle_left.move_up()
            elif p1_controls.down in self.keys_pressed:
                self.paddle_left.move_down()
            else:
                self.paddle_left.stop()

            # Player 2 (right paddle)
            if p2_controls.up in self.keys_pressed:
                self.paddle_right.move_up()
            elif p2_controls.down in self.keys_pressed:
                self.paddle_right.move_down()
            else:
                self.paddle_right.stop()

    def _check_paddle_collisions(self) -> None:
        """Check for ball-paddle collisions."""
        # Left paddle collision
        if (
            self.ball.velocity_x < 0 and
            self.paddle_left.collides_with_sprite(self.ball)
        ):
            self.ball.bounce_off_paddle(
                self.paddle_left.center_y,
                settings.paddle_height
            )
            self.audio_manager.play_bounce()

        # Right paddle collision
        if (
            self.ball.velocity_x > 0 and
            self.paddle_right.collides_with_sprite(self.ball)
        ):
            self.ball.bounce_off_paddle(
                self.paddle_right.center_y,
                settings.paddle_height
            )
            self.audio_manager.play_bounce()

        # Wall bounces
        if (
            self.ball.center_y <= self.ball.min_y or
            self.ball.center_y >= self.ball.max_y
        ):
            self.audio_manager.play_wall_bounce()

    def _check_scoring(self) -> None:
        """Check if anyone scored."""
        if self.ball.is_out_of_bounds_left():
            self.score_right += 1
            self.audio_manager.play_score()
            self._reset_ball()
            self._check_win_condition()

        elif self.ball.is_out_of_bounds_right():
            self.score_left += 1
            self.audio_manager.play_score()
            self._reset_ball()
            self._check_win_condition()

    def _reset_ball(self) -> None:
        """Reset ball to center after scoring."""
        self.ball.reset(
            settings.screen_width / 2,
            settings.screen_height / 2
        )

        # Small delay before launching
        arcade.schedule(self._delayed_ball_launch, 0.5)

    def _delayed_ball_launch(self, delta_time: float) -> None:
        """Launch ball after delay."""
        self.ball.launch()
        arcade.unschedule(self._delayed_ball_launch)

    def _check_win_condition(self) -> None:
        """Check if someone won the game."""
        if self.score_left >= settings.winning_score:
            self.game_over = True
            self.winner = "Player 1"
            self.audio_manager.play_game_end()

        elif self.score_right >= settings.winning_score:
            self.game_over = True
            if self.game_mode == "single":
                self.winner = "AI"
            else:
                self.winner = "Player 2"
            self.audio_manager.play_game_end()

    def _toggle_pause(self) -> None:
        """Toggle pause state."""
        if self.game_over:
            return

        self.paused = not self.paused
        if self.paused:
            self.pause_menu.show()
        else:
            self.pause_menu.hide()

    def _resume_game(self) -> None:
        """Resume the game."""
        self.paused = False
        self.pause_menu.hide()

    def _quit_to_menu(self) -> None:
        """Return to main menu."""
        from game.ui.main_menu import MainMenuView

        menu = MainMenuView()
        menu.setup()

        # Set up menu callbacks
        menu.on_single_player = lambda: self._start_game("single")
        menu.on_two_player = lambda: self._start_game("two_player")
        menu.on_settings = lambda: self._show_settings(menu)
        menu.on_quit = self.window.close

        self.window.show_view(menu)

    def _start_game(self, mode: Literal["single", "two_player"]) -> None:
        """Start a new game."""
        game_view = PongGameView(mode)
        game_view.setup()
        self.window.show_view(game_view)

    def _show_settings(self, return_view: arcade.View) -> None:
        """Show settings menu."""
        from game.ui.settings_menu import SettingsMenuView

        settings_view = SettingsMenuView()
        settings_view.on_back = lambda: self.window.show_view(return_view)
        settings_view.setup()
        self.window.show_view(settings_view)

    def _draw_center_line(self) -> None:
        """Draw dashed center line."""
        center_x = settings.screen_width / 2
        dash_height = 20
        gap_height = 15
        y = 0

        while y < settings.screen_height:
            arcade.draw.draw_line(
                center_x, y,
                center_x, y + dash_height,
                settings.center_line_color,
                line_width=2
            )
            y += dash_height + gap_height

    def _draw_scores(self) -> None:
        """Draw player scores with neon glow."""
        score_color = settings.synthwave_city_windows_cyan
        glow_color = settings.synthwave_grid_glow

        # Left score with glow
        for offset, alpha in [(4, 40), (2, 80)]:
            arcade.draw_text(
                str(self.score_left),
                settings.screen_width / 4 + offset,
                settings.screen_height - 80 - offset,
                (*glow_color, alpha),
                font_size=48,
                anchor_x="center",
                bold=True
            )
        arcade.draw_text(
            str(self.score_left),
            settings.screen_width / 4,
            settings.screen_height - 80,
            score_color,
            font_size=48,
            anchor_x="center",
            bold=True
        )

        # Right score with glow
        for offset, alpha in [(4, 40), (2, 80)]:
            arcade.draw_text(
                str(self.score_right),
                settings.screen_width * 3 / 4 + offset,
                settings.screen_height - 80 - offset,
                (*glow_color, alpha),
                font_size=48,
                anchor_x="center",
                bold=True
            )
        arcade.draw_text(
            str(self.score_right),
            settings.screen_width * 3 / 4,
            settings.screen_height - 80,
            score_color,
            font_size=48,
            anchor_x="center",
            bold=True
        )

    def _draw_game_over(self) -> None:
        """Draw game over screen."""
        # Semi-transparent overlay
        rect = arcade.types.XYWH(
            settings.screen_width / 2,
            settings.screen_height / 2,
            settings.screen_width,
            settings.screen_height
        )
        arcade.draw.draw_rect_filled(rect, (0, 0, 0, 200))

        # Game over text
        arcade.draw_text(
            "GAME OVER",
            settings.screen_width / 2,
            settings.screen_height / 2 + 100,
            (0, 255, 255),
            font_size=60,
            anchor_x="center",
            bold=True
        )

        # Winner text
        arcade.draw_text(
            f"{self.winner} WINS!",
            settings.screen_width / 2,
            settings.screen_height / 2 + 30,
            (255, 255, 100),
            font_size=40,
            anchor_x="center",
            bold=True
        )

        # Final scores
        arcade.draw_text(
            f"{self.score_left} - {self.score_right}",
            settings.screen_width / 2,
            settings.screen_height / 2 - 40,
            settings.score_color,
            font_size=48,
            anchor_x="center",
            bold=True
        )

        # Instructions
        arcade.draw_text(
            "Press ENTER to play again",
            settings.screen_width / 2,
            settings.screen_height / 2 - 120,
            (150, 150, 200),
            font_size=20,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ESC for main menu",
            settings.screen_width / 2,
            settings.screen_height / 2 - 150,
            (150, 150, 200),
            font_size=20,
            anchor_x="center"
        )
