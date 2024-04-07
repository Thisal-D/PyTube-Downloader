from .playList import playList
import pytube
from .addedVideo import addedVideo
import threading
import time
import customtkinter as ctk

class addedPlaylist(playList):
    def __init__(self,
                master=None,
                width=None,
                height=None,
                border_width=None,
                
                playlist_url=None,
                playlist_title = "---------",
                channel = "---------",
                channel_url = None,
                loading_done = False,
                
                download_btn_command = None,
                bg_color=None,
                fg_color=None,
                text_color=None,
                theme_color=None,
                hover_color=None,
                special_color=None,
                
                videos_thumbnails = None,
                playlist_thumbnails = None,):
        
        super().__init__(
                master=master,
                height=height,
                width=width,
                border_width=border_width,
                
                channel_url = channel_url,
                playlist_url=playlist_url,
                loading_done = loading_done,
                playlist_title=playlist_title,
                channel=channel,
                
                download_btn_command = download_btn_command,
                bg_color=bg_color,
                fg_color=fg_color,
                text_color=text_color,
                theme_color=theme_color,
                hover_color=hover_color,
                special_color=special_color,
                
                videos_thumbnails = videos_thumbnails,
                playlist_thumbnails = playlist_thumbnails)
        
        self.loading_failed_videos = []
        threading.Thread(target=self.get_playlist_data).start()
    
    
    def create_widgets(self):
        super().create_widgets()
        self.info_frame = ctk.CTkFrame(master=self,
                                        height=self.height-4,
                                        width=270,
                                        bg_color=self.fg_color,
                                        fg_color=self.fg_color)
        self.resolutions_box = ctk.CTkComboBox(master=self.info_frame, values=[".........."])
        
        #⇩ ⤓
        self.download_btn = ctk.CTkButton(master=self.info_frame, text="Download", width=80, height=25,
                                        border_width=2,
                                        fg_color=self.fg_color, bg_color=self.fg_color,
                                        hover_color=self.hover_color,
                                        text_color=self.text_color,
                                        state="disabled",
                                        command=lambda:self.download_btn_command(self))
        
        self.status_label = ctk.CTkLabel(master=self.info_frame,
                                        text="Loading",
                                        height=15,
                                        font=("arial", 13, "bold"),
                                        bg_color=self.fg_color,
                                        fg_color=self.fg_color,
                                        )
            
        self.reload_btn = ctk.CTkButton(self ,text="⟳", 
                                        width=15 ,height=15,
                                        font=("arial", 22, "normal"),
                                        command = self.reload_playlist,
                                        fg_color=self.fg_color,
                                        bg_color=self.fg_color,
                                        hover=False,
                                        )
    
    
    def place_widgets(self):
        super().place_widgets()
        self.info_frame.place(y=2, relx=1, x=-330)
        self.resolutions_box.place(y=25,x=0)
        self.download_btn.place(x=160 ,y=12)
        self.status_label.place(x=200, anchor="n", y=52)
    
    
    def reload_playlist(self):
        self.reload_btn.place_forget()
        self.status_label.configure(text_color=self.theme_color, text="Loading")
        if len(self.loading_failed_videos) != 0:
            for video in self.loading_failed_videos:
                if video.loading_failed:
                    video.reload_video()
                threading.Thread(target=self.check_videos_loading).start()
        else:
            for video_widget in self.playlist_item_frame.winfo_children():
                video_widget.pack_forget()
                del video_widget
            threading.Thread(target=self.get_playlist_data).start()
            
    
    def get_playlist_data(self):
        self.view_btn.configure(state="disabled")
        try:
            self.playlist = pytube.Playlist(self.playlist_url)

            self.video_count = self.playlist.length
            self.channel = self.playlist.owner
            self.playlist_title = self.playlist.title
            self.channel_url = self.playlist.owner_url
            
            self.view_btn.configure(state="normal")
            
            self.set_playlist_data()
            self.get_videos_data()
        except:
            self.set_loading_failed()
            
            
    def get_videos_data(self):
        for video_url in (self.playlist.video_urls):
            self.videos.append(addedVideo(master=self.playlist_item_frame, 
                        height=70,
                        width=self.playlist_item_frame.winfo_width()-20,
                        fg_color=self.fg_color,
                        bg_color=self.bg_color,
                        theme_color = self.theme_color,
                        text_color=self.text_color,      
                        hover_color=self.hover_color,
                        special_color=self.special_color,
                        border_width=1, 
                        url=video_url, download_btn_command=self.download_btn_command))
            
            self.videos[-1].pack(fill="x", padx=(20,0), pady=1)
        threading.Thread(target=self.check_videos_loading).start()
    
    def check_videos_loading(self):
        i = 0
        loaded = 0
        while i < len(self.videos):
            if not self.videos[i].loading_done and not self.videos[i].loading_failed:
                time.sleep(0.5)
                continue
            else:
                if not self.videos[i].loading_failed:
                    loaded += 1
                else:
                    self.loading_failed_videos.append(self.videos[i])
                i += 1
        if loaded==len(self.videos):
            self.set_loading_done()
        else:
            self.set_loading_failed()
            
            
    def set_loading_failed(self):
        self.status_label.configure(text="Failed", text_color=self.special_color)
        self.reload_btn.place(relx=1, y=32, x=-80)

    
    def set_loading_done(self):
        self.status_label.configure(text="Loaded")
        self.download_btn.configure(state="normal")