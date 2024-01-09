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
        tv_show_id = info['tvshowid']
        # If tvshowid is not None or -1, fetch the TMDB ID from the TV show details
        tv_show_url = f"http://localhost:{port}/jsonrpc?request={{%22jsonrpc%22:%222.0%22,%22method%22:%22VideoLibrary.GetTVShowDetails%22,%22params%22:{{%22tvshowid%22:{tv_show_id},%22properties%22:[%22uniqueid%22]}},%22id%22:%22libTvShow%22}}"
        tv_show_response = requests.get(tv_show_url).json()
        logger.debug(f"TMDB Show search response: {tv_show_response}")
        # Check if 'result' key exists in the response
        if 'result' in tv_show_response and 'tvshowdetails' in tv_show_response['result'] and 'uniqueid' in tv_show_response['result']['tvshowdetails'] and 'tmdb' in tv_show_response['result']['tvshowdetails']['uniqueid']:
            tmdb_id = tv_show_response['result']['tvshowdetails']['uniqueid']['tmdb']
            logger.debug("Found uniqueid in tvshowdetails")
    # Check if 'uniqueid' and 'tmdb' keys exist in the info
        elif tv_show_id == -1:
            tmdb_id = get_tmdb_id_for_episode(info)
            logger.debug("Cannot find uniqueid, trying to find tmdb_id via showtitle")
    else:
        if info['type'] == 'movie':
            if 'uniqueid' in info and 'tmdb' in info['uniqueid']:
                tmdb_id = info['uniqueid']['tmdb']
                logger.debug("Found uniqueid in info")
            elif 'uniqueid' not in info or 'tmdb' not in info['uniqueid']:
                tmdb_id = get_tmdb_id_for_movie(info)
                logger.debug("Cannot find uniqueid, trying to find tmdb_id via title")
    logger.debug(f"TMDB ID: {tmdb_id}")
    return tmdb_id

# Function to get the TMDB ID of an episode
def get_tmdb_id_for_episode(info):
    if 'uniqueid' in info and 'tmdb' in info['uniqueid']:
        return info['uniqueid']['tmdb']
    else:
        return get_tmdb_id_for_episode_via_api(info)

# Function to get the TMDB ID of a movie
def get_tmdb_id_for_movie(info):
    if 'uniqueid' in info and 'tmdb' in info['uniqueid']:
        return info['uniqueid']['tmdb']
    else:
        return get_tmdb_id_for_movie_via_api(info)

# Function to get the TMDB ID of a TV show via the TMDB API if the TMDB ID is not available in the info
def get_tmdb_id_for_episode_via_api(info):
    showtitle = quote(info['showtitle'])
    showtitle_url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={showtitle}"
    showtitle_response = requests.get(showtitle_url).json()
    logger.debug(f"TMDB Episode search response: {showtitle_response}")
    if 'results' in showtitle_response and len(showtitle_response['results']) > 0:
        logger.debug(f"TMDB Episode search results: {showtitle_response['results'][0]['id']}")
        return showtitle_response['results'][0]['id']
    return None

# Function to get the TMDB ID of a movie via the TMDB API if the TMDB ID is not available in the info
def get_tmdb_id_for_movie_via_api(info):
    title = quote(info['title'])
    title_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    title_response = requests.get(title_url).json()
    logger.debug(f"TMDB Movie search response: {title_response}")
    if 'results' in title_response and len(title_response['results']) > 0:
        logger.debug(f"TMDB Movie search results: {title_response['results'][0]['id']}")
        return title_response['results'][0]['id']
    return None

# Function to get the Trakt URL of a media
def get_trakt_url(tmdb_id, media_type):
    # Define the base URL
    base_url = "https://trakt.tv/"

    # Check the media type
    if media_type == "movie":
        media_url = base_url + "movies/"
        search_type = "movie"
    elif media_type == "tv":
        media_url = base_url + "shows/"
        search_type = "episode"
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

        # Get the Trakt slug from the first result
        if media_type == "tv":
            trakt_slug = data[0]["show"]["ids"]["slug"]
            season = data[0]["episode"]["season"]
            episode = data[0]["episode"]["number"]
            trakt_url = f"{media_url}{trakt_slug}/seasons/{season}/episodes/{episode}"
        else:
            trakt_slug = data[0][search_type]["ids"]["slug"]
            trakt_url = media_url + trakt_slug

        logger.debug(f"Generated Trakt URL: {trakt_url}")
        return trakt_url
    else:
        logger.error(f"Failed to get Trakt URL: {response.content}")
        return None