import requests
from urllib.parse import quote

from config import DEFAULT_POSTER_URL
from .custom_logger import logger
from .globals import TMDB_API_KEY, port

"""
This file contains functions to fetch data from the TMDB API.
"""

# Function to get the media type of a media
def get_media_type(info):
    media_type = info['type']
    logger.debug(f"Media type: {media_type}")
    # If the media type is an episode, return 'tv', this is necessary because the TMDB API uses 'tv' for TV shows and Kodi uses 'episode' for TV shows
    return 'tv' if media_type == 'episode' else media_type

# Function to get the TMDB ID of a media
def get_tmdb_id_tmdb(info, media_type):
    # If the media type is a channel, return None
    if media_type == 'channel':
        return None

    tmdb_id = None
    if media_type == 'tv':
        tmdb_id = get_tmdb_id_for_tv_show(info)
    elif media_type == 'movie':
        tmdb_id = get_tmdb_id_for_media(info, 'movie')

    logger.debug(f"TMDB ID: {tmdb_id}")
    return tmdb_id

# Function to get the TMDB ID of a TV show
def get_tmdb_id_for_tv_show(info):
    tv_show_id = info['tvshowid']
    # If tvshowid is not None or -1, fetch the TMDB ID from the TV show details
    if tv_show_id != -1:
        tmdb_id = get_tmdb_id_from_tv_show_details(tv_show_id)
    else:
        tmdb_id = get_tmdb_id_for_media(info, 'tv')
    return tmdb_id

# Function to get the TMDB ID of a media via the TMDB API if the TMDB ID is not available in the info
def get_tmdb_id_from_tv_show_details(tv_show_id):
    tv_show_url = f"http://localhost:{port}/jsonrpc?request={{%22jsonrpc%22:%222.0%22,%22method%22:%22VideoLibrary.GetTVShowDetails%22,%22params%22:{{%22tvshowid%22:{tv_show_id},%22properties%22:[%22uniqueid%22]}},%22id%22:%22libTvShow%22}}"
    tv_show_response = requests.get(tv_show_url).json()
    logger.debug(f"TMDB Show search response: {tv_show_response}")
    # Check if 'result' key exists in the response
    if 'result' in tv_show_response and 'tvshowdetails' in tv_show_response['result'] and 'uniqueid' in tv_show_response['result']['tvshowdetails'] and 'tmdb' in tv_show_response['result']['tvshowdetails']['uniqueid']:
        return tv_show_response['result']['tvshowdetails']['uniqueid']['tmdb']
    return None

# Function to get the TMDB ID of a media via the TMDB API if the TMDB ID is not available in the info
def get_tmdb_id_for_media(info, media_type):
    title = quote(info['showtitle'] if media_type == 'tv' else info['title'])
    title_url = f"https://api.themoviedb.org/3/search/{media_type}?api_key={TMDB_API_KEY}&query={title}"
    title_response = requests.get(title_url).json()
    logger.debug(f"TMDB {media_type.capitalize()} search response: {title_response}")
    if 'results' in title_response and len(title_response['results']) > 0:
        logger.debug(f"TMDB {media_type.capitalize()} search results: {title_response['results'][0]['id']}")
        return title_response['results'][0]['id']
    return None

# Function to get the image URL of a media
def get_image_url(tmdb_id, media_type):
    # Default image URL
    image_url = DEFAULT_POSTER_URL
    if tmdb_id:
        # Fetch the image URL from the TMDB API
        image_url = get_image_url_from_tmdb(tmdb_id, media_type)
    logger.debug(f"Image URL: {image_url}")
    return image_url

# Function to get the image URL of a media via the TMDB API
def get_image_url_from_tmdb(tmdb_id, media_type):
    tmdb_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}"
    tmdb_response = requests.get(tmdb_url).json()
    logger.debug(f"TMDB Poster response: {tmdb_response}")
    if 'poster_path' in tmdb_response and tmdb_response['poster_path']:
        return f"https://image.tmdb.org/t/p/w185{tmdb_response['poster_path']}"
    return DEFAULT_POSTER_URL

# Function to get the TMDB URL of a media
def get_tmdb_url(tmdb_id, media_type):
    # Use a ternary operator to simplify the if-else structure
    url = f"https://www.themoviedb.org/{media_type}/{tmdb_id}" if tmdb_id else None
    logger.debug(f"TMDB URL: {url}")
    return url