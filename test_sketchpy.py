import os
from sketchpy import library as sketch_lib

def create_sketch():
    # Define the path to the photo
    photo_folder = os.path.join(os.path.dirname(__file__), 'original_photos')
    photo_path = os.path.join(photo_folder, 'photo.jpg')  # Replace 'photo.jpg' with the actual filename
    
    # Check if the photo exists
    if not os.path.exists(photo_path):
        print(f"Error: Photo not found at {photo_path}")
        return

    # Create and draw the sketch
    sketch = sketch_lib.ImageSketch(photo_path)
    sketch.draw()

if __name__ == "__main__":
    create_sketch()


