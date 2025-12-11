"""Generate retro 80s arcade-style background music."""
import wave
import struct
import math
from pathlib import Path


def generate_arcade_music(
    filename: str,
    duration: float = 30.0,
    tempo: int = 120,
    volume: float = 0.3
) -> None:
    """Generate simple 80s arcade-style background music.

    Creates a looping melodic pattern with a retro synthesizer sound.

    Args:
        filename: Output WAV file path
        duration: Duration in seconds
        tempo: Tempo in BPM
        volume: Volume (0.0 to 1.0)
    """
    sample_rate = 22050

    # Note frequencies (in Hz) for a pentatonic scale (C major pentatonic)
    # This scale sounds good and avoids dissonance
    notes = {
        'C4': 261.63,
        'D4': 293.66,
        'E4': 329.63,
        'G4': 392.00,
        'A4': 440.00,
        'C5': 523.25,
        'D5': 587.33,
        'E5': 659.25,
    }

    # Simple melody pattern (classic arcade-style)
    melody = [
        ('E4', 0.5), ('G4', 0.5), ('A4', 0.5), ('C5', 0.5),
        ('A4', 0.5), ('G4', 0.5), ('E4', 1.0),
        ('D4', 0.5), ('E4', 0.5), ('G4', 0.5), ('A4', 0.5),
        ('G4', 0.5), ('E4', 0.5), ('D4', 1.0),
        ('C4', 0.5), ('E4', 0.5), ('G4', 0.5), ('E4', 0.5),
        ('C4', 0.5), ('E4', 0.5), ('C4', 1.0),
        ('D4', 0.5), ('E4', 0.5), ('D4', 0.5), ('C4', 0.5),
        ('D4', 2.0),
    ]

    # Bass line (plays with the melody)
    bass_notes = {
        'C2': 65.41,
        'D2': 73.42,
        'E2': 82.41,
        'G2': 98.00,
        'A2': 110.00,
    }

    bass_pattern = [
        ('C2', 2.0), ('G2', 2.0),
        ('A2', 2.0), ('E2', 2.0),
        ('C2', 2.0), ('G2', 2.0),
        ('D2', 2.0), ('G2', 2.0),
    ]

    # Calculate beat duration
    beat_duration = 60.0 / tempo

    num_samples = int(sample_rate * duration)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))

        melody_index = 0
        bass_index = 0
        melody_time = 0
        bass_time = 0
        current_melody_duration = melody[0][1] * beat_duration
        current_bass_duration = bass_pattern[0][1] * beat_duration

        for i in range(num_samples):
            t = i / sample_rate

            # Update melody note if needed
            if t >= melody_time + current_melody_duration:
                melody_time = t
                melody_index = (melody_index + 1) % len(melody)
                current_melody_duration = melody[melody_index][1] * beat_duration

            # Update bass note if needed
            if t >= bass_time + current_bass_duration:
                bass_time = t
                bass_index = (bass_index + 1) % len(bass_pattern)
                current_bass_duration = bass_pattern[bass_index][1] * beat_duration

            # Get current notes
            melody_note, _ = melody[melody_index]
            bass_note, _ = bass_pattern[bass_index]

            melody_freq = notes[melody_note]
            bass_freq = bass_notes[bass_note]

            # Time within current note
            note_t = t - melody_time
            bass_t = t - bass_time

            # ADSR envelope for melody (Attack, Decay, Sustain, Release)
            attack_time = 0.01
            decay_time = 0.05
            sustain_level = 0.7
            release_time = 0.1

            if note_t < attack_time:
                envelope = note_t / attack_time
            elif note_t < attack_time + decay_time:
                envelope = 1.0 - ((note_t - attack_time) / decay_time) * (1.0 - sustain_level)
            elif note_t < current_melody_duration - release_time:
                envelope = sustain_level
            else:
                release_progress = (note_t - (current_melody_duration - release_time)) / release_time
                envelope = sustain_level * (1.0 - release_progress)

            # Simple envelope for bass
            bass_envelope = max(0, 1.0 - (bass_t / current_bass_duration))

            # Generate melody with some harmonic richness (square wave-ish)
            melody_value = 0
            melody_value += math.sin(2 * math.pi * melody_freq * t)
            melody_value += 0.3 * math.sin(4 * math.pi * melody_freq * t)  # Second harmonic
            melody_value *= envelope * volume * 0.5

            # Generate bass (sine wave)
            bass_value = math.sin(2 * math.pi * bass_freq * t) * bass_envelope * volume * 0.4

            # Mix melody and bass
            value = melody_value + bass_value

            # Clamp to prevent clipping
            value = max(-1.0, min(1.0, value))

            # Convert to 16-bit integer
            sample = int(value * 32767)
            packed_value = struct.pack('h', sample)
            wav_file.writeframes(packed_value)


def generate_background_music(output_dir: Path) -> None:
    """Generate background music for the game.

    Args:
        output_dir: Directory to save music file
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating retro arcade background music...")
    print("  (This may take a moment...)")

    # Generate a 30-second loop
    generate_arcade_music(
        str(output_dir / "background_music.wav"),
        duration=30.0,
        tempo=120,
        volume=0.25  # Keep it subtle
    )

    print("  ✓ background_music.wav (30s loop)")
    print("Music generation complete!")


if __name__ == "__main__":
    from pathlib import Path
    sounds_dir = Path(__file__).parent.parent / "assets" / "sounds"
    generate_background_music(sounds_dir)
