import threading
import customtkinter as ctk
import pytube
from typing import Literal, Union, List
from .play_list import PlayList
from widgets import AddedVideo
from utils import GuiUtils
from settings import AppearanceSettings


class AddedPlayList(PlayList):
    def __init__(
            self,
            root: ctk.CTk = None,
            master: ctk.CTkScrollableFrame = None,
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
        self.videos_status_counts_label: Union[ctk.CTkLabel, None] = None
        """self.loading_video_count_label: Union[ctk.CTkLabel, None] = None
        self.waiting_video_count_label: Union[ctk.CTkLabel, None] = None"""
        # playlist object
        self.playlist: Union[pytube.Playlist, None] = None
        # callback utils
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
            root=root,
            master=master,
            height=height,
            width=width,
            playlist_url=playlist_url
        )

        self.indicate_loading()
        threading.Thread(target=self.load_playlist, daemon=True).start()

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
            print(f"added_play_list.py : {error}")
            self.indicate_loading_failure()

    def load_videos(self):
        for video_url in self.playlist.video_urls:
            video = AddedVideo(
                root=self.root,
                master=self.playlist_item_frame,
                width=self.playlist_item_frame.winfo_width() - 20,
                height=70 * AppearanceSettings.settings["scale_r"],
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
            self.videos_status_counts_label.configure(
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
                if len(self.waiting_videos) == self.playlist_video_count:
                    self.indicate_waiting()
                else:
                    self.indicate_loading()
            if len(self.loading_videos) == 0 and len(self.waiting_videos) == 0 and len(self.failed_videos) == 0:
                self.set_loading_completed()

    def reload_playlist(self):
        if len(self.loading_videos) == 0 and len(self.videos) != 0:
            self.indicate_waiting()
        else:
            self.indicate_loading()

        if len(self.videos) != 0:
            for video in self.videos:
                if video.load_state == "failed":
                    video.reload_video()
        else:
            threading.Thread(target=self.load_playlist, daemon=True).start()

    def indicate_waiting(self):
        self.status_label.configure(
            text="Waiting",
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.reload_btn.place_forget()

    def indicate_loading_failure(self):
        self.status_label.configure(
            text="Failed",
            text_color=AppearanceSettings.settings["video_object"]["error_color"]["normal"]
        )
        self.reload_btn.place(
            relx=1,
            rely=0.5,
            anchor="w",
            x=-80 * AppearanceSettings.settings["scale_r"])

    def indicate_loading(self):
        self.status_label.configure(
            text="Loading",
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
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
            video.choose_download_type(video.resolution_select_menu.get())

    def kill(self):
        for video in self.videos:
            video.video_load_status_callback = GuiUtils.do_nothing
            video.kill()
        super().kill()

    # create widgets
    def create_widgets(self):
        super().create_widgets()

        self.sub_frame = ctk.CTkFrame(master=self.playlist_main_frame)
        self.resolution_select_menu = ctk.CTkComboBox(
            master=self.sub_frame,
            values=["..........", "..........", ".........."],
            width=150 * AppearanceSettings.settings["scale_r"],
            height=28 * AppearanceSettings.settings["scale_r"]
        )
        self.download_btn = ctk.CTkButton(
            master=self.sub_frame,
            text="Download",
            state="disabled",
            hover=False,
            command=lambda: self.playlist_download_button_click_callback(self)
        )
        self.status_label = ctk.CTkLabel(master=self.sub_frame, text="Loading")
        self.reload_btn = ctk.CTkButton(
            self.playlist_main_frame,
            text="⟳",
            command=self.reload_playlist,
            hover=False,
        )
        self.videos_status_counts_label = ctk.CTkLabel(
            master=self.sub_frame,
            text=f"Failed : {len(self.failed_videos)} |   "
                 f"Waiting : {len(self.waiting_videos)} |   "
                 f"Loading : {len(self.loading_videos)} |   "
                 f"Loaded : {len(self.completed_videos)}"
        )

    def set_widgets_fonts(self):
        super().set_widgets_fonts()

        scale = AppearanceSettings.settings["scale_r"]

        self.resolution_select_menu.configure(
            dropdown_font=("Segoe UI", 13 * scale, "normal"),
            font=("Segoe UI", 13 * scale, "normal")
        )
        self.download_btn.configure(font=("arial", 12 * scale, "bold"))
        self.status_label.configure(font=("arial", 13 * scale, "bold"))
        self.reload_btn.configure(font=("arial", 22 * scale, "normal"))
        self.videos_status_counts_label.configure(font=("Segoe UI", 11 * scale, "normal"))

    def set_widgets_sizes(self):
        super().set_widgets_sizes()

        scale = AppearanceSettings.settings["scale_r"]

        self.sub_frame.configure(height=self.height - 3, width=340 * scale)
        self.resolution_select_menu.configure(width=150 * scale, height=28 * scale)
        self.download_btn.configure(width=80 * scale, height=25 * scale, border_width=2)
        self.status_label.configure(height=15 * scale, width=80 * scale)
        self.reload_btn.configure(width=15 * scale, height=15 * scale)
        self.videos_status_counts_label.configure(height=15 * scale)

    # configure widgets colors
    def set_widgets_accent_color(self):
        super().set_widgets_accent_color()

        self.resolution_select_menu.configure(
            button_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            button_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            dropdown_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.download_btn.configure(border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        self.reload_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

        self.download_btn.configure(border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        self.reload_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

    def set_widgets_colors(self):
        super().set_widgets_colors()

        self.sub_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.download_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["btn_fg_color"]["normal"],
            text_color=AppearanceSettings.settings["video_object"]["btn_text_color"]["normal"]
        )
        self.status_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.reload_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.videos_status_counts_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.resolution_select_menu.configure(
            dropdown_fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"],
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
        )

    def on_mouse_enter_self(self, _event):
        super().on_mouse_enter_self(_event)

        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])
        self.reload_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])

    def on_mouse_leave_self(self, _event):
        super().on_mouse_leave_self(_event)

        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.reload_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])

    def bind_widgets_events(self):
        super().bind_widgets_events()

        def on_mouse_enter_download_btn(_event):
            if self.download_btn.cget("state") == "normal":
                self.download_btn.configure(
                    fg_color=AppearanceSettings.settings["video_object"]["btn_fg_color"]["hover"],
                    text_color=AppearanceSettings.settings["video_object"]["btn_text_color"]["hover"],
                    border_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
                )
            self.on_mouse_enter_self(_event)

        def on_mouse_leave_download_btn(_event):
            if self.download_btn.cget("state") == "normal":
                self.download_btn.configure(
                    fg_color=AppearanceSettings.settings["video_object"]["btn_fg_color"]["normal"],
                    text_color=AppearanceSettings.settings["video_object"]["btn_text_color"]["normal"],
                    border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
                )

        self.download_btn.bind("<Enter>", on_mouse_enter_download_btn)
        self.download_btn.bind("<Leave>", on_mouse_leave_download_btn)

        def on_mouse_enter_reload_btn(_event):
            self.reload_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            )
            self.on_mouse_enter_self(_event)

        def on_mouse_leave_reload_btn(_event):
            self.reload_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            )

        self.reload_btn.bind("<Enter>", on_mouse_enter_reload_btn)
        self.reload_btn.bind("<Leave>", on_mouse_leave_reload_btn)

    # place widgets
    def place_widgets(self):
        super().place_widgets()

        scale = AppearanceSettings.settings["scale_r"]

        self.sub_frame.place(y=1, relx=1, x=-390 * scale)

        self.resolution_select_menu.place(rely=0.5, x=0, anchor="w")
        self.download_btn.place(x=190 * scale, rely=0.25, anchor='w')
        self.status_label.place(x=190 * scale, rely=0.60, anchor='w')
        self.videos_status_counts_label.place(rely=0.875, relx=0.5, anchor="center")

    def configure_widget_sizes(self, _event):
        scale = AppearanceSettings.settings["scale_r"]
        self.info_frame.configure(
            width=self.master.winfo_width() - (390*scale) - (50*scale + 15 * scale) - (20 * scale)
        )
