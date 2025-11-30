#!/usr/bin/env python3
"""Helper script to create sprite sheets from base image"""
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is required for this script.")
    print("Install it with: pip install Pillow")
    print("Or install all requirements: pip install -r requirements.txt")
    sys.exit(1)


def create_simple_sprite_sheet(base_image_path: str, output_path: str, 
                               frames_per_row: int = 3, rows: int = 2):
    """
    Create a sprite sheet by duplicating the base image.
    You can then edit individual frames in an image editor.
    
    Args:
        base_image_path: Path to base cyfox.png
        output_path: Where to save sprite sheet
        frames_per_row: Number of frames per row
        rows: Number of rows
    """
    base_img = Image.open(base_image_path)
    width, height = base_img.size
    
    # Create sprite sheet
    sheet_width = width * frames_per_row
    sheet_height = height * rows
    sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
    
    # Place base image in all positions (you'll edit these later)
    for row in range(rows):
        for col in range(frames_per_row):
            x = col * width
            y = row * height
            sheet.paste(base_img, (x, y))
    
    sheet.save(output_path)
    print(f"✓ Sprite sheet created: {output_path}")
    print(f"  Size: {sheet_width}×{sheet_height}")
    print(f"  Frames: {frames_per_row}×{rows} = {frames_per_row * rows}")
    print(f"  Frame size: {width}×{height}")
    print(f"\nNext steps:")
    print(f"  1. Open {output_path} in GIMP/Photoshop/Aseprite")
    print(f"  2. Edit each frame to create animations")
    print(f"  3. Update AnimationManager to use sprite sheet")


def add_frame_labels(image_path: str, output_path: str, 
                    frames_per_row: int, rows: int):
    """Add frame numbers to sprite sheet for easier editing"""
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    frame_width = img.width // frames_per_row
    frame_height = img.height // rows
    
    for row in range(rows):
        for col in range(frames_per_row):
            x = col * frame_width + 5
            y = row * frame_height + 5
            frame_num = row * frames_per_row + col
            draw.text((x, y), str(frame_num), fill=(255, 255, 255), font=font)
    
    img.save(output_path)
    print(f"✓ Labeled sprite sheet: {output_path}")


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    base_image = project_root / "res" / "cyfox.png"
    output = project_root / "res" / "cyfox_sprites.png"
    
    if not base_image.exists():
        print(f"Error: Base image not found at {base_image}")
        sys.exit(1)
    
    # Create sprite sheet (3 frames per row, 8 rows for all animations)
    create_simple_sprite_sheet(str(base_image), str(output), frames_per_row=3, rows=8)
    
    # Create labeled version
    labeled_output = project_root / "res" / "cyfox_sprites_labeled.png"
    add_frame_labels(str(output), str(labeled_output), frames_per_row=3, rows=8)
    
    print(f"\n✓ Done! Edit {output} to create your animations")

