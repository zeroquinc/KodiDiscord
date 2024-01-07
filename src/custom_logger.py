from loguru import logger
import sys

"""
This file contains the custom logger.
"""

# Remove the default handler and add a new one that only logs INFO and higher
logger.remove()
logger.add(sys.stdout, level='INFO', colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | <level>{message}</level>")