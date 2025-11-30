"""State management for Cyfox"""
from enum import Enum
from typing import Callable
import threading


class CyfoxState(Enum):
    """Main states for Cyfox"""
    IDLE = "idle"
    EATING = "eating"
    DRINKING = "drinking"
    RESTING = "resting"
    FOCUSING = "focusing"
    SCANNING = "scanning"
    READING = "reading"  # Reading Reddit posts
    ALERT = "alert"      # Showing reminder/alert


class CyfoxMode(Enum):
    """Operating modes"""
    BUDDY = "buddy"           # Reminder mode
    SCANNER = "scanner"       # Network scanning mode
    REDDIT = "reddit"         # Reddit browsing mode


class StateManager:
    """Manages Cyfox's state and mode"""

    def __init__(self):
        self._state = CyfoxState.IDLE
        self._mode = CyfoxMode.BUDDY
        self._lock = threading.Lock()
        self._state_callbacks: list[Callable] = []
        self._mode_callbacks: list[Callable] = []

    @property
    def state(self) -> CyfoxState:
        """Get current state"""
        with self._lock:
            return self._state

    @state.setter
    def state(self, new_state: CyfoxState):
        """Set new state and notify callbacks"""
        with self._lock:
            old_state = self._state
            self._state = new_state
            for callback in self._state_callbacks:
                try:
                    callback(old_state, new_state)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"Error in state callback: {e}")

    @property
    def mode(self) -> CyfoxMode:
        """Get current mode"""
        with self._lock:
            return self._mode

    @mode.setter
    def mode(self, new_mode: CyfoxMode):
        """Set new mode and notify callbacks"""
        with self._lock:
            old_mode = self._mode
            self._mode = new_mode
            for callback in self._mode_callbacks:
                try:
                    callback(old_mode, new_mode)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"Error in mode callback: {e}")

    def register_state_callback(self, callback: Callable):
        """Register a callback for state changes"""
        self._state_callbacks.append(callback)

    def register_mode_callback(self, callback: Callable):
        """Register a callback for mode changes"""
        self._mode_callbacks.append(callback)

    def cycle_mode(self):
        """Cycle through available modes"""
        modes = list(CyfoxMode)
        current_index = modes.index(self.mode)
        next_index = (current_index + 1) % len(modes)
        self.mode = modes[next_index]

