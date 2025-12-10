"""Button component for menus."""
import arcade


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

        # Colors
        self.normal_color = (50, 50, 100)
        self.hover_color = (80, 80, 150)
        self.selected_color = (100, 200, 255)
        self.text_color = (200, 200, 255)

    def draw(self) -> None:
        """Draw the button."""
        # Choose color based on state
        if self.selected:
            color = self.selected_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.normal_color

        # Draw button background
        rect = arcade.types.XYWH(self.x, self.y, self.width, self.height)
        arcade.draw.draw_rect_filled(rect, color)

        # Draw border
        arcade.draw.draw_rect_outline(rect, (150, 150, 255), border_width=2)

        # Draw text
        arcade.draw_text(
            self.text,
            self.x,
            self.y,
            self.text_color,
            font_size=18,
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
