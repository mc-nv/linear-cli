import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(debug=False):
    """Setup logger to write to LINEAR_CLI_LOG_DIR or console if --debug."""
    logger = logging.getLogger("linear-cli")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    log_dir = os.getenv("LINEAR_CLI_LOG_DIR")
    
    if log_dir:
        # Log to file in designated directory
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        log_file = log_path / f"linear-{datetime.now().strftime('%Y%m%d')}.log"
        
        handler = logging.FileHandler(log_file)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
    
    if debug:
        # Log to console when --debug flag is used
        console = logging.StreamHandler()
        console.setFormatter(
            logging.Formatter("%(levelname)s: %(message)s")
        )
        logger.addHandler(console)
    
    return logger


def get_logger():
    """Get the configured logger instance."""
    return logging.getLogger("linear-cli")

