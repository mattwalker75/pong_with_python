# Arcade 3.3.3 Migration Guide

This document details the changes made to migrate the Pong game to Arcade 3.3.3.

## Overview

Arcade 3.3.3 introduced significant API changes, particularly in the drawing functions. This migration updates all code to use the new API.

## Key API Changes

### 1. Rectangle Drawing

**Old API (Arcade < 3.0):**
```python
arcade.draw_rectangle_filled(x, y, width, height, color)
arcade.draw_rectangle_outline(x, y, width, height, color, border_width)
```

**New API (Arcade 3.3.3):**
```python
rect = arcade.types.XYWH(x, y, width, height)
arcade.draw.draw_rect_filled(rect, color)
arcade.draw.draw_rect_outline(rect, color, border_width=2)
```

### 2. Line Drawing

**Old API:**
```python
arcade.draw_line(x1, y1, x2, y2, color, width)
```

**New API:**
```python
arcade.draw.draw_line(x1, y1, x2, y2, color, line_width=2)
```

### 3. Sprite Drawing

**Old API:**
Sprites had individual `draw()` methods that were called automatically.

**New API:**
Sprites no longer have individual `draw()` methods. You must either:
- Use `arcade.draw.draw_sprite(sprite)` 
- Add custom `draw()` methods to your sprite classes

## Files Modified

### 1. `src/game/ui/components/button.py`
- Updated `draw()` method to use `arcade.types.XYWH()` and `arcade.draw.draw_rect_filled()`
- Updated border drawing to use `arcade.draw.draw_rect_outline()`

```python
# Lines 52-57
rect = arcade.types.XYWH(self.x, self.y, self.width, self.height)
arcade.draw.draw_rect_filled(rect, color)
arcade.draw.draw_rect_outline(rect, (150, 150, 255), border_width=2)
```

### 2. `src/game/paddle.py`
- Added `draw()` method using `arcade.draw.draw_sprite()`

```python
# Lines 87-89
def draw(self) -> None:
    """Draw the paddle."""
    arcade.draw.draw_sprite(self)
```

### 3. `src/game/ball.py`
- Added `draw()` method using `arcade.draw.draw_sprite()`

```python
# Lines 116-118
def draw(self) -> None:
    """Draw the ball."""
    arcade.draw.draw_sprite(self)
```

### 4. `src/game/pong_window.py`
- Updated `_draw_center_line()` to use `arcade.draw.draw_line()`
- Updated `_draw_game_over()` to use new rect API

```python
# Lines 357-361 (_draw_center_line)
arcade.draw.draw_line(
    center_x, y,
    center_x, y + dash_height,
    settings.center_line_color,
    line_width=2
)

# Lines 392-398 (_draw_game_over)
rect = arcade.types.XYWH(
    settings.screen_width / 2,
    settings.screen_height / 2,
    settings.screen_width,
    settings.screen_height
)
arcade.draw.draw_rect_filled(rect, (0, 0, 0, 200))
```

### 5. `src/game/ui/pause_menu.py`
- Updated overlay drawing to use new rect API

```python
# Lines 64-70
rect = arcade.types.XYWH(
    settings.screen_width / 2,
    settings.screen_height / 2,
    settings.screen_width,
    settings.screen_height
)
arcade.draw.draw_rect_filled(rect, (0, 0, 0, 200))
```

## Testing

All components have been tested and verified to work with Arcade 3.3.3:
- Button rendering
- Paddle and ball sprites
- Game window drawing
- Menu overlays
- Line drawing for center line

## Common Migration Patterns

### Pattern 1: Filled Rectangle
```python
# Before
arcade.draw_rectangle_filled(x, y, width, height, color)

# After
rect = arcade.types.XYWH(x, y, width, height)
arcade.draw.draw_rect_filled(rect, color)
```

### Pattern 2: Rectangle Outline
```python
# Before
arcade.draw_rectangle_outline(x, y, width, height, color, border_width)

# After
rect = arcade.types.XYWH(x, y, width, height)
arcade.draw.draw_rect_outline(rect, color, border_width=border_width)
```

### Pattern 3: Sprite Drawing
```python
# Before (sprites had built-in draw methods)
class MySprite(arcade.Sprite):
    pass

my_sprite.draw()  # Worked automatically

# After (need to add draw method)
class MySprite(arcade.Sprite):
    def draw(self) -> None:
        arcade.draw.draw_sprite(self)

my_sprite.draw()  # Now works with custom method
```

## Performance Notes

- The `arcade.draw_text()` function generates a performance warning in Arcade 3.3.3
- For frequently updated text, consider using `arcade.Text` objects instead
- For menu text that updates infrequently, `arcade.draw_text()` is acceptable

## Compatibility

This codebase now requires:
- Python 3.10 or higher
- Arcade 3.3.3 or higher

Earlier versions of Arcade are not supported.
