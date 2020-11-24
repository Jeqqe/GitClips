import praw
import json


def getClips(amount):

    with open("settings.json", "r") as file:
        json_data = json.load(file)

    reddit = praw.Reddit(
        client_id = json_data['reddit']['client_id'],
        client_secret = json_data['reddit']['client_secret'],
        user_agent = json_data['reddit']['user_agent'],
        username = json_data['reddit']['username'],
        password = json_data['reddit']['password']
    )

    subred = reddit.subreddit("livestreamfail")

    dailyTop = subred.top("day", limit=amount)
    clips = dict()
    for post in dailyTop:
        clip_url = "https://clips.twitch.tv/"
        url = str(post.url)

        if url[0:len(clip_url)] == clip_url:
            if len(str(post.title)) <= 100:
                clips[(url.replace(clip_url, ""))] = post.title

    return clips
