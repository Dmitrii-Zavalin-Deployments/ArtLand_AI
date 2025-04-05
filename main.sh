#!/bin/bash

# Script Name: main.sh
# Description: Entry point script for orchestrating tasks with dependency fixes.

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
pip install opencv-python opencv-python-headless numpy torch torchvision
pip install 'git+https://github.com/facebookresearch/detectron2.git'
if [ $? -ne 0 ]; then
    echo "Error: Failed to install detectron2. Please check your Python version and dependencies."
    deactivate
    exit 1
fi
echo "Python libraries installed successfully!"

# Make all scripts executable
echo "Ensuring all scripts are executable..."
chmod +x "$sketch_script"
chmod +x "$painting_script"
chmod +x "$combine_script"
chmod +x "$colored_sketch_script"

# Ensure the sketch script exists
if [ ! -f "$sketch_script" ]; then
    echo "Error: Script 'create_sketch.sh' not found in the directory $base_dir"
    deactivate
    exit 1
fi

# Ensure the painting script exists
if [ ! -f "$painting_script" ]; then
    echo "Error: Script 'create_painting.sh' not found in the directory $base_dir"
    deactivate
    exit 1
fi

# Ensure the combine artworks script exists
if [ ! -f "$combine_script" ]; then
    echo "Error: Script 'combine_artworks.sh' not found in the directory $base_dir"
    deactivate
    exit 1
fi

# Ensure the colored sketch script exists
if [ ! -f "$colored_sketch_script" ]; then
    echo "Error: Script 'create_colored_sketch.sh' not found in the directory $base_dir"
    deactivate
    exit 1
fi

# Ensure the Python script exists
if [ ! -f "$python_script" ]; then
    echo "Error: Script 'remove_unwanted_elements.py' not found in the directory $base_dir"
    deactivate
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

# Run the colored sketch script
echo "Starting create_colored_sketch.sh..."
bash "$colored_sketch_script"

# Run the painting script
echo "Starting create_painting.sh..."
bash "$painting_script"

# Run the combine artworks script
echo "Starting combine_artworks.sh..."
bash "$combine_script"

# Run the Python script to remove unwanted elements
echo "Starting remove_unwanted_elements.py..."
$PYTHON_BIN "$python_script"

# Deactivate virtual environment
deactivate

# Confirm completion
echo "Finished creating and refining sketches and paintings!"


