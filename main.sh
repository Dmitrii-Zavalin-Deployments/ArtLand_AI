#!/bin/bash

# Script Name: main.sh
# Description: Entry point script for orchestrating tasks.

# Define paths
base_dir=$(dirname "$0")
sketch_script="$base_dir/create_sketch.sh"

# Ensure the sketch script exists
if [ ! -f "$sketch_script" ]; then
    echo "Error: Script 'create_sketch.sh' not found in the directory $base_dir"
    exit 1
fi

# Run the sketch script
echo "Starting create_sketch.sh..."
bash "$sketch_script"

# Confirm completion
echo "Finished create_sketch.sh!"



