from typing import Dict, Any, Callable
import customtkinter as ctk
from Services import ThemeManager
from functions import validate_simultaneous_count


class NetworkPanel(ctk.CTkFrame):
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

        self.load_label = ctk.CTkLabel(
            master=self,
            text="Maximum Simultaneous Loads"
        )
        self.dash1_label = ctk.CTkLabel(
            master=self,
            text=":"
        )
        self.simultaneous_load_entry = ctk.CTkEntry(
            master=self,
            justify="right"
        )

        self.simultaneous_load_range_label = ctk.CTkLabel(
            master=self,
            text="(1-10)"
        )

        self.download_label = ctk.CTkLabel(
            master=self,
            text="Maximum Simultaneous Downloads"
        )
        self.dash2_label = ctk.CTkLabel(
            master=self,
            text=":"
        )
        self.simultaneous_download_entry = ctk.CTkEntry(
            master=self,
            justify="right"
        )

        self.simultaneous_download_range_label = ctk.CTkLabel(
            master=self,
            text="(1-10)"
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
        self.set_accent_color()
        self.place_widgets()
        self.bind_widgets()
        self.configure_values()
        ThemeManager.bind_widget(self)

    def apply_general_settings(self):
        self.general_settings["simultaneous_loads"] = int(self.simultaneous_load_entry.get())
        self.general_settings["simultaneous_downloads"] = int(self.simultaneous_download_entry.get())
        self.general_settings_change_callback(self.general_settings)

    def simultaneous_load_count_check(self, _event):
        value = self.simultaneous_load_entry.get()
        if validate_simultaneous_count(value) and int(value) != self.general_settings["simultaneous_loads"]:
            self.apply_changes_btn.configure(state="normal")
        else:
            self.apply_changes_btn.configure(state="disabled")

    def simultaneous_download_count_check(self, _event):
        value = self.simultaneous_download_entry.get()
        if validate_simultaneous_count(value) and int(value) != self.general_settings["simultaneous_downloads"]:
            self.apply_changes_btn.configure(state="normal")
        else:
            self.apply_changes_btn.configure(state="disabled")

    def bind_widgets(self):
        self.simultaneous_load_entry.bind("<KeyRelease>", self.simultaneous_load_count_check)
        self.simultaneous_download_entry.bind("<KeyRelease>", self.simultaneous_download_count_check)

    # set default values to widgets
    def configure_values(self):
        self.simultaneous_load_entry.insert(
            "end",
            self.general_settings["simultaneous_loads"]
        )
        self.simultaneous_download_entry.insert(
            "end",
            self.general_settings["simultaneous_downloads"]
        )

    def update_accent_color(self, new_accent_color: Dict):
        self.theme_settings["root"]["accent_color"] = new_accent_color
        self.set_accent_color()

    def set_accent_color(self):
        self.apply_changes_btn.configure(
            fg_color=self.theme_settings["root"]["accent_color"]["normal"],
            hover_color=self.theme_settings["root"]["accent_color"]["hover"]
        )
        self.simultaneous_load_entry.configure(
            border_color=self.theme_settings["root"]["accent_color"]["normal"],
        )
        self.simultaneous_download_entry.configure(
            border_color=self.theme_settings["root"]["accent_color"]["normal"],
        )

    def place_widgets(self):
        self.load_label.place(y=50, x=50)
        self.dash1_label.place(y=50, x=270)
        self.simultaneous_load_entry.place(y=50, x=300)
        self.simultaneous_load_range_label.place(y=50, x=450)

        self.download_label.place(y=100, x=50)
        self.dash2_label.place(y=100, x=270)
        self.simultaneous_download_entry.place(y=100, x=300)
        self.simultaneous_download_range_label.place(y=100, x=450)

        self.apply_changes_btn.place(y=150, x=380)

    def reset_widgets_colors(self):
        ...
