"""
Image Serving Routes
"""

from flask import Blueprint, send_file, jsonify
import os

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.logger import get_logger

logger = get_logger(__name__)

images_bp = Blueprint('images', __name__, url_prefix='/api')


@images_bp.route("/image/<path:filepath>")
def serve_image(filepath):
    """Serve image files"""
    try:
        if os.path.exists(filepath):
            return send_file(filepath)
        else:
            return jsonify({"error": "Image not found"}), 404
    except Exception as e:
        logger.error(f"Error serving image: {e}")
        return jsonify({"error": str(e)}), 500
