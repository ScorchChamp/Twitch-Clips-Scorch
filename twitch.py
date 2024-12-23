import requests
import os, dotenv
import datetime
import tos_obfuscation

def get_oauth(client_id, client_secret):
    response = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials").json()
    return f"{response.get('token_type').capitalize()} {response.get('access_token')}"

def get_api_data(endpoint, parameters):
    return requests.get(endpoint, parameters, headers={
        "Client-Id": os.getenv("TWITCH_CLIENT_ID"),
        "Authorization": get_oauth(os.getenv("TWITCH_CLIENT_ID"), os.getenv("TWITCH_CLIENT_SECRET"))
    }).json().get('data')

def get_userid_by_name(name):
    return get_api_data("https://api.twitch.tv/helix/users", {"login": name})[0].get('id')

def get_gameid_by_name(name):
    return get_api_data("https://api.twitch.tv/helix/games", {"name": name})[0].get('id')

def get_top_clips(parameters, start_date=datetime.datetime.now() - datetime.timedelta(days=1), end_date=datetime.datetime.now(), limit=100):
    return get_api_data("https://api.twitch.tv/helix/clips", {
        "started_at": start_date.strftime("%Y-%m-%dT%H:%M:%S") + "Z",
        "ended_at": end_date.strftime("%Y-%m-%dT%H:%M:%S") + "Z",
        "first": limit,
        **parameters
    })

if not os.getenv("TWITCH_CLIENT_ID"): dotenv.load_dotenv()

def get_clips(game, start_date, end_date, required_language, required_views):
    top_clips = get_top_clips({'started_at': start_date, 'ended_at': end_date, 'game_id': get_gameid_by_name(game)})
    for clip in top_clips:  clip['download_url'] = tos_obfuscation.convert_clip_to_download_url(clip)
    
    top_clips = [clip for clip in top_clips if clip.get('language') == required_language]
    top_clips = [clip for clip in top_clips if clip.get('view_count') >= required_views]
    
    return top_clips