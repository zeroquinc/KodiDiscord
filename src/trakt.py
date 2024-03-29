import requests
from urllib.parse import quote

from .custom_logger import logger
from .globals import TRAKT_API_KEY, TMDB_API_KEY

"""
This file contains functions to fetch data from the Trakt API.
"""

# Function to get the TMDB ID of a media
def get_tmdb_id_trakt(info, media_type):
    # If the media type is a channel, return None
    if media_type == 'channel':
        return None

    tmdb_id = None
    if info['type'] == 'episode':
        tmdb_id = get_tmdb_id_for_media(info, 'tv')
    elif info['type'] == 'movie':
        tmdb_id = get_tmdb_id_for_media(info, 'movie')

    logger.debug(f"TMDB ID: {tmdb_id}")
    return tmdb_id

# Function to fetch the tmdb_id of the media
def get_tmdb_id_for_media(info, media_type):
    if 'uniqueid' in info and 'tmdb' in info['uniqueid']:
        logger.debug("Found uniqueid in info")
        return info['uniqueid']['tmdb']
    else:
        logger.debug("Can't find TMDB ID in uniqueid")
        return None

# Function to get the Trakt URL of a media
def get_trakt_url(tmdb_id, media_type):
        # Return None if tmdb_id is None
    if tmdb_id is None:
        return None
    
    # Define the base URL
    base_url = "https://trakt.tv/"

    # Check the media type
    if media_type == "movie":
        media_url = base_url + "movies/"
        search_type = "movie"
    elif media_type == "tv":
        media_url = base_url + "shows/"
        search_type = "show"
    else:
        return None

    search_url = f"https://api.trakt.tv/search/tmdb/{tmdb_id}?type={search_type}"

    # Send a GET request to the search endpoint
    headers = {"trakt-api-key": TRAKT_API_KEY}
    response = requests.get(search_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        logger.debug(f"Trakt search response: {data}")

        trakt_slug = data[0][search_type]["ids"]["slug"]
        trakt_url = media_url + trakt_slug

        logger.debug(f"Generated Trakt URL: {trakt_url}")
        return trakt_url
    else:
        logger.error(f"Failed to get Trakt URL: {response.content}")
        return None