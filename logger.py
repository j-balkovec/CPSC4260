# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: logger.py
#
# __brief__: TODO

import logging
import colorlog
import os
from datetime import datetime
from constants import (LOG_COLORS)

def setup_logger(name: str, log_file: str = None, level: int = logging.DEBUG, enable_console = False) -> logging.Logger:
    """_summary_

    Args:
        name (str): Name of the logger.
        log_file (str, optional): Path to the log file. Defaults to None.
        level (int, optional): Logging level. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False 

    log_format = (
        "%(log_color)s%(asctime)s | %(levelname)-8s | %(message)s%(reset)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    formatter = colorlog.ColoredFormatter(
        log_format,
        datefmt=date_format,
        log_colors=LOG_COLORS
    )

    if enable_console:
        formatter = colorlog.ColoredFormatter(
            log_format,
            datefmt=date_format,
            log_colors=LOG_COLORS
        )
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    if log_file:
        log_file = "logs/log_" + log_file  # to avoid accidental overwriting
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt=date_format
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger