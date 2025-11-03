"""
Search Service for semantic and hybrid image search
"""

from typing import List, Dict, Any, Optional
from qdrant_client.models import Filter, FieldCondition, MatchValue

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.config import Config
from shared.logger import get_logger
from shared.clip_manager import get_clip_manager
from shared.qdrant_manager import get_qdrant_manager

logger = get_logger(__name__)


class SearchService:
    """Service for performing image searches"""

    def __init__(self):
        self.clip_manager = get_clip_manager()
        self.qdrant_manager = get_qdrant_manager()

    def search(
        self,
        query: str,
        limit: Optional[int] = None,
        min_score: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Standard semantic search

        Args:
            query: Text query
            limit: Maximum number of results
            min_score: Minimum similarity score

        Returns:
            List of search results with scores and metadata
        """
        limit = limit or Config.DEFAULT_SEARCH_LIMIT
        min_score = min_score or Config.MIN_SIMILARITY_SCORE

        logger.info(f"Searching for: '{query}'")

        # Encode text query
        text_embedding = self.clip_manager.embed_text(query)
        if text_embedding is None:
            raise ValueError("Failed to encode query")

        # Search in Qdrant
        results = self.qdrant_manager.search(
            query_vector=text_embedding.tolist(),
            limit=limit,
            score_threshold=min_score,
        )

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "score": float(result.score),
                "filename": result.payload["filename"],
                "path": result.payload["path"],
                "description": result.payload.get("description", "No description"),
                "folder": result.payload.get("folder", ""),
            })

        logger.info(f"Found {len(formatted_results)} results")
        return formatted_results

    def hybrid_search(
        self,
        text_query: str,
        metadata_filter: Optional[Dict[str, Any]] = None,
        weights: Optional[Dict[str, float]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search combining text semantic search with metadata filtering

        Args:
            text_query: Text query
            metadata_filter: Metadata filter conditions
            weights: Search weights (text and metadata)
            limit: Maximum number of results

        Returns:
            List of search results with hybrid scores
        """
        limit = limit or Config.DEFAULT_SEARCH_LIMIT
        metadata_filter = metadata_filter or {}
        weights = weights or {}

        # Default weights
        text_weight = weights.get("text", Config.TEXT_SEARCH_WEIGHT)
        metadata_weight = weights.get("metadata", Config.METADATA_SEARCH_WEIGHT)

        logger.info(f"Hybrid search for: '{text_query}' with filters: {metadata_filter}")

        # Encode text query
        text_embedding = self.clip_manager.embed_text(text_query)
        if text_embedding is None:
            raise ValueError("Failed to encode query")

        # Build Qdrant filter from metadata
        query_filter = None
        if metadata_filter:
            conditions = []
            for key, value in metadata_filter.items():
                conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))

            if conditions:
                query_filter = Filter(must=conditions)

        # Search in Qdrant with filter
        results = self.qdrant_manager.search(
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
                    1 for key, value in metadata_filter.items()
                    if result.payload.get(key) == value
                )
                metadata_bonus = (metadata_matches / len(metadata_filter)) * metadata_weight
                hybrid_score += metadata_bonus

            formatted_results.append({
                "score": float(result.score),
                "hybrid_score": float(hybrid_score),
                "filename": result.payload["filename"],
                "path": result.payload["path"],
                "description": result.payload.get("description", "No description"),
                "folder": result.payload.get("folder", ""),
            })

        # Sort by hybrid score
        formatted_results.sort(key=lambda x: x["hybrid_score"], reverse=True)

        logger.info(f"Found {len(formatted_results)} hybrid results")
        return formatted_results


# Global instance getter
def get_search_service() -> SearchService:
    """Get search service instance"""
    return SearchService()
