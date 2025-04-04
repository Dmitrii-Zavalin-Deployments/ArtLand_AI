#!/bin/bash

# Script Name: create_painting.sh
# Description: Converts a photo into a professional painting using ImageMagick and saves it in the converted_sketches folder.

# Function to create a painting from a photo using ImageMagick
create_painting() {
    # Define paths
    base_dir=$(dirname "$0")
    photo_folder="$base_dir/original_photos"
    converted_folder="$base_dir/converted_sketches"

    # Define the input and output paths
    photo_path="$photo_folder/photo.jpg"  # Replace 'photo.jpg' with your image file name
    painting_path="$converted_folder/painted_photo.jpg"  # Output painting saved as a jpg image

    # Ensure the converted sketches folder exists
    mkdir -p "$converted_folder"

    # Check if the photo exists
    if [ ! -f "$photo_path" ]; then
        echo "Error: Photo not found at $photo_path"
        exit 1
    fi

    # Create and save the painting using ImageMagick
    echo "Creating professional painting from $photo_path..."
    magick "$photo_path" -colorspace RGB -filter Gaussian -resize 3000x3000 -brightness-contrast 8x10 -normalize -modulate 100,110,100 "$painting_path"

    # Apply subtle artistic enhancements
    magick "$painting_path" -bordercolor white -border 10 -bordercolor black -border 5 -frame 15x15+4+4 "$painting_path"

    # Check if the painting was successfully created
    if [ -f "$painting_path" ]; then
        echo "Painting created successfully! Saved to $painting_path"
    else
        echo "Error: Failed to create the painting."
        exit 1
    fi
}

# Call the function
create_painting


