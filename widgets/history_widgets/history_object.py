import customtkinter as ctk
from tkinter import PhotoImage
import tkinter as tk
from settings import AppearanceSettings
from services import ThemeManager
from utils import ImageUtility, FileUtility
from PIL import Image
import webbrowser
import os


class HistoryObject(ctk.CTkFrame):
    def __init__(
        self,
        master: ctk.CTkFrame = None,
        width: int = 130,
        no: int = None,
        channel: str = None,
        title: str = None,
        url: str = None,
        thumbnail_path_normal: str = None,
        thumbnail_path_hover: str = None,
        add_to_download_callback: callable = None,
        download_date: str = None):
        
        super().__init__(master=master, width=width, border_width=1)
        
        self.thumbnail_button: tk.Button = None
        self.label_frame: ctk.CTkFrame = None
        self.title_label: ctk.CTkLabel = None
        self.channel_label: ctk.CTkLabel = None
        self.download_date_label: ctk.CTkLabel = None
        
        self.width = width
        self.height = width / 16 * 9 + 15 * 3 + 20
        
        self.no = no
        self.channel = channel
        self.title = title
        self.url = url
        self.thumbnail_path_normal = thumbnail_path_normal
        self.thumbnail_path_hover = thumbnail_path_hover
        self.download_date = download_date
        self.thumbnail_normal: PhotoImage = None 
        self.thumbnail_hover: PhotoImage = None
        self.default_thumbnail_used = False
        self.add_to_download_callback = add_to_download_callback
        
        self.create_widgets()
        self.place_widgets()
        self.set_data()
        
        self.set_widgets_sizes()
        self.set_widgets_fonts()
        
        self.set_widgets_accent_color()
        self.tk_widgets_colors()
        self.set_widgets_colors()
        
        self.bind_widgets_events()
        
        ThemeManager.register_widget(self)
        
    def get_resized_thumbnail(self, thumbnail_path: str):
        thumbnail_size_for_video_history_object = (
            int(self.width) - 5,
            int((self.width/ 16*9))
        )
        
        thumbnail_image = Image.open(thumbnail_path)
        thumbnail_image = ImageUtility.resize_image(
            image=thumbnail_image,
            new_size=thumbnail_size_for_video_history_object
        )
        
        thumbnail_path = FileUtility.get_available_file_name("temp\\thumbnails\\history.png")
        thumbnail_image.save(FileUtility.get_available_file_name(thumbnail_path))

        return thumbnail_path
    
    def get_default_thumbnail(self):
        ...
        
    def configure_default_thumbnails(self):
        ...
    
    def set_data(self):
        if os.path.exists(self.thumbnail_path_normal) and self.thumbnail_path_normal != "":
            self.thumbnail_normal = PhotoImage(file=self.get_resized_thumbnail(self.thumbnail_path_normal))
            self.thumbnail_hover = PhotoImage(file=self.get_resized_thumbnail(self.thumbnail_path_hover))
        else:
            self.default_thumbnail_used = True
            self.get_default_thumbnail()
        
        self.thumbnail_button.configure(image=self.thumbnail_normal)
        self.title_label.configure(text=self.title)
        self.channel_label.configure(text=self.channel)
        self.download_date_label.configure(text=self.download_date)
        
    def bind_widgets_events(self):
        def on_mouse_enter_self(event):
            self.configure(border_color=AppearanceSettings.settings["root"]["accent_color"]["hover"])
            self.thumbnail_button.configure(image=self.thumbnail_hover)
         
        def on_mouse_leave_self(event):
            self.configure(border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
            self.thumbnail_button.configure(image=self.thumbnail_normal)

        self.bind("<Enter>", on_mouse_enter_self)
        self.bind("<Leave>", on_mouse_leave_self)
        
        self.thumbnail_button.bind("<Enter>", on_mouse_enter_self)
        self.thumbnail_button.bind("<Leave>", on_mouse_leave_self)
        
        self.title_label.bind("<Enter>", on_mouse_enter_self)
        self.title_label.bind("<Leave>", on_mouse_leave_self)
        
        self.channel_label.bind("<Enter>", on_mouse_enter_self)
        self.channel_label.bind("<Leave>", on_mouse_leave_self)
        
        self.download_date_label.bind("<Enter>", on_mouse_enter_self)
        self.download_date_label.bind("<Leave>", on_mouse_leave_self)
        
    def create_widgets(self):
        self.thumbnail_button = tk.Button(master=self, text="", relief="sunken", bd=0, cursor="hand2", command=lambda: webbrowser.open(self.url))
        self.label_frame = ctk.CTkFrame(master=self)
        self.title_label = ctk.CTkLabel(master=self.label_frame, text="", justify="left", anchor="w")
        self.channel_label = ctk.CTkLabel(master=self.label_frame, text="", justify="left", anchor="w")
        self.download_date_label = ctk.CTkLabel(master=self.label_frame, text="", justify="left", anchor="e")
        self.download_btn = ctk.CTkButton(master=self.label_frame, text="Download", command=lambda: self.add_to_download_callback(self.url))
        
    def place_widgets(self):
        scale = AppearanceSettings.settings["scale_r"]
        self.thumbnail_button.place(x=1, y=3)
            
        y = (self.width) / 16 * 9 + 10
        self.label_frame.place(x=4, y=y)
        
        y=0
        self.title_label.place(x=0, y=y)
        self.channel_label.place(x=0, y=(y + 15) * scale)
        self.download_date_label.place(x=0, y=(y + 30) * scale)
        self.download_btn.place(x=0, y=(y + 45) * scale)
    
    def set_widgets_colors(self):
        """Set colors for widgets."""
        self.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.label_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
    
    def tk_widgets_colors(self):
        self.thumbnail_button.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
            ),
            disabledforeground=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["text_color"]["normal"]
            ),
            activebackground=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
            )
        )
        
    def update_widgets_colors(self):
        """Update colors for widgets."""
        self.tk_widgets_colors()
        if self.default_thumbnail_used:
            self.configure_default_thumbnails()

    def set_widgets_accent_color(self):
        """Set accent color for widgets."""

        self.configure(border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        self.download_btn.configure(
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )

    def update_widgets_accent_color(self):
        """Update accent color for widgets."""
        self.set_widgets_accent_color()
        
    def set_widgets_sizes(self):
        """Set sizes for widgets."""
        scale = AppearanceSettings.settings["scale_r"]
        
        width = self.width
        height = 15 * scale
        self.title_label.configure(height=height, width=width - 8)
        self.channel_label.configure(height=height, width=width - 8)
        self.download_date_label.configure(height=height, width=width - 8)
        
        self.download_btn.configure(
            width = width - 8,
            height = 20 * scale
        )
        
        self.label_frame.configure(width=width-8, height=65*scale)
        
        widget_height = ((self.width/ 16*9)) + (3 * (15 * scale)) + (20 * scale) + 14
        self.configure(
            width = self.width,
            height = widget_height
        )
        
    def set_widgets_fonts(self):
        """Set fonts for widgets."""
        scale = AppearanceSettings.settings["scale_r"]

        self.title_label.configure(font=('arial', int(11 * scale), 'bold'))
        self.channel_label.configure(font=('arial', int(10 * scale), 'bold'))
        self.download_date_label.configure(font=('arial', int(10 * scale), 'normal'))
        
        self.download_btn.configure(font=('arial', int(11 * scale), 'bold'))
        
        