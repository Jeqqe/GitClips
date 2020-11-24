import twitchAPI
import youtubeAPI
import redditAPI
import json
import os


def getSettings():
    with open("settings.json", "r") as file:
        return json.load(file)

def getQueue():
    with open("queue.json", "r") as file:
        return json.load(file)

class App:

    def __init__(self):
        self.settings = getSettings()
        self.queue = getQueue()

    def checkQueue(self):

        # Check if the queue is full, return None if there's already 10 clips pending
        if len(self.queue["queue"]) >= 1:
            print("Qeueu full, wont look for new clips...")
            return None

        else:
            print(f"Queue empty! ({len(self.queue['queue'])}/1) Loading new clips...")
            return self.queue

    def addNewClipsToQueue(self, clips):

        for key,title in clips.items():

            if key in self.queue["queue"] or key in self.queue["past"]:
                continue

            # Add data to clip
            self.queue["queue"][key] = twitchAPI.addClipData(key, self.settings['twitch']['token'], self.settings['twitch']['client_id'], title)

            # Download clip
            twitchAPI.downloadClip(self.queue["queue"][key])

            if len(self.queue["queue"]) >= 1:
                break

        with open("queue.json", "w") as file:
            json.dump(self.queue, file, indent=2)


    def removeFromQueue(self, addToPast):

        clip_id = self.queue["queue"][list(self.queue["queue"].keys())[0]]["id"]
        del self.queue["queue"][list(self.queue["queue"].keys())[0]]

        if addToPast:
            self.queue["past"].append(clip_id)

            if len(self.queue["past"]) > 10:
                del self.queue["past"][0]
        
        with open("queue.json", "w") as file:
            json.dump(self.queue, file, indent=2)
        os.remove(f"clips/{clip_id}.mp4")


if __name__ == "__main__":

    app = App()
    queue = app.checkQueue()

    if queue is not None:

        # Load new clips from reddit/Livestreamfails
        clip_ids = redditAPI.getClips(10)

        # Add new clip(s) to queue until its full again
        app.addNewClipsToQueue(clip_ids)

    # Upload to youtube
    status = youtubeAPI.initUpload()

    # Remove from queue
    app.removeFromQueue(status)


