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
        
        self.downloaded_callback_function = downloaded_callback_function
        self.videos = videos
        self.download_directory = download_directory
        self.downloading_videos = []
        threading.Thread(target=self.download_videos).start()
    
    def create_widgets(self):
        super().create_widgets()
        self.info_frame = ctk.CTkFrame(self, height=self.height-4, bg_color=self.fg_color, fg_color=self.fg_color)
        
        self.download_progress_bar = ctk.CTkProgressBar(master=self.info_frame,
                                                        bg_color=self.fg_color,
                                                        height=8)
             
        self.download_percentage_label = ctk.CTkLabel(master=self.info_frame,
                                                      text="",
                                                      font=("arial", 12, "bold"),
                                                      bg_color=self.fg_color,
                                                      fg_color=self.fg_color,
                                                      text_color=self.text_color)
        
        self.status_label = ctk.CTkLabel(master=self.info_frame,
                                         text="",
                                         font=("arial", 12, "bold"),
                                         bg_color=self.fg_color,
                                         fg_color=self.fg_color,
                                         )
        
        self.redownload_btn = ctk.CTkButton(self ,text="⟳", 
                                            width=15 ,height=15,
                                            font=("arial", 20,"normal"),
                                            command = self.redownload_video,
                                            fg_color=self.fg_color,
                                            bg_color=self.fg_color,
                                            hover=False,
                                            )
        
    def set_theme(self):
        super().set_theme()
        self.redownload_btn.configure(text_color=self.theme_color)
        for video in self.downloading_videos:
            video.set_new_theme(self.theme_color)
    
    
    def configure_widget_sizes(self, e):
        self.info_frame.configure(width=self.winfo_width()/2 - 150)
    
    def place_widgets(self):
        super().place_widgets()
        
        self.title_label.place(x=50, y=10, height=20, width=-50, relwidth=0.5)
        self.channel_label.place(x=50, y=34, height=20, width=-50, relwidth=0.5)
        self.url_label.place(x=50, y=54, height=20, width=-50, relwidth=0.5)
        
        self.info_frame.place(relx=0.5, y=2, x=50)
        self.download_percentage_label.place(relx=0.5, anchor="n", y=12)
        self.download_percentage_label.configure(height=20)
        self.download_progress_bar.place(relwidth=1, y=40)
        self.status_label.place(relx=0.775, anchor="n", y=55)
        self.status_label.configure(height=20)

    
    def redownload_video(self):
        self.redownload_btn.place_forget()
        for video in self.downloading_videos:
            if video.download_failed:
                video.redownload_video()
        

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
                    length=video.length,
                    
                    download_directory = self.download_directory,
                    downloaded_callback_function = None
                    )
                )
            self.downloading_videos[-1].pack(fill="x", padx=(20,0), pady=1)
            self.downloading_videos[-1].remove_btn.configure(command=lambda video = self.downloading_videos[-1]: self.remove_video(video))
        self.view_btn.configure(state="normal")
        threading.Thread(target=self.progress_track).start()
    
    
    def progress_track(self):
        downloading_videos = self.downloading_videos.copy()
        while True:
            download_complete = True
            download_fails = False
            downloaded_count = 0
            for video in downloading_videos:
                if video not in self.downloading_videos:
                    downloading_videos.remove(video)
                    continue
                if video.download_failed:
                    download_complete = False
                    download_fails = True
                elif video.download_completed:
                    downloaded_count += 1
                    #downloading_videos.remove(video)
                else:
                    download_complete = False
            
            self.set_progress(downloaded_count/self.video_count)
            
            if not download_fails:
                self.set_download_runnning()
            if download_fails:
                self.set_download_failed()
            elif download_complete:
                break
            time.sleep(1)
        self.set_downloading_done()
    
    
    def set_progress(self, progress):
        self.download_progress_bar.set(progress)
        self.download_percentage_label.configure(text = str(round(progress*100, 2)) + " %")
    
    
    def set_download_failed(self):
        self.redownload_btn.place(relx=1, y=32, x=-80)
        self.status_label.configure(text="Failed", text_color=self.special_color)
    
    
    def set_downloading_done(self):
        self.status_label.configure(text="Downloaded", text_color=self.theme_color)
        self.downloaded_callback_function(self)
        self.kill()  


    def set_download_runnning(self):
        self.redownload_btn.place_forget()
        self.status_label.configure(text="Downloading", text_color=self.theme_color)
    
    def remove_video(self, video):
        self.downloading_videos.remove(video)
        self.complete_count_label.configure(text=len(self.downloading_videos))
        self.video_count -= 1
        video.pack_forget()
        video.kill()
    
    
    def kill(self):
        for video in self.downloading_videos:
            video.kill()
        super().kill()