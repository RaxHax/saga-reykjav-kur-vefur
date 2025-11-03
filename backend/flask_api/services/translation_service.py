"""
Translation Service for Icelandic language support
"""

from typing import Tuple, Optional
from deep_translator import GoogleTranslator

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.config import Config
from shared.logger import get_logger

logger = get_logger(__name__)


class TranslationService:
    """Service for translating Icelandic text to English"""

    _instance: Optional['TranslationService'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize translator (only once)"""
        if self._initialized:
            return

        self.translator = None
        self.enabled = Config.ENABLE_ICELANDIC_TRANSLATION

        if self.enabled:
            self._initialize()

        self._initialized = True

    def _initialize(self):
        """Initialize Google Translator"""
        try:
            self.translator = GoogleTranslator(source="is", target="en")
            logger.info("Translation service initialized for Icelandic support")
        except Exception as e:
            logger.warning(f"Failed to initialize translator: {e}")
            self.translator = None

    def translate_if_icelandic(self, text: str) -> Tuple[str, bool]:
        """
        Detect if text is Icelandic and translate to English if needed.

        Args:
            text: Input text

        Returns:
            Tuple of (translated_text, was_translated)
        """
        if not self.enabled or not self.translator:
            return text, False

        try:
            # Simple heuristic: if text contains Icelandic characters, try translation
            icelandic_chars = set("áðéíóúýþæö")
            if any(char in text.lower() for char in icelandic_chars):
                logger.info(f"Detected Icelandic text, translating: '{text}'")
                translated = self.translator.translate(text)
                logger.info(f"Translated to: '{translated}'")
                return translated, True
        except Exception as e:
            logger.warning(f"Translation failed: {e}")
            if Config.TRANSLATION_FALLBACK:
                return text, False

        return text, False

    def is_enabled(self) -> bool:
        """Check if translation is enabled"""
        return self.enabled and self.translator is not None


# Global instance getter
def get_translation_service() -> TranslationService:
    """Get translation service instance"""
    return TranslationService()
