#!/bin/bash
# Installation script for Pong game

set -e  # Exit on error

echo "======================================"
echo "Pong Game Installation"
echo "======================================"
echo

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "❌ Error: Python 3.10 or higher is required"
    echo "   Current version: $python_version"
    exit 1
fi
echo "✓ Python version OK: $python_version"
echo

# Check if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS system"
    echo

    # Check for Homebrew
    if ! command -v brew &> /dev/null; then
        echo "⚠️  Homebrew not found"
        echo "   Install Homebrew from https://brew.sh"
        echo "   Or install portaudio manually"
        echo
    else
        echo "Checking for PortAudio..."
        if ! brew list portaudio &> /dev/null; then
            echo "Installing PortAudio..."
            brew install portaudio
            echo "✓ PortAudio installed"
        else
            echo "✓ PortAudio already installed"
        fi
        echo
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux system"
    echo "⚠️  Please ensure portaudio19-dev is installed:"
    echo "   sudo apt-get install portaudio19-dev  (Debian/Ubuntu)"
    echo "   sudo dnf install portaudio-devel      (Fedora)"
    echo "   sudo pacman -S portaudio              (Arch)"
    echo
fi

# Check if virtual environment exists
if [ ! -d "pong_venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv pong_venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo

# Activate virtual environment
echo "Activating virtual environment..."
source pong_venv/bin/activate
echo "✓ Virtual environment activated"
echo

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo

# Generate audio files
echo "Generating audio files..."
if [ ! -d "src/assets/sounds" ] || [ -z "$(ls -A src/assets/sounds 2>/dev/null)" ]; then
    python setup_audio.py
    echo "✓ Audio files generated"
else
    echo "✓ Audio files already exist"
fi
echo

echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo
echo "To run the game:"
echo "  1. Activate virtual environment: source pong_venv/bin/activate"
echo "  2. Run the game: python src/main.py"
echo
echo "To test audio:"
echo "  python test_audio_window.py"
echo
echo "To run tests:"
echo "  pytest"
echo
echo "Enjoy playing Pong!"
echo
