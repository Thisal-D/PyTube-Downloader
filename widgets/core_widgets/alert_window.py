import customtkinter as ctk
from PIL import Image
from typing import Callable
from settings import AppearanceSettings, GeneralSettings


class AlertWindow(ctk.CTkToplevel):
    def __init__(
            self,
            master: ctk.CTk = None,
            alert_msg: str = "Something went wrong,,.!",
            ok_button_text: str = None,
            ok_button_callback: Callable = None,
            cancel_button_text: str = None,
            cancel_button_callback: Callable = None,
            callback: Callable = None,
            width: int = 400,
            height: int = 200):

        super().__init__(
            master=master,
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            width=width,
            height=height)

        scale = AppearanceSettings.settings["scale_r"]

        self.master: ctk.CTk = master
        self.width = width
        self.height = height
        self.callback = callback
        self.geometry(f"{self.width}x{self.height}")
        print(f"{self.width}x{self.height}")
        self.configure(width=self.width),
        self.configure(height=self.height)
        self.resizable(False, False)
        self.iconbitmap("assets\\main icon\\icon.ico")
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
            text=alert_msg,
            text_color=AppearanceSettings.settings["alert_window"]["msg_color"]["normal"],
            font=("Arial", 13 * scale, "bold")
        )
        self.error_msg_label.pack(pady=(20 * scale, 15 * scale), padx=(0, 30 * scale))

        if cancel_button_text is not None:
            self.cancel_button = ctk.CTkButton(
                border_width=2,
                border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                master=self,
                hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                command=self.on_click_cancel_button,
                text=cancel_button_text,
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                width=100 * scale,
                height=28 * scale,
                font=("Arial", 12 * scale, "bold")
            )
            self.cancel_button.pack(side="right", padx=(20 * scale, 40 * scale))

        if ok_button_text is not None:
            self.ok_button = ctk.CTkButton(
                border_width=2,
                border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                master=self,
                hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                command=self.on_click_ok_button,
                text=ok_button_text,
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