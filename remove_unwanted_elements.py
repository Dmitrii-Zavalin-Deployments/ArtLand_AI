import numpy as np
from skimage import io, measure, color
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.morphology import label
import os

def process_image(image_path, size_threshold_percentage):
    """
    Processes an input image, filters out small objects, and returns the cleaned image.
    """
    # Ensure the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No such file: '{image_path}'")

    # Load the image
    try:
        image = io.imread(image_path)
        grayscale_image = color.rgb2gray(image)

        # Threshold the image
        threshold = threshold_otsu(grayscale_image)
        binary_image = grayscale_image > threshold

        # Clear border artifacts
        binary_image = clear_border(binary_image)

        # Label connected regions
        labeled_image = label(binary_image)

        # Calculate total pixels
        total_pixels = image.shape[0] * image.shape[1]

        # Process and filter regions
        for region in measure.regionprops(labeled_image):
            region_area = region.area
            region_percentage = (region_area / total_pixels) * 100

            # Remove regions below the size threshold
            if region_percentage < size_threshold_percentage:
                for coords in region.coords:
                    image[coords[0], coords[1]] = [255, 255, 255]  # Replace with white

        return image

    except Exception as e:
        raise RuntimeError(f"Error processing the image: {e}")


if __name__ == "__main__":
    try:
        # Define input and output paths
        input_path = "converted_sketches/colored_sketch.jpg"
        output_path = "converted_sketches/filtered_colored_sketch.jpg"

        print(f"Processing image: {input_path}")
        output_image = process_image(input_path, size_threshold_percentage=5)
        io.imsave(output_path, output_image)
        print(f"Filtered image saved to: {output_path}")

    except FileNotFoundError as fnf_error:
        print(fnf_error)

    except RuntimeError as runtime_error:
        print(runtime_error)

    except Exception as general_error:
        print(f"Unexpected error: {general_error}")


