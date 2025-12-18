## **A. Format USB Drive**
```
Format: FAT32
Label: STORYBOX (optional but recommended)
Size: Any size (8GB+ recommended)
```

## **B. Folder Structure**
```
USB Drive (STORYBOX)
│
├── 01_Goldilocks_And_Three_Bears/
│   ├── 01_Once_Upon_A_Time.mp3
│   ├── 02_The_Bears_House.mp3
│   ├── 03_Porridge_Too_Hot.mp3
│   ├── 04_Someone_Sleeping.mp3
│   └── 05_The_End.mp3
│
├── 02_Three_Little_Pigs/
│   ├── 01_Introduction.mp3
│   ├── 02_Building_Houses.mp3
│   ├── 03_The_Big_Bad_Wolf.mp3
│   └── 04_Happy_Ending.mp3
│
├── 03_Little_Red_Riding_Hood/
│   ├── 01_Going_To_Grandmas.mp3
│   ├── 02_Meeting_The_Wolf.mp3
│   └── 03_The_Woodcutter.mp3
│
└── 04_Bedtime_Stories/
    ├── 01_Sleepy_Moon_Song.mp3
    ├── 02_Counting_Stars.mp3
    └── 03_Dream_Lullaby.mp3
```

## **C. File Naming Conventions**

**Folders:**
- Number prefix (01_, 02_, etc.) for sorting
- Use underscores instead of spaces
- Keep names descriptive but not too long
- Example: `03_Gruffalo_Story`

**Files:**
- Number prefix (01_, 02_, etc.) for track order
- Descriptive names
- Supported formats: MP3, WAV, OGG, FLAC, M4A
- Example: `01_Chapter_One.mp3`

## **D. Recommended Audio Settings**
```
Format: MP3
Bitrate: 128 kbps (good quality, smaller files)
Sample Rate: 44.1 kHz or 48 kHz
Channels: Stereo
```

Lower bitrate = less CPU usage on Pi Zero.

## **E. Free Audio Content Sources**

**Public Domain Stories:**
- LibriVox (librivox.org) - Free audiobooks
- Storynory (storynory.com) - Original stories
- Loyal Books (loyalbooks.com) - Classics
- Internet Archive (archive.org) - Radio plays

**Download and organize:**
1. Download MP3 files
2. Rename with numbers
3. Create folders on USB
4. Test on Story Box
