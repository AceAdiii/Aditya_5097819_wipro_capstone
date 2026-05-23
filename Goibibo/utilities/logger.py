import logging
import os

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/execution.log"

_logger = None

def get_logger():

    global _logger

    if _logger:
        return _logger

    logger = logging.getLogger("execution")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:

        file_handler = logging.FileHandler(LOG_FILE)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    _logger = logger
    return logger