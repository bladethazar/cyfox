"""Reminder module for eating, drinking, resting, and focusing"""
import threading
import time
from typing import Optional, Callable
from datetime import datetime, timedelta
from src.core.config import Config
from src.core.state import StateManager, CyfoxState


class Reminder:
    """Represents a single reminder"""

    def __init__(self, name: str, interval_minutes: int, message: str):
        self.name = name
        self.interval_minutes = interval_minutes
        self.message = message
        self.last_triggered: Optional[datetime] = None
        self.acknowledged = False

    def should_trigger(self) -> bool:
        """Check if reminder should be triggered"""
        if self.last_triggered is None:
            return True

        elapsed = datetime.now() - self.last_triggered
        return elapsed >= timedelta(minutes=self.interval_minutes)

    def trigger(self):
        """Mark reminder as triggered"""
        self.last_triggered = datetime.now()
        self.acknowledged = False

    def acknowledge(self):
        """Acknowledge the reminder"""
        self.acknowledged = True


class ReminderModule:
    """Manages reminders for eating, drinking, resting, and focusing"""

    def __init__(self, config: Config, state_manager: StateManager):
        self.config = config
        self.state_manager = state_manager
        self.reminders: dict[str, Reminder] = {}
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.callback: Optional[Callable] = None

        self._initialize_reminders()

    def _initialize_reminders(self):
        """Initialize reminders from config"""
        reminder_config = self.config.get('cyfox.reminders', {})

        self.reminders = {
            'eat': Reminder(
                'eat',
                reminder_config.get('eat_interval', 180),
                "🍕 Time to eat! Take a break and fuel up!"
            ),
            'drink': Reminder(
                'drink',
                reminder_config.get('drink_interval', 60),
                "💧 Stay hydrated! Time for a drink!"
            ),
            'rest': Reminder(
                'rest',
                reminder_config.get('rest_interval', 90),
                "😴 Take a rest! Your eyes need a break!"
            ),
            'focus': Reminder(
                'focus',
                reminder_config.get('focus_interval', 25),
                "🎯 Focus time! Let's get things done!"
            ),
        }

    def register_callback(self, callback: Callable):
        """Register callback for when reminders trigger"""
        self.callback = callback

    def acknowledge_reminder(self, reminder_name: Optional[str] = None):
        """Acknowledge a reminder"""
        if reminder_name:
            if reminder_name in self.reminders:
                self.reminders[reminder_name].acknowledge()
        else:
            # Acknowledge all active reminders
            for reminder in self.reminders.values():
                if not reminder.acknowledged and reminder.should_trigger():
                    reminder.acknowledge()

        # Return to idle if in alert state
        if self.state_manager.state == CyfoxState.ALERT:
            self.state_manager.state = CyfoxState.IDLE

    def _check_reminders(self):
        """Check reminders periodically (runs in thread)"""
        while self.running:
            # pylint: disable=too-many-nested-blocks
            active_reminder = None

            for name, reminder in self.reminders.items():
                if reminder.should_trigger() and not reminder.acknowledged:
                    if active_reminder is None:
                        active_reminder = reminder
                        reminder.trigger()

                        # Map reminder to state
                        state_mapping = {
                            'eat': CyfoxState.EATING,
                            'drink': CyfoxState.DRINKING,
                            'rest': CyfoxState.RESTING,
                            'focus': CyfoxState.FOCUSING,
                        }

                        new_state = state_mapping.get(name, CyfoxState.ALERT)
                        self.state_manager.state = new_state

                        # Trigger callback
                        if self.callback:
                            try:
                                self.callback(reminder)
                            except Exception as e:  # pylint: disable=broad-exception-caught
                                print(f"Error in reminder callback: {e}")

            time.sleep(10)  # Check every 10 seconds

    def start(self):
        """Start reminder monitoring"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._check_reminders, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop reminder monitoring"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def get_active_reminder(self) -> Optional[Reminder]:
        """Get currently active reminder"""
        for reminder in self.reminders.values():
            if not reminder.acknowledged and reminder.should_trigger():
                return reminder
        return None

