#third party libs
import customtkinter as ctk
from widgets import  addedVideo, downloadingVideo, downloadedVideo, settingPanel


class app(ctk.CTk):
    def __init__(self,
                 app_fg_color= ("#ffffff", "#101010"),
                 app_btn_fg_color= ("#eeeeee","#202020"),
                 app_btn_fg_hover_color= ("#cccccc","#252525"),
                 app_frame_fg_color = ("#ffffff", "#101010"),
                 app_widget_fg_color = ("#ffffff", "#101010"),
                 app_widget_text_color = ("#404040", "#aaaaaa"),
                 app_theme_color = "#1f9bfd",
                 app_special_color = "#fc4a46",
                 app_theme_colors = [],
                 ):
        
        super().__init__()
        self.root_w = self.winfo_width()
        self.root_h = self.winfo_height()
        
        self.app_fg_color = app_fg_color
        self.app_btn_fg_color = app_btn_fg_color
        self.app_btn_fg_hover_color = app_btn_fg_hover_color
        self.app_frame_fg_color = app_frame_fg_color
        self.app_widget_fg_color = app_widget_fg_color
        self.app_widget_text_color = app_widget_text_color
        self.app_theme_color = app_theme_color
        self.app_special_color = app_special_color
        self.app_theme_colors = app_theme_colors
        self.reset_widgets = True
        self.loop_run = False
        
        addedVideo.addedVideo.configure_loading_display()


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
        
        self.settings_panel = settingPanel.settingPanel(master=self, fg_color=self.app_fg_color, bg_color=self.app_fg_color,
                                                        text_color=self.app_widget_text_color, app_theme_colors=self.app_theme_colors,
                                                        theme_color=self.app_theme_color, call_back=self.theme_color_change_callback,
                                                       )
        self.setting_btn = ctk.CTkButton(master=self, text="⚡", border_spacing=0,
                                         hover=False, fg_color=self.app_fg_color, width=30, height=40,
                                         command=self.open_settings)
         
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
        self.link_entry.configure(width = root_width-156)
        
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
        self.link_entry.place(x=43)
        self.add_btn.place(relx=1, x=-110)
        
        self.added_btn.place(y=45, x=10)
        self.downloading_btn.place(y=45)
        self.downloaded_btn.place(y=45)
        self.setting_btn.place(x=-5)
        self.bind("<Configure>", self.check_root_size)

        
    def set_widgets_colors(self):
        self.configure(fg_color=self.app_fg_color)
        self.link_entry.configure(fg_color=self.app_fg_color, border_color=self.app_theme_color)
        self.add_btn.configure(fg_color=self.app_btn_fg_color, border_color=self.app_theme_color,
                               hover_color=self.app_btn_fg_hover_color, text_color=self.app_theme_color,
                               border_width=2)
        
        self.added_btn.configure(fg_color=self.app_btn_fg_color, hover_color=self.app_btn_fg_hover_color, text_color=self.app_theme_color)
        self.downloading_btn.configure(fg_color=self.app_btn_fg_color, hover_color=self.app_btn_fg_hover_color, text_color=self.app_theme_color)
        self.downloaded_btn.configure(fg_color=self.app_btn_fg_color, hover_color=self.app_btn_fg_hover_color, text_color=self.app_theme_color)
        
        self.scroll_frame_added.configure(fg_color=self.app_frame_fg_color)
        self.scroll_frame_downloading.configure(fg_color=self.app_frame_fg_color)
        self.scroll_frame_downloaded.configure(fg_color=self.app_frame_fg_color)
        self.setting_btn.configure(text_color=self.app_theme_color)
        

    
    def set_widgets_fonts(self):
        self.link_entry.configure(font=("arial", 15, "underline"))
        self.add_btn.configure(font=("arial", 15, "bold"))
        self.added_btn.configure(font=("arial", 15, "bold"))
        self.downloading_btn.configure(font=("arial", 15, "bold"))
        self.downloaded_btn.configure(font=("arial", 15, "bold"))
        self.setting_btn.configure(font=("arial", 25, "normal"))
        
    
    def run(self):
        self.mainloop()
        
        
    def add_video(self):
        yt_url = self.link_entry.get()
        addedVideo.addedVideo(master=self.scroll_frame_added, 
                              height=70,
                              width=self.scroll_frame_added.winfo_width(),
                              fg_color=self.app_widget_fg_color,
                              bg_color=self.app_fg_color,
                              theme_color = self.app_theme_color,
                              text_color=self.app_widget_text_color,      
                              hover_color=self.app_btn_fg_hover_color,
                              special_color=self.app_special_color,
                              
                              border_width=1, 
                              url=yt_url, download_btn_command=self.download_video).\
        pack(fill="x", pady=2)
        
        
    def download_video(self, video: addedVideo.addedVideo):
        downloadingVideo.downloadingVideo(master=self.scroll_frame_downloading,
                                          height=70,
                                          border_width=1,
                                          width=self.scroll_frame_downloading.winfo_width(),
                                          fg_color=self.app_widget_fg_color,
                                          bg_color=self.app_fg_color,
                                          theme_color=self.app_theme_color,
                                          text_color=self.app_widget_text_color,
                                          hover_color=self.app_btn_fg_hover_color,
                                          special_color=self.app_special_color,
                                          
                                          channel_url=video.channel_url,
                                          url=video.url,
                                          download_quality=video.download_quallity,
                                          download_type=video.download_type,
                                          title=video.title,
                                          channel=video.channel,
                                          thumbnails=video.thumbnails,
                                          video_stream_data=video.video_stream_data,
                                          downloaded_callback_function=self.downloaded_video).\
        pack(fill="x", pady=2)
        
    
    def downloaded_video(self, video: downloadingVideo.downloadingVideo):
        downloadedVideo.downloadedVideo(master=self.scroll_frame_downloaded,
                                        height=70,
                                        border_width=1,
                                        width=self.scroll_frame_downloaded.winfo_width(),
                                        download_quality=video.download_quality,
                                        download_type=video.download_type,
                                        
                                        fg_color=self.app_widget_fg_color,
                                        bg_color=self.app_fg_color,
                                        text_color=self.app_widget_text_color,
                                        hover_color=self.app_btn_fg_hover_color,
                                        theme_color=self.app_theme_color,
                                        special_color=self.app_special_color,
                                        
                                        thumbnails=video.thumbnails,
                                        title=video.title,
                                        channel=video.channel,
                                        channel_url=video.channel_url,
                                        url=video.url,
                                        download_path=video.download_file_name,
                                        file_size=video.total_bytes,
                                        ).\
        pack(fill="x", pady=2)
 
    
    def theme_color_change_callback(self, new_theme_color):
        self.app_theme_color = new_theme_color
        self.set_widgets_colors()
        for video_object in self.scroll_frame_added.winfo_children():
            if type(video_object) == addedVideo.addedVideo:
                video_object.set_new_theme(self.app_theme_color)
        
        for video_object in self.scroll_frame_downloading.winfo_children():
            if type(video_object) == downloadingVideo.downloadingVideo:
                video_object.set_new_theme(self.app_theme_color)
        
        for video_object in self.scroll_frame_downloaded.winfo_children():
            if type(video_object) == downloadedVideo.downloadedVideo:
                video_object.set_new_theme(self.app_theme_color)
                
    
    def open_settings(self):
        self.settings_panel.place(relwidth=1, relheight=1)
        self.setting_btn.configure(command=self.close_settings)
        
    def close_settings(self):
        self.settings_panel.place_forget()
        self.setting_btn.configure(command=self.open_settings)
    