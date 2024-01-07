# 🎬 KodiDiscord 🎮
Discord Rich Presence for Kodi

# 📝 Prerequisites
* Kodi Nexus 20.0 or higher (19 and lower might not work with thumbnails)
* Python (version 3.x)

## 📝 Optional
* A TMDb account for dynamic images and TMDb button
* A Trakt account for Trakt button

# 🚀 Installation
1. Clone the repository
2. Install the dependencies from `requirements.txt`
3. Rename `.env.example` to `.env`
4. Optional: Edit `.env` and fill in your TMDB API key & Trakt Client ID
5. Optional: Edit `config.py` to your liking, see configuration below

# 🎯 Usage
Run `main.py`

# 🎞️ Supported Media Types 
* TV Shows 📺
* Movies 🎥
* Live TV (PVR IPTV Simple Client) 📡

## 📸 Examples
![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/848cbe27-d508-46c5-93dd-a8b9c72c92a1)

![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/e494b101-c764-4901-bd7d-a53aa186b0e4)

![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/e22e37c0-27a6-429a-a2c4-21e412aad10a)

# 🔧 Configuration

The file `config.py` contains the configuration for the Discord application. You can customize it according to your needs.

## Discord ID

Change the `DISCORD_ID` to your own Discord ID if you want to use your own Discord application. Make sure to upload images as "play" and "pause" in the Rich Presence tab of your Discord application.

- `DISCORD_ID`

## Global Config Variables

- `TMDB_THUMBNAIL_ENABLED`: Set this to False to disable the TMDB thumbnail in the RPC
- `TIME_REMAINING_RPC_ENABLED`: Set this to False to disable the time remaining RPC

## Fields

You can only set 1 of the following to True, set the other to False:

- `DIRECTOR_ENABLED`: Set this to False to disable the director field in the RPC
- `GENRES_ENABLED`: Set this to False to disable the genres field in the RPC

## Buttons

You can only set 2 of the following to True, set the rest to False:

- `IMDB_BUTTON_ENABLED`: Set this to False to disable the IMDb button in the RPC
- `TMDB_BUTTON_ENABLED`: Set this to False to disable the TMDB button in the RPC
- `TRAKT_BUTTON_ENABLED`: Set this to False to disable the Trakt buttons in the RPC

## Default Poster URL

This will be used if the movie or TV show doesn't have a poster or if you are not using TMDb thumbnails.

- `DEFAULT_POSTER_URL` Change this to an image of your own liking if needed

## Hover Texts

You can change the following variables if you want to change the texts that are displayed when you hover over the RPC:

- `LIVETV_LARGE_TEXT`: Change this to your own text if you want to change the hover over text for Live TV
- `EPISODE_LARGE_TEXT`: Change this to your own text if you want to change the hover over text for TV Shows
- `MOVIE_LARGE_TEXT`: Change this to your own text if you want to change the hover over text for Movies

# 💡 Future Ideas
* Add Music
* Try to make it a Kodi addon

# 📞 Contact
If you have any questions, please create an issue or add me on Discord 💬
