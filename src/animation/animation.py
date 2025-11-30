"""Animation system for Cyfox sprites"""
import pygame
import os
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum
from cyfox.core.state import CyfoxState
from cyfox.core.config import Config


class AnimationType(Enum):
    """Types of animations"""
    IDLE = "idle"
    EATING = "eating"
    DRINKING = "drinking"
    RESTING = "resting"
    FOCUSING = "focusing"
    SCANNING = "scanning"
    READING = "reading"
    ALERT = "alert"
    BLINK = "blink"
    HAPPY = "happy"
    THINKING = "thinking"


class SpriteSheet:
    """Handles sprite sheet loading and frame extraction"""
    
    def __init__(self, image_path: str, frame_width: int, frame_height: int, 
                 rows: int = 1, cols: int = 1):
        """
        Initialize sprite sheet
        
        Args:
            image_path: Path to sprite sheet image
            frame_width: Width of each frame
            frame_height: Height of each frame
            rows: Number of rows in sprite sheet
            cols: Number of columns in sprite sheet
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.rows = rows
        self.cols = cols
        self.frames: List[pygame.Surface] = []
        self._extract_frames()
    
    def _extract_frames(self):
        """Extract individual frames from sprite sheet"""
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.image.subsurface(
                    pygame.Rect(x, y, self.frame_width, self.frame_height)
                )
                self.frames.append(frame)
    
    def get_frame(self, index: int) -> pygame.Surface:
        """Get a specific frame by index"""
        if 0 <= index < len(self.frames):
            return self.frames[index]
        return self.frames[0] if self.frames else None
    
    def get_frame_count(self) -> int:
        """Get total number of frames"""
        return len(self.frames)


class Animation:
    """Represents a single animation sequence"""
    
    def __init__(self, frames: List[pygame.Surface], fps: int = 8, loop: bool = True):
        """
        Initialize animation
        
        Args:
            frames: List of pygame surfaces (frames)
            fps: Frames per second for this animation
            loop: Whether animation should loop
        """
        self.frames = frames
        self.fps = fps
        self.loop = loop
        self.current_frame = 0
        self.frame_time = 0
        self.frame_duration = 1000 / fps  # milliseconds per frame
        self.playing = False
        self.finished = False
    
    def update(self, dt: int):
        """Update animation (dt in milliseconds)"""
        if not self.playing:
            return
        
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            self.frame_time = 0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    self.playing = False
    
    def get_current_frame(self) -> pygame.Surface:
        """Get current frame"""
        if self.frames and 0 <= self.current_frame < len(self.frames):
            return self.frames[self.current_frame]
        return None
    
    def play(self):
        """Start playing animation"""
        self.playing = True
        self.finished = False
        self.current_frame = 0
        self.frame_time = 0
    
    def stop(self):
        """Stop animation"""
        self.playing = False
    
    def reset(self):
        """Reset animation to beginning"""
        self.current_frame = 0
        self.frame_time = 0
        self.finished = False


class AnimationManager:
    """Manages all animations for Cyfox"""
    
    def __init__(self, config: Config, sprite_path: Optional[str] = None):
        """
        Initialize animation manager
        
        Args:
            config: Configuration object
            sprite_path: Path to sprite image/sheet
        """
        self.config = config
        self.animations: Dict[AnimationType, Animation] = {}
        self.current_animation: Optional[Animation] = None
        self.current_type: AnimationType = AnimationType.IDLE
        
        # Default sprite path
        if sprite_path is None:
            project_root = Path(__file__).parent.parent.parent
            sprite_path = project_root / "frontend" / "assets" / "cyfox.png"
        
        self.sprite_path = Path(sprite_path)
        self._load_animations()
    
    def _load_animations(self):
        """Load all animations from sprite or sprite sheet"""
        if not self.sprite_path.exists():
            print(f"Warning: Sprite not found at {self.sprite_path}")
            # Create a simple placeholder
            self._create_placeholder_animations()
            return
        
        sprite_image = pygame.image.load(str(self.sprite_path)).convert_alpha()
        width, height = sprite_image.get_size()
        
        # Check if this is a sprite sheet or single image
        # Try to detect sprite sheet: if width/height is divisible by common frame sizes
        frame_width = self.config.get('cyfox.animation.frame_width', None)
        frame_height = self.config.get('cyfox.animation.frame_height', None)
        sprite_rows = self.config.get('cyfox.animation.sprite_rows', None)
        sprite_cols = self.config.get('cyfox.animation.sprite_cols', None)
        
        # Auto-detect if not configured
        if frame_width is None or frame_height is None:
            # Try common frame sizes
            for test_size in [128, 64, 32]:
                if width % test_size == 0 and height % test_size == 0:
                    frame_width = test_size
                    frame_height = test_size
                    sprite_cols = width // test_size
                    sprite_rows = height // test_size
                    break
        
        # Fallback to single sprite
        if frame_width is None or frame_height is None:
            frame_width = width
            frame_height = height
            sprite_cols = 1
            sprite_rows = 1
        
        # Create sprite sheet
        sprite_sheet = SpriteSheet(
            str(self.sprite_path),
            frame_width,
            frame_height,
            rows=sprite_rows or 1,
            cols=sprite_cols or 1
        )
        
        # Get FPS settings
        idle_fps = self.config.get('cyfox.animation.idle_fps', 8)
        active_fps = self.config.get('cyfox.animation.active_fps', 12)
        
        # Load animations from sprite sheet
        # If sprite sheet has multiple frames, distribute them across animations
        total_frames = sprite_sheet.get_frame_count()
        
        if total_frames == 1:
            # Single sprite - use for all animations
            base_frame = sprite_sheet.get_frame(0)
            self.animations[AnimationType.IDLE] = Animation([base_frame], fps=idle_fps)
            self.animations[AnimationType.EATING] = Animation([base_frame], fps=active_fps)
            self.animations[AnimationType.DRINKING] = Animation([base_frame], fps=active_fps)
            self.animations[AnimationType.RESTING] = Animation([base_frame], fps=idle_fps)
            self.animations[AnimationType.FOCUSING] = Animation([base_frame], fps=active_fps)
            self.animations[AnimationType.SCANNING] = Animation([base_frame], fps=active_fps)
            self.animations[AnimationType.READING] = Animation([base_frame], fps=idle_fps)
            self.animations[AnimationType.ALERT] = Animation([base_frame], fps=active_fps)
        else:
            # Multiple frames - distribute across animations
            # Default distribution: 3 frames per row, 8 rows
            frames_per_animation = max(1, total_frames // 8)  # Distribute across 8 main animations
            
            anim_types = [
                AnimationType.IDLE,
                AnimationType.EATING,
                AnimationType.DRINKING,
                AnimationType.RESTING,
                AnimationType.FOCUSING,
                AnimationType.SCANNING,
                AnimationType.READING,
                AnimationType.ALERT,
            ]
            
            frame_idx = 0
            for anim_type in anim_types:
                frames = []
                for _ in range(frames_per_animation):
                    if frame_idx < total_frames:
                        frames.append(sprite_sheet.get_frame(frame_idx))
                        frame_idx += 1
                
                if not frames:
                    # Fallback to first frame if no frames assigned
                    frames = [sprite_sheet.get_frame(0)]
                
                # Use appropriate FPS
                fps = idle_fps if anim_type in [AnimationType.IDLE, AnimationType.RESTING, AnimationType.READING] else active_fps
                self.animations[anim_type] = Animation(frames, fps=fps)
        
        # Set default animation
        self.current_animation = self.animations[AnimationType.IDLE]
        self.current_animation.play()
    
    def _create_placeholder_animations(self):
        """Create placeholder animations if sprite is missing"""
        # Create a simple colored rectangle as placeholder
        placeholder = pygame.Surface((64, 64))
        placeholder.fill((100, 150, 255))  # Blue-ish color
        
        idle_fps = self.config.get('cyfox.animation.idle_fps', 8)
        for anim_type in AnimationType:
            self.animations[anim_type] = Animation([placeholder], fps=idle_fps)
        
        self.current_animation = self.animations[AnimationType.IDLE]
        self.current_animation.play()
    
    def set_animation(self, anim_type: AnimationType):
        """Switch to a different animation"""
        if anim_type in self.animations:
            if self.current_animation:
                self.current_animation.stop()
            self.current_animation = self.animations[anim_type]
            self.current_type = anim_type
            self.current_animation.play()
    
    def update(self, dt: int):
        """Update current animation"""
        if self.current_animation:
            self.current_animation.update(dt)
    
    def get_current_frame(self) -> Optional[pygame.Surface]:
        """Get current animation frame"""
        if self.current_animation:
            return self.current_animation.get_current_frame()
        return None
    
    def map_state_to_animation(self, state: CyfoxState) -> AnimationType:
        """Map CyfoxState to AnimationType"""
        mapping = {
            CyfoxState.IDLE: AnimationType.IDLE,
            CyfoxState.EATING: AnimationType.EATING,
            CyfoxState.DRINKING: AnimationType.DRINKING,
            CyfoxState.RESTING: AnimationType.RESTING,
            CyfoxState.FOCUSING: AnimationType.FOCUSING,
            CyfoxState.SCANNING: AnimationType.SCANNING,
            CyfoxState.READING: AnimationType.READING,
            CyfoxState.ALERT: AnimationType.ALERT,
        }
        return mapping.get(state, AnimationType.IDLE)

