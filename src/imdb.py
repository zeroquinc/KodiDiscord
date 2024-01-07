# Function to get the IMDb ID of a media
def get_imdb_id(info):
    imdb_id = None
    # Check if 'uniqueid' and 'imdb' keys exist in the info
    if 'uniqueid' in info and 'imdb' in info['uniqueid']:
        imdb_id = info['uniqueid']['imdb']
    return imdb_id

# Function to get the IMDb URL of a media
def get_imdb_url(imdb_id):
    if imdb_id is not None:
        return f"https://www.imdb.com/title/{imdb_id}/"
    else:
        return None