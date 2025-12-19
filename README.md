# Story Box 📖🔊

A DIY children's audio player built on Raspberry Pi Zero 2 W that brings stories to life through tactile buttons, an LCD display, and quality audio playback.

Perfect for young children to independently listen to their favorite stories, audiobooks, and bedtime tales without screens.

![Story Box](https://img.shields.io/badge/Platform-Raspberry%20Pi%20Zero%202W-red)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 What is Story Box?

Story Box is a screen-free audio player designed for children. Simply insert a USB drive with your favorite stories, press the big green play button, and let the adventure begin! With large, colorful buttons and a simple LCD display, even young children can navigate between stories and control their listening experience.

**Key Features:**
- 🎵 Multi-story support with folder-based organization
- 🔘 5 large, tactile buttons (Play, Next, Prev, Vol+, Vol-)
- 📟 16x2 LCD display showing current story and track
- 💾 Remembers last played position
- 🔊 High-quality I2S audio through 3W stereo speakers
- 🔒 Child-safe volume limiting and safe shutdown
- 🎨 LED feedback on play button

---

## 📚 Documentation Guide

This repository contains comprehensive documentation to build your own Story Box. Follow the steps in order for the best experience.

### 🛠️ **Building Your Story Box**

#### **1. [Hardware Requirements](hardware-requirements.md)**
Start here! This document lists all the components you need to purchase, including:
- Raspberry Pi Zero 2 W
- Audio bonnet and speakers
- LCD display and buttons
- Total cost breakdown (~£131)

#### **2. [Wiring Guide](wiring-guide.md)**
Complete wiring diagrams and pin assignments for connecting:
- I2C LCD display (4 wires)
- 5 buttons with LED (18 wires total)
- Speakers to audio bonnet
- Detailed GPIO pin layout

#### **3. [Software Installation](software-installation.md)**
Install all required packages and dependencies:
- System updates
- Python libraries (pygame, RPi.GPIO, RPLCD)
- I2C tools and USB auto-mount
- Performance optimizations

#### **4. [System Configuration](system-config.md)**
Configure your Raspberry Pi for optimal Story Box operation:
- Boot configuration (/boot/config.txt)
- Enable I2S audio and I2C
- Disable conflicting services
- Verification tests

#### **5. [Sound Effects](sound-effects.md)**
Create audio feedback sounds using `sox`:
- Startup chime
- Button press beep
- Story loaded confirmation
- Shutdown melody

#### **6. [Story Box Code](storybox-code.md)**
Install the main Python application:
- Create project directory
- Download and install `storybox.py`
- Set proper permissions

#### **7. [Auto-Start Configuration](auto-start.md)**
Set up the Story Box to run automatically on boot:
- Create systemd service
- Enable auto-start
- Service management commands
- Log viewing

### 📀 **Preparing Your Content**

#### **8. [External Media Structure](external-media-structure.md)**
Learn how to organize stories on your USB drive:
- USB formatting (FAT32)
- Folder and file naming conventions
- Recommended audio settings
- Free audio content sources

### 🎮 **Using Your Story Box**

#### **9. [Usage Guide](usage-guide.md)**
Complete instructions for operating your Story Box:
- Startup procedure
- Button controls
- Story selection mode
- Safe shutdown process
- Display states and LED indicators

#### **10. [Quick Reference](quick-reference.md)**
One-page cheat sheet with:
- Control summary
- Special button combinations
- Troubleshooting quick tips
- Hardware and software checklists

### 🔧 **Maintenance & Support**

#### **11. [Testing Procedures](testing-procedures.md)**
Verify each component works correctly:
- Individual component tests (LCD, audio, buttons, LED)
- Complete system test checklist

#### **12. [Troubleshooting](troubleshooting.md)**
Solutions for common problems:
- No audio output
- Crackling audio
- Buttons not working
- LCD not working
- USB not detected
- Service failures

---

## 🚀 Quick Start

**Already familiar with Raspberry Pi projects?** Here's the express route:

1. **Buy hardware** → [Hardware Requirements](hardware-requirements.md)
2. **Wire everything** → [Wiring Guide](wiring-guide.md)
3. **Install software** → [Software Installation](software-installation.md) + [System Config](system-config.md)
4. **Run the code** → [Story Box Code](storybox-code.md)
5. **Set auto-start** → [Auto-Start](auto-start.md)
6. **Load stories** → [External Media Structure](external-media-structure.md)
7. **Start playing!** → [Usage Guide](usage-guide.md)

---

## 💡 Project Highlights

- **Child-Friendly**: Large buttons, no complicated menus
- **Screen-Free**: Reduces screen time while keeping kids entertained
- **Educational**: Promotes listening skills and imagination
- **Customizable**: Add any audio content you want
- **Affordable**: Total build cost around £131 plus optional enclosure
- **Safe**: Volume limiting and proper shutdown protection

---

## 📋 Technical Specifications

| Component | Specification |
|-----------|--------------|
| **Processor** | Raspberry Pi Zero 2 W (1GHz quad-core) |
| **Audio** | I2S DAC with 3W stereo speakers |
| **Display** | 16x2 RGB LCD (I2C) |
| **Controls** | 5 arcade-style buttons (1 with LED) |
| **Storage** | USB drive (FAT32, any size) |
| **Power** | 5V 2.5A+ micro USB |
| **Audio Formats** | MP3, WAV, OGG, FLAC, M4A |

---

## 🤝 Contributing

Found an issue or have an improvement? Contributions are welcome! Please feel free to:
- Report bugs
- Suggest enhancements
- Submit pull requests
- Share your build photos and improvements

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

Built with love for children who deserve screen-free story time. Special thanks to:
- The Raspberry Pi Foundation
- Adafruit for excellent I2S audio hardware
- The open-source Python community

---

## 📞 Need Help?

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review the [Quick Reference](quick-reference.md)
3. Ensure you followed all steps in the [documentation guide](#-documentation-guide)
4. Open an issue on GitHub with details about your problem

---

**Happy Story Time! 📚✨**
