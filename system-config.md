## A. Configure Boot Settings
```bash
sudo nano /boot/config.txt
```
Add or ensure these lines exist:
```ini
# ═══════════════════════════════════════════════════
# Story Box Audio Configuration
# ═══════════════════════════════════════════════════

# Disable onboard audio (conflicts with I2S)
dtparam=audio=off

# Disable HDMI audio
dtoverlay=vc4-kms-v3d,noaudio

# Enable I2S for Audio Bonnet
dtparam=i2s=on
dtoverlay=hifiberry-dac

# Enable I2C for LCD Display
dtparam=i2c_arm=on
dtparam=i2c1=on

# Optional: Performance boost for Pi Zero 2 W
arm_freq=1000
over_voltage=2

# Optional: Disable Bluetooth to save power
dtoverlay=disable-bt
```
Save (Ctrl+X, Y, Enter) and reboot:
```bash
sudo reboot
```
## B. Verify Configuration After Reboot
```bash
# Check audio card detected
aplay -l
# Should show: card 0: sndrpihifiberry [snd_rpi_hifiberry_dac]

# Check I2C bus active
ls /dev/i2c*
# Should show: /dev/i2c-1

# Detect LCD on I2C bus
sudo i2cdetect -y 1
# Should show address: 27 or 3f (LCD address)

# Test speakers
speaker-test -Dhw:0,0 -c2 -t wav
# Press Ctrl+C to stop after verifying sound
```
