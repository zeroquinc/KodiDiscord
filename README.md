# 🎬 KodiDiscord 🎮
Discord Rich Presence for Kodi

## 📝 Prerequisites
* Kodi Nexus 20.0 or higher (19 and lower might not work with thumbnails)
* Python (version 3.x)
* A TMDB account

## 🚀 Installation
1. Clone the repository
2. Install the dependencies from `requirements.txt`
3. Rename `.env.example` to `.env`
4. Edit `.env` and fill in your TMDB API key

## ⚙️ Configuration

Edit `config.py` and make the following changes:

This section contains all the configuration options for the script.

- `TMDB_THUMBNAIL_ENABLED`: Set this to `False` to disable the TMDb poster. Default is `False`.
- `TIME_REMAINING_RPC_ENABLED`: Set this to `False` to disable the time remaining RPC. Default is `True`.

You can only set **1** of the following to `True`, set the rest to `False`:

- `DIRECTOR_ENABLED`: Set this to `False` to disable the director field. Default is `False`.
- `GENRES_ENABLED`: Set this to `False` to disable the genres field. Default is `True`.

You can only set **2** of the following to `True`, set the rest to `False`:

- `IMDB_BUTTON_ENABLED`: Set this to `False` to disable the IMDb button. Default is `True`.
- `TMDB_BUTTON_ENABLED`: Set this to `False` to disable the TMDB button. Default is `False`.
- `TRAKT_BUTTON_ENABLED`: Set this to `False` to disable the Trakt buttons. Default is `False`.

## 🎯 Usage
Run `main.py`

## 🎞️ Supported Media Types
* TV Shows 📺
* Movies 🎥
* Live TV (PVR IPTV Simple Client) 📡

## 📸 Examples
![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/848cbe27-d508-46c5-93dd-a8b9c72c92a1)

![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/e494b101-c764-4901-bd7d-a53aa186b0e4)

![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/e22e37c0-27a6-429a-a2c4-21e412aad10a)

## 💡 Future Ideas
* Add Music
* Try to make it a Kodi addon

## 📞 Contact
If you have any questions, please create an issue or add me on Discord 💬
