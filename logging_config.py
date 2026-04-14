import logging
import json
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Structured JSON formatter for MoJ production logging."""

    RESERVED_FIELDS = {
        'name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
        'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
        'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
        'thread', 'threadName', 'processName', 'process', 'message',
        'taskName', 'asctime'
    }

    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in self.RESERVED_FIELDS:
                log_entry[key] = value

        return json.dumps(log_entry)


def configure_logging(app):
    """Call this in the app factory, after config is loaded."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.propagate = False