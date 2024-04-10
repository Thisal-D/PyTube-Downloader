from .Video import Video
import customtkinter as ctk
import os
from functions.getConvertedSize import getConvertedSize

class downloadedVideo(Video):
    def __init__(self, master,
                 border_width=None,
                 height=None,
                 width=None,
                 download_quality=None,
                 download_type=None,
                 
                 title=None,
                 channel=None,
                 thumbnails=(None,None),
                 loading_done = True,
                 url=None,
                 channel_url=None,
                 file_size=0,
                 download_path="",
                 length=None,
                 
                 bg_color=None,
                 fg_color=None,
                 text_color=None,
                 theme_color=None,
                 hover_color=None,
                 special_color=None
                 ):
        
        self.download_path = download_path
        self.file_size=file_size
        self.download_quality = download_quality
        self.download_type = download_type
        super().__init__(master=master, border_width=border_width, theme_color=theme_color,hover_color=hover_color,
                         channel_url=channel_url,special_color=special_color,width=width, length=length,
                         fg_color=fg_color, bg_color=bg_color, height=height ,url=url, text_color=text_color,
                         thumbnails=thumbnails, title=title, channel=channel, loading_done=loading_done)
        self.set_state()
        
    
    def create_widgets(self):
        super().create_widgets()
        self.download_type_label = ctk.CTkLabel(master=self, 
                                              text=self.download_type + " : "+ self.download_quality,
                                              fg_color=self.fg_color,
                                              height=15,
                                              font=("arial", 12, "bold"),
                                              text_color=self.text_color, bg_color=self.fg_color)
        self.file_size_label = ctk.CTkLabel(master=self, 
                                              text=getConvertedSize(self.file_size,2)  , fg_color=self.fg_color, 
                                              font=("arial", 12, "normal"),
                                              height=15,
                                              text_color=self.text_color, bg_color=self.fg_color)
        #📁🗀📂🖿🗁
        self.download_path_btn = ctk.CTkButton(master=self,
                                               text="📂",
                                               font=("arial", 30, "bold"),
                                               cursor="hand2",
                                               command=lambda:os.startfile("\\".join(self.download_path.split("\\")[0:-1])),
                                               hover=False,
                                               bg_color=self.fg_color,
                                               fg_color=self.fg_color, height=15,width=30)
        
        
    def set_theme(self):
        super().set_theme()
        self.download_path_btn.configure(text_color=self.theme_color)
        
        
    def place_widgets(self):
        super().place_widgets()
        self.download_type_label.place(y=14)
        self.file_size_label.place(y=40)
        self.download_path_btn.place(y=12)
        
        
    def configure_widget_sizes(self, e):
        super().configure_widget_sizes(e)
        self.download_type_label.place(x=self.winfo_width()-300)
        self.file_size_label.place(x=self.winfo_width()-300)  
        self.download_path_btn.place(x=self.winfo_width()-150)    
    
    
    def set_state(self):
        self.thumbnail_btn.configure(state="normal")
        self.channel_label.configure(state="normal")
        self.thumbnail_btn.configure(command=lambda:os.startfile(self.download_path))