import numpy as np
import cv2
import os
from pathlib import Path


def read_image_as_binary(image_path):
    """
    Reads an image file and converts it into a binary (black-and-white) numpy array.
    """
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Read image in grayscale
        _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)  # Convert to binary
        return binary_image
    except Exception as e:
        print(f"Error reading image: {e}")
        return None


def remove_small_objects(binary_image, size_threshold):
    """
    Detect and remove small objects from the binary image using connected components.
    """
    labeled_image = np.zeros_like(binary_image, dtype=np.int32)
    current_label = 1
    height, width = binary_image.shape

    # Label connected components with a flood-fill approach
    for y in range(height):
        for x in range(width):
            if binary_image[y, x] == 255 and labeled_image[y, x] == 0:
                flood_fill(binary_image, labeled_image, x, y, current_label)
                current_label += 1

    # Calculate the size of each labeled component
    component_sizes = np.bincount(labeled_image.ravel())
    for component_id, size in enumerate(component_sizes):
        if size < size_threshold and component_id != 0:  # Skip background (label 0)
            binary_image[labeled_image == component_id] = 0  # Remove small object

    return binary_image


def flood_fill(binary_image, labeled_image, x, y, label):
    """
    Flood-fill algorithm to label connected components in a binary image.
    """
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()  # Correctly unpack the tuple (x, y)
        if cx < 0 or cy < 0 or cx >= binary_image.shape[1] or cy >= binary_image.shape[0]:
            continue
        if binary_image[cy, cx] == 255 and labeled_image[cy, cx] == 0:
            labeled_image[cy, cx] = label
            stack.extend([(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)])  # Push tuples (x, y)


def save_binary_image_as_jpg(image_array, output_path):
    """
    Saves the binary image as a JPG file.
    """
    try:
        cv2.imwrite(output_path, image_array)
        print(f"Cleaned image saved to {output_path}")
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
    binary_image = read_image_as_binary(str(sketch_path))
    if binary_image is not None:
        cleaned_image = remove_small_objects(binary_image, size_threshold=1000)
        save_binary_image_as_jpg(cleaned_image, str(cleaned_sketch_path))


