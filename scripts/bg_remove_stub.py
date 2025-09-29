#!/usr/bin/env python3
"""
Background Removal Pipeline Stub
Compatible with rembg for transparent backgrounds in avatar compositing
"""

import os
import shutil
import sys
from pathlib import Path


def remove_background(input_path, output_path, method='rembg'):
    """
    Remove background from image for avatar compositing
    
    Args:
        input_path: Path to input image
        output_path: Path to output image with transparent background
        method: Background removal method ('rembg', 'copy', 'stub')
    """
    
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"🖼️  Processing: {input_path.name}")
    print(f"📤 Output: {output_path}")
    
    if method == 'rembg':
        try:
            # Try to use rembg if available
            from rembg import new_session, remove

            # Load image
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()
            
            # Remove background
            session = new_session('u2net')  # Universal model
            output_data = remove(input_data, session=session)
            
            # Save result
            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
            
            print("✅ Background removed using rembg")
            return True
            
        except ImportError:
            print("⚠️  rembg not installed, falling back to copy method")
            method = 'copy'
        except Exception as e:
            print(f"❌ rembg error: {e}")
            method = 'copy'
    
    if method == 'copy':
        # Simple copy (for testing when rembg not available)
        shutil.copy2(input_path, output_path)
        print("📋 Copied image (rembg not available)")
        return True
    
    if method == 'stub':
        # Create a stub file for testing
        with open(output_path, 'w') as f:
            f.write(f"# Background removal stub for {input_path.name}\n")
            f.write(f"# Install rembg: pip install rembg\n")
            f.write(f"# Then re-run with method='rembg'\n")
        print("📝 Created stub file")
        return True
    
    return False

def batch_remove_backgrounds(input_dir, output_dir, method='rembg'):
    """
    Batch process multiple images for background removal
    """
    
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    # Supported image formats
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'}
    
    # Find all images
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_dir.glob(f'*{ext}'))
        image_files.extend(input_dir.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print(f"❌ No images found in {input_dir}")
        return False
    
    print(f"🖼️  Found {len(image_files)} images to process")
    
    success_count = 0
    for image_file in image_files:
        output_file = output_dir / f"{image_file.stem}_nobg{image_file.suffix}"
        
        if remove_background(image_file, output_file, method):
            success_count += 1
    
    print(f"✅ Processed {success_count}/{len(image_files)} images")
    return success_count > 0

def main():
    """Command line interface"""
    
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 bg_remove_stub.py <input> <output> [method]")
        print("  python3 bg_remove_stub.py batch <input_dir> <output_dir> [method]")
        print("")
        print("Methods:")
        print("  rembg  - Use rembg library (install: pip install rembg)")
        print("  copy   - Simple copy (fallback)")
        print("  stub   - Create stub file")
        print("")
        print("Examples:")
        print("  python3 bg_remove_stub.py avatar.png avatar_nobg.png")
        print("  python3 bg_remove_stub.py batch ./avatars ./processed")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'batch':
        if len(sys.argv) < 4:
            print("❌ Batch mode requires input and output directories")
            sys.exit(1)
        
        input_dir = sys.argv[2]
        output_dir = sys.argv[3]
        method = sys.argv[4] if len(sys.argv) > 4 else 'rembg'
        
        batch_remove_backgrounds(input_dir, output_dir, method)
    
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        method = sys.argv[3] if len(sys.argv) > 3 else 'rembg'
        
        remove_background(input_path, output_path, method)

if __name__ == '__main__':
    main()
