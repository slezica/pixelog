import sys
import os
from pathlib import Path
from collections import Counter

from PIL import Image
from colorspacious import cspace_convert


def main():
    try:
        # Load image:
        image_path = parse_args()
        img = load_image(image_path)

        # Extract and count pixels of colors:
        color_counts = extract_colors(img)
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)

        # Calculate total pixels
        total_pixels = sum(color_counts.values())

        for (r, g, b), count in sorted_colors:
            print(format_color_line(r, g, b, count, total_pixels))

    except (BrokenPipeError, KeyboardInterrupt):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno()) # prevent errors on final flush runtime makes
        sys.exit(0)


def parse_args():
    """Parse and validate command line arguments."""
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: pixelog <image_path>\n")
        sys.exit(1)

    image_path = Path(sys.argv[1])

    if not image_path.exists():
        sys.stderr.write(f"Error: File not found: {image_path}\n")
        sys.exit(1)

    if not image_path.is_file():
        sys.stderr.write(f"Error: Not a file: {image_path}\n")
        sys.exit(1)

    return image_path


def load_image(image_path):
    """Load image and convert to RGB."""
    try:
        img = Image.open(image_path)
        return img.convert("RGB")
    except Exception as e:
        sys.stderr.write(f"Error: Failed to load image: {e}\n")
        sys.exit(1)


def extract_colors(img):
    """Extract all pixels and count color occurrences."""
    pixels = list(img.getdata())
    color_counts = Counter(pixels)
    return color_counts


def format_color_line(r, g, b, count, total_pixels):
    """Format a single color line with colored block and all formats."""
    # Calculate percentage
    percentage = (count / total_pixels) * 100
    percentage_str = f"{percentage:6.2f}%"

    # ANSI 24-bit true color escape code
    colored_block = f"\x1b[38;2;{r};{g};{b}m██\x1b[0m"

    # Hex format (always 7 chars)
    hex_color = f"#{r:02x}{g:02x}{b:02x}"

    # RGB format - natural, then right-pad to 18 chars (max: "rgb(255, 255, 255)")
    rgb_color = f"rgb({r}, {g}, {b})".ljust(18)

    # OKLCH format - natural, then right-pad to 27 chars (max: "oklch(100.0% 9.999 360.0)")
    oklch_color = rgb_to_oklch(r, g, b).ljust(27)

    return f"{percentage_str} {colored_block} {hex_color} {rgb_color} {oklch_color}"


def rgb_to_oklch(r, g, b):
    """Convert RGB (0-255) to OKLCH format."""
    # Normalize RGB to 0-1 range
    rgb_normalized = [r / 255.0, g / 255.0, b / 255.0]

    # Convert to JCh (similar to OKLCH)
    jch = cspace_convert(rgb_normalized, "sRGB1", "JCh")

    # JCh format: [J (lightness), C (chroma), h (hue)]
    lightness = jch[0]  # 0-100
    chroma = jch[1] / 100.0  # Normalize chroma
    hue = jch[2]  # 0-360

    return f"oklch({lightness:.1f}% {chroma:.3f} {hue:.1f})"
