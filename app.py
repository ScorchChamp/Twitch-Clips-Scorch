import twitch
import youtube
import datetime
import re
import requests

DAYS_AGO = int(5*365.25)
START_DATE = (datetime.datetime.now() - datetime.timedelta(days=DAYS_AGO)).strftime("%Y-%m-%dT%H:%M:%SZ")
END_DATE = (datetime.datetime.now() - datetime.timedelta(days=DAYS_AGO) + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
REQUIRED_LANGUAGE = "en"
REQUIRED_VIEWS = 1000
GAME_NAME = "minecraft"
EXTRA_TAGS = [GAME_NAME, "english"]

best_clip = twitch.get_clips(GAME_NAME, START_DATE, END_DATE, REQUIRED_LANGUAGE, REQUIRED_VIEWS)[0]
title = best_clip.get('title')
tags = title.split(" ") + EXTRA_TAGS

description = f"""
5 years ago on twitch: {title}

Please follow {best_clip.get('creator_name')} on Twitch: https://www.twitch.tv/{best_clip.get('creator_name')}
Original VOD: https://www.twitch.tv/{best_clip.get('creator_name')}/clip/{best_clip.get('id')}
"""

title_re = re.sub(r'[^\w\s]', '', title)
with open(f"clips/{title_re}.mp4", "wb") as file: file.write(requests.get(best_clip.get('download_url')).content)

metadata = youtube.upload_video('CHANNEL_ID', f"clips/{title_re}.mp4", title, description, tags, 20)
print(f'Successfully uploaded video to https://www.youtube.com/watch?v={metadata["id"]}')