import requests
import json
import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getNewToken():

    token_url = "https://id.twitch.tv/oauth2/token?"
    with open("settings.json", "r") as file:
        json_data = json.load(file)

    response = requests.post(f"{token_url}"
                             f"client_id={json_data['client_id']}&"
                             f"client_secret={json_data['client_secret']}&"
                             f"grant_type={json_data['grant_type']}"
                             )

    token = response.json()['access_token']
    json_data['twitch']['token'] = token

    with open("settings.json", "w") as file:
        json.dump(json_data, file, indent=2)

    return token


def getToken():

    token = None

    with open("settings.json", "r") as file:
        json_data = json.load(file)

        if "token" in json_data['twitch']:
            token = json_data['twitch']['token']

    if token is None:
        token = getNewToken()

    return token


def addClipData(clip_id, token, client_id, title):

    response = requests.get(
        f"https://api.twitch.tv/helix/clips",
        headers={
            "Authorization" : f"Bearer {token}",
            "Client-ID" : client_id
        },
        params=f"id={clip_id}"
    )

    resp = response.json()["data"][0]
    return {
        "id" : resp["id"],
        "url": resp["url"],
        "broadcaster" : resp["broadcaster_name"],
        "title" : title
    }


def downloadClip(data):

    options = webdriver.ChromeOptions()
    options.add_argument('no-sandbox')
    options.add_argument("headless")
    options.add_argument('disable-dev-shm-usage')
    options.add_experimental_option("prefs", {
        "safebrowsing.enabled": True,
        "profile.managed_default_content_settings.images": 2
    })

    driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)

    driver.get(data["url"])
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
    video_url = str(elem.get_attribute("src"))

    while video_url is "":
        time.sleep(2)
        video_url = str(elem.get_attribute("src"))

    with requests.get(video_url, stream=True) as r:
        with open(f"clips/{data['id']}.mp4", "wb") as file:
            for chunk in r.iter_content(chunk_size=16*1024):
                file.write(chunk)

    driver.quit()