"""Synthwave background renderer with city skyline and perspective grid."""
import arcade
import random
import math
from game.settings import settings


class BackgroundRenderer:
    """Renders synthwave-themed background with stars, city, and grid."""

    def __init__(self, width: int, height: int):
        """Initialize background renderer.

        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height
        self.stars = self._generate_stars()
        self.buildings = self._generate_buildings()

    def _generate_stars(self) -> list[tuple[float, float, float]]:
        """Generate random star positions and sizes.

        Returns:
            List of (x, y, size) tuples for each star
        """
        stars = []
        for _ in range(settings.star_count):
            x = random.uniform(0, self.width)
            y = random.uniform(self.height * 0.5, self.height)  # Stars in upper half
            size = random.uniform(0.5, 2.5)
            stars.append((x, y, size))
        return stars

    def _generate_buildings(self) -> list[dict]:
        """Generate city skyline buildings.

        Returns:
            List of building dictionaries with position and window data
        """
        buildings = []
        x_pos = 0
        horizon_y = self.height * 0.4  # Buildings below this line

        while x_pos < self.width:
            # Random building dimensions
            building_width = random.randint(60, 120)
            building_height = random.randint(80, 200)

            # Random window pattern
            window_rows = random.randint(5, 12)
            window_cols = random.randint(3, 6)

            # Random accent color for windows
            accent_colors = [
                settings.synthwave_city_windows_cyan,
                settings.synthwave_city_windows_pink,
                settings.synthwave_city_windows_orange
            ]
            accent_color = random.choice(accent_colors)

            buildings.append({
                'x': x_pos,
                'width': building_width,
                'height': building_height,
                'horizon_y': horizon_y,  # Store horizon instead of pre-calculated y
                'window_rows': window_rows,
                'window_cols': window_cols,
                'accent_color': accent_color
            })

            x_pos += building_width + random.randint(10, 30)  # Gap between buildings

        return buildings

    def draw(self) -> None:
        """Draw the complete synthwave background."""
        self._draw_sky_gradient()
        self._draw_stars()
        self._draw_city_skyline()
        self._draw_perspective_grid()

    def _draw_sky_gradient(self) -> None:
        """Draw vertical gradient sky from deep blue to purple."""
        # Draw as horizontal strips for smooth gradient
        num_strips = 100
        strip_height = self.height / num_strips

        sky_top = settings.synthwave_sky_top
        sky_bottom = settings.synthwave_sky_bottom

        for i in range(num_strips):
            # Interpolate between top and bottom colors
            ratio = i / num_strips
            r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * ratio)
            g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * ratio)
            b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * ratio)

            y = self.height - (i * strip_height)

            rect = arcade.types.XYWH(
                self.width / 2,
                y - strip_height / 2,
                self.width,
                strip_height
            )
            arcade.draw.draw_rect_filled(rect, (r, g, b))

    def _draw_stars(self) -> None:
        """Draw twinkling stars in the background."""
        for x, y, size in self.stars:
            # Slight brightness variation for twinkling effect
            brightness = random.uniform(0.6, 1.0)
            color = tuple(int(255 * brightness) for _ in range(3))
            arcade.draw_circle_filled(x, y, size, color)

    def _draw_city_skyline(self) -> None:
        """Draw cyberpunk city skyline with neon windows."""
        for building in self.buildings:
            # Calculate building position
            # The building should sit ON the horizon, extending upward
            # Center Y = horizon + (height / 2) so bottom edge is at horizon
            center_y = building['horizon_y'] + building['height'] / 2
            center_x = building['x'] + building['width'] / 2

            # Draw building base
            rect = arcade.types.XYWH(
                center_x,
                center_y,
                building['width'],
                building['height']
            )
            arcade.draw.draw_rect_filled(rect, settings.synthwave_city_base)

            # Draw neon outline
            arcade.draw.draw_rect_outline(
                rect,
                building['accent_color'],
                border_width=2
            )

            # Draw windows
            window_width = building['width'] / (building['window_cols'] + 1)
            window_height = building['height'] / (building['window_rows'] + 1)
            window_size_w = window_width * 0.4
            window_size_h = window_height * 0.5

            # Calculate window positions relative to building's bottom (at horizon)
            building_bottom = building['horizon_y']
            building_left = building['x']

            for row in range(building['window_rows']):
                for col in range(building['window_cols']):
                    # Random chance for window to be lit
                    if random.random() < 0.7:
                        # Windows start from bottom and go up
                        window_x = building_left + (col + 1) * window_width
                        window_y = building_bottom + (row + 1) * window_height

                        window_rect = arcade.types.XYWH(
                            window_x,
                            window_y,
                            window_size_w,
                            window_size_h
                        )
                        arcade.draw.draw_rect_filled(
                            window_rect,
                            building['accent_color']
                        )

    def _draw_perspective_grid(self) -> None:
        """Draw perspective grid floor in synthwave style."""
        horizon_y = self.height * 0.4
        grid_bottom = 0
        grid_top = horizon_y

        # Vertical lines (receding into distance)
        num_vertical_lines = 20
        for i in range(num_vertical_lines + 1):
            # Lines converge toward center
            x_top = self.width / 2 + (i - num_vertical_lines / 2) * (self.width / num_vertical_lines) * settings.grid_perspective_depth
            x_bottom = self.width / 2 + (i - num_vertical_lines / 2) * (self.width / num_vertical_lines)

            # Draw line with glow effect
            self._draw_glowing_line(
                x_bottom, grid_bottom,
                x_top, grid_top,
                settings.synthwave_grid_color,
                settings.synthwave_grid_glow,
                line_width=2
            )

        # Horizontal lines (parallel, evenly spaced)
        num_horizontal_lines = 15
        for i in range(num_horizontal_lines + 1):
            # Perspective scaling - lines closer together near horizon
            ratio = i / num_horizontal_lines
            # Non-linear spacing for perspective effect
            perspective_ratio = ratio ** 2
            y = grid_bottom + perspective_ratio * (grid_top - grid_bottom)

            # Draw line with glow effect
            self._draw_glowing_line(
                0, y,
                self.width, y,
                settings.synthwave_grid_color,
                settings.synthwave_grid_glow,
                line_width=2
            )

    def _draw_glowing_line(
        self,
        x1: float, y1: float,
        x2: float, y2: float,
        core_color: tuple[int, int, int],
        glow_color: tuple[int, int, int],
        line_width: int = 2
    ) -> None:
        """Draw a line with a glowing effect.

        Args:
            x1, y1: Start position
            x2, y2: End position
            core_color: Main line color
            glow_color: Glow halo color
            line_width: Line thickness
        """
        # Draw glow layers (outer to inner)
        glow_layers = [
            (line_width + 6, (*glow_color, 30)),
            (line_width + 4, (*glow_color, 60)),
            (line_width + 2, (*glow_color, 100))
        ]

        for width, color in glow_layers:
            arcade.draw_line(x1, y1, x2, y2, color, width)

        # Draw core line
        arcade.draw_line(x1, y1, x2, y2, core_color, line_width)
