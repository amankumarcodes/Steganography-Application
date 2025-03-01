import cv2
from utils import validate_image, get_image_capacity
import logging

def xor_decrypt(encrypted_bytes, password):
    """
    Decrypt message using XOR with password
    """
    decrypted = ""
    for i in range(len(encrypted_bytes)):
        decrypted += chr(encrypted_bytes[i] ^ ord(password[i % len(password)]))
    return decrypted

def decrypt_image(image_path, password):
    """
    Decrypt a message from an image using steganography

    Args:
        image_path (str): Path to the encrypted image
        password (str): Password for decryption

    Returns:
        str: Decrypted message
    """
    # Validate password
    if not password:
        raise ValueError("Password cannot be empty")

    # Read and validate image
    img = validate_image(image_path)
    height, width = img.shape[:2]

    # Extract message length from first 4 bytes
    msg_length = 0
    byte_count = 0

    for i in range(4):
        row = byte_count // width
        col = byte_count % width
        msg_length |= (img[row, col, 0] << (i * 8))
        byte_count += 1

    logging.info(f"Detected message length: {msg_length} bytes")

    # Validate message length
    max_bytes = get_image_capacity(img)
    if msg_length <= 0 or msg_length > max_bytes:
        raise ValueError("Invalid message length detected")

    # Extract encrypted bytes
    encrypted_bytes = []
    try:
        for _ in range(msg_length):
            row = byte_count // width
            col = byte_count % width
            channel = byte_count % 3
            encrypted_bytes.append(img[row, col, channel])
            byte_count += 1
    except IndexError:
        raise ValueError("Image appears to be corrupted")

    logging.info(f"Extracted {len(encrypted_bytes)} encrypted bytes")

    # Decrypt the message using the password
    try:
        message = xor_decrypt(encrypted_bytes, password)
        logging.info("Message decrypted successfully")
        return message
    except Exception as e:
        raise ValueError(f"Failed to decrypt message: {str(e)}")