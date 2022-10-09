
dict_config = {
    'version': 1,
    'formatters': {
        'basic': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'loggers': {
        'root-logger': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}