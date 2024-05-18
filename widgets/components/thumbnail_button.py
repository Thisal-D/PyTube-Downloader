import tkinter as tk
from tkinter import PhotoImage
import threading
import time
from typing import Tuple, List, Literal, Any
from services import LoadingIndicateManager
from settings import GeneralSettings


class ThumbnailButton(tk.Button):
    def __init__(
            self,
            master: Any = None,
            font: Tuple[str, int, str] = ("arial", 14, "bold"),
            command: callable = None,
            height: int = 0,
            width: int = 0,
            thumbnails: List[PhotoImage] = None,
            state: Literal["normal", "disabled"] = "normal",
            ):

        from widgets.video.added_video import AddedVideo

        self.master: AddedVideo = master
        self.loading_animation_state: Literal["enabled", "disabled", None] = None
        self.loading_animation_running: bool = False
        self.thumbnails = thumbnails

        super().__init__(
            master=master,
            width=width,
            height=height,
            bd=0,
            font=font,
            relief="sunken",
            state=state,
            cursor="hand2",
            command=command
        )

    def run_loading_animation_thread(self):
        self.configure(image="")
        self.loading_animation_running = True
        if self.loading_animation_state != "disabled":
            self.loading_animation_state = "enabled"
            while self.master.load_state != "removed":
                self.configure(text="." * LoadingIndicateManager.dots_count)
                time.sleep(GeneralSettings.settings["update_delay"])
                if self.loading_animation_state == "disabled" and self.master.load_state != "removed":
                    break
        self.loading_animation_running = False

    def run_loading_animation(self):
        self.loading_animation_state = "enabled"
        threading.Thread(target=self.run_loading_animation_thread).start()

    def stop_loading_animation(self):
        self.loading_animation_state = 'disabled'
        while self.loading_animation_running:
            time.sleep(GeneralSettings.settings["update_delay"])

    def configure_thumbnail(self, thumbnails: List[PhotoImage]):
        self.stop_loading_animation()
        self.thumbnails = thumbnails
        self.configure(image=thumbnails[0], text="")

    def show_failure_indicator(self, text_color: str):
        self.stop_loading_animation()
        self.configure(text="....", disabledforeground=text_color, image="")

    def on_mouse_enter(self, _event):
        self.configure(image=self.thumbnails[1])

    def on_mouse_leave(self, _event):
        self.configure(image=self.thumbnails[0])
