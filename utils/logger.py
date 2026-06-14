# utils/logger.py
import logging

def setup_logger(name=__name__, level=logging.INFO):
    """Set up a simple console logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(ch)
    return logger
