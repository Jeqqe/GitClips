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
