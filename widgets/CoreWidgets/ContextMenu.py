import customtkinter as ctk
import pyautogui
from services import ThemeManager


class ContextMenu(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(
            master=master,
            width=width,
            height=height,
            border_width=2,
            corner_radius=0,
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["hover"]
        )

        self.select_all_button = ctk.CTkButton(
            master=self,
            command=self.select_all,
            text="Select All",
            width=width,
            corner_radius=0,
            text_color=ThemeManager.theme_settings["context_menu"]["text_color"],
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["hover"]
        )
        self.cut_button = ctk.CTkButton(
            master=self,
            command=self.cut,
            text="Cut",
            width=width,
            corner_radius=0,
            text_color=ThemeManager.theme_settings["context_menu"]["text_color"],
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["hover"]
        )
        self.copy_button = ctk.CTkButton(
            master=self,
            command=self.copy,
            text="Copy",
            width=width,
            corner_radius=0,
            text_color=ThemeManager.theme_settings["context_menu"]["text_color"],
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["hover"]
        )
        self.paste_button = ctk.CTkButton(
            master=self,
            command=self.paste,
            text="Paste",
            width=width,
            corner_radius=0,
            text_color=ThemeManager.theme_settings["context_menu"]["text_color"],
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["hover"]
        )

        self.set_accent_color()
        self.place_widgets()
        ThemeManager.bind_widget(self)

    def place_widgets(self):
        self.select_all_button.pack(fill="x", padx=2, pady=(2, 0))
        self.cut_button.pack(fill="x", padx=2)
        self.copy_button.pack(fill="x", padx=2)
        self.paste_button.pack(fill="x", padx=2, pady=(0, 2))

    def update_accent_color(self):
        self.set_accent_color()

    def set_accent_color(self):
        self.configure(
            border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
        )
        self.select_all_button.configure(
            hover_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
        )
        self.cut_button.configure(
            hover_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
        )
        self.copy_button.configure(
            hover_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
        )
        self.paste_button.configure(
            hover_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
        )
        
    def reset_widgets_colors(self):
        ...
        
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
