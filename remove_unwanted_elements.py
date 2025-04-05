import cv2
import numpy as np
import os
from pathlib import Path

def detect_and_filter(image, size_threshold):
    """
    Detect and filter out small objects based on contour area.
    """
    # Convert image to grayscale and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Find contours of objects
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask for small objects
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < size_threshold:  # Remove small objects
            cv2.drawContours(mask, [contour], -1, 255, -1)

    return mask

def clean_sketch(image_path, cleaned_path, size_threshold):
    """
    Remove small objects from the sketch and save the cleaned image.
    """
    image = cv2.imread(image_path)
    mask = detect_and_filter(image, size_threshold)
    inpainted = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    cv2.imwrite(cleaned_path, inpainted)
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


