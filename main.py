"""
@File: main.py
@Description: Main application logic
"""

import os
from api import reddit, twitch, youtube

from utils import log

def setup():

    if not os.path.exists('clips'):
        os.mkdir('clips')
        log('Clips folder created (/clips)')

    if not os.path.exists('data'):
        os.mkdir('data')
        log('Data folder created (/data)')

    if not os.path.exists('data/description.txt'):
        with open('data/description.txt', 'w') as description:
            description.write('Default description.')
            description.close()
        log('Default description created. (/data/description.txt)')

    if not os.path.exists('data/tags.txt'):
        with open('data/tags.txt', 'w') as description:
            description.write('gitclips,default,tags')
            description.close()
        log('Default tags created. (/data/tags.txt)')

if __name__ == '__main__':

    setup()

    # Setup the youtube API service
    service = youtube.setupService()

    # Check if secret_file is successfully found, if not, break the loop and
    # end program.
    if not service:
        exit()

    # Request (6) clips from reddit [r/LiveStreamFail]
    clips = reddit.getClips(6)

    # Go through each fetched clip, download it and upload to youtube
    # with title, description and tag
    for clip in clips:
        twitch.downloadClip(clip)
        youtube.initUpload(service, clip)
