# 👏 Wake Up

**Cross-platform** voice and clap-controlled app launcher! Say a wake word, then use clap patterns to launch apps.

✅ **Automatically detects your OS** (macOS, Windows, Linux) and adjusts commands accordingly!

## 🎬 How It Works

1. **Say wake word** (e.g., "jarvis") → Activates system
2. **Double clap** 👏👏 → Launches your configured apps
3. **Triple clap** 👏👏👏 (within 30 seconds) → Opens a video/URL

## ✨ Features

- 🖥️ **Cross-platform**: Works on macOS, Windows, and Linux
- 🔌 **100% Offline**: Wake word detection runs locally
- 🎯 **Smart OS Detection**: Automatically uses the right commands for your system
- 🎤 **Fast & Accurate**: Porcupine wake word engine
- 🎵 **Customizable**: Configure any apps and actions

## 📋 Requirements

- Python 3.7 or higher
- Microphone
- macOS, Windows, or Linux
- Free Porcupine API key from [console.picovoice.ai](https://console.picovoice.ai/)

## 🚀 Quick Start

### 1. Get API Key

Sign up at [console.picovoice.ai](https://console.picovoice.ai/) and copy your Access Key (free tier available).

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

**Linux:**
```bash
git clone https://github.com/tpateeq/wake-up.git
cd wake-up
python3 -m venv venv
source venv/bin/activate
sudo apt-get install portaudio19-dev  # Ubuntu/Debian
# OR
sudo dnf install portaudio-devel      # Fedora
pip install -r requirements.txt
```

**If PyAudio fails on Windows:**
Download the wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install:
```bash
pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl
```

### 3. Add Your API Key

Open `clap_launcher.py` and add your key at line 32:

```python
PORCUPINE_ACCESS_KEY = "your-key-here"
```

### 4. Configure Your Apps

The script **automatically detects your OS** and uses the appropriate commands! Just customize the app names in the `launch_all_apps()` method (starting at line 267):

**Default configuration works for all platforms:**
```python
def launch_all_apps(self):
    print("\n🚀 DOUBLE CLAP DETECTED! Launching apps...\n")
    
    if self.os_type == "Darwin":  # macOS
        # Your macOS apps here
        self._launch_app_macos("Visual Studio Code")
        self._launch_app_macos("Google Chrome", args=["--new-window", "https://claude.ai"])
        self._launch_app_macos("Discord")
        
    elif self.os_type == "Windows":
        # Your Windows apps here
        self._launch_app_windows("code")  # VS Code
        self._launch_app_windows("chrome", args=["https://claude.ai"])
        self._launch_app_windows("discord")
        
    elif self.os_type == "Linux":
        # Your Linux apps here
        self._launch_app_linux("code")  # VS Code
        self._launch_app_linux("google-chrome", args=["https://claude.ai"])
        self._launch_app_linux("discord")
```

**Customize for your favorite apps:**

*macOS examples:*
```python
self._launch_app_macos("Spotify")
self._launch_app_macos("Slack")
self._launch_app_macos("Safari", args=["https://example.com"])
self._launch_app_macos("Terminal")
```

*Windows examples:*
```python
self._launch_app_windows("spotify")
self._launch_app_windows("slack")
self._launch_app_windows("notepad")
# Full path for apps not in PATH:
subprocess.Popen([r"C:\Program Files\App\app.exe"])
```

*Linux examples:*
```python
self._launch_app_linux("spotify")
self._launch_app_linux("slack")
self._launch_app_linux("firefox", args=["https://example.com"])
self._launch_app_linux("gnome-terminal")
```

### 5. Run

**All platforms:**
```bash
# macOS/Linux
python3 clap_launcher.py

# Windows
python clap_launcher.py
```

Say **"jarvis"** and start clapping! 🎉

The script will automatically detect your OS and display:
```
🖥️  Detected OS: Darwin  # or Windows, or Linux
```

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

**Use a different wake word:**
```bash
python3 clap_launcher.py --wake computer
```

## 🛠️ Advanced Customization

### Customize the video/URL (triple clap action)

Edit the `play_youtube_video()` method around line 333:

```python
def play_youtube_video(self):
    youtube_url = "https://www.instagram.com/p/DMZ58Whvfir/"  # Change to any URL!
    
    # The script automatically handles opening URLs on all platforms
```

You can use any URL - YouTube, Instagram, websites, local files, etc!

### Adjust clap sensitivity

If claps aren't being detected or too many false positives:

```python
# In main() function, around line 416:
launcher = UnifiedLauncher(
    wake_word=wake_word, 
    clap_threshold=1800,  # Lower = more sensitive, Higher = less sensitive
    debug=debug_mode
)
```

Run with `--debug` to see amplitude levels and find the right threshold:
```bash
python3 clap_launcher.py --debug
```

## 🐛 Troubleshooting

### Wake word not detected
- Speak clearly at normal volume
- **macOS**: System Preferences → Security & Privacy → Microphone → Enable Terminal
- **Windows**: Settings → Privacy → Microphone → Enable Python
- **Linux**: Check microphone permissions for your terminal
- Try different wake word: `--wake computer`

### Claps not detected
- Run debug mode: `python3 clap_launcher.py --debug`
- Clap sharply and crisply
- Adjust `clap_threshold` in code (line 416) - lower = more sensitive
- Watch the amplitude output in debug mode to calibrate

### "No module named 'pvporcupine'"
```bash
pip install pvporcupine
```

### "PortAudio not found"

**macOS:**
```bash
brew install portaudio
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev

# Fedora
sudo dnf install portaudio-devel
```

**Windows:** Usually not needed, but if required:
- Download from [PortAudio website](http://www.portaudio.com/)

### Apps not launching

**Check app installation:**
```bash
# macOS
open -a "AppName"  # Test if app opens

# Windows
where appname  # Check if app is in PATH

# Linux
which appname  # Check if app is installed
```

**For Windows apps not in PATH:**
Use full path in the script:
```python
subprocess.Popen([r"C:\Program Files\YourApp\app.exe"])
```

### PyAudio installation fails (Windows)

1. Download the appropriate wheel from [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Check your Python version: `python --version`
3. Download matching wheel (e.g., cp39 = Python 3.9, cp310 = Python 3.10)
4. Install: `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`

## 📝 How It Works Internally

1. **OS Detection**: Script detects your platform using `platform.system()`
2. **Wake Word**: Porcupine continuously listens for your wake word
3. **Activation Window**: 5 seconds to perform double clap
4. **App Launch**: OS-appropriate commands launch your apps
5. **Triple Clap Window**: 30 seconds to perform triple clap for secondary action

## 🔒 Privacy

- Wake word detection runs **100% offline** on your machine
- No audio data is sent to any server
- Porcupine API key only validates the library, doesn't transmit audio
- Completely private and secure

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add support for more platforms
- Improve clap detection algorithm
- Add more customization options
- Fix bugs or improve documentation

## 📄 License

MIT License - feel free to use and modify!

---

**⭐ Star this repo if you find it useful!**

**Made with 💙 for productivity enthusiasts**