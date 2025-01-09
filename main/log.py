import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime


def configure_logging(log_file: str = "app.log", level: int = logging.INFO) -> None:
    # Full path to the log file
    today_date = datetime.now().strftime("%Y-%m-%d")
    log_file_with_date = f"{today_date}_{log_file}"

    # Create a root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Prevent duplicate handlers if configure_logging is called multiple times
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create file handler with rotation
        file_handler = RotatingFileHandler(log_file_with_date, maxBytes=5_000_000, backupCount=3)
        file_handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Attach formatter to handlers
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

configure_logging()
logger = logging.getLogger(__name__)

# example uses
# logger.info("Starting code")
# logger.debug("This is a debug message for troubleshooting.")
# logger.warning("This is a warning message.")
# logger.error("An error occurred!")
# logger.critical("Critical issue!")