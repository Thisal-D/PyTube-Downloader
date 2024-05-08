from widgets.Video import Video
import customtkinter as ctk
from tkinter import PhotoImage
from typing import List, Literal, Union, Any, Callable, Dict
import os
from functions import (
    get_converted_size
)


class DownloadedVideo(Video):
    def __init__(
            self,
            master: Any = None,
            height: int = 0,
            width: int = 0,
            # video info
            video_title: str = "",
            channel: str = "",
            video_url: str = "",
            channel_url: str = "",
            file_size: int = 0,
            length: int = 0,
            thumbnails: List[PhotoImage] = (None, None),
            # download info
            download_path: str = "",
            download_quality: Literal["128kbps", "360p", "720p"] = "720p",
            download_type: Literal["Audio", "Video"] = "Video",
            # mode
            mode: Literal["video", "playlist"] = 'video',
            # state callbacks
            video_status_callback: Callable = None,
            # color info
            accent_color: Dict = None,
            theme_settings: Dict = None):

        # video info
        self.file_size: int = file_size
        # download info
        self.download_path: str = download_path
        self.download_quality: Literal["128kbps", "360p", "720p"] = download_quality
        self.download_type: Literal["Audio", "Video"] = download_type
        # widgets
        self.download_type_label: Union[ctk.CTkLabel, None] = None
        self.file_size_label: Union[ctk.CTkLabel, None] = None
        self.download_path_btn: Union[ctk.CTkButton, None] = None
        # state callbacks
        self.video_status_callback = video_status_callback
        self.mode = mode

        super().__init__(
            master=master,
            width=width,
            height=height,
            thumbnails=thumbnails,
            video_title=video_title,
            channel=channel,
            channel_url=channel_url,
            length=length,
            video_url=video_url,
            theme_settings=theme_settings,
            accent_color=accent_color,
        )

        self.set_video_data()

    def kill(self):
        if self.mode == "playlist":
            self.video_status_callback(self, "removed")
        super().kill()

    def create_widgets(self):
        super().create_widgets()

        self.download_type_label = ctk.CTkLabel(
            master=self,
            text=f"{self.download_type} : {self.download_quality}",
            height=15,
            font=("arial", 12, "bold"),
        )

        self.file_size_label = ctk.CTkLabel(
            master=self,
            text=get_converted_size(self.file_size, 2),
            font=("arial", 12, "normal"),
            height=15,
        )

        self.download_path_btn = ctk.CTkButton(
            master=self,
            text="📂",
            font=("arial", 30, "bold"),
            cursor="hand2",
            command=lambda: os.startfile("\\".join(self.download_path.split("\\")[0:-1])),
            hover=False,
            height=15,
            width=30
        )

    # place widgets
    def place_widgets(self):
        super().place_widgets()
        self.download_type_label.place(y=14, relx=1, x=-300)
        self.file_size_label.place(y=40, relx=1, x=-300)
        self.download_path_btn.place(y=12, relx=1, x=-150)

    # configure widgets sizes and place location depend on root width
    def configure_widget_sizes(self, e):
        ...

    # configure widgets colors
    def set_accent_color(self):
        super().set_accent_color()
        self.download_path_btn.configure(text_color=self.accent_color["normal"])

    def reset_widgets_colors(self):
        super().reset_widgets_colors()

    def set_widgets_colors(self):
        super().set_widgets_colors()
        self.download_type_label.configure(
            text_color=self.theme_settings["text_color"]["normal"]
        )
        self.file_size_label.configure(
            text_color=self.theme_settings["text_color"]["normal"]
        )
        self.download_path_btn.configure(
            fg_color=self.theme_settings["fg_color"]["normal"]
        )

    def on_mouse_enter_self(self, event):
        super().on_mouse_enter_self(event)
        self.download_path_btn.configure(fg_color=self.theme_settings["fg_color"]["hover"])

    def on_mouse_leave_self(self, event):
        super().on_mouse_leave_self(event)
        self.download_path_btn.configure(fg_color=self.theme_settings["fg_color"]["normal"])

    def bind_widget_events(self):
        super().bind_widget_events()

        def on_mouse_enter_download_path_btn(event):
            self.download_path_btn.configure(text_color=self.accent_color["hover"])
            self.on_mouse_enter_self(event)

        def on_mouse_leave_download_path_btn(_event):
            self.download_path_btn.configure(text_color=self.accent_color["normal"])
        self.download_path_btn.bind("<Enter>", on_mouse_enter_download_path_btn)
        self.download_path_btn.bind("<Leave>", on_mouse_leave_download_path_btn)
