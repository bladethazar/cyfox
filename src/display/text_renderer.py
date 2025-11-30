"""Text rendering for display"""
from typing import Optional, Tuple
import pygame


class TextRenderer:
    """Handles text rendering on the display"""

    def __init__(self, display_width: int, display_height: int):
        self.display_width = display_width
        self.display_height = display_height
        self.fonts: dict[int, pygame.font.Font] = {}
        self._init_fonts()

    def _init_fonts(self):
        """Initialize fonts"""
        # Try to load system fonts, fallback to default
        try:
            # Try different font sizes
            for size in [8, 10, 12, 14, 16]:
                try:
                    font = pygame.font.Font(None, size)
                    self.fonts[size] = font
                except pygame.error:
                    pass
        except (pygame.error, OSError):
            # Fallback to default font
            try:
                default_font = pygame.font.Font(None, 12)
                self.fonts[12] = default_font
            except pygame.error:
                pass

    def render_text(self, text: str, size: int = 12, color: Tuple[int, int, int] = (255, 255, 255),
                    max_width: Optional[int] = None) -> pygame.Surface:
        """
        Render text to a surface

        Args:
            text: Text to render
            size: Font size
            color: RGB color tuple
            max_width: Maximum width for text wrapping (None = no wrapping)

        Returns:
            pygame.Surface with rendered text
        """
        font = self.fonts.get(size, self.fonts.get(12))
        if not font:
            return pygame.Surface((1, 1), pygame.SRCALPHA)

        if max_width:
            # Word wrap text
            words = text.split(' ')
            lines = []
            current_line = []

            for word in words:
                test_line = ' '.join(current_line + [word])
                width, _ = font.size(test_line)

                if width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]

            if current_line:
                lines.append(' '.join(current_line))

            # Render each line
            rendered_lines = [font.render(line, True, color) for line in lines]

            # Combine lines into single surface
            if rendered_lines:
                line_height = rendered_lines[0].get_height()
                total_height = len(rendered_lines) * line_height
                max_width_surf = max(line.get_width() for line in rendered_lines)

                surface = pygame.Surface((max_width_surf, total_height), pygame.SRCALPHA)
                y = 0
                for line_surf in rendered_lines:
                    surface.blit(line_surf, (0, y))
                    y += line_height

                return surface
            return pygame.Surface((1, 1), pygame.SRCALPHA)

        return font.render(text, True, color)

    def render_multiline(self, lines: list[str], size: int = 12,
                         color: Tuple[int, int, int] = (255, 255, 255),
                         spacing: int = 2) -> pygame.Surface:
        """
        Render multiple lines of text

        Args:
            lines: List of text lines
            size: Font size
            color: RGB color tuple
            spacing: Space between lines

        Returns:
            pygame.Surface with all lines rendered
        """
        font = self.fonts.get(size, self.fonts.get(12))
        if not font:
            return pygame.Surface((1, 1), pygame.SRCALPHA)

        rendered_lines = [font.render(line, True, color) for line in lines if line]

        if not rendered_lines:
            return pygame.Surface((1, 1), pygame.SRCALPHA)

        max_width = max(line.get_width() for line in rendered_lines)
        total_height = sum(line.get_height() for line in rendered_lines) + spacing * (len(rendered_lines) - 1)

        surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
        y = 0
        for line_surf in rendered_lines:
            surface.blit(line_surf, (0, y))
            y += line_surf.get_height() + spacing

        return surface

