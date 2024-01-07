import time
import requests
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

# Create dictionaries for caching
tmdb_id_cache = {}
imdb_id_cache = {}
media_type_cache = {}
image_url_cache = {}
imdb_url_cache = {}

""""
The following functions are used to update the RP
"""

# Function to set the RP with the provided info and length
def set_rp(info, length):
    global previous_info, previous_speed
    info = info['result']['item']
    length = length['result']
    if previous_info == info and previous_speed == length['speed']:  # Check if both info and speed are the same as before to prevent unnecessary updates
        return
    start_time = calculate_start_time(length)
    end_time = calculate_end_time(start_time, length)
    media_type = get_media_type(info)
    trakt_url, tmdb_url, imdb_url, letterboxd_url, image_url = get_urls(info, media_type)
    
    if info['type'] == 'movie':
        # If the media type is a movie, update the RP accordingly
        update_rpc_movie(info, length, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url)
    elif info['type'] == 'episode':
        # If the media type is an episode, update the RP accordingly
        update_rpc_episode(info, length, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url)
    elif info['type'] == 'channel':
        # If the media type is a channel, update the RP accordingly
        update_rpc_channel(info, length, start_time, end_time, image_url)
    elif info['type'] == 'unknown' and length['speed'] == 0:
        # If nothing is playing, log an info message and clear the RP
        logger.info("Nothing is playing. Clearing RPC...")
        RPC.clear()

    previous_info = info
    previous_speed = length['speed']
    
    # Log the current time and total time for debugging
    logger.debug(f"Current time: {length['time']}")
    logger.debug(f"Total time: {length['totaltime']}")

def get_urls(info, media_type):
    trakt_url = None
    tmdb_url = None
    imdb_url = None
    letterboxd_url = None
    image_url = DEFAULT_POSTER_URL # We set the default poster URL in case we can't get the image URL or if TMDB_THUMBNAIL_ENABLED is False
    
    """"
    The following if statements are used to get the URLs for the buttons and thumbnail
    """
    
    # We don't need thumbnail or buttons for channels
    if TMDB_THUMBNAIL_ENABLED and media_type != 'channel':
        tmdb_id_tmdb = get_tmdb_id_tmdb(info, media_type)
        tmdb_url = get_tmdb_url(tmdb_id_tmdb, media_type)
        image_url = get_image_url(tmdb_id_tmdb, media_type)
        logger.debug(f"TMDB Thumbnail URL: {image_url}")
    if IMDB_BUTTON_ENABLED and media_type != 'channel':
        imdb_id = get_imdb_id(info)
        imdb_url = get_imdb_url(imdb_id)
    if TMDB_BUTTON_ENABLED and media_type != 'channel':
        tmdb_id = get_tmdb_id_tmdb(info, media_type)
        tmdb_url = get_tmdb_url(tmdb_id, media_type)
        logger.debug(f"TMDB Button URL: {tmdb_url}")
    if TRAKT_BUTTON_ENABLED and media_type != 'channel':
        tmdb_id_trakt = get_tmdb_id_trakt(info, media_type)
        trakt_url = get_trakt_url(tmdb_id_trakt, media_type)
        logger.debug(f"Trakt Button URL: {trakt_url}")
    if LETTERBOXD_BUTTON_ENABLED and media_type != 'channel':
        tmdb_id = get_tmdb_id_tmdb(info, media_type)
        letterboxd_url = get_letterboxd_url(tmdb_id)
        logger.debug(f"Letterboxd Button URL: {letterboxd_url}")
    
    return trakt_url, tmdb_url, imdb_url, letterboxd_url, image_url

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
The following functions are used to calculate the start and end time of a media
"""

# Function to calculate the start time of a media
def calculate_start_time(length):
    return (datetime.now() - timedelta(hours=length["time"]['hours'], minutes=length["time"]['minutes'], seconds=length["time"]['seconds'])).timestamp()

# Function to calculate the end time of a media
def calculate_end_time(start_time, length):
    start_time = datetime.fromtimestamp(start_time)
    return (start_time + timedelta(hours=length['totaltime']['hours'], minutes=length['totaltime']['minutes'], seconds=length['totaltime']['seconds'])).timestamp()

"""
The following functions are used to get the state info and title of a media
"""

# Function to get the state info of a media
def get_state_info(info):
    if 'season' in info and info['season'] and 'episode' in info and info['episode']:
        season_number = str(info['season']).zfill(2)
        episode_number = str(info['episode']).zfill(2)
        return f'S{season_number}E{episode_number}: {info["title"]}'
    else:
        return info["title"]

# Function to get the title of a media
def get_title(info):
    try:
        title = str(info['title'])
        if not title:
            title = 'Unknown'
    except KeyError:
        title = 'Unknown'
    return title

# Function to get the director state of a media
def get_director_state(info):
    director = ', '.join(info['director'])
    return f"{director}"

# Function to get the genres state of a media
def get_genres_state(info):
    genres = ', '.join(info['genre'])
    return f"{genres}"

# Function to create the buttons for a media
def create_buttons(imdb_url, letterboxd_url, tmdb_url, trakt_url):
    buttons = []
    if IMDB_BUTTON_ENABLED and imdb_url is not None:
        buttons.append({"label": "IMDb", "url": imdb_url})

    if LETTERBOXD_BUTTON_ENABLED and letterboxd_url is not None:
        buttons.append({"label": "Letterboxd", "url": letterboxd_url})

    if len(buttons) < 2 and TRAKT_BUTTON_ENABLED and tmdb_url is not None:
        buttons.append({"label": "Trakt", "url": trakt_url})

    if len(buttons) < 2 and TMDB_BUTTON_ENABLED and tmdb_url is not None:
        buttons.append({"label": "TMDb", "url": tmdb_url})

    return buttons

# Function to limit the buttons for a media to 2 because of Discord's Rich Presence limit
def limit_buttons(buttons):
    buttons.sort(key=len, reverse=True)
    return buttons[:2]

"""
The following functions check the speed and time of the media and sends the info to the appropriate function
"""

# Function to update the RP for a movie
def update_rpc_movie(info, length, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url):
    if length['speed'] == 0:
        # If the movie is paused, update the RP accordingly
        update_rpc_paused_movie(info, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url)
    else:
        # If the movie is playing, update the RP accordingly
        update_rpc_playing_movie(info, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url)

# Function to update the RP for an episode
def update_rpc_episode(info, length, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url):
    if length['speed'] == 0:
        # If the episode is paused, update the RP accordingly
        update_rpc_paused_episode(info, image_url, imdb_url, tmdb_url, trakt_url)
    else:
        # If the episode is playing, update the RP accordingly
        update_rpc_playing_episode(info, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url)

# Function to update the RP for a channel
def update_rpc_channel(info, length, start_time, end_time, image_url):
    if length['speed'] == 0:
        # If the channel is paused, update the RP accordingly
        update_rpc_paused_channel(info, image_url)
    elif length['time']['hours'] == 0 and length['time']['minutes'] == 0 and length['time']['seconds'] == 0 and length['totaltime']['hours'] == 0 and length['totaltime']['minutes'] == 0 and length['totaltime']['seconds'] == 0:
        # If start_time and end_time are both zero, update the RP without them, for EPG without information about start and end time
        update_rpc_playing_channel_without_time(info, image_url)
    else:
        # If the channel is playing, update the RP accordingly
        update_rpc_playing_channel(info, start_time, end_time, image_url)

"""	
The following functions update the RP based on the type of media (movie, episode, channel) and whether it's playing or paused
"""

# Function to update the RP when a movie is paused
def update_rpc_paused_movie(info, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url):
    logger.info(f"{UPDATED_RPC} - Paused Movie:")
    logger.info(f"{info['title']}")
    
    large_image = image_url
    
    if TMDB_THUMBNAIL_ENABLED and image_url is not None:
        large_image = image_url
    
    buttons = create_buttons(imdb_url, letterboxd_url, tmdb_url, trakt_url)
    buttons = limit_buttons(buttons)
    
    rpc_params = {
        "details": str(info['title']) + ' (' + str(info['year']) + ')',
        "state": "Paused...",
        "large_image": large_image,
        "large_text": MOVIE_LARGE_TEXT,
        "small_image": 'pause',
        "small_text": 'Paused'
    }
    
    if buttons:
        rpc_params["buttons"] = buttons

    RPC.update(**rpc_params)

# Function to update the RP when a movie is playing
def update_rpc_playing_movie(info, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url):
    logger.info(f"{UPDATED_RPC} - Playing Movie:")
    logger.info(f"{info['title']}")
    
    large_image = image_url
    
    if TMDB_THUMBNAIL_ENABLED and image_url is not None:
        large_image = image_url
    
    buttons = create_buttons(imdb_url, letterboxd_url, tmdb_url, trakt_url)
    buttons = limit_buttons(buttons)
    
    rpc_params = {
        "details": str(info['title']) + ' (' + str(info['year']) + ')',
        "large_image": large_image,
        "large_text": MOVIE_LARGE_TEXT,
        "small_image": 'play',
        "small_text": 'Playing'
    }
    
    if TIME_REMAINING_RPC_ENABLED:
        rpc_params["start"] = start_time
        rpc_params["end"] = end_time

    if DIRECTOR_ENABLED and 'director' in info and info['director'] is not None and GENRES_ENABLED is False:
        rpc_params["state"] = get_director_state(info)
    
    if GENRES_ENABLED and 'genre' in info and info['genre'] is not None and DIRECTOR_ENABLED is False:
        rpc_params["state"] = get_genres_state(info)
    
    if buttons:
        rpc_params["buttons"] = buttons

    RPC.update(**rpc_params)

# Function to update the RP when an episode is paused
def update_rpc_paused_episode(info, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url=None):
    state_info = get_state_info(info)
    logger.info(f"{UPDATED_RPC} - Paused Episode:")
    logger.info(f"{info['showtitle']}")
    logger.info(f"{state_info}")
    
    large_image = image_url

    if TMDB_THUMBNAIL_ENABLED and image_url is not None:
        large_image = image_url
    
    buttons = create_buttons(imdb_url, letterboxd_url, tmdb_url, trakt_url)
    buttons = limit_buttons(buttons)
    
    rpc_params = {
        "state": state_info,
        "details": str(info['showtitle']),
        "large_image": large_image,
        "large_text": EPISODE_LARGE_TEXT,
        "small_image": 'pause',
        "small_text": 'Paused'
    }
    
    if buttons:
        rpc_params["buttons"] = buttons

    RPC.update(**rpc_params)

# Function to update the RP when an episode is playing
def update_rpc_playing_episode(info, start_time, end_time, image_url, imdb_url, tmdb_url, trakt_url, letterboxd_url=None):
    state_info = get_state_info(info)
    logger.info(f"{UPDATED_RPC} - Playing Episode:")
    logger.info(f"{info['showtitle']}")
    logger.info(f"{state_info}")
    
    large_image = image_url
    
    if TMDB_THUMBNAIL_ENABLED and image_url is not None:
        large_image = image_url
        
    buttons = create_buttons(imdb_url, letterboxd_url, tmdb_url, trakt_url)
    buttons = limit_buttons(buttons)
    
    rpc_params = {
        "state": state_info,
        "details": str(info['showtitle']),
        "large_image": large_image,
        "large_text": EPISODE_LARGE_TEXT,
        "small_image": 'play',
        "small_text": 'Playing'
    }
    
    if TIME_REMAINING_RPC_ENABLED:
        rpc_params["start"] = start_time
        rpc_params["end"] = end_time
    
    if buttons:
        rpc_params["buttons"] = buttons

    RPC.update(**rpc_params)

# Function to update the RP when a channel is paused
def update_rpc_paused_channel(info, image_url):
    title = get_title(info)
    logger.info(f"{UPDATED_RPC} - Paused Channel:")
    logger.info(f"{info['label']}")
    
    rpc_params = {
        "state": title,
        "details": str(info['label']),
        "large_image": image_url,
        "large_text": LIVETV_LARGE_TEXT,
        "small_image": 'pause',
        "small_text": 'Paused'
    }
    
    RPC.update(**rpc_params)

# Function to update the RP when a channel is playing
def update_rpc_playing_channel(info, start_time, end_time, image_url):
    title = get_title(info)
    logger.info(f"{UPDATED_RPC} - Playing Channel:")
    logger.info(f"{info['label']}")
    
    rpc_params = {
        "state": title,
        "details": str(info['label']),
        "large_image": image_url,
        "large_text": LIVETV_LARGE_TEXT,
        "small_image": 'play',
        "small_text": 'Playing'
    }
    
    if TIME_REMAINING_RPC_ENABLED:
        rpc_params["start"] = start_time
        rpc_params["end"] = end_time
    
    RPC.update(**rpc_params)
    
# Function to update the RP when a channel is playing without start and end time
def update_rpc_playing_channel_without_time(info, image_url):
    title = get_title(info)
    logger.info(f"{UPDATED_RPC} - Playing Channel:")
    logger.info(f"{info['label']}")
    
    rpc_params = {
        "state": title,
        "details": str(info['label']),
        "large_image": image_url,
        "large_text": LIVETV_LARGE_TEXT,
        "small_image": 'play',
        "small_text": 'Playing'
    }
    
    RPC.update(**rpc_params)