"""
Qdrant Manager - Singleton for managing Qdrant vector database connection
"""

from typing import Optional, List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter

from .config import Config
from .logger import get_logger

logger = get_logger(__name__)


class QdrantManager:
    """Singleton manager for Qdrant vector database"""

    _instance: Optional['QdrantManager'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize Qdrant client (only once)"""
        if self._initialized:
            return

        self.client = None
        self.collection_name = Config.QDRANT_COLLECTION_NAME

        self._initialize()
        self._initialized = True

    def _initialize(self):
        """Initialize Qdrant client and ensure collection exists"""
        logger.info("Initializing Qdrant client...")

        try:
            # Connect to Qdrant
            logger.info(f"Connecting to Qdrant: {Config.QDRANT_STORAGE_PATH}")
            self.client = QdrantClient(path=Config.QDRANT_STORAGE_PATH)

            # Create collection if it doesn't exist
            self._ensure_collection_exists()

            logger.info("Qdrant client initialized successfully!")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {e}")
            raise

    def _ensure_collection_exists(self):
        """Ensure the collection exists, create if not"""
        try:
            # Try to get collection info
            self.client.get_collection(self.collection_name)
            logger.info(f"Using existing collection: {self.collection_name}")
        except Exception:
            # Collection doesn't exist, create it
            logger.info(f"Creating new collection: {self.collection_name}")

            # Map distance metric string to enum
            distance_map = {
                "Cosine": Distance.COSINE,
                "Euclidean": Distance.EUCLID,
                "Dot": Distance.DOT,
            }
            distance = distance_map.get(Config.QDRANT_DISTANCE_METRIC, Distance.COSINE)

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=Config.QDRANT_VECTOR_SIZE,
                    distance=distance
                ),
            )
            logger.info("Collection created successfully!")

    def search(
        self,
        query_vector: List[float],
        limit: int = None,
        score_threshold: float = None,
        query_filter: Optional[Filter] = None,
    ) -> List[Any]:
        """
        Search for similar vectors

        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results
            score_threshold: Minimum similarity score
            query_filter: Optional metadata filter

        Returns:
            List of search results
        """
        limit = limit or Config.DEFAULT_SEARCH_LIMIT
        score_threshold = score_threshold or Config.MIN_SIMILARITY_SCORE

        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
            score_threshold=score_threshold,
        )

    def upsert(self, points: List[PointStruct]):
        """
        Insert or update points

        Args:
            points: List of PointStruct objects to upsert
        """
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "points_count": collection_info.points_count,
                "vector_size": Config.QDRANT_VECTOR_SIZE,
                "distance_metric": Config.QDRANT_DISTANCE_METRIC,
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                "collection_name": self.collection_name,
                "points_count": 0,
                "vector_size": Config.QDRANT_VECTOR_SIZE,
                "distance_metric": Config.QDRANT_DISTANCE_METRIC,
                "error": str(e),
            }

    def delete_collection(self):
        """Delete the collection (use with caution!)"""
        logger.warning(f"Deleting collection: {self.collection_name}")
        self.client.delete_collection(self.collection_name)

    def get_client(self) -> QdrantClient:
        """Get raw Qdrant client"""
        return self.client


# Global instance getter
def get_qdrant_manager() -> QdrantManager:
    """Get Qdrant manager instance"""
    return QdrantManager()
