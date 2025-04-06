import numpy as np
from skimage import io, measure, color
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.morphology import label

def process_image(image_path, size_threshold_percentage):
    # Load the image
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

# Example usage
output_image = process_image("input.jpg", size_threshold_percentage=5)
io.imsave("filtered_image.jpg", output_image)


