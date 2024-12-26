import customtkinter as ctk
import time
from PIL import Image
from typing import Callable
from settings import AppearanceSettings
from services import LanguageManager

class AlertWindow(ctk.CTkToplevel):
    """
    Use to track any alert windows running or not
    """
    Running = False
    
    def __init__(
            self,
            master: ctk.CTk = None,
            original_configure_callback : Callable = None,
            alert_msg: str = "something_went_wrong",
            ok_button_display: bool = None,
            ok_button_callback: Callable = None,
            cancel_button_display: bool = None,
            cancel_button_callback: Callable = None,
            callback: Callable = None,
            wait_for_previous: bool = False,
            more_details: str = None,
            width: int = 400,
            height: int = 200):

        super().__init__(
            master=master,
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            width=width,
            height=height)

        # If ensure_previous_closed is true, wait until the previous alert window is closed
        if wait_for_previous:
            while AlertWindow.Running :
                time.sleep(0.5)
                
        if not master.is_app_running:
            return
        
        # Start the alert window
        AlertWindow.Running = True
        
        scale = AppearanceSettings.settings["scale_r"]

        self.master: ctk.CTk = master
        self.original_configure_callback  = original_configure_callback 
        self.width = width
        self.height = height
        self.callback = callback
        self.geometry(f"{self.width}x{self.height}")
        self.attributes("-alpha", AppearanceSettings.settings["opacity_r"])
        self.configure(width=self.width),
        self.configure(height=self.height)
        self.resizable(False, False)
        self.iconbitmap("assets\\main icon\\512x512.ico")
        self.title("PytubeDownloader")
        self.transient(master)
        self.grab_set()

        self.info_image = ctk.CTkImage(Image.open("assets\\ui images\\info.png"), size=(70 * scale, 70 * scale))
        self.info_image_label = ctk.CTkLabel(
            master=self,
            text="",
            image=self.info_image,
            width=70, height=70
        )
        self.info_image_label.pack(side="left", fill="y", padx=(30 * scale, 10 * scale))

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
        
        if more_details is not None:
            self.more_details_label = ctk.CTkLabel(
                master=self,
                text=more_details,
                text_color=AppearanceSettings.settings["alert_window"]["details"]["normal"],
                font=("Arial", 12 * scale, "bold")
            )
            self.more_details_label.pack(pady=(8 * scale, 15 * scale), padx=(0, 30 * scale))

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

        self.master.bind("<Configure>", self.move)
        self.bind("<Configure>", self.move)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.move("event")

    def move(self, _event):
        geometry_x = int(self.master.winfo_width() * 0.5 + self.master.winfo_x() - 0.5 * self.width)
        geometry_y = int(self.master.winfo_height() * 0.5 + self.master.winfo_y() - 0.5 * self.height)
        self.geometry(f"{self.width}x{self.height}+{geometry_x}+{geometry_y}")

    def on_closing(self):
        self.transient(None)
        self.grab_release()
        self.unbind("<Configure>")
        self.master.unbind("<Configure>")
        self.destroy()
        AlertWindow.Running = False
        if self.callback is not None:
            self.callback()
            
        if self.original_configure_callback  is not None:
            self.master.bind("<Configure>", self.original_configure_callback )

    def on_click_ok_button(self):
        if self.ok_button_callback is not None:
            self.ok_button_callback()
        self.on_closing()

    def on_click_cancel_button(self):
        if self.cancel_button_callback is not None:
            self.cancel_button_callback()
        self.on_closing()