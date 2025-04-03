#!/bin/bash

# Script Name: main.sh
# Description: Entry point script for orchestrating tasks.

# Define paths
base_dir=$(dirname "$0")
sketch_script="$base_dir/create_sketch.sh"
painting_script="$base_dir/create_painting.sh"
converted_sketches_folder="$base_dir/converted_sketches"

# Ensure the sketch script exists
if [ ! -f "$sketch_script" ]; then
    echo "Error: Script 'create_sketch.sh' not found in the directory $base_dir"
    exit 1
fi

# Ensure the painting script exists
if [ ! -f "$painting_script" ]; then
    echo "Error: Script 'create_painting.sh' not found in the directory $base_dir"
    exit 1
fi

# Delete all files in the converted_sketches folder
if [ -d "$converted_sketches_folder" ]; then
    echo "Clearing all files in $converted_sketches_folder..."
    rm -rf "$converted_sketches_folder"/*
    echo "Folder $converted_sketches_folder cleared!"
else
    echo "Folder $converted_sketches_folder does not exist. Creating it..."
    mkdir -p "$converted_sketches_folder"
fi

# Run the sketch script
echo "Starting create_sketch.sh..."
bash "$sketch_script"

# Run the painting script
echo "Starting create_painting.sh..."
bash "$painting_script"

# Confirm completion
echo "Finished creating sketches and paintings!"



