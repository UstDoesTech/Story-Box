## Physical Assembly Stack

     Button/LCD wires
            ↓↓↓
    ┌────────────────┐
    │ Stacking Header│ ← Extra tall pins (23mm)
    │  (soldered on) │    providing accessible pins
    ├────────────────┤
    │ Audio Bonnet   │ ← Fully seated on Pi GPIO
    │   (I2S DAC)    │    (6 pins: 1,4,6,12,35,40)
    ├────────────────┤
    │ Raspberry Pi   │
    │  Zero 2 W      │
    └────────────────┘
          ↓ ↓
    Speakers connect to
    bonnet terminals

## Complete Wiring Table

┌──────────────────────────────────────────────────────────────────┐
│                    COMPLETE WIRING REFERENCE                     │
└──────────────────────────────────────────────────────────────────┘

COMPONENT           WIRE COLOR    BONNET TOP PIN    GPIO/FUNCTION
═══════════════════════════════════════════════════════════════════

LCD DISPLAY (I2C) - 4 wires
──────────────────────────────────────────────────────────────────
  VCC               Red           Pin 2             5V Power
  GND               Black         Pin 6             Ground
  SDA               Green         Pin 3             GPIO 2 (I2C Data)
  SCL               Yellow        Pin 5             GPIO 3 (I2C Clock)

PLAY BUTTON (Green 100mm) - 4 wires
──────────────────────────────────────────────────────────────────
  Switch NO         White         Pin 11            GPIO 17
  Switch COM        Black         Pin 14            Ground
  LED Positive      Red           Pin 4             5V Power
  LED Negative      Blue          Pin 16            GPIO 23 (Control)

PREV BUTTON (Yellow 60mm) - 2 wires
──────────────────────────────────────────────────────────────────
  Switch NO         White         Pin 13            GPIO 27
  Switch COM        Black         Pin 20            Ground

NEXT BUTTON (Yellow 60mm) - 2 wires
──────────────────────────────────────────────────────────────────
  Switch NO         White         Pin 15            GPIO 22
  Switch COM        Black         Pin 25            Ground

VOL DOWN BUTTON (Blue 60mm) - 2 wires
──────────────────────────────────────────────────────────────────
  Switch NO         White         Pin 19            GPIO 10
  Switch COM        Black         Pin 30            Ground

VOL UP BUTTON (Blue 60mm) - 2 wires
──────────────────────────────────────────────────────────────────
  Switch NO         White         Pin 21            GPIO 9
  Switch COM        Black         Pin 34            Ground

SPEAKERS - Connect to Audio Bonnet screw terminals
──────────────────────────────────────────────────────────────────
  Left Speaker +    Red           L+ terminal       Audio Left+
  Left Speaker -    Black         L- terminal       Audio Left-
  Right Speaker +   Red           R+ terminal       Audio Right+
  Right Speaker -   Black         R- terminal       Audio Right-

═══════════════════════════════════════════════════════════════════
TOTAL WIRING: 18 wires (4 LCD + 4 Play + 10 other buttons)
═══════════════════════════════════════════════════════════════════

## GPIO Pin Layout (Stacking Header Top View)

Looking down at the stacked assembly with bonnet on top:

     ODD PINS (LEFT SIDE)             EVEN PINS (RIGHT SIDE)
     ────────────────────             ──────────────────────

Pin 1  ● 3.3V                         ● Pin 2  (5V) ← LCD VCC
Pin 3  ● GPIO 2 (SDA) ← LCD SDA       ● Pin 4  (5V) ← LED+
Pin 5  ● GPIO 3 (SCL) ← LCD SCL       ● Pin 6  (GND) ← LCD GND
Pin 7  ●                              ● Pin 8
Pin 9  ●                              ● Pin 10
Pin 11 ● GPIO 17 ← PLAY               ● Pin 12 (GPIO 18) ✗ I2S CLK
Pin 13 ● GPIO 27 ← PREV               ● Pin 14 (GND) ← Play COM
Pin 15 ● GPIO 22 ← NEXT               ● Pin 16 (GPIO 23) ← LED-
Pin 17 ●                              ● Pin 18
Pin 19 ● GPIO 10 ← VOL-               ● Pin 20 (GND) ← Prev COM
Pin 21 ● GPIO 9  ← VOL+               ● Pin 22
Pin 23 ●                              ● Pin 24
Pin 25 ● (GND) ← Next COM             ● Pin 26
Pin 27 ●                              ● Pin 28
Pin 29 ●                              ● Pin 30 (GND) ← VolDown COM
Pin 31 ●                              ● Pin 32
Pin 33 ●                              ● Pin 34 (GND) ← VolUp COM
Pin 35 ● (GPIO 19) ✗ I2S LRCLK       ● Pin 36
Pin 37 ●                              ● Pin 38
Pin 39 ●                              ● Pin 40 (GPIO 21) ✗ I2S DATA

✗ = Reserved by audio bonnet - DO NOT CONNECT

## Audio Bonnet to Pi Connection (Under the bonnet)

These 6 pins connect bonnet to Pi (automatically when stacked):

Pin 1  (3.3V)      → Pin 1  (3.3V Power)
Pin 4  (5V)        → Pin 4  (5V Power)
Pin 6  (GND)       → Pin 6  (Ground)
Pin 12 (GPIO 18)   → Pin 12 (I2S Clock)
Pin 35 (GPIO 19)   → Pin 35 (I2S L/R Clock)
Pin 40 (GPIO 21)   → Pin 40 (I2S Data)

These are handled by stacking - no separate wiring needed.
