import customtkinter as ctk
import tkinter as tk
import pytube
from .Video import Video


class playList(ctk.CTkFrame):
    def __init__(self,
                 master=None,
                 border_width=None,
                 width=None,
                 height=None,
                 url=None,
                 title = "---------",
                 channel = "---------",
                 thumbnails = (None, None),
                 channel_url = None,
                 loading_done = False,
                 
                 bg_color=None,
                 fg_color=None,
                 text_color=None,
                 theme_color=None,
                 hover_color=None,
                 special_color=None):
        super().__init__(master=master)
        
        self.master = master
        self.border_width = border_width
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.height = height
        self.width = width
        self.create_widgets()
        
    
    def create_widgets(self):
        self.playlist_videos = Video(master=self.master , border_width=self.border_width, corner_radius=8,
                         fg_color=self.fg_color, bg_color=self.bg_color, height=self.height, width=self.width)
        self.playlist_item_frame = ctk.CTkFrame(self, fg_color="red")
        
    
    def place_widgets(self):
        self.playlist_videos.pack()
        self.playlist_item_frame.pack(padx=10)