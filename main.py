import requests
import time
import logging
import os
from pypresence import Presence
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
    info = info['result']['item']
    length = length['result']
    start_time = (datetime.now() - timedelta(hours=length["time"]['hours'], minutes=length["time"]['minutes'], seconds=length["time"]['seconds']))
    end_time = (start_time + timedelta(hours=length['totaltime']['hours'], minutes=length['totaltime']['minutes'], seconds=length['totaltime']['seconds'])).timestamp()
    start_time = start_time.timestamp()
    
    tmdb_id = None
    if info['type'] == 'episode':
        tv_show_id = info['tvshowid']
        tv_show_url = f"http://localhost:{port}/jsonrpc?request={{%22jsonrpc%22:%222.0%22,%22method%22:%22VideoLibrary.GetTVShowDetails%22,%22params%22:{{%22tvshowid%22:{tv_show_id},%22properties%22:[%22uniqueid%22]}},%22id%22:%22libTvShow%22}}"
        tv_show_response = requests.get(tv_show_url).json()
        tmdb_id = tv_show_response['result']['tvshowdetails']['uniqueid']['tmdb']
        media_type = 'tv'
    elif info['type'] == 'movie':
        tmdb_id = info['uniqueid']['tmdb']
        media_type = 'movie'

    # Default stock image URL
    image_url = "https://i.imgur.com/QONOI11.png"

    if tmdb_id:
        # Check if the TMDB ID is in the cache
        if tmdb_id in tmdb_cache:
            image_url = tmdb_cache[tmdb_id]
        else:
            # If not in the cache, make a request to the TMDB API
            tmdb_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}"
            tmdb_response = requests.get(tmdb_url).json()
            if 'poster_path' in tmdb_response and tmdb_response['poster_path']:
                image_url = f"https://image.tmdb.org/t/p/w500{tmdb_response['poster_path']}"
                # Store the image URL in the cache
                tmdb_cache[tmdb_id] = image_url

    if info['type'] == 'movie':
        if length['speed'] == 0:
            RPC.update(details=str(info['title']),
                       state="Paused...",
                       large_image=image_url,
                       large_text='Watching a movie on Kodi',
                       small_image='pause',
                       small_text='Paused')
        else:
            RPC.update(details=str(info['title']),
                       start=start_time,
                       end=end_time,
                       large_image=image_url,
                       large_text='Watching a movie on Kodi',
                       small_image='play',
                       small_text='Playing')

    if info['type'] == "episode":
        season_number = str(info['season']).zfill(2)
        episode_number = str(info['episode']).zfill(2)
        state_info = f'S{season_number}E{episode_number}: {info["title"]}'
        if length['speed'] == 0:
            RPC.update(state=state_info,
                       details=str(info['showtitle']),
                       start=start_time,
                       end=end_time,
                       large_image=image_url,
                       large_text='Watching a TV Show on Kodi',
                       small_image='pause',
                       small_text='Paused')
        else:
            RPC.update(state=state_info,
                       details=str(info['showtitle']),
                       start=start_time,
                       end=end_time,
                       large_image=image_url,
                       large_text='Watching a TV Show on Kodi',
                       small_image='play',
                       small_text='Playing')
            
    if info['type'] == "channel":
        try:
            title = str(info['title'])
            if not title:  # Check if title is empty
                title = 'Not available'
        except KeyError:
            title = 'Not available'
        if length['speed'] == 0:
            RPC.update(state=title,
                       details=str(info['label']),
                       start=start_time,
                       end=end_time,
                       large_image=image_url,
                       large_text='Watching Live TV on Kodi',
                       small_image='pause',
                       small_text='Paused')
        else:
            RPC.update(state=title,
                       details=str(info['label']),
                       start=start_time,
                       end=end_time,
                       large_image=image_url,
                       large_text='Watching Live TV on Kodi',
                       small_image='play',
                       small_text='Playing')

    if info['type'] == 'unknown':
        RPC.clear()

    time.sleep(15)


while True:
    try:
        info = requests.get(url+infourl).json()
        length = requests.get(url+lengthurl).json()
        set_rp(info, length)
    except requests.exceptions.RequestException:
        print("Cant connect to Kodi web interface. Are you sure its running? Is the web interface on?")
        loading("Trying again in 5 seconds")