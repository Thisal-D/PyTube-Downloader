from widgets import (
    AppearancePanel,
    NetworkPanel,
    DownloadsPanel,
    NavigationPanel
)
from typing import Dict, Any, Callable
import customtkinter as ctk


class SettingPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            # color info
            theme_settings: Dict = None,
            # general info
            general_settings: Dict = None,
            # changes callbacks
            theme_settings_change_callback: Callable = None,
            general_settings_change_callback: Callable = None):
        super().__init__(
            master=master,
            fg_color=theme_settings["root"]["fg_color"]["normal"]
        )
        self.vr = ctk.CTkFrame(
            master=self,
            width=2,
        )

        self.appearance_panel = AppearancePanel(
            master=self,
            theme_settings_change_callback=theme_settings_change_callback,
            theme_settings=theme_settings,
        )

        self.network_panel = NetworkPanel(
            master=self,
            theme_settings=theme_settings,
            general_settings=general_settings,
            general_settings_change_callback=general_settings_change_callback
        )

        self.downloads_panel = DownloadsPanel(
            master=self,
            theme_settings=theme_settings,
            general_settings=general_settings,
            general_settings_change_callback=general_settings_change_callback
        )

        self.panels = [self.appearance_panel, self.network_panel, self.downloads_panel]

        self.navigation_panel = NavigationPanel(
            master=self,
            width=250,
            theme_settings=theme_settings,
            navigation_panels=self.panels,
            navigation_button_on_click_callback=self.place_panel,
            navigation_buttons_text=["Appearance", "Network", "Downloads"]
        )

        self.theme_settings = theme_settings
        self._accent_color = theme_settings["root"]["accent_color"]
        self.place_widgets()

    def place_widgets(self) -> None:
        self.navigation_panel.pack(side="left", fill="y")
        self.vr.pack(side="left", fill="y")
        self.appearance_panel.pack(side="right", fill="both", expand=True)

    def place_panel(self, selected_panel: ctk.CTkFrame) -> None:
        for panel in self.panels:
            if panel is not selected_panel:
                panel.pack_forget()
            else:
                selected_panel.pack(side="right", fill="both", expand=True)
