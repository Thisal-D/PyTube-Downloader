import customtkinter as ctk
from PIL import Image
from typing import Callable
from settings import ThemeSettings


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
            width: int = 450,
            height: int = 130):

        super().__init__(
            master=master,
            fg_color=ThemeSettings.settings["root"]["fg_color"]["normal"])
        self.master: ctk.CTk = master
        self.width = width
        self.height = height
        self.callback = callback

        self.resizable(False, False)
        self.iconbitmap("assets\\icon.ico")
        self.title("PytubeDownloader")
        self.transient(master)
        self.attributes('-topmost', True)
        self.grab_set()

        self.info_image = ctk.CTkImage(Image.open("assets\\info.png"), size=(60, 60))
        self.info_image_label = ctk.CTkLabel(
            master=self,
            text="",
            image=self.info_image
        )
        self.info_image_label.pack(side="left", fill="y", padx=(30, 10))

        self.error_msg_label = ctk.CTkLabel(
            master=self,
            text=alert_msg,
            text_color=ThemeSettings.settings["alert_window"]["msg_color"]["normal"],
            font=("Arial", 13, "bold")
        )
        self.error_msg_label.pack(pady=(20, 15), padx=(0, 30))

        if cancel_button_text is not None:
            self.cancel_button = ctk.CTkButton(
                border_width=2,
                border_color=ThemeSettings.settings["root"]["accent_color"]["normal"],
                master=self,
                hover_color=ThemeSettings.settings["root"]["accent_color"]["hover"],
                command=self.on_click_cancel_button,
                text=cancel_button_text,
                fg_color=ThemeSettings.settings["root"]["accent_color"]["normal"],
                width=100
            )
            self.cancel_button.pack(side="right", padx=(20, 40))

        if ok_button_text is not None:
            self.ok_button = ctk.CTkButton(
                border_width=2,
                border_color=ThemeSettings.settings["root"]["accent_color"]["normal"],
                master=self,
                hover_color=ThemeSettings.settings["root"]["accent_color"]["hover"],
                command=self.on_click_ok_button,
                text=ok_button_text,
                fg_color=ThemeSettings.settings["root"]["accent_color"]["normal"],
                width=100
            )
            self.ok_button.pack(side="right", padx=(0, 20))

        self.ok_button_callback = ok_button_callback
        self.cancel_button_callback = cancel_button_callback

        self.master.bind("<Configure>", self.move)
        self.bind("<Configure>", self.move)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.move("event")

    def move(self, _event):
        geometry_x = int(self.master.winfo_width() * 0.5 + self.master.winfo_x() - 0.5 * self.width + 7)
        geometry_y = int(self.master.winfo_height() * 0.5 + self.master.winfo_y() - 0.5 * self.height + 20)
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
