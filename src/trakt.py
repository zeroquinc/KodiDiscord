import requests
from urllib.parse import quote

from src.custom_logger import logger
from .globals import TRAKT_API_KEY, TMDB_API_KEY

# Function to get the TMDB ID of a media
def get_tmdb_id_trakt(info, media_type):
    # If the media type is a channel, return None
    if media_type == 'channel':
        return None

    tmdb_id = None
    if info['type'] == 'episode':
        if 'uniqueid' in info and 'tmdb' in info['uniqueid']:
            tmdb_id = info['uniqueid']['tmdb']
            logger.debug("Found uniqueid in info")
        elif 'uniqueid' not in info or 'tmdb' not in info['uniqueid']:
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
    return tmdb_id

# Function to get the TMDB ID of a TV show via the TMDB API if the TMDB ID is not available in the info
def get_tmdb_id_for_episode(info):
    showtitle = quote(info['showtitle'])
    showtitle_url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={showtitle}"
    showtitle_response = requests.get(showtitle_url).json()
    if 'results' in showtitle_response and len(showtitle_response['results']) > 0:
        return showtitle_response['results'][0]['id']
    return None

# Function to get the TMDB ID of a movie via the TMDB API if the TMDB ID is not available in the info
def get_tmdb_id_for_movie(info):
    title = quote(info['title'])
    title_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    title_response = requests.get(title_url).json()
    if 'results' in title_response and len(title_response['results']) > 0:
        return title_response['results'][0]['id']
    return None

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
        logger.error(f"Invalid media type: {media_type}")
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