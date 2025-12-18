## **A. No Audio Output**
```
Problem: Speakers are silent
Solutions:
1. Check audio card:
   aplay -l
   (should show card 0: sndrpihifiberry)

2. Check speaker connections to bonnet terminals

3. Test with speaker-test:
   speaker-test -Dhw:0,0 -c2 -t wav

4. Check volume isn't at minimum

5. Verify audio bonnet fully seated on GPIO pins

6. Check /boot/config.txt has correct settings
```

## **B. Crackling Audio**
```
Problem: Audio is distorted or crackly
Solutions:
1. Increase buffer in code:
   buffer=8192 → buffer=16384

2. Reduce sample rate:
   frequency=48000 → frequency=44100

3. Check power supply (need 2.5A minimum)

4. Disable GUI if running

5. Use lower bitrate MP3 files (128kbps)

6. Ensure bonnet is fully seated
```

## **C. Buttons Not Working**
```
Problem: Button presses don't respond
Solutions:
1. Test individual button:
   python3 button_test_script.py

2. Check GPIO wiring matches diagram

3. Verify buttons connected to bonnet TOP pins

4. Check button wiring:
   - Switch NO → GPIO pin
   - Switch COM → GND

5. Restart service:
   sudo systemctl restart storybox.service
```

## **D. LCD Not Working**
```
Problem: LCD blank or showing garbage
Solutions:
1. Check I2C bus:
   sudo i2cdetect -y 1
   (should show address 27 or 3f)

2. Check LCD connections:
   VCC → Pin 2 (5V)
   GND → Pin 6 (GND)
   SDA → Pin 3 (GPIO 2)
   SCL → Pin 5 (GPIO 3)

3. Try alternate I2C address:
   Change LCD_ADDRESS = 0x3f in code

4. Check /boot/config.txt:
   dtparam=i2c_arm=on

5. Reboot
```

## **E. USB Not Detected**
```
Problem: "No audio found" message
Solutions:
1. Check USB is FAT32 formatted

2. Verify folder structure:
   - Folders contain audio files
   - Files have supported extensions

3. Manual mount:
   sudo mount /dev/sda1 /media/admin/STORYBOX

4. Check USB drive detected:
   lsblk
   (should show sda1)

5. Check permissions:
   sudo chmod -R 755 /media/admin/STORYBOX

6. Try different USB drive
```

## **F. Service Won't Start**
```
Problem: Systemd service fails
Solutions:
1. Check status:
   sudo systemctl status storybox.service

2. View logs:
   sudo journalctl -u storybox.service -n 50

3. Verify paths in service file:
   /home/admin/story_box/storybox.py exists

4. Check file permissions:
   chmod +x /home/admin/story_box/storybox.py

5. Test manually:
   python3 /home/admin/story_box/storybox.py

6. Reload systemd:
   sudo systemctl daemon-reload
```

## **G. Shutdown Not Working**
```
Problem: Can't shutdown with buttons
Solutions:
1. Check both Vol buttons work individually

2. Verify holding for full 5 seconds

3. Check GPIO wiring for Vol+/Vol- buttons

4. Use manual shutdown:
   sudo shutdown -h now

5. Check logs for errors:
   sudo journalctl -u storybox.service -f
```

## **H. Audio Device Busy**
```
Problem: "ALSA: Couldn't open audio device: Device or resource busy"
Solutions:
1. Check what's using audio:
   sudo fuser -v /dev/snd/*

2. Kill conflicting processes:
   sudo pkill aplay
   sudo pkill python3

3. Stop pipewire:
   systemctl --user stop pipewire pipewire.socket

4. Reboot:
   sudo reboot
```
