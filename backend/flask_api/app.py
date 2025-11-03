"""
Main Flask Application for SAGA Reykjavík Image Search

This is the reorganized version with modular structure:
- Routes are organized by functionality
- Services handle business logic
- Shared utilities in backend/shared/
"""

from flask import Flask
from flask_cors import CORS
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.config import Config
from shared.logger import setup_logger
from shared.clip_manager import CLIPManager
from shared.qdrant_manager import QdrantManager
from flask_api.routes import search_bp, health_bp, ui_bp, images_bp

# Setup logger
logger = setup_logger("flask_api")


def create_app() -> Flask:
    """Create and configure Flask application"""

    # Determine template and static paths (in root directory)
    root_dir = Path(__file__).parent.parent.parent
    template_dir = root_dir / "templates"
    static_dir = root_dir / "static"

    # Create Flask app
    app = Flask(
        __name__,
        template_folder=str(template_dir),
        static_folder=str(static_dir),
    )

    # Configuration
    app.config["SECRET_KEY"] = Config.FLASK_SECRET_KEY

    # CORS configuration
    CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=Config.CORS_ALLOW_CREDENTIALS)

    # Register blueprints
    app.register_blueprint(search_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(ui_bp)
    app.register_blueprint(images_bp)

    logger.info("Flask app created and configured")

    return app


def initialize_services():
    """Initialize all required services"""
    logger.info("=" * 60)
    logger.info("🖼️  SAGA Reykjavík Image Search System Starting...")
    logger.info("=" * 60)

    # Initialize CLIP model (singleton)
    logger.info("Initializing CLIP model...")
    clip_manager = CLIPManager()
    logger.info(f"CLIP model loaded: {clip_manager.get_info()}")

    # Initialize Qdrant client (singleton)
    logger.info("Initializing Qdrant database...")
    qdrant_manager = QdrantManager()
    stats = qdrant_manager.get_stats()
    logger.info(f"Qdrant ready: {stats['points_count']} images indexed")

    logger.info("=" * 60)
    logger.info("✅ Server ready!")
    logger.info(f"🌐 Open http://localhost:{Config.FLASK_PORT} in your browser")
    logger.info("=" * 60)


def main():
    """Main entry point"""
    # Initialize services
    initialize_services()

    # Create Flask app
    app = create_app()

    # Run server
    app.run(
        debug=Config.FLASK_DEBUG,
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        threaded=True,
    )


if __name__ == "__main__":
    main()
