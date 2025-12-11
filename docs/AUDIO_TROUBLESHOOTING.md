# Audio Troubleshooting Guide

## Overview

The game uses PyAudio for audio playback, which provides reliable cross-platform audio support.

## Common Issues

### 1. No Audio / Silent Game

**Check:**
- System volume is turned up (not muted)
- Correct audio output device is selected
- Audio is enabled in the game's Settings menu

**Fix:**
1. Check System Preferences → Sound → Output
2. Ensure correct output device is selected (speakers/headphones)
3. Test with system alert sounds to verify device works
4. In game, press ESC → Settings → Verify audio is enabled
5. Adjust master volume slider in game settings

### 2. Audio Files Missing

**Check:**
```bash
ls -lh src/assets/sounds/
```

Should show:
- paddle_hit.wav
- wall_hit.wav
- score.wav
- game_start.wav
- game_over.wav
- background_music.wav

**Fix:**
```bash
python setup_audio.py
```

### 3. PyAudio Not Installed

**Error:** `ModuleNotFoundError: No module named 'pyaudio'`

**Fix (macOS):**
```bash
brew install portaudio
pip install pyaudio
```

**Fix (Linux - Debian/Ubuntu):**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**Fix (Windows):**
```bash
pip install pyaudio
```

### 4. PortAudio Library Missing

**Error:** `ImportError: libportaudio.so.2: cannot open shared object file`

**Fix (macOS):**
```bash
brew install portaudio
```

**Fix (Linux):**
```bash
sudo apt-get install portaudio19-dev
```

### 5. Audio Popping or Crackling

This should not occur with the current configuration, but if it does:

1. Close other audio applications (Spotify, etc.)
2. Restart your computer
3. Try different audio output device

### 6. Background Music Not Playing

1. Check that audio is enabled in Settings
2. Verify background_music.wav exists (1.3 MB file)
3. Check master volume is not set to 0
4. Restart the game

## Platform-Specific Notes

### macOS
- Requires PortAudio: `brew install portaudio`
- May need to grant audio permissions in System Preferences
- If no sound, restart Core Audio: `sudo killall coreaudiod`

### Linux
- Requires portaudio19-dev package
- May need to configure ALSA/PulseAudio
- Check audio group permissions

### Windows
- PyAudio usually works out of the box
- Windows Defender may block first-time audio playback

## Verification Steps

1. **Verify installation:**
   ```bash
   python -c "import pyaudio; print('PyAudio version:', pyaudio.__version__)"
   ```

2. **Check audio files:**
   ```bash
   ls -lh src/assets/sounds/
   ```

3. **Run the game:**
   ```bash
   python src/main.py
   ```

4. **Test in-game:**
   - Press ESC → Settings
   - Verify audio is enabled
   - Adjust volume slider
   - Start a game and listen for sounds

## Still Having Issues?

If none of these solutions work:

1. **Verify system audio:**
   - Play a YouTube video
   - Test system alert sounds
   - Try other audio applications

2. **Check Python environment:**
   - Ensure virtual environment is activated
   - Verify all dependencies: `pip list | grep pyaudio`
   - Try: `pip install --force-reinstall pyaudio`

3. **Restart everything:**
   - Close the game
   - Restart terminal/command prompt
   - Restart computer if needed

4. **File an issue:**
   Provide the following information:
   - OS and version (`sw_vers` on macOS, `uname -a` on Linux)
   - Python version (`python --version`)
   - PyAudio version (`pip show pyaudio`)
   - Error messages or console output

## Technical Details

The game uses:
- **Audio library:** PyAudio with PortAudio backend
- **Sample rate:** 22,050 Hz
- **Bit depth:** 16-bit PCM
- **Channels:** Mono
- **Buffer size:** 2048 frames (for smooth playback)

All audio files are generated procedurally using Python's wave module.
