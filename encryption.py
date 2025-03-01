import cv2
from utils import validate_image, get_image_capacity
import logging

def xor_encrypt(message, password):
    """
    Encrypt message using XOR with password
    """
    encrypted = []
    for i in range(len(message)):
        encrypted.append(ord(message[i]) ^ ord(password[i % len(password)]))
    return encrypted

def encrypt_image(image_path, message, password):
    """
    Encrypt a message into an image using steganography

    Args:
        image_path (str): Path to the input image
        message (str): Secret message to encrypt
        password (str): Password for encryption

    Returns:
        str: Path to the encrypted image
    """
    # Validate inputs
    if not message or not password:
        raise ValueError("Message and password cannot be empty")

    # Read and validate image
    img = validate_image(image_path)

    # Encrypt message using password
    encrypted_bytes = xor_encrypt(message, password)
    logging.info(f"Message encrypted: {len(encrypted_bytes)} bytes")

    # Check if message can fit in the image
    max_bytes = get_image_capacity(img)
    if len(encrypted_bytes) > max_bytes:
        raise ValueError(f"Message too long. Maximum length allowed: {max_bytes} characters")

    # Get image dimensions
    height, width = img.shape[:2]

    # Embed message length (32 bits / 4 bytes)
    msg_length = len(encrypted_bytes)
    byte_count = 0

    # Store length in first 4 bytes
    for i in range(4):
        row = byte_count // width
        col = byte_count % width
        img[row, col, 0] = (msg_length >> (i * 8)) & 0xFF
        byte_count += 1

    logging.info(f"Embedded message length: {msg_length} bytes")

    # Embed encrypted message bytes
    for byte in encrypted_bytes:
        row = byte_count // width
        col = byte_count % width
        channel = byte_count % 3
        img[row, col, channel] = byte
        byte_count += 1

    # Save the encrypted image
    output_path = "encrypted_" + image_path.split('/')[-1]
    cv2.imwrite(output_path, img)
    logging.info(f"Encrypted image saved as: {output_path}")

    return output_path