"""
@File: twitch.py
@Description: Handles twitch requests
"""

import requests
from utils import log

# Simple function to download the mp4 file based on
# the clip's url.
def downloadClip(clip):
    log(f'Downloading clip: {clip}')

    name = str(clip['id']) + '.mp4'
    response = requests.get(clip['mp4'])

    file = open(f'clips/{name}', 'wb')

    for chunk in response.iter_content(chunk_size=255):
        if chunk:
            file.write(chunk)
    file.close()