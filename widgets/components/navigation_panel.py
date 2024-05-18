import customtkinter as ctk
from typing import Any, List, Callable
from services import ThemeManager, LanguageManager
from settings import (
    AppearanceSettings
)


class NavigationPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            navigation_panels: List[ctk.CTkFrame] = None,
            navigation_button_on_click_callback: Callable = None,
            navigation_buttons_texts: List[str] = None,
            width: int = None):

        super().__init__(
            master=master,
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            width=width
        )

        self.navigation_buttons_texts = navigation_buttons_texts
        self.navigation_buttons = []
        self.navigation_buttons_clicked_state = []
        for i in range(len(navigation_buttons_texts)):
            self.navigation_buttons.append(
                ctk.CTkButton(
                    master=self,
                    corner_radius=0,
                    text="",
                    hover=False,
                    text_color=AppearanceSettings.settings["settings_panel"]["nav_text_color"]
                )
            )
            self.navigation_buttons[-1].configure(
                command=lambda panel=navigation_panels[i], button=self.navigation_buttons[-1]:
                self.on_click_navigation_button(button, panel)
            )
            self.navigation_buttons_clicked_state.append(False)

        self.navigation_button_on_click_callback = navigation_button_on_click_callback
        self.width = width

        self.set_widgets_accent_color()
        self.set_widgets_sizes()
        self.set_widgets_texts()
        self.set_widgets_fonts()
        self.place_widgets()
        # place first panel @ startup
        self.on_click_navigation_button(self.navigation_buttons[0], navigation_panels[0])

        ThemeManager.register_widget(self)
        LanguageManager.register_widget(self)

    def on_click_navigation_button(self, clicked_button: ctk.CTkButton, navigation_panel: ctk.CTkFrame):
        for i, navigation_button in enumerate(self.navigation_buttons):
            if clicked_button is navigation_button:
                self.navigation_buttons_clicked_state[i] = True
                navigation_button.configure(fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
            else:
                self.navigation_buttons_clicked_state[i] = False
                navigation_button.configure(fg_color=AppearanceSettings.settings["root"]["accent_color"]["hover"])
        self.navigation_button_on_click_callback(navigation_panel)

    def place_widgets(self):
        self.navigation_buttons[0].pack(pady=(50 * AppearanceSettings.settings["scale_r"], 0))
        for navigation_button in self.navigation_buttons[1::]:
            navigation_button.pack()

    def set_widgets_texts(self):
        for i, button in enumerate(self.navigation_buttons):
            button.configure(text=LanguageManager.data[self.navigation_buttons_texts[i]])
            
    def update_widgets_text(self):
        self.set_widgets_texts()

    def set_widgets_fonts(self):
        scale = AppearanceSettings.settings["scale_r"]
        button_font = ("Comic Sans MS", int(14 * scale), "bold")
        for navigation_button in self.navigation_buttons:
            navigation_button.configure(font=button_font)

    def set_widgets_sizes(self):
        scale = AppearanceSettings.settings["scale_r"]
        for navigation_button in self.navigation_buttons:
            navigation_button.configure(height=int(36 * scale), width=self.width)

    def update_widgets_accent_color(self) -> None:
        self.set_widgets_accent_color()

    def set_widgets_accent_color(self):
        for i, navigation_button in enumerate(self.navigation_buttons):
            if not self.navigation_buttons_clicked_state[i]:
                navigation_button.configure(
                    fg_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
                )
            else:
                navigation_button.configure(
                    fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
                )

    def update_widgets_colors(self):
        """Update colors for the widgets."""
