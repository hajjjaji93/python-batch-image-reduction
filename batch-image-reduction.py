"""
Batch Image Reduction Script
Dependencies: pip install Pillow
"""

import os
import sys
from tkinter import filedialog, Tk
from PIL import Image, ImageOps

# --- CONFIGURATION ---
# Max width in pixels. 1920 is standard HD. Set to None to disable resizing.
MAX_WIDTH = 1920 

# JPEG Quality: 65 is 'web high' (good balance). 85 is 'visually lossless'.
JPEG_QUALITY = 65

# Name of the subfolder where processed images will be saved.
OUTPUT_DIRNAME = 'fixed'

# Supported formats
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')

def compress_images():
    # 1. Initialize hidden window and ask for folder
    root = Tk()
    root.withdraw() # Hide the main window

    print("Please select the folder containing your images...")
    folder_path = filedialog.askdirectory(title="Select Image Folder")
    
    # Destroy the root window immediately after selection to prevent hanging processes.
    root.destroy() 

    if not folder_path:
        print("No folder selected. Exiting.")
        return

    # 2. Setup Output Folder
    output_folder = os.path.join(folder_path, OUTPUT_DIRNAME)
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Processing images in: {folder_path}")
    print(f"Saving to: {output_folder}\n")
    
    count = 0
    saved_space = 0

    # 3. Process Files
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(VALID_EXTENSIONS):
            file_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                with Image.open(file_path) as img:
                    original_size = os.path.getsize(file_path)
                    
                    # Fix orientation (keep vertical photos vertical).
                    img = ImageOps.exif_transpose(img)

                    # Resize Logic.
                    if MAX_WIDTH and img.width > MAX_WIDTH:
                        ratio = MAX_WIDTH / float(img.width)
                        new_height = int((float(img.height) * float(ratio)))
                        img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

                    # Specific conversion based on the file extension to avoid crashes (e.g. RGBA -> JPEG).
                    ext = filename.lower()
                    
                    if ext in ('.jpg', '.jpeg'):
                        # JPEGs do not support transparency (Alpha). Force convert to RGB.
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Save: progressive + quality setting
                        img.save(output_path, "JPEG", optimize=True, quality=JPEG_QUALITY, progressive=True)

                    elif ext == '.png':
                        # PNGs support transparency. Keep RGBA or P mode.
                        # If it's CMYK or something weird, convert to RGBA.
                        if img.mode not in ('RGBA', 'P'):
                            img = img.convert('RGBA')
                            
                        # Save: PNG optimize helps, but is not as drastic as JPEG compression.
                        img.save(output_path, "PNG", optimize=True)

                    else:
                        # Fallback for BMP/TIFF.
                        # We convert to RGB to ensure compatibility, as some TIFFs are CMYK.
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        img.save(output_path, optimize=True)

                    # Stats
                    new_size = os.path.getsize(output_path)
                    saved_space += (original_size - new_size)
                    count += 1
                    
                    percent = ((original_size - new_size) / original_size) * 100
                    print(f"Processed: {filename} | Reduced by {percent:.1f}% ({original_size/1024/1024:.2f}MB -> {new_size/1024/1024:.2f}MB)")

            except Exception as e:
                print(f"Could not process {filename}: {e}")

    # 4. Summary
    print("-" * 30)
    print(f"Complete! Processed {count} images.")
    if count > 0:
        print(f"Total space saved: {saved_space / 1024 / 1024:.2f} MB")
    print(f"Images are located in: {output_folder}")

if __name__ == "__main__":
    # Check for Pillow installation
    try:
        import PIL
        compress_images()
    except ImportError:
        print("Error: The 'Pillow' library is not installed.")
        print("Please run: pip install Pillow")
        input("Press Enter to exit...")