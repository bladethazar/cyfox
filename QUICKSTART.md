# Quick Start Guide

Get Cyfox up and running quickly!

## Prerequisites

- Raspberry Pi Zero 2W
- Argon40 Pod Display connected
- Raspberry Pi OS installed
- Python 3.11+

## Installation

### Option 1: Local Installation

```bash
# Clone repository
git clone <your-repo-url>
cd cyfox

# Install dependencies
pip install -r requirements.txt

# Run
python run.py
```

### Option 2: Using Make

```bash
make install
make run
```

### Option 3: Quick Start Script

```bash
./scripts/quick_start.sh
```

## Docker Deployment

### Build Image

```bash
docker build -t cyfox:latest .
```

### Run Container

```bash
docker run --privileged \
  --network host \
  --pid host \
  -v /dev:/dev \
  -v /sys:/sys \
  cyfox:latest
```

## k3s Deployment

```bash
# Apply manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods -n cyfoxlab
kubectl logs -n cyfoxlab -l app=cyfox
```

## Configuration

Edit `config/config.yaml` to customize:

- **Reminder intervals**: How often to remind you
- **Network scanner**: Scan range and ports
- **Reddit**: Subreddits to fetch from
- **Buttons**: GPIO pin mappings

## First Run

1. **Start Cyfox**: `python run.py`
2. **See Cyfox idle**: Default animation should appear
3. **Press Button 4**: Cycle through modes (Buddy → Scanner → Reddit)
4. **Wait for reminder**: First reminder will appear after configured interval
5. **Press Button 1**: Acknowledge reminder

## Troubleshooting

### Display Not Working

```bash
# Install Argon40 Pod drivers
curl https://download.argon40.com/podsystem.sh | bash
argonpod-config
```

### Buttons Not Working

```bash
# Check GPIO permissions
groups  # Should include 'gpio' group
sudo usermod -a -G gpio $USER
# Logout and login again
```

### Import Errors

```bash
# Install missing dependencies
pip install -r requirements.txt
```

### Docker Issues

```bash
# Ensure privileged mode and host networking
docker run --privileged --network host --pid host ...
```

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [DEVELOPMENT.md](DEVELOPMENT.md) for development guide
- See [ARCHITECTURE.md](ARCHITECTURE.md) for architecture details

## Getting Help

- Check logs: `kubectl logs -n cyfoxlab -l app=cyfox`
- Review configuration: `config/config.yaml`
- Check GPIO: `gpio readall` (if installed)

