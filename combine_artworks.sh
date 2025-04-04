#!/bin/bash

# Script Name: combine_artworks.sh
# Description: Combines a black-and-white sketch and a painting into a polished professional artwork.

# Function to create a professional painting by combining a sketch and a painting
combine_artworks() {
    # Define paths
    base_dir=$(dirname "$0")
    converted_folder="$base_dir/converted_sketches"

    # Input files
    sketch_path="$converted_folder/sketched_photo.jpg"
    painting_path="$converted_folder/painted_photo.jpg"
    output_path="$converted_folder/final_painting.jpg"

    # Check if the sketch file exists
    if [ ! -f "$sketch_path" ]; then
        echo "Error: Sketch file not found at $sketch_path"
        exit 1
    fi

    # Check if the painting file exists
    if [ ! -f "$painting_path" ]; then
        echo "Error: Painting file not found at $painting_path"
        exit 1
    fi

    echo "Combining $sketch_path and $painting_path into $output_path..."

    # Step 1: Layer the sketch over the painting with controlled opacity
    echo "Applying layering effect..."
    magick "$painting_path" "$sketch_path" -compose Multiply -define compose:args=50 -composite "$output_path"

    # Step 2: Blend the sketch and painting using blending modes
    echo "Applying blending effect..."
    magick "$output_path" "$sketch_path" -compose Overlay -composite "$output_path"

    # Step 3: Apply a soft color wash from the painting to the sketch
    echo "Applying color wash effect..."
    magick "$output_path" -modulate 105,120,100 "$output_path"

    # Step 4: Add artistic finishing touches
    echo "Adding artistic finishing touches..."
    magick "$output_path" -adaptive-sharpen 0x1 -brightness-contrast 5x10 "$output_path"

    # Step 5: Add a professional border/frame
    echo "Adding border/frame..."
    magick "$output_path" -bordercolor white -border 10 -bordercolor black -border 5 -frame 20x20+4+4 "$output_path"

    # Check if the final artwork was successfully created
    if [ -f "$output_path" ]; then
        echo "Final professional painting created successfully! Saved to $output_path"
    else
        echo "Error: Failed to create the final professional painting."
        exit 1
    fi
}

# Call the function
combine_artworks