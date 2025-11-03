"""
CLIP Model Manager - Singleton for managing CLIP model across services
"""

import torch
import open_clip
from PIL import Image
from typing import Optional, Tuple
import numpy as np

from .config import Config
from .logger import get_logger

logger = get_logger(__name__)


class CLIPManager:
    """Singleton manager for CLIP model"""

    _instance: Optional['CLIPManager'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize CLIP model (only once)"""
        if self._initialized:
            return

        self.device = None
        self.model = None
        self.preprocess = None
        self.tokenizer = None

        self._initialize()
        self._initialized = True

    def _initialize(self):
        """Initialize CLIP model and components"""
        logger.info("Initializing CLIP model...")

        # Determine device
        if Config.CLIP_DEVICE == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = Config.CLIP_DEVICE

        logger.info(f"Using device: {self.device}")

        # Load CLIP model
        logger.info(f"Loading CLIP model: {Config.CLIP_MODEL} ({Config.CLIP_PRETRAINED})")
        try:
            self.model, _, self.preprocess = open_clip.create_model_and_transforms(
                Config.CLIP_MODEL,
                pretrained=Config.CLIP_PRETRAINED
            )
            self.model = self.model.to(self.device)
            self.model.eval()
            self.tokenizer = open_clip.get_tokenizer(Config.CLIP_MODEL)

            logger.info("CLIP model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {e}")
            raise

    def embed_text(self, text: str) -> Optional[np.ndarray]:
        """
        Generate embedding for text

        Args:
            text: Input text

        Returns:
            512-dimensional embedding vector or None on error
        """
        try:
            text_input = self.tokenizer([text]).to(self.device)

            with torch.no_grad():
                text_features = self.model.encode_text(text_input)
                text_features /= text_features.norm(dim=-1, keepdim=True)

            return text_features.cpu().numpy()[0]
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            return None

    def embed_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Generate embedding for image

        Args:
            image_path: Path to image file

        Returns:
            512-dimensional embedding vector or None on error
        """
        try:
            image = Image.open(image_path).convert("RGB")
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                image_features = self.model.encode_image(image_input)
                image_features /= image_features.norm(dim=-1, keepdim=True)

            return image_features.cpu().numpy()[0]
        except Exception as e:
            logger.error(f"Error processing {image_path}: {e}")
            return None

    def embed_image_pil(self, image: Image.Image) -> Optional[np.ndarray]:
        """
        Generate embedding for PIL Image

        Args:
            image: PIL Image object

        Returns:
            512-dimensional embedding vector or None on error
        """
        try:
            image_input = self.preprocess(image.convert("RGB")).unsqueeze(0).to(self.device)

            with torch.no_grad():
                image_features = self.model.encode_image(image_input)
                image_features /= image_features.norm(dim=-1, keepdim=True)

            return image_features.cpu().numpy()[0]
        except Exception as e:
            logger.error(f"Error processing PIL image: {e}")
            return None

    def get_info(self) -> dict:
        """Get model information"""
        return {
            "model": Config.CLIP_MODEL,
            "pretrained": Config.CLIP_PRETRAINED,
            "device": self.device,
            "initialized": self._initialized,
        }


# Global instance getter
def get_clip_manager() -> CLIPManager:
    """Get CLIP manager instance"""
    return CLIPManager()
