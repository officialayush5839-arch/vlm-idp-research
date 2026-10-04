"""
Structured logging module for VLM-IDP research system.
Ensures uniform format, timestamping, run_id propagation, and credential redaction.
"""

from __future__ import annotations

import logging
import re
import sys
from typing import Optional

# Sensitive patterns that must never appear in logs
SENSITIVE_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password|bearer|auth)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-\.]{8,})['\"]?"),
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"ghp_[a-zA-Z0-9]{20,}"),
]


class SecurityRedactionFilter(logging.Filter):
    """Redacts accidental secrets, tokens, and passwords from log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            msg = record.msg
            for pattern in SENSITIVE_PATTERNS:
                if pattern.groups >= 2:
                    msg = pattern.sub(r"\1=[REDACTED]", msg)
                elif pattern.groups == 1:
                    msg = pattern.sub(r"[REDACTED]", msg)
                else:
                    msg = pattern.sub(r"[REDACTED]", msg)
            record.msg = msg
        return True


class RunContextFormatter(logging.Formatter):
    """Injects run_id context and standardized format into log messages."""

    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "run_id"):
            record.run_id = "-"
        return super().format(record)


def get_logger(name: str, run_id: Optional[str] = None) -> logging.Logger:
    """
    Get or configure a standardized logger.
    
    Args:
        name: Module or logger name (typically __name__)
        run_id: Optional active experiment run identifier
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = RunContextFormatter(
            fmt="%(asctime)s | %(levelname)-7s | run_id=%(run_id)s | %(name)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        handler.addFilter(SecurityRedactionFilter())
        logger.addHandler(handler)

    if run_id:
        logger = logging.LoggerAdapter(logger, {"run_id": run_id})  # type: ignore

    return logger
