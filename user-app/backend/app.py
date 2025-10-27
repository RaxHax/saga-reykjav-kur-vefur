"""
SAGA Reykjavík Image Search API
Clean search-only backend for user-facing application
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import torch
import open_clip
from PIL import Image
from qdrant_client import QdrantClient
from pathlib import Path
import os
import logging
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="[%(asctime)s] %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
CORS(app, origins=cors_origins)

# Configuration
CONFIG = {
    "device": os.getenv("CLIP_DEVICE", "auto"),
    "clip_model": os.getenv("CLIP_MODEL", "ViT-B-32"),
    "clip_pretrained": os.getenv("CLIP_PRETRAINED", "laion2b_s34b_b79k"),
    "qdrant_path": os.getenv("QDRANT_STORAGE_PATH", "./qdrant_storage"),
    "collection_name": os.getenv("QDRANT_COLLECTION_NAME", "image_search"),
    "vector_size": int(os.getenv("QDRANT_VECTOR_SIZE", 512)),
    "enable_icelandic": os.getenv("ENABLE_ICELANDIC_TRANSLATION", "true").lower() == "true",
}

# Global variables
device = None
model = None
preprocess = None
tokenizer = None
client = None
translator = None


def initialize_models():
    """Initialize CLIP model, Qdrant client, and translator"""
    global model, preprocess, tokenizer, client, device, translator

    logger.info("=" * 60)
    logger.info("🖼️ SAGA Reykjavík Image Search API Starting...")
    logger.info("=" * 60)

    # Determine device
    if CONFIG["device"] == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = CONFIG["device"]

    logger.info(f"Using device: {device}")

    # Load CLIP
    logger.info(f"Loading CLIP model: {CONFIG['clip_model']} ({CONFIG['clip_pretrained']})")
    model, _, preprocess = open_clip.create_model_and_transforms(
        CONFIG["clip_model"], pretrained=CONFIG["clip_pretrained"]
    )
    model = model.to(device)
    model.eval()
    tokenizer = open_clip.get_tokenizer(CONFIG["clip_model"])
    logger.info("CLIP model loaded successfully")

    # Initialize Qdrant
    logger.info(f"Connecting to Qdrant: {CONFIG['qdrant_path']}")
    client = QdrantClient(path=CONFIG["qdrant_path"])
    logger.info("Qdrant connected successfully")

    # Initialize translator for Icelandic support
    if CONFIG["enable_icelandic"]:
        try:
            translator = GoogleTranslator(source="is", target="en")
            logger.info("Icelandic translator initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize translator: {e}")
            translator = None

    logger.info("=" * 60)
    logger.info("✅ Search API ready!")
    logger.info("=" * 60)


def translate_if_icelandic(text: str) -> tuple:
    """
    Detect if text is Icelandic and translate to English if needed.
    Returns: (translated_text, was_translated)
    """
    if not CONFIG["enable_icelandic"] or not translator:
        return text, False

    try:
        # Detect Icelandic characters
        icelandic_chars = set("áðéíóúýþæö")
        if any(char in text.lower() for char in icelandic_chars):
            logger.info(f"Translating Icelandic: '{text}'")
            translated = translator.translate(text)
            logger.info(f"Translated to: '{translated}'")
            return translated, True
    except Exception as e:
        logger.warning(f"Translation failed: {e}")

    return text, False


def embed_text(text: str):
    """Generate embedding for text"""
    try:
        text_input = tokenizer([text]).to(device)

        with torch.no_grad():
            text_features = model.encode_text(text_input)
            text_features /= text_features.norm(dim=-1, keepdim=True)

        return text_features.cpu().numpy()[0]
    except Exception as e:
        logger.error(f"Error encoding text: {e}")
        return None


# ============================================================================
# API ROUTES
# ============================================================================

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "search-api",
        "model_loaded": model is not None,
        "device": str(device),
        "translator_available": translator is not None,
    })


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get database statistics"""
    try:
        collection_info = client.get_collection(CONFIG["collection_name"])
        return jsonify({
            "total_images": collection_info.points_count,
            "vector_size": CONFIG["vector_size"],
            "device": str(device),
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/search", methods=["POST"])
def search_images():
    """Search for images using text query"""
    try:
        data = request.get_json()
        query = data.get("query", "")
        limit = data.get("limit", 50)
        min_score = data.get("min_score", 0.2)

        if not query:
            return jsonify({"error": "Query is required"}), 400

        logger.info(f"Searching for: '{query}'")

        # Generate text embedding
        query_embedding = embed_text(query)
        if query_embedding is None:
            return jsonify({"error": "Failed to generate embedding"}), 500

        # Search in Qdrant
        results = client.search(
            collection_name=CONFIG["collection_name"],
            query_vector=query_embedding.tolist(),
            limit=limit,
        )

        # Filter by minimum score and format results
        formatted_results = []
        for result in results:
            if result.score >= min_score:
                formatted_results.append({
                    "image_path": result.payload.get("image_path"),
                    "description": result.payload.get("description", ""),
                    "metadata": result.payload.get("metadata", {}),
                    "score": float(result.score),
                })

        logger.info(f"Found {len(formatted_results)} results")

        return jsonify({
            "results": formatted_results,
            "query": query,
            "count": len(formatted_results),
        })

    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/search/icelandic", methods=["POST"])
def search_images_icelandic():
    """Search with automatic Icelandic translation"""
    try:
        data = request.get_json()
        query = data.get("query", "")
        limit = data.get("limit", 50)
        min_score = data.get("min_score", 0.2)

        if not query:
            return jsonify({"error": "Query is required"}), 400

        # Translate if Icelandic
        translated_query, was_translated = translate_if_icelandic(query)

        logger.info(f"Searching for: '{translated_query}' (translated: {was_translated})")

        # Generate text embedding
        query_embedding = embed_text(translated_query)
        if query_embedding is None:
            return jsonify({"error": "Failed to generate embedding"}), 500

        # Search in Qdrant
        results = client.search(
            collection_name=CONFIG["collection_name"],
            query_vector=query_embedding.tolist(),
            limit=limit,
        )

        # Filter by minimum score and format results
        formatted_results = []
        for result in results:
            if result.score >= min_score:
                formatted_results.append({
                    "image_path": result.payload.get("image_path"),
                    "description": result.payload.get("description", ""),
                    "metadata": result.payload.get("metadata", {}),
                    "score": float(result.score),
                })

        logger.info(f"Found {len(formatted_results)} results")

        return jsonify({
            "results": formatted_results,
            "query": query,
            "translated_query": translated_query if was_translated else None,
            "was_translated": was_translated,
            "count": len(formatted_results),
        })

    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/image/<path:image_path>", methods=["GET"])
def get_image(image_path):
    """Serve image file"""
    try:
        if not os.path.exists(image_path):
            return jsonify({"error": "Image not found"}), 404

        return send_file(image_path, mimetype="image/jpeg")
    except Exception as e:
        logger.error(f"Error serving image: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    initialize_models()

    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
    )
