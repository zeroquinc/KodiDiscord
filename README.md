# 🎬 KodiDiscord 🎮
Discord Rich Presence for Kodi

![T6gJtlM](https://github.com/zeroquinc/KodiDiscord/assets/39315068/ae5557bc-7705-44b2-a9e1-69d02055afa5)

---

# 📝 Prerequisites
* Kodi Nexus 20.0 or higher (19 and lower might not work with thumbnails)
* Python (version 3.x)

## 📝 Optional
* A TMDb account for dynamic images and TMDb button
* A Trakt account for Trakt button

---

# 🚀 Installation
1. Clone the repository
2. Install the dependencies from `requirements.txt`
3. Rename `.env.example` to `.env`

## 🚀  Optional
1. Edit `.env` and fill in your TMDB API key & Trakt Client ID
2. Edit `config.py` to your liking, see configuration below

---

# 🎯 Usage
1. Make sure `Allow remote control via HTTP` is enabled in Kodi
2. Run `main.py`
3. Profit

---

# 🎞️ Supported Media Types 
* TV Shows 📺
* Movies 🎥
* Live TV (PVR IPTV Simple Client) 📡

---

## 📸 Examples
TV Shows:

![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/bd290633-6341-4b65-8955-961fa1026db4)

![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/0e9417eb-2459-4ce4-aa66-444be0065581)

---

Movies:

![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/6a3f363e-b1c1-4489-898c-6c38a9bcd349)

![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/07cecdf8-9557-470a-8a70-7607493ee85f)

---

No buttons:

![image](https://github.com/zeroquinc/KodiDiscord/assets/39315068/c35231b8-31a9-4663-aa84-728430ecb0b3)

---

# 🔧 Configuration

The file `config.py` contains the configuration for the Discord Rich Presence. You can customize it according to your needs.

## Globals

Change the `DISCORD_ID` to your own Discord ID if you want to use your own Discord application. Make sure to upload images as "play" and "pause" in the Rich Presence tab of your Discord application.

- `DISCORD_ID`
- `LOG_LEVEL`: Set this to either INFO or DEBUG, CRITICAL, WARNING etc

## Global Config Variables

- `TMDB_THUMBNAIL_ENABLED`: Set this to False to disable the TMDB thumbnail in the RPC
- `TIME_REMAINING_RPC_ENABLED`: Set this to False to disable the time remaining RPC

## Fields

You can only set 1 of the following to True, set the other to False:

- `DIRECTOR_ENABLED`: Set this to False to disable the director field in the RPC
- `GENRES_ENABLED`: Set this to False to disable the genres field in the RPC

## Buttons

```
You can only set 2 of the following to True, set the rest to False
Except for the Letterboxd button, you can keep it to True if you use it
You can set everything to True but due to Discord's 2 button limit, the bottom 2 will be removed
```

- `IMDB_BUTTON_ENABLED`: Set this to False to disable the IMDb button in the RPC
- `TMDB_BUTTON_ENABLED`: Set this to False to disable the TMDB button in the RPC
- `TRAKT_BUTTON_ENABLED`: Set this to False to disable the Trakt button in the RPC
- `LETTERBOXD_BUTTON_ENABLED`: Set this to False to disable the Letterboxd button in the RPC

## Default Poster URL

This will be used if the movie or TV show doesn't have a poster or if you are not using TMDb thumbnails.

- `DEFAULT_POSTER_URL` Change this to an image of your own liking if needed

## Hover Texts

You can change the following variables if you want to change the texts that are displayed when you hover over the RPC:

- `LIVETV_LARGE_TEXT`: Change this to your own text if you want to change the hover over text for Live TV
- `EPISODE_LARGE_TEXT`: Change this to your own text if you want to change the hover over text for TV Shows
- `MOVIE_LARGE_TEXT`: Change this to your own text if you want to change the hover over text for Movies

---

# 💡 Future Ideas
* Add Music
* Try to make it a Kodi addon

---

# 📞 Contact
If you have any questions, please create an issue or add me on Discord 💬
