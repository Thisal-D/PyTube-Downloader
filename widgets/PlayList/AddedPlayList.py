import threading
import customtkinter as ctk
import pytube
from typing import Literal, Union, Any, List
from .PlayList import PlayList
from widgets import AddedVideo
from functions import pass_command
from services import ThemeManager


class AddedPlayList(PlayList):
    def __init__(
            self,
            master: Any = None,
            width: int = None,
            height: int = None,
            # playlist info
            playlist_url: str = None,
            # callback function for download buttons
            playlist_download_button_click_callback: callable = None,
            video_download_button_click_callback: callable = None):

        # widgets
        self.sub_frame: Union[ctk.CTkFrame, None] = None
        self.resolution_select_menu: Union[ctk.CTkComboBox, None] = None
        self.download_btn: Union[ctk.CTkButton, None] = None
        self.status_label: Union[ctk.CTkLabel, None] = None
        self.reload_btn: Union[ctk.CTkButton, None] = None
        self.videos_status_label: Union[ctk.CTkLabel, None] = None
        """self.loading_video_count_label: Union[ctk.CTkLabel, None] = None
        self.waiting_video_count_label: Union[ctk.CTkLabel, None] = None"""
        # playlist object
        self.playlist: Union[pytube.Playlist, None] = None
        # callback functions
        self.playlist_download_button_click_callback: callable = playlist_download_button_click_callback
        self.video_download_button_click_callback: callable = video_download_button_click_callback
        # all video objects
        self.videos: List[Union[None, AddedVideo]] = []
        # state
        self.load_state: Literal[None, "waiting", "loading", "failed", "completed"] = None
        # vars for state track
        self.waiting_videos: List[AddedVideo] = []
        self.loading_videos: List[AddedVideo] = []
        self.failed_videos: List[AddedVideo] = []
        self.completed_videos: List[AddedVideo] = []

        super().__init__(
            master=master,
            height=height,
            width=width,
            playlist_url=playlist_url
        )

        threading.Thread(target=self.load_playlist).start()

    def load_playlist(self):
        self.view_btn.configure(state="disabled")
        try:
            self.playlist = pytube.Playlist(self.playlist_url)
            self.playlist_video_count = int(self.playlist.length)
            self.channel = str(self.playlist.owner)
            self.playlist_title = str(self.playlist.title)
            self.channel_url = str(self.playlist.owner_url)
            self.view_btn.configure(state="normal")
            self.channel_btn.configure(state="normal")
            self.load_state = "completed"
            self.set_playlist_data()
            self.load_videos()
        except Exception as error:
            print(f"@1 > AddedPlayList.py : {error}")
            self.indicate_loading_failure()

    def load_videos(self):
        for video_url in self.playlist.video_urls:
            video = AddedVideo(
                master=self.playlist_item_frame,
                width=self.playlist_item_frame.winfo_width() - 20,
                height=70,
                video_url=video_url,
                video_download_button_click_callback=self.video_download_button_click_callback,
                mode="playlist",
                # videos state track
                video_load_status_callback=self.videos_status_track,
            )
            video.pack(fill="x", padx=(20, 0), pady=1)
            self.videos.append(video)

    def videos_status_track(
            self,
            video: AddedVideo,
            state: Literal["waiting", "loading", "completed", "failed", "removed"]):
        if state == "removed":
            self.videos.remove(video)
            self.playlist_video_count -= 1
            if len(self.videos) == 0:
                self.kill()
            else:
                if video in self.loading_videos:
                    self.loading_videos.remove(video)
                if video in self.failed_videos:
                    self.failed_videos.remove(video)
                if video in self.waiting_videos:
                    self.waiting_videos.remove(video)
                if video in self.completed_videos:
                    self.completed_videos.remove(video)
        elif state == "failed":
            self.failed_videos.append(video)
            if video in self.loading_videos:
                self.loading_videos.remove(video)
        elif state == "loading":
            if video in self.waiting_videos:
                self.waiting_videos.remove(video)
            if video in self.failed_videos:
                self.failed_videos.remove(video)
            self.loading_videos.append(video)
        elif state == "waiting":
            self.waiting_videos.append(video)
            if video in self.failed_videos:
                self.failed_videos.remove(video)
        elif state == "completed":
            self.completed_videos.append(video)
            self.loading_videos.remove(video)

        if len(self.videos) != 0:
            self.videos_status_label.configure(
                text=f"Failed : {len(self.failed_videos)} |   "
                     f"Waiting : {len(self.waiting_videos)} |   "
                     f"Loading : {len(self.loading_videos)} |   "
                     f"Loaded : {len(self.completed_videos)}"
                )
            self.playlist_video_count_label.configure(
                text=self.playlist_video_count
            )
            if len(self.failed_videos) != 0:
                self.indicate_loading_failure()
            else:
                self.clear_loading_failure()
            if len(self.loading_videos) == 0 and len(self.waiting_videos) == 0 and len(self.failed_videos) == 0:
                self.set_loading_completed()

    def reload_playlist(self):
        self.reload_btn.place_forget()
        self.status_label.configure(text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"], text="Loading")
        if len(self.videos) != 0:
            for video in self.videos:
                if video.load_state == "failed":
                    video.reload_video()
        else:
            threading.Thread(target=self.load_playlist).start()

    def indicate_loading_failure(self):
        self.status_label.configure(text="Failed", text_color=ThemeManager.theme_settings["video_object"]["error_color"]["normal"])
        self.reload_btn.place(relx=1, y=32, x=-80)

    def clear_loading_failure(self):
        self.status_label.configure(text="Loading", text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"])
        self.reload_btn.place_forget()

    def set_loading_completed(self):
        self.status_label.configure(text="Loaded")
        self.download_btn.configure(state="normal")
        self.resolution_select_menu.configure(values=["Highest Quality", "Lowest Quality", "Audio Only"])
        self.resolution_select_menu.set("Highest Quality")
        self.resolution_select_menu.configure(command=self.select_download_option)

    def select_download_option(self, e):
        index = None
        if e == "Highest Quality":
            index = 0
        elif e == "Lowest Quality":
            index = -2
        elif e == "Audio Only":
            index = -1
        for video in self.videos:
            video.resolution_select_menu.set(video.resolution_select_menu.cget("values")[index])
            video.choose_download_option(video.resolution_select_menu.cget("values")[index])

    def kill(self):
        for video in self.videos:
            video.video_load_status_callback = pass_command
            video.kill()
        super().kill()

    # create widgets
    def create_widgets(self):
        super().create_widgets()

        self.sub_frame = ctk.CTkFrame(
            master=self.playlist_info_widget,
            height=self.height - 4,
            width=340,
        )

        self.resolution_select_menu = ctk.CTkComboBox(
            master=self.sub_frame,
            values=["..........", "..........", ".........."]
        )

        self.download_btn = ctk.CTkButton(
            master=self.sub_frame,
            text="Download",
            width=80,
            height=25,
            border_width=2,
            state="disabled",
            hover=False,
            command=lambda: self.playlist_download_button_click_callback(self)
        )

        self.status_label = ctk.CTkLabel(
            master=self.sub_frame,
            text="Loading",
            height=15,
            font=("arial", 13, "bold"),
        )

        self.reload_btn = ctk.CTkButton(
            self.playlist_info_widget,
            text="⟳",
            width=15, height=15,
            font=("arial", 22, "normal"),
            command=self.reload_playlist,
            hover=False,
        )

        self.videos_status_label = ctk.CTkLabel(
            master=self.sub_frame,
            text=f"Failed : {len(self.failed_videos)} |   "
                 f"Waiting : {len(self.waiting_videos)} |   "
                 f"Loading : {len(self.loading_videos)} |   "
                 f"Loaded : {len(self.completed_videos)}",

            height=15,
            font=("arial", 11, "bold"),
        )

    # configure widgets colors
    def set_accent_color(self):
        super().set_accent_color()
        self.download_btn.configure(border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"])
        self.reload_btn.configure(text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"])

        self.download_btn.configure(border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"])
        self.reload_btn.configure(text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"])

    def reset_widgets_colors(self):
        super().reset_widgets_colors()

    def set_widgets_colors(self):
        super().set_widgets_colors()
        self.sub_frame.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]
        )
        self.download_btn.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["btn_fg_color"]["normal"],
            text_color=ThemeManager.theme_settings["video_object"]["btn_text_color"]["normal"]
        )
        self.status_label.configure(
            text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"]
        )
        self.reload_btn.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]
        )
        self.videos_status_label.configure(
            text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"]
        )

    def on_mouse_enter_self(self, _event):
        super().on_mouse_enter_self(_event)
        self.sub_frame.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])
        self.reload_btn.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])

    def on_mouse_leave_self(self, _event):
        super().on_mouse_leave_self(_event)
        self.sub_frame.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])
        self.reload_btn.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])

    def bind_widget_events(self):
        super().bind_widget_events()

        def on_mouse_enter_download_btn(_event):
            if self.download_btn.cget("state") == "normal":
                self.download_btn.configure(
                    fg_color=ThemeManager.theme_settings["video_object"]["btn_fg_color"]["hover"],
                    text_color=ThemeManager.theme_settings["video_object"]["btn_text_color"]["hover"],
                    border_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"]
                )
            self.on_mouse_enter_self(_event)

        def on_mouse_leave_download_btn(_event):
            if self.download_btn.cget("state") == "normal":
                self.download_btn.configure(
                    fg_color=ThemeManager.theme_settings["video_object"]["btn_fg_color"]["normal"],
                    text_color=ThemeManager.theme_settings["video_object"]["btn_text_color"]["normal"],
                    border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
                )

        self.download_btn.bind("<Enter>", on_mouse_enter_download_btn)
        self.download_btn.bind("<Leave>", on_mouse_leave_download_btn)

        def on_mouse_enter_reload_btn(_event):
            self.reload_btn.configure(
                text_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"],
            )
            self.on_mouse_enter_self(_event)

        def on_mouse_leave_reload_btn(_event):
            self.reload_btn.configure(
                text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            )

        self.reload_btn.bind("<Enter>", on_mouse_enter_reload_btn)
        self.reload_btn.bind("<Leave>", on_mouse_leave_reload_btn)

    # place widgets
    def place_widgets(self):
        self.playlist_info_widget.pack(fill="x")
        self.view_btn.place(y=55, x=10)
        self.title_label.place(x=50, y=10, height=20, width=-460, relwidth=1)
        self.channel_btn.place(x=50, y=34, height=20, width=-460, relwidth=1)
        self.url_label.place(x=50, y=54, height=20, width=-460, relwidth=1)
        self.playlist_video_count_label.place(relx=1, x=-40, rely=1, y=-25)
        self.remove_btn.place(relx=1, x=-25, y=3)

        self.sub_frame.place(y=2, relx=1, x=-390)
        self.resolution_select_menu.place(y=22, x=0)
        self.download_btn.place(x=160, y=8)
        self.status_label.place(x=200, anchor="n", y=40)
        self.videos_status_label.place(rely=1, y=-18, relx=0.5, anchor="n")
