"""
This module provides an upgraded logging utility.

Author: Kirtland McKenna - 8 March 2018
Copyright 2018 Kirtland McKenna
"""

import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(name, level=logging.INFO, max_bytes=2*1024*1024, backup=5):
    # Logging Levels:
    # CRITICAL
    # ERROR
    # WARNING
    # INFO
    # DEBUG

    root_path = os.path.dirname(os.path.dirname(__file__))
    log_file = root_path + '/Logs/' + name + '.out'

    handler = RotatingFileHandler(log_file, mode='w', maxBytes=max_bytes, encoding=None, delay=0, backupCount=backup)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    logger.info('Initialize {0} log file.'.format(name))
    return logger


runlog = setup_logger('runlog', level=logging.DEBUG)
alglog = setup_logger('alglog')

