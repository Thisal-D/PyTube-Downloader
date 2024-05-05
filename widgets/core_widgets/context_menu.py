import customtkinter as ctk
import pyautogui
from services import ThemeManager
from settings import (
    ThemeSettings,
    GeneralSettings
)


class ContextMenu(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(
            master=master,
            width=width,
            height=height,
            border_width=2,
            corner_radius=0,
            fg_color=ThemeSettings.settings["root"]["fg_color"]["hover"]
        )

        self.select_all_button = ctk.CTkButton(
            master=self,
            command=self.select_all,
            text="Select All",
            corner_radius=0,
            text_color=ThemeSettings.settings["context_menu"]["text_color"],
            fg_color=ThemeSettings.settings["root"]["fg_color"]["hover"]
        )
        self.cut_button = ctk.CTkButton(
            master=self,
            command=self.cut,
            text="Cut",
            corner_radius=0,
            text_color=ThemeSettings.settings["context_menu"]["text_color"],
            fg_color=ThemeSettings.settings["root"]["fg_color"]["hover"]
        )
        self.copy_button = ctk.CTkButton(
            master=self,
            command=self.copy,
            text="Copy",
            corner_radius=0,
            text_color=ThemeSettings.settings["context_menu"]["text_color"],
            fg_color=ThemeSettings.settings["root"]["fg_color"]["hover"]
        )
        self.paste_button = ctk.CTkButton(
            master=self,
            command=self.paste,
            text="Paste",
            corner_radius=0,
            text_color=ThemeSettings.settings["context_menu"]["text_color"],
            fg_color=ThemeSettings.settings["root"]["fg_color"]["hover"]
        )
        self.width = width
        self.height = height
        self.set_widgets_accent_color()
        self.set_widgets_font()
        self.set_widgets_sizes()
        self.place_widgets()
        ThemeManager.register_widget(self)

    def place_widgets(self):
        self.select_all_button.pack(fill="x", padx=2, pady=(2, 0))
        self.cut_button.pack(fill="x", padx=2)
        self.copy_button.pack(fill="x", padx=2)
        self.paste_button.pack(fill="x", padx=2, pady=(0, 2))

    def update_widgets_accent_color(self):
        self.set_widgets_accent_color()

    def set_widgets_sizes(self):
        self.copy_button.configure(
            height=self.height / 4,
            width=self.width
        )
        self.cut_button.configure(
            height=self.height / 4,
            width=self.width
        )
        self.select_all_button.configure(
            height=self.height / 4,
            width=self.width
        )
        self.paste_button.configure(
            height=self.height / 4,
            width=self.width
        )

    def set_widgets_font(self):
        scale = GeneralSettings.settings["scale_r"]
        font = ("Segoe UI", 12 * scale, "bold")
        self.copy_button.configure(
            font=font
        )
        self.cut_button.configure(
            font=font
        )
        self.select_all_button.configure(
            font=font
        )
        self.paste_button.configure(
            font=font
        )

    def set_widgets_accent_color(self):
        self.configure(
            border_color=ThemeSettings.settings["root"]["accent_color"]["normal"],
        )
        self.select_all_button.configure(
            hover_color=ThemeSettings.settings["root"]["accent_color"]["normal"],
        )
        self.cut_button.configure(
            hover_color=ThemeSettings.settings["root"]["accent_color"]["normal"],
        )
        self.copy_button.configure(
            hover_color=ThemeSettings.settings["root"]["accent_color"]["normal"],
        )
        self.paste_button.configure(
            hover_color=ThemeSettings.settings["root"]["accent_color"]["normal"],
        )
        
    def update_widgets_colors(self):
        """Update colors for the widgets."""
        
    def select_all(self):
        pyautogui.hotkey("ctrl", "a")
        self.place_forget()

    def cut(self):
        pyautogui.hotkey("ctrl", "x")
        self.place_forget()

    def copy(self):
        pyautogui.hotkey("ctrl", "c")
        self.place_forget()

    def paste(self):
        pyautogui.hotkey("ctrl", "v")
        self.place_forget()
