## **A. Starting Up**
```
1. Insert External MEdia with stories
2. Power on Raspberry Pi
3. Wait for startup sound (5-10 seconds)
4. LCD shows "Ready!"
5. Story Box loads last played story
6. Auto-plays if enabled
```

## **B. Basic Controls**
```
┌─────────────────────────────────────────┐
│        STORY BOX CONTROLS               │
├─────────────────────────────────────────┤
│ PLAY         Play / Pause current track│
│ NEXT         Skip to next track        │
│ PREV         Go to previous track      │
│ VOL+         Increase volume           │
│ VOL-         Decrease volume           │
└─────────────────────────────────────────┘
```

## **C. Story Selection**
```
1. Hold PREV + NEXT together for 2 seconds
2. Display shows: "Story 1/5" / "Story Name"
3. Press NEXT to browse forward
4. Press PREV to browse backward
5. Press PLAY to select story
6. Story loads and starts playing
```

## **D. Safe Shutdown**
```
1. Hold VOL- + VOL+ together for 5 seconds
2. Display shows: "Hold 5s to shutdown..."
3. Keep holding until display shows: "Shutting down"
4. LED blinks 5 times
5. Display shows: "Safe to power off now"
6. Wait 10 seconds
7. Unplug power
```

## **E. Display States**
```
┌──────────────────┬──────────────────┐
│ ROW 1            │ ROW 2            │
├──────────────────┼──────────────────┤
│ Story Box        │ Starting...      │ ← Startup
│ Ready!           │ Insert USB       │ ← Waiting
│ Scanning...      │ Please wait      │ ← Scanning
│ Story Name       │ Track Name       │ ← Playing
│ Story Name       │ Paused           │ ← Paused
│ Volume: 70%      │ ==============   │ ← Volume
│ Story 2/5        │ Three Pigs       │ ← Selection
│ Shutting down    │ Please wait...   │ ← Shutdown
└──────────────────┴──────────────────┘
```

## **F. LED Indicator**
```
LED State             Meaning
─────────────────────────────────────
ON (Bright)          Playing audio
OFF                  Paused or stopped
Blinking slowly      Loading
Blinking fast        Shutting down
```
