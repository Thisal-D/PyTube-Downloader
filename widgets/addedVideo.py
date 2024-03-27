from .Video import Video
import customtkinter as ctk
from functions.getThumbnails import getThumbnails
from functions.passIt import passIt
from functions.getSupportedDownloadTypes import getSupportedDownloadTypes
from functions.sortDict import sortDict
from functions.formatToComboBoxValues import formatToComboBoxValues
import time
import pytube
import threading

class addedVideo(Video):
    index = 0
    def configure_loading_display():
        def loading_count():
            while True:
                addedVideo.index += 1
                if addedVideo.index > 4:
                    addedVideo.index = 1
                time.sleep(0.7)
        threading.Thread(target=loading_count).start()
    
    
    def __init__(self, master,
                 border_width=None,
                 border_color=None,
                 bg_color=None,
                 fg_color=None,
                 height=None,
                 text_color=None,
                 url=None,
                 download_btn_command=passIt):
        
        self.download_btn_command = download_btn_command
        super().__init__(master=master, border_width=border_width, border_color=border_color,
                         fg_color=fg_color, bg_color=bg_color, height=height ,url=url, text_color=text_color)
        
        threading.Thread(target=self.loading).start()
        threading.Thread(target=self.get_video_data).start()
    
    
    def loading(self):
        while not self.loading_done :
            self.thumbnail_btn.configure(text="."*addedVideo.index)
            self.update()
            time.sleep(0.7)
        self.set_video_data()
        self.set_fetch_data()
    
    
    def get_video_data(self):
        self.video = pytube.YouTube(self.url)
        self.title = self.video.title
        self.channel = self.video.author
        self.length = self.video.length
        self.video_stream_data  = self.video.streams
        self.channel_url = self.video.channel_url
        self.thumbnails = getThumbnails(self.video)
        self.supported_download_types = sortDict(getSupportedDownloadTypes(self.video_stream_data))
        self.loading_done = True
    
    
    def select_download_option(self, e: str):
        self.download_quallity = e.replace(" ","").split("|")[0]
        if "kbps" in self.download_quallity:
            self.download_type = "audio"
        else: 
            self.download_type = "video"
            
            
    def set_fetch_data(self):
        self.resolutions_box.configure(values=formatToComboBoxValues(self.supported_download_types))
        self.resolutions_box.set(self.resolutions_box.cget("values")[0])
        self.select_download_option(self.resolutions_box.get())
        self.resolutions_box.configure(command=self.select_download_option)
        self.thumbnail_btn.configure(state="normal")
        self.channel_label.configure(state="normal")
        self.download_btn.configure(state="normal")
        
        
    def set_video_data(self):
        super().set_video_data()
        
        
    def create_widgets(self):
        super().create_widgets()
        self.info_frame = ctk.CTkFrame(master=self,
                                       height=self.height-4,
                                       width=250,
                                       bg_color=self.bg_color,
                                       fg_color=self.fg_color)
        self.resolutions_box = ctk.CTkComboBox(master=self.info_frame, values=[".........."])
        self.download_btn = ctk.CTkButton(master=self.info_frame, text="Download", width=80, height=25,
                                          border_width=2, fg_color=("#eeeeee", "#202020"), bg_color=self.bg_color,
                                          hover_color=("#dddddd","#353535"),
                                          border_color=("#dddddd", "#353535"), text_color=("#505050","#cccccc"),
                                          state="disabled",
                                          command=lambda:self.download_btn_command(self))
    
    
    def place_widgets(self):
        super().place_widgets()
        self.info_frame.place(y=2, relx=1, x=-300)
        self.resolutions_box.place(y=20)
        self.download_btn.place(x=150 ,y=22)
    
    
    def configure_widget_sizes(self, e):
        super().configure_widget_sizes(e)
