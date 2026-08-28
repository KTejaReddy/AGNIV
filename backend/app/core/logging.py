import logging
from logging.handlers import RotatingFileHandler
import os

LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    app_logger = logging.getLogger("agniv")
    app_logger.setLevel(logging.INFO)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    # File Handler
    file_handler = RotatingFileHandler(f"{LOGS_DIR}/app.log", maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(log_formatter)
    
    # Error Handler
    error_handler = RotatingFileHandler(f"{LOGS_DIR}/error.log", maxBytes=5*1024*1024, backupCount=5)
    error_handler.setFormatter(log_formatter)
    error_handler.setLevel(logging.ERROR)
    
    if not app_logger.handlers:
        app_logger.addHandler(console_handler)
        app_logger.addHandler(file_handler)
        app_logger.addHandler(error_handler)

    return app_logger

logger = setup_logging()
