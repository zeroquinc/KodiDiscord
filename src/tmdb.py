import requests
from config import DEFAULT_POSTER_URL
from .custom_logger import logger
from .globals import TMDB_API_KEY, port

"""
A collection of functions for interacting with The Movie Database (TMDb) API.

Args:
    info (dict): A dictionary containing information about the media.
    media_type (str): The type of media ('tv', 'movie', etc.).
    url (str): The URL to make the API request.
    tv_show_id (int): The ID of the TV show.
    tmdb_id (int): The TMDb ID of the media.
    tmdb_id (int): The TMDb ID of the media.
    media_type (str): The type of media ('tv', 'movie', etc.).

Returns:
    str: The media type ('tv' or 'movie').
    int: The TMDb ID of the media.
    dict: The API response in JSON format.
    str: The URL of the image.
    str: The URL of the TMDb page.
"""

def get_media_type(info):
    media_type = info['type']
    return 'tv' if media_type == 'episode' else media_type

def get_tmdb_id_tmdb(info, media_type):
    if media_type == 'channel':
        return None
    return (
        get_tmdb_id_for_tv_show(info)
        if media_type == 'tv'
        else get_tmdb_id_for_media(info)
    )

def get_tmdb_id_for_tv_show(info):
    tv_show_id = info.get('tvshowid', -1)
    return get_tmdb_id_from_tv_show_details(tv_show_id) if tv_show_id != -1 else None

def make_api_request(url):
    response = requests.get(url).json()
    logger.debug(f"API Response: {response}")
    return response

def get_tmdb_id_from_tv_show_details(tv_show_id):
    tv_show_url = f"http://localhost:{port}/jsonrpc?request={{%22jsonrpc%22:%222.0%22,%22method%22:%22VideoLibrary.GetTVShowDetails%22,%22params%22:{{%22tvshowid%22:{tv_show_id},%22properties%22:[%22uniqueid%22]}},%22id%22:%22libTvShow%22}}"
    response = make_api_request(tv_show_url)
    return response.get('result', {}).get('tvshowdetails', {}).get('uniqueid', {}).get('tmdb')

def get_tmdb_id_for_media(info):
    return info.get('uniqueid', {}).get('tmdb')

def get_image_url(tmdb_id, media_type):
    return get_image_url_from_tmdb(tmdb_id, media_type) if tmdb_id else DEFAULT_POSTER_URL

def get_image_url_from_tmdb(tmdb_id, media_type):
    tmdb_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}"
    response = make_api_request(tmdb_url)
    return f"https://image.tmdb.org/t/p/w185{response['poster_path']}" if 'poster_path' in response and response['poster_path'] else DEFAULT_POSTER_URL

def get_tmdb_url(tmdb_id, media_type):
    return f"https://www.themoviedb.org/{media_type}/{tmdb_id}" if tmdb_id else None