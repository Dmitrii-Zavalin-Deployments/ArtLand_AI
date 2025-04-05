#!/bin/bash

# Script Name: main.sh
# Description: Entry point script for orchestrating shell-based tasks.

# Define paths
base_dir=$(dirname "$0")
sketch_script="$base_dir/create_sketch.sh"
painting_script="$base_dir/create_painting.sh"
combine_script="$base_dir/combine_artworks.sh"
colored_sketch_script="$base_dir/create_colored_sketch.sh"
converted_sketches_folder="$base_dir/converted_sketches"

# Ensure required scripts are executable
echo "Setting script execution permissions..."
chmod +x "$sketch_script" "$painting_script" "$combine_script" "$colored_sketch_script"
echo "Scripts made executable successfully!"

# Ensure required files exist
echo "Checking for required scripts..."
for script in "$sketch_script" "$painting_script" "$combine_script" "$colored_sketch_script"; do
    if [ ! -f "$script" ]; then
        echo "Error: Script $script not found!"
        exit 1
    fi
done
echo "All required scripts found."

# Ensure the converted folder exists
if [ ! -d "$converted_sketches_folder" ]; then
    mkdir -p "$converted_sketches_folder"
    echo "Created folder: $converted_sketches_folder."
else
    rm -rf "$converted_sketches_folder"/*
    echo "Cleared files in folder: $converted_sketches_folder."
fi

# Run scripts sequentially
echo "Running the sketch script..."
bash "$sketch_script"

echo "Running the colored sketch script..."
bash "$colored_sketch_script"

echo "Running the painting script..."
bash "$painting_script"

echo "Running the combine artworks script..."
bash "$combine_script"

echo "Finished creating and refining sketches and paintings!"


