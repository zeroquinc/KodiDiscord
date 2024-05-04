import requests
from .custom_logger import logger
from .globals import TRAKT_API_KEY

def get_tmdb_id_trakt(info, media_type):
    if media_type == 'channel':
        return None

    tmdb_id = get_tmdb_id_for_media(info) if info['type'] in ('episode', 'movie') else None
    logger.debug(f"TMDB ID: {tmdb_id}")
    return tmdb_id

def get_tmdb_id_for_media(info):
    tmdb_id = info.get('uniqueid', {}).get('tmdb')
    logger.debug(f"{'Found' if tmdb_id else 'Can\'t find'} TMDB ID in uniqueid")
    return tmdb_id

def get_trakt_url(tmdb_id, media_type):
    if tmdb_id is None:
        return None

    media_urls = {"movie": "movies/", "tv": "shows/"}
    search_types = {"movie": "movie", "tv": "show"}

    media_url = f"https://trakt.tv/{media_urls.get(media_type)}"
    search_type = search_types.get(media_type)

    if not media_url or not search_type:
        return None

    search_url = f"https://api.trakt.tv/search/tmdb/{tmdb_id}?type={search_type}"
    headers = {"trakt-api-key": TRAKT_API_KEY}
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        return trakt_url(response, search_type, media_url)
    logger.error(f"Failed to get Trakt URL: {response.content}")
    return None

def trakt_url(response, search_type, media_url):
    data = response.json()
    logger.debug(f"Trakt search response: {data}")
    trakt_slug = data[0][search_type]["ids"]["slug"]
    trakt_url = media_url + trakt_slug
    logger.debug(f"Generated Trakt URL: {trakt_url}")
    return trakt_url