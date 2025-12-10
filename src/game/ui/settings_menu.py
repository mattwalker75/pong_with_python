"""Settings menu view."""
import arcade
from typing import Optional, Callable, Literal
from game.settings import settings, update_difficulty_preset
from game.ui.components.button import Button


class SettingsMenuView(arcade.View):
    """Settings menu screen."""

    def __init__(self):
        """Initialize settings menu."""
        super().__init__()
        self.buttons = []
        self.selected_index = 0

        # Callbacks
        self.on_back: Optional[Callable] = None

        # Settings state
        self.difficulty_options: list[Literal["Easy", "Normal", "Hard"]] = [
            "Easy", "Normal", "Hard"
        ]
        self.current_difficulty_index = self.difficulty_options.index(
            settings.difficulty_preset
        )

    def setup(self) -> None:
        """Set up menu elements."""
        center_x = settings.screen_width / 2
        start_y = settings.screen_height / 2 + 100
        button_spacing = 80

        # Create settings buttons
        self.buttons = [
            Button(
                center_x, start_y, 400, 50,
                f"Difficulty: {settings.difficulty_preset}",
                self._toggle_difficulty
            ),
            Button(
                center_x, start_y - button_spacing, 400, 50,
                f"Audio: {'ON' if settings.audio_enabled else 'OFF'}",
                self._toggle_audio
            ),
            Button(
                center_x, start_y - button_spacing * 2, 400, 50,
                f"Fullscreen: {'ON' if settings.fullscreen else 'OFF'}",
                self._toggle_fullscreen
            ),
            Button(
                center_x, start_y - button_spacing * 3, 300, 50,
                "Back",
                lambda: self.on_back() if self.on_back else None
            ),
        ]

        self.buttons[0].selected = True

    def _toggle_difficulty(self) -> None:
        """Toggle difficulty setting."""
        self.current_difficulty_index = (
            (self.current_difficulty_index + 1) % len(self.difficulty_options)
        )
        new_difficulty = self.difficulty_options[self.current_difficulty_index]
        update_difficulty_preset(new_difficulty)
        self.buttons[0].text = f"Difficulty: {new_difficulty}"

    def _toggle_audio(self) -> None:
        """Toggle audio setting."""
        settings.audio_enabled = not settings.audio_enabled
        self.buttons[1].text = f"Audio: {'ON' if settings.audio_enabled else 'OFF'}"

    def _toggle_fullscreen(self) -> None:
        """Toggle fullscreen setting."""
        settings.fullscreen = not settings.fullscreen
        self.window.set_fullscreen(settings.fullscreen)
        self.buttons[2].text = f"Fullscreen: {'ON' if settings.fullscreen else 'OFF'}"

    def on_draw(self) -> None:
        """Draw the menu."""
        self.clear()
        arcade.set_background_color(settings.background_color)

        # Draw title
        arcade.draw_text(
            "SETTINGS",
            settings.screen_width / 2,
            settings.screen_height - 150,
            (0, 255, 255),
            font_size=60,
            anchor_x="center",
            bold=True
        )

        # Draw buttons
        for button in self.buttons:
            button.draw()

        # Draw controls info
        y_pos = 180
        arcade.draw_text(
            "Controls:",
            settings.screen_width / 2,
            y_pos,
            (200, 200, 255),
            font_size=24,
            anchor_x="center",
            bold=True
        )

        controls = [
            "Player 1: W (Up) / S (Down)",
            "Player 2: Arrow Up / Arrow Down",
            "Pause: ESC",
            "Fullscreen Toggle: F11"
        ]

        for i, control in enumerate(controls):
            arcade.draw_text(
                control,
                settings.screen_width / 2,
                y_pos - 40 - (i * 25),
                (150, 150, 200),
                font_size=14,
                anchor_x="center"
            )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle key presses.

        Args:
            key: Key that was pressed
            modifiers: Modifier keys held
        """
        if key == arcade.key.UP:
            self.buttons[self.selected_index].selected = False
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
            self.buttons[self.selected_index].selected = True

        elif key == arcade.key.DOWN:
            self.buttons[self.selected_index].selected = False
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
            self.buttons[self.selected_index].selected = True

        elif key == arcade.key.ENTER:
            self.buttons[self.selected_index].on_click()

        elif key == arcade.key.ESCAPE:
            if self.on_back:
                self.on_back()

        elif key == arcade.key.F11:
            self._toggle_fullscreen()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        """Handle mouse motion.

        Args:
            x: Mouse x position
            y: Mouse y position
            dx: Change in x
            dy: Change in y
        """
        for i, button in enumerate(self.buttons):
            button.hovered = button.is_point_inside(x, y)
            if button.hovered and not button.selected:
                self.buttons[self.selected_index].selected = False
                self.selected_index = i
                button.selected = True

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Handle mouse clicks.

        Args:
            x: Mouse x position
            y: Mouse y position
            button: Mouse button pressed
            modifiers: Modifier keys held
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            for btn in self.buttons:
                if btn.is_point_inside(x, y):
                    btn.on_click()
                    break
