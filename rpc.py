import time
import requests
from globals import RPC
from tmdb import get_tmdb_id, get_media_type, get_image_url
from globals import RPC, INFO_URL, LENGTH_URL
from pypresence.exceptions import PipeClosed
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

result = None
previous_info = None

def fetch_info(session):
    try:
        return session.get(INFO_URL).json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Can't connect to Kodi web interface: {e}. Are you sure it's running? Is the web interface on?")
        time.sleep(60)

def fetch_length(session):
    try:
        return session.get(LENGTH_URL).json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Can't connect to Kodi web interface: {e}. Are you sure it's running? Is the web interface on?")
        time.sleep(60)

def update_rp(info, length):
    try:
        set_rp(info, length)
    except PipeClosed:
        logging.info("Connection to Discord lost. Attempting to reconnect...")
        RPC.connect()

def update_rpc_movie(info, length, start_time, end_time, image_url):
    if length['speed'] == 0:
        update_rpc_paused_movie(info, image_url)
    else:
        update_rpc_playing_movie(info, start_time, end_time, image_url)

def update_rpc_episode(info, length, start_time, end_time, image_url):
    if length['speed'] == 0:
        update_rpc_paused_episode(info, image_url)
    else:
        update_rpc_playing_episode(info, start_time, end_time, image_url)

def update_rpc_channel(info, length, start_time, end_time, image_url):
    if length['speed'] == 0:
        update_rpc_paused_channel(info, image_url)
    else:
        update_rpc_playing_channel(info, start_time, end_time, image_url)

def update_rpc_paused_movie(info, image_url):
    logging.info(f"Updated RPC - Paused movie \n{info['title']}")
    RPC.update(details=str(info['title']),
               state="Paused...",
               large_image=image_url,
               large_text='Watching a movie on Kodi',
               small_image='pause',
               small_text='Paused')

def update_rpc_playing_movie(info, start_time, end_time, image_url):
    logging.info(f"Updated RPC - Playing movie \n{info['title']}")
    RPC.update(details=str(info['title']),
               start=start_time,
               end=end_time,
               large_image=image_url,
               large_text='Watching a movie on Kodi',
               small_image='play',
               small_text='Playing')

def update_rpc_paused_episode(info, image_url):
    state_info = get_state_info(info)
    logging.info(f"Updated RPC - Paused episode \n{info['showtitle']} {state_info}")
    RPC.update(state=state_info,
               details=str(info['showtitle']),
               large_image=image_url,
               large_text='Watching a TV Show on Kodi',
               small_image='pause',
               small_text='Paused')

def update_rpc_playing_episode(info, start_time, end_time, image_url):
    state_info = get_state_info(info)
    logging.info(f"Updated RPC - Playing episode \n{info['showtitle']} {state_info}")
    RPC.update(state=state_info,
               details=str(info['showtitle']),
               start=start_time,
               end=end_time,
               large_image=image_url,
               large_text='Watching a TV Show on Kodi',
               small_image='play',
               small_text='Playing')

def update_rpc_paused_channel(info, image_url):
    title = get_title(info)
    logging.info(f"Updated RPC - Paused channel \n{info['label']}")
    RPC.update(state=title,
               details=str(info['label']),
               large_image=image_url,
               large_text='Watching Live TV on Kodi',
               small_image='pause',
               small_text='Paused')

def update_rpc_playing_channel(info, start_time, end_time, image_url):
    title = get_title(info)
    logging.info(f"Updated RPC - Playing channel \n{info['label']}")
    RPC.update(state=title,
               details=str(info['label']),
               start=start_time,
               end=end_time,
               large_image=image_url,
               large_text='Watching Live TV on Kodi',
               small_image='play',
               small_text='Playing')
    
def set_rp(info, length):
    global previous_info, previous_speed
    info = info['result']['item']
    length = length['result']
    if previous_info == info and previous_speed == length['speed']:  # Check if both info and speed are the same as before
        return
    start_time = calculate_start_time(length)
    end_time = calculate_end_time(start_time, length)
    
    tmdb_id = get_tmdb_id(info)
    media_type = get_media_type(info)
    image_url = get_image_url(tmdb_id, media_type)

    if info['type'] == 'movie':
        update_rpc_movie(info, length, start_time, end_time, image_url)
    elif info['type'] == 'episode':
        update_rpc_episode(info, length, start_time, end_time, image_url)
    elif info['type'] == 'channel':
        update_rpc_channel(info, length, start_time, end_time, image_url)
    elif info['type'] == 'unknown' and length['speed'] == 0:
        logging.info("Nothing is playing. Clearing RPC...")
        RPC.clear()

    previous_info = info
    previous_speed = length['speed']

    time.sleep(15)

def calculate_start_time(length):
    return (datetime.now() - timedelta(hours=length["time"]['hours'], minutes=length["time"]['minutes'], seconds=length["time"]['seconds'])).timestamp()

def calculate_end_time(start_time, length):
    start_time = datetime.fromtimestamp(start_time)
    return (start_time + timedelta(hours=length['totaltime']['hours'], minutes=length['totaltime']['minutes'], seconds=length['totaltime']['seconds'])).timestamp()

def get_state_info(info):
    season_number = str(info['season']).zfill(2)
    episode_number = str(info['episode']).zfill(2)
    return f'S{season_number}E{episode_number}: {info["title"]}'

def get_title(info):
    try:
        title = str(info['title'])
        if not title:
            title = 'Not available'
    except KeyError:
        title = 'Not available'
    return title