import requests
import json

from .custom_logger import logger
from .globals import port

def get_media_type(info):
    media_type = info['type']
    logger.debug(f"Media type: {media_type}")
    return 'tv' if media_type == 'episode' else media_type

def get_imdb_id(info, media_type):
    if media_type == 'channel':
        return None

    function_map = {'tv': get_imdb_id_for_tv_show, 'movie': get_imdb_id_for_movie}
    imdb_id = function_map.get(media_type, lambda x: None)(info)
    logger.debug(f"IMDb ID: {imdb_id}")
    return imdb_id

def get_imdb_id_for_tv_show(info):
    tv_show_id = info['tvshowid']
    return get_imdb_id_from_tv_show_details(tv_show_id) if tv_show_id != -1 else None

def get_imdb_id_from_tv_show_details(tv_show_id):
    data = {
        "jsonrpc": "2.0",
        "method": "VideoLibrary.GetTVShowDetails",
        "params": {
            "tvshowid": tv_show_id,
            "properties": ["uniqueid"]
        },
        "id": "libTvShow"
    }
    tv_show_url = f"http://localhost:{port}/jsonrpc"
    headers = {'content-type': 'application/json'}
    tv_show_response = requests.post(tv_show_url, data=json.dumps(data), headers=headers).json()
    logger.debug(f"Kodi JSONRPC search response: {tv_show_response}")
    return tv_show_response.get('result', {}).get('tvshowdetails', {}).get('uniqueid', {}).get('imdb', None)

def get_imdb_id_for_movie(info):
    return info['uniqueid']['imdb']

def get_imdb_url(imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None
    logger.debug(f"IMDb URL: {url}")
    return url