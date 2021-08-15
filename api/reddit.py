"""
@File: reddit.py
@Description: Handles reddit requests
"""

import requests
from utils import log

URL = 'https://www.reddit.com/r/LivestreamFail'

def getClips(amount):

    log('Fetching clips info from reddit...')

    # Request extra amount of posts from reddit
    # The amount is doubled incase some of the posts
    # are not clips or the clip may be unavailable
    response = requests.get(f'{URL}/top/.json',
                            params={'limit': (amount+10)+((amount+10)/2)},
                            headers={'User-agent': 'gitclips'}
                            )

    # Fetch posts from the response data
    posts = response.json()['data']['children']

    count = 1
    clips = []
    for value in posts:
        data = value['data']

        # Checking if the post contains an acceptable clip
        if not data['secure_media']:
            continue
        if not data['secure_media']['oembed']['provider_url'] == 'http://www.twitch.tv':
            continue
        if len(data['link_flair_richtext']) != 2:
            continue

        # To avoid having to extend the program with Twitch's own API
        # we simply fetch the broadcaster from the flair that r/LiveStreamFails
        # provides. At the same time we gather the category in which the clip is
        # connected to. (ie. Just Chatting, Valorant etc.)
        flair = data['link_flair_richtext'][1]['t'].replace(' ', '')
        if '|' not in flair:
            continue

        broadcaster, category = flair.split('|')

        # Gathering all the necessary data from the response into a simple dictionary
        # and appending it to the clips array.
        clips.append({
            'id': count,
            'broadcaster': broadcaster,
            'category': category,
            'title': data['title'].encode('unicode-escape').decode("raw_unicode_escape"),
            'url': data['url'],
            'mp4': data['secure_media']['oembed']['thumbnail_url'].replace('-social-preview.jpg', '.mp4')
        })

        # If the required amount of clips has been gathered, we break the loop
        # and return the list
        if len(clips) == amount:
            break

        count += 1

    log(f'Clips have been fetched: \n{clips}')
    return clips