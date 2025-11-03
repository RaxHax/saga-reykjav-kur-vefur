"""
Health Check and Stats API Routes
"""

from flask import Blueprint, jsonify

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.logger import get_logger
from shared.clip_manager import get_clip_manager
from shared.qdrant_manager import get_qdrant_manager
from shared.config import Config
from flask_api.services.translation_service import get_translation_service

logger = get_logger(__name__)

health_bp = Blueprint('health', __name__, url_prefix='/api')


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    try:
        clip_manager = get_clip_manager()
        translation_service = get_translation_service()

        return jsonify({
            "status": "healthy",
            "model_loaded": clip_manager.model is not None,
            "device": clip_manager.device,
            "translator_available": translation_service.is_enabled(),
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


@health_bp.route("/stats", methods=["GET"])
def get_stats():
    """Get database statistics"""
    try:
        clip_manager = get_clip_manager()
        qdrant_manager = get_qdrant_manager()
        qdrant_stats = qdrant_manager.get_stats()

        return jsonify({
            "total_images": qdrant_stats.get("points_count", 0),
            "vector_size": Config.QDRANT_VECTOR_SIZE,
            "device": clip_manager.device,
            "icelandic_enabled": Config.ENABLE_ICELANDIC_TRANSLATION,
            "collection_name": qdrant_stats.get("collection_name"),
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            "total_images": 0,
            "vector_size": Config.QDRANT_VECTOR_SIZE,
            "device": "unknown",
            "icelandic_enabled": Config.ENABLE_ICELANDIC_TRANSLATION,
            "error": str(e)
        }), 500
