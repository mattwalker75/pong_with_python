"""Pause menu overlay."""
import arcade
from typing import Optional, Callable
from game.settings import settings
from game.ui.components.button import Button


class PauseMenu:
    """Pause menu overlay."""

    def __init__(self):
        """Initialize pause menu."""
        self.buttons = []
        self.selected_index = 0
        self.visible = False

        # Callbacks
        self.on_resume: Optional[Callable] = None
        self.on_quit: Optional[Callable] = None

        self._setup_buttons()

    def _setup_buttons(self) -> None:
        """Set up menu buttons."""
        center_x = settings.screen_width / 2
        center_y = settings.screen_height / 2
        button_spacing = 70

        self.buttons = [
            Button(
                center_x, center_y + button_spacing / 2, 300, 50,
                "Resume",
                lambda: self.on_resume() if self.on_resume else None
            ),
            Button(
                center_x, center_y - button_spacing / 2, 300, 50,
                "Quit to Menu",
                lambda: self.on_quit() if self.on_quit else None
            ),
        ]

        self.buttons[0].selected = True

    def show(self) -> None:
        """Show the pause menu."""
        self.visible = True

    def hide(self) -> None:
        """Hide the pause menu."""
        self.visible = False

    def draw(self) -> None:
        """Draw the pause menu."""
        if not self.visible:
            return

        # Draw semi-transparent overlay
        rect = arcade.types.XYWH(
            settings.screen_width / 2,
            settings.screen_height / 2,
            settings.screen_width,
            settings.screen_height
        )
        arcade.draw.draw_rect_filled(rect, (0, 0, 0, 200))

        # Draw pause title
        arcade.draw_text(
            "PAUSED",
            settings.screen_width / 2,
            settings.screen_height / 2 + 200,
            (0, 255, 255),
            font_size=60,
            anchor_x="center",
            bold=True
        )

        # Draw buttons
        for button in self.buttons:
            button.draw()

    def handle_key_press(self, key: int) -> bool:
        """Handle key presses.

        Args:
            key: Key that was pressed

        Returns:
            True if key was handled
        """
        if not self.visible:
            return False

        if key == arcade.key.UP:
            self.buttons[self.selected_index].selected = False
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
            self.buttons[self.selected_index].selected = True
            return True

        elif key == arcade.key.DOWN:
            self.buttons[self.selected_index].selected = False
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
            self.buttons[self.selected_index].selected = True
            return True

        elif key == arcade.key.ENTER:
            self.buttons[self.selected_index].on_click()
            return True

        elif key == arcade.key.ESCAPE:
            if self.on_resume:
                self.on_resume()
            return True

        return False

    def handle_mouse_motion(self, x: float, y: float) -> bool:
        """Handle mouse motion.

        Args:
            x: Mouse x position
            y: Mouse y position

        Returns:
            True if mouse is over menu
        """
        if not self.visible:
            return False

        for i, button in enumerate(self.buttons):
            button.hovered = button.is_point_inside(x, y)
            if button.hovered and not button.selected:
                self.buttons[self.selected_index].selected = False
                self.selected_index = i
                button.selected = True

        return True

    def handle_mouse_press(self, x: float, y: float) -> bool:
        """Handle mouse clicks.

        Args:
            x: Mouse x position
            y: Mouse y position

        Returns:
            True if click was on menu
        """
        if not self.visible:
            return False

        for button in self.buttons:
            if button.is_point_inside(x, y):
                button.on_click()
                return True

        return False
