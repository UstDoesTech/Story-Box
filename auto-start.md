## A. Create Systemd Service

```bash
sudo nano /etc/systemd/system/storybox.service
```

```ini
[Unit]
Description=Story Box Audio Player
After=multi-user.target network.target

[Service]
Type=simple
User=admin
WorkingDirectory=/home/admin/story_box
ExecStart=/usr/bin/python3 /home/admin/story_box/storybox.py
Restart=on-failure
RestartSec=10s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## B. Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable storybox.service

# Start service now
sudo systemctl start storybox.service

# Check status
sudo systemctl status storybox.service
```

## C. View Logs

```bash
# Live log view
sudo journalctl -u storybox.service -f

# Recent logs
sudo journalctl -u storybox.service -n 50

# Logs since last boot
sudo journalctl -u storybox.service -b
```

## D. Service Management Commands

```bash
# Stop service
sudo systemctl stop storybox.service

# Restart service
sudo systemctl restart storybox.service

# Disable auto-start
sudo systemctl disable storybox.service

# Check if enabled
systemctl is-enabled storybox.service
```
