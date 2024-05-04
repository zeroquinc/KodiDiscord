from loguru import logger
import sys

from config import LOG_LEVEL

def switch_logger():
    """
    Switch the logger configuration based on the LOG_LEVEL variable.

    Explanation:
    This function sets up the logger configuration based on the value of the LOG_LEVEL variable. It removes the existing logger configuration and adds a new one with specific settings determined by the LOG_LEVEL value.

    Args:
        None

    Returns:
        None

    Raises:
        ValueError: If the LOG_LEVEL is not 'DEBUG' or 'INFO'.
    """
    logger.remove()
    log_configs = {
        'DEBUG': {"level": 'DEBUG', "colorize": True, "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <red>{file}</red> | <yellow>{function}</yellow> | <white>{level}</white> | <level>{message}</level>"},
        'INFO': {"level": 'INFO', "colorize": True, "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <white>{level}</white> | <level>{message}</level>"}
    }
    if LOG_LEVEL in log_configs:
        logger.add(sys.stdout, **log_configs[LOG_LEVEL])
    else:
        raise ValueError("Invalid log level")

switch_logger()