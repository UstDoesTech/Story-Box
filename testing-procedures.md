## A. Test Individual Components

### Test LCD Display

```bash
python3 << 'EOF'
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
lcd.clear()
lcd.write_string('Story Box')
lcd.cursor_pos = (1, 0)
lcd.write_string('LCD Works!')
print("LCD test complete - check display")
EOF
```

### Test Audio

```bash
# List audio devices
aplay -l

# Test speakers (card 0)
speaker-test -Dhw:0,0 -c2 -t wav
# Press Ctrl+C after hearing sound

# Test with sound file
aplay -D hw:0,0 /usr/share/storybox/sounds/startup.wav
```

### Test Individual Button

```bash
python3 << 'EOF'
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press Play button (Ctrl+C to exit)")
try:
    while True:
        if GPIO.input(17) == GPIO.LOW:
            print("PLAY BUTTON PRESSED!")
            time.sleep(0.3)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nTest complete")
EOF
```
Repeat for other buttons (GPIO 27, 22, 10, 9).

### Test LED

```bash
python3 << 'EOF'
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

print("Blinking LED 5 times...")
for i in range(5):
    GPIO.output(23, GPIO.LOW)   # ON
    print("LED ON")
    time.sleep(0.5)
    GPIO.output(23, GPIO.HIGH)  # OFF
    print("LED OFF")
    time.sleep(0.5)

GPIO.cleanup()
print("LED test complete")
EOF
```

## B. Test Complete System

```bash
python3 /home/admin/story_box/storybox.py
```
Test checklist:

[] LCD shows "Ready! Insert USB"
[] Startup sound plays
[] All 5 buttons beep when pressed
[] Play button LED lights during playback
[] Volume controls work
[] Track navigation works
[] Story selection mode works (hold Prev+Next)
[] Shutdown works (hold Vol-+Vol+)
