import numpy as np
import cv2
import os
from pathlib import Path


def read_image(image_path):
    """
    Reads the image file and returns it as a color image and its grayscale binary version.
    """
    try:
        color_image = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Read color image
        grayscale_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        _, binary_image = cv2.threshold(grayscale_image, 128, 255, cv2.THRESH_BINARY)  # Convert to binary
        return color_image, binary_image
    except Exception as e:
        print(f"Error reading image: {e}")
        return None, None


def remove_small_objects(binary_image, color_image, size_threshold):
    """
    Detect and remove small objects from the binary image and apply changes to the color image.
    """
    # Find connected components
    num_labels, labeled_image, stats, _ = cv2.connectedComponentsWithStats(binary_image, connectivity=8)

    # Remove components smaller than size_threshold
    for i in range(1, num_labels):  # Skip background component (label 0)
        if stats[i, cv2.CC_STAT_AREA] < size_threshold:
            color_image[labeled_image == i] = (255, 255, 255)  # Replace small objects with white pixels

    return color_image


def save_image(image, output_path):
    """
    Saves the processed image to the specified path as a JPG file.
    """
    try:
        cv2.imwrite(output_path, image)
        print(f"Processed image saved to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")


# File paths
base_dir = Path(__file__).parent
sketch_path = base_dir / "converted_sketches" / "colored_sketch.jpg"
cleaned_sketch_path = base_dir / "converted_sketches" / "cleaned_colored_sketch.jpg"

# Ensure input file exists
if not os.path.exists(sketch_path):
    print(f"Error: File {sketch_path} not found.")
else:
    print("Processing the sketch...")
    color_image, binary_image = read_image(str(sketch_path))
    if color_image is not None and binary_image is not None:
        cleaned_image = remove_small_objects(binary_image, color_image, size_threshold=1000)
        save_image(cleaned_image, str(cleaned_sketch_path))


