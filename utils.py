import logging


def get_logger_by_name(logger_name: str):
    """
    Retrieve a logger by its name
    from dict_config
    """
    logger = logging.getLogger(logger_name)
    return logger
