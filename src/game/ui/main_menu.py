"""Main menu view."""
import arcade
from typing import Optional, Callable
from game.settings import settings
from game.ui.components.button import Button


class MainMenuView(arcade.View):
    """Main menu screen."""

    def __init__(self):
        """Initialize main menu."""
        super().__init__()
        self.buttons = []
        self.selected_index = 0
        self.title = "PONG"

        # Callbacks
        self.on_single_player: Optional[Callable] = None
        self.on_two_player: Optional[Callable] = None
        self.on_settings: Optional[Callable] = None
        self.on_quit: Optional[Callable] = None

    def setup(self) -> None:
        """Set up menu elements."""
        center_x = settings.screen_width / 2
        start_y = settings.screen_height / 2 - 50
        button_spacing = 70

        # Create menu buttons
        self.buttons = [
            Button(
                center_x, start_y, 300, 50,
                "Single Player",
                lambda: self.on_single_player() if self.on_single_player else None
            ),
            Button(
                center_x, start_y - button_spacing, 300, 50,
                "Two Players",
                lambda: self.on_two_player() if self.on_two_player else None
            ),
            Button(
                center_x, start_y - button_spacing * 2, 300, 50,
                "Settings",
                lambda: self.on_settings() if self.on_settings else None
            ),
            Button(
                center_x, start_y - button_spacing * 3, 300, 50,
                "Quit",
                lambda: self.on_quit() if self.on_quit else None
            ),
        ]

        self.buttons[0].selected = True

    def on_draw(self) -> None:
        """Draw the menu."""
        self.clear()
        arcade.set_background_color(settings.background_color)

        # Draw title
        arcade.draw_text(
            self.title,
            settings.screen_width / 2,
            settings.screen_height - 150,
            (0, 255, 255),
            font_size=80,
            anchor_x="center",
            bold=True
        )

        # Draw subtitle
        arcade.draw_text(
            "Arcade Edition",
            settings.screen_width / 2,
            settings.screen_height - 210,
            (200, 200, 255),
            font_size=24,
            anchor_x="center"
        )

        # Draw buttons
        for button in self.buttons:
            button.draw()

        # Draw controls hint
        arcade.draw_text(
            "Use Arrow Keys and Enter to select",
            settings.screen_width / 2,
            50,
            (100, 100, 150),
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
            if self.on_quit:
                self.on_quit()

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
