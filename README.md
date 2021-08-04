# GitClips - Simple Twitch.tv clip uploader

GitClips' purpose is to automatically collect some of the more popular
clips from the streaming platform known as
[Twitch](https://www.twitch.tv/) and upload them to a
[YouTube channel](https://www.youtube.com/channel/UCNR6zkFCc4PsQtbtDjF02Lw/featured).

The process of identifying the more popular clips from Twitch is handled
by gathering the clips from Reddit, more specifically from
[r/LiveStreamFail](https://www.reddit.com/r/LivestreamFail/). The
program also fetches all the necessary information about the clips and
the broadcastor from reddit, which makes it unnecessary to use Twitch's
own API. This is a good thing since we don't have to bother messing with
twitch's access tokens etc. It's also beneficial since twitch's clip
titles are usually a lot worse than those posted on Reddit.

After the data has been gathered from Reddit, the program downloads the
*clip.mp4* based on the url fetched from the embedded video data of the
reddit request. And then proceeds to prepare a resumable upload to
youtube using the
[YouTube API](https://developers.google.com/youtube/v3/docs).


## Setup

**NOTE** - It is recommended to execute the program first on your PC instead of a
server. The program asks you to authorize the google application on its
setup process, which requires actions on a browser.

1. Download the repository contents manually or click
   [HERE](https://github.com/Jeqqe/GitClips/archive/refs/heads/v2.zip).
2. Drag and drop the *main.py* file and the *api* directory to your
   desired location
3. Install script requirements with `pip install -r requirements.txt`
4. Fetch your Google API *client_secret.json* file, rename it to
   *youtube.json* and place it inside the api directory.
5. Execute the *main.py* file, it should prompt you to visit a url to
   authorize the google application. (Server: At this point if you
   already have your YTtoken.pickle on your PC, drag and drop it in the
   api directory on the server)
6. The first launch also generated the data directory, where you can
   edit your video tags and description.
7. Once the token has been placed in the api directory, re-execute the
   *main.py* and you're done.

