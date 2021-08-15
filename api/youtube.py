"""
@File: youtube.py
@Description: Handles youtube requests
"""

import pickle
import os
import random
import time
import httplib2
from datetime import datetime, timedelta

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

from utils import log

def setupService():

    # secret_file is fetched straight from the google's API credentials page
    # Paths to both, the secret file and where the token file is to be stored
    secret_file = 'api/youtube.json'
    token_file = 'api/YTtoken.pickle'

    if not os.path.exists(secret_file):
        log('Youtube API secret_file not found. You can download your secret file from the google cloud console. '
              'Rename it to "youtube.json" and drop it in the /api directory.')
        return False

    # Settings for the youtube's API service
    api_service_name = 'youtube'
    api_version = 'v3'
    scopes = ['https://www.googleapis.com/auth/youtube']

    # Get credentials from existing token_file or generate a new one
    # if one isn't available or has expired.
    credentials = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:

        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secret_file, scopes)
            credentials = flow.run_local_server()

        with open(token_file, 'wb') as token:
            pickle.dump(credentials, token)

    # Build the YouTube API service based on the loaded credentials
    # and settings and return it
    try:
        service = build(api_service_name, api_version, credentials=credentials)
        log('Connection to youtube API successful.')
        return service
    except Exception as e:
        log(e)

# Possible exceptions that cause the program to retry the uploading process
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


def resumableUpload(clip, video_data):

    response = None
    error = None
    retry = 0

    # Start up the process to upload the video based on video_data
    while response is None:
        try:

            log('Starting video upload...')
            status, response = video_data.next_chunk()

            if response is not None:
                log(f'Video id "{response["id"]}" has been uploaded!')
                # Remove uploaded file from the app/clips directory
                os.remove(f'clips/{str(clip["id"]) + ".mp4"}')
                return
            else:
                exit(f'The upload failed with an unexpected response: {response}')

        # If response caused and exception, update the error variable and attempt to
        # resume the upload if possible
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f'A retriable HTTP error {e.resp.status} occured:\n{e.content}'
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f'A retriable error occured: {e}'

        MAX_RETRIES = 10
        log(error)

        retry += 1
        if retry > MAX_RETRIES:
            exit('No longer attempting to retry.')

        max_sleep = 2 ** retry
        sleep_seconds = random.random() * max_sleep

        log(f'Sleeping {sleep_seconds} seconds and then retrying...')
        time.sleep(sleep_seconds)

def replacePlaceholders(text, clip):
    return text \
        .replace('%title%', clip['title']) \
        .replace('%broadcaster%', clip['broadcaster']) \
        .replace('%url%', clip['url']) \
        .replace('%category%', clip['category'])

def initUpload(service, clip):

    # Setup video details, load description and tags from data folder
    title = str(clip['title'])
    desc = replacePlaceholders(open('data/description.txt', 'r+', encoding="utf8").read(), clip)
    tags = replacePlaceholders(open('data/tags.txt', 'r+', encoding="utf8").read(), clip)

    # Setup body data for upload/insert
    body = dict(
        snippet=dict(
            title = title,
            description = desc,
            tags = tags,
            categoryId = '24'
        ),
        status = dict(
            privacyStatus = 'private',
            publishAt = (datetime.now() + timedelta(hours=clip['id']*4)).isoformat()
        )
    )

    # Setup request for upload/insert
    video_data = service.videos().insert(
        part=','.join(body.keys()),
        body = body,
        media_body=MediaFileUpload(f'clips/{clip["id"]}.mp4', chunksize=-1, resumable=True)
    )

    try:
        # Attempt to start upload
        resumableUpload(clip, video_data)

    except Exception as e:
        log('Video not uploaded cause of the following error:')
        log(e)
        return False

    return True
