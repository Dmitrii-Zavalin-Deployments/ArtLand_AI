import cv2
import numpy as np
import torch
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
import os
from pathlib import Path

def load_model():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # Use GPU if available
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # Set threshold for detection
    return DefaultPredictor(cfg)

def detect_and_filter(image, predictor, size_threshold):
    outputs = predictor(image)  # Run the model
    instances = outputs["instances"].to("cpu")
    masks = instances.pred_masks.numpy()  # Extract masks
    areas = instances.pred_boxes.area().numpy()  # Get sizes of objects

    # Create a mask for small objects
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    for i, area in enumerate(areas):
        if area < size_threshold:  # Small objects
            mask[masks[i]] = 255  # Mark areas to clean
    return mask

def clean_sketch(image_path, cleaned_path, predictor, size_threshold):
    image = cv2.imread(image_path)
    mask = detect_and_filter(image, predictor, size_threshold)
    inpainted = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    cv2.imwrite(cleaned_path, inpainted)
    print(f"Cleaned sketch saved to {cleaned_path}")

# File paths
base_dir = Path(__file__).parent
sketch_path = base_dir / "converted_sketches" / "colored_sketch.jpg"
cleaned_sketch_path = base_dir / "converted_sketches" / "cleaned_colored_sketch.jpg"

# Ensure input file exists
if not os.path.exists(sketch_path):
    print(f"Error: File {sketch_path} not found.")
else:
    print("Loading model...")
    predictor = load_model()  # Load Detectron2 model
    print("Model loaded successfully.")
    # Adjust size threshold based on your requirements (e.g., 1000 pixels)
    clean_sketch(str(sketch_path), str(cleaned_sketch_path), predictor, size_threshold=1000)


