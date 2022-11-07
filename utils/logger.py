import os
import config
import logging
from logging import ERROR, INFO
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


log_level_map = {
    "info": INFO,
    "error": ERROR
}


def get_logger_lubber(log_file, log_format, log_level="info"):
    if not os.path.exists(log_file):
        os.makedirs(os.path.dirname(log_file))
    
    _logger = logging.getLogger("tornado.general")
    _logger.setLevel(log_level_map.get(config.log_level, INFO))
    fh = TimedRotatingFileHandler(filename=log_file, when='D', backupCount=30, encoding="utf-8")
    # fh = RotatingFileHandler(filename=log_file, mode='a', maxBytes=10*1024**2, backupCount=10, encoding="utf-8")
    ch = logging.StreamHandler()
    fh.setLevel(log_level_map.get(config.log_level, INFO))
    ch.setLevel(log_level_map.get(config.log_level, INFO))
    formatter = logging.Formatter(log_format)
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    _logger.addHandler(ch)
    _logger.addHandler(fh)
    _logger.removeHandler(ch)
    return _logger


def get_logger_tornado(log_name="tornado.general"):
    if not os.path.exists(config.log_file):
        os.makedirs(os.path.dirname(config.log_file))
    return logging.getLogger(log_name)


logger = get_logger_tornado()
# logger = get_logger_lubber(log_file=config.log_file, log_format=config.log_format, log_level="info")