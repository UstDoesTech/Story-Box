#!/usr/bin/env python3
"""
Story Box - Children's Audio Player
Hardware: Raspberry Pi Zero 2 W + I2S Audio Bonnet + I2C LCD + 5 Buttons
Features: Multi-story selection, Audio feedback, Auto-play, Safe shutdown
"""

import os
import time
import pygame
import json
from pathlib import Path
from threading import Thread, Event
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

class StoryBox:
    """Story Box Controller"""
    
    # GPIO Pin assignments
    PIN_PLAY = 17       # Play/Pause button
    PIN_PREV = 27       # Previous button
    PIN_NEXT = 22       # Next button
    PIN_VOL_DOWN = 10   # Volume down button
    PIN_VOL_UP = 9      # Volume up button
    PIN_LED = 23        # Play button LED
    
    # Paths
    USB_MOUNT_BASE = '/media/admin'
    STATE_FILE = '/home/admin/story_box/state.json'
    SOUNDS_DIR = '/usr/share/storybox/sounds'
    
    # Audio settings
    AUDIO_CARD = 0      # HiFiBerry card
    VOLUME_STEP = 0.1
    VOLUME_MIN = 0.0
    VOLUME_MAX = 0.85   # Child hearing protection
    
    # LCD
    LCD_ADDRESS = 0x27
    
    # Timings
    SELECTION_MODE_HOLD_TIME = 2.0  # Hold Prev+Next for story selection
    SHUTDOWN_HOLD_TIME = 5.0        # Hold Vol-+Vol+ for shutdown
    
    def __init__(self):
        """Initialize Story Box"""
        print("=" * 60)
        print("STORY BOX INITIALIZING")
        print("=" * 60)
        
        # Initialize LCD
        try:
            self.lcd = CharLCD(
                i2c_expander='PCF8574',
                address=self.LCD_ADDRESS,
                cols=16,
                rows=2,
                charmap='A00'
            )
            self.lcd.clear()
            self.lcd.write_string("Story Box")
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string("Starting...")
            print("✓ LCD initialized")
        except Exception as e:
            print(f"✗ LCD failed: {e}")
            self.lcd = None
        
        # Clean up GPIO
        try:
            GPIO.cleanup()
        except:
            pass
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup button inputs
        GPIO.setup(self.PIN_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.PIN_PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.PIN_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.PIN_VOL_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.PIN_VOL_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Setup LED output
        GPIO.setup(self.PIN_LED, GPIO.OUT)
        GPIO.output(self.PIN_LED, GPIO.HIGH)  # OFF
        
        print("✓ GPIO initialized")
        
        # Initialize audio
        os.environ['SDL_AUDIODRIVER'] = 'alsa'
        os.environ['AUDIODEV'] = f'hw:{self.AUDIO_CARD},0'
        
        print(f"Initializing audio on card {self.AUDIO_CARD}...")
        try:
            pygame.mixer.init(
                frequency=48000,  # Match HiFiBerry sample rate
                size=-16,
                channels=2,
                buffer=8192  # Large buffer for Pi Zero
            )
            
            self.volume = 0.7
            pygame.mixer.music.set_volume(self.volume)
            print("✓ Audio initialized")
            
        except Exception as e:
            print(f"✗ Audio failed: {e}")
            self.update_display("Audio Error!", str(e)[:16])
            raise
        
        # Load sound effects
        self.sounds = {}
        self.load_sounds()
        
        # Playback state
        self.current_folder = None
        self.playlist = []
        self.current_track_index = 0
        self.is_playing = False
        self.is_paused = False
        
        # Story selection
        self.available_folders = []
        self.selected_folder_index = 0
        self.in_selection_mode = False
        
        # Auto-play setting
        self.auto_play = True  # Auto-play on startup
        
        # Threads
        self.stop_event = Event()
        
        self.monitor_thread = Thread(target=self.monitor_playback, daemon=True)
        self.monitor_thread.start()
        
        self.button_thread = Thread(target=self.poll_buttons, daemon=True)
        self.button_thread.start()
        
        print("✓ Story Box initialized\n")
        
        # Play startup sound
        self.play_sound('startup')
        self.update_display("Ready!", "Insert USB")
    
    def load_sounds(self):
        """Load sound effects"""
        sound_files = {
            'startup': 'startup.wav',
            'button': 'button.wav',
            'story_loaded': 'story_loaded.wav',
            'goodbye': 'goodbye.wav',
            'error': 'error.wav'
        }
        
        for name, filename in sound_files.items():
            path = os.path.join(self.SOUNDS_DIR, filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(0.5)  # Quieter than music
                    print(f"✓ Loaded sound: {name}")
                except Exception as e:
                    print(f"✗ Failed to load {name}: {e}")
            else:
                print(f"⚠ Sound not found: {path}")
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def save_state(self):
        """Save current playback state"""
        if not self.current_folder or not self.playlist:
            return
        
        state = {
            'folder_path': str(self.current_folder),
            'track_index': self.current_track_index,
            'volume': self.volume,
            'auto_play': self.auto_play
        }
        
        try:
            with open(self.STATE_FILE, 'w') as f:
                json.dump(state, f)
            print(f"✓ State saved")
        except Exception as e:
            print(f"✗ Failed to save state: {e}")
    
    def load_state(self):
        """Load previous playback state"""
        if not os.path.exists(self.STATE_FILE):
            return False
        
        try:
            with open(self.STATE_FILE, 'r') as f:
                state = json.load(f)
            
            folder_path = Path(state['folder_path'])
            
            if folder_path.exists() and folder_path.is_dir():
                audio_extensions = ['*.mp3', '*.MP3', '*.wav', '*.WAV',
                                  '*.ogg', '*.OGG', '*.flac', '*.FLAC',
                                  '*.m4a', '*.M4A']
                
                audio_files = []
                for ext in audio_extensions:
                    audio_files.extend(folder_path.glob(ext))
                
                if audio_files:
                    self.current_folder = folder_path
                    self.playlist = sorted(audio_files)
                    self.current_track_index = state.get('track_index', 0)
                    
                    if self.current_track_index >= len(self.playlist):
                        self.current_track_index = 0
                    
                    self.volume = state.get('volume', 0.7)
                    self.auto_play = state.get('auto_play', True)
                    pygame.mixer.music.set_volume(self.volume)
                    
                    folder_name = self.current_folder.name.replace('_', ' ')
                    if len(folder_name) > 3 and folder_name[:2].isdigit():
                        folder_name = folder_name[3:]
                    
                    print(f"✓ Restored: {folder_name}")
                    print(f"✓ Track: {self.current_track_index + 1}/{len(self.playlist)}")
                    
                    self.update_display(folder_name[:16], "Ready to play")
                    return True
            
            return False
            
        except Exception as e:
            print(f"✗ Failed to load state: {e}")
            return False
    
    def update_display(self, line1, line2=""):
        """Update LCD display"""
        if not self.lcd:
            return
        
        try:
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string(line1[:16])
            if line2:
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(line2[:16])
        except Exception as e:
            print(f"LCD error: {e}")
    
    def shutdown_sequence(self):
        """Perform safe shutdown"""
        print("\n→ Shutdown initiated")
        
        # Save state
        self.save_state()
        
        # Stop playback
        if self.is_playing:
            pygame.mixer.music.stop()
        
        # Visual feedback
        self.update_display("Shutting down", "Please wait...")
        self.play_sound('goodbye')
        
        # Blink LED
        for i in range(5):
            GPIO.output(self.PIN_LED, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.PIN_LED, GPIO.HIGH)
            time.sleep(0.2)
        
        # Final message
        self.update_display("Safe to", "power off now")
        time.sleep(2)
        
        # Cleanup
        if self.lcd:
            self.lcd.clear()
        GPIO.cleanup()
        
        # Shutdown
        print("Executing shutdown...")
        os.system("sudo shutdown -h now")
    
    def poll_buttons(self):
        """Poll button states"""
        prev_states = {
            self.PIN_PLAY: 1,
            self.PIN_PREV: 1,
            self.PIN_NEXT: 1,
            self.PIN_VOL_DOWN: 1,
            self.PIN_VOL_UP: 1
        }
        
        selection_hold_start = None
        shutdown_hold_start = None
        
        while not self.stop_event.is_set():
            # Check for shutdown combo (Vol- + Vol+ held together)
            vol_down_pressed = GPIO.input(self.PIN_VOL_DOWN) == 0
            vol_up_pressed = GPIO.input(self.PIN_VOL_UP) == 0
            
            if vol_down_pressed and vol_up_pressed:
                if shutdown_hold_start is None:
                    shutdown_hold_start = time.time()
                    self.update_display("Hold 5s to", "shutdown...")
                    print("Shutdown combo detected...")
                elif time.time() - shutdown_hold_start > self.SHUTDOWN_HOLD_TIME:
                    self.shutdown_sequence()
                    return  # Exit thread
            else:
                if shutdown_hold_start is not None:
                    # Released early, restore display
                    print("Shutdown cancelled")
                    if self.is_playing and self.playlist:
                        story_name = self.current_folder.name.replace('_', ' ')
                        if len(story_name) > 3 and story_name[:2].isdigit():
                            story_name = story_name[3:]
                        story_name = story_name[:16]
                        
                        if self.is_paused:
                            self.update_display(story_name, "Paused")
                        else:
                            track = self.playlist[self.current_track_index]
                            track_name = track.stem.replace('_', ' ')
                            if len(track_name) > 3 and track_name[:2].isdigit():
                                track_name = track_name[3:]
                            self.update_display(story_name, track_name[:16])
                    else:
                        self.update_display("Ready!", "")
                shutdown_hold_start = None
            
            # Check for story selection mode (hold Prev + Next together)
            prev_pressed = GPIO.input(self.PIN_PREV) == 0
            next_pressed = GPIO.input(self.PIN_NEXT) == 0
            
            if prev_pressed and next_pressed and not self.in_selection_mode:
                if selection_hold_start is None:
                    selection_hold_start = time.time()
                elif time.time() - selection_hold_start > self.SELECTION_MODE_HOLD_TIME:
                    self.enter_selection_mode()
                    selection_hold_start = None
                    time.sleep(0.5)
            else:
                selection_hold_start = None
            
            # Normal button handling
            if not self.in_selection_mode and shutdown_hold_start is None:
                for pin in prev_states.keys():
                    state = GPIO.input(pin)
                    
                    if state == 0 and prev_states[pin] == 1:
                        self.play_sound('button')
                        
                        if pin == self.PIN_PLAY:
                            self.button_play()
                        elif pin == self.PIN_PREV:
                            self.button_prev()
                        elif pin == self.PIN_NEXT:
                            self.button_next()
                        elif pin == self.PIN_VOL_DOWN:
                            self.button_vol_down()
                        elif pin == self.PIN_VOL_UP:
                            self.button_vol_up()
                        
                        time.sleep(0.3)
                    
                    prev_states[pin] = state
            elif self.in_selection_mode:
                # Selection mode button handling
                if GPIO.input(self.PIN_NEXT) == 0 and prev_states[self.PIN_NEXT] == 1:
                    self.play_sound('button')
                    self.browse_next_story()
                    time.sleep(0.3)
                
                if GPIO.input(self.PIN_PREV) == 0 and prev_states[self.PIN_PREV] == 1:
                    self.play_sound('button')
                    self.browse_prev_story()
                    time.sleep(0.3)
                
                if GPIO.input(self.PIN_PLAY) == 0 and prev_states[self.PIN_PLAY] == 1:
                    self.play_sound('button')
                    self.select_current_story()
                    time.sleep(0.3)
                
                # Update prev states
                for pin in prev_states.keys():
                    prev_states[pin] = GPIO.input(pin)
            
            time.sleep(0.05)
    
    def enter_selection_mode(self):
        """Enter story selection mode"""
        print("\n→ Entering story selection mode")
        self.in_selection_mode = True
        
        # Scan for all folders
        self.scan_all_folders()
        
        if self.available_folders:
            self.selected_folder_index = 0
            self.show_story_selection()
            self.play_sound('story_loaded')
        else:
            self.update_display("No stories", "found!")
            self.play_sound('error')
            time.sleep(2)
            self.in_selection_mode = False
    
    def scan_all_folders(self):
        """Scan USB for all story folders"""
        os.system('sudo mount /dev/sda1 /media/admin/STORYBOX 2>/dev/null')
        
        self.available_folders = []
        
        if not os.path.exists(self.USB_MOUNT_BASE):
            return
        
        try:
            for mount in Path(self.USB_MOUNT_BASE).iterdir():
                if mount.is_dir():
                    folders = sorted([f for f in mount.iterdir() if f.is_dir()])
                    
                    for folder in folders:
                        # Check if folder has audio
                        audio_extensions = ['*.mp3', '*.MP3', '*.wav', '*.WAV',
                                          '*.ogg', '*.OGG', '*.flac', '*.FLAC',
                                          '*.m4a', '*.M4A']
                        
                        has_audio = False
                        for ext in audio_extensions:
                            if list(folder.glob(ext)):
                                has_audio = True
                                break
                        
                        if has_audio:
                            self.available_folders.append(folder)
        except Exception as e:
            print(f"Error scanning folders: {e}")
        
        print(f"Found {len(self.available_folders)} stories")
    
    def show_story_selection(self):
        """Show current story in selection"""
        if not self.available_folders:
            return
        
        folder = self.available_folders[self.selected_folder_index]
        folder_name = folder.name.replace('_', ' ')
        
        # Remove leading numbers from folder name
        if len(folder_name) > 3 and folder_name[:2].isdigit():
            folder_name = folder_name[3:]
        
        self.update_display(
            f"Story {self.selected_folder_index + 1}/{len(self.available_folders)}",
            folder_name[:16]
        )
    
    def browse_next_story(self):
        """Browse to next story"""
        if not self.available_folders:
            return
        
        self.selected_folder_index += 1
        if self.selected_folder_index >= len(self.available_folders):
            self.selected_folder_index = 0
        
        self.show_story_selection()
    
    def browse_prev_story(self):
        """Browse to previous story"""
        if not self.available_folders:
            return
        
        self.selected_folder_index -= 1
        if self.selected_folder_index < 0:
            self.selected_folder_index = len(self.available_folders) - 1
        
        self.show_story_selection()
    
    def select_current_story(self):
        """Select and load current story"""
        if not self.available_folders:
            return
        
        folder = self.available_folders[self.selected_folder_index]
        
        # Load this folder
        audio_extensions = ['*.mp3', '*.MP3', '*.wav', '*.WAV',
                          '*.ogg', '*.OGG', '*.flac', '*.FLAC',
                          '*.m4a', '*.M4A']
        
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(folder.glob(ext))
        
        if audio_files:
            self.current_folder = folder
            self.playlist = sorted(audio_files)
            self.current_track_index = 0
            
            folder_name = folder.name.replace('_', ' ')
            if len(folder_name) > 3 and folder_name[:2].isdigit():
                folder_name = folder_name[3:]
            
            print(f"✓ Selected: {folder_name}")
            self.update_display(folder_name[:16], "Loading...")
            self.play_sound('story_loaded')
            time.sleep(1)
            
            self.save_state()
            self.in_selection_mode = False
            
            # Auto-start playing
            self.play_current_track()
    
    def find_usb_mounts(self):
        """Find USB devices"""
        usb_mounts = []
        
        if not os.path.exists(self.USB_MOUNT_BASE):
            return usb_mounts
        
        try:
            for mount in Path(self.USB_MOUNT_BASE).iterdir():
                if mount.is_dir():
                    usb_mounts.append(mount)
        except:
            pass
        
        return usb_mounts
    
    def scan_for_audio(self):
        """Scan for audio files (loads first story found)"""
        os.system('sudo mount /dev/sda1 /media/admin/STORYBOX 2>/dev/null')
        
        usb_mounts = self.find_usb_mounts()
        
        if not usb_mounts:
            return None
        
        for usb_mount in usb_mounts:
            folders = sorted([f for f in usb_mount.iterdir() if f.is_dir()])
            
            if not folders:
                folders = [usb_mount]
            
            for folder in folders:
                audio_extensions = ['*.mp3', '*.MP3', '*.wav', '*.WAV',
                                  '*.ogg', '*.OGG', '*.flac', '*.FLAC',
                                  '*.m4a', '*.M4A']
                
                audio_files = []
                for ext in audio_extensions:
                    audio_files.extend(folder.glob(ext))
                
                if audio_files:
                    return folder, sorted(audio_files)
        
        return None
    
    def load_audio_folder(self):
        """Load audio from USB"""
        self.update_display("Scanning...", "Please wait")
        print("\nScanning for audio...")
        
        result = self.scan_for_audio()
        
        if result:
            folder, files = result
            self.current_folder = folder
            self.playlist = files
            self.current_track_index = 0
            
            folder_name = folder.name.replace('_', ' ')
            if len(folder_name) > 3 and folder_name[:2].isdigit():
                folder_name = folder_name[3:]
            
            print(f"✓ Loaded: {folder_name}")
            print(f"✓ Tracks: {len(files)}")
            
            self.update_display(folder_name[:16], f"{len(files)} tracks")
            self.play_sound('story_loaded')
            self.save_state()
            time.sleep(2)
            return True
        else:
            print("✗ No audio found")
            self.update_display("No audio found", "Insert USB")
            self.play_sound('error')
            return False
    
    def play_current_track(self):
        """Play current track"""
        if not self.playlist:
            return
        
        track = self.playlist[self.current_track_index]
        
        try:
            pygame.mixer.music.load(str(track))
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            GPIO.output(self.PIN_LED, GPIO.LOW)
            
            story_name = self.current_folder.name.replace('_', ' ')
            if len(story_name) > 3 and story_name[:2].isdigit():
                story_name = story_name[3:]
            story_name = story_name[:16]
            
            track_name = track.stem.replace('_', ' ')
            if len(track_name) > 3 and track_name[:2].isdigit():
                track_name = track_name[3:]
            
            self.update_display(story_name, track_name[:16])
            
            print(f"▶ Playing [{self.current_track_index + 1}/{len(self.playlist)}]: {track.name}")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            self.update_display("Error playing", "track")
            self.play_sound('error')
            GPIO.output(self.PIN_LED, GPIO.HIGH)
    
    def stop_playback(self):
        """Stop playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        GPIO.output(self.PIN_LED, GPIO.HIGH)
        
        if self.current_folder:
            story_name = self.current_folder.name.replace('_', ' ')
            if len(story_name) > 3 and story_name[:2].isdigit():
                story_name = story_name[3:]
            self.update_display(story_name[:16], "Stopped")
        else:
            self.update_display("Stopped", "")
        
        print("■ Stopped")
    
    def pause_playback(self):
        """Pause/unpause"""
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                GPIO.output(self.PIN_LED, GPIO.LOW)
                
                story_name = self.current_folder.name.replace('_', ' ')
                if len(story_name) > 3 and story_name[:2].isdigit():
                    story_name = story_name[3:]
                story_name = story_name[:16]
                
                track = self.playlist[self.current_track_index]
                track_name = track.stem.replace('_', ' ')
                if len(track_name) > 3 and track_name[:2].isdigit():
                    track_name = track_name[3:]
                
                self.update_display(story_name, track_name[:16])
                print("▶ Resumed")
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                GPIO.output(self.PIN_LED, GPIO.HIGH)
                
                story_name = self.current_folder.name.replace('_', ' ')
                if len(story_name) > 3 and story_name[:2].isdigit():
                    story_name = story_name[3:]
                self.update_display(story_name[:16], "Paused")
                print("⏸ Paused")
                self.save_state()
    
    def next_track(self):
        """Next track"""
        if not self.playlist:
            return
        
        self.current_track_index += 1
        if self.current_track_index >= len(self.playlist):
            self.current_track_index = 0
            print("↻ Loop to start")
        
        self.save_state()
        self.stop_playback()
        self.play_current_track()
    
    def previous_track(self):
        """Previous track"""
        if not self.playlist:
            return
        
        self.current_track_index -= 1
        if self.current_track_index < 0:
            self.current_track_index = len(self.playlist) - 1
            print("↻ Loop to end")
        
        self.save_state()
        self.stop_playback()
        self.play_current_track()
    
    def adjust_volume(self, change):
        """Adjust volume"""
        self.volume = max(self.VOLUME_MIN,
                         min(self.VOLUME_MAX, self.volume + change))
        pygame.mixer.music.set_volume(self.volume)
        
        vol_percent = int(self.volume * 100)
        bar = "=" * (vol_percent // 7)
        self.update_display(f"Volume: {vol_percent}%", bar)
        print(f"🔊 Volume: {vol_percent}%")
        
        self.save_state()
        
        time.sleep(2)
        if self.is_playing and self.playlist:
            story_name = self.current_folder.name.replace('_', ' ')
            if len(story_name) > 3 and story_name[:2].isdigit():
                story_name = story_name[3:]
            story_name = story_name[:16]
            
            if self.is_paused:
                self.update_display(story_name, "Paused")
            else:
                track = self.playlist[self.current_track_index]
                track_name = track.stem.replace('_', ' ')
                if len(track_name) > 3 and track_name[:2].isdigit():
                    track_name = track_name[3:]
                self.update_display(story_name, track_name[:16])
    
    def monitor_playback(self):
        """Monitor for track end"""
        while not self.stop_event.is_set():
            if self.is_playing and not self.is_paused:
                if not pygame.mixer.music.get_busy():
                    print("→ Auto-advance")
                    self.next_track()
            time.sleep(0.5)
    
    # Button handlers
    def button_play(self):
        """Play/Pause pressed"""
        if not self.playlist:
            if not self.load_state():
                if self.load_audio_folder():
                    if self.auto_play:
                        self.play_current_track()
            else:
                if self.auto_play:
                    self.play_current_track()
        else:
            if self.is_playing:
                self.pause_playback()
            else:
                self.play_current_track()
    
    def button_prev(self):
        """Previous pressed"""
        self.previous_track()
    
    def button_next(self):
        """Next pressed"""
        self.next_track()
    
    def button_vol_down(self):
        """Volume down pressed"""
        self.adjust_volume(-self.VOLUME_STEP)
    
    def button_vol_up(self):
        """Volume up pressed"""
        self.adjust_volume(self.VOLUME_STEP)
    
    def run(self):
        """Main loop"""
        print("Waiting for USB...")
        time.sleep(3)
        
        # Try to restore previous state
        if not self.load_state():
            self.load_audio_folder()
        
        # Auto-play if enabled
        if self.auto_play and self.playlist and not self.is_playing:
            print("→ Auto-playing last story")
            time.sleep(1)
            self.play_current_track()
        
        print("\nStory Box running")
        print("Hold Prev+Next for 2s to select stories")
        print("Hold Vol-+Vol+ for 5s to shutdown")
        print("Press Ctrl+C to exit\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
        
        self.cleanup()
    
    def cleanup(self):
        """Cleanup"""
        self.play_sound('goodbye')
        time.sleep(0.5)
        
        self.save_state()
        self.stop_event.set()
        time.sleep(0.5)
        self.stop_playback()
        
        if self.lcd:
            self.lcd.clear()
            self.lcd.write_string("Goodbye!")
        
        GPIO.output(self.PIN_LED, GPIO.HIGH)
        pygame.mixer.quit()
        GPIO.cleanup()
        print("Story Box stopped")


if __name__ == '__main__':
    try:
        story_box = StoryBox()
        story_box.run()
    except Exception as e:
        print(f"\nFatal error: {e}")
        GPIO.cleanup()
