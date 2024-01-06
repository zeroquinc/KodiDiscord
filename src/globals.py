import os
from dotenv import load_dotenv
from pypresence import Presence

load_dotenv()

"""Global variables"""

# Discord client ID
client_id = '1190792021263265912'

# TMDB API key
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# Trakt API key
TRAKT_API_KEY = os.getenv('TRAKT_API_KEY')

# Discord Rich Presence
RPC = Presence(client_id)
RPC.connect()

# Kodi server configuration
port = 8080
BASE_URL = f"http://localhost:{port}/jsonrpc"
INFO_URL = BASE_URL + "?request={%20%22jsonrpc%22:%20%222.0%22,%20%22method%22:%20%22Player.GetItem%22,%20%22params%22:%20{%20%22properties%22:%20[%20%22title%22,%20%22season%22,%20%22episode%22,%20%22duration%22,%20%22showtitle%22,%20%22tvshowid%22,%20%22year%22,%20%22genre%22,%20%22director%22,%20%22uniqueid%22],%20%22playerid%22:%201%20},%20%22id%22:%20%22VideoGetItem%22%20}"
LENGTH_URL = BASE_URL + "?request={%22jsonrpc%22:%222.0%22,%22method%22:%22Player.GetProperties%22,%22params%22:{%22playerid%22:1,%22properties%22:[%22speed%22,%22time%22,%22totaltime%22]},%22id%22:%221%22}"

# Discord Rich Presence texts
UPDATED_RPC = "Updated RPC"
LIVETV_LARGE_TEXT = 'Watching Live TV on Kodi'
EPISODE_LARGE_TEXT = 'Watching a TV Show on Kodi'
MOVIE_LARGE_TEXT = 'Watching a Movie on Kodi'