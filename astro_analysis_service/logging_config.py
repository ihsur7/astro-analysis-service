"""Central logging configuration for the service."""
from __future__ import annotations

import json
import logging
from logging.config import dictConfig


def configure_logging() -> None:
    """Configure structured JSON logging for the service."""
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                }
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                }
            },
            "root": {
                "handlers": ["default"],
                "level": "INFO",
            },
        }
    )


class JsonFormatter(logging.Formatter):
    """Simple JSON formatter that keeps structured `extra` fields intact."""

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        payload.update(getattr(record, "extra_data", {}))
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


logger = logging.getLogger("astro-analysis-service")
