## A. Create Sounds Directory

```bash
# Create system sounds directory
sudo mkdir -p /usr/share/storybox/sounds
sudo chown admin:admin /usr/share/storybox/sounds
```
## B. Generate Sound Effects (Using sox)

```bash
# Install sox
sudo apt-get install -y sox

# Navigate to sounds directory
cd /usr/share/storybox/sounds

# Create startup sound (ascending chime)
sox -n startup.wav synth 0.2 sine 523 0.2 sine 659 0.2 sine 784

# Create button press sound (short beep)
sox -n button.wav synth 0.05 sine 1000

# Create story loaded sound (success chime)
sox -n story_loaded.wav synth 0.1 sine 659 0.1 sine 784 0.2 sine 1047

# Create goodbye sound (descending chime)
sox -n goodbye.wav synth 0.2 sine 784 0.2 sine 659 0.2 sine 523

# Create error sound (low beep)
sox -n error.wav synth 0.3 sine 200

# Verify files created
ls -lh /usr/share/storybox/sounds/
```
