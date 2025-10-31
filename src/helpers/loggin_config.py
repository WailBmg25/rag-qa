import logging
import sys

# Basic configuration
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # logs to console
    ],
)

# Optional: define a specific logger for your app
logger = logging.getLogger("booklook")
