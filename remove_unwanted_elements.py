import numpy as np
from skimage import io, measure, color
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.morphology import label
import os


def process_image(image_path, output_path, size_threshold_percentage):
    """
    Processes an input image, keeps only main elements (large objects),
    and saves the cleaned image.
    """
    # Ensure the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No such file: '{image_path}'")

    # Load the image
    try:
        # Load image and convert to grayscale
        image = io.imread(image_path)
        grayscale_image = color.rgb2gray(image)

        # Threshold the grayscale image to create a binary mask
        threshold = threshold_otsu(grayscale_image)
        binary_image = grayscale_image > threshold

        # Remove artifacts touching the border
        binary_image = clear_border(binary_image)

        # Label connected regions
        labeled_image = label(binary_image)

        # Calculate total pixels of the image
        total_pixels = image.shape[0] * image.shape[1]

        # Process regions to keep only large objects
        for region in measure.regionprops(labeled_image):
            region_area = region.area
            region_percentage = (region_area / total_pixels) * 100

            # Remove small regions below the size threshold
            if region_percentage < size_threshold_percentage:
                for coords in region.coords:
                    # Replace small regions with white in the original image
                    image[coords[0], coords[1]] = [255, 255, 255]  # White

        # Save the cleaned image
        io.imsave(output_path, image)
        print(f"Processed image saved to: {output_path}")

    except Exception as e:
        raise RuntimeError(f"Error processing the image: {e}")


if __name__ == "__main__":
    try:
        # Define input and output file paths
        input_path = "converted_sketches/colored_sketch.jpg"
        output_path = "converted_sketches/filtered_colored_sketch.jpg"

        # Define the size threshold percentage (adjust as needed)
        size_threshold_percentage = 5  # Keeps regions larger than 5% of the image

        print(f"Processing image: {input_path}")
        process_image(input_path, output_path, size_threshold_percentage)

    except FileNotFoundError as fnf_error:
        print(fnf_error)

    except RuntimeError as runtime_error:
        print(runtime_error)

    except Exception as general_error:
        print(f"Unexpected error: {general_error}")