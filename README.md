# Batch Image Reducer

A robust Python script to bulk compress and resize images within a directory. 

This tool is designed to drastically reduce file sizes (often by 90%+) by resizing images to HD standards and applying aggressive web-optimization, without overwriting your original files.

## Features

* **Smart Resizing:** Automatically detects images wider than **1920px** and resizes them (maintaining aspect ratio).
* **Crash-Proof Conversion:** Intelligently handles color modes (automatically converting transparent images to RGB if saving as JPEG) to prevent errors.
* **Non-Destructive:** Creates a subfolder named `fixed` containing the processed images. Your originals are untouched.
* **Auto-Rotation:** Detects vertical photos (via EXIF data) and ensures they remain vertical.
* **Web Optimization:**
    * **JPEGs:** Compressed to Quality 65 (Web High) with progressive loading.
    * **PNGs:** Optimized specifically to preserve transparency where needed.
    * **Metadata:** Strips EXIF/Camera data to save space.

## Prerequisites

* **Python 3.x**
* **Pillow Library**

## Installation

1.  Clone this repository or download `batch_image_reduction.py`.
2.  Install the required image library:

```bash
pip install Pillow
```

## Usage

* **Run the Script:**

```bash
python batch_image_reduction.py
```

* **A Window Will Pop-Up:** Select the folder containing your images.

* **Script Runs:** The script will process the images and save the optimized versions in a new folder named 'fixed' inside your selected directory.

## Configuration

You can easily adjust the settings at the top of the script file:

* **MAX_WIDTH = 1920:** The maximum width in pixels. Images wider than this will be resized. Set to None to keep original resolution.
* **JPEG_QUALITY = 65:** The compression level for JPEGs (1-100). Lower is smaller but lower quality.
* **OUTPUT_DIRNAME = 'fixed':** The name of the output folder.

## Limitations

* **Recursion:** The script only processes the files in the folder you select. It does not look into sub-folders.
* **PNG Compression:** While the script optimizes PNG structure, it does not convert PNGs to JPEGs (to preserve file names and transparency). If you have massive non-transparent PNGs (like photos saved as PNG), they may not reduce in size significantly.
* **TIFF/BMP:** These formats are processed for compatibility, but file size savings are minimal unless converted to JPEG (which this script avoids to preserve file extensions).

### License

Free, open-source. MIT licensed.
