#!/bin/bash

# Script Name: create_colored_sketch.sh
# Description: Converts a photo into a colored sketch and enhances it to look like professional artwork.

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

    # Create a refined and professional colored sketch
    echo "Creating a professional colored sketch from $photo_path..."
    
    # Step 1: Create a preliminary sketch and remove grey lines using artistic filters
    magick "$photo_path" -colorspace Gray -sketch 0x20+120 -normalize -contrast "$converted_folder/temp_gray_sketch.jpg"
    
    # Step 2: Blend the sketch with the original photo for color enhancement
    magick "$photo_path" "$converted_folder/temp_gray_sketch.jpg" -compose Multiply -composite "$sketch_path"

    # Step 3: Apply further artistic filters for a professional appearance
    magick "$sketch_path" -modulate 110,130,100 -sharpen 0x1 -brightness-contrast 15x10 -normalize "$sketch_path"

    # Step 4: Add final artistic touches
    magick "$sketch_path" -bordercolor white -border 5 -bordercolor black -border 2 -frame 15x15+2+2 "$sketch_path"

    # Clean up temporary files
    rm "$converted_folder/temp_gray_sketch.jpg"

    # Check if the colored sketch was successfully created
    if [ -f "$sketch_path" ]; then
        echo "Professional colored sketch created successfully! Saved to $sketch_path"
    else
        echo "Error: Failed to create the professional colored sketch."
        exit 1
    fi
}

# Call the function
create_colored_sketch


