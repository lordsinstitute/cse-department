"""
Centralized logging configuration.

Use get_logger(__name__) in modules instead of print().
"""

import logging
import sys
from typing import Optional

from app.config import LOG_FORMAT, LOG_LEVEL


def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None,
) -> None:
    """
    Configure root logger for the application.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR). Defaults to config.
        format_string: Log format. Defaults to config.
    """
    lvl = (level or LOG_LEVEL).upper()
    fmt = format_string or LOG_FORMAT
    logging.basicConfig(
        level=getattr(logging, lvl, logging.INFO),
        format=fmt,
        stream=sys.stdout,
        force=True,
    )
    # Reduce noise from third-party libs
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a logger instance for the given module name."""
    return logging.getLogger(name)
