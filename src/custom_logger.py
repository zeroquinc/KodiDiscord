from loguru import logger
import sys

from config import LOG_LEVEL

"""
This file contains the custom logger.
"""

# Function to switch the logger according to the LOG_LEVEL variable
def switch_logger():
    logger.remove()
    if LOG_LEVEL == 'DEBUG':
        logger.add(sys.stdout, level='DEBUG', colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <red>{file}</red> | <yellow>{function}</yellow> | <white>{level}</white> | <level>{message}</level>")
    elif LOG_LEVEL == 'INFO':
        logger.add(sys.stdout, level='INFO', colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <white>{level}</white> | <level>{message}</level>")
    else:
        raise ValueError("Invalid log level")

# Call the function to set the logger according to the LOG_LEVEL variable
switch_logger()