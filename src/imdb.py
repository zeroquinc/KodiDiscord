from .custom_logger import logger

"""
This file contains functions to get IMDb information about a media.
"""

# Get IMDb ID
def get_imdb_id(info):
    imdb_id = info.get('uniqueid', {}).get('imdb')
    logger.debug(f"IMDb ID: {imdb_id}")
    return imdb_id

# Get IMDb URL
def get_imdb_url(imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None
    logger.debug(f"IMDb URL: {url}")
    return url