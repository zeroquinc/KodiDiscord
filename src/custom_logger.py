from loguru import logger
import sys

# Remove the default handler and add a new one that only logs INFO and higher
logger.remove()
logger.add(sys.stderr, level='INFO')