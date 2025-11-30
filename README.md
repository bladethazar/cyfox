# Cyfox - Animated Desktop DevOps Buddy

A sophisticated, animated desktop buddy for Raspberry Pi Zero 2W with Argon40 Pod Display. Cyfox helps you stay healthy, scans your network, and keeps you entertained with Reddit posts.

## Features

### 🤖 Desktop DevOps Buddy
- **Reminders**: Gently reminds you to eat, drink, rest, and focus
- **Smooth Animations**: Beautiful sprite-based animations for different states
- **Interactive**: 4-button control for navigation and interaction

### 🔍 Network Vulnerability Scanner
- **Bjorn-inspired**: Network scanning and vulnerability detection
- **Automatic Scanning**: Periodic network scans with customizable intervals
- **Service Detection**: Identifies open ports and services
- **Vulnerability Checks**: Basic vulnerability detection for common services

### 📱 Reddit Integration
- **IT/DevOps Content**: Fetches posts from ProgrammerHumor, sysadmin, devops, and linuxmemes
- **Auto-refresh**: Periodically updates with new content
- **Navigation**: Browse posts using button controls

## Architecture

Cyfox is built with a modular architecture:

```
cyfox/
├── core/           # Core state management and configuration
├── display/        # Argon40 Pod Display handling
├── animation/      # Sprite animation system
├── buttons/        # GPIO button handling
└── modules/        # Functional modules
    ├── reminder.py    # Reminder system
    ├── scanner.py     # Network scanner
    └── reddit.py      # Reddit fetcher
```

## Prerequisites

### Hardware
- Raspberry Pi Zero 2W
- Argon40 Pod Display (2.13" e-Paper HAT)
- MicroSD card with Raspberry Pi OS

### Software
- Raspberry Pi OS (64-bit recommended)
- Python 3.11+
- Docker (for containerized deployment)
- k3s (for Kubernetes deployment)

## Installation

### Local Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd cyfox
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure**:
   Edit `config/config.yaml` to match your setup

4. **Run**:
   ```bash
   python run.py
   ```

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t cyfox:latest .
   ```

2. **Run container** (with hardware access):
   ```bash
   docker run --privileged \
     --network host \
     --pid host \
     -v /dev:/dev \
     -v /sys:/sys \
     cyfox:latest
   ```

### k3s Deployment

See [k8s/README.md](k8s/README.md) for detailed Kubernetes deployment instructions.

## Configuration

Edit `config/config.yaml` to customize:

- **Display settings**: Resolution, FPS
- **Animation settings**: Frame rates, transitions
- **Reminder intervals**: Eating, drinking, resting, focusing
- **Network scanner**: Scan intervals, network range, ports
- **Reddit**: Subreddits, fetch intervals
- **Button mappings**: GPIO pins for Argon40 Pod buttons

## Button Controls

- **Button 1**: Acknowledge reminder/alert
- **Button 2**: Next Reddit post (in Reddit mode)
- **Button 3**: Start network scan (in Scanner mode)
- **Button 4**: Cycle through modes (Buddy → Scanner → Reddit)

## Modes

### Buddy Mode (Default)
Cyfox acts as your desktop buddy, showing reminders and animations.

### Scanner Mode
Cyfox scans your network for vulnerabilities and open ports.

### Reddit Mode
Cyfox displays IT/DevOps related Reddit posts.

## Animation System

The animation system supports:
- State-based animations (idle, eating, drinking, etc.)
- Smooth transitions
- Customizable frame rates
- Sprite sheet support (for future expansion)

To add more animations, create sprite sheets and update the `AnimationManager`.

## Development

### Project Structure
```
cyfox/
├── cyfox/          # Main package
│   ├── core/       # Core functionality
│   ├── display/    # Display handling
│   ├── animation/  # Animation system
│   ├── buttons/    # Button handling
│   └── modules/    # Feature modules
├── config/         # Configuration files
├── frontend/       # Frontend assets (sprites)
├── k8s/           # Kubernetes manifests
└── requirements.txt
```

### Adding New Modules

1. Create a new module in `cyfox/modules/`
2. Inherit from base module pattern
3. Register with main application in `cyfox/main.py`
4. Add configuration to `config/config.yaml`

## Troubleshooting

### Display Not Working
- Ensure Argon40 Pod drivers are installed: `curl https://download.argon40.com/podsystem.sh | bash`
- Check display connection
- Verify GPIO permissions

### Buttons Not Responding
- Check GPIO pin mappings in config
- Verify RPi.GPIO is installed
- Check container has GPIO access (privileged mode)

### Network Scanner Issues
- Ensure nmap is installed (optional, for advanced scanning)
- Check network permissions
- Verify network range in config

## Future Enhancements

- [ ] AI personality integration
- [ ] Enhanced sprite animations with multiple frames
- [ ] Web interface for remote monitoring
- [ ] More advanced vulnerability detection
- [ ] Custom attack modules (like Bjorn)
- [ ] Voice interactions
- [ ] Integration with home automation

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please read CONTRIBUTING.md (to be created) for guidelines.

## Acknowledgments

- Inspired by [Bjorn](https://github.com/infinition/Bjorn) for network scanning concepts
- Built for Argon40 Pod Display
