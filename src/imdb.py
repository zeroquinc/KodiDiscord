"""
This file contains functions to get IMDb information about a media.
"""

from .custom_logger import logger

# Function to get the IMDb ID of a media
def get_imdb_id(info):
    imdb_id = None
    # Check if 'uniqueid' and 'imdb' keys exist in the info
    if 'uniqueid' in info and 'imdb' in info['uniqueid']:
        imdb_id = info['uniqueid']['imdb']
    logger.debug(f"IMDb ID: {imdb_id}")
    return imdb_id

# Function to get the IMDb URL of a media
def get_imdb_url(imdb_id):
    if imdb_id is not None:
        logger.debug(f"IMDb URL: https://www.imdb.com/title/{imdb_id}/")
        return f"https://www.imdb.com/title/{imdb_id}/"
    else:
        logger.debug("IMDb URL: None")
        return None