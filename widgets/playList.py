import customtkinter as ctk
import tkinter as tk
import pytube
import time
import threading
from functions.getColor import getColor
import webbrowser

class playList(ctk.CTkFrame):
    def __init__(self,
                    master=None,
                    width=None,
                    height=None,
                    border_width=None,
                    
                    channel_url = None,
                    playlist_url=None,
                    loading_done = False,
                    playlist_title = "---------",
                    channel = "---------",
                    video_count = "?",
                
                    download_btn_command = None,
                    bg_color=None,
                    fg_color=None,
                    text_color=None,
                    theme_color=None,
                    hover_color=None,
                    special_color=None,
                    
                    videos_thumbnails = None,
                    playlist_thumbnails = None,):
        
        super().__init__(master=master, fg_color=fg_color)
        
        self.height = height
        self.width = width
        self.border_width = border_width
        
        self.channel_url = channel_url
        self.channel = channel
       
        self.playlist_url = playlist_url
        self.playlist_thumbnails = playlist_thumbnails
        self.videos_thumbnails = videos_thumbnails
        self.playlist_title =playlist_title
        
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.theme = "-"
        self.theme_color = theme_color
        self.text_color = text_color
        self.special_color = special_color
        self.hover_color = hover_color
        self.download_btn_command = download_btn_command
        self.videos = []
        
        self.video_count = video_count
        
        self.create_widgets()
        self.place_widgets()
        self.set_playlist_data()
        threading.Thread(target=self.RunThemeTracker).start()
        
    
    
    def create_widgets(self):
        self.playlist_info_widget = ctk.CTkFrame(master=self, border_width=self.border_width,
                                                 fg_color=self.fg_color, bg_color=self.bg_color,
                                                 border_color=self.theme_color, height=85)
        
        self.view_btn = ctk.CTkButton(master=self.playlist_info_widget,
                                       font=('arial', 18, 'bold'),
                                       text = ">",
                                       width=1,
                                       height=1,
                                       bg_color=self.fg_color,
                                       fg_color=self.fg_color,
                                       hover=False,
                                       text_color=self.theme_color,
                                       command=self.view_videos,
                                       state="disabled",
                                       cursor="hand2",
                                       )
        """
        self.thumbnail_btn = tk.Button(master=self.playlist_info_widget,
                                       bd=0,
                                       font=("arial", 14, "bold"),
                                       bg=self.getColorBasedOnTheme(self.bg_color),
                                       relief="sunken",
                                       state="disabled",
                                       cursor="hand2",
                                       command=lambda:webbrowser.open(self.playlist_url)
                                       )
        """
        self.title_label = tk.Label(master=self.playlist_info_widget ,anchor="w",
                                    text = "Title : ",
                                    font=('arial',10,'bold'),
                                    bg=self.getColorBasedOnTheme(self.fg_color),
                                    fg=self.getColorBasedOnTheme(self.text_color)
                                    )

        self.channel_label = tk.Button(master=self.playlist_info_widget,
                                       font=('arial',9,'bold'), 
                                       anchor="w",
                                       text = "Channel : ",
                                       bd=0,
                                       bg=self.getColorBasedOnTheme(self.fg_color),
                                       fg=self.getColorBasedOnTheme(self.text_color),
                                       command=lambda:webbrowser.open(self.channel_url),
                                       relief="sunken",
                                       state="disabled",
                                       cursor="hand2",
                                       )
        
        self.url_label = tk.Label(master=self.playlist_info_widget ,anchor="w",
                                  bg=self.getColorBasedOnTheme(self.fg_color),
                                  text=self.playlist_url, font=('arial',11,"underline"),
                                  )
 
        self.remove_btn = ctk.CTkButton(master=self.playlist_info_widget,
                                        command=self.kill,
                                        text="X",
                                        font=("arial", 10, "bold"),
                                        fg_color=self.fg_color,
                                        bg_color=self.fg_color,
                                        border_width=2,
                                        border_color=self.special_color,
                                        text_color=self.special_color,
                                        width=12, height=10,
                                        border_spacing=0,
                                        hover=False,
                                        )
        
        self.complete_count_label = ctk.CTkLabel(master=self.playlist_info_widget, text="?",
                                               width=15 ,height=15,
                                               font=("arial", 13, "normal"),
                                               fg_color=self.fg_color,
                                               bg_color=self.fg_color,
                                               text_color=self.theme_color, justify="right")
        
        self.playlist_item_frame = ctk.CTkFrame(self, fg_color=self.fg_color)
        
        self.bind("<Configure>", self.configure_widget_sizes)
    
    def getColorBasedOnTheme(self, color):
        return getColor(color, self.theme)
    
    
    def RunThemeTracker(self):
        while True:
            if ctk.get_appearance_mode() != self.theme:
                self.theme = ctk.get_appearance_mode()
                self.set_theme()
            time.sleep(2)
            
            
    def set_theme(self):
        self.configure(border_color=self.theme_color)
        
        #self.thumbnail_btn.configure(bg=self.getColorBasedOnTheme(self.fg_color), 
        #                            fg=self.getColorBasedOnTheme(self.text_color),
        #                            disabledforeground=self.getColorBasedOnTheme(self.text_color),
        #                            activebackground=self.getColorBasedOnTheme(self.fg_color))
        self.title_label.configure(bg=self.getColorBasedOnTheme(self.fg_color),
                                fg=self.getColorBasedOnTheme(self.text_color))
    
        self.url_label.configure(bg=self.getColorBasedOnTheme(self.fg_color),
                                fg=self.theme_color)
    
        self.channel_label.configure(bg=self.getColorBasedOnTheme(self.fg_color),
                                    fg=self.getColorBasedOnTheme(self.text_color),
                                    activebackground=self.getColorBasedOnTheme(self.fg_color),
                                    activeforeground=self.theme_color,)
            
    
    def place_widgets(self):
        self.playlist_info_widget.pack(fill="x")
        self.view_btn.place(y=55, x=10)
        #self.thumbnail_btn.place(x=25, y=2, relheight=1, height=-4, width=int((self.height-4)/9*16))
        self.title_label.place(x=50, y=10, height=20)
        self.channel_label.place(x=50, y=34, height=20)
        self.url_label.place(x=50, y=54, height=20)
        self.complete_count_label.place(relx=1, x=-60, rely=1, y=-25)

    
    def hide_videos(self):
        self.view_btn.configure(command=self.view_videos, text=">", font=('arial', 18, 'bold'))
        self.playlist_item_frame.pack_forget()
    
    
    def view_videos(self):
        self.view_btn.configure(command=self.hide_videos, text="V",  font=('arial', 13, 'bold'))
        self.playlist_item_frame.pack(padx=10, fill="x", pady=2)
        
        
    def configure_widget_sizes(self, e):
        self.remove_btn.place(x=self.winfo_width()-24,y=4)
        self.title_label.place(width=self.winfo_width()-420)
        self.url_label.place(width=self.winfo_width()-420)
        self.channel_label.place(width=self.winfo_width()-420)
        
    
    def set_playlist_data(self):
        self.complete_count_label.configure(text=f"{self.video_count}")
        self.title_label.configure(text="Title : "+self.playlist_title)
        self.channel_label.configure(text="Channel : "+self.channel)
        self.url_label.configure(text=self.playlist_url)
    
        
    def kill(self):
        self.pack_forget()
        self.destroy()