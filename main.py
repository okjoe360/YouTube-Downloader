import eel
from services import YouTubeDownloader
import easygui

eel.init('web')

@eel.expose
def searchURL(url):
    streams = YouTubeDownloader().yt_downloader(url)
    return streams

@eel.expose
def downloadVideo(url, default_filename, itag, last_audio):
    path = easygui.diropenbox()
    outfile = YouTubeDownloader().download_video(url, itag, path, last_audio)
    return outfile


eel.start('index.html', size=(450, 550))