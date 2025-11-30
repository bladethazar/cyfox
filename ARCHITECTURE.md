# Cyfox Architecture

## Overview

Cyfox is built with a modular, maintainable architecture designed for the Raspberry Pi Zero 2W with Argon40 Pod Display. The system is containerized and deployable to k3s clusters.

## Core Components

### 1. Core Module (`cyfox/core/`)

**State Management** (`state.py`):
- Manages application state (idle, eating, drinking, etc.)
- Manages operating modes (Buddy, Scanner, Reddit)
- Provides callbacks for state/mode changes
- Thread-safe state updates

**Configuration** (`config.py`):
- YAML-based configuration
- Dot notation access (e.g., `config.get('display.width')`)
- Runtime configuration updates
- Default value support

### 2. Display Module (`cyfox/display/`)

**Display Handler** (`display.py`):
- Manages pygame display initialization
- Handles display updates and rendering
- Optimized for 128x128 Argon40 Pod Display
- Fullscreen mode for hardware display

**Text Renderer** (`text_renderer.py`):
- Multi-line text rendering
- Text wrapping support
- Multiple font sizes
- Efficient surface caching

### 3. Animation Module (`cyfox/animation/`)

**Animation System** (`animation.py`):
- Sprite sheet support
- Frame-based animations
- State-to-animation mapping
- Configurable FPS per animation
- Smooth transitions

**Features**:
- Supports single sprite and sprite sheets
- Automatic frame extraction
- Animation looping
- State-based animation switching

### 4. Button Handler (`cyfox/buttons/`)

**GPIO Button Handler** (`button_handler.py`):
- Debounced button input
- Thread-safe callback system
- Simulation mode for development
- Configurable GPIO pins

**Button Mappings**:
- Button 1: Acknowledge reminder
- Button 2: Next Reddit post
- Button 3: Start network scan
- Button 4: Cycle modes

### 5. Functional Modules (`cyfox/modules/`)

#### Reminder Module (`reminder.py`)
- Configurable reminder intervals
- Eating, drinking, resting, focusing reminders
- Acknowledgment system
- State integration

#### Network Scanner (`scanner.py`)
- Bjorn-inspired network scanning
- Port scanning
- Service identification
- Basic vulnerability detection
- Configurable scan intervals

#### Reddit Fetcher (`reddit.py`)
- Multi-subreddit support
- IT/DevOps content filtering
- Post caching
- Navigation support

## Data Flow

```
User Input (Buttons)
    ↓
Button Handler → State Manager
    ↓
State Manager → Animation Manager
    ↓
Animation Manager → Display
    ↓
Display → Hardware (Argon40 Pod)
```

## Module Communication

Modules communicate through:
1. **State Manager**: Central state coordination
2. **Callbacks**: Event-driven communication
3. **Configuration**: Shared configuration access

## Threading Model

- **Main Thread**: Display rendering, event loop
- **Reminder Thread**: Periodic reminder checks
- **Scanner Thread**: Network scanning (when active)
- **Reddit Thread**: Periodic post fetching
- **Button Thread**: GPIO button monitoring

All threads are daemon threads, ensuring clean shutdown.

## State Machine

```
IDLE ←→ EATING
  ↑       ↓
  |    DRINKING
  |       ↓
  |    RESTING
  |       ↓
  |    FOCUSING
  |       ↓
  └──→ SCANNING (Scanner Mode)
  └──→ READING (Reddit Mode)
  └──→ ALERT (Reminder triggered)
```

## Mode Switching

```
Buddy Mode (Default)
    ↓ Button 4
Scanner Mode
    ↓ Button 4
Reddit Mode
    ↓ Button 4
Buddy Mode (loop)
```

## Configuration Structure

```yaml
cyfox:
  display:        # Display settings
  animation:      # Animation settings
  reminders:      # Reminder intervals
  scanner:       # Network scanner config
  reddit:        # Reddit fetcher config
  buttons:       # GPIO pin mappings
```

## Extension Points

### Adding New States
1. Add to `CyfoxState` enum
2. Map to `AnimationType` in `AnimationManager`
3. Add state handling in `main.py`

### Adding New Modules
1. Create module in `cyfox/modules/`
2. Register in `CyfoxApp.__init__()`
3. Start/stop in `run()`/`shutdown()`
4. Add configuration section

### Adding New Animations
1. Create sprite sheet
2. Update `AnimationManager._load_animations()`
3. Add to `AnimationType` enum
4. Map to state in `map_state_to_animation()`

## Performance Considerations

- **Display**: 30 FPS cap for smooth rendering
- **Animations**: Lower FPS for idle (8fps), higher for active (12fps)
- **Network**: Rate-limited API calls
- **GPIO**: 10ms polling interval for buttons
- **Memory**: Cached surfaces, limited history

## Security Considerations

- Non-root user in Docker
- Network scanner requires proper authorization
- Reddit API uses User-Agent identification
- GPIO access requires privileged container

## Deployment Architecture

```
k3s Cluster
    ↓
Namespace: cyfoxlab
    ↓
Deployment: cyfox
    ↓
Container (privileged, hostNetwork)
    ↓
Hardware Access (GPIO, Display)
```

## Future Enhancements

- Web interface for remote monitoring
- Database for scan results
- Plugin system for custom modules
- AI personality integration
- Advanced sprite animations
- Voice interactions

