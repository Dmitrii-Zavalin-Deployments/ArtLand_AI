#!/bin/bash

# Script Name: combine_artworks.sh
# Description: Combines a black-and-white sketch and a painting into a polished professional artwork by matching sketch points to colors from the painting.

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

    # Step 1: Create a base by merging sketch and painting with subtle blending
    echo "Merging sketch and painting with subtle blending..."
    magick "$painting_path" "$sketch_path" -compose Screen -composite "$output_path"

    # Step 2: Fill sketch points with colors from the painting
    echo "Matching sketch points to colors from painting..."
    magick "$output_path" "$sketch_path" -compose CopyOpacity -composite "$output_path"

    # Step 3: Apply additional adjustments for realism
    echo "Refining details and adding realism..."
    magick "$output_path" -modulate 105,120,100 -brightness-contrast 10x15 -normalize "$output_path"

    # Step 4: Final artistic enhancements
    echo "Adding final artistic touches..."
    magick "$output_path" -sharpen 0x1 -bordercolor white -border 10 -bordercolor black -border 5 -frame 20x20+5+5 "$output_path"

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


