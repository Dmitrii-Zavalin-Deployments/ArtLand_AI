#!/bin/bash

# Script Name: create_painting.sh
# Description: Converts a photo into a painting-like artwork using ImageMagick and saves it in the converted_paintings folder.

# Function to create painting-like effect from photo using ImageMagick
create_painting() {
    # Define paths
    base_dir=$(dirname "$0")
    photo_folder="$base_dir/original_photos"
    converted_folder="$base_dir/converted_paintings"

    photo_path="$photo_folder/photo.jpg"  # Replace 'photo.jpg' with the name of your image file
    painting_path="$converted_folder/painted_photo.jpg"  # Output painting saved as a jpg image

    # Check if the photo exists
    if [ ! -f "$photo_path" ]; then
        echo "Error: Photo not found at $photo_path"
        exit 1
    fi

    # Create and save the painting using ImageMagick
    echo "Creating painting from $photo_path..."
    magick "$photo_path" -paint 4 -modulate 110,140,100 -unsharp 0x1 "$painting_path"

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



