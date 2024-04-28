from widgets.Video import Video
import customtkinter as ctk
import pytube
import threading
from typing import Literal, Union, List, Any, Callable, Dict
from services import (
    LoadManager,
    ThemeManager
)
from functions import (
    get_thumbnails,
    get_supported_download_types,
    sort_dict,
    get_formated_combo_box_values,
)


class AddedVideo(Video):
    def __init__(
            self,
            master: Any,
            width: int = 0,
            height: int = 0,
            # video info
            video_url: str = "",
            # callback functions for buttons
            video_download_button_click_callback: Callable = None,
            # state callbacks only use if mode is play list
            mode: Literal["video", "playlist"] = "video",
            video_load_status_callback: callable = None,
            # download_mode
            accent_color: Dict = None,
            theme_settings: Dict = None):

        self.loading_loop_running: bool = False
        # video info
        self.video_stream_data: pytube.YouTube.streams = None
        self.support_download_types: Union[List[str], None] = None
        # download info
        self.download_quality: Literal["128kbps", "360p", "720p"] = "720p"
        self.download_type: Literal["Audio", "Video"] = "Video"
        # callback functions
        self.video_download_button_click_callback: Callable = video_download_button_click_callback
        self.video_load_status_callback: Callable = video_load_status_callback
        # state
        self.load_state: Literal["waiting", "loading", "failed", "completed", "removed"] = "waiting"
        # widgets
        self.sub_frame: Union[ctk.CTkFrame, None] = None
        self.resolution_select_menu: Union[ctk.CTkComboBox, None] = None
        self.download_btn: Union[ctk.CTkButton, None] = None
        self.status_label: Union[ctk.CTkLabel, None] = None
        self.reload_btn: Union[ctk.CTkButton, None] = None
        # video object
        self.video: Union[pytube.YouTube, None] = None

        self.mode: Literal["video", "playlist"] = mode

        super().__init__(
            master=master,
            width=width,
            height=height,
            video_url=video_url,
            accent_color=accent_color,
            theme_settings=theme_settings
        )
        self.load_video()

    def reload_video(self):
        self.load_state = None
        self.reload_btn.place_forget()
        self.thumbnail_btn.configure(
            disabledforeground=ThemeManager.get_color_based_on_theme(self.theme_settings["text_color"]["normal"])
        )
        self.thumbnail_btn.run_loading_animation()
        self.status_label.configure(
            text_color=self.theme_settings["text_color"]["normal"],
            text="Loading"
        )
        self.load_video()

    def load_video(self):
        self.thumbnail_btn.run_loading_animation()
        if LoadManager.max_concurrent_loads > LoadManager.active_load_count:
            self.load_state = "loading"
            LoadManager.active_loads.append(self)
            LoadManager.active_load_count += 1
            if self.mode == "playlist":
                self.video_load_status_callback(self, self.load_state)
            self.status_label.configure(text="Loading")
            threading.Thread(target=self.retrieve_video_data).start()
        else:
            self.set_waiting()

    def retrieve_video_data(self):
        try:
            self.video = pytube.YouTube(self.video_url)
            self.video_title = str(self.video.title)
            self.channel = str(self.video.author)
            self.length = int(self.video.length)
            self.video_stream_data = self.video.streams
            self.channel_url = str(self.video.channel_url)
            self.thumbnails = get_thumbnails(self.video)
            self.support_download_types = sort_dict(get_supported_download_types(self.video_stream_data))
            self.set_load_completed()
            self.set_video_data()
        except Exception as error:
            print(f"@1AddedVideo.py > {error}")
            self.set_loading_failed()

    def choose_download_option(self, e: str):
        self.download_quality = e.replace(" ", "").split("|")[0]
        if "kbps" in self.download_quality:
            self.download_type = "Audio"
        else:
            self.download_type = "Video"

    def set_waiting(self):
        self.load_state = "waiting"
        if self.mode == "playlist":
            self.video_load_status_callback(self, self.load_state)
        LoadManager.queued_loads.append(self)
        self.status_label.configure(text="Waiting")

    def set_load_completed(self):
        if self.load_state != "removed":
            self.load_state = "completed"
            if self.mode == "playlist":
                self.video_load_status_callback(self, self.load_state)
            self.status_label.configure(text="Loaded")
            if self in LoadManager.active_loads:
                LoadManager.active_loads.remove(self)
            LoadManager.active_load_count -= 1

    def set_loading_failed(self):
        if self.load_state != "removed":
            print(self.load_state)
            if self in LoadManager.active_loads:
                LoadManager.active_loads.remove(self)
                LoadManager.active_load_count -= 1
            self.load_state = "failed"
            if self.mode == "playlist":
                self.video_load_status_callback(self, self.load_state)
            self.thumbnail_btn.show_failure_indicator(text_color=self.theme_settings["error_color"]["normal"])
            self.status_label.configure(
                text_color=self.theme_settings["error_color"]["normal"],
                text="Failed"
            )
            self.reload_btn.place(relx=1, y=22, x=-80)
        else:
            print(self.load_state)

    def set_video_data(self):
        if self.load_state != "removed":
            super().set_video_data()
            self.resolution_select_menu.configure(
                values=get_formated_combo_box_values(self.support_download_types)
            )
            self.resolution_select_menu.set(self.resolution_select_menu.cget("values")[0])
            self.choose_download_option(self.resolution_select_menu.get())
            self.resolution_select_menu.configure(command=self.choose_download_option)
            self.channel_btn.configure(state="normal")
            self.download_btn.configure(state="normal")

    def kill(self):
        self.load_state = "removed"
        if self in LoadManager.active_loads:
            LoadManager.active_loads.remove(self)
            LoadManager.active_load_count -= 1
        if self in LoadManager.queued_loads:
            LoadManager.queued_loads.remove(self)
        if self.mode == "playlist":
            self.video_load_status_callback(self, self.load_state)
        super().kill()

    # create widgets
    def create_widgets(self):

        self.sub_frame = ctk.CTkFrame(
            master=self,
            height=self.height - 4,
            width=250,
        )

        self.resolution_select_menu = ctk.CTkComboBox(
            master=self.sub_frame,
            values=["..........", "..........", ".........."]
        )

        self.download_btn = ctk.CTkButton(
            master=self.sub_frame, text="Download", width=80, height=25,
            border_width=2,
            state="disabled",
            hover=False,
            command=lambda: self.video_download_button_click_callback(self)
        )

        self.status_label = ctk.CTkLabel(
            master=self.sub_frame,
            text="",
            height=15,
            font=("arial", 12, "bold"),
        )

        self.reload_btn = ctk.CTkButton(
            master=self,
            text="⟳",
            width=15, height=15,
            font=("arial", 20, "normal"),
            command=self.reload_video,
            hover=False,
        )
        super().create_widgets()

    # configure widgets colors
    def set_accent_color(self):
        self.download_btn.configure(border_color=self.accent_color["normal"])
        self.reload_btn.configure(text_color=self.accent_color["normal"])
        super().set_accent_color()

    def set_widgets_colors(self):
        self.reload_btn.configure(
            fg_color=self.theme_settings["fg_color"]["normal"]
        )
        self.download_btn.configure(
            fg_color=self.theme_settings["btn_fg_color"]["normal"],
            text_color=self.theme_settings["btn_text_color"]["normal"]
        )
        self.sub_frame.configure(
            fg_color=self.theme_settings["fg_color"]["normal"]
        )
        self.status_label.configure(
            text_color=self.theme_settings["text_color"]["normal"]
        )
        super().set_widgets_colors()

    def on_mouse_enter_self(self, event):
        super().on_mouse_enter_self(event)
        self.sub_frame.configure(fg_color=self.theme_settings["fg_color"]["hover"])
        self.reload_btn.configure(fg_color=self.theme_settings["fg_color"]["hover"])

    def on_mouse_leave_self(self, event):
        super().on_mouse_leave_self(event)
        self.sub_frame.configure(fg_color=self.theme_settings["fg_color"]["normal"])
        self.reload_btn.configure(fg_color=self.theme_settings["fg_color"]["normal"])

    def bind_widget_events(self):
        super().bind_widget_events()
        super().bind_widget_events()

        def on_mouse_enter_download_btn(event):
            self.on_mouse_enter_self(event)
            if self.download_btn.cget("state") == "normal":
                self.download_btn.configure(
                    fg_color=self.theme_settings["btn_fg_color"]["hover"],
                    text_color=self.theme_settings["btn_text_color"]["hover"],
                    border_color=self.accent_color["hover"]
                )

        def on_mouse_leave_download_btn(event):
            self.on_mouse_leave_self(event)
            if self.download_btn.cget("state") == "normal":
                self.download_btn.configure(
                    fg_color=self.theme_settings["btn_fg_color"]["normal"],
                    text_color=self.theme_settings["btn_text_color"]["normal"],
                    border_color=self.accent_color["normal"]
                )

        self.download_btn.bind("<Enter>", on_mouse_enter_download_btn)
        self.download_btn.bind("<Leave>", on_mouse_leave_download_btn)

        def on_mouse_enter_reload_btn(event):
            self.on_mouse_enter_self(event)
            self.reload_btn.configure(
                text_color=self.accent_color["hover"],
            )

        def on_mouse_leave_reload_btn(event):
            self.on_mouse_leave_self(event)
            self.reload_btn.configure(
                text_color=self.accent_color["normal"],
            )

        self.reload_btn.bind("<Enter>", on_mouse_enter_reload_btn)
        self.reload_btn.bind("<Leave>", on_mouse_leave_reload_btn)

    # place widgets
    def place_widgets(self):
        super().place_widgets()

        self.sub_frame.place(y=2, relx=1, x=-350)
        self.resolution_select_menu.place(y=15, x=20)
        self.download_btn.place(x=170, y=8)
        self.status_label.place(x=210, anchor="n", y=44)

    # static method
    active_load_count = 0
    max_concurrent_loads = 1
    queued_loads = []
    active_loads = []
