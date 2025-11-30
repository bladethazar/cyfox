"""Display handler for Argon40 Pod Display"""
import pygame
from src.core.config import Config


class Display:
    """Manages the Argon40 Pod Display"""

    def __init__(self, config: Config):
        self.config = config
        self.width = config.get('cyfox.display.width', 128)
        self.height = config.get('cyfox.display.height', 128)
        self.fps = config.get('cyfox.display.fps', 30)

        pygame.init()
        # Set display mode for Argon40 Pod
        # Try fullscreen first (for hardware), fallback to windowed (for development)
        try:
            # For Argon40 Pod hardware display
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        except pygame.error:
            # Fallback for development/testing without hardware display
            self.screen = pygame.display.set_mode((self.width, self.height))
            print("Warning: Running in windowed mode (hardware display not available)")

        pygame.display.set_caption("Cyfox Buddy")
        pygame.mouse.set_visible(False)  # Hide cursor for embedded display
        self.clock = pygame.time.Clock()

    def clear(self, color=(0, 0, 0)):
        """Clear the display with a color"""
        self.screen.fill(color)

    def blit(self, surface, position):
        """Blit a surface to the display"""
        self.screen.blit(surface, position)

    def flip(self):
        """Update the display"""
        pygame.display.flip()

    def tick(self):
        """Tick the clock"""
        return self.clock.tick(self.fps)

    def get_surface(self):
        """Get the display surface"""
        return self.screen

    def quit(self):
        """Clean up pygame"""
        pygame.quit()

