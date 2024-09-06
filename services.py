from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
from datetime import date
import os, time, shutil


class YouTubeDownloader:
    def __init__(self):
        self.file_name = None
        self.audio_file = None
        self.temp_video_file = None
        
        self.outfile = None

        self.today = date.today().strftime("%d_%m_%Y")
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.file_path = os.path.join(self.dir_path, 'temp', 'youtube_downloads', self.today)
        try:
            self.remove_temp_files()
        except:
            print('Temp Files not Deleted...')

    def yt_downloader(self, url):
        try:
            yt = YouTube(url, on_progress_callback = on_progress)
        except:
            return {'error':'YouTube Link Invalid...'}
        result = []
        audio_files = []
        video_files= []
        preview = self.getParams(url)
        for f in yt.streams:
            attrps = {
                'filesize': f.filesize, 
                "filesize_mb": f.filesize_mb,
                "audio_codec":f.audio_codec, 
                "bitrate":f.bitrate,
                'res': f.resolution,
                'type': f.type,
                'video_codec': f.video_codec,
                'mime_type': f.mime_type,
                'title': f.title,
                'abr':f.abr,
                'size': str(f),
                'itag':f.itag,
                'default_filename':f.default_filename
                }
            try:
                attrps["fps"] = f.fps
            except:
                pass

            try:
                attrps["width"] = f.width
            except:
                pass

            result.append(attrps)
            audio_files = sorted([r for r in result if r.get('type') == 'audio'], key=lambda x:x['filesize'], reverse = True)
            video_files = sorted([r for r in result if r.get('type') == 'video'], key=lambda x:x['filesize'], reverse = True)
        return {'full':result, 'audio':audio_files, 'video':video_files, 'streams':yt.streams.order_by('resolution'), 'preview':preview, 'last_audio':audio_files[-1]['itag'] }

    
    def download_video(self, url, itag, download_location, last_audio=None):
        yt = YouTube(url, on_progress_callback = on_progress)

        y = yt.streams.get_by_itag(itag)
        self.file_name = f"{y.default_filename}"

        if y.abr in ['None', None] and str(y.type) in ['video']:
            if last_audio:
                aud = yt.streams.get_by_itag(last_audio)
            else:
                aud = yt.streams.get_audio_only()
            self.audio_file = aud.download(output_path=self.file_path, filename=f"{aud.default_filename.replace('.mp4', '.mp3')}", mp3=True)

        if y.type in ['audio']:
            self.file_name = self.file_name.replace('.mp4', '.mp3')

        if self.audio_file:
            while self.temp_video_file == None:
                self.temp_video_file = y.download(output_path=self.file_path, filename=self.file_name)
            else:
                return self.combine_video_audio(download_location)
        else:
            self.outfile = y.download(output_path=download_location, filename=self.file_name)
            return self.outfile

    def combine_video_audio(self, download_location):
        new_out_video_path = os.path.join(download_location, f"_{self.file_name}")
        ffmpeg_merge_video_audio(self.temp_video_file, self.audio_file, new_out_video_path)
        time.sleep(2)
        #final_clip = None
        time.sleep(3)
        return new_out_video_path


    def getParams(self, url):
        query = url.split('=')[-1]
        params = url.split("?")[1]
        params = params.split('=')
        pairs = zip(params[0::2], params[1::2])
        answer = dict((k,v) for k,v in pairs)
        if answer.get('v'):
            query = answer.get('v').split('&')[0]
        return f"https://i.ytimg.com/vi/{query}/hqdefault.jpg"


    def remove_temp_files(self):
        youtube_downloads_file_path = os.path.join(self.dir_path, 'temp', 'youtube_downloads')
        print(os.walk(youtube_downloads_file_path))
        subfolders = [ f for f in os.scandir(youtube_downloads_file_path) if f.is_dir() ]
        for s in subfolders:
            if os.path.basename(s) != self.file_path:
                shutil.rmtree(s.path)

