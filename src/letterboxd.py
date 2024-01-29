from .custom_logger import logger

class Letterboxd:
    """	
    This class contains methods related to Letterboxd.
    """

    def __init__(self, tmdb_id):
        self.tmdb_id = tmdb_id
        self.url = self.get_letterboxd_url()

    # Method to get the Letterboxd URL of a media
    def get_letterboxd_url(self):
        url = f"https://letterboxd.com/tmdb/{self.tmdb_id}" if self.tmdb_id else None
        logger.debug(f"Letterboxd URL: {url}")
        return url