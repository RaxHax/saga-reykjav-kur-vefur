"""
Logging Configuration
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name: str) -> logging.Logger:
    """
    Setup a logger with file and console handlers

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Get log level from environment
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger.level)

    # File handler (if LOG_FILE is set)
    log_file = os.getenv("LOG_FILE")
    if log_file:
        # Create log directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Rotating file handler
        max_bytes = int(os.getenv("MAX_LOG_SIZE_MB", 100)) * 1024 * 1024
        backup_count = int(os.getenv("LOG_BACKUP_COUNT", 5))

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
        )
        file_handler.setLevel(logger.level)

        # File formatter (more detailed)
        file_formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Console formatter (simpler)
    console_formatter = logging.Formatter(
        "%(levelname)s [%(name)s] %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger
