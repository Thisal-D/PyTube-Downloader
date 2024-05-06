import customtkinter as ctk
import tkinter as tk
from typing import Tuple, Any, Union
from PIL import Image
import webbrowser
from services import ThemeManager
from settings import (
    ThemeSettings,
    GeneralSettings
)


class ContributorProfileWidget:
    def __init__(
            self,
            master: Any = None,
            width: int = 35,
            height: int = 35,
            user_name: str = "",
            profile_url: str = "",
            profile_images_paths: Tuple[str, str] = None):

        self.profile_images = (
            ctk.CTkImage(
                Image.open(profile_images_paths[0]),
                size=(width * GeneralSettings.settings["scale_r"], height * GeneralSettings.settings["scale_r"])
            ),
            ctk.CTkImage(
                Image.open(profile_images_paths[1]),
                size=(width * GeneralSettings.settings["scale_r"], height * GeneralSettings.settings["scale_r"])
            )
        )

        self.profile_pic_button = ctk.CTkButton(
            master=master,
            hover=False,
            text="",
            command=lambda: webbrowser.open(profile_url),
            image=self.profile_images[0],
            fg_color=ThemeSettings.settings["root"]["fg_color"]["normal"],
        )

        self.user_name_button = ctk.CTkButton(
            master=master,
            text=user_name,
            hover=False,
            width=1,
            command=lambda: webbrowser.open(profile_url),
            fg_color=ThemeSettings.settings["root"]["fg_color"]["normal"],
            text_color=ThemeSettings.settings["settings_panel"]["text_color"]
        )

        self.profile_url_button = ctk.CTkButton(
            master=master,
            text=profile_url,
            hover=False,
            width=1,
            command=lambda: webbrowser.open(profile_url),
            fg_color=ThemeSettings.settings["root"]["fg_color"]["normal"],
            text_color=ThemeSettings.settings["settings_panel"]["text_color"]
        )

        self.hr = tk.Frame(
            master=master,
            height=1,
        )

        self.width = width
        self.height = height

        self.set_widgets_fonts()
        self.set_widgets_sizes()
        self.bind_events()
        self.set_accent_color()
        ThemeManager.register_widget(self)

    def bind_events(self):
        self.profile_pic_button.bind(
            "<Enter>",
            lambda event_: self.profile_pic_button.configure(image=self.profile_images[1])
        )

        self.profile_pic_button.bind(
            "<Leave>",
            lambda event_: self.profile_pic_button.configure(image=self.profile_images[0])
        )

    def set_accent_color(self):
        self.hr.configure(
            bg=ThemeSettings.settings["root"]["accent_color"]["normal"]
        )
        
    def update_accent_color(self):
        self.set_accent_color()
        
    def reset_widgets_colors(self):
        ...

    def set_widgets_sizes(self):
        scale = GeneralSettings.settings["scale_r"]
        self.profile_pic_button.configure(
            width=self.width * scale,
            height=self.height * scale
        )

    def set_widgets_fonts(self):
        scale = GeneralSettings.settings["scale_r"]
        title_font = ("Segoe UI", 13 * scale, "bold")
        self.user_name_button.configure(font=title_font)

        value_font = ("Segoe UI", 13 * scale, "normal")
        self.profile_url_button.configure(font=value_font)

    def grid(
            self,
            row: int = 0,
            pady: int = 3,
            padx: Tuple[
                Union[int, Tuple[int, int]],
                Union[int, Tuple[int, int]],
                Union[int, Tuple[int, int]]] = None) -> None:
        scale = GeneralSettings.settings["scale_r"]
        self.profile_pic_button.grid(row=row, column=0, padx=padx[0] * scale, pady=pady * scale, sticky="w")
        self.user_name_button.grid(row=row, column=1, padx=padx[1] * scale, pady=pady * scale, sticky="w")
        self.profile_url_button.grid(row=row, column=2, padx=padx[2] * scale, pady=pady * scale, sticky="w")
        self.hr.grid(columnspan=3, row=row+1, column=0, sticky="ew", padx=50 * scale)
        