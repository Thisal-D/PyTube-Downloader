import tkinter as tk
import webbrowser
import customtkinter as ctk
from typing import List, Union, Any
from tkinter import PhotoImage
from functions import (
    get_converted_time,
)
from widgets.Components import ThumbnailButton
from services import ThemeManager


class Video(ctk.CTkFrame):
    def __init__(
            self,
            master: Any,
            width: int = 0,
            height: int = 0,
            # video info
            video_url: str = "",
            video_title: str = "-------",
            channel: str = "-------",
            thumbnails: List[PhotoImage] = (None, None),
            channel_url: str = "-------",
            length: int = 0):

        super().__init__(
            master=master,
            height=height,
            width=width,
            border_width=1,
            corner_radius=8,
        )

        self.height: int = height
        # video details
        self.video_url: str = video_url
        self.video_title: str = video_title
        self.channel: str = channel
        self.channel_url: str = channel_url
        self.length: int = length
        self.thumbnails: List[PhotoImage] = thumbnails
        # widgets
        self.url_label: Union[tk.Button, None] = None
        self.video_title_label: Union[tk.Button, None] = None
        self.channel_btn: Union[tk.Button, None] = None
        self.len_label: Union[ctk.CTkButton, None] = None
        self.thumbnail_btn: Union[ThumbnailButton, None] = None
        self.remove_btn: Union[ctk.CTkButton, None] = None
        # initialize the object
        self.create_widgets()
        self.set_widgets_colors()
        self.set_accent_color()
        self.reset_widgets_colors()
        self.place_widgets()
        self.bind_widget_events()
        # self append to theme manger
        ThemeManager.bind_widget(self)

    # display video data on widgets
    def set_video_data(self):
        self.video_title_label.configure(text=f"Title : {self.video_title}")
        self.channel_btn.configure(text=f"Channel : {self.channel}", state="normal")
        self.url_label.configure(text=self.video_url)
        self.len_label.configure(text=get_converted_time(self.length))

        self.thumbnail_btn.stop_loading_animation()
        self.thumbnail_btn.configure_thumbnail(thumbnails=self.thumbnails)
        self.thumbnail_btn.configure(state="normal")

        def on_mouse_enter_thumbnail_btn(event):
            self.on_mouse_enter_self(event)
            self.thumbnail_btn.on_mouse_enter(event)

        def on_mouse_leave_thumbnail_btn(event):
            self.on_mouse_leave_self(event)
            self.thumbnail_btn.on_mouse_leave(event)

        self.thumbnail_btn.bind("<Enter>", on_mouse_enter_thumbnail_btn)
        self.thumbnail_btn.bind("<Leave>", on_mouse_leave_thumbnail_btn)
        self.len_label.bind("<Enter>", on_mouse_enter_thumbnail_btn)
        self.len_label.bind("<Leave>", on_mouse_leave_thumbnail_btn)

    # kill itself
    def kill(self):
        ThemeManager.unbind_widget(self)
        self.pack_forget()
        self.destroy()

    # create widgets
    def create_widgets(self):
        self.thumbnail_btn = ThumbnailButton(
            master=self,
            font=("arial", 14, "bold"),
            state="disabled",
            command=lambda: webbrowser.open(self.video_url),
        )

        self.len_label = ctk.CTkLabel(
            master=self,
            width=1,
            height=1,
            font=("arial", 11, "bold"),
            text=get_converted_time(self.length)
        )

        self.video_title_label = tk.Label(
            master=self,
            anchor="w",
            font=('arial', 10, 'normal'),
            text=f"Title : {self.video_title}"
        )

        self.channel_btn = tk.Button(
            master=self, font=('arial', 9, 'bold'),
            anchor="w",
            bd=0,
            command=lambda: webbrowser.open(self.channel_url),
            relief="sunken",
            state="disabled",
            cursor="hand2",
            text=f"Channel : {self.channel}"
        )

        self.url_label = tk.Label(
            master=self, anchor="w",
            font=('arial', 10, "italic underline"),
            text=self.video_url
        )

        self.remove_btn = ctk.CTkButton(
            master=self,
            command=self.kill,
            text="X",
            font=("arial", 12, "bold"),
            width=12,
            height=20,
            border_spacing=0,
            hover=False,
        )

        self.bind("<Configure>", self.configure_widget_sizes)

    # set widgets colors
    def set_accent_color(self):
        self.configure(border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"])
        self.thumbnail_btn.configure(
            fg=(ThemeManager.theme_settings["root"]["accent_color"]["normal"]),
        )
        self.channel_btn.configure(activeforeground=ThemeManager.theme_settings["root"]["accent_color"]["normal"])
        self.url_label.configure(fg=ThemeManager.theme_settings["root"]["accent_color"]["normal"])

    def update_accent_color(self):
        self.set_accent_color()

    def reset_widgets_colors(self):
        self.thumbnail_btn.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]),
            disabledforeground=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["text_color"]["normal"]),
            activebackground=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])
        )

        self.video_title_label.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]),
            fg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["text_color"]["normal"])
        )

        self.url_label.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]),
        )

        self.channel_btn.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]),
            fg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["btn_text_color"]["normal"]),
            activebackground=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]),
        )

    def set_widgets_colors(self):
        self.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])
        self.remove_btn.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["error_color"]["normal"],
            text_color=ThemeManager.theme_settings["video_object"]["remove_btn_text_color"]["normal"]
        )

    def on_mouse_enter_self(self, event):
        self.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"],
            border_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"]
        )
        self.thumbnail_btn.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])
        )
        self.video_title_label.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])
        )
        self.channel_btn.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])
        )
        self.url_label.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])
        )

    def on_mouse_leave_self(self, event):
        self.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"],
            border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
        )
        self.thumbnail_btn.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])
        )
        self.video_title_label.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])
        )
        self.channel_btn.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])
        )
        self.url_label.configure(
            bg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])
        )

    def bind_widget_events(self):
        self.bind("<Enter>", self.on_mouse_enter_self)
        self.bind("<Leave>", self.on_mouse_leave_self)
        for child_widgets in self.winfo_children():
            child_widgets.bind("<Enter>", self.on_mouse_enter_self)
            child_widgets.bind("<Leave>", self.on_mouse_leave_self)
            try:
                for sub_child_widgets in child_widgets.winfo_children():
                    sub_child_widgets.bind("<Enter>", self.on_mouse_enter_self)
                    sub_child_widgets.bind("<Leave>", self.on_mouse_leave_self)
            except Exception as error:
                print(f"@1 Video.py > err : {error}")

        def on_mouse_enter_channel_btn(event):
            self.channel_btn.configure(
                fg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["btn_text_color"]["hover"]),
            )
            self.on_mouse_enter_self(event)

        def on_mouse_leave_channel_btn(_event):
            self.channel_btn.configure(
                fg=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["video_object"]["btn_text_color"]["normal"]),
            )

        self.channel_btn.bind("<Enter>", on_mouse_enter_channel_btn)
        self.channel_btn.bind("<Leave>", on_mouse_leave_channel_btn)

        def on_mouse_enter_remove_btn(event):
            self.remove_btn.configure(
                fg_color=ThemeManager.theme_settings["video_object"]["error_color"]["hover"],
                text_color=ThemeManager.theme_settings["video_object"]["remove_btn_text_color"]["hover"]
            )
            self.on_mouse_enter_self(event)

        def on_mouse_leave_remove_btn(event):
            self.remove_btn.configure(
                fg_color=ThemeManager.theme_settings["video_object"]["error_color"]["normal"],
                text_color=ThemeManager.theme_settings["video_object"]["remove_btn_text_color"]["normal"]
            )
            self.on_mouse_leave_self(event)

        self.remove_btn.bind("<Enter>", on_mouse_enter_remove_btn)
        self.remove_btn.bind("<Leave>", on_mouse_leave_remove_btn)

    # place widgets
    def place_widgets(self):
        self.remove_btn.place(relx=1, x=-25, y=3)
        self.thumbnail_btn.place(x=5, y=2, relheight=1, height=-4, width=int((self.height - 4) / 9 * 16))
        self.len_label.place(rely=1, y=-10, x=117, anchor="e")
        self.video_title_label.place(x=130, y=4, height=20, relwidth=1, width=-480)
        self.channel_btn.place(x=130, y=24, height=20, relwidth=1, width=-480)
        self.url_label.place(x=130, y=44, height=20, relwidth=1, width=-480)
    
    # configure widgets sizes and place location depend on root width
    def configure_widget_sizes(self, event):
        ...
