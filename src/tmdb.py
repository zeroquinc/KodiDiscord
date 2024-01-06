import requests
from urllib.parse import quote

from .globals import TMDB_API_KEY, port

"""
This file contains functions to fetch data from the TMDB API.
"""

# Function to get the media type of a media
def get_media_type(info):
    if info['type'] == 'episode':
        # If the media type is an episode, return 'tv', this is necessary because the TMDB API uses 'tv' for TV shows and Kodi uses 'episode' for TV shows
        return 'tv'
    elif info['type'] == 'movie':
        # If the media type is a movie, return 'movie'
        return 'movie'

# Function to get the TMDB ID of a media
def get_tmdb_id(info):
    tmdb_id = None
    # Check if 'uniqueid' and 'tmdb' keys exist in the info
    if 'uniqueid' in info and 'tmdb' in info['uniqueid']:
        tmdb_id = info['uniqueid']['tmdb']
    else:
        if info['type'] == 'episode':
            tmdb_id = get_tmdb_id_for_episode(info)
        elif info['type'] == 'movie':
            tmdb_id = get_tmdb_id_for_movie(info)
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

# Function to get the IMDb ID of a media
def get_imdb_id(info):
    imdb_id = None
    # Check if 'uniqueid' and 'imdb' keys exist in the info
    if 'uniqueid' in info and 'imdb' in info['uniqueid']:
        imdb_id = info['uniqueid']['imdb']
    return imdb_id

# Function to get the image URL of a media
def get_image_url(tmdb_id, media_type):
    # Default image URL
    image_url = "https://i.imgur.com/QONOI11.png"
    if tmdb_id:
        # Fetch the image URL from the TMDB API
        tmdb_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}"
        tmdb_response = requests.get(tmdb_url).json()
        if 'poster_path' in tmdb_response and tmdb_response['poster_path']:
            image_url = f"https://image.tmdb.org/t/p/w500{tmdb_response['poster_path']}"
    return image_url

# Function to get the IMDb URL of a media
def get_imdb_url(imdb_id):
    if imdb_id is not None:
        return f"https://www.imdb.com/title/{imdb_id}/"
    else:
        return None