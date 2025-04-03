#!/bin/bash

# Script Name: create_sketch.sh
# Description: Converts a photo into a sketch using ImageMagick and saves it in the converted_sketches folder.

# Function to create sketch from photo using ImageMagick
create_sketch() {
    # Define paths
    base_dir=$(dirname "$0")
    photo_folder="$base_dir/original_photos"
    converted_folder="$base_dir/converted_sketches"

    photo_path="$photo_folder/photo.jpg"  # Replace 'photo.jpg' with the name of your image file
    sketch_path="$converted_folder/sketched_photo.jpg"  # Output sketch saved as a jpg image

    # Check if the photo exists
    if [ ! -f "$photo_path" ]; then
        echo "Error: Photo not found at $photo_path"
        exit 1
    fi

    # Create and save the sketch using ImageMagick
    echo "Creating sketch from $photo_path..."
    magick "$photo_path" -charcoal 2 "$sketch_path"

    # Check if the sketch was successfully created
    if [ -f "$sketch_path" ]; then
        echo "Sketch created successfully! Saved to $sketch_path"
    else
        echo "Error: Failed to create the sketch."
        exit 1
    fi
}

# Call the function
create_sketch
