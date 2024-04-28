import customtkinter as ctk
from typing import Any, Dict, List, Callable
from services import ThemeManager


class NavigationPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            theme_settings: Dict = None,
            navigation_panels: List[ctk.CTkFrame] = None,
            navigation_button_on_click_callback: Callable = None,
            navigation_buttons_text: List[str] = None,
            width: int = 0):

        super().__init__(
            width=width,
            master=master,
            fg_color=theme_settings["root"]["fg_color"]["normal"]
        )

        self.navigation_buttons = []
        self.navigation_buttons_clicked_state = []
        for i, button_text in enumerate(navigation_buttons_text):
            self.navigation_buttons.append(
                ctk.CTkButton(
                    master=self,
                    width=width,
                    corner_radius=0,
                    text=button_text,
                    hover=False
                )
            )
            self.navigation_buttons[-1].configure(
                command=lambda panel=navigation_panels[i], button=self.navigation_buttons[-1]:
                self.on_click_navigation_button(button, panel)
            )
            self.navigation_buttons_clicked_state.append(False)

        self.navigation_button_on_click_callback = navigation_button_on_click_callback
        self.theme_settings = theme_settings
        ThemeManager.bind_widget(self)
        self.set_accent_color()
        self.place_widgets()
        # place appearance panel @ startup
        self.on_click_navigation_button(self.navigation_buttons[0], navigation_panels[0])

    def on_click_navigation_button(self, clicked_button: ctk.CTkButton, navigation_panel: ctk.CTkFrame):
        for i, navigation_button in enumerate(self.navigation_buttons):
            if clicked_button is navigation_button:
                self.navigation_buttons_clicked_state[i] = True
                navigation_button.configure(fg_color=self.theme_settings["root"]["accent_color"]["normal"])
            else:
                self.navigation_buttons_clicked_state[i] = False
                navigation_button.configure(fg_color=self.theme_settings["root"]["accent_color"]["hover"])
        self.navigation_button_on_click_callback(navigation_panel)

    def place_widgets(self):
        self.navigation_buttons[0].pack(pady=(50, 0))
        for navigation_button in self.navigation_buttons[1::]:
            navigation_button.pack()

    def update_accent_color(self, new_accent_color: Dict) -> None:
        self.theme_settings["root"]["accent_color"] = new_accent_color
        self.set_accent_color()

    def set_accent_color(self):
        for i, navigation_button in enumerate(self.navigation_buttons):
            if not self.navigation_buttons_clicked_state[i]:
                navigation_button.configure(
                    fg_color=self.theme_settings["root"]["accent_color"]["hover"]
                )
            else:
                navigation_button.configure(
                    fg_color=self.theme_settings["root"]["accent_color"]["normal"]
                )

    def reset_widgets_colors(self):
        ...
