import time
import requests
import json
from pypresence.exceptions import PipeClosed
from datetime import datetime, timedelta

from config import (
    IMDB_BUTTON_ENABLED, 
    TMDB_BUTTON_ENABLED, 
    TRAKT_BUTTON_ENABLED, 
    LETTERBOXD_BUTTON_ENABLED, 
    TIME_REMAINING_RPC_ENABLED, 
    TMDB_THUMBNAIL_ENABLED, 
    DIRECTOR_ENABLED, 
    GENRES_ENABLED, 
    LIVETV_LARGE_TEXT, 
    EPISODE_LARGE_TEXT, 
    MOVIE_LARGE_TEXT, 
    DEFAULT_POSTER_URL
)

from .globals import (
    RPC, 
    INFO_URL, 
    LENGTH_URL, 
    UPDATED_RPC
)

from .custom_logger import logger
from .imdb import get_imdb_id, get_imdb_url
from .tmdb import get_tmdb_id_tmdb, get_media_type, get_image_url, get_tmdb_url
from .trakt import get_trakt_url, get_tmdb_id_trakt
from .letterboxd import get_letterboxd_url

""""
The following variables are used to prevent unnecessary updates to the RP
"""

# Initialize global variables
result = None
previous_info = None
session = requests.Session()
large_text_map = {
    "channel": LIVETV_LARGE_TEXT,
    "episode": EPISODE_LARGE_TEXT,
    "movie": MOVIE_LARGE_TEXT
}

# Initialize the cache
cache = {}

"""
The following functions are used to update the RP with the provided info and length
"""

# Function to update the Rich Presence (RP) with the provided info and length
def update_rp(info, length):
    try:
        # Set the RP with the provided info and length
        set_rp(info, length)
    except PipeClosed:
        # If the connection to Discord is lost, log an info message and attempt to reconnect
        logger.info("Connection to Discord lost. Attempting to reconnect...")
        RPC.connect()
        
"""
The following functions are used to fetch information from a session
"""

# Function to fetch information from a session
def fetch_info(session):
    while True:  # Retry indefinitely
        try:
            # Return the JSON response from the session's INFO_URL
            response = session.get(INFO_URL).json()
            return response
        except requests.exceptions.RequestException as e:
            # Log an error message if there's a connection issue and wait for an exponentially increasing amount of time before the next attempt
            logger.error(f"Can't connect to Kodi web interface: {e}. Are you sure it's running? Is the web interface on?")
            time.sleep(2)  # Wait for 2 seconds before the next attempt

# Function to fetch the length of a session
def fetch_length(session):
    while True:  # Retry indefinitely
        try:
            # Return the JSON response from the session's LENGTH_URL
            response = session.get(LENGTH_URL).json()
            return response
        except requests.exceptions.RequestException as e:
            # Log an error message if there's a connection issue and wait for an exponentially increasing amount of time before the next attempt
            logger.error(f"Can't connect to Kodi web interface: {e}. Are you sure it's running? Is the web interface on?")
            time.sleep(2)  # Wait for 2 seconds before the next attempt

""""
The following functions are used to update the RP
"""

# Function to set the RP with the provided info and length
def set_rp(info, length):
    global previous_info, previous_speed, cache
    # Initialize start_time with a default value
    start_time, end_time = None, None
    # Check if 'result' and 'item' keys exist in the info and 'result' and 'speed' keys exist in the length to prevent errors
    if 'result' in info and 'item' in info['result']:
        info = info['result']['item']
    else:
        logger.error("Key 'result' or 'item' not found in info")
        return
    if 'result' in length and 'speed' in length['result']:
        length = length['result']
    else:
        logger.error("Key 'result' or 'speed' not found in length")
        return
    if previous_info == info and previous_speed == length['speed']:  # Check if both info and speed are the same as before to prevent unnecessary updates
        return

    # Create a key for the cache
    cache_key = json.dumps(info, sort_keys=True)

    # If the key is in the cache, use the cached values
    if cache_key in cache:
        media_type, urls = cache[cache_key]
        trakt_url, tmdb_url, imdb_url, letterboxd_url, image_url = urls
        logger.debug(f"Retrieved cached values for {cache_key}: media_type={media_type}, urls={urls}")
    else:
        # Otherwise, calculate the values and store them in the cache
        media_type = get_media_type(info)
        urls = get_urls(info, media_type)
        trakt_url, tmdb_url, imdb_url, letterboxd_url, image_url = urls

        cache[cache_key] = (media_type, urls)
        logger.debug(f"Cached values for {cache_key}: media_type={media_type}, urls={urls}")

    # Calculate start_time and end_time outside the cache check, as they are not being cached, but only if the media is playing
    if length['speed'] != 0:
        start_time = calculate_start_time(length)
        end_time = calculate_end_time(start_time, length)
        logger.debug(f"Calculated start_time={start_time} and end_time={end_time}")

    update_rpc_mediatype(info, length, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url)

    previous_info = info
    previous_speed = length['speed']
    
# Function to update the RP based on the media type
def update_rpc_mediatype(info, length, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url):
    media_type_functions = {
        'movie': update_rpc_movie,
        'episode': update_rpc_episode,
        'channel': update_rpc_channel,
        'unknown': clear_rpc_if_unknown
    }

    media_type = info['type']
    if media_type in media_type_functions:
        media_type_functions[media_type](info, length, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url)
    else:
        logger.info("Media type is not recognized. Clearing RPC...")
        RPC.clear()

# Function to clear the RP if nothing is playing or if the media type is unknown
def clear_rpc_if_unknown(info, length, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url):
    if length['speed'] == 0:
        # If nothing is playing, log an info message and clear the RP
        logger.info("Nothing is playing. Clearing RPC...")
        RPC.clear()
    else:
        # If something is playing but the media type is unknown, log an info message and clear the RP
        logger.info("Something is playing but the media type is unknown. Clearing RPC...")
        RPC.clear()

# Function to update the RP for a movie
def update_rpc_movie(info, length, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url):
    is_playing = length['speed'] != 0
    update_rpc(info, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url, 'movie', is_playing)

# Function to update the RP for an episode
def update_rpc_episode(info, length, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url=None):
    is_playing = length['speed'] != 0
    update_rpc(info, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, None, 'episode', is_playing)

# Function to update the RP for a channel
def update_rpc_channel(info, length, start_time, end_time, image_url, *_):
    is_playing = length['speed'] != 0
    update_rpc(info, start_time, end_time, image_url, None, None, None, None, 'channel', is_playing)

# Function to update the RP
def update_rpc(info, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url, media_type, is_playing):
    logger.info(f"{UPDATED_RPC} - {'Playing' if is_playing else 'Paused'} {media_type.capitalize()}:")
    logger.info(f"{info['title']}")

    buttons = create_buttons(imdb_url, letterboxd_url, tmdb_url, trakt_url)

    rpc_params = {
        "details": str(info['label']) if media_type == 'channel' else (str(info['title']) + ' (' + str(info['year']) + ')' if media_type == 'movie' else str(info['showtitle']) if media_type == 'episode' else str(info['title'])),
        "state": str(info['title']) if media_type == 'channel' else ("Playing" if is_playing else "Paused"),
        "large_image": image_url,
        "large_text": large_text_map.get(media_type.lower(), "Default Large Text"),
        "small_image": 'play' if is_playing else 'pause',
        "small_text": 'Playing' if is_playing else 'Paused'
    }

    if buttons:
        rpc_params["buttons"] = buttons

    if TIME_REMAINING_RPC_ENABLED and is_playing and start_time is not None and end_time is not None:
        rpc_params["start"] = start_time
        rpc_params["end"] = end_time

    if media_type == 'episode':
        if 'season' in info and info['season'] and 'episode' in info and info['episode']:
            season_number = str(info['season']).zfill(2)
            episode_number = str(info['episode']).zfill(2)
            rpc_params["state"] = f'S{season_number}E{episode_number}: {info["title"]}'
        else:
            rpc_params["state"] = info["title"]

    if media_type == 'movie' and is_playing:
        if DIRECTOR_ENABLED and 'director' in info and info['director'] is not None and GENRES_ENABLED is False:
            director = ', '.join(info['director'])
            rpc_params["state"] = f"{director}"
        if GENRES_ENABLED and 'genre' in info and info['genre'] is not None and DIRECTOR_ENABLED is False:
            genres = ', '.join(info['genre'])
            rpc_params["state"] = f"{genres}"

    RPC.update(**rpc_params)
    
"""
Start and end time calculations, button creation, URL fetching
"""

# Function to calculate the start time of a media
def calculate_start_time(length):
    return (datetime.now() - timedelta(hours=length["time"]['hours'], minutes=length["time"]['minutes'], seconds=length["time"]['seconds'])).timestamp()

# Function to calculate the end time of a media
def calculate_end_time(start_time, length):
    start_time = datetime.fromtimestamp(start_time)
    return (start_time + timedelta(hours=length['totaltime']['hours'], minutes=length['totaltime']['minutes'], seconds=length['totaltime']['seconds'])).timestamp()

# Function to create the buttons for a media
def create_buttons(imdb_url, letterboxd_url, tmdb_url, trakt_url):
    buttons = []
    button_data = [
        (IMDB_BUTTON_ENABLED, imdb_url, "IMDb"),
        (LETTERBOXD_BUTTON_ENABLED, letterboxd_url, "Letterboxd"),
        (TRAKT_BUTTON_ENABLED, trakt_url, "Trakt"),
        (TMDB_BUTTON_ENABLED, tmdb_url, "TMDb")
    ]

    for button_enabled, url, label in button_data:
        if button_enabled and url is not None and len(buttons) < 2:
            buttons.append({"label": label, "url": url})

    # Function to limit the buttons for a media to 2 because of Discord's Rich Presence limit
    def limit_buttons(buttons):
        buttons.sort(key=len, reverse=True)
        return buttons[:2]

    return limit_buttons(buttons)

# Function to get the URLs for a media
def get_urls(info, media_type):
    trakt_url = None
    tmdb_url = None
    imdb_url = None
    letterboxd_url = None
    image_url = DEFAULT_POSTER_URL # We set the default poster URL in case we can't get the image URL or if TMDB_THUMBNAIL_ENABLED is False
    
    # We don't need thumbnail or buttons for channels
    if media_type != 'channel':
        tmdb_id = get_tmdb_id_tmdb(info, media_type)
        
        if TMDB_THUMBNAIL_ENABLED:
            tmdb_url = get_tmdb_url(tmdb_id, media_type)
            image_url = get_image_url(tmdb_id, media_type)
        if IMDB_BUTTON_ENABLED:
            imdb_id = get_imdb_id(info)
            imdb_url = get_imdb_url(imdb_id)
        if TMDB_BUTTON_ENABLED:
            tmdb_url = get_tmdb_url(tmdb_id, media_type)
        if TRAKT_BUTTON_ENABLED:
            tmdb_id_trakt = get_tmdb_id_trakt(info, media_type)
            trakt_url = get_trakt_url(tmdb_id_trakt, media_type)
        if LETTERBOXD_BUTTON_ENABLED:
            letterboxd_url = get_letterboxd_url(tmdb_id)
    
    return trakt_url, tmdb_url, imdb_url, letterboxd_url, image_url