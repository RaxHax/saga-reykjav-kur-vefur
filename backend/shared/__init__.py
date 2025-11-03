"""
Shared utilities for SAGA Reykjavík backend services
"""

from .config import get_config
from .logger import setup_logger, get_logger
from .clip_manager import CLIPManager
from .qdrant_manager import QdrantManager

__all__ = [
    "get_config",
    "setup_logger",
    "get_logger",
    "CLIPManager",
    "QdrantManager",
]
