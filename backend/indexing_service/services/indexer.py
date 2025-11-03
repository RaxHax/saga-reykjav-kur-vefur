"""
Image Indexer

Handles CLIP embedding generation and Qdrant vector storage
Now uses shared CLIP and Qdrant managers for consistency
"""

from pathlib import Path
from qdrant_client.models import PointStruct
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.clip_manager import get_clip_manager
from shared.qdrant_manager import get_qdrant_manager
from shared.config import Config
from shared.logger import get_logger

logger = get_logger(__name__)


class ImageIndexer:
    """Handles image indexing with CLIP and Qdrant using shared managers"""

    def __init__(self):
        self.clip_manager = None
        self.qdrant_manager = None
        self.collection_name = Config.QDRANT_COLLECTION_NAME

    async def initialize(self):
        """Initialize using shared managers"""
        logger.info("Initializing Image Indexer with shared managers...")

        # Use shared CLIP manager (singleton)
        self.clip_manager = get_clip_manager()
        logger.info(f"Using shared CLIP manager: {self.clip_manager.get_info()}")

        # Use shared Qdrant manager (singleton)
        self.qdrant_manager = get_qdrant_manager()
        stats = self.qdrant_manager.get_stats()
        logger.info(f"Using shared Qdrant manager: {stats}")

        logger.info("Image Indexer initialized successfully")

    async def shutdown(self):
        """Clean up resources"""
        logger.info("Shutting down Image Indexer...")
        # Shared managers are singletons, so we don't clean them up here
        self.clip_manager = None
        self.qdrant_manager = None
        logger.info("Image Indexer shut down successfully")

    async def index_image(self, image_path: Path) -> str:
        """
        Index a single image
        Returns: point ID
        """
        try:
            # Generate embedding
            embedding = await self._embed_image(image_path)

            # Read description if exists
            description = await self._read_description(image_path)

            # Create point
            point_id = str(hash(str(image_path)))

            # Prepare payload
            payload = {
                "filename": image_path.name,
                "path": str(image_path.absolute()),
                "description": description,
                "folder": str(image_path.parent),
            }

            # Upsert to Qdrant using shared manager
            point = PointStruct(id=point_id, vector=embedding.tolist(), payload=payload)
            self.qdrant_manager.upsert([point])

            logger.debug(f"Indexed: {image_path}")
            return point_id

        except Exception as e:
            logger.error(f"Error indexing {image_path}: {e}")
            raise

    async def _embed_image(self, image_path: Path):
        """Generate CLIP embedding for an image using shared CLIP manager"""
        try:
            # Use shared CLIP manager's embed_image method
            embedding = self.clip_manager.embed_image(str(image_path))
            if embedding is None:
                raise ValueError(f"Failed to embed image: {image_path}")
            return embedding

        except Exception as e:
            logger.error(f"Error embedding {image_path}: {e}")
            raise

    async def _read_description(self, image_path: Path) -> str:
        """Read description from paired .txt file"""
        txt_path = image_path.with_suffix(".txt")

        if txt_path.exists():
            try:
                with open(txt_path, "r", encoding="utf-8") as f:
                    description = f.read().strip()
                    return description if description else "No description"
            except Exception as e:
                logger.warning(f"Error reading description for {image_path}: {e}")
                return "No description"

        return "No description"

    async def batch_index_images(self, image_paths: list[Path], batch_size: int = None):
        """
        Index multiple images in batches
        """
        batch_size = batch_size or Config.INDEX_BATCH_SIZE
        total = len(image_paths)
        logger.info(f"Batch indexing {total} images (batch size: {batch_size})")

        for i in range(0, total, batch_size):
            batch = image_paths[i : i + batch_size]
            points = []

            for image_path in batch:
                try:
                    # Generate embedding
                    embedding = await self._embed_image(image_path)

                    # Read description
                    description = await self._read_description(image_path)

                    # Create point
                    point_id = str(hash(str(image_path)))

                    payload = {
                        "filename": image_path.name,
                        "path": str(image_path.absolute()),
                        "description": description,
                        "folder": str(image_path.parent),
                    }

                    point = PointStruct(id=point_id, vector=embedding.tolist(), payload=payload)
                    points.append(point)

                except Exception as e:
                    logger.error(f"Error processing {image_path}: {e}")
                    continue

            # Batch upsert using shared Qdrant manager
            if points:
                self.qdrant_manager.upsert(points)
                logger.info(f"Batch indexed: {len(points)} images ({i + len(points)}/{total})")

        logger.info(f"Batch indexing complete: {total} images")
