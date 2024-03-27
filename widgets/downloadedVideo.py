from .Video import Video
import customtkinter as ctk

class downloadedVideo(Video):
    def __init__(self, master, 
                 border_width=None,
                 border_color=None,
                 bg_color=None, fg_color=None,
                 height=None, text_color=None, url=None,
                 resolution=None, file_size=None):
        
        self.resolution = resolution
        self.file_size = file_size
        super().__init__(master, border_width, border_color, bg_color, fg_color, height, text_color, url)

    
    def create_widgets(self):
        super().create_widgets()
        self.resolution_label = ctk.CTkLabel(master=self, 
                                              text=self.resolution, fg_color=self.fg_color,
                                              height=1,
                                              font=("arial", 10, "normal"),
                                              text_color=self.text_color, bg_color=self.bg_color)
        self.file_size_label = ctk.CTkLabel(master=self, 
                                              text="1.32 GB", fg_color=self.fg_color, 
                                              font=("arial", 10, "normal"),
                                              height=1,
                                              text_color=self.text_color, bg_color=self.bg_color)
        self.video_len_label = ctk.CTkLabel(master=self, 
                                              text="15 min", fg_color=self.fg_color,
                                              font=("arial", 12, "normal"),
                                              height=1,
                                              text_color=self.text_color, bg_color=self.bg_color)
        
    def place_widgets(self):
        super().place_widgets()
        self.resolution_label.place(y=7)
        self.file_size_label.place(y=28)
        self.video_len_label.place(y=48)
        
    def configure_widget_sizes(self, e):
        super().configure_widget_sizes(e)
        self.resolution_label.place(x=self.winfo_width()-250)
        self.file_size_label.place(x=self.winfo_width()-250)  
        self.video_len_label.place(x=self.winfo_width()-250)    
          