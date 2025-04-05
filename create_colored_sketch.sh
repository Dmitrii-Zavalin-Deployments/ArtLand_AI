#!/bin/bash

# Script Name: create_colored_sketch.sh
# Description: Converts a photo into a colored sketch using ImageMagick and saves it in the converted_sketches folder.

# Function to create a colored sketch from a photo using ImageMagick
create_colored_sketch() {
    # Define paths
    base_dir=$(dirname "$0")
    photo_folder="$base_dir/original_photos"
    converted_folder="$base_dir/converted_sketches"

    # Define the input and output paths
    photo_path="$photo_folder/photo.jpg"  # Replace 'photo.jpg' with your image file name
    sketch_path="$converted_folder/colored_sketch.jpg"  # Output sketch saved as a jpg image

    # Ensure the converted sketches folder exists
    mkdir -p "$converted_folder"

    # Check if the photo exists
    if [ ! -f "$photo_path" ]; then
        echo "Error: Photo not found at $photo_path"
        exit 1
    fi

    # Create and save the colored sketch using ImageMagick
    echo "Creating colored sketch from $photo_path..."
    magick "$photo_path" -colorspace Gray -sketch 0x20+120 -normalize "$converted_folder/temp_gray_sketch.jpg"  # Temporary grayscale sketch
    magick "$photo_path" "$converted_folder/temp_gray_sketch.jpg" -compose Multiply -composite "$sketch_path"

    # Clean up temporary files
    rm "$converted_folder/temp_gray_sketch.jpg"

    # Check if the colored sketch was successfully created
    if [ -f "$sketch_path" ]; then
        echo "Colored sketch created successfully! Saved to $sketch_path"
    else
        echo "Error: Failed to create the colored sketch."
        exit 1
    fi
}

# Call the function
create_colored_sketch


