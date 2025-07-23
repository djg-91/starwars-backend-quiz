import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from decouple import config as env

LOG_DIR = Path(__file__).resolve().parent.parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    LOG_FILE = LOG_DIR / f'{name}.log'
    logger = logging.getLogger(name)

    logger.setLevel(env('LOG_LEVEL').upper())
    logger.propagate = False  # Avoid duplicate logging in console

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s => %(message)s')

        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
