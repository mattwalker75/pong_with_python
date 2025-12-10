"""Audio manager for game sound effects."""
import arcade
from pathlib import Path
from game.settings import settings


class AudioManager:
    """Manages game audio and sound effects."""

    def __init__(self):
        """Initialize audio manager."""
        self.sounds = {}
        self.enabled = settings.audio_enabled
        self._load_sounds()

    def _load_sounds(self) -> None:
        """Load sound files (or create placeholder sounds)."""
        # For now, we'll use arcade's built-in sound generation
        # In production, these would load actual sound files

        # Note: Arcade can generate simple beep sounds programmatically
        # We'll create placeholder sounds that can be replaced with actual files
        pass

    def play_bounce(self) -> None:
        """Play ball bounce sound."""
        if not self.enabled:
            return

        # Play a short beep sound at a higher pitch
        arcade.play_sound(
            arcade.Sound(":resources:sounds/hit1.wav", streaming=False),
            volume=settings.master_volume * 0.3
        )

    def play_wall_bounce(self) -> None:
        """Play wall bounce sound."""
        if not self.enabled:
            return

        # Play a slightly different sound for wall bounces
        arcade.play_sound(
            arcade.Sound(":resources:sounds/hit2.wav", streaming=False),
            volume=settings.master_volume * 0.2
        )

    def play_score(self) -> None:
        """Play score sound."""
        if not self.enabled:
            return

        # Play a distinct sound for scoring
        arcade.play_sound(
            arcade.Sound(":resources:sounds/coin1.wav", streaming=False),
            volume=settings.master_volume * 0.5
        )

    def play_game_start(self) -> None:
        """Play game start sound."""
        if not self.enabled:
            return

        arcade.play_sound(
            arcade.Sound(":resources:sounds/upgrade1.wav", streaming=False),
            volume=settings.master_volume * 0.4
        )

    def play_game_end(self) -> None:
        """Play game end sound."""
        if not self.enabled:
            return

        arcade.play_sound(
            arcade.Sound(":resources:sounds/gameover1.wav", streaming=False),
            volume=settings.master_volume * 0.6
        )

    def toggle_audio(self) -> bool:
        """Toggle audio on/off.

        Returns:
            New audio state
        """
        self.enabled = not self.enabled
        settings.audio_enabled = self.enabled
        return self.enabled

    def set_volume(self, volume: float) -> None:
        """Set master volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        settings.master_volume = max(0.0, min(1.0, volume))
