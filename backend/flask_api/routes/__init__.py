"""
Flask API Routes
"""

from .search import search_bp
from .health import health_bp
from .ui import ui_bp
from .images import images_bp

__all__ = ["search_bp", "health_bp", "ui_bp", "images_bp"]
