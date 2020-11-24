import json
import pickle
import os
import random
import time

import httplib2
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

def setupService():

    secret_file = "youtube.json"
    api_service_name = "youtube"
    api_version = "v3"
    scopes = ["https://www.googleapis.com/auth/youtube"]

    credentials = None

    if os.path.exists("YTtoken.pickle"):
        with open("YTtoken.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secret_file, scopes)
            credentials = flow.run_local_server()

        with open("YTtoken.pickle", "wb") as token:
            pickle.dump(credentials, token)


    try:
        service = build(api_service_name, api_version, credentials=credentials)
        print("Connection to youtube API successful.")
        return service
    except Exception as e:
        print(e)


service = setupService()

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


def resumableUpload(insert_request):

    response = None
    error = None
    retry = 0

    while response is None:
        try:
            print("Uploading video...")
            status, response = insert_request.next_chunk()
            if response is not None:
                print(f"Video id '{response['id']}'")
            else:
                exit(f"The upload failed with an unexpected response: {response}")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occured:\n{e.content}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occured: {e}"

    MAX_RETRIES = 10
    if error is not None:
        print(error)

        retry += 1
        if retry > MAX_RETRIES:
            exit("No longer attempting to retry.")

        max_sleep = 2 ** retry
        sleep_seconds = random.random() * max_sleep

        print(f"Sleeping {sleep_seconds} seconds and then retrying...")
        time.sleep(sleep_seconds)


def initUpload():

    with open("queue.json", "r") as json_file:
        info_section = json.load(json_file)["queue"]
        info = info_section[list(info_section.keys())[0]]

    title = str(info["title"])
    desc = f"{title}\n\n" + "Your description."

    body = dict(
        snippet=dict(
            title = title,
            description = desc,
            tags = f"{info['broadcaster']}, your tags",
            categoryId = "24"
        ),
        status = dict(
            privacyStatus = "public"
        )
    )

    insert_request = service.videos().insert(
        part=",".join(body.keys()),
        body = body,
        media_body=MediaFileUpload(f"clips/{info['id']}.mp4", chunksize=-1, resumable=True)
    )

    try:
        resumableUpload(insert_request)

    except Exception as e:
        print("Video not uploaded cause of the following error:")
        print(e)
        return False

    return True
