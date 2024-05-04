from .custom_logger import logger

def get_letterboxd_url(tmdb_id):
    """
    Constructs the Letterboxd URL for a given TMDB ID.

    Parameters:
    - tmdb_id: The Movie Database (TMDB) ID of the media.

    Returns:
    - The Letterboxd URL string if tmdb_id is provided, else None.
    """
    url = f"https://letterboxd.com/tmdb/{tmdb_id}" if tmdb_id else None
    logger.debug(f"Letterboxd URL: {url}")
    return url