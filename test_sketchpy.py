import os
from sketchpy import library as sketch_lib

def create_sketch():
    # Define paths
    base_dir = os.path.dirname(__file__)
    photo_folder = os.path.join(base_dir, 'original_photos')
    converted_folder = os.path.join(base_dir, 'converted_sketches')
    
    # Ensure converted_sketches folder exists
    os.makedirs(converted_folder, exist_ok=True)
    
    photo_path = os.path.join(photo_folder, 'photo.jpg')  # Replace 'photo.jpg' with your image file
    sketch_path = os.path.join(converted_folder, 'sketched_photo.txt')  # Sketch saved as plain text for simplicity

    # Check if the photo exists
    if not os.path.exists(photo_path):
        print(f"Error: Photo not found at {photo_path}")
        return

    # Create and draw the sketch, and save output
    sketch = sketch_lib.ImageSketch(photo_path)
    print(f"Drawing sketch from {photo_path}...")
    sketch.draw()  # This opens Turtle graphics to create the sketch
    
    # Save a placeholder indicating the sketch was created
    with open(sketch_path, 'w') as f:
        f.write("Sketch created successfully! Check Turtle graphics window for details.")
    print(f"Sketch saved to {sketch_path}")

if __name__ == "__main__":
    create_sketch()



