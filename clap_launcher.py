"""
Clap-Activated App Launcher for macOS with LOCAL Wake Word Detection
Say a wake word to activate, then double/triple clap!
Uses Porcupine for fast, offline wake word detection
"""

import pyaudio
import numpy as np
import subprocess
import time
import sys
import os
from collections import deque
import struct
import signal

try:
    import pvporcupine
except ImportError:
    print("❌ Porcupine not installed!")
    print("\nInstall it with:")
    print("  pip install pvporcupine")
    sys.exit(1)

# Your Porcupine API key
PORCUPINE_ACCESS_KEY = "KEY_HERE"


class UnifiedLauncher:
    
    def __init__(self, wake_word="jarvis", clap_threshold=1800, debug=False):
        self.wake_word = wake_word.lower()
        self.clap_threshold = clap_threshold
        self.debug = debug
        
        self.is_active = False
        self.activation_time = 0
        self.active_duration = 5
        self.running = True
        
        self.waiting_for_triple = False
        self.triple_wait_time = 0
        self.triple_wait_duration = 30
        
        self.clap_times = []
        self.last_clap_time = 0
        self.clap_interval = 0.7
        self.previous_amplitude = 0
        self.amplitude_history = deque(maxlen=10)
        
        builtin_keywords = pvporcupine.KEYWORDS
        print(f"📋 Available wake words: {', '.join(builtin_keywords)}")
        
        if self.wake_word not in builtin_keywords:
            print(f"⚠️  '{self.wake_word}' not available, using 'jarvis' instead")
            self.wake_word = "jarvis"
        
        try:
            self.porcupine = pvporcupine.create(
                access_key=PORCUPINE_ACCESS_KEY,
                keywords=[self.wake_word]
            )
            print(f"Wake word '{self.wake_word}' loaded successfully!")
            print("This runs 100% locally - no internet needed!\n")
        except Exception as e:
            print(f"❌ Error initializing Porcupine: {e}")
            sys.exit(1)
        
        self.sample_rate = self.porcupine.sample_rate
        self.frame_length = self.porcupine.frame_length
        
        self.pa = pyaudio.PyAudio()
        self.audio_stream = None
        
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        print("\n\n👋 Shutting down clap launcher...")
        self.running = False
    
    def start_audio_stream(self):
        """Start the unified audio stream"""
        try:
            self.audio_stream = self.pa.open(
                rate=self.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.frame_length
            )
            print(f"🎧 Listening for '{self.wake_word}'...")
            print("💡 Say the wake word to start clap detection\n")
        except Exception as e:
            print(f"❌ Error opening audio stream: {e}")
            sys.exit(1)
    
    def detect_wake_word(self, pcm):
        """Detect wake word from audio data"""
        try:
            keyword_index = self.porcupine.process(pcm)
            return keyword_index >= 0
        except Exception as e:
            if self.debug:
                print(f"Wake word error: {e}")
            return False
    
    def detect_clap(self, pcm):
        """Detect clap from audio data"""
        try:
            # Convert to numpy array and get amplitude
            audio_data = np.array(pcm, dtype=np.int16)
            amplitude = np.abs(audio_data).max()
            
            self.amplitude_history.append(amplitude)
            current_time = time.time()
            
            if self.debug and amplitude > 500:
                print(f"📊 Amplitude: {amplitude} (threshold: {self.clap_threshold})")
            
            # Check for sharp sound (clap )
            amplitude_jump = amplitude - self.previous_amplitude
            sharp_attack = amplitude_jump > (self.clap_threshold * 0.4)
            loud_enough = amplitude > self.clap_threshold
            
            if len(self.amplitude_history) >= 3:
                avg_recent = sum(self.amplitude_history) / len(self.amplitude_history)
                not_sustained = avg_recent < (self.clap_threshold * 0.5)
            else:
                not_sustained = True
            
            is_clap = loud_enough and (sharp_attack or not_sustained)
            
            if is_clap and current_time - self.last_clap_time > 0.1:
                self.clap_times.append(current_time)
                self.last_clap_time = current_time
                print(f"👏 Clap #{len(self.clap_times)} detected!")
                
                # Clean up old claps
                self.clap_times = [t for t in self.clap_times 
                                  if current_time - t < self.clap_interval * 2.5]
                
                # Check for triple clap
                if len(self.clap_times) >= 3:
                    time_span = self.clap_times[-1] - self.clap_times[-3]
                    if time_span < self.clap_interval * 2.5:
                        self.clap_times.clear()
                        return 3
                
                # Check for double clap (only if NOT waiting for triple)
                if not self.waiting_for_triple and len(self.clap_times) >= 2:
                    time_span = self.clap_times[-1] - self.clap_times[-2]
                    if time_span < self.clap_interval:
                        self.clap_times.clear()
                        return 2
            
            self.previous_amplitude = amplitude
            
            # Clean up old claps periodically
            if len(self.clap_times) > 0 and current_time - self.clap_times[-1] > self.clap_interval * 2:
                self.clap_times.clear()
            
            return 0
            
        except Exception as e:
            if self.debug:
                print(f"Clap detection error: {e}")
            return 0
    
    def activate(self):
        """Activate clap listening mode"""
        self.is_active = True
        self.activation_time = time.time()
        print("\n" + "="*60)
        print(f"✨ '{self.wake_word.upper()}' DETECTED! Listening for claps...")
        print("👏👏  Double clap = Launch apps + enable triple clap mode")
        print(f"⏱️  You have {self.active_duration} seconds...")
        print("="*60 + "\n")
    
    def deactivate(self):
        """Deactivate clap listening mode"""
        self.is_active = False
        print(f"\n⏰ Time's up! Say '{self.wake_word}' to try again.\n")
    
    def enter_triple_wait_mode(self):
        """Enter mode where only triple clap is allowed"""
        self.waiting_for_triple = True
        self.triple_wait_time = time.time()
        print("\n" + "="*60)
        print("⏳ WAITING FOR TRIPLE CLAP...")
        print("👏👏👏 Triple clap within 30 seconds = Play YouTube")
        print("🚫 Double clap disabled during this time")
        print(f"⏱️  You have {self.triple_wait_duration} seconds...")
        print("="*60 + "\n")
    
    def exit_triple_wait_mode(self):
        """Exit triple wait mode"""
        self.waiting_for_triple = False
        print(f"\n⏰ Triple clap window expired! Say '{self.wake_word}' to start again.\n")
    
    def is_triple_wait_active(self):
        """Check if still in triple wait window"""
        if not self.waiting_for_triple:
            return False
        
        elapsed = time.time() - self.triple_wait_time
        if elapsed > self.triple_wait_duration:
            self.exit_triple_wait_mode()
            return False
            
        return True
    
    def is_still_active(self):
        """Check if still in active listening window"""
        if not self.is_active:
            return False
        
        elapsed = time.time() - self.activation_time
        if elapsed > self.active_duration:
            self.deactivate()
            return False
            
        return True
    
    def launch_all_apps(self):
        """Launch all configured apps"""
        print("\n DOUBLE CLAP DETECTED! Launching apps...\n")
        
        tbt_path = os.path.expanduser("~/code/tbt")
        subprocess.Popen(["open", "-a", "Visual Studio Code", tbt_path])
        print(f"✅ Launched VS Code with folder: {tbt_path}")
        time.sleep(0.5)
        
        subprocess.Popen(["open", "-na", "Google Chrome", "--args", "--new-window", "https://claude.ai"])
        print("✅ Launched Chrome (new window) with https://claude.ai")
        time.sleep(0.5)
        
        subprocess.Popen(["open", "-a", "Discord"])
        print("✅ Launched Discord")
        time.sleep(0.5)
        
        print("\n✨ All apps launched!\n")
    
    def play_youtube_video(self):
        """Play a YouTube video"""
        print("\n🎵 TRIPLE CLAP DETECTED! Playing YouTube video...\n")
        
        youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1"
        subprocess.Popen(["open", youtube_url])
        print(f"✅ Opening YouTube: {youtube_url}")
    
    def run(self):
        """Main run loop"""
        self.start_audio_stream()
        
        try:
            while self.running:
                # Read audio frame
                pcm_bytes = self.audio_stream.read(self.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.frame_length, pcm_bytes)
                
                # Check for wake word when not active and not waiting for triple
                if not self.is_active and not self.waiting_for_triple:
                    if self.detect_wake_word(pcm):
                        self.activate()
                
                # Check for claps when active (initial 5 second window)
                elif self.is_still_active():
                    clap_type = self.detect_clap(pcm)
                    
                    if clap_type == 2:  # Double clap
                        self.launch_all_apps()
                        self.deactivate()
                        self.enter_triple_wait_mode()  # Enter 30 second triple clap window
                        time.sleep(1)
                        
                    elif clap_type == 3:  # Triple clap (shouldn't happen in first window but handle it)
                        self.play_youtube_video()
                        self.deactivate()
                        time.sleep(1)
                
                # Check for triple clap during 30 second wait window
                elif self.is_triple_wait_active():
                    clap_type = self.detect_clap(pcm)
                    
                    if clap_type == 3:  # Triple clap
                        self.play_youtube_video()
                        self.waiting_for_triple = False  # Reset everything
                        time.sleep(1)
                    # Double claps are ignored during this time
                        
        except KeyboardInterrupt:
            print("\n\n Shutting down...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up...")
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.pa:
            self.pa.terminate()
        if self.porcupine:
            self.porcupine.delete()
        print("Goodbye!")


def main():
    print("=" * 70)
    print("  👏 CLAP LAUNCHER - Local Wake Word Edition")
    print("=" * 70)
    print("\n🚀 100% LOCAL - No internet needed!")
    print("🗣️  Say wake word → 👏👏 Double clap → Launch apps")
    print("⏳  Then 30 sec window → 👏👏👏 Triple clap → Play vid")
    print("\nPress Ctrl+C to exit\n")
    
    debug_mode = "--debug" in sys.argv
    
    # Get wake word from command line or use default
    wake_word = "jarvis"
    for i, arg in enumerate(sys.argv):
        if arg == "--wake" and i + 1 < len(sys.argv):
            wake_word = sys.argv[i + 1]
    
    if not debug_mode:
        print("💡 Tip: Run with '--debug' to see amplitude levels")
        print("💡 Tip: Run with '--wake computer' to change wake word\n")
    
    launcher = UnifiedLauncher(wake_word=wake_word, clap_threshold=1800, debug=debug_mode)
    launcher.run()


if __name__ == "__main__":
    main()