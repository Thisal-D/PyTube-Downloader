import customtkinter as ctk
from typing import Callable, List
from settings import AppearanceSettings
from services import ThemeManager


class ContextMenu(ctk.CTkFrame):

    child_widgets: List["ContextMenu"] = []

    @staticmethod
    def close_all_menus():
        for child_widget in ContextMenu.child_widgets:
            if child_widget.is_open:
                child_widget.place_forget()

    def __init__(
            self,
            master=None,
            width: int = 70,
            height: int = 100,
            font: tuple[str, int, str] = ("arial", 10, "bold"),
            options_texts: List[str] = None,
            options_commands: List[Callable] = None):

        super().__init__(master=master, width=width, height=height, border_width=1, corner_radius=0)

        self.width = width
        self.height = height
        self.font = font
        self.options_texts = options_texts
        self.options_commands = options_commands
        self.option_buttons: List[ctk.CTkButton] = []

        self.create_widgets()
        self.set_widgets_accent_color()
        self.set_widgets_colors()
        self.set_widgets_fonts()
        self.set_widgets_sizes()
        self.place_widgets()

        self.is_open = False

        ThemeManager.register_widget(self)
        ContextMenu.child_widgets.append(self)

    def bind_widgets_events(self, event: str, event_command: Callable):
        self.bind(event, event_command)
        self._canvas.bind(event, event_command)
        for option_button in self.option_buttons:
            option_button.bind(event, event_command)

    def set_open(self):
        self.is_open = True

    def set_closed(self):
        self.is_open = False

    def create_widgets(self):
        for i, option_text in enumerate(self.options_texts):
            button = ctk.CTkButton(self, text=option_text, command=self.options_commands[i])
            self.option_buttons.append(button)

    def set_widgets_accent_color(self):
        self.configure(border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        for option_button in self.option_buttons:
            option_button.configure(
                hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            )

    def update_widgets_accent_color(self):
        self.set_widgets_accent_color()

    def set_widgets_colors(self):
        self.configure(fg_color=AppearanceSettings.settings["root"]["fg_color"]["hover"])
        for option_button in self.option_buttons:
            option_button.configure(
                fg_color=AppearanceSettings.settings["root"]["fg_color"]["hover"],
                text_color=AppearanceSettings.settings["context_menu"]["text_color"]
            )

    def update_widgets_colors(self):
        """Update colors for the widgets."""

    def set_widgets_fonts(self):
        for option_button in self.option_buttons:
            option_button.configure(
                font=(self.font[0], self.font[1], self.font[2])
            )

    def set_widgets_sizes(self):
        button_height = int((self.height - 2) / len(self.options_texts))
        for option_button in self.option_buttons:
            option_button.configure(
                width=self.width,
                height=button_height,
                corner_radius=0
            )

    def place_widgets(self):
        self.option_buttons[0].pack(pady=1, padx=1)
        for button in self.option_buttons[1:-1]:
            button.pack(pady=(0, 0), padx=1)
        self.option_buttons[-1].pack(pady=1, padx=1)

    def configure(self, **kwargs):
        if "font" in kwargs:
            self.font = kwargs["font"]
            self.set_widgets_fonts()
        elif "width" in kwargs and "height" in kwargs:
            self.width = kwargs["width"]
            self.height = kwargs["height"]
            super().configure(**kwargs)
            self.set_widgets_sizes()
        else:
            super().configure(**kwargs)
