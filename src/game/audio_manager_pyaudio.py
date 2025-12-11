"""Alternative audio manager using PyAudio for macOS compatibility."""
import wave
from pathlib import Path
from game.settings import settings
import threading

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("[AUDIO] PyAudio not available - install with: pip install pyaudio")


class PyAudioManager:
    """Audio manager using PyAudio for better macOS compatibility."""

    def __init__(self):
        """Initialize PyAudio audio manager."""
        self.enabled = settings.audio_enabled
        self.sounds = {}
        self.music_thread = None
        self.music_stop_flag = False

        print("[AUDIO] Initializing PyAudio manager...")
        print(f"[AUDIO] PyAudio available: {PYAUDIO_AVAILABLE}")
        print(f"[AUDIO] Audio enabled: {self.enabled}")

        if not PYAUDIO_AVAILABLE:
            self.enabled = False
            print("[AUDIO] Disabling audio - PyAudio not installed")
            return

        try:
            self.pa = pyaudio.PyAudio()
            print(f"[AUDIO] PyAudio initialized: {self.pa}")
            self._load_sounds()
        except Exception as e:
            print(f"[AUDIO] Error initializing PyAudio: {e}")
            self.enabled = False

    def _load_sounds(self) -> None:
        """Load sound files into memory."""
        sounds_dir = Path(__file__).parent.parent / "assets" / "sounds"

        sound_files = {
            'paddle_hit': 'paddle_hit.wav',
            'wall_hit': 'wall_hit.wav',
            'score': 'score.wav',
            'game_start': 'game_start.wav',
            'game_over': 'game_over.wav',
            'background_music': 'background_music.wav',
        }

        for sound_name, filename in sound_files.items():
            sound_path = sounds_dir / filename
            if sound_path.exists():
                try:
                    # Load WAV file into memory
                    with wave.open(str(sound_path), 'rb') as wf:
                        frames = wf.readframes(wf.getnframes())
                        self.sounds[sound_name] = {
                            'data': frames,
                            'channels': wf.getnchannels(),
                            'sample_width': wf.getsampwidth(),
                            'framerate': wf.getframerate(),
                        }
                    print(f"[AUDIO] Loaded {sound_name}: {len(frames)} bytes")
                except Exception as e:
                    print(f"[AUDIO] Warning: Could not load {filename}: {e}")
            else:
                print(f"[AUDIO] Warning: Sound file not found: {sound_path}")

    def _play_sound(self, sound_name: str, volume: float = 1.0) -> None:
        """Play a sound effect.

        Args:
            sound_name: Name of the sound to play
            volume: Volume level (0.0 to 1.0)
        """
        if not self.enabled or sound_name not in self.sounds:
            return

        sound = self.sounds[sound_name]

        def play():
            try:
                # Use larger frames_per_buffer to reduce clicking/popping
                # frames_per_buffer of 2048 provides better buffering
                stream = self.pa.open(
                    format=self.pa.get_format_from_width(sound['sample_width']),
                    channels=sound['channels'],
                    rate=sound['framerate'],
                    output=True,
                    frames_per_buffer=2048  # Larger buffer reduces popping
                )

                # Apply volume by scaling the audio data
                # This is a simple approach; for production you'd want better volume control
                data = sound['data']
                stream.write(data, exception_on_underflow=False)  # Don't raise on underflow

                # Let the stream finish playing before closing
                import time
                time.sleep(0.01)  # Small delay to ensure buffer is flushed

                stream.stop_stream()
                stream.close()

            except Exception as e:
                print(f"[AUDIO] Error playing {sound_name}: {e}")

        # Play in background thread to avoid blocking
        thread = threading.Thread(target=play, daemon=True)
        thread.start()

    def play_bounce(self) -> None:
        """Play ball bounce sound (paddle hit)."""
        print(f"[AUDIO] Playing paddle hit (volume: {settings.master_volume * 0.6})")
        self._play_sound('paddle_hit', settings.master_volume * 0.6)

    def play_wall_bounce(self) -> None:
        """Play wall bounce sound."""
        self._play_sound('wall_hit', settings.master_volume * 0.5)

    def play_score(self) -> None:
        """Play score sound."""
        print(f"[AUDIO] Playing score (volume: {settings.master_volume * 0.7})")
        self._play_sound('score', settings.master_volume * 0.7)

    def play_game_start(self) -> None:
        """Play game start sound."""
        print(f"[AUDIO] Playing game start (volume: {settings.master_volume * 0.6})")
        self._play_sound('game_start', settings.master_volume * 0.6)

    def play_game_end(self) -> None:
        """Play game end sound."""
        print(f"[AUDIO] Playing game over (volume: {settings.master_volume * 0.8})")
        self._play_sound('game_over', settings.master_volume * 0.8)

    def play_background_music(self) -> None:
        """Start playing background music in a loop."""
        if not self.enabled or 'background_music' not in self.sounds:
            return

        if self.music_thread and self.music_thread.is_alive():
            print("[AUDIO] Music already playing")
            return

        self.music_stop_flag = False

        def play_music():
            sound = self.sounds['background_music']
            volume = settings.master_volume * 0.3

            print(f"[AUDIO] Starting background music (volume: {volume})")

            try:
                while not self.music_stop_flag:
                    stream = self.pa.open(
                        format=self.pa.get_format_from_width(sound['sample_width']),
                        channels=sound['channels'],
                        rate=sound['framerate'],
                        output=True,
                        frames_per_buffer=2048  # Larger buffer reduces popping
                    )

                    stream.write(sound['data'], exception_on_underflow=False)
                    stream.stop_stream()
                    stream.close()

                    # Loop seamlessly
                    if self.music_stop_flag:
                        break

            except Exception as e:
                print(f"[AUDIO] Error playing background music: {e}")

        self.music_thread = threading.Thread(target=play_music, daemon=True)
        self.music_thread.start()

    def stop_background_music(self) -> None:
        """Stop background music."""
        print("[AUDIO] Stopping background music...")
        self.music_stop_flag = True
        if self.music_thread:
            self.music_thread.join(timeout=1.0)
            self.music_thread = None

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

    def cleanup(self) -> None:
        """Clean up PyAudio resources."""
        self.stop_background_music()
        if hasattr(self, 'pa'):
            self.pa.terminate()
