"""
Search API Routes
"""

from flask import Blueprint, request, jsonify

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.config import Config
from shared.logger import get_logger
from flask_api.services.search_service import get_search_service
from flask_api.services.translation_service import get_translation_service

logger = get_logger(__name__)

search_bp = Blueprint('search', __name__, url_prefix='/api')


@search_bp.route("/search", methods=["POST"])
def search():
    """Standard semantic search"""
    data = request.json
    query = data.get("query", "")
    limit = data.get("limit", Config.DEFAULT_SEARCH_LIMIT)
    min_score = data.get("min_score", Config.MIN_SIMILARITY_SCORE)

    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        search_service = get_search_service()
        results = search_service.search(query, limit, min_score)

        return jsonify({
            "query": query,
            "results": results,
            "count": len(results)
        })

    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@search_bp.route("/search/icelandic", methods=["POST"])
def icelandic_search():
    """Search with Icelandic language support"""
    data = request.json
    query = data.get("query", "")
    limit = data.get("limit", Config.DEFAULT_SEARCH_LIMIT)
    min_score = data.get("min_score", Config.MIN_SIMILARITY_SCORE)

    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        logger.info(f"Icelandic search for: '{query}'")

        # Translate if Icelandic
        translation_service = get_translation_service()
        translated_query, was_translated = translation_service.translate_if_icelandic(query)

        # Perform search
        search_service = get_search_service()
        results = search_service.search(translated_query, limit, min_score)

        return jsonify({
            "query": query,
            "translated_query": translated_query if was_translated else None,
            "was_translated": was_translated,
            "results": results,
            "count": len(results)
        })

    except Exception as e:
        logger.error(f"Icelandic search error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@search_bp.route("/search/hybrid", methods=["POST"])
def hybrid_search():
    """Hybrid search combining text semantic search with metadata filtering"""
    data = request.json
    text_query = data.get("text_query", "")
    metadata_filter = data.get("metadata_filter", {})
    weights = data.get("weights", {})
    limit = data.get("limit", Config.DEFAULT_SEARCH_LIMIT)

    if not text_query:
        return jsonify({"error": "text_query is required"}), 400

    try:
        search_service = get_search_service()
        results = search_service.hybrid_search(
            text_query=text_query,
            metadata_filter=metadata_filter,
            weights=weights,
            limit=limit
        )

        # Get actual weights used
        text_weight = weights.get("text", Config.TEXT_SEARCH_WEIGHT)
        metadata_weight = weights.get("metadata", Config.METADATA_SEARCH_WEIGHT)

        return jsonify({
            "text_query": text_query,
            "metadata_filter": metadata_filter,
            "weights": {"text": text_weight, "metadata": metadata_weight},
            "results": results,
            "count": len(results)
        })

    except Exception as e:
        logger.error(f"Hybrid search error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
