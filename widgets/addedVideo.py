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
                 width=None,
                 height=None,
                 url=None,
                 download_btn_command=passIt,
                         
                 bg_color=None,
                 fg_color=None,
                 text_color=None,
                 theme_color=None,
                 hover_color=None,
                 special_color=None,
                 ):
        
        self.loading_failed = False
        self.loading_loop_running = True
        self.download_btn_command = download_btn_command
        
        super().__init__(master=master, border_width=border_width, theme_color=theme_color, hover_color=hover_color,
                         special_color=special_color, width=width,
                         fg_color=fg_color, bg_color=bg_color, height=height ,url=url, text_color=text_color)
        
        threading.Thread(target=self.loading).start()
        threading.Thread(target=self.get_video_data).start()
    
    
    def loading(self):
        while not self.loading_done and not self.loading_failed :
            self.loading_loop_running = True
            self.thumbnail_btn.configure(text="."*addedVideo.index)
            self.update()
            time.sleep(0.7)
        if not self.loading_failed:
            self.set_video_data()
            self.set_fetch_data()
        self.loading_loop_running = False

    
    def get_video_data(self):
        try:
            self.video = pytube.YouTube(self.url)
            self.title = self.video.title
            self.channel = self.video.author
            self.length = self.video.length
            self.video_stream_data  = self.video.streams
            self.channel_url = self.video.channel_url
            self.thumbnails = getThumbnails(self.video)
            self.supported_download_types = sortDict(getSupportedDownloadTypes(self.video_stream_data))
            self.loading_done = True
            self.status_label.configure(text="Loaded")
        except Exception as error:
            print(error)
            self.loading_failed = False
            self.set_loading_failed()
    
    def select_download_option(self, e: str):
        self.download_quallity = e.replace(" ","").split("|")[0]
        if "kbps" in self.download_quallity:
            self.download_type = "Audio"
        else: 
            self.download_type = "Video"
            
            
    def set_fetch_data(self):
        self.resolutions_box.configure(values=formatToComboBoxValues(self.supported_download_types))
        self.resolutions_box.set(self.resolutions_box.cget("values")[0])
        self.select_download_option(self.resolutions_box.get())
        self.resolutions_box.configure(command=self.select_download_option)
        self.thumbnail_btn.configure(state="normal")
        self.channel_label.configure(state="normal")
        self.download_btn.configure(state="normal")
    
    

    def create_widgets(self):
        super().create_widgets()
        self.info_frame = ctk.CTkFrame(master=self,
                                       height=self.height-4,
                                       width=250,
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
                                         font=("arial", 12, "bold"),
                                         bg_color=self.fg_color,
                                         fg_color=self.fg_color,
                                         )
        
        self.reload_btn = ctk.CTkButton(self ,text="⟳", 
                                        width=15 ,height=15,
                                        font=("arial", 20, "normal"),
                                        command = self.reload_video,
                                        fg_color=self.fg_color,
                                        bg_color=self.fg_color,
                                        hover=False,
                                        )
        #  ⏯ ↺ ↻ ⏵ ⏸ ▷
        
    
    def set_theme(self):
        super().set_theme()
        self.download_btn.configure(border_color=self.theme_color)
        self.status_label.configure(text_color=self.theme_color)
        self.reload_btn.configure(text_color=self.theme_color)
    
    def place_widgets(self):
        super().place_widgets()
        self.info_frame.place(y=2, relx=1, x=-350)
        self.resolutions_box.place(y=15,x=20)
        self.download_btn.place(x=170 ,y=8)
        self.status_label.place(x=210, anchor="n", y=44)
        
    
    def set_loading_failed(self):
        self.loading_failed = True
        while self.loading_loop_running: self.master.master.master.update()
        self.thumbnail_btn.configure(text="...",
                                     disabledforeground=self.special_color)
        self.status_label.configure(text_color=self.special_color,
                                    text="Failed")
        self.reload_btn.place(relx=1, y=22, x=-80)
        
        
    def reload_video(self):
        self.loading_failed = False
        self.reload_btn.place_forget()
        self.thumbnail_btn.configure(disabledforeground=self.getColorBasedOnTheme(self.text_color))
        self.status_label.configure(text_color=self.theme_color, text="Loading")
        threading.Thread(target=self.loading).start()
        threading.Thread(target=self.get_video_data).start()