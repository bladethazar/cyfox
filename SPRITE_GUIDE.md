# Sprite Creation Guide for Cyfox

This guide explains how to create sprite sheets from your `cyfox.png` for smooth animations.

## Understanding Sprite Sheets

A sprite sheet is a single image containing multiple frames of animation arranged in a grid. Cyfox supports sprite sheets with multiple rows and columns.

### Example Layout

```
[Frame 1] [Frame 2] [Frame 3]  <- Row 1: Idle animation (3 frames)
[Frame 4] [Frame 5] [Frame 6]  <- Row 2: Eating animation (3 frames)
[Frame 7] [Frame 8] [Frame 9]  <- Row 3: Drinking animation (3 frames)
```

## Creating Sprites from Your PNG

### Option 1: Using Image Editing Software

#### GIMP (Free)
1. Open your `cyfox.png`
2. **Create sprite sheet**:
   - Image → Canvas Size
   - Set width: `128 * number_of_frames` (e.g., 384 for 3 frames)
   - Set height: `128 * number_of_rows` (e.g., 256 for 2 rows)
3. **Duplicate and modify frames**:
   - Copy your original sprite
   - Paste into new positions
   - Modify each frame slightly (eyes blinking, mouth moving, etc.)
4. **Export as PNG**: File → Export As → `cyfox_sprites.png`

#### Photoshop
1. Open `cyfox.png`
2. Create new document: `128 * frames` × `128 * rows`
3. Copy and paste frames
4. Modify each frame
5. Export as PNG

#### Aseprite (Recommended for pixel art)
1. Open `cyfox.png`
2. Create new sprite: `128 × 128` (single frame)
3. Import your PNG as first frame
4. Duplicate frames and animate
5. Export as sprite sheet: File → Export Sprite Sheet
6. Choose layout: Horizontal/Vertical/Grid

### Option 2: Using Online Tools

- **Piskel** (https://www.piskelapp.com/): Free online sprite editor
- **Lospec Sprite Editor** (https://lospec.com/pixel-editor): Simple pixel editor
- **Sprite Sheet Packer**: Combine individual frames into sheets

### Option 3: Programmatic Creation (Python)

Create `scripts/create_sprites.py`:

```python
from PIL import Image
import os

def create_sprite_sheet(base_image_path, output_path, frames_per_row=3, rows=2):
    """Create a sprite sheet from base image"""
    base_img = Image.open(base_image_path)
    width, height = base_img.size
    
    # Create sprite sheet
    sheet_width = width * frames_per_row
    sheet_height = height * rows
    sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
    
    # Place base image in first position
    sheet.paste(base_img, (0, 0))
    
    # For now, duplicate base image (you can modify each frame)
    for row in range(rows):
        for col in range(frames_per_row):
            if row == 0 and col == 0:
                continue  # Already placed
            x = col * width
            y = row * height
            # You can modify the image here before pasting
            modified = base_img.copy()
            # Example: Add slight variations
            sheet.paste(modified, (x, y))
    
    sheet.save(output_path)
    print(f"Sprite sheet created: {output_path}")

if __name__ == "__main__":
    create_sprite_sheet(
        "frontend/assets/cyfox.png",
        "frontend/assets/cyfox_sprites.png",
        frames_per_row=3,
        rows=3
    )
```

## Recommended Sprite Sheet Layout

For Cyfox, here's a recommended layout:

```
Row 1: Idle Animation (3-4 frames)
  - Frame 1: Normal pose
  - Frame 2: Slight movement/blink
  - Frame 3: Return to normal
  - Frame 4: (Optional) Blink

Row 2: Eating Animation (2-3 frames)
  - Frame 1: Normal
  - Frame 2: Mouth open/eating
  - Frame 3: Chewing

Row 3: Drinking Animation (2 frames)
  - Frame 1: Normal
  - Frame 2: Drinking

Row 4: Resting/Sleeping (2-3 frames)
  - Frame 1: Eyes open
  - Frame 2: Eyes half-closed
  - Frame 3: Eyes closed

Row 5: Focusing/Working (2 frames)
  - Frame 1: Normal
  - Frame 2: Focused expression

Row 6: Scanning (2-3 frames)
  - Frame 1: Normal
  - Frame 2: Scanning pose
  - Frame 3: Scanning pose 2

Row 7: Reading (2 frames)
  - Frame 1: Normal
  - Frame 2: Reading pose

Row 8: Alert (2 frames)
  - Frame 1: Normal
  - Frame 2: Alert expression
```

## Frame Size Guidelines

- **Display Size**: 128×128 pixels
- **Frame Size**: Should match display or be smaller (will be centered)
- **Consistency**: Keep all frames the same size
- **Transparency**: Use PNG with alpha channel for transparency

## Animation Tips

1. **Start Simple**: Begin with 2-3 frames per animation
2. **Smooth Transitions**: Make small changes between frames
3. **Timing**: 
   - Idle: Slow (8 fps) - 2-3 frames
   - Active: Medium (12 fps) - 2-4 frames
   - Alert: Fast (12 fps) - 2 frames
4. **Common Animations**:
   - **Blink**: Add 1 frame with eyes closed
   - **Breathing**: Slight size variation
   - **Mouth**: Open/close for eating/drinking

## Updating Cyfox to Use Sprite Sheets

Once you have your sprite sheet, update `cyfox/animation/animation.py`:

```python
def _load_animations(self):
    """Load all animations from sprite sheet"""
    if not self.sprite_path.exists():
        # ... existing code ...
        return
    
    # Load sprite sheet
    sprite_sheet = SpriteSheet(
        str(self.sprite_path),
        frame_width=128,   # Width of each frame
        frame_height=128,   # Height of each frame
        rows=8,            # Number of rows in your sheet
        cols=3             # Number of columns in your sheet
    )
    
    # Define frame ranges for each animation
    # Assuming 3 frames per row, 8 rows
    self.animations[AnimationType.IDLE] = Animation(
        [sprite_sheet.get_frame(i) for i in range(0, 3)],  # Row 1: frames 0-2
        fps=idle_fps
    )
    
    self.animations[AnimationType.EATING] = Animation(
        [sprite_sheet.get_frame(i) for i in range(3, 6)],  # Row 2: frames 3-5
        fps=active_fps
    )
    
    # ... continue for other animations ...
```

## Quick Start: Simple Blink Animation

1. **Create 2-frame sprite sheet**:
   - Frame 1: Your original `cyfox.png`
   - Frame 2: Same image with eyes closed (edit in GIMP/Photoshop)

2. **Layout**: Horizontal (256×128) or Vertical (128×256)

3. **Update code**:
   ```python
   sprite_sheet = SpriteSheet("cyfox_sprites.png", 128, 128, rows=1, cols=2)
   idle_frames = [sprite_sheet.get_frame(0), sprite_sheet.get_frame(1)]
   self.animations[AnimationType.IDLE] = Animation(idle_frames, fps=2)  # Slow blink
   ```

## Testing Your Sprites

1. Place sprite sheet in `frontend/assets/cyfox_sprites.png`
2. Update `AnimationManager` to load from sprite sheet
3. Run: `python run.py`
4. Watch the animation play

## Tools Reference

- **Aseprite**: https://www.aseprite.org/ (Paid, best for pixel art)
- **GIMP**: https://www.gimp.org/ (Free, powerful)
- **Piskel**: https://www.piskelapp.com/ (Free, online)
- **Photoshop**: Industry standard (Paid)

## Example: Creating a Simple Blink

Using GIMP:
1. Open `cyfox.png`
2. Duplicate layer
3. On duplicate: Use eraser/paintbrush to close eyes
4. Export both frames
5. Use ImageMagick to combine:
   ```bash
   montage frame1.png frame2.png -tile 2x1 -geometry 128x128 cyfox_blink.png
   ```

## Next Steps

1. Start with a simple 2-frame blink animation
2. Test it works
3. Gradually add more frames and animations
4. Experiment with timing and FPS
5. Create more complex animations as needed

Remember: You can always start with your single PNG and add animations incrementally!

