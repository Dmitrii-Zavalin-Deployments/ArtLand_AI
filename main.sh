#!/bin/bash

# Script Name: main.sh
# Description: Entry point script for orchestrating tasks without detectron2 dependency.

# Define paths
base_dir=$(dirname "$0")
sketch_script="$base_dir/create_sketch.sh"
painting_script="$base_dir/create_painting.sh"
combine_script="$base_dir/combine_artworks.sh"
colored_sketch_script="$base_dir/create_colored_sketch.sh"
python_script="$base_dir/remove_unwanted_elements.py"
converted_sketches_folder="$base_dir/converted_sketches"

# Use Python 3.7 explicitly
PYTHON_BIN="/usr/bin/python3.7"

# Ensure Python 3.7 is installed
if [ ! -x "$PYTHON_BIN" ]; then
    echo "Error: Python 3.7 is not installed. Please install Python 3.7 and try again."
    exit 1
fi

# Create and activate a virtual environment using Python 3.7
echo "Setting up virtual environment..."
$PYTHON_BIN -m venv venv
source venv/bin/activate

# Install necessary Python libraries
echo "Installing Python libraries..."
pip install --upgrade pip
pip install numpy
pip install opencv-python opencv-python-headless numpy
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Python libraries. Please check your network or dependencies."
    deactivate
    exit 1
fi
echo "Python libraries installed successfully!"

# Make all scripts executable
echo "Setting script execution permissions..."
chmod +x "$sketch_script" "$painting_script" "$combine_script" "$colored_sketch_script"
echo "Scripts made executable successfully!"

# Ensure required files exist
echo "Checking for required scripts..."
for script in "$sketch_script" "$painting_script" "$combine_script" "$colored_sketch_script" "$python_script"; do
    if [ ! -f "$script" ]; then
        echo "Error: Script $script not found!"
        deactivate
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

# Run the Python script for cleaning up unwanted elements
echo "Running Python script to remove unwanted elements..."
$PYTHON_BIN "$python_script"

# Deactivate virtual environment
echo "Deactivating virtual environment..."
deactivate

# Confirm completion
echo "Finished creating and refining sketches and paintings!"


