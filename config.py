"""
Change the DISCORD_ID to your own Discord ID if you want to use your own Discord application.
Make sure to upload images as "play" and "pause" in the Rich Presence tab of your Discord application.
"""

DISCORD_ID = '1190792021263265912'  # Your Discord ID, you can change this if you want to use your own Discord application

"""
Global config variables
"""
LOG_LEVEL = 'DEBUG'  # or 'DEBUG, WARNING, ERROR, CRITICAL'                                                
TMDB_THUMBNAIL_ENABLED = True  # Set this to False to disable the TMDB thumbnail
TIME_REMAINING_RPC_ENABLED = True  # Set this to False to disable the time remaining RPC

"""
You can only set 1 of the following to True, set the rest to False
"""

DIRECTOR_ENABLED = False  # Set this to False to disable the director field
GENRES_ENABLED = True  # Set this to False to disable the genres field

"""
You can only set 2 of the following to True, set the rest to False
Except for the Letterboxd button, you can keep it to True if you use it
You can set everything to True but due to Discord's 2 button limit, the bottom 2 will be removed
"""

IMDB_BUTTON_ENABLED = True  # Set this to False to disable the IMDb button
TMDB_BUTTON_ENABLED = False  # Set this to False to disable the TMDB button
TRAKT_BUTTON_ENABLED = False  # Set this to False to disable the Trakt buttons
LETTERBOXD_BUTTON_ENABLED = False  # Set this to False to disable the Letterboxd button

"""
Default poster url. This will be used if the movie or TV show doesn't have a poster or if you are not using TMDb thumbnails.
"""

DEFAULT_POSTER_URL = "https://i.imgur.com/QONOI11.png" # Change this to your own image URL if you want to use a custom image

"""	
You can change the following variables if you want to change the texts that are displayed when you hover over the RPC.
"""

LIVETV_LARGE_TEXT = 'Watching Live TV on Kodi' # Change this to your own text if you want to change the hover over text for Live TV
EPISODE_LARGE_TEXT = 'Watching a TV Show on Kodi' # Change this to your own text if you want to change the hover over text for TV Shows
MOVIE_LARGE_TEXT = 'Watching a Movie on Kodi' # Change this to your own text if you want to change the hover over text for Movies