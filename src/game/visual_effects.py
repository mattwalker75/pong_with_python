"""Visual effects system for glow, trails, and synthwave aesthetics."""
import arcade
import math
from collections import deque
from typing import Deque
from game.settings import settings


class GlowEffect:
    """Renders radial glow effects around objects."""

    @staticmethod
    def draw_radial_glow(
        center_x: float,
        center_y: float,
        radius: float,
        core_color: tuple[int, int, int],
        glow_color: tuple[int, int, int],
        intensity: float = 1.0
    ) -> None:
        """Draw a radial glow effect.

        Args:
            center_x: X position of glow center
            center_y: Y position of glow center
            radius: Base radius
            core_color: Core object color
            glow_color: Glow halo color
            intensity: Glow intensity multiplier
        """
        adjusted_intensity = intensity * settings.glow_intensity

        # Draw multiple expanding circles with decreasing opacity for glow
        glow_layers = [
            (radius * 3.0, 20 * adjusted_intensity),
            (radius * 2.5, 40 * adjusted_intensity),
            (radius * 2.0, 60 * adjusted_intensity),
            (radius * 1.5, 100 * adjusted_intensity),
            (radius * 1.2, 150 * adjusted_intensity)
        ]

        for layer_radius, alpha in glow_layers:
            color_with_alpha = (*glow_color, int(alpha))
            arcade.draw_circle_filled(
                center_x, center_y,
                layer_radius,
                color_with_alpha
            )

        # Draw bright core
        arcade.draw_circle_filled(center_x, center_y, radius, core_color)

    @staticmethod
    def draw_rectangular_glow(
        center_x: float,
        center_y: float,
        width: float,
        height: float,
        core_color: tuple[int, int, int],
        glow_color: tuple[int, int, int],
        intensity: float = 1.0
    ) -> None:
        """Draw a rectangular glow effect (for paddles).

        Args:
            center_x: X position of rectangle center
            center_y: Y position of rectangle center
            width: Rectangle width
            height: Rectangle height
            core_color: Core object color
            glow_color: Glow halo color
            intensity: Glow intensity multiplier
        """
        adjusted_intensity = intensity * settings.glow_intensity

        # Draw multiple expanding rectangles with decreasing opacity
        glow_layers = [
            (width + 30, height + 30, 20 * adjusted_intensity),
            (width + 20, height + 20, 40 * adjusted_intensity),
            (width + 15, height + 15, 60 * adjusted_intensity),
            (width + 10, height + 10, 100 * adjusted_intensity),
            (width + 5, height + 5, 150 * adjusted_intensity)
        ]

        for layer_width, layer_height, alpha in glow_layers:
            color_with_alpha = (*glow_color, int(alpha))
            rect = arcade.types.XYWH(center_x, center_y, layer_width, layer_height)
            arcade.draw.draw_rect_filled(rect, color_with_alpha)

        # Draw bright core rectangle
        core_rect = arcade.types.XYWH(center_x, center_y, width, height)
        arcade.draw.draw_rect_filled(core_rect, core_color)

        # Add edge highlighting for 3D effect
        edge_highlight = tuple(min(c + 50, 255) for c in core_color)
        arcade.draw.draw_rect_outline(core_rect, edge_highlight, border_width=2)


class MotionTrail:
    """Manages motion blur trail effect for moving objects."""

    def __init__(self, max_length: int = 15):
        """Initialize motion trail.

        Args:
            max_length: Maximum number of trail segments
        """
        self.max_length = max_length
        self.positions: Deque[tuple[float, float]] = deque(maxlen=max_length)

    def update(self, x: float, y: float) -> None:
        """Update trail with new position.

        Args:
            x: Current x position
            y: Current y position
        """
        self.positions.append((x, y))

    def draw(
        self,
        radius: float,
        core_color: tuple[int, int, int],
        trail_color: tuple[int, int, int]
    ) -> None:
        """Draw the motion trail.

        Args:
            radius: Base radius of trail segments
            core_color: Color of most recent segment
            trail_color: Color of older segments
        """
        if not settings.motion_blur_enabled or len(self.positions) < 2:
            return

        # Draw trail segments from oldest to newest
        for i, (x, y) in enumerate(self.positions):
            # Calculate fade factor (older = more transparent)
            age_ratio = i / len(self.positions)
            alpha = int(200 * age_ratio)  # 0 to 200 opacity

            # Interpolate between trail color and core color
            r = int(trail_color[0] + (core_color[0] - trail_color[0]) * age_ratio)
            g = int(trail_color[1] + (core_color[1] - trail_color[1]) * age_ratio)
            b = int(trail_color[2] + (core_color[2] - trail_color[2]) * age_ratio)

            # Scale radius based on age (older = smaller)
            segment_radius = radius * (0.5 + 0.5 * age_ratio)

            # Draw trail segment
            arcade.draw_circle_filled(
                x, y,
                segment_radius,
                (*((r, g, b)), alpha)
            )

    def clear(self) -> None:
        """Clear all trail positions."""
        self.positions.clear()


class ParticleEffect:
    """Simple particle system for impact effects."""

    def __init__(self):
        """Initialize particle system."""
        self.particles: list[dict] = []

    def emit_burst(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        count: int = 8
    ) -> None:
        """Emit a burst of particles.

        Args:
            x: Emission position x
            y: Emission position y
            color: Particle color
            count: Number of particles
        """
        for i in range(count):
            angle = (2 * math.pi * i) / count
            speed = 3.0

            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': color,
                'life': 1.0,  # 1.0 = full life, 0.0 = dead
                'size': 3.0
            })

    def update(self, delta_time: float) -> None:
        """Update particle positions and lifetimes.

        Args:
            delta_time: Time since last update
        """
        for particle in self.particles[:]:
            # Update position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']

            # Apply drag
            particle['vx'] *= 0.95
            particle['vy'] *= 0.95

            # Decrease life
            particle['life'] -= delta_time * 2.0

            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw(self) -> None:
        """Draw all active particles."""
        for particle in self.particles:
            alpha = int(255 * particle['life'])
            size = particle['size'] * particle['life']
            color = (*particle['color'], alpha)

            arcade.draw_circle_filled(
                particle['x'],
                particle['y'],
                size,
                color
            )
