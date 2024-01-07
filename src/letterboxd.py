"""	
This module contains functions related to Letterboxd.
"""

# Function to get the Letterboxd URL of a media
def get_letterboxd_url(tmdb_id):
    if tmdb_id is not None:
        return f"https://letterboxd.com/tmdb/{tmdb_id}"
    else:
        return None