import sys
import logging
from logging.handlers import RotatingFileHandler

# logger
formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
log_file = "text_service.py"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    return console_handler


def get_file_handler():
    file_handler = RotatingFileHandler(log_file, maxBytes=1048576)
    file_handler.setFormatter(formatter)
    return file_handler


def get_logger(logger_name, debug='0'):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG) if debug=='1' else logger.setLevel(logging.WARNING) # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


