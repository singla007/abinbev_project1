import logging
import os

LOG_DIR = "logs"
LOG_FILE = "app.log"

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels

    # Prevent duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        # ch.setFormatter(formatter)
        # logger.addHandler(ch)

        # Ensure log directory exists
        os.makedirs(LOG_DIR, exist_ok=True)

        # File handler
        fh = logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger