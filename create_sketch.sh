#!/bin/bash

# Script Name: create_sketch.sh
# Description: Converts a photo into a professional-quality sketch using ImageMagick and saves it in the converted_sketches folder.

# Function to create a sketch from a photo using ImageMagick
create_sketch() {
    # Define paths
    base_dir=$(dirname "$0")
    photo_folder="$base_dir/original_photos"
    converted_folder="$base_dir/converted_sketches"

    # Define the input and output paths
    photo_path="$photo_folder/photo.jpg"  # Replace 'photo.jpg' with your image file name
    sketch_path="$converted_folder/sketched_photo.jpg"  # Output sketch saved as a jpg image

    # Ensure the converted sketches folder exists
    mkdir -p "$converted_folder"

    # Check if the photo exists
    if [ ! -f "$photo_path" ]; then
        echo "Error: Photo not found at $photo_path"
        exit 1
    fi

    # Create and save the professional sketch using ImageMagick
    echo "Creating sketch from $photo_path..."
    magick "$photo_path" -colorspace Gray -sketch 0x20+120 -normalize -brightness-contrast 10x15 -bordercolor black -border 5 "$sketch_path"

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



