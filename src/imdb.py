import requests

from .custom_logger import logger
from .globals import port

"""
This file contains functions to get IMDb information about a media.
"""

# Function to get the media type of a media
def get_media_type(info):
    media_type = info['type']
    logger.debug(f"Media type: {media_type}")
    # If the media type is an episode, return 'tv', this is necessary because the TMDB API uses 'tv' for TV shows and Kodi uses 'episode' for TV shows
    return 'tv' if media_type == 'episode' else media_type

# Function to get the IMDb ID of a media
def get_imdb_id(info, media_type):
    # If the media type is a channel, return None
    if media_type == 'channel':
        return None

    imdb_id = None
    if media_type == 'tv':
        imdb_id = get_imdb_id_for_tv_show(info)
    elif media_type == 'movie':
        imdb_id = get_imdb_id_for_movie(info, 'movie')

    logger.debug(f"IMDb ID: {imdb_id}")
    return imdb_id

# Function to get the IMDb ID of a TV show
def get_imdb_id_for_tv_show(info):
    tv_show_id = info['tvshowid']
    # If tvshowid is not None or -1, fetch the IMDb ID from the TV show details
    if tv_show_id != -1:
        imdb_id = get_imdb_id_from_tv_show_details(tv_show_id)
    else: 
        return None
    return imdb_id

# Function to get the IMDb ID of a TV show via the Kodi JSONRPC API
def get_imdb_id_from_tv_show_details(tv_show_id):
    tv_show_url = f"http://localhost:{port}/jsonrpc?request={{%22jsonrpc%22:%222.0%22,%22method%22:%22VideoLibrary.GetTVShowDetails%22,%22params%22:{{%22tvshowid%22:{tv_show_id},%22properties%22:[%22uniqueid%22]}},%22id%22:%22libTvShow%22}}"
    tv_show_response = requests.get(tv_show_url).json()
    logger.debug(f"Kodi JSONRPC search response: {tv_show_response}")
    # Check if 'result' key exists in the response
    if 'result' in tv_show_response and 'tvshowdetails' in tv_show_response['result'] and 'uniqueid' in tv_show_response['result']['tvshowdetails'] and 'tmdb' in tv_show_response['result']['tvshowdetails']['uniqueid']:
        return tv_show_response['result']['tvshowdetails']['uniqueid']['imdb']
    return None

# Function to get the TMDB ID of a TV show
def get_imdb_id_for_movie(info):
    imdb_id = info['uniqueid']['imdb']
    return imdb_id

# Get IMDb URL
def get_imdb_url(imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None
    logger.debug(f"IMDb URL: {url}")
    return url