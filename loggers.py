
dict_config = {
    "version": 1,
    'disable_existing_loggers': False,
    'formatters': {
	},
    "formatters": {
        "basic": {
            '()': 'colorlog.ColoredFormatter',
            "format": "{log_color}{levelname} - {asctime} - {name} - {blue}{message}",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            "style": '{',
        }
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": 'DEBUG',
        }
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": 'DEBUG',
            "propagate": False
        },
        "uvicorn": {
            "handlers": ["console"],
            "propagate": True
        },
        "gunicorn": {
            "propagate": True
            },
    },
}