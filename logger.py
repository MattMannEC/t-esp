import logging

# Configure the logging system to include file name and line number
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

# Create a logger
logger = logging.getLogger(__name__)