import requests

from .custom_logger import logger
from .globals import port

class IMDB:
    def __init__(self, info):
        self.info = info
        self.media_type = self.get_media_type()
        self.imdb_id = self.get_imdb_id()

    def get_media_type(self):
        media_type = self.info['type']
        logger.debug(f"Media type: {media_type}")
        return 'tv' if media_type == 'episode' else media_type

    def get_imdb_id(self):
        if self.media_type == 'channel':
            return None

        if self.media_type == 'tv':
            return self.get_imdb_id_for_tv_show()
        elif self.media_type == 'movie':
            return self.get_imdb_id_for_movie()

        logger.debug(f"IMDb ID: {self.imdb_id}")
        return self.imdb_id

    def get_imdb_id_for_tv_show(self):
        tv_show_id = self.info['tvshowid']
        if tv_show_id != -1:
            return self.get_imdb_id_from_tv_show_details(tv_show_id)
        else: 
            return None

    def get_imdb_id_from_tv_show_details(self, tv_show_id):
        tv_show_url = f"http://localhost:{port}/jsonrpc?request={{%22jsonrpc%22:%222.0%22,%22method%22:%22VideoLibrary.GetTVShowDetails%22,%22params%22:{{%22tvshowid%22:{tv_show_id},%22properties%22:[%22uniqueid%22]}},%22id%22:%22libTvShow%22}}"
        tv_show_response = requests.get(tv_show_url).json()
        logger.debug(f"Kodi JSONRPC search response: {tv_show_response}")
        if 'result' in tv_show_response and 'tvshowdetails' in tv_show_response['result'] and 'uniqueid' in tv_show_response['result']['tvshowdetails'] and 'tmdb' in tv_show_response['result']['tvshowdetails']['uniqueid']:
            return tv_show_response['result']['tvshowdetails']['uniqueid']['imdb']
        return None

    def get_imdb_id_for_movie(self):
        return self.info['uniqueid']['imdb']

    def get_imdb_url(self):
        url = f"https://www.imdb.com/title/{self.imdb_id}/" if self.imdb_id else None
        logger.debug(f"IMDb URL: {url}")
        return url