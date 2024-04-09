import customtkinter as ctk
import tkinter as tk
import pytube
import time
import threading
from functions.getColor import getColor
from .playList import playList 
from .downloadingVideo import downloadingVideo
import webbrowser

class downloadingPlayList(playList):
    def __init__(self,
                master=None,
                width=None,
                height=None,
                border_width=None,
                
                channel_url = None,
                playlist_url=None,
                playlist_title = "---------",
                channel = "---------",
                video_count = "?",
        
                bg_color=None,
                fg_color=None,
                text_color=None,
                theme_color=None,
                hover_color=None,
                special_color=None,
                
                videos: list[downloadingVideo] = None,
                download_directory = "",
                downloaded_callback_function = None
                ):
        
        super().__init__(master=master,
                        height=height,
                        width=width,
                        border_width=border_width,
                        
                        channel_url = channel_url,
                        playlist_url=playlist_url,
                        playlist_title=playlist_title,
                        channel=channel,
                        video_count=video_count,
                        
                        bg_color=bg_color,
                        fg_color=fg_color,
                        text_color=text_color,
                        theme_color=theme_color,
                        hover_color=hover_color,
                        special_color=special_color,
                        )
        
        self.videos = videos
        self.download_directory = download_directory
        self.downloading_videos = []
        threading.Thread(target=self.download_videos).start()


    def download_videos(self):
        for video in self.videos:
            self.downloading_videos.append(
                downloadingVideo(
                    master=self.playlist_item_frame,
                    height=70,
                    width=self.playlist_item_frame.winfo_width()-20,
                    border_width=1,
                                
                    fg_color=self.fg_color,
                    bg_color=self.bg_color,
                    theme_color=self.theme_color,
                    text_color=self.text_color,
                    hover_color=self.hover_color,
                    special_color=self.special_color,
                    
                    channel_url=video.channel_url,
                    url=video.url,
                    download_quality=video.download_quality,
                    download_type=video.download_type,
                    title=video.title,
                    channel=video.channel,
                    thumbnails=video.thumbnails,
                    video_stream_data=video.video_stream_data,
                    
                    download_directory = self.download_directory,
                    downloaded_callback_function = None
                    )
                
                )
            self.downloading_videos[-1].pack(fill="x", padx=(20,0), pady=1)
        self.view_btn.configure(state="normal")
        