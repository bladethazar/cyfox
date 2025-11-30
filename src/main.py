"""Main application entry point for Cyfox"""
import sys
import signal
import traceback
# pylint: disable=import-error
import pygame
from src.core.config import Config
from src.core.state import StateManager, CyfoxState, CyfoxMode
from src.display.display import Display
from src.display.text_renderer import TextRenderer
from src.animation.animation import AnimationManager
from src.buttons.button_handler import ButtonHandler
from src.modules.reminder import ReminderModule
from src.modules.scanner import NetworkScanner
from src.modules.reddit import RedditFetcher


class CyfoxApp:
    """Main application class for Cyfox"""
    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        # Initialize configuration
        self.config = Config()

        # Initialize core components
        self.state_manager = StateManager()
        self.display = Display(self.config)
        self.text_renderer = TextRenderer(self.display.width, self.display.height)
        self.animation_manager = AnimationManager(self.config)
        self.button_handler = ButtonHandler(self.config)

        # Initialize modules
        self.reminder_module = ReminderModule(self.config, self.state_manager)
        self.scanner_module = NetworkScanner(self.config, self.state_manager)
        self.reddit_module = RedditFetcher(self.config, self.state_manager)

        # Setup callbacks
        self._setup_callbacks()

        # Running flag
        self.running = False

    def _setup_callbacks(self):
        """Setup callbacks between components"""

        # State change callback - update animation
        def on_state_change(old_state, new_state):
            # pylint: disable=unused-argument
            anim_type = self.animation_manager.map_state_to_animation(new_state)
            self.animation_manager.set_animation(anim_type)

        self.state_manager.register_state_callback(on_state_change)

        # Reminder callback
        def on_reminder(reminder):
            print(f"Reminder: {reminder.message}")
            # Animation already updated via state change

        self.reminder_module.register_callback(on_reminder)

        # Scanner callback
        def on_scan_complete(results):
            print(f"Scan complete: Found {len(results)} hosts with open ports")
            for result in results:
                print(f"  {result.host}: {result.ports}")

        self.scanner_module.register_callback(on_scan_complete)

        # Reddit callback
        def on_reddit_posts(posts):
            print(f"Fetched {len(posts)} Reddit posts")

        self.reddit_module.register_callback(on_reddit_posts)

        # Button callbacks
        self.button_handler.register_callback(1, self._on_button1)  # Acknowledge
        self.button_handler.register_callback(2, self._on_button2)  # Next Reddit
        self.button_handler.register_callback(3, self._on_button3)  # Start scan
        self.button_handler.register_callback(4, self._on_button4)  # Cycle mode

    def _on_button1(self):
        """Button 1: Acknowledge reminder"""
        if self.state_manager.state == CyfoxState.ALERT:
            self.reminder_module.acknowledge_reminder()
        elif self.state_manager.mode == CyfoxMode.BUDDY:
            # Acknowledge any active reminder
            self.reminder_module.acknowledge_reminder()

    def _on_button2(self):
        """Button 2: Next Reddit post"""
        if self.state_manager.mode == CyfoxMode.REDDIT:
            self.reddit_module.next_post()
            self.state_manager.state = CyfoxState.READING

    def _on_button3(self):
        """Button 3: Start network scan"""
        if self.state_manager.mode == CyfoxMode.SCANNER:
            self.scanner_module.scan_network()

    def _on_button4(self):
        """Button 4: Cycle mode"""
        self.state_manager.cycle_mode()
        # Update state based on mode
        if self.state_manager.mode == CyfoxMode.REDDIT:
            self.state_manager.state = CyfoxState.READING
        elif self.state_manager.mode == CyfoxMode.SCANNER:
            self.state_manager.state = CyfoxState.IDLE
        else:
            self.state_manager.state = CyfoxState.IDLE

    def _render_text(self, text: str, position: tuple, color=(255, 255, 255),
                    max_width: int = None, size: int = 10):
        """Render text on display"""
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        if not text:
            return
        text_surface = self.text_renderer.render_text(
            text, size=size, color=color, max_width=max_width)
        self.display.blit(text_surface, position)

    def _render_ui(self):
        """Render UI elements based on current state and mode"""
        # pylint: disable=too-many-locals
        self.display.clear()

        # Get current animation frame
        frame = self.animation_manager.get_current_frame()
        if frame:
            # Center the frame
            frame_x = (self.display.width - frame.get_width()) // 2
            frame_y = (self.display.height - frame.get_height()) // 2
            self.display.blit(frame, (frame_x, frame_y))

        # Render mode indicator (top corner)
        mode_text = self.state_manager.mode.value[:3].upper()
        mode_surface = self.text_renderer.render_text(mode_text, size=8, color=(100, 100, 100))
        self.display.blit(mode_surface, (2, 2))

        # Render state-specific UI
        if self.state_manager.state == CyfoxState.ALERT:
            active_reminder = self.reminder_module.get_active_reminder()
            if active_reminder:
                # Render reminder icon/indicator (simplified - just show state)
                icon_map = {
                    'eat': '🍕',
                    'drink': '💧',
                    'rest': '😴',
                    'focus': '🎯'
                }
                icon = icon_map.get(active_reminder.name, '!')
                icon_surf = self.text_renderer.render_text(icon, size=12)
                self.display.blit(icon_surf, (self.display.width - 20, 2))

        elif self.state_manager.mode == CyfoxMode.REDDIT:
            post = self.reddit_module.get_current_post()
            if post:
                # Render post title (truncated for small display)
                title = post.title[:20] + "..." if len(post.title) > 20 else post.title
                title_surf = self.text_renderer.render_text(
                    title, size=8, max_width=self.display.width - 4)
                self.display.blit(title_surf, (2, self.display.height - 20))

        elif self.state_manager.mode == CyfoxMode.SCANNER:
            if self.state_manager.state == CyfoxState.SCANNING:
                # Render scanning indicator
                scan_text = self.text_renderer.render_text("SCAN...", size=8, color=(255, 255, 0))
                self.display.blit(scan_text, (2, self.display.height - 12))
            else:
                results = self.scanner_module.get_results()
                if results:
                    # Render scan results summary
                    result_text = f"{len(results)} hosts"
                    result_surf = self.text_renderer.render_text(
                        result_text, size=8, color=(0, 255, 0))
                    self.display.blit(result_surf, (2, self.display.height - 12))

    def run(self):
        """Main application loop"""
        self.running = True

        # Start all modules
        self.reminder_module.start()
        self.scanner_module.start()
        self.reddit_module.start()
        self.button_handler.start()

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        print("Cyfox is running! Press Ctrl+C to stop.")

        # Main loop
        while self.running:
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Calculate delta time
            dt = self.display.tick()

            # Update animation
            self.animation_manager.update(dt)

            # Render
            self._render_ui()
            self.display.flip()

        # Cleanup
        self.shutdown()

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        # pylint: disable=unused-argument
        print("\nShutting down Cyfox...")
        self.running = False

    def shutdown(self):
        """Cleanup and shutdown"""
        print("Stopping modules...")
        self.reminder_module.stop()
        self.scanner_module.stop()
        self.reddit_module.stop()
        self.button_handler.stop()
        self.display.quit()
        print("Cyfox stopped.")


def main():
    """Entry point"""
    app = CyfoxApp()
    try:
        app.run()
    except KeyboardInterrupt:
        app.shutdown()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")
        traceback.print_exc()
        app.shutdown()
        sys.exit(1)


if __name__ == "__main__":
    main()
