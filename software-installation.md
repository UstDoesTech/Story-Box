## A. Update System
```bash
sudo apt-get update
sudo apt-get upgrade -y
```
## B. Install Required Packages

```bash
# Core packages
sudo apt-get install -y python3-pygame python3-rpi.gpio i2c-tools

# LCD library
pip3 install RPLCD --break-system-packages

# USB auto-mount
sudo apt-get install -y udisks2
sudo systemctl enable udisks2
```
## C. Disable GUI (Recommended for Performance)

```bash
# Boot to console instead of desktop
sudo systemctl set-default multi-user.target

# Reboot to apply
sudo reboot
```
After reboot, connect via SSH:

```bash
ssh admin@storybox.local
```
## D. Disable Unnecessary Services

```bash
# Disable services to reduce CPU load
sudo systemctl disable bluetooth
sudo systemctl stop bluetooth
sudo systemctl mask pipewire pipewire.socket
```

## E. Disable Auto-playing Speaker Test

```bash
# Check for and disable aplay service
sudo systemctl stop aplay.service
sudo systemctl disable aplay.service
sudo systemctl mask aplay.service
```
