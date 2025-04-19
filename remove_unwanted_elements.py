import numpy as np
from skimage import io, measure, color
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.morphology import label
import os


def process_image(image_path, output_path):
    """
    Processes an input image to keep only the largest object,
    making all other objects fully transparent.
    """
    # Ensure the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No such file: '{image_path}'")

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

        # Identify the largest object by area
        regions = measure.regionprops(labeled_image)
        largest_region = max(regions, key=lambda r: r.area) if regions else None

        # Create a transparent version of the image
        transparent_image = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)

        for region in regions:
            for coords in region.coords:
                if region == largest_region:
                    # Keep the largest region as it is
                    transparent_image[coords[0], coords[1], :3] = image[coords[0], coords[1]]  # Preserve color
                    transparent_image[coords[0], coords[1], 3] = 255  # Set alpha to opaque
                else:
                    # Make other regions fully transparent
                    transparent_image[coords[0], coords[1], 3] = 0  # Fully transparent

        # Save the processed image
        io.imsave(output_path, transparent_image)
        print(f"Processed image saved to: {output_path}")

    except Exception as e:
        raise RuntimeError(f"Error processing the image: {e}")


if __name__ == "__main__":
    try:
        # Define input and output file paths
        input_path = "converted_sketches/colored_sketch.jpg"
        output_path = "converted_sketches/filtered_colored_sketch.png"  # Save as PNG to support transparency

        print(f"Processing image: {input_path}")
        process_image(input_path, output_path)

    except FileNotFoundError as fnf_error:
        print(fnf_error)

    except RuntimeError as runtime_error:
        print(runtime_error)

    except Exception as general_error:
        print(f"Unexpected error: {general_error}")



