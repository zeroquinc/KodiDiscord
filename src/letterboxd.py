from .custom_logger import logger

"""	
This module contains functions related to Letterboxd.
"""

# Function to get the Letterboxd URL of a media
def get_letterboxd_url(tmdb_id):
    url = f"https://letterboxd.com/tmdb/{tmdb_id}" if tmdb_id else None
    logger.debug(f"Letterboxd URL: {url}")
    return url