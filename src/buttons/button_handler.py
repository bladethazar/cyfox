"""GPIO button handler for Argon40 Pod Display"""
import threading
import time
from typing import Dict, Callable, Optional
from src.core.config import Config

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("Warning: RPi.GPIO not available. Running in simulation mode.")


class ButtonHandler:
    """Handles GPIO button inputs for Argon40 Pod Display"""
    
    def __init__(self, config: Config):
        self.config = config
        self.gpio_available = GPIO_AVAILABLE
        self.button_callbacks: Dict[int, Callable] = {}
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
        # Get button pin mappings from config
        self.button_pins = {
            1: config.get('cyfox.buttons.button1', 5),
            2: config.get('cyfox.buttons.button2', 6),
            3: config.get('cyfox.buttons.button3', 13),
            4: config.get('cyfox.buttons.button4', 19),
        }
        
        if self.gpio_available:
            self._setup_gpio()
        else:
            print("Running in simulation mode - buttons will not work")
    
    def _setup_gpio(self):
        """Setup GPIO pins for buttons"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        for pin in self.button_pins.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def register_callback(self, button_num: int, callback: Callable):
        """Register a callback for a button press"""
        if button_num in self.button_pins:
            self.button_callbacks[button_num] = callback
        else:
            raise ValueError(f"Invalid button number: {button_num}")
    
    def _check_buttons(self):
        """Check button states (runs in separate thread)"""
        last_state = {pin: True for pin in self.button_pins.values()}
        debounce_time = {pin: 0 for pin in self.button_pins.values()}
        debounce_delay = 50  # milliseconds
        
        while self.running:
            current_time = time.time() * 1000  # milliseconds
            
            for button_num, pin in self.button_pins.items():
                if self.gpio_available:
                    current_state = GPIO.input(pin)
                else:
                    # Simulation mode - buttons always high
                    current_state = True
                
                # Button pressed (LOW) when pulled up
                if not current_state and last_state[pin]:
                    # Button just pressed
                    if current_time - debounce_time[pin] > debounce_delay:
                        debounce_time[pin] = current_time
                        if button_num in self.button_callbacks:
                            try:
                                self.button_callbacks[button_num]()
                            except Exception as e:
                                print(f"Error in button {button_num} callback: {e}")
                
                last_state[pin] = current_state
            
            time.sleep(0.01)  # Check every 10ms
    
    def start(self):
        """Start button monitoring thread"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._check_buttons, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop button monitoring"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        
        if self.gpio_available:
            GPIO.cleanup()

