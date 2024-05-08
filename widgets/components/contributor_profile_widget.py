import customtkinter as ctk
import tkinter as tk
from typing import Tuple, Any, Union
from PIL import Image
import webbrowser
from services import ThemeManager
from settings import ThemeSettings


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
            ctk.CTkImage(Image.open(profile_images_paths[0]), size=(width, height)),
            ctk.CTkImage(Image.open(profile_images_paths[1]), size=(width, height))
        )

        self.profile_pic_button = ctk.CTkButton(
            master=master,
            width=width,
            height=height,
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
        
    def grid(
            self,
            row: int = 0,
            pady: int = 3,
            padx: Tuple[
                Union[int, Tuple[int, int]],
                Union[int, Tuple[int, int]],
                Union[int, Tuple[int, int]]] = None) -> None:
        
        self.profile_pic_button.grid(row=row, column=0, padx=padx[0], pady=pady, sticky="w")
        self.user_name_button.grid(row=row, column=1, padx=padx[1], pady=pady, sticky="w")
        self.profile_url_button.grid(row=row, column=2, padx=padx[2], pady=pady, sticky="w")
        self.hr.grid(columnspan=3, row=row+1, column=0, sticky="ew", padx=50)
        