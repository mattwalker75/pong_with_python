#!/usr/bin/env python
"""Setup script to generate game audio files."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from game.sound_generator import generate_all_sounds
from game.music_generator import generate_background_music


def main():
    """Generate all audio files for the game."""
    print("=" * 60)
    print("PONG AUDIO SETUP")
    print("=" * 60)
    print()

    sounds_dir = Path(__file__).parent / "src" / "assets" / "sounds"

    # Generate sound effects
    generate_all_sounds(sounds_dir)
    print()

    # Generate background music
    generate_background_music(sounds_dir)
    print()

    print("=" * 60)
    print("AUDIO SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("All sound files have been generated in:")
    print(f"  {sounds_dir}")
    print()
    print("You can now run the game with:")
    print("  python src/main.py")
    print()


if __name__ == "__main__":
    main()
