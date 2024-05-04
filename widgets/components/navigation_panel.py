import customtkinter as ctk
from typing import Any, List, Callable
from services import ThemeManager
from settings import (
    ThemeSettings,
    ScaleSettings,
    GeneralSettings
)


class NavigationPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            navigation_panels: List[ctk.CTkFrame] = None,
            navigation_button_on_click_callback: Callable = None,
            navigation_buttons_text: List[str] = None,
            width: int = None):

        super().__init__(
            master=master,
            fg_color=ThemeSettings.settings["root"]["fg_color"]["normal"],
            width=width * GeneralSettings.settings["scale_r"]
        )

        self.navigation_buttons = []
        self.navigation_buttons_clicked_state = []
        for i, button_text in enumerate(navigation_buttons_text):
            self.navigation_buttons.append(
                ctk.CTkButton(
                    master=self,
                    corner_radius=0,
                    text=button_text,
                    hover=False,
                    text_color=ThemeSettings.settings["settings_panel"]["nav_text_color"]
                )
            )
            self.navigation_buttons[-1].configure(
                command=lambda panel=navigation_panels[i], button=self.navigation_buttons[-1]:
                self.on_click_navigation_button(button, panel)
            )
            self.navigation_buttons_clicked_state.append(False)

        self.navigation_button_on_click_callback = navigation_button_on_click_callback
        ThemeManager.register_widget(self)
        self.width = width
        self.set_accent_color()
        self.set_widgets_sizes()
        self.set_widgets_fonts()
        self.place_widgets()
        # place appearance panel @ startup
        self.on_click_navigation_button(self.navigation_buttons[0], navigation_panels[0])

    def on_click_navigation_button(self, clicked_button: ctk.CTkButton, navigation_panel: ctk.CTkFrame):
        for i, navigation_button in enumerate(self.navigation_buttons):
            if clicked_button is navigation_button:
                self.navigation_buttons_clicked_state[i] = True
                navigation_button.configure(fg_color=ThemeSettings.settings["root"]["accent_color"]["normal"])
            else:
                self.navigation_buttons_clicked_state[i] = False
                navigation_button.configure(fg_color=ThemeSettings.settings["root"]["accent_color"]["hover"])
        self.navigation_button_on_click_callback(navigation_panel)

    def place_widgets(self):
        self.navigation_buttons[0].pack(pady=(50 * GeneralSettings.settings["scale_r"], 0))
        for navigation_button in self.navigation_buttons[1::]:
            navigation_button.pack()

    def set_widgets_fonts(self):
        scale = GeneralSettings.settings["scale_r"]
        button_font = ("Comic Sans MS", 14 * scale, "bold")
        for navigation_button in self.navigation_buttons:
            navigation_button.configure(font=button_font)

    def set_widgets_sizes(self):
        scale = GeneralSettings.settings["scale_r"]
        for navigation_button in self.navigation_buttons:
            navigation_button.configure(height=34 * scale, width=self.width * scale)

    def update_accent_color(self) -> None:
        self.set_accent_color()

    def set_accent_color(self):
        for i, navigation_button in enumerate(self.navigation_buttons):
            if not self.navigation_buttons_clicked_state[i]:
                navigation_button.configure(
                    fg_color=ThemeSettings.settings["root"]["accent_color"]["hover"]
                )
            else:
                navigation_button.configure(
                    fg_color=ThemeSettings.settings["root"]["accent_color"]["normal"]
                )

    def reset_widgets_colors(self):
        ...
