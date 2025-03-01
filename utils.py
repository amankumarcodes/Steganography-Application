import cv2
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_image(image_path):
    """
    Validate and read an image file

    Args:
        image_path (str): Path to the input image

    Returns:
        cv2.Mat: Image matrix
    """
    # Check if file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Check file extension
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    file_ext = os.path.splitext(image_path)[1].lower()

    if file_ext not in valid_extensions:
        raise ValueError(f"Unsupported image format. Supported formats: {valid_extensions}")

    # Read image
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Failed to read image file")

    logging.info(f"Image loaded successfully: {image_path}")
    logging.info(f"Image dimensions: {img.shape[:2]}")

    return img

def get_image_capacity(img):
    """Calculate maximum bytes that can be stored in the image"""
    height, width = img.shape[:2]
    # We can use all color channels for storage
    return height * width * 3  # Full byte per channel

def create_char_mappings():
    """
    Create character to integer and integer to character mappings

    Returns:
        tuple: (char_to_int, int_to_char) dictionaries
    """
    char_to_int = {}
    int_to_char = {}

    # Create mappings for ASCII characters (0-255)
    for i in range(256):
        char = chr(i)
        char_to_int[char] = i
        int_to_char[i] = char

    return char_to_int, int_to_char