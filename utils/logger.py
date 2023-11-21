import logging
from logging.handlers import RotatingFileHandler


# Configure logger
logger = logging.getLogger('quvery_logger')
logger.setLevel(logging.INFO)

# Create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create rotating file handler
file_handler = RotatingFileHandler(
    'quvery-core.log', maxBytes=1048576, backupCount=1)  # 1 MB per file, keep 1 backups
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Add formatter to handlers
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
