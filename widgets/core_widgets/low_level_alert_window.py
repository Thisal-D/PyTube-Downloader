import customtkinter as ctk
import time
from PIL import Image
from typing import Callable
from settings import AppearanceSettings
from services import LanguageManager

class LowLevelAlertWindow(ctk.CTk):
    """
    Use to track any alert windows running or not
    """
    
    def __init__(self,
                 alert_msg: str = "something_went_wrong",
                 ok_button_display: bool = None,
                 ok_button_callback: Callable = None,
                 cancel_button_display: bool = None,
                 cancel_button_callback: Callable = None,
                 callback: Callable = None,
                 more_details: str = None,
                 width: int = 400,
                 height: int = 200):
        super().__init__(fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],)

        scale = AppearanceSettings.settings["scale_r"]

        self.callback = callback
        self.width = width
        self.height = height
        self.geometry(f"{self.width}x{self.height}")
        self.attributes("-alpha", AppearanceSettings.settings["opacity_r"])
        self.resizable(False, False)
        self.iconbitmap("assets\\main icon\\512x512.ico")
        self.title("PytubeDownloader")

        # Info Image
        self.info_image = ctk.CTkImage(Image.open("assets\\ui images\\info.png"), size=(70 * scale, 70 * scale))
        self.info_image_label = ctk.CTkLabel(
            master=self,
            text="",
            image=self.info_image,
            width=70, height=70
        )
        self.info_image_label.pack(side="left", fill="y", padx=(30 * scale, 10 * scale))

        # Error Message Label
        self.error_msg_label = ctk.CTkLabel(
            master=self,
            text=LanguageManager.data[alert_msg],
            text_color=AppearanceSettings.settings["alert_window"]["msg_color"]["normal"],
            font=("Arial", 13 * scale, "bold")
        )
        if more_details is None:
            self.error_msg_label.pack(pady=(20 * scale, 15 * scale), padx=(0, 30 * scale))
        else:
            self.error_msg_label.pack(pady=(10 * scale, 0 * scale), padx=(0, 30 * scale))
        
        # More Details (if provided)
        if more_details is not None:
            self.more_details_label = ctk.CTkLabel(
                master=self,
                text=more_details,
                text_color=AppearanceSettings.settings["alert_window"]["details"]["normal"],
                font=("Arial", 12 * scale, "bold")
            )
            self.more_details_label.pack(pady=(8 * scale, 15 * scale), padx=(0, 30 * scale))

        # Cancel Button (if required)
        if cancel_button_display is True:
            self.cancel_button = ctk.CTkButton(
                border_width=2,
                border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                master=self,
                hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                command=self.on_click_cancel_button,
                text=LanguageManager.data["cancel"],
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                width=100 * scale,
                height=28 * scale,
                font=("Arial", 12 * scale, "bold")
            )
            self.cancel_button.pack(side="right", padx=(20 * scale, 40 * scale))

        # OK Button (if required)
        if ok_button_display is True:
            self.ok_button = ctk.CTkButton(
                border_width=2,
                border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                master=self,
                hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                command=self.on_click_ok_button,
                text=LanguageManager.data["ok"],
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                width=100 * scale,
                height=28 * scale,
                font=("Arial", 12 * scale, "bold")
            )
            self.ok_button.pack(side="right", padx=(0, 20 * scale))

        self.ok_button_callback = ok_button_callback
        self.cancel_button_callback = cancel_button_callback

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.destroy()
        if self.callback is not None:
            self.callback()

    def on_click_ok_button(self):
        if self.ok_button_callback is not None:
            self.ok_button_callback()
        self.on_closing()

    def on_click_cancel_button(self):
        if self.cancel_button_callback is not None:
            self.cancel_button_callback()
        self.on_closing()
