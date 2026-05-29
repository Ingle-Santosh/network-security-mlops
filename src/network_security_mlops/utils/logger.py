import sys
import logging
from pathlib import Path
from datetime import datetime


# 1. Path Management
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# Using the / operator to join paths
LOG_FILE_PATH = LOG_DIR / LOG_FILE

# 2. Configuration
LOG_FORMAT = (
    "[%(asctime)s] %(filename)s:%(lineno)d %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("Network_security_mlops")
logger.setLevel(logging.INFO)

# 3. Handler Setup
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    console_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
