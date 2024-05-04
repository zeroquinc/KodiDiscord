import os
from dotenv import load_dotenv
from pypresence import Presence
from config import DISCORD_ID

load_dotenv()

def setup_discord_presence(client_id):
    rpc = Presence(client_id)
    rpc.connect()
    return rpc

client_id = DISCORD_ID
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TRAKT_API_KEY = os.getenv('TRAKT_API_KEY')
RPC = setup_discord_presence(client_id)

port = 8080
BASE_URL = f"http://localhost:{port}/jsonrpc"
INFO_URL = f"{BASE_URL}?request={{%20%22jsonrpc%22:%20%222.0%22,%20%22method%22:%20%22Player.GetItem%22,%20%22params%22:%20{{%20%22properties%22:%20[%20%22title%22,%20%22season%22,%20%22episode%22,%20%22duration%22,%20%22showtitle%22,%20%22tvshowid%22,%20%22year%22,%20%22genre%22,%20%22director%22,%20%22uniqueid%22],%20%22playerid%22:%201%20}},%20%22id%22:%20%22VideoGetItem%22%20}}"
LENGTH_URL = f"{BASE_URL}?request={{%22jsonrpc%22:%222.0%22,%22method%22:%22Player.GetProperties%22,%22params%22:{{%22playerid%22:1,%22properties%22:[%22speed%22,%22time%22,%22totaltime%22]}},%22id%22:%221%22}}"