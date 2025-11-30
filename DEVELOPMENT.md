# Development Guide

This guide provides information for developing and extending Cyfox.

## Architecture Overview

Cyfox follows a modular architecture:

```
cyfox/
├── core/              # Core functionality
│   ├── config.py      # Configuration management
│   └── state.py       # State management
├── display/           # Display handling
│   ├── display.py     # Display manager
│   └── text_renderer.py  # Text rendering
├── animation/         # Animation system
│   └── animation.py   # Sprite animations
├── buttons/           # Button handling
│   └── button_handler.py  # GPIO button handler
├── modules/           # Feature modules
│   ├── reminder.py    # Reminder system
│   ├── scanner.py     # Network scanner
│   └── reddit.py      # Reddit fetcher
└── main.py           # Main application
```

## Adding New Animations

### Single Sprite
Currently, Cyfox uses a single sprite image. To add animations:

1. Create a sprite sheet with multiple frames
2. Update `AnimationManager._load_animations()` to extract frames
3. Create `Animation` objects for each state

Example sprite sheet layout:
```
[Frame1] [Frame2] [Frame3]  <- Row 1 (Idle animation)
[Frame4] [Frame5] [Frame6]  <- Row 2 (Eating animation)
```

### Animation States
Map your animations to `AnimationType` enum:
- `IDLE` - Default idle animation
- `EATING`, `DRINKING`, `RESTING`, `FOCUSING` - Reminder states
- `SCANNING` - Network scanning
- `READING` - Reading Reddit posts
- `ALERT` - Showing alerts

## Adding New Modules

1. **Create module file** in `cyfox/modules/`:
   ```python
   """Your new module"""
   import threading
   from cyfox.core.config import Config
   from cyfox.core.state import StateManager
   
   class YourModule:
       def __init__(self, config: Config, state_manager: StateManager):
           self.config = config
           self.state_manager = state_manager
           # Initialize
       
       def start(self):
           # Start background thread if needed
           pass
       
       def stop(self):
           # Cleanup
           pass
   ```

2. **Register in main.py**:
   ```python
   self.your_module = YourModule(self.config, self.state_manager)
   self.your_module.start()
   ```

3. **Add configuration** to `config/config.yaml`

4. **Add button handlers** if needed

## Button Handling

Buttons are mapped in `config/config.yaml`:
```yaml
buttons:
  button1: 5   # GPIO pin
  button2: 6
  button3: 13
  button4: 19
```

Register callbacks in `CyfoxApp._setup_callbacks()`:
```python
self.button_handler.register_callback(1, self._on_button1)
```

## Display Rendering

The display is 128x128 pixels. Use `TextRenderer` for text:
```python
text_surf = self.text_renderer.render_text("Hello", size=12, color=(255, 255, 255))
self.display.blit(text_surf, (x, y))
```

## State Management

States are managed through `StateManager`:
```python
# Change state
self.state_manager.state = CyfoxState.EATING

# Register callback
def on_state_change(old_state, new_state):
    print(f"State changed: {old_state} -> {new_state}")

self.state_manager.register_state_callback(on_state_change)
```

## Testing

### Local Testing
```bash
# Without hardware (simulation mode)
python run.py
```

### Hardware Testing
```bash
# On Raspberry Pi
python run.py
```

### Docker Testing
```bash
docker build -t cyfox:test .
docker run --privileged --network host --pid host \
  -v /dev:/dev -v /sys:/sys cyfox:test
```

## Debugging

### Enable Debug Logging
Add logging configuration:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### GPIO Debugging
If buttons don't work:
1. Check GPIO pin mappings
2. Verify RPi.GPIO is installed
3. Check permissions (may need sudo or GPIO group)
4. Test GPIO manually:
   ```python
   import RPi.GPIO as GPIO
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   print(GPIO.input(5))
   ```

### Display Debugging
If display doesn't work:
1. Verify Argon40 Pod drivers installed
2. Check display connection
3. Test with simple pygame script:
   ```python
   import pygame
   pygame.init()
   screen = pygame.display.set_mode((128, 128))
   screen.fill((255, 0, 0))
   pygame.display.flip()
   ```

## Performance Optimization

### Animation
- Use appropriate FPS (idle: 8fps, active: 12fps)
- Cache rendered surfaces
- Limit text rendering

### Network Scanner
- Limit scan range
- Use threading for non-blocking scans
- Cache results

### Reddit Fetcher
- Rate limit API calls
- Cache posts
- Use async requests (future enhancement)

## Best Practices

1. **Thread Safety**: Use locks for shared state
2. **Error Handling**: Wrap external calls in try/except
3. **Resource Cleanup**: Always stop threads and cleanup GPIO
4. **Configuration**: Use config file, not hardcoded values
5. **Modularity**: Keep modules independent
6. **Documentation**: Document public APIs

## Future Enhancements

- [ ] Web interface for remote monitoring
- [ ] Database for scan results
- [ ] More advanced animations (sprite sheets)
- [ ] Voice interactions
- [ ] AI personality integration
- [ ] Plugin system for custom modules
- [ ] Metrics and monitoring

