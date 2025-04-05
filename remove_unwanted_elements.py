import cv2
import numpy as np
import os
from pathlib import Path

# Placeholder function to simulate object detection
def detect_objects(image):
    # Simulated output: list of bounding boxes [(x1, y1, x2, y2), ...] and sizes
    # Replace this with actual object detection model output
    detected_objects = [
        {"bbox": (50, 50, 200, 200), "size": 150*150},  # Example big object
        {"bbox": (300, 300, 320, 320), "size": 20*20}   # Example small object
    ]
    return detected_objects

def remove_small_objects(sketch_path, cleaned_sketch_path, size_threshold):
    print(f"Processing {sketch_path}...")

    # Load the sketch image
    sketch = cv2.imread(sketch_path)

    # Detect objects (you'd replace this with a real detection function)
    detected_objects = detect_objects(sketch)

    # Create a mask for small objects
    mask = np.zeros(sketch.shape[:2], dtype=np.uint8)
    for obj in detected_objects:
        if obj["size"] < size_threshold:  # Check size threshold
            x1, y1, x2, y2 = obj["bbox"]
            mask[y1:y2, x1:x2] = 255  # Mark small object area on the mask

    # Inpaint to remove small objects
    inpainted_sketch = cv2.inpaint(sketch, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    # Save the cleaned image
    cv2.imwrite(cleaned_sketch_path, inpainted_sketch)
    print(f"Cleaned sketch saved to {cleaned_sketch_path}")

# File paths
base_dir = Path(__file__).parent
sketch_path = base_dir / "converted_sketches" / "colored_sketch.jpg"
cleaned_sketch_path = base_dir / "converted_sketches" / "cleaned_colored_sketch.jpg"

# Ensure input file exists
if not os.path.exists(sketch_path):
    print(f"Error: File {sketch_path} not found.")
else:
    # Adjust size threshold based on your requirements (e.g., 1000 pixels)
    remove_small_objects(str(sketch_path), str(cleaned_sketch_path), size_threshold=1000)


