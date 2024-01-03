import logging

def get_logger(name):
    # Create a custom logger
    logger = logging.getLogger(name)
    
    # Any message below this level will be ignored.
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('logfile.log')
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.WARNING)

    # Create formatters and add it to handlers
    console_format = logging.Formatter('[%(levelname)s] - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger