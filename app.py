import customtkinter as ctk
from widgets import  addedVideo, downloadingVideo, downloadedVideo,\
    settingPanel , addedPlayList, downloadingPlayList, downloadedPlayList

class app(ctk.CTk):
    def __init__(self,
                 app_fg_color= ("#ffffff", "#101010"),
                 app_btn_fg_color= ("#eeeeee","#202020"),
                 app_btn_fg_hover_color= ("#cccccc","#252525"),
                 app_frame_fg_color = ("#ffffff", "#101010"),
                 app_widget_fg_color = ("#ffffff", "#101010"),
                 app_widget_text_color = ("#404040", "#aaaaaa"),
                 app_theme_color = "#1f9bfd",
                 app_theme_mode = "System",
                 app_special_color = "#fc4a46",
                 app_theme_colors = [],
                 download_directory = "",
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
        self.app_theme_mode = app_theme_mode
        self.reset_widgets = True
        self.loop_run = False
        self.download_directory = download_directory
        self.selected_download_mode = "video"#"video"
        
        self.downloading = False
        self.downloaded = False
        self.added = False
        
    def create_widgets(self):
        self.link_entry = ctk.CTkEntry(master=self, height=40, placeholder_text="Enter Youtube URL")
        self.add_btn =  ctk.CTkButton(master=self, text="Add +", height=40, width=100, command=self.add_video)
        
        self.video_radio_btn = ctk.CTkRadioButton(master=self, text="Video", fg_color=self.app_theme_color,
                                                  radiobutton_width=16, radiobutton_height=16,
                                                  width=60, height=18,
                                                  command=lambda:self.select_download_mode("video"))
        self.video_radio_btn.select()
        self.playlist_radio_btn = ctk.CTkRadioButton(master=self, text="Playlist", fg_color=self.app_theme_color,
                                                     radiobutton_width=16, radiobutton_height=16,
                                                     width=60, height=18,
                                                     command=lambda:self.select_download_mode("playlist"))
        
        self.scroll_frame_added = ctk.CTkScrollableFrame(master=self)
        self.scroll_frame_downloading = ctk.CTkScrollableFrame(master=self)
        self.scroll_frame_downloaded = ctk.CTkScrollableFrame(master=self)
        self.settings_btn = ctk.CTkButton(master=self, text="Setting")
        
        self.added_btn =  ctk.CTkButton(master=self, text="Added", height=40, command=lambda: self.place_frame(self.scroll_frame_added, "added"))
        self.downloading_btn =  ctk.CTkButton(master=self, text="Downloading", height=40, command=lambda: self.place_frame(self.scroll_frame_downloading, "downloading"))
        self.downloaded_btn =  ctk.CTkButton(master=self, text="Downloaded", height=40, command=lambda: self.place_frame(self.scroll_frame_downloaded, "downloaded"))

        font_style = ("arial", 18, "bold")
        self.added_frame_label = ctk.CTkLabel(master=self, text="Added videos will display here.", font=font_style,
                                              text_color=self.app_theme_color,)
        self.downloading_frame_label = ctk.CTkLabel(master=self, text="Downloading videos will display here.", font=font_style,
                                                    text_color=self.app_theme_color,)
        self.downloaded_frame_label = ctk.CTkLabel(master=self, text="Downloaded videos will display here.", font=font_style,
                                                   text_color=self.app_theme_color,)
        
        self.settings_panel = settingPanel.settingPanel(master=self, fg_color=self.app_fg_color, bg_color=self.app_fg_color,
                                                        text_color=self.app_widget_text_color,
                                                        directory_change_call_back=self.directory_change_callback,
                                                        theme_color_change_call_back=self.theme_color_change_callback,
                                                       )
        self.setting_btn = ctk.CTkButton(master=self, text="⚡", border_spacing=0, 
                                         hover=False, fg_color=self.app_fg_color, width=30, height=40,
                                         command=self.open_settings)
         
    
    def place_forget_frames(self):
        self.scroll_frame_added.place_forget()
        self.scroll_frame_downloading.place_forget()
        self.scroll_frame_downloaded.place_forget()
    
    
    def place_forget_labels(self, label:str = None):
        if label == None:
            self.added_frame_label.place_forget()
            self.downloading_frame_label.place_forget()
            self.downloaded_frame_label.place_forget()
        elif label == "added":
            self.added_frame_label.place_forget()
        elif label == "downloading":
            self.downloading_frame_label.place_forget()
        elif label == "downloaded":
            self.downloaded_frame_label.place_forget()
            
            
    def place_label(self, frame_name: str):
        self.place_forget_labels()
        if frame_name == "added" and self.added is not True:
            self.added_frame_label.place(y=45, rely=0.5, relx=0.5, anchor="center")
        elif frame_name == "downloading" and self.downloading is not True:
            self.downloading_frame_label.place(y=45, rely=0.5, relx=0.5, anchor="center")
        elif frame_name == "downloaded" and self.downloaded is not True:
            self.downloaded_frame_label.place(y=45, rely=0.5, relx=0.5, anchor="center")
            
            
    def place_frame(self, frame: ctk.CTkScrollableFrame, frame_name: str):
        self.place_forget_frames()
        frame.place(y=90, x=10)
        self.place_label(frame_name)
    
    def set_widgets_size(self):
        root_width = self.winfo_width()
        root_height = self.winfo_height()
        self.link_entry.configure(width = root_width-250)
        
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
        self.video_radio_btn.place(relx=1, x=-190,y=2)
        self.playlist_radio_btn.place(relx=1, x=-190, y=22)
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
        
        
    def select_download_mode(self, download_mode):
        self.selected_download_mode = download_mode
        if download_mode == "playlist":
            self.video_radio_btn.deselect()
        else:
            self.playlist_radio_btn.deselect()
    
   
        
    def add_video(self):
        self.added = True
        self.place_forget_labels("added")
        yt_url = self.link_entry.get()
        if self.selected_download_mode == "video":
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
        else:
            addedPlayList.addedPlayList(master=self.scroll_frame_added, 
                              height=85,
                              width=self.scroll_frame_added.winfo_width(),
                              fg_color=self.app_widget_fg_color,
                              bg_color=self.app_fg_color,
                              theme_color = self.app_theme_color,
                              text_color=self.app_widget_text_color,      
                              hover_color=self.app_btn_fg_hover_color,
                              special_color=self.app_special_color,
                              download_btn_command=self.download_playlist,
                              video_download_btn_command=self.download_video,
                              border_width=1, 
                              playlist_url=yt_url).\
            pack(fill="x", pady=2)
        
        
    def download_video(self, video: addedVideo.addedVideo):
        self.downloading = True
        self.place_forget_labels("downloading")
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
                                          download_quality=video.download_quality,
                                          download_type=video.download_type,
                                          title=video.title,
                                          channel=video.channel,
                                          thumbnails=video.thumbnails,
                                          video_stream_data=video.video_stream_data,
                                          length=video.length,
                                          
                                          download_directory = self.download_directory,
                                          downloaded_callback_function=self.downloaded_video).\
        pack(fill="x", pady=2)
    
    
    def download_playlist(self, playlist: addedPlayList.addedPlayList):
        self.downloading = True
        self.place_forget_labels("downloading")
        downloadingPlayList.downloadingPlayList(master=self.scroll_frame_downloading,
                                                height=85,
                                                width=self.scroll_frame_downloading.winfo_width(),
                                                border_width=1,
                                                
                                                
                                                fg_color=self.app_widget_fg_color,
                                                bg_color=self.app_fg_color,
                                                theme_color=self.app_theme_color,
                                                text_color=self.app_widget_text_color,
                                                hover_color=self.app_btn_fg_hover_color,
                                                special_color=self.app_special_color,
                                                
                                                channel_url=playlist.channel_url,
                                                channel=playlist.channel,
                                                playlist_title=playlist.playlist_title,
                                                video_count=playlist.video_count,
                                                playlist_url=playlist.playlist_url,
                                                
                                                download_directory = self.download_directory,
                                                videos=playlist.videos,
                                                downloaded_callback_function = self.downloaded_playlist
                                                ).\
            pack(fill="x", pady=2)
              
    
    def downloaded_video(self, video: downloadingVideo.downloadingVideo):
        self.downloaded = True
        self.place_forget_labels("downloaded")
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
                                        length=video.length
                                        ).\
        pack(fill="x", pady=2)
    
    def downloaded_playlist(self, playlist: downloadingPlayList.downloadingPlayList):
        self.downloaded = True
        self.place_forget_labels("downloaded")
        downloadedPlayList.downloadedPlayList(master=self.scroll_frame_downloaded,
                                                height=85,
                                                width=self.scroll_frame_downloaded.winfo_width(),
                                                border_width=1,
                                                
                                                fg_color=self.app_widget_fg_color,
                                                bg_color=self.app_fg_color,
                                                theme_color=self.app_theme_color,
                                                text_color=self.app_widget_text_color,
                                                hover_color=self.app_btn_fg_hover_color,
                                                special_color=self.app_special_color,
                                                
                                                channel_url=playlist.channel_url,
                                                channel=playlist.channel,
                                                playlist_title=playlist.playlist_title,
                                                video_count=playlist.video_count,
                                                playlist_url=playlist.playlist_url,
                                                
                                                videos=playlist.downloading_videos).\
            pack(fill="x", pady=2)
        
    
    def theme_color_change_callback(self, new_theme_color):
        self.app_theme_color = new_theme_color
        self.set_widgets_colors()
        for video_object in self.scroll_frame_added.winfo_children():
            if type(video_object) == addedVideo.addedVideo or type(video_object) == addedPlayList.addedPlayList:
                video_object.set_new_theme(self.app_theme_color)
        
        for video_object in self.scroll_frame_downloading.winfo_children():
            if type(video_object) == downloadingVideo.downloadingVideo or type(video_object) == downloadingPlayList.downloadingPlayList:
                video_object.set_new_theme(self.app_theme_color)
        
        for video_object in self.scroll_frame_downloaded.winfo_children():
            if type(video_object) == downloadedVideo.downloadedVideo or type(video_object) == downloadedPlayList.downloadedPlayList:
                video_object.set_new_theme(self.app_theme_color)
        
        self.added_frame_label.configure(text_color=self.app_theme_color)
        self.downloading_frame_label.configure(text_color=self.app_theme_color)
        self.downloaded_frame_label.configure(text_color=self.app_theme_color)
        self.video_radio_btn.configure(fg_color=self.app_theme_color)
        self.playlist_radio_btn.configure(fg_color=self.app_theme_color)
        
    
    def directory_change_callback(self, download_directory):
        self.download_directory = download_directory
    
    def open_settings(self):
        self.settings_panel.place(relwidth=1, relheight=1)
        self.setting_btn.configure(command=self.close_settings)
        
    def close_settings(self):
        self.settings_panel.place_forget()
        self.setting_btn.configure(command=self.open_settings)
    
    def run(self):
        self.mainloop()
