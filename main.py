import requests
import time
import logging
import os
from pypresence import Presence
from pypresence.exceptions import PipeClosed
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

client_id = '1190792021263265912'
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
RPC = Presence(client_id)
RPC.connect()
port = 8080
url = f"http://localhost:{port}/jsonrpc"
infourl = "?request={%20%22jsonrpc%22:%20%222.0%22,%20%22method%22:%20%22Player.GetItem%22,%20%22params%22:%20{%20%22properties%22:%20[%20%22title%22,%20%22season%22,%20%22episode%22,%20%22duration%22,%20%22showtitle%22,%20%22tvshowid%22],%20%22playerid%22:%201%20},%20%22id%22:%20%22VideoGetItem%22%20}"
lengthurl = "?request={%22jsonrpc%22:%222.0%22,%22method%22:%22Player.GetProperties%22,%22params%22:{%22playerid%22:1,%22properties%22:[%22speed%22,%22time%22,%22totaltime%22]},%22id%22:%221%22}"
result = None
previous_info = None
tmdb_cache = {}

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def loading(string):
    for x in range(0, 6):
        b = string + "." * x
        print(b, end="\r")
        time.sleep(1)


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
        if length['speed'] == 0:
            print(f"Updated RPC - Paused movie \n{info['title']}")
            RPC.update(details=str(info['title']),
                       state="Paused...",
                       large_image=image_url,
                       large_text='Watching a movie on Kodi',
                       small_image='pause',
                       small_text='Paused')
        else:
            print(f"Updated RPC - Playing movie \n{info['title']}")
            RPC.update(details=str(info['title']),
                       start=start_time,
                       end=end_time,
                       large_image=image_url,
                       large_text='Watching a movie on Kodi',
                       small_image='play',
                       small_text='Playing')
        previous_info = info
        previous_speed = length['speed']

    if info['type'] == "episode":
        state_info = get_state_info(info)
        if length['speed'] == 0:
            print(f"Updated RPC - Paused episode \n{info['showtitle']} {state_info}")
            RPC.update(state=state_info,
                       details=str(info['showtitle']),
                       large_image=image_url,
                       large_text='Watching a TV Show on Kodi',
                       small_image='pause',
                       small_text='Paused')
        else:
            print(f"Updated RPC - Playing episode \n{info['showtitle']} {state_info}")
            RPC.update(state=state_info,
                       details=str(info['showtitle']),
                       start=start_time,
                       end=end_time,
                       large_image=image_url,
                       large_text='Watching a TV Show on Kodi',
                       small_image='play',
                       small_text='Playing')
        previous_info = info
        previous_speed = length['speed']
            
    if info['type'] == "channel":
        title = get_title(info)
        if length['speed'] == 0:
            print(f"Updated RPC - Paused channel \n{info['label']}")
            RPC.update(state=title,
                       details=str(info['label']),
                       large_image=image_url,
                       large_text='Watching Live TV on Kodi',
                       small_image='pause',
                       small_text='Paused')
        else:
            print(f"Updated RPC - Playing channel \n{info['label']}")
            RPC.update(state=title,
                       details=str(info['label']),
                       start=start_time,
                       end=end_time,
                       large_image=image_url,
                       large_text='Watching Live TV on Kodi',
                       small_image='play',
                       small_text='Playing')
        previous_info = info
        previous_speed = length['speed']

    if info['type'] == 'unknown':
        print("Cleared RPC")
        RPC.clear()

    time.sleep(15)

def calculate_start_time(length):
    return (datetime.now() - timedelta(hours=length["time"]['hours'], minutes=length["time"]['minutes'], seconds=length["time"]['seconds'])).timestamp()

def calculate_end_time(start_time, length):
    start_time = datetime.fromtimestamp(start_time)
    return (start_time + timedelta(hours=length['totaltime']['hours'], minutes=length['totaltime']['minutes'], seconds=length['totaltime']['seconds'])).timestamp()

def get_tmdb_id(info):
    tmdb_id = None
    if info['type'] == 'episode':
        tv_show_id = info['tvshowid']
        tv_show_url = f"http://localhost:{port}/jsonrpc?request={{%22jsonrpc%22:%222.0%22,%22method%22:%22VideoLibrary.GetTVShowDetails%22,%22params%22:{{%22tvshowid%22:{tv_show_id},%22properties%22:[%22uniqueid%22]}},%22id%22:%22libTvShow%22}}"
        tv_show_response = requests.get(tv_show_url).json()
        tmdb_id = tv_show_response['result']['tvshowdetails']['uniqueid']['tmdb']
    elif info['type'] == 'movie':
        tmdb_id = info['uniqueid']['tmdb']
    return tmdb_id

def get_media_type(info):
    if info['type'] == 'episode':
        return 'tv'
    elif info['type'] == 'movie':
        return 'movie'

def get_image_url(tmdb_id, media_type):
    image_url = "https://i.imgur.com/QONOI11.png"
    if tmdb_id:
        if tmdb_id in tmdb_cache:
            image_url = tmdb_cache[tmdb_id]
        else:
            tmdb_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}"
            tmdb_response = requests.get(tmdb_url).json()
            if 'poster_path' in tmdb_response and tmdb_response['poster_path']:
                image_url = f"https://image.tmdb.org/t/p/w500{tmdb_response['poster_path']}"
                tmdb_cache[tmdb_id] = image_url
    return image_url

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

try:
    while True:
        try:
            info = requests.get(url+infourl).json()
            length = requests.get(url+lengthurl).json()
            try:
                set_rp(info, length)
            except PipeClosed:
                print("Connection to Discord lost. Attempting to reconnect...")
                RPC.connect()
        except requests.exceptions.RequestException as e:
            print(f"Can't connect to Kodi web interface: {e}. Are you sure it's running? Is the web interface on?")
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)
except KeyboardInterrupt:
    print("Program interrupted by user. Exiting...")