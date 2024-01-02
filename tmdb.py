import requests
from globals import TMDB_API_KEY, port

tmdb_cache = {}

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