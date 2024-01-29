import requests
from urllib.parse import quote

from config import DEFAULT_POSTER_URL
from .custom_logger import logger
from .globals import TMDB_API_KEY, port

class TMDB:
    def __init__(self, info):
        self.info = info
        self.media_type = self.get_media_type()
        self.tmdb_id = self.get_tmdb_id()

    def get_media_type(self):
        media_type = self.info['type']
        logger.debug(f"Media type: {media_type}")
        return 'tv' if media_type == 'episode' else media_type

    def get_tmdb_id_tmdb(self):
        if self.media_type == 'channel':
            return None

        tmdb_id = None
        if self.media_type == 'tv':
            tmdb_id = self.get_tmdb_id_for_tv_show()
        elif self.media_type == 'movie':
            tmdb_id = self.get_tmdb_id_for_media()

        logger.debug(f"TMDB ID: {tmdb_id}")
        return tmdb_id

    def get_tmdb_id_for_tv_show(self):
        tv_show_id = self.info['tvshowid']
        if tv_show_id != -1:
            return self.get_tmdb_id_from_tv_show_details(tv_show_id)
        else:
            return None

    def get_tmdb_id_from_tv_show_details(self, tv_show_id):
        tv_show_url = f"http://localhost:{port}/jsonrpc?request={{%22jsonrpc%22:%222.0%22,%22method%22:%22VideoLibrary.GetTVShowDetails%22,%22params%22:{{%22tvshowid%22:{tv_show_id},%22properties%22:[%22uniqueid%22]}},%22id%22:%22libTvShow%22}}"
        tv_show_response = requests.get(tv_show_url).json()
        logger.debug(f"Kodi JSONRPC search response: {tv_show_response}")
        if 'result' in tv_show_response and 'tvshowdetails' in tv_show_response['result'] and 'uniqueid' in tv_show_response['result']['tvshowdetails'] and 'tmdb' in tv_show_response['result']['tvshowdetails']['uniqueid']:
            return tv_show_response['result']['tvshowdetails']['uniqueid']['tmdb']
        return None

    def get_tmdb_id_for_media(self):
        if 'uniqueid' in self.info and 'tmdb' in self.info['uniqueid']:
            logger.debug("Found uniqueid in info")
            return self.info['uniqueid']['tmdb']
        else:
            logger.debug("Can't find TMDB ID in uniqueid")
            return None

    def get_image_url(self):
        image_url = DEFAULT_POSTER_URL
        if self.tmdb_id:
            image_url = self.get_image_url_from_tmdb()
        logger.debug(f"Image URL: {image_url}")
        return image_url

    def get_image_url_from_tmdb(self):
        tmdb_url = f"https://api.themoviedb.org/3/{self.media_type}/{self.tmdb_id}?api_key={TMDB_API_KEY}"
        tmdb_response = requests.get(tmdb_url).json()
        logger.debug(f"TMDB Poster response: {tmdb_response}")
        if 'poster_path' in tmdb_response and tmdb_response['poster_path']:
            return f"https://image.tmdb.org/t/p/w185{tmdb_response['poster_path']}"
        return DEFAULT_POSTER_URL

    def get_tmdb_url(self):
        url = f"https://www.themoviedb.org/{self.media_type}/{self.tmdb_id}" if self.tmdb_id else None
        logger.debug(f"TMDB URL: {url}")
        return url