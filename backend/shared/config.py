"""
Centralized configuration management for all backend services
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from root .env file
root_dir = Path(__file__).parent.parent.parent
env_path = root_dir / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Config:
    """Application configuration"""

    # Flask Configuration
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

    # Indexing Service Configuration
    INDEXING_SERVICE_HOST = os.getenv("INDEXING_SERVICE_HOST", "0.0.0.0")
    INDEXING_SERVICE_PORT = int(os.getenv("INDEXING_SERVICE_PORT", 8001))
    INDEXING_SERVICE_WORKERS = int(os.getenv("INDEXING_SERVICE_WORKERS", 1))

    # CLIP Model Configuration
    CLIP_MODEL = os.getenv("CLIP_MODEL", "ViT-B-32")
    CLIP_PRETRAINED = os.getenv("CLIP_PRETRAINED", "laion2b_s34b_b79k")
    CLIP_DEVICE = os.getenv("CLIP_DEVICE", "auto")
    CLIP_BATCH_SIZE = int(os.getenv("CLIP_BATCH_SIZE", 32))

    # Qdrant Configuration
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    QDRANT_STORAGE_PATH = os.getenv("QDRANT_STORAGE_PATH", "./qdrant_storage")
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "image_search")
    QDRANT_VECTOR_SIZE = int(os.getenv("QDRANT_VECTOR_SIZE", 512))
    QDRANT_DISTANCE_METRIC = os.getenv("QDRANT_DISTANCE_METRIC", "Cosine")

    # Image Indexing Configuration
    DEFAULT_IMAGE_FOLDER = os.getenv("DEFAULT_IMAGE_FOLDER", "./scraped_images")
    SUPPORTED_IMAGE_FORMATS = os.getenv("SUPPORTED_IMAGE_FORMATS", "jpg,jpeg,png,webp").split(",")
    INDEX_BATCH_SIZE = int(os.getenv("INDEX_BATCH_SIZE", 100))
    MAX_CONCURRENT_INDEXING_JOBS = int(os.getenv("MAX_CONCURRENT_INDEXING_JOBS", 1))

    # Search Configuration
    DEFAULT_SEARCH_LIMIT = int(os.getenv("DEFAULT_SEARCH_LIMIT", 50))
    MIN_SIMILARITY_SCORE = float(os.getenv("MIN_SIMILARITY_SCORE", 0.0))
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", 100))
    TEXT_SEARCH_WEIGHT = float(os.getenv("TEXT_SEARCH_WEIGHT", 0.7))
    METADATA_SEARCH_WEIGHT = float(os.getenv("METADATA_SEARCH_WEIGHT", 0.3))

    # Icelandic Language Support
    ENABLE_ICELANDIC_TRANSLATION = os.getenv("ENABLE_ICELANDIC_TRANSLATION", "true").lower() == "true"
    TRANSLATION_FALLBACK = os.getenv("TRANSLATION_FALLBACK", "true").lower() == "true"
    SUPPORTED_LANGUAGES = os.getenv("SUPPORTED_LANGUAGES", "en,is").split(",")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

    # CORS Configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "")
    ENABLE_AUDIT_LOG = os.getenv("ENABLE_AUDIT_LOG", "true").lower() == "true"
    AUDIT_LOG_FILE = os.getenv("AUDIT_LOG_FILE", "audit.log")
    MAX_LOG_SIZE_MB = int(os.getenv("MAX_LOG_SIZE_MB", 10))

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("_") and key.isupper()
        }

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        return getattr(cls, key, default)


def get_config() -> Config:
    """Get configuration instance"""
    return Config
