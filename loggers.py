import logging
from logging import Logger, config, getLogger

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": "{log_color}{levelname} - {asctime} - {name} - {blue}{message}",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": "DEBUG",
        }
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "uvicorn": {"handlers": ["console"], "propagate": False},
        "gunicorn": {"propagate": False},
    },
}


def setup_logging() -> None:
    """Setup logging from dict configuration object."""
    config.dictConfig(config=LOGGING_CONFIG)


def get_logger(name: str) -> Logger:
    """Retrieve a logger by its name from dict_config."""
    return getLogger(name)
