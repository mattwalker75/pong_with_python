"""Audio manager for game sound effects."""
import arcade
from pathlib import Path
from game.settings import settings
import pyglet.media


class AudioManager:
    """Manages game audio and sound effects."""

    def __init__(self):
        """Initialize audio manager."""
        self.sounds = {}
        self.music_player = None
        self.music_source = None
        self.enabled = settings.audio_enabled
        print("[AUDIO] Initializing audio manager...")
        print(f"[AUDIO] Audio enabled: {self.enabled}")
        self._load_sounds()
        self._load_music()
        print(f"[AUDIO] Loaded {len(self.sounds)} sound effects")

    def _load_sounds(self) -> None:
        """Load sound files."""
        sounds_dir = Path(__file__).parent.parent / "assets" / "sounds"

        # Load custom sound effects using pyglet directly
        sound_files = {
            'paddle_hit': 'paddle_hit.wav',
            'wall_hit': 'wall_hit.wav',
            'score': 'score.wav',
            'game_start': 'game_start.wav',
            'game_over': 'game_over.wav',
        }

        for sound_name, filename in sound_files.items():
            sound_path = sounds_dir / filename
            if sound_path.exists():
                try:
                    # Load using pyglet for better macOS compatibility
                    self.sounds[sound_name] = pyglet.media.load(str(sound_path), streaming=False)
                    print(f"[AUDIO] Loaded {sound_name}: {self.sounds[sound_name]}")
                except Exception as e:
                    print(f"[AUDIO] Warning: Could not load {filename}: {e}")
            else:
                print(f"[AUDIO] Warning: Sound file not found: {sound_path}")

    def _load_music(self) -> None:
        """Load and start background music."""
        if not self.enabled:
            return

        sounds_dir = Path(__file__).parent.parent / "assets" / "sounds"
        music_path = sounds_dir / "background_music.wav"

        if music_path.exists():
            try:
                # Load music using pyglet directly for better control
                self.music_source = pyglet.media.load(str(music_path), streaming=False)
                print(f"[AUDIO] Background music loaded: {self.music_source}")
            except Exception as e:
                print(f"[AUDIO] Warning: Could not load background music: {e}")

    def play_background_music(self) -> None:
        """Start playing background music."""
        if not self.enabled or not self.music_source:
            print(f"[AUDIO] Background music not playing - enabled: {self.enabled}, source: {self.music_source}")
            return

        # Create a player and set it to loop
        print(f"[AUDIO] Creating music player...")
        self.music_player = pyglet.media.Player()
        self.music_player.queue(self.music_source)
        self.music_player.loop = True
        self.music_player.volume = settings.master_volume * 0.3

        print(f"[AUDIO] Starting background music (volume: {self.music_player.volume})")
        self.music_player.play()
        print(f"[AUDIO] Music player playing: {self.music_player.playing}")

    def stop_background_music(self) -> None:
        """Stop background music."""
        if self.music_player:
            print("[AUDIO] Stopping background music...")
            self.music_player.pause()
            self.music_player = None

    def play_bounce(self) -> None:
        """Play ball bounce sound (paddle hit)."""
        if not self.enabled:
            return

        if 'paddle_hit' in self.sounds:
            volume = settings.master_volume * 0.6
            print(f"[AUDIO] Playing paddle hit (volume: {volume})")
            try:
                # Use StaticSource.play() - simplest method
                player = self.sounds['paddle_hit'].play()
                if player:
                    player.volume = volume
                    print(f"[AUDIO] Paddle hit playing, volume set to {player.volume}")
                else:
                    print(f"[AUDIO] Warning: paddle_hit.play() returned None")
            except Exception as e:
                print(f"[AUDIO] Error playing paddle hit: {e}")

    def play_wall_bounce(self) -> None:
        """Play wall bounce sound."""
        if not self.enabled:
            return

        if 'wall_hit' in self.sounds:
            volume = settings.master_volume * 0.5
            try:
                player = self.sounds['wall_hit'].play()
                if player:
                    player.volume = volume
            except Exception as e:
                print(f"[AUDIO] Error playing wall hit: {e}")

    def play_score(self) -> None:
        """Play score sound."""
        if not self.enabled:
            return

        if 'score' in self.sounds:
            volume = settings.master_volume * 0.7
            print(f"[AUDIO] Playing score (volume: {volume})")
            try:
                player = self.sounds['score'].play()
                if player:
                    player.volume = volume
            except Exception as e:
                print(f"[AUDIO] Error playing score: {e}")

    def play_game_start(self) -> None:
        """Play game start sound."""
        if not self.enabled:
            return

        if 'game_start' in self.sounds:
            volume = settings.master_volume * 0.6
            print(f"[AUDIO] Playing game start (volume: {volume})")
            try:
                player = self.sounds['game_start'].play()
                if player:
                    player.volume = volume
            except Exception as e:
                print(f"[AUDIO] Error playing game start: {e}")

    def play_game_end(self) -> None:
        """Play game end sound."""
        if not self.enabled:
            return

        if 'game_over' in self.sounds:
            volume = settings.master_volume * 0.8
            print(f"[AUDIO] Playing game over (volume: {volume})")
            try:
                player = self.sounds['game_over'].play()
                if player:
                    player.volume = volume
            except Exception as e:
                print(f"[AUDIO] Error playing game over: {e}")

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
