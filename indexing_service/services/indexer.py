"""
Image Indexer

Handles CLIP embedding generation and Qdrant vector storage
"""

import os
import torch
from pathlib import Path
from PIL import Image
import open_clip
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import logging

from utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageIndexer:
    """Handles image indexing with CLIP and Qdrant"""

    def __init__(self):
        self.device = None
        self.model = None
        self.preprocess = None
        self.tokenizer = None
        self.client = None
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "image_search")
        self.vector_size = int(os.getenv("QDRANT_VECTOR_SIZE", 512))

    async def initialize(self):
        """Initialize CLIP model and Qdrant client"""
        logger.info("Initializing Image Indexer...")

        # Determine device
        device_config = os.getenv("CLIP_DEVICE", "auto")
        if device_config == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device_config

        logger.info(f"Using device: {self.device}")

        # Load CLIP model
        model_name = os.getenv("CLIP_MODEL", "ViT-B-32")
        pretrained = os.getenv("CLIP_PRETRAINED", "laion2b_s34b_b79k")

        logger.info(f"Loading CLIP model: {model_name} ({pretrained})")
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            model_name, pretrained=pretrained
        )
        self.tokenizer = open_clip.get_tokenizer(model_name)
        self.model = self.model.to(self.device)
        self.model.eval()

        logger.info("CLIP model loaded successfully")

        # Initialize Qdrant client
        storage_path = os.getenv("QDRANT_STORAGE_PATH", "./qdrant_storage")
        logger.info(f"Connecting to Qdrant: {storage_path}")

        self.client = QdrantClient(path=storage_path)

        # Create collection if it doesn't exist
        try:
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception:
            logger.info(f"Creating collection '{self.collection_name}'")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )

        logger.info("Image Indexer initialized successfully")

    async def shutdown(self):
        """Clean up resources"""
        logger.info("Shutting down Image Indexer...")
        # Clean up if needed
        self.model = None
        self.client = None
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

            # Upsert to Qdrant
            point = PointStruct(id=point_id, vector=embedding.tolist(), payload=payload)

            self.client.upsert(collection_name=self.collection_name, points=[point])

            logger.debug(f"Indexed: {image_path}")
            return point_id

        except Exception as e:
            logger.error(f"Error indexing {image_path}: {e}")
            raise

    async def _embed_image(self, image_path: Path):
        """Generate CLIP embedding for an image"""
        try:
            with Image.open(image_path).convert("RGB") as img:
                image_tensor = self.preprocess(img).unsqueeze(0).to(self.device)

                with torch.no_grad():
                    image_features = self.model.encode_image(image_tensor)
                    image_features /= image_features.norm(dim=-1, keepdim=True)

                return image_features.cpu().numpy()[0]

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

    async def batch_index_images(self, image_paths: list[Path], batch_size: int = 100):
        """
        Index multiple images in batches
        """
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

            # Batch upsert
            if points:
                self.client.upsert(collection_name=self.collection_name, points=points)
                logger.info(f"Batch indexed: {len(points)} images")

        logger.info(f"Batch indexing complete: {total} images")
