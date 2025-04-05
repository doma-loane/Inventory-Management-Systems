from flask import jsonify
import base64
from io import BytesIO
from PIL import Image

def process_qrcode(image_data):
    """
    Process a QR code image and extract the QR code value.
    :param image_data: Base64 encoded image data
    :return: Extracted QR code value or error message
    """
    try:
        # Decode the base64 image
        image_bytes = base64.b64decode(image_data.split(",")[1])
        image = Image.open(BytesIO(image_bytes))

        # Simulate QR code processing (replace with actual library if needed)
        qrcode_value = "SIMULATED_QRCODE_ABCDEF"  # Replace with actual QR code processing logic

        return jsonify({"success": True, "qrcode": qrcode_value}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

def optimize_image(image_path):
    """
    Optimize an image by converting it to WebP format.
    :param image_path: Path to the original image
    :return: Path to the optimized WebP image
    """
    try:
        image = Image.open(image_path)
        optimized_path = image_path.replace(".png", ".webp").replace(".jpg", ".webp")
        image.save(optimized_path, "WEBP", quality=80)
        return optimized_path
    except Exception as e:
        raise RuntimeError(f"Failed to optimize image: {e}")
