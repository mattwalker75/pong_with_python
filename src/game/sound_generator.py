"""Generate retro Pong sound effects."""
import wave
import struct
import math
from pathlib import Path


def generate_beep(
    filename: str,
    frequency: float,
    duration: float,
    volume: float = 0.5,
    sample_rate: int = 22050
) -> None:
    """Generate a simple beep sound with smooth envelope.

    Args:
        filename: Output WAV file path
        frequency: Frequency in Hz
        duration: Duration in seconds
        volume: Volume (0.0 to 1.0)
        sample_rate: Sample rate in Hz
    """
    num_samples = int(sample_rate * duration)

    with wave.open(filename, 'w') as wav_file:
        # Set parameters: 1 channel, 2 bytes per sample, sample rate
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))

        # Generate samples
        for i in range(num_samples):
            # Create a sine wave with exponential decay for a more retro sound
            t = i / sample_rate

            # Smooth fade-in to prevent click at start (first 10% of sound)
            # Use sine curve for smoother fade
            fade_in_samples = int(num_samples * 0.1)
            if i < fade_in_samples:
                fade_in = math.sin((i / fade_in_samples) * math.pi / 2)
            else:
                fade_in = 1.0

            # Smooth fade-out at end (last 30% of sound)
            # Use sine curve for smoother fade
            fade_out_samples = int(num_samples * 0.3)
            if i > num_samples - fade_out_samples:
                fade_out = math.sin(((num_samples - i) / fade_out_samples) * math.pi / 2)
            else:
                fade_out = 1.0

            # Gentler exponential decay for retro feel (reduced from 5 to 3)
            decay = math.exp(-t * 3)

            # Combine all envelopes
            envelope = fade_in * fade_out * decay
            value = volume * envelope * math.sin(2 * math.pi * frequency * t)

            # Convert to 16-bit integer
            sample = int(value * 32767)
            packed_value = struct.pack('h', sample)
            wav_file.writeframes(packed_value)


def generate_paddle_hit(filename: str) -> None:
    """Generate classic Pong paddle hit sound (smooth, low-pitched thump).

    Args:
        filename: Output WAV file path
    """
    # Softer paddle hit: 220 Hz (lower A note), slightly longer for smoother sound
    # Lower frequency and longer duration = less harsh, warmer sound
    generate_beep(filename, frequency=220, duration=0.08, volume=0.5)


def generate_wall_hit(filename: str) -> None:
    """Generate wall hit sound (soft, muted thump).

    Args:
        filename: Output WAV file path
    """
    # Wall hit: 165 Hz (lower E note), soft and muted
    # Even lower frequency for a subtle, non-harsh sound
    generate_beep(filename, frequency=165, duration=0.06, volume=0.4)


def generate_score_sound(filename: str) -> None:
    """Generate score sound (descending beep).

    Args:
        filename: Output WAV file path
    """
    sample_rate = 22050
    duration = 0.3
    num_samples = int(sample_rate * duration)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))

        for i in range(num_samples):
            t = i / sample_rate
            # Descending frequency from 550 Hz to 220 Hz
            frequency = 550 - (330 * t / duration)
            decay = math.exp(-t * 3)
            value = 0.5 * decay * math.sin(2 * math.pi * frequency * t)

            sample = int(value * 32767)
            packed_value = struct.pack('h', sample)
            wav_file.writeframes(packed_value)


def generate_game_start(filename: str) -> None:
    """Generate game start sound (ascending beep).

    Args:
        filename: Output WAV file path
    """
    sample_rate = 22050
    duration = 0.4
    num_samples = int(sample_rate * duration)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))

        for i in range(num_samples):
            t = i / sample_rate
            # Ascending frequency from 220 Hz to 880 Hz
            frequency = 220 + (660 * t / duration)
            decay = 1.0 - (t / duration)
            value = 0.4 * decay * math.sin(2 * math.pi * frequency * t)

            sample = int(value * 32767)
            packed_value = struct.pack('h', sample)
            wav_file.writeframes(packed_value)


def generate_game_over(filename: str) -> None:
    """Generate game over sound (descending dramatic beep).

    Args:
        filename: Output WAV file path
    """
    sample_rate = 22050
    duration = 0.6
    num_samples = int(sample_rate * duration)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))

        for i in range(num_samples):
            t = i / sample_rate
            # Descending frequency from 440 Hz to 110 Hz
            frequency = 440 - (330 * t / duration)
            value = 0.5 * math.sin(2 * math.pi * frequency * t)

            sample = int(value * 32767)
            packed_value = struct.pack('h', sample)
            wav_file.writeframes(packed_value)


def generate_all_sounds(output_dir: Path) -> None:
    """Generate all game sound effects.

    Args:
        output_dir: Directory to save sound files
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating retro Pong sound effects...")

    generate_paddle_hit(str(output_dir / "paddle_hit.wav"))
    print("  ✓ paddle_hit.wav")

    generate_wall_hit(str(output_dir / "wall_hit.wav"))
    print("  ✓ wall_hit.wav")

    generate_score_sound(str(output_dir / "score.wav"))
    print("  ✓ score.wav")

    generate_game_start(str(output_dir / "game_start.wav"))
    print("  ✓ game_start.wav")

    generate_game_over(str(output_dir / "game_over.wav"))
    print("  ✓ game_over.wav")

    print("Sound generation complete!")


if __name__ == "__main__":
    # Generate sounds when run directly
    from pathlib import Path
    sounds_dir = Path(__file__).parent.parent / "assets" / "sounds"
    generate_all_sounds(sounds_dir)
