# 👏 Clap Launcher

Control your computer with voice and claps! Say a wake word, then use clap patterns to launch apps.

## 🎬 How It Works

1. **Say wake word** (e.g., "jarvis") → Activates system
2. **Double clap** 👏👏 → Launches your configured apps
3. **Triple clap** 👏👏👏 (within 30 seconds) → Triggers secondary action

## 📋 Requirements

- Python 3.7 or higher
- Microphone
- macOS or Windows
- Free Porcupine API key from [console.picovoice.ai](https://console.picovoice.ai/)

## 🚀 Quick Start

### 1. Get API Key

Sign up at [console.picovoice.ai](https://console.picovoice.ai/) and copy your Access Key.

### 2. Install

**macOS:**
```bash
git clone https://github.com/yourusername/clap-launcher.git
cd clap-launcher
python3 -m venv venv
source venv/bin/activate
brew install portaudio
pip install -r requirements.txt
```

**Windows:**
```bash
git clone https://github.com/yourusername/clap-launcher.git
cd clap-launcher
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

*Note: Windows users see [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for app launching modifications.*

### 3. Add Your API Key

Open `clap_launcher.py` and add your key at line 24:

```python
PORCUPINE_ACCESS_KEY = "your-key-here"
```

### 4. Run

```bash
python3 clap_launcher.py
```

Say **"jarvis"** and start clapping!

## 🎮 Available Wake Words

- `jarvis` (default)
- `computer`
- `alexa`
- `hey google`
- `hey siri`
- `ok google`
- `terminator`
- `bumblebee`
- `porcupine`
- `blueberry`
- `grapefruit`
- `grasshopper`

Use different wake word: `python3 clap_launcher.py --wake computer`

## 🐛 Troubleshooting

### Wake word not detected
- Speak clearly at normal volume
- Check microphone permissions (System Preferences → Security & Privacy → Microphone)
- Try different wake word: `--wake computer`

### Claps not detected
- Run debug mode: `python3 clap_launcher.py --debug`
- Clap sharply and crisply
- Adjust `clap_threshold` in code (line 274) - lower = more sensitive

### "No module named 'pvporcupine'"
```bash
pip install pvporcupine
```

### "PortAudio not found" (macOS)
```bash
brew install portaudio
```

### Apps not launching (Windows)
See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for proper Windows app launching syntax.

---

**⭐ Star this repo if you find it useful!**