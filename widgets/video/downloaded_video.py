from widgets.video import Video
import customtkinter as ctk
from tkinter import PhotoImage
from typing import List, Literal, Union, Callable
import os
from utils import (
    ValueConvertUtility
)
from services import LanguageManager
from settings import AppearanceSettings


class DownloadedVideo(Video):
    def __init__(
            self,
            root: ctk.CTk,
            master: Union[ctk.CTkFrame, ctk.CTkScrollableFrame],
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
            # download mode
            mode: Literal["video", "playlist"] = 'video',
            # state callbacks
            video_status_callback: Callable = None):

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
        # status callbacks
        self.video_status_callback = video_status_callback
        self.mode = mode

        super().__init__(
            root=root,
            master=master,
            width=width,
            height=height,
            thumbnails=thumbnails,
            video_title=video_title,
            channel=channel,
            channel_url=channel_url,
            length=length,
            video_url=video_url
        )

        self.set_video_data()

    def kill(self):
        if self.mode == "playlist":
            self.video_status_callback(self, "removed")
        super().kill()

    def create_widgets(self):
        super().create_widgets()

        self.download_type_label = ctk.CTkLabel(
            master=self
        )
        self.file_size_label = ctk.CTkLabel(
            master=self,
            text=ValueConvertUtility.convert_size(self.file_size, 2),
        )
        self.download_path_btn = ctk.CTkButton(
            master=self,
            text="📂",
            cursor="hand2",
            command=lambda: os.startfile("\\".join(self.download_path.split("\\")[0:-1])),
            hover=False,
        )

    def set_widgets_texts(self):
        super().set_widgets_texts()

        self.download_type_label.configure(
            text=f"{LanguageManager.data[self.download_type.lower()]} : {self.download_quality}"
        )

    def set_widgets_fonts(self):
        super().set_widgets_fonts()

        scale = AppearanceSettings.settings["scale_r"]

        self.download_type_label.configure(font=("arial", 12 * scale, "bold"))
        self.file_size_label.configure(font=("arial", 12 * scale, "normal"))
        self.download_path_btn.configure(font=("arial", 30 * scale, "bold"))

    def set_widgets_sizes(self):
        super().set_widgets_sizes()

        scale = AppearanceSettings.settings["scale_r"]

        self.download_type_label.configure(height=15 * scale)
        self.file_size_label.configure(height=15 * scale)
        self.download_path_btn.configure(height=15 * scale, width=30 * scale)

    def set_widgets_accent_color(self):
        super().set_widgets_accent_color()

        self.download_path_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

    def set_widgets_colors(self):
        super().set_widgets_colors()

        self.download_type_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.file_size_label.configure(text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"])
        self.download_path_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])

    def on_mouse_enter_self(self, event):
        super().on_mouse_enter_self(event)

        self.download_path_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])

    def on_mouse_leave_self(self, event):
        super().on_mouse_leave_self(event)

        self.download_path_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])

    def bind_widgets_events(self):
        super().bind_widgets_events()

        def on_mouse_enter_download_path_btn(event):
            self.download_path_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"])
            self.on_mouse_enter_self(event)

        def on_mouse_leave_download_path_btn(_event):
            self.download_path_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

        self.download_path_btn.bind("<Enter>", on_mouse_enter_download_path_btn)
        self.download_path_btn.bind("<Leave>", on_mouse_leave_download_path_btn)

    def place_widgets(self):
        super().place_widgets()

        scale = AppearanceSettings.settings["scale_r"]

        self.download_type_label.place(relx=1, x=-300 * scale, rely=0.3, anchor="w")
        self.download_path_btn.place(relx=1, x=-150 * scale, rely=0.5, anchor="w")
        self.file_size_label.place(relx=1, x=-300 * scale, rely=0.7, anchor="w")

    def configure_widget_sizes(self, _event):
        scale = AppearanceSettings.settings["scale_r"]
        self.info_frame.configure(
            width=(
                self.master.winfo_width() - (300 * scale) -
                (self.thumbnail_btn.winfo_width() + 5) - (10 * scale) -
                (20 * scale)
            )
        )
