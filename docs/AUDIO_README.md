# Audio System Documentation

## Overview

The Pong game features a complete retro audio system with programmatically generated sounds and music.

### Features

- **5 Sound Effects**: Paddle hit, wall hit, score, game start, game over
- **Background Music**: Looping 80s-style arcade music (30 seconds)
- **Volume Control**: Adjustable master volume in settings
- **Toggle**: Enable/disable audio in settings menu

## Audio Files

All audio files are in `src/assets/sounds/`:

| File | Size | Duration | Description |
|------|------|----------|-------------|
| paddle_hit.wav | ~2 KB | 80ms | Soft thump when ball hits paddle (220 Hz) |
| wall_hit.wav | ~2 KB | 60ms | Muted thump when ball hits wall (165 Hz) |
| score.wav | ~13 KB | 300ms | Descending tone when scoring (550→220 Hz) |
| game_start.wav | ~18 KB | 400ms | Rising tone at game start (220→880 Hz) |
| game_over.wav | ~27 KB | 600ms | Falling tone at game end (440→110 Hz) |
| background_music.wav | ~1.3 MB | 30s | 80s arcade-style music (120 BPM) |

## Installation

### System Requirements

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**Windows:**
```bash
pip install pyaudio
```

### Generate Audio Files

Run once after installation:
```bash
python setup_audio.py
```

## Technical Implementation

### Audio Backend

Uses **PyAudio** with PortAudio for cross-platform support.

- 22,050 Hz sample rate
- 16-bit PCM encoding
- Mono channel
- 2048-frame buffer

### Sound Generation

Procedurally generated using Python's `wave` module with smooth envelopes to prevent clicks.

## Usage

### In-Game

- **M key** - Toggle audio on/off
- **ESC → Settings** - Adjust volume

### Code Integration

```python
from game.audio_manager_pyaudio import PyAudioManager as AudioManager

audio = AudioManager()
audio.play_bounce()          # Paddle hit
audio.play_background_music()
audio.cleanup()              # When done
```

## Troubleshooting

See [AUDIO_TROUBLESHOOTING.md](AUDIO_TROUBLESHOOTING.md) for help.
