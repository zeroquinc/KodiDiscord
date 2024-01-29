import requests
from urllib.parse import quote

from .custom_logger import logger
from .globals import TRAKT_API_KEY, TMDB_API_KEY

class Trakt:
    def __init__(self, info, media_type):
        self.info = info
        self.media_type = media_type
        self.tmdb_id = self.get_tmdb_id_trakt()

    def get_tmdb_id_trakt(self):
        if self.media_type == 'channel':
            return None

        tmdb_id = None
        if self.info['type'] == 'episode':
            tmdb_id = self.get_tmdb_id_for_media('tv')
        elif self.info['type'] == 'movie':
            tmdb_id = self.get_tmdb_id_for_media('movie')

        logger.debug(f"TMDB ID: {tmdb_id}")
        return tmdb_id

    def get_tmdb_id_for_media(self, media_type):
        if 'uniqueid' in self.info and 'tmdb' in self.info['uniqueid']:
            logger.debug("Found uniqueid in info")
            return self.info['uniqueid']['tmdb']
        else:
            logger.debug("Can't find TMDB ID in uniqueid")
            return None

    def get_trakt_url(self):
        if self.tmdb_id is None:
            return None

        base_url = "https://trakt.tv/"

        if self.media_type == "movie":
            media_url = base_url + "movies/"
            search_type = "movie"
        elif self.media_type == "tv":
            media_url = base_url + "shows/"
            search_type = "show"
        else:
            return None

        search_url = f"https://api.trakt.tv/search/tmdb/{self.tmdb_id}?type={search_type}"

        headers = {"trakt-api-key": TRAKT_API_KEY}
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            logger.debug(f"Trakt search response: {data}")

            trakt_slug = data[0][search_type]["ids"]["slug"]
            trakt_url = media_url + trakt_slug

            logger.debug(f"Generated Trakt URL: {trakt_url}")
            return trakt_url
        else:
            logger.error(f"Failed to get Trakt URL: {response.content}")
            return None