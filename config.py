"""
This file contains all the configuration options for the script.
"""

TMDB_THUMBNAIL_ENABLED = False  # Set this to False to disable the TMDB thumbnail
TIME_REMAINING_RPC_ENABLED = True  # Set this to False to disable the time remaining RPC

"""
You can only set 1 of the following to True, set the rest to False
"""

DIRECTOR_ENABLED = False  # Set this to False to disable the director field
GENRES_ENABLED = True  # Set this to False to disable the genres field

"""
You can only set 2 of the following to True, set the rest to False
"""

IMDB_BUTTON_ENABLED = True  # Set this to False to disable the IMDb button
TMDB_BUTTON_ENABLED = False  # Set this to False to disable the TMDB button
TRAKT_BUTTON_ENABLED = False  # Set this to False to disable the Trakt buttons

"""
Default poster url. This will be used if the movie or TV show doesn't have a poster or if you are not using TMDb thumbnails.
"""

DEFAULT_POSTER_URL = "https://i.imgur.com/QONOI11.png" # Change this to your own image URL if you want to use a custom image