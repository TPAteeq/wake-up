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

- **Python 3.9-3.12** (avoid 3.13 on Windows - dependency issues)
- Microphone
- macOS, Windows, or Linux
- Free Porcupine API key from [console.picovoice.ai](https://console.picovoice.ai/)

## 🚀 Quick Start

### 1. Get API Key

Sign up at [console.picovoice.ai](https://console.picovoice.ai/) and copy your Access Key (free tier available).

### 2. Install

**macOS:**
```bash
# Install portaudio first (required for PyAudio)
brew install portaudio

git clone https://github.com/tpateeq/wake-up.git
cd wake-up
python3 -m venv venv
source venv/bin/activate
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
# Install portaudio first (required for PyAudio)
sudo apt-get install portaudio19-dev  # Ubuntu/Debian
# OR
sudo dnf install portaudio-devel      # Fedora

git clone https://github.com/tpateeq/wake-up.git
cd wake-up
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add Your API Key

Open `clap_launcher.py` and add your key at line 32:

```python
PORCUPINE_ACCESS_KEY = "your-key-here"
```

### 4. Configure Your Apps

The script **automatically detects your OS** and uses the appropriate commands! Just customize the app names in the `launch_all_apps()` method (starting at line 267):

**Example configuration:**
```python
def launch_all_apps(self):
    print("\n🚀 DOUBLE CLAP DETECTED! Launching apps...\n")
    
    if self.os_type == "Darwin":  # macOS
        self._launch_app_macos("Visual Studio Code")
        self._launch_app_macos("Google Chrome", args=["--new-window", "https://claude.ai"])
        self._launch_app_macos("Discord")
        
    elif self.os_type == "Windows":
        self._launch_app_windows("code")  # VS Code
        self._launch_app_windows("chrome", args=["https://claude.ai"])
        self._launch_app_windows("discord")
        
    elif self.os_type == "Linux":
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

```bash
python3 clap_launcher.py  # macOS/Linux
python clap_launcher.py   # Windows
```

Say **"jarvis"** and start clapping! 🎉

The script will automatically detect your OS:
```
🖥️  Detected OS: Windows  # or Darwin (macOS), or Linux
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

## 🛠️ Customization

### Change the video URL (triple clap action)

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

**Run with debug mode** to see amplitude levels and find the right threshold:
```bash
python3 clap_launcher.py --debug
```

## 🐛 Troubleshooting

### Wake word not detected

**Check microphone permissions:**
- **macOS**: System Preferences → Security & Privacy → Microphone → Enable Terminal
- **Windows**: Settings → Privacy → Microphone → Enable Python
- **Linux**: Check microphone permissions for your terminal

**Test your microphone:**
- Speak clearly at normal volume
- Make sure you're using the correct microphone (if you have multiple)
- Try a different wake word: `python3 clap_launcher.py --wake computer`

**Check which microphone is being used:**
Run this Python snippet to list available audio devices:
```python
import pyaudio
pa = pyaudio.PyAudio()
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"{i}: {info['name']}")
```

### Claps not detected

- **Run debug mode**: `python3 clap_launcher.py --debug`
- Clap sharply and crisply near the microphone
- Watch the amplitude output - it should spike above the threshold
- Adjust `clap_threshold` in code (line 416)
  - Lower value = more sensitive (might pick up background noise)
  - Higher value = less sensitive (might miss soft claps)
- Default threshold is 1800 - adjust based on your debug output

**Example debug output:**
```
Amplitude: 2500 (threshold: 1800)  # ✅ Clap detected!
Amplitude: 1200 (threshold: 1800)  # ❌ Too quiet
```

### "No module named 'pvporcupine'"

```bash
pip install pvporcupine
```

### macOS: "PortAudio not found" or "portaudio.h not found"

This means portaudio wasn't installed before PyAudio:

```bash
# Install portaudio
brew install portaudio

# Then reinstall requirements
pip install -r requirements.txt
```

### Windows: Python 3.13 installation fails

**Recommended solution:** Use Python 3.11 or 3.12 instead.

Some dependencies (numpy, PyAudio) don't have pre-built wheels for Python 3.13 on Windows yet.

1. Download Python 3.12 from [python.org](https://www.python.org/downloads/)
2. Reinstall and create new venv:
   ```bash
   py -3.12 -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Windows: Apps not launching

**Check if apps are installed and in PATH:**
```bash
where appname  # Check if app is in PATH
```

**For apps not in PATH:**
Use full path in the script:
```python
subprocess.Popen([r"C:\Program Files\YourApp\app.exe"])
```

**Common app commands:**
- VS Code: `code`
- Chrome: `chrome`
- Discord: `discord`
- Spotify: `spotify`
- Slack: `slack`

### API Key errors

**"Invalid access key" or initialization failed:**
- Make sure you copied the key correctly (no extra spaces)
- Verify the key at [console.picovoice.ai](https://console.picovoice.ai/)
- Check if you're using a v3 key with v4 library (or vice versa)
- Free tier keys have device limits - you may need a new key if using on multiple devices

### Linux: PyAudio installation fails

```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-dev

# Fedora
sudo dnf install portaudio-devel python3-devel

# Then reinstall
pip install -r requirements.txt
```

## 📝 How It Works Internally

1. **OS Detection**: Script detects your platform using `platform.system()`
2. **Wake Word**: Porcupine continuously listens for your wake word (offline)
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