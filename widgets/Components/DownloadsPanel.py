import customtkinter as ctk
from typing import Dict, Callable, Any
from tkinter import filedialog
from Services import ThemeManager
from functions import validate_download_path, format_path


class DownloadsPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            theme_settings: Dict = None,
            general_settings: Dict = None,
            general_settings_change_callback: Callable = None,
            width: int = 0):

        super().__init__(
            width=width,
            master=master,
            fg_color=theme_settings["root"]["fg_color"]["normal"]
        )

        self.download_path_label = ctk.CTkLabel(
            master=self,
            text="Download Path"
        )
        self.dash1_label = ctk.CTkLabel(

            master=self,
            text=":"
        )
        self.download_path_entry = ctk.CTkEntry(
            master=self,
            justify="left",
            width=350
        )

        self.download_path_choose_button = ctk.CTkButton(
            master=self,
            width=30,
            height=30,
            font=("arial", 28, "bold"),
            text="📂",
            fg_color=theme_settings["root"]["fg_color"]["normal"],
            hover=False,
            command=self.select_download_path,
            )

        self.apply_changes_btn = ctk.CTkButton(
            master=self,
            text="Apply",
            state="disabled",
            height=24,
            width=50,
            command=self.apply_general_settings,
        )

        self.general_settings_change_callback = general_settings_change_callback
        self.theme_settings = theme_settings
        self.general_settings = general_settings
        self.configure_values()
        self.set_accent_color()
        self.place_widgets()
        self.bind_events()
        ThemeManager.bind_widget(self)

    def apply_general_settings(self):
        self.general_settings["download_directory"] = format_path(self.download_path_entry.get())
        self.general_settings_change_callback(self.general_settings)

    def download_path_validate(self, _event):
        path = format_path(self.download_path_entry.get())
        if path != self.general_settings["download_directory"]:
            if validate_download_path(path):
                self.apply_changes_btn.configure(state="normal")
            else:
                self.apply_changes_btn.configure(state="disabled")

    def select_download_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.download_path_entry.delete(0, "end")
            self.download_path_entry.insert(0, directory)
            self.download_path_validate("event")

    def bind_events(self):
        self.download_path_entry.bind("<KeyRelease>", self.download_path_validate)

    def set_accent_color(self):
        self.download_path_choose_button.configure(text_color=self.theme_settings["root"]["accent_color"]["normal"])
        self.apply_changes_btn.configure(
            fg_color=self.theme_settings["root"]["accent_color"]["normal"],
            hover_color=self.theme_settings["root"]["accent_color"]["hover"]
        )
        self.download_path_entry.configure(
            border_color=self.theme_settings["root"]["accent_color"]["normal"]
        )

    def update_accent_color(self, new_accent_color: Dict):
        self.theme_settings["root"]["accent_color"] = new_accent_color
        self.set_accent_color()

    def reset_widgets_colors(self):
        ...

    def place_widgets(self):
        self.download_path_label.place(y=50, x=50)
        self.dash1_label.place(y=50, x=150)
        self.download_path_entry.place(y=50, x=170)
        self.download_path_choose_button.place(y=42, x=540)
        self.apply_changes_btn.place(y=100, x=500)

    def configure_values(self):
        self.download_path_entry.insert(0, self.general_settings["download_directory"])
