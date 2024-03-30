import customtkinter as ctk
import tkinter as tk
import webbrowser
import time
import threading
from functions.getColor import getColor


class Video(ctk.CTkFrame):
    def __init__(self,
                 master,
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
        
        super().__init__(master=master, border_width=border_width, corner_radius=8,
                         fg_color=fg_color, bg_color=bg_color, height=height, width=width)

        self.loading_done = loading_done
        self.url = url
        self.title = title
        self.channel = channel
        self.thumbnails = thumbnails
        self.supported_download_types = ["..........","..........",".........."]
        
        self.channel_url = channel_url
        
        self.theme = "-"
        self.fg_color = fg_color
        self.text_color = text_color
        self.height = height
        self.theme_color = theme_color
        self.hover_color = hover_color
        self.special_color = special_color
        
        self.create_widgets()
        self.place_widgets()
        threading.Thread(target=self.RunThemeTracker).start()
        self.set_video_data()


    def create_widgets(self):
        self.thumbnail_btn = tk.Button(master=self,
                                       bd=0,
                                       font=("arial", 14, "bold"),
                                       bg=self.getColorBasedOnTheme(self.fg_color),
                                       relief="sunken",
                                       state="disabled",
                                       cursor="hand2",
                                       command=lambda:webbrowser.open(self.url)
                                       )
        
        self.title_label = tk.Label(master=self ,anchor="w",
                                    text = "Title : ",
                                    font=('arial',10,'normal'),
                                    bg=self.getColorBasedOnTheme(self.fg_color),
                                    fg=self.getColorBasedOnTheme(self.text_color)
                                    )

        self.channel_label = tk.Button(master=self ,font=('arial',9,'bold'), 
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
        
        self.url_label = tk.Label(master=self ,anchor="w",
                                  bg=self.getColorBasedOnTheme(self.fg_color),
                                  text=self.url, font=('arial',9,"underline"),
                                  )
 
        self.remove_btn = ctk.CTkButton(master=self,
                                        command=self.kill,
                                        text="X",
                                        font=("arial", 12, "bold"),
                                        fg_color=self.fg_color,
                                        bg_color=self.fg_color,
                                        border_width=2,
                                        border_color=self.special_color,
                                        text_color=self.special_color,
                                        width=12, height=10,
                                        border_spacing=0,
                                        hover=False,
                                        )
        
        self.bind("<Configure>", self.configure_widget_sizes)
        
        
    def set_theme(self):
        self.configure(border_color=self.theme_color)
        self.thumbnail_btn.configure(bg=self.getColorBasedOnTheme(self.fg_color), 
                                     fg=self.getColorBasedOnTheme(self.text_color),
                                     disabledforeground=self.getColorBasedOnTheme(self.text_color),
                                     activebackground=self.getColorBasedOnTheme(self.fg_color))
        self.title_label.configure(bg=self.getColorBasedOnTheme(self.fg_color),
                                   fg=self.getColorBasedOnTheme(self.text_color))
        self.url_label.configure(bg=self.getColorBasedOnTheme(self.fg_color),
                                 fg=self.theme_color)
        self.channel_label.configure(bg=self.getColorBasedOnTheme(self.fg_color),
                                     fg=self.getColorBasedOnTheme(self.text_color),
                                     activebackground=self.getColorBasedOnTheme(self.fg_color),
                                     activeforeground=self.theme_color,)
        
    
    def getColorBasedOnTheme(self, color):
        return getColor(color, self.theme)
    
    
    def RunThemeTracker(self):
        while True:
            if ctk.get_appearance_mode() != self.theme:
                self.theme = ctk.get_appearance_mode()
                self.set_theme()
            time.sleep(2)
    
    
    def configure_widget_sizes(self, e):
        self.remove_btn.place(x=self.winfo_width()-24,y=4)
        self.title_label.place(width=self.winfo_width()-450)
        self.url_label.place(width=self.winfo_width()-450)
        self.channel_label.place(width=self.winfo_width()-450)

    
    def place_widgets(self):
        self.thumbnail_btn.place(x=5, y=2, relheight=1, height=-4, width=int((self.height-4)/9*16))
        self.title_label.place(x=130, y=4, height=20)
        self.channel_label.place(x=130, y=24, height=20)
        self.url_label.place(x=130, y=44, height=20)
        

    def set_video_data(self):
        self.title_label.configure(text="Title : "+self.title)
        self.channel_label.configure(text="Channel : "+self.channel)
        self.url_label.configure(text=self.url)
        if self.loading_done:
            self.thumbnail_btn.configure(image=self.thumbnails[0], text="")
            def thumbnail_hover_img_set(e):
                self.thumbnail_btn.configure(image=self.thumbnails[1], text="")
            def thumbnail_img_set(e):
                self.thumbnail_btn.configure(image=self.thumbnails[0], text="")
            self.thumbnail_btn.bind("<Enter>",thumbnail_hover_img_set)
            self.thumbnail_btn.bind("<Leave>",thumbnail_img_set)    
            
            
    def kill(self):
        for child_widget in self.winfo_children():
            for sub_child_widget in child_widget.winfo_children():
                sub_child_widget.destroy()
            child_widget.destroy()
        self.place_forget()
        self.destroy()
        
        
    def set_new_theme(self, new_theme_color):
        self.theme_color = new_theme_color
        self.set_theme()