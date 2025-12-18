```
╔═══════════════════════════════════════════════════════════╗
║              STORY BOX - QUICK REFERENCE                  ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  CONTROLS:                                                ║
║  ─────────                                                ║
║  Play            Play / Pause                             ║
║  Next            Next track                               ║
║  Prev            Previous track                           ║
║  Vol+            Volume up                                ║
║  Vol-            Volume down                              ║
║                                                           ║
║  SPECIAL:                                                 ║
║  ────────                                                 ║
║  Hold Prev+Next 2s    Story selection mode                ║
║  Hold Vol-+Vol+ 5s    Safe shutdown                       ║
║                                                           ║
║  STARTUP:                                                 ║
║  ────────                                                 ║
║  1. Insert USB with stories                               ║
║  2. Power on                                              ║
║  3. Auto-plays last story                                 ║
║                                                           ║
║  SHUTDOWN:                                                ║
║  ─────────                                                ║
║  1. Hold Vol- and Vol+ for 5 seconds                      ║
║  2. Wait for "Safe to power off"                          ║
║  3. Unplug power                                          ║
║                                                           ║
║  TROUBLESHOOTING:                                         ║
║  ────────────────                                         ║
║  No sound        → Check speaker connections              ║
║  No USB          → Reformat as FAT32                      ║
║  Buttons stuck   → Check GPIO wiring                      ║
║  LCD blank       → Run: sudo i2cdetect -y 1               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```
```
Hardware Assembly:
□ Audio bonnet stacked on Pi GPIO
□ Extra-tall stacking header installed
□ LCD wired (4 wires: VCC, GND, SDA, SCL)
□ All 5 buttons wired correctly
□ Play button LED wired
□ Speakers connected to bonnet terminals
□ All connections secure
□ Button panel mounted safely

Software Configuration:
□ /boot/config.txt configured
□ All packages installed
□ Sound effects created
□ Main script installed
□ Script is executable
□ Systemd service created
□ Service enabled and running

Testing:
□ LCD displays correctly
□ Audio plays through speakers
□ All buttons respond
□ LED lights during playback
□ Story selection works
□ Auto-play works
□ Shutdown works
□ State saving works

USB Content:
□ Drive formatted FAT32
□ Folders properly named
□ Audio files in folders
□ Files numbered correctly
□ USB auto-mounts

Ready to Use:
□ Enclosure complete (if applicable)
□ All wiring tucked away
□ No sharp edges exposed
□ Child-safe construction
□ Parent instructions provided
```
