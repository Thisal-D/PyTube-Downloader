import customtkinter as ctk
from typing import Callable, Any
from tkinter import filedialog
from services import (
    ThemeManager,
)
from settings import (
    AppearanceSettings,
    GeneralSettings
)
from utils import SettingsValidateUtility
from utils import FileUtility


class DownloadsPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            general_settings_change_callback: Callable = None):

        super().__init__(
            master=master,
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )

        self.download_path_label = ctk.CTkLabel(
            master=self,
            text="Download Path",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.dash1_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.download_path_entry = ctk.CTkEntry(
            master=self,
            justify="left",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )

        self.download_path_choose_button = ctk.CTkButton(
            master=self,
            text="📂",
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            hover=False,
            command=self.select_download_path,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
            )

        self.apply_changes_button = ctk.CTkButton(
            master=self,
            text="Apply",
            state="disabled",
            command=self.apply_general_settings,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )

        self.general_settings_change_callback = general_settings_change_callback
        self.configure_values()
        self.set_widgets_accent_color()
        self.set_widgets_sizes()
        self.set_widgets_fonts()
        self.place_widgets()
        self.bind_widgets_events()
        ThemeManager.register_widget(self)

    def apply_general_settings(self):
        GeneralSettings.settings["download_directory"] = FileUtility.format_path(self.download_path_entry.get())
        self.general_settings_change_callback()
        self.apply_changes_button.configure(state="disabled")

    def download_path_validate(self, _event):
        path = FileUtility.format_path(self.download_path_entry.get())
        if path != GeneralSettings.settings["download_directory"]:
            if SettingsValidateUtility.validate_download_path(path):
                self.apply_changes_button.configure(state="normal")
            else:
                self.apply_changes_button.configure(state="disabled")
        else:
            self.apply_changes_button.configure(state="disabled")

    def select_download_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.download_path_entry.delete(0, "end")
            self.download_path_entry.insert(0, directory)
            self.download_path_validate("event")

    def bind_widgets_events(self):
        self.download_path_entry.bind("<KeyRelease>", self.download_path_validate)

    def set_widgets_accent_color(self):
        self.download_path_choose_button.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.apply_changes_button.configure(
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.download_path_entry.configure(
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )

    def update_widgets_accent_color(self):
        self.set_widgets_accent_color()

    def update_widgets_colors(self):
        """Update colors for the widgets."""

    def place_widgets(self):
        scale = AppearanceSettings.settings["scale_r"]
        pady = 25 * scale

        self.download_path_label.grid(row=0, column=0, padx=(100, 0), pady=(50, 0), sticky="w")
        self.dash1_label.grid(row=0, column=1, padx=(30, 30), pady=(50, 0), sticky="w")
        self.download_path_entry.grid(row=0, column=2, pady=(50, 0), sticky="w")
        self.download_path_choose_button.grid(row=0, column=3, pady=(50, 0), padx=(20, 0), sticky="w")
        self.apply_changes_button.grid(row=1, column=3, pady=(pady, 0), padx=(20, 0), sticky="w")

    def set_widgets_sizes(self):
        scale = AppearanceSettings.settings["scale_r"]
        self.download_path_entry.configure(width=350 * scale, height=28 * scale)
        self.download_path_choose_button.configure(width=30 * scale, height=30 * scale)
        self.apply_changes_button.configure(width=50 * scale, height=24 * scale)

    def set_widgets_fonts(self):
        scale = AppearanceSettings.settings["scale_r"]
        title_font = ("Segoe UI", 13 * scale, "bold")
        self.download_path_label.configure(font=title_font)
        self.dash1_label.configure(font=title_font)

        value_font = ("Segoe UI", 13 * scale, "normal")
        self.download_path_entry.configure(font=value_font)

        button_font = ("Segoe UI", 13 * scale, "bold")
        self.apply_changes_button.configure(font=button_font)

        button_font2 = ("Segoe UI", 28 * scale, "bold")
        self.download_path_choose_button.configure(font=button_font2)

    def configure_values(self):
        self.download_path_entry.insert(0, GeneralSettings.settings["download_directory"])
