"""
Enhanced Flask Application for SAGA Reykjavík Image Search

Enhancements:
- Icelandic language support with automatic translation
- Hybrid search (text + metadata keywords)
- Environment variable configuration
- Better error handling and logging
- CORS support
- Additional search endpoints
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import torch
import open_clip
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from pathlib import Path
import os
import threading
import time
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
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
CORS(app, origins=cors_origins)

# Global configuration
CONFIG = {
    "device": os.getenv("CLIP_DEVICE", "auto"),
    "clip_model": os.getenv("CLIP_MODEL", "ViT-B-32"),
    "clip_pretrained": os.getenv("CLIP_PRETRAINED", "laion2b_s34b_b79k"),
    "qdrant_path": os.getenv("QDRANT_STORAGE_PATH", "./qdrant_storage"),
    "collection_name": os.getenv("QDRANT_COLLECTION_NAME", "image_search"),
    "vector_size": int(os.getenv("QDRANT_VECTOR_SIZE", 512)),
    "enable_icelandic": os.getenv("ENABLE_ICELANDIC_TRANSLATION", "true").lower() == "true",
    "translation_fallback": os.getenv("TRANSLATION_FALLBACK", "true").lower() == "true",
}

# Global variables
device = None
model = None
preprocess = None
tokenizer = None
client = None
translator = None

indexing_status = {
    "is_indexing": False,
    "progress": 0,
    "total": 0,
    "message": "",
    "start_time": None,
    "estimated_time": None,
}


def initialize_models():
    """Initialize CLIP model, Qdrant client, and translator"""
    global model, preprocess, tokenizer, client, device, translator

    logger.info("Initializing models...")

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

    # Initialize Qdrant
    logger.info(f"Connecting to Qdrant: {CONFIG['qdrant_path']}")
    client = QdrantClient(path=CONFIG["qdrant_path"])

    # Create collection if doesn't exist
    try:
        client.create_collection(
            collection_name=CONFIG["collection_name"],
            vectors_config=VectorParams(size=CONFIG["vector_size"], distance=Distance.COSINE),
        )
        logger.info("Created new collection")
    except Exception:
        logger.info("Using existing collection")

    # Initialize translator for Icelandic support
    if CONFIG["enable_icelandic"]:
        try:
            translator = GoogleTranslator(source="is", target="en")
            logger.info("Translator initialized for Icelandic support")
        except Exception as e:
            logger.warning(f"Failed to initialize translator: {e}")
            translator = None

    logger.info("Models initialized successfully!")


def translate_if_icelandic(text: str) -> tuple[str, bool]:
    """
    Detect if text is Icelandic and translate to English if needed.
    Returns: (translated_text, was_translated)
    """
    if not CONFIG["enable_icelandic"] or not translator:
        return text, False

    try:
        # Simple heuristic: if text contains Icelandic characters, try translation
        icelandic_chars = set("áðéíóúýþæö")
        if any(char in text.lower() for char in icelandic_chars):
            logger.info(f"Detected Icelandic text, translating: '{text}'")
            translated = translator.translate(text)
            logger.info(f"Translated to: '{translated}'")
            return translated, True
    except Exception as e:
        logger.warning(f"Translation failed: {e}")
        if CONFIG["translation_fallback"]:
            return text, False

    return text, False


def embed_image(image_path):
    """Generate embedding for an image"""
    try:
        image = Image.open(image_path).convert("RGB")
        image_input = preprocess(image).unsqueeze(0).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)

        return image_features.cpu().numpy()[0]
    except Exception as e:
        logger.error(f"Error processing {image_path}: {e}")
        return None


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


def read_description(txt_path):
    """Read description from .txt file"""
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content if content else "No description"
    except:
        return "No description"


def estimate_time_remaining(progress, total, start_time):
    """Estimate time remaining for indexing"""
    if progress == 0:
        return "Calculating..."

    elapsed = time.time() - start_time
    rate = progress / elapsed
    remaining = (total - progress) / rate

    if remaining < 60:
        return f"{int(remaining)}s remaining"
    elif remaining < 3600:
        return f"{int(remaining / 60)}m remaining"
    else:
        return f"{int(remaining / 3600)}h {int((remaining % 3600) / 60)}m remaining"


def index_images_background(image_folder):
    """Index images in background thread"""
    global indexing_status

    image_folder = Path(image_folder)

    # Find all image files
    supported_formats = os.getenv("SUPPORTED_IMAGE_FORMATS", "jpg,jpeg,png,webp").split(",")
    image_files = []

    for ext in supported_formats:
        image_files.extend(image_folder.glob(f"*.{ext}"))
        image_files.extend(image_folder.rglob(f"*.{ext}"))

    # Remove duplicates
    image_files = list(set(image_files))

    indexing_status["total"] = len(image_files)
    indexing_status["progress"] = 0
    indexing_status["start_time"] = time.time()
    indexing_status["message"] = f"Found {len(image_files)} images"

    logger.info(f"Starting to index {len(image_files)} images...")

    points = []
    batch_size = int(os.getenv("INDEX_BATCH_SIZE", 100))
    errors = 0

    for idx, image_file in enumerate(image_files):
        try:
            # Read description
            txt_file = image_file.with_suffix(".txt")
            description = read_description(txt_file)

            # Generate embedding
            embedding = embed_image(str(image_file))

            if embedding is None:
                errors += 1
                continue

            # Create point
            points.append(
                PointStruct(
                    id=idx,
                    vector=embedding.tolist(),
                    payload={
                        "filename": image_file.name,
                        "path": str(image_file.absolute()),
                        "description": description,
                        "folder": str(image_file.parent),
                    },
                )
            )

            # Batch upload
            if len(points) >= batch_size:
                client.upsert(collection_name=CONFIG["collection_name"], points=points)
                points = []

            # Update progress
            indexing_status["progress"] = idx + 1
            indexing_status["estimated_time"] = estimate_time_remaining(
                idx + 1, len(image_files), indexing_status["start_time"]
            )
            indexing_status["message"] = f"Processed {idx + 1}/{len(image_files)} images"

            # Log progress every 100 images
            if (idx + 1) % 100 == 0:
                logger.info(
                    f"Progress: {idx + 1}/{len(image_files)} ({(idx+1)/len(image_files)*100:.1f}%)"
                )

        except Exception as e:
            logger.error(f"Error with {image_file}: {e}")
            errors += 1
            continue

    # Upload remaining points
    if points:
        client.upsert(collection_name=CONFIG["collection_name"], points=points)

    # Finish
    indexing_status["is_indexing"] = False
    success_count = len(image_files) - errors
    indexing_status[
        "message"
    ] = f"Completed! Indexed {success_count} images ({errors} errors)"

    logger.info(f"Indexing complete! {success_count}/{len(image_files)} images indexed successfully")


# =============================================================================
# Routes - UI
# =============================================================================


@app.route("/")
def landing():
    """Serve the landing page"""
    return render_template("index.html")


@app.route("/workspace")
def workspace():
    """Serve the workspace UI"""
    return render_template("app.html")


@app.route("/projects")
def k2_projects():
    """Placeholder route for K2 Projects hub"""
    return render_template("k2_projects/index.html")


@app.route("/search/engines")
def k2_search():
    """Placeholder route for the K2 search engine hub"""
    return render_template("k2_search/index.html")


# =============================================================================
# Routes - API
# =============================================================================


@app.route("/api/index", methods=["POST"])
def start_indexing():
    """Start indexing images"""
    global indexing_status

    if indexing_status["is_indexing"]:
        return jsonify({"error": "Indexing already in progress"}), 400

    data = request.json
    image_folder = data.get("folder", os.getenv("DEFAULT_IMAGE_FOLDER", "./scraped_images"))

    if not os.path.exists(image_folder):
        return jsonify({"error": f"Folder not found: {image_folder}"}), 404

    # Reset status
    indexing_status = {
        "is_indexing": True,
        "progress": 0,
        "total": 0,
        "message": "Starting indexing...",
        "start_time": None,
        "estimated_time": None,
    }

    # Start background thread
    thread = threading.Thread(target=index_images_background, args=(image_folder,))
    thread.daemon = True
    thread.start()

    return jsonify({"message": "Indexing started", "status": indexing_status})


@app.route("/api/index/status", methods=["GET"])
def get_indexing_status():
    """Get current indexing status"""
    return jsonify(indexing_status)


@app.route("/api/search", methods=["POST"])
def search():
    """Standard semantic search"""
    data = request.json
    query = data.get("query", "")
    limit = data.get("limit", int(os.getenv("DEFAULT_SEARCH_LIMIT", 50)))
    min_score = data.get("min_score", float(os.getenv("MIN_SIMILARITY_SCORE", 0.0)))

    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        logger.info(f"Searching for: '{query}'")

        # Encode text query
        text_embedding = embed_text(query)
        if text_embedding is None:
            return jsonify({"error": "Failed to encode query"}), 500

        # Search in Qdrant
        results = client.search(
            collection_name=CONFIG["collection_name"],
            query_vector=text_embedding.tolist(),
            limit=limit,
            score_threshold=min_score,
        )

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append(
                {
                    "score": float(result.score),
                    "filename": result.payload["filename"],
                    "path": result.payload["path"],
                    "description": result.payload.get("description", "No description"),
                    "folder": result.payload.get("folder", ""),
                }
            )

        logger.info(f"Found {len(formatted_results)} results")

        return jsonify({"query": query, "results": formatted_results, "count": len(formatted_results)})

    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/search/icelandic", methods=["POST"])
def icelandic_search():
    """Search with Icelandic language support"""
    data = request.json
    query = data.get("query", "")
    limit = data.get("limit", int(os.getenv("DEFAULT_SEARCH_LIMIT", 50)))
    min_score = data.get("min_score", float(os.getenv("MIN_SIMILARITY_SCORE", 0.0)))

    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        logger.info(f"Icelandic search for: '{query}'")

        # Translate if Icelandic
        translated_query, was_translated = translate_if_icelandic(query)

        # Encode text query
        text_embedding = embed_text(translated_query)
        if text_embedding is None:
            return jsonify({"error": "Failed to encode query"}), 500

        # Search in Qdrant
        results = client.search(
            collection_name=CONFIG["collection_name"],
            query_vector=text_embedding.tolist(),
            limit=limit,
            score_threshold=min_score,
        )

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append(
                {
                    "score": float(result.score),
                    "filename": result.payload["filename"],
                    "path": result.payload["path"],
                    "description": result.payload.get("description", "No description"),
                    "folder": result.payload.get("folder", ""),
                }
            )

        logger.info(f"Found {len(formatted_results)} results")

        return jsonify(
            {
                "query": query,
                "translated_query": translated_query if was_translated else None,
                "was_translated": was_translated,
                "results": formatted_results,
                "count": len(formatted_results),
            }
        )

    except Exception as e:
        logger.error(f"Icelandic search error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/search/hybrid", methods=["POST"])
def hybrid_search():
    """Hybrid search combining text semantic search with metadata filtering"""
    data = request.json
    text_query = data.get("text_query", "")
    metadata_filter = data.get("metadata_filter", {})
    weights = data.get("weights", {})
    limit = data.get("limit", int(os.getenv("DEFAULT_SEARCH_LIMIT", 50)))

    # Default weights
    text_weight = weights.get("text", float(os.getenv("TEXT_SEARCH_WEIGHT", 0.7)))
    metadata_weight = weights.get("metadata", float(os.getenv("METADATA_SEARCH_WEIGHT", 0.3)))

    if not text_query:
        return jsonify({"error": "text_query is required"}), 400

    try:
        logger.info(f"Hybrid search for: '{text_query}' with filters: {metadata_filter}")

        # Encode text query
        text_embedding = embed_text(text_query)
        if text_embedding is None:
            return jsonify({"error": "Failed to encode query"}), 500

        # Build Qdrant filter from metadata
        query_filter = None
        if metadata_filter:
            conditions = []
            for key, value in metadata_filter.items():
                conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))

            if conditions:
                query_filter = Filter(must=conditions)

        # Search in Qdrant with filter
        results = client.search(
            collection_name=CONFIG["collection_name"],
            query_vector=text_embedding.tolist(),
            query_filter=query_filter,
            limit=limit,
        )

        # Format results with hybrid scoring
        formatted_results = []
        for result in results:
            # Calculate hybrid score (text score weighted + metadata match bonus)
            hybrid_score = result.score * text_weight

            # Add metadata match bonus if applicable
            if metadata_filter:
                metadata_matches = sum(
                    1 for key, value in metadata_filter.items() if result.payload.get(key) == value
                )
                metadata_bonus = (metadata_matches / len(metadata_filter)) * metadata_weight
                hybrid_score += metadata_bonus

            formatted_results.append(
                {
                    "score": float(result.score),
                    "hybrid_score": float(hybrid_score),
                    "filename": result.payload["filename"],
                    "path": result.payload["path"],
                    "description": result.payload.get("description", "No description"),
                    "folder": result.payload.get("folder", ""),
                }
            )

        # Sort by hybrid score
        formatted_results.sort(key=lambda x: x["hybrid_score"], reverse=True)

        logger.info(f"Found {len(formatted_results)} hybrid results")

        return jsonify(
            {
                "text_query": text_query,
                "metadata_filter": metadata_filter,
                "weights": {"text": text_weight, "metadata": metadata_weight},
                "results": formatted_results,
                "count": len(formatted_results),
            }
        )

    except Exception as e:
        logger.error(f"Hybrid search error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get database statistics"""
    try:
        collection_info = client.get_collection(CONFIG["collection_name"])
        return jsonify(
            {
                "total_images": collection_info.points_count,
                "vector_size": CONFIG["vector_size"],
                "device": device,
                "is_indexing": indexing_status["is_indexing"],
                "icelandic_enabled": CONFIG["enable_icelandic"],
            }
        )
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify(
            {
                "total_images": 0,
                "vector_size": CONFIG["vector_size"],
                "device": device,
                "is_indexing": False,
                "icelandic_enabled": CONFIG["enable_icelandic"],
            }
        )


@app.route("/api/image/<path:filepath>")
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


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "model_loaded": model is not None,
            "device": device,
            "translator_available": translator is not None,
        }
    )


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🖼️  SAGA Reykjavík Image Search System Starting...")
    print("=" * 60 + "\n")

    initialize_models()

    print("\n" + "=" * 60)
    print("✅ Server ready!")
    print(f"🌐 Open http://localhost:{os.getenv('FLASK_PORT', 5000)} in your browser")
    print("=" * 60 + "\n")

    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", 5000)),
        threaded=True,
    )
