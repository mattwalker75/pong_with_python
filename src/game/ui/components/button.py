"""Button component for menus."""
import arcade
from game.settings import settings


class Button:
    """Simple button for menu interfaces."""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        text: str,
        action=None
    ):
        """Initialize button.

        Args:
            x: X position (center)
            y: Y position (center)
            width: Button width
            height: Button height
            text: Button text
            action: Callback function when clicked
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.selected = False
        self.hovered = False

        # Synthwave colors
        self.normal_color = (20, 20, 40)
        self.hover_color = (40, 20, 60)
        self.selected_color = (60, 30, 80)
        self.border_normal = settings.synthwave_grid_color
        self.border_selected = settings.synthwave_city_windows_cyan
        self.text_color = (255, 255, 255)
        self.glow_color = settings.synthwave_grid_glow

    def draw(self) -> None:
        """Draw the button with synthwave neon glow."""
        # Choose color based on state
        if self.selected:
            color = self.selected_color
            border_color = self.border_selected
            has_glow = True
        elif self.hovered:
            color = self.hover_color
            border_color = self.glow_color
            has_glow = True
        else:
            color = self.normal_color
            border_color = self.border_normal
            has_glow = False

        # Draw glow layers if selected/hovered
        if has_glow:
            glow_layers = [
                (self.width + 20, self.height + 20, 20),
                (self.width + 15, self.height + 15, 40),
                (self.width + 10, self.height + 10, 60),
                (self.width + 5, self.height + 5, 100)
            ]
            for glow_w, glow_h, alpha in glow_layers:
                glow_color = (*border_color, alpha)
                glow_rect = arcade.types.XYWH(self.x, self.y, glow_w, glow_h)
                arcade.draw.draw_rect_filled(glow_rect, glow_color)

        # Draw button background
        btn_rect = arcade.types.XYWH(self.x, self.y, self.width, self.height)
        arcade.draw.draw_rect_filled(btn_rect, color)

        # Draw border
        arcade.draw.draw_rect_outline(
            btn_rect,
            border_color,
            border_width=3 if self.selected else 2
        )

        # Draw text with subtle glow if selected
        if self.selected:
            # Text glow
            arcade.draw_text(
                self.text,
                self.x,
                self.y,
                (*self.border_selected, 100),
                font_size=20,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

        # Draw main text
        arcade.draw_text(
            self.text,
            self.x,
            self.y,
            self.text_color,
            font_size=18 if not self.selected else 20,
            anchor_x="center",
            anchor_y="center",
            bold=self.selected
        )

    def is_point_inside(self, x: float, y: float) -> bool:
        """Check if a point is inside the button.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if point is inside button
        """
        return (
            self.x - self.width / 2 <= x <= self.x + self.width / 2 and
            self.y - self.height / 2 <= y <= self.y + self.height / 2
        )

    def on_click(self) -> None:
        """Handle button click."""
        if self.action:
            self.action()
