import torch
import numpy as np
from pathlib import Path
import imageio.v3 as iio


def read_image(image_path):
    """
    Reads an image file and returns it as a tensor (original color image) and a binary tensor.
    """
    try:
        # Read the image as a NumPy array
        color_image = torch.from_numpy(iio.imread(image_path)).float() / 255.0  # Normalize to [0, 1]
        grayscale_image = color_image.mean(dim=2)  # Convert to grayscale by averaging across channels
        binary_image = (grayscale_image > 0.5).float()  # Threshold to binary (0 or 1)
        return color_image, binary_image
    except Exception as e:
        print(f"Error reading image: {e}")
        return None, None


def remove_small_objects(binary_image, color_image, size_threshold):
    """
    Removes small objects from the binary tensor and updates the color image.
    """
    # Convert binary tensor to NumPy for connected component analysis
    binary_np = binary_image.numpy().astype(np.uint8)
    labeled_image, num_labels = connected_components(binary_np)

    # Iterate over connected components and filter based on size
    for label in range(1, num_labels):  # Skip the background (label 0)
        mask = labeled_image == label
        if np.sum(mask) < size_threshold:
            # Set the corresponding regions in the color image to white
            color_image[mask] = torch.tensor([1.0, 1.0, 1.0])  # RGB white

    return color_image


def connected_components(binary_image):
    """
    Implements connected component labeling for a binary image.
    """
    height, width = binary_image.shape
    labeled_image = np.zeros((height, width), dtype=np.int32)
    current_label = 1

    for y in range(height):
        for x in range(width):
            if binary_image[y, x] == 1 and labeled_image[y, x] == 0:
                stack = [(x, y)]
                while stack:
                    cx, cy = stack.pop()
                    if 0 <= cx < width and 0 <= cy < height:
                        if binary_image[cy, cx] == 1 and labeled_image[cy, cx] == 0:
                            labeled_image[cy, cx] = current_label
                            stack.extend([(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)])
                current_label += 1

    return labeled_image, current_label


def save_image(image_tensor, output_path):
    """
    Saves a color tensor as a JPG image.
    """
    try:
        # Convert the tensor back to a NumPy array and scale to [0, 255]
        image_np = (image_tensor.numpy() * 255).astype(np.uint8)
        iio.imwrite(output_path, image_np)
        print(f"Processed image saved to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")


# File paths
base_dir = Path(__file__).parent
sketch_path = base_dir / "converted_sketches" / "colored_sketch.jpg"
cleaned_sketch_path = base_dir / "converted_sketches" / "cleaned_colored_sketch.jpg"

# Ensure input file exists
if not sketch_path.exists():
    print(f"Error: File {sketch_path} not found.")
else:
    print("Processing the sketch...")
    color_image, binary_image = read_image(str(sketch_path))
    if color_image is not None and binary_image is not None:
        cleaned_image = remove_small_objects(binary_image, color_image, size_threshold=1000)
        save_image(cleaned_image, str(cleaned_sketch_path))


