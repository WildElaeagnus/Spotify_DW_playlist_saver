
Spotify_DW_playlist_saver
===
 Saves the weekly Spotify recommendations playlist, taking into account tracks you don't like.

## Deprecation wrning
[Here](https://github.com/akorzunin/Spotify_save_DW) is new project for the same purpose but with better implementation as a web app.

Why 
--- 
 Each week, Discover Weekly playlist is updated and the user's list of tracks he doesn't like is deleted. The program allows you to save a playlist generated from the recommendation playlist. 
 
 ![image](https://user-images.githubusercontent.com/54314123/132143250-be86711c-0662-4cf0-9106-cb65e718257f.png)



Installing
---
1. Make sure python3 is installed.
1. Use `pip install -r requirements.txt` to install    required libraries for python.
1. Configure the fields in the `auth_info.txt` file


### Setting up `auth_info.txt` file
- You can fill in the `user_id:` field by going to your [profile](https://www.spotify.com/ru-ru/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account) and copying the **user name** field
- Getting the token manually
	- You have to fill in the field `token_manual:` if you want to get the token manually. This can be done by [link](https://developer.spotify.com/console/get-album/), the permissions are in the file `permissons.py`.
- Getting a token using an automated browser
	- The `browser_profile_path: ` field is the path to your browser profile (if you use firefox it can be found at [about:profiles](about:profiles) under **Root Directory**). Use whatever browser profile your Spotify account is registered in.
	- The field `webdriver_exec_path: `is the path to the webdriver, for firefox it can be downloaded [here](https://github.com/mozilla/geckodriver/releases/tag/v0.29.1).
	- The field `firefox_binary_path: ` is the path to the executable file of the browser to be used (for example **C:\\Program Files\\Mozilla Firefox\\\firefox.exe**)
	- The field `web_browser: ` allows you to choose between `chrome` or `firefox` browser.
- The field `save_full_playlist:` 
`True` if the playlist has all 30 songs, it will be saved
The default setting is `False`.
- The field `publisity: ` is responsible for the availability of the created playlist to other users. It can be `public` / `private` by default `public`.
- The field `fav_device_name:` is the name of the preferred device from which the playlist will be played. By default, the first active device will be used.


How to use
---

### To run it manually

   Run the file `Spotify_DW_playlist_saver.pyw

### Run on schedule
- Using **SDWPS_playlist.pyw** 
	1.  Set up the configuration file **sheduler_config.txt**.
		Example:

			[Sheduler_config]
			period: weekly, Su, 20:00
			skript_name_py: Spotify_DW_playlist_saver.pyw 
	

	- Possible options for `period: ` hourly, daily, weekly, monthly
		
	2. Add the file **SDWPS_scheduler.pyw** to the autoloader.
	- You can find out the time before the script runs with the command `python ѕсheduler.pyw time` the script will not run in this case.

- Run with Windows Task Scheduler [link](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10)
- Run with cron (Linux) [link](https://www.jessicayung.com/automate-running-a-script-using-crontab/)





How it works
---
&nbsp;&nbsp;&nbsp;&nbsp;Since the Spotify API doesn't have a tool to figure out which tracks in the playlist recommendations you don't like, you'll have to use a workaround.
The method consists of the program trying to play a track from the recommendation playlist. If the track is not "disconnected," then it is possible to play it, but if the track is "disconnected," then it will not be playable and will not be included in the saved playlist. 

&nbsp;&nbsp;&nbsp;&nbsp;This way a selection of 30 tracks is made and only the ones left in the playlist recommendations by the end of the week will be saved by the program into a new playlist.


License
---
Spotify_DW_playlist_saver is free and open source software under the [Apache 2.0 License](https://github.com/create-go-app/cli/blob/master/LICENSE).

