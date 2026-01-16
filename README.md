# 👏 Wake Up

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
git clone https://github.com/tpateeq/wake-up.git
cd wake-up
python3 -m venv venv
source venv/bin/activate
brew install portaudio
pip install -r requirements.txt
```

**Windows:**
```bash
git clone https://github.com/tpateeq/wake-up.git
cd wake-up
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**If PyAudio fails on Windows:**
Download the wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install:
```bash
pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl
```

### 3. Add Your API Key

Open `clap_launcher.py` and add your key at line 24:

```python
PORCUPINE_ACCESS_KEY = "your-key-here"
```

### 4. Configure Apps

**macOS** - Works by default with:
```python
subprocess.Popen(["open", "-a", "Visual Studio Code"])
subprocess.Popen(["open", "-a", "Google Chrome"])
```

**Windows** - Replace app launching code (line 200) with:
```python
def launch_all_apps(self):
    print("\n🚀 DOUBLE CLAP DETECTED! Launching apps...\n")
    
    # VS Code
    subprocess.Popen(["code"], shell=True)
    print("✅ Launched VS Code")
    time.sleep(0.5)
    
    # Chrome
    subprocess.Popen(["start", "chrome", "https://claude.ai"], shell=True)
    print("✅ Launched Chrome")
    time.sleep(0.5)
    
    # Discord
    subprocess.Popen(["start", "discord"], shell=True)
    print("✅ Launched Discord")
    
    print("\n✨ All apps launched!\n")
```

**Common Windows apps:**
```python
# Spotify
subprocess.Popen(["start", "spotify"], shell=True)

# Slack
subprocess.Popen(["start", "slack"], shell=True)

# Any executable with full path
subprocess.Popen([r"C:\Program Files\App\app.exe"], shell=True)
```

### 5. Run

**macOS:**
```bash
python3 clap_launcher.py
```

**Windows:**
```bash
python clap_launcher.py
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
- **macOS**: System Preferences → Security & Privacy → Microphone → Enable Terminal
- **Windows**: Settings → Privacy → Microphone → Enable Python
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

### Windows: Apps not launching
- Make sure apps are installed and accessible
- Use full paths if app not in PATH: `subprocess.Popen([r"C:\path\to\app.exe"], shell=True)`
- Check app name with: `where appname` in Command Prompt

### Windows: PyAudio installation fails
1. Download wheel from [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Choose correct Python version (check with `python --version`)
3. Install: `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`

---

**⭐ Star this repo if you find it useful!**
