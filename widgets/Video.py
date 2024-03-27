import customtkinter as ctk
from tkinter import PhotoImage
import tkinter as tk
import webbrowser
import time
import threading
class Video(ctk.CTkFrame):
    
    #remove_btn_normal_img = PhotoImage(file=r"./imgs/remove button/normal.png")
    #remove_btn_hover_img = PhotoImage(file=r"./imgs/remove button/hover.png")
    
    def __init__(self,
                 master,
                 border_width=None,
                 border_color=None,
                 bg_color=None,
                 fg_color=None,
                 height=None,
                 text_color=None,
                 url=None,
                 title = "---------",
                 channel = "---------",
                 thumbnails = (None, None),
                 loading_done = False,
                 ):
        super().__init__(master=master, border_width=border_width, border_color=border_color,
                         fg_color=fg_color, bg_color=bg_color, height=height)

        
        self.loading_done = loading_done
        self.url = url
        self.title = title
        self.channel = channel
        self.thumbnails = thumbnails
        self.supported_download_types = ["..........","..........",".........."]
        
        self.channel_url = ""
        
        self.theme = "-"
        self.fg_color = fg_color
        self.text_color = text_color
        self.bg_color = bg_color
        self.height = height
        
        
        
        self.create_widgets()
        self.place_widgets()
        threading.Thread(target=self.RunThemeTracker).start()
        self.set_video_data()


    def create_widgets(self):
        self.thumbnail_btn = tk.Button(master=self,
                                        bd=0,
                                        font=("arial", 14, "bold"),
                                        bg=self.get_color(self.fg_color),
                                        activebackground=self.get_color(self.fg_color),
                                        relief="sunken",
                                        state="disabled",
                                        command=lambda:webbrowser.open(self.url),
                                        )
        
        self.title_label = tk.Label(master=self ,anchor="w",
                                        text = "Title : ",
                                        font=('arial',10,'normal'),
                                        bg=self.get_color(self.fg_color),
                                        fg=self.get_color(self.text_color),
                                        #bg="red",
                                        )

        self.channel_label = tk.Button(master=self ,font=('arial',9,'bold') ,anchor="w",
                                        text = "Channel : ",
                                        bd=0,
                                        bg=self.get_color(self.fg_color),
                                        fg=self.get_color(self.text_color),
                                        command=lambda:webbrowser.open(self.channel_url),
                                        activebackground=self.get_color(self.fg_color),
                                        relief="sunken",
                                        state="disabled"
                                        )
        
        self.url_label = tk.Label(master=self ,anchor="w",
                                    bg=self.get_color(self.fg_color),
                                    fg=self.get_color(self.text_color),
                                    text=self.url, font=('arial',9,"underline"),
                                    #bg="blue",
                                    )
 
        self.remove_image = PhotoImage(file=r"./imgs/remove button/normal.png")
        self.remove_hover_image = PhotoImage(file=r"./imgs/remove button/hover.png")
        
        self.remove_btn = ctk.CTkButton(master=self,
                                        command=self.remove,
                                        text = None,
                                        image=self.remove_image,
                                        bg_color=self.bg_color,
                                        fg_color=self.fg_color,
                                        width=12, height=15,
                                        hover_color=self.fg_color)
        def remove_btn_enter(e):
            self.remove_btn.configure(image=self.remove_hover_image)
        def remove_btn_leave(e):
            self.remove_btn.configure(image=self.remove_image)
            
        self.remove_btn.bind("<Enter>", remove_btn_enter)
        self.remove_btn.bind("<Leave >", remove_btn_leave)
        
        self.bind("<Configure>", self.configure_widget_sizes)
        
        
    def get_color(self, color):
        if self.theme == "Dark":
            return color[1]
        return color[0]
    
    
    def set_theme(self):
        self.thumbnail_btn.configure(bg=self.get_color(self.bg_color), fg=self.get_color(self.text_color), activebackground=self.get_color(self.fg_color))
        self.title_label.configure(bg=self.get_color(self.bg_color), fg=self.get_color(self.text_color))
        self.url_label.configure(bg=self.get_color(self.bg_color), fg="#1f9bfd")
        self.channel_label.configure(bg=self.get_color(self.bg_color), fg=self.get_color(self.text_color), activebackground=self.get_color(self.fg_color))
        
        
    def RunThemeTracker(self):
        while True:
            if ctk.get_appearance_mode() != self.theme:
                self.theme = ctk.get_appearance_mode()
                self.set_theme()
            time.sleep(2)
    
    
    def configure_widget_sizes(self, e):
        self.remove_btn.place(x=self.winfo_width()-34,y=2)
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
            
            
    def remove(self):
        self.pack_forget()
        for childs_widget in self.winfo_children():
            childs_widget.destroy()
        self.destroy()
        del self