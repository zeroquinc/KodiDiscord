"""	
This module contains functions related to Letterboxd.
"""

from .custom_logger import logger

# Function to get the Letterboxd URL of a media
def get_letterboxd_url(tmdb_id):
    logger.debug(f"Letterboxd URL: https://letterboxd.com/tmdb/{tmdb_id}")
    if tmdb_id is not None:
        return f"https://letterboxd.com/tmdb/{tmdb_id}"
    else:
        logger.debug("Letterboxd URL: None")
        return None