import tkinter as tk
from .playList import playList
from .downloadingPlayList import downloadingPlayList
from .downloadedVideo import downloadedVideo
from .downloadingVideo import downloadingVideo

class downloadedPlayList(playList):
    def __init__(self,
                master=None,
                width=None,
                height=None,
                border_width=None,
                
                bg_color=None,
                fg_color=None,
                text_color=None,
                theme_color=None,
                hover_color=None,
                special_color=None,
                
                channel_url = None,
                playlist_url=None,
                playlist_title = "---------",
                channel = "---------",
                video_count = "?",
                
                videos=None,
                ):
        super().__init__(master=master,
                         width=width,
                         height=height,
                         border_width=border_width,
                         
                         bg_color=bg_color,
                         fg_color=fg_color,
                         text_color=text_color,
                         theme_color=theme_color,
                         hover_color=hover_color,
                         special_color=special_color,
                         
                         channel_url=channel_url,
                         playlist_url=playlist_url,
                         playlist_title=playlist_title,
                         channel=channel,
                         video_count=video_count,)
        
        self.videos: list[downloadingVideo] = videos
        self.downloaded_videos = []
        self.create_downloaded_widgets()
        
    def create_downloaded_widgets(self):
        for video in self.videos:
            self.downloaded_videos.append(
                downloadedVideo(master=self.playlist_item_frame,
                                height=70,
                                border_width=1,
                                width=self.playlist_item_frame.winfo_width()-20,
                                download_quality=video.download_quality,
                                download_type=video.download_type,
                                
                                fg_color=self.fg_color,
                                bg_color=self.bg_color,
                                text_color=self.text_color,
                                hover_color=self.hover_color,
                                theme_color=self.theme_color,
                                special_color=self.special_color,
                                
                                thumbnails=video.thumbnails,
                                title=video.title,
                                channel=video.channel,
                                channel_url=video.channel_url,
                                url=video.url,
                                download_path=video.download_file_name,
                                file_size=video.total_bytes,
                                length=video.length,
                                )
                )
            
            self.downloaded_videos[-1].remove_btn.configure(command = lambda video=self.downloaded_videos[-1]: self.remove_video(video))
            self.downloaded_videos[-1].pack(fill="x", padx=(20,0), pady=1)
            
        self.view_btn.configure(state="normal")
    
    
    def set_theme(self):
        super().set_theme()
        for video in self.downloaded_videos:
            video.set_new_theme(self.theme_color)
    
    
    def remove_video(self, video: downloadingVideo):
        self.video_count -= 1
        self.complete_count_label.configure(text=self.video_count)
        video.kill()