from typing import Any, Callable
import customtkinter as ctk
from widgets import (
    AppearancePanel,
    NetworkPanel,
    DownloadsPanel,
    AboutPanel,
    NavigationPanel
)
from services import (
    ThemeManager
)
from settings import ThemeSettings


class SettingPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            # changes callbacks
            theme_settings_change_callback: Callable = None,
            general_settings_change_callback: Callable = None):
        super().__init__(
            master=master,
            fg_color=ThemeSettings.settings["root"]["fg_color"]["normal"]
        )

        self.appearance_panel = AppearancePanel(
            master=self,
            theme_settings_change_callback=theme_settings_change_callback,
        )

        self.network_panel = NetworkPanel(
            master=self,
            general_settings_change_callback=general_settings_change_callback
        )

        self.downloads_panel = DownloadsPanel(
            master=self,
            general_settings_change_callback=general_settings_change_callback
        )

        self.about_panel = AboutPanel(
            master=self
        )

        self.panels = [self.appearance_panel, self.network_panel, self.downloads_panel, self.about_panel]
        self.nav_buttons = ["Appearance", "Network", "Downloads", "About"]
        self.navigation_panel = NavigationPanel(
            master=self,
            navigation_panels=self.panels,
            navigation_button_on_click_callback=self.place_panel,
            navigation_buttons_text=self.nav_buttons
        )

        self.vertical_line = ctk.CTkFrame(
            master=self,
            width=2
        )

        (ThemeManager.register_widget(self))
        self.set_accent_color()
        self.place_widgets()

    def place_widgets(self) -> None:
        self.navigation_panel.pack(side="left", fill="y")
        self.vertical_line.pack(side="left", fill="y")
        self.appearance_panel.pack(side="right", fill="both", expand=True)

    def place_panel(self, selected_panel: ctk.CTkFrame) -> None:
        for panel in self.panels:
            if panel is not selected_panel:
                panel.pack_forget()
            else:
                selected_panel.pack(side="right", fill="both", expand=True)

    def set_accent_color(self):
        self.vertical_line.configure(fg_color=ThemeSettings.settings["root"]["accent_color"]["hover"])

    def update_accent_color(self):
        self.set_accent_color()

    def reset_widgets_colors(self):
        ...
