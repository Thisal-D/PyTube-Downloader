#third party libs
import customtkinter as ctk
from widgets import  addedVideo, downloadingVideo, downloadedVideo


class app(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.root_w = self.winfo_width()
        self.root_h = self.winfo_height()
        self.reset_widgets = True
        self.loop_run = False
    

    def create_widgets(self):
        self.link_entry = ctk.CTkEntry(master=self, height=40, placeholder_text="Enter Youtube URL")
        self.add_btn =  ctk.CTkButton(master=self, text="Add +", height=40, width=100, command=self.add_video)
        
        self.scroll_frame_added = ctk.CTkScrollableFrame(master=self)
        self.scroll_frame_downloading = ctk.CTkScrollableFrame(master=self)
        self.scroll_frame_downloaded = ctk.CTkScrollableFrame(master=self)
        self.settings_btn = ctk.CTkButton(master=self, text="Setting")
        
        self.added_btn =  ctk.CTkButton(master=self, text="Added", height=40, command=lambda: self.place_frame(self.scroll_frame_added))
        self.downloading_btn =  ctk.CTkButton(master=self, text="Downloading", height=40, command=lambda: self.place_frame(self.scroll_frame_downloading))
        self.downloaded_btn =  ctk.CTkButton(master=self, text="Downloaded", height=40, command=lambda: self.place_frame(self.scroll_frame_downloaded))
        
    
    def place_forget_frames(self):
        self.scroll_frame_added.place_forget()
        self.scroll_frame_downloading.place_forget()
        self.scroll_frame_downloaded.place_forget()
        
        
    def place_frame(self, frame: ctk.CTkScrollableFrame):
        self.place_forget_frames()
        frame.place(y=90, x=10)
    
    
    def set_widgets_size(self):
        root_width = self.winfo_width()
        root_height = self.winfo_height()
        self.link_entry.configure(width = root_width-130)
        
        btn_width = (root_width-26)/3
        self.added_btn.configure(width=btn_width)
        self.downloading_btn.configure(width=btn_width)
        self.downloading_btn.place(x=btn_width+10+3)
        self.downloaded_btn.configure(width=btn_width)
        self.downloaded_btn.place(x=btn_width*2+10+6)
        
        frame_height = root_height - 105
        frame_width = root_width - 40
        self.scroll_frame_added.configure(height=frame_height, width=frame_width)
        self.scroll_frame_downloading.configure(height=frame_height, width=frame_width)
        self.scroll_frame_downloaded.configure(height=frame_height, width=frame_width)
        
    
    def loop(self):
        self.loop_run = True
        change = False

        if self.root_w != self.winfo_width() or self.root_h != self.winfo_height():
            change = True
            self.reset_widgets = True
            self.root_w = self.winfo_width()
            self.root_h = self.winfo_height()
    
        if self.reset_widgets and change==False:
            self.loop_run = False
            self.reset_widgets = False
            self.set_widgets_size()
        elif self.reset_widgets==False and change==False :
            self.loop_run = False
            pass
        else:
            self.after(200, self.loop)
            
        
    def check_root_size(self, e):
       if not self.loop_run :
           self.loop()
    
    
    def place_widgets(self):
        self.link_entry.place(x=10)
        self.add_btn.place(relx=1, x=-110)
        
        self.added_btn.place(y=45, x=10)
        self.downloading_btn.place(y=45)
        self.downloaded_btn.place(y=45)
        self.bind("<Configure>", self.check_root_size)

        
    def set_widgets_colors(self):
        self.configure(fg_color=("#ffffff", "#101010"))
        self.link_entry.configure(fg_color=("#ffffff", "#101010"), border_color=("#1f9bfd", "#1f9bfd"))
        self.add_btn.configure(fg_color=("#dedede", "#202020"), border_color=("#1f9bfd", "#1f9bfd"),
                               hover_color=("#eeeeee", "#252525"), text_color=("#1f9bfd", "#1f9bfd"),
                               border_width=2)
        
        self.added_btn.configure(fg_color=("#eeeeee","#202020"), hover_color=("#cccccc","#252525"), text_color=("#1f9bfd", "#1f9bfd"))
        self.downloading_btn.configure(fg_color=("#eeeeee","#202020"), hover_color=("#cccccc","#252525"), text_color=("#1f9bfd", "#1f9bfd"))
        self.downloaded_btn.configure(fg_color=("#eeeeee","#202020"), hover_color=("#cccccc","#252525"), text_color=("#1f9bfd", "#1f9bfd"))
        
        self.scroll_frame_added.configure(fg_color=("#ffffff", "#101010"),) #scrollbar_button_color="#1f9bfd")
        self.scroll_frame_downloading.configure(fg_color=("#ffffff", "#101010"),) #scrollbar_button_color="#1f9bfd")
        self.scroll_frame_downloaded.configure(fg_color=("#ffffff", "#101010"),) #scrollbar_button_color="#1f9bfd")

    
    def set_widgets_fonts(self):
        self.link_entry.configure(font=("arial", 15, "underline"))
        self.add_btn.configure(font=("arial", 15, "bold"))
        self.added_btn.configure(font=("arial", 15, "bold"))
        self.downloading_btn.configure(font=("arial", 15, "bold"))
        self.downloaded_btn.configure(font=("arial", 15, "bold"))
        
    
    def run(self):
        self.mainloop()
        
        
    def add_video(self):
        yt_url = self.link_entry.get()
        addedVideo.addedVideo(master=self.scroll_frame_added, height=70,
                    fg_color=("#ffffff", "#101010"),
                    bg_color=("#ffffff", "#101010"),
                    border_color=("#1f9bfd", "#1f9bfd"),
                    border_width=1, text_color=("#404040", "#aaaaaa"),
                    url=yt_url, download_btn_command=self.download_video).pack(fill="x", pady=2)
        
    def download_video(self, video: addedVideo.addedVideo):
        downloadingVideo.downloadingVideo(master=self.scroll_frame_downloading,
                                          height=70, fg_color=("#ffffff", "#101010"),
                                          bg_color=("#ffffff", "#101010"),
                                          border_color=("#1f9bfd", "#1f9bfd"),
                                          border_width=1, text_color=("#404040", "#aaaaaa"),
                                          url=video.url, download_quality=video.download_quallity,
                                          download_type=video.download_type, title=video.title,
                                          channel=video.channel, thumbnails=video.thumbnails,
                                          video_stream_data=video.video_stream_data).pack(fill="x", pady=2)
