"""Controls configuration menu view."""
import arcade
from typing import Optional, Callable, Literal
from game.settings import settings, save_settings, ControlMapping
from game.ui.components.button import Button


class ControlsMenuView(arcade.View):
    """Controls configuration screen."""

    def __init__(self):
        """Initialize controls menu."""
        super().__init__()
        self.buttons = []
        self.selected_index = 0

        # Callbacks
        self.on_back: Optional[Callable] = None

        # State for control remapping
        self.remapping_mode: Optional[Literal["single_up", "single_down", "p1_up", "p1_down", "p2_up", "p2_down"]] = None

    def setup(self) -> None:
        """Set up menu elements."""
        center_x = settings.screen_width / 2
        start_y = settings.screen_height / 2 + 140
        button_spacing = 60

        # Get key names for display
        single_up_key = arcade.key.key_to_string(settings.single_player_controls.up)
        single_down_key = arcade.key.key_to_string(settings.single_player_controls.down)
        p1_up_key = arcade.key.key_to_string(settings.two_player_p1_controls.up)
        p1_down_key = arcade.key.key_to_string(settings.two_player_p1_controls.down)
        p2_up_key = arcade.key.key_to_string(settings.two_player_p2_controls.up)
        p2_down_key = arcade.key.key_to_string(settings.two_player_p2_controls.down)

        # Create controls buttons
        self.buttons = [
            Button(
                center_x, start_y, 500, 50,
                f"Single Player Up: {single_up_key}",
                lambda: self._start_remap("single_up")
            ),
            Button(
                center_x, start_y - button_spacing, 500, 50,
                f"Single Player Down: {single_down_key}",
                lambda: self._start_remap("single_down")
            ),
            Button(
                center_x, start_y - button_spacing * 2, 500, 50,
                f"Two Player P1 Up: {p1_up_key}",
                lambda: self._start_remap("p1_up")
            ),
            Button(
                center_x, start_y - button_spacing * 3, 500, 50,
                f"Two Player P1 Down: {p1_down_key}",
                lambda: self._start_remap("p1_down")
            ),
            Button(
                center_x, start_y - button_spacing * 4, 500, 50,
                f"Two Player P2 Up: {p2_up_key}",
                lambda: self._start_remap("p2_up")
            ),
            Button(
                center_x, start_y - button_spacing * 5, 500, 50,
                f"Two Player P2 Down: {p2_down_key}",
                lambda: self._start_remap("p2_down")
            ),
            Button(
                center_x, start_y - button_spacing * 6.5, 300, 50,
                "Back",
                lambda: self.on_back() if self.on_back else None
            ),
        ]

        self.buttons[0].selected = True

    def _start_remap(self, control: Literal["single_up", "single_down", "p1_up", "p1_down", "p2_up", "p2_down"]) -> None:
        """Start remapping a control.

        Args:
            control: Which control to remap
        """
        self.remapping_mode = control

    def _update_button_text(self) -> None:
        """Update button text to reflect current key bindings."""
        self.buttons[0].text = f"Single Player Up: {arcade.key.key_to_string(settings.single_player_controls.up)}"
        self.buttons[1].text = f"Single Player Down: {arcade.key.key_to_string(settings.single_player_controls.down)}"
        self.buttons[2].text = f"Two Player P1 Up: {arcade.key.key_to_string(settings.two_player_p1_controls.up)}"
        self.buttons[3].text = f"Two Player P1 Down: {arcade.key.key_to_string(settings.two_player_p1_controls.down)}"
        self.buttons[4].text = f"Two Player P2 Up: {arcade.key.key_to_string(settings.two_player_p2_controls.up)}"
        self.buttons[5].text = f"Two Player P2 Down: {arcade.key.key_to_string(settings.two_player_p2_controls.down)}"

    def on_draw(self) -> None:
        """Draw the menu."""
        self.clear()
        arcade.set_background_color(settings.background_color)

        # Draw title
        arcade.draw_text(
            "CONTROLS",
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

        # Draw remapping prompt
        if self.remapping_mode:
            # Semi-transparent overlay
            rect = arcade.types.XYWH(
                settings.screen_width / 2,
                settings.screen_height / 2,
                settings.screen_width,
                settings.screen_height
            )
            arcade.draw.draw_rect_filled(rect, (0, 0, 0, 200))

            # Prompt text
            arcade.draw_text(
                "Press any key to remap...",
                settings.screen_width / 2,
                settings.screen_height / 2 + 40,
                (0, 255, 255),
                font_size=40,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                "Press ESC to cancel",
                settings.screen_width / 2,
                settings.screen_height / 2 - 20,
                (150, 150, 200),
                font_size=20,
                anchor_x="center"
            )

        # Draw info text
        else:
            arcade.draw_text(
                "Click a button or press ENTER to remap a control",
                settings.screen_width / 2,
                100,
                (150, 150, 200),
                font_size=16,
                anchor_x="center"
            )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle key presses.

        Args:
            key: Key that was pressed
            modifiers: Modifier keys held
        """
        # Handle remapping mode
        if self.remapping_mode:
            if key == arcade.key.ESCAPE:
                # Cancel remapping
                self.remapping_mode = None
            else:
                # Remap the control
                if self.remapping_mode == "single_up":
                    settings.single_player_controls = ControlMapping(
                        up=key,
                        down=settings.single_player_controls.down
                    )
                elif self.remapping_mode == "single_down":
                    settings.single_player_controls = ControlMapping(
                        up=settings.single_player_controls.up,
                        down=key
                    )
                elif self.remapping_mode == "p1_up":
                    settings.two_player_p1_controls = ControlMapping(
                        up=key,
                        down=settings.two_player_p1_controls.down
                    )
                elif self.remapping_mode == "p1_down":
                    settings.two_player_p1_controls = ControlMapping(
                        up=settings.two_player_p1_controls.up,
                        down=key
                    )
                elif self.remapping_mode == "p2_up":
                    settings.two_player_p2_controls = ControlMapping(
                        up=key,
                        down=settings.two_player_p2_controls.down
                    )
                elif self.remapping_mode == "p2_down":
                    settings.two_player_p2_controls = ControlMapping(
                        up=settings.two_player_p2_controls.up,
                        down=key
                    )

                # Save settings and update button text
                save_settings()
                self._update_button_text()
                self.remapping_mode = None
            return

        # Normal navigation
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

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        """Handle mouse motion.

        Args:
            x: Mouse x position
            y: Mouse y position
            dx: Change in x
            dy: Change in y
        """
        # Don't handle mouse events during remapping
        if self.remapping_mode:
            return

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
        # Don't handle mouse events during remapping
        if self.remapping_mode:
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            for btn in self.buttons:
                if btn.is_point_inside(x, y):
                    btn.on_click()
                    break
