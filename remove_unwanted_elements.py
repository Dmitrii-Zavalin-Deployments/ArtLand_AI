from PIL import Image, ImageDraw
import numpy as np
import os
from pathlib import Path


def detect_and_filter(image_array, size_threshold):
    """
    Detect and filter out small objects based on connected components.
    """
    height, width = image_array.shape
    mask = np.zeros((height, width), dtype=np.uint8)

    # Label components in the binary image
    labeled, num_features = label_components(image_array)

    # Calculate sizes of each component
    component_sizes = np.bincount(labeled.ravel())

    # Create mask to filter out small components
    for component_id, size in enumerate(component_sizes):
        if size < size_threshold and component_id != 0:  # Skip background
            mask[labeled == component_id] = 255

    return mask


def label_components(binary_image):
    """
    Label connected components in a binary image using a flood-fill algorithm.
    """
    labeled = np.zeros_like(binary_image, dtype=np.int32)
    current_label = 1

    height, width = binary_image.shape
    for y in range(height):
        for x in range(width):
            if binary_image[y, x] == 255 and labeled[y, x] == 0:
                # Start a flood-fill for new component
                flood_fill(binary_image, labeled, x, y, current_label)
                current_label += 1

    return labeled, current_label - 1


def flood_fill(binary_image, labeled, x, y, label):
    """
    Perform a flood-fill operation to label a connected component.
    """
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if cx < 0 or cy < 0 or cx >= binary_image.shape[1] or cy >= binary_image.shape[0]:
            continue
        if binary_image[cy, cx] == 255 and labeled[cy, cx] == 0:
            labeled[cy, cx] = label
            stack.extend([(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)])


def clean_sketch(image_path, cleaned_path, size_threshold):
    """
    Remove small objects from the sketch and save the cleaned image.
    """
    # Open image and convert to grayscale
    image = Image.open(image_path).convert("L")

    # Convert grayscale image to binary (0 and 255)
    binary_image = np.array(image)
    binary_image[binary_image < 128] = 0
    binary_image[binary_image >= 128] = 255

    # Detect and create mask for small objects
    mask = detect_and_filter(binary_image, size_threshold)

    # Create a cleaned version by masking out small objects
    cleaned_image = Image.fromarray(binary_image).convert("RGB")
    draw = ImageDraw.Draw(cleaned_image)
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if mask[y, x] == 255:
                draw.point((x, y), fill=(255, 255, 255))  # Fill small object areas with white

    # Save the cleaned image
    cleaned_image.save(cleaned_path)
    print(f"Cleaned sketch saved to {cleaned_path}")


# File paths
base_dir = Path(__file__).parent
sketch_path = base_dir / "converted_sketches" / "colored_sketch.jpg"
cleaned_sketch_path = base_dir / "converted_sketches" / "cleaned_colored_sketch.jpg"

# Ensure input file exists
if not os.path.exists(sketch_path):
    print(f"Error: File {sketch_path} not found.")
else:
    print("Processing the sketch...")
    # Adjust size threshold based on your requirements (e.g., 1000 pixels)
    clean_sketch(str(sketch_path), str(cleaned_sketch_path), size_threshold=1000)


