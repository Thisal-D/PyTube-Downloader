import customtkinter as ctk
import threading
from typing import List, Any, Literal, Union, Callable
from widgets.PlayList import PlayList
from widgets.Video.DownloadingVideo import DownloadingVideo
from widgets.Video.AddedVideo import AddedVideo
from functions import pass_command
from services import ThemeManager


class DownloadingPlayList(PlayList):
    def __init__(
            self,
            master: Any,
            width: int = None,
            height: int = None,
            # playlist details
            channel_url: str = None,
            playlist_url: str = None,
            playlist_title: str = "---------",
            channel: str = "---------",
            playlist_video_count: int = 0,
            # videos of playlist
            videos: List[AddedVideo] = None,
            # download directory
            download_directory: str = "",
            # playlist download completed callback functions
            playlist_download_complete_callback: Callable = None):

        # widgets
        self.sub_frame: Union[ctk.CTkFrame, None] = None
        self.download_progress_bar: Union[ctk.CTkProgressBar, None] = None
        self.download_percentage_label: Union[ctk.CTkLabel, None] = None
        self.status_label: Union[ctk.CTkLabel, None] = None
        self.re_download_btn: Union[ctk.CTkButton, None] = None
        self.videos_status_label: Union[ctk.CTkLabel, None] = None
        # callback functions
        self.playlist_download_complete_callback = playlist_download_complete_callback
        self.added_videos: List[AddedVideo] = videos
        self.download_directory = download_directory
        self.videos: List[DownloadingVideo] = []
        # vars for state track
        self.waiting_videos: List[DownloadingVideo] = []
        self.downloading_videos: List[DownloadingVideo] = []
        self.paused_videos: List[DownloadingVideo] = []
        self.failed_videos: List[DownloadingVideo] = []
        self.completed_videos: List[DownloadingVideo] = []

        super().__init__(
            master=master,
            height=height,
            width=width,
            channel_url=channel_url,
            playlist_url=playlist_url,
            playlist_title=playlist_title,
            channel=channel,
            playlist_video_count=playlist_video_count,
        )
        self.channel_btn.configure(state="normal")
        threading.Thread(target=self.download_videos).start()

    def re_download_videos(self):
        self.re_download_btn.place_forget()
        for video in self.videos:
            if video.download_state == "failed":
                video.re_download_video()

    def download_videos(self):
        for added_video in self.added_videos:
            video = DownloadingVideo(
                master=self.playlist_item_frame,
                height=70,
                width=self.playlist_item_frame.winfo_width() - 20,
                channel_url=added_video.channel_url,
                video_url=added_video.video_url,
                # download info
                download_type=added_video.download_type,
                download_quality=added_video.download_quality,
                download_directory=self.download_directory,
                # video info
                video_title=added_video.video_title,
                channel=added_video.channel,
                thumbnails=added_video.thumbnails,
                video_stream_data=added_video.video_stream_data,
                length=added_video.length,
                # download mode
                mode="playlist",
                video_download_complete_callback=None,
                # videos state, download progress track
                video_download_status_callback=self.videos_status_track,
                video_download_progress_callback=self.videos_progress_track,
            )
            video.pack(fill="x", padx=(20, 0), pady=1)
            self.videos.append(video)
        self.view_btn.configure(state="normal")

    def videos_status_track(
            self,
            video: DownloadingVideo,
            state: Literal["waiting", "downloading", "paused", "completed", "failed", "removed"]):
        if state == "removed":
            self.videos.remove(video)
            self.playlist_video_count -= 1
            if len(self.videos) == 0:
                self.kill()
            else:
                if video in self.downloading_videos:
                    self.downloading_videos.remove(video)
                if video in self.failed_videos:
                    self.failed_videos.remove(video)
                if video in self.waiting_videos:
                    self.waiting_videos.remove(video)
                if video in self.completed_videos:
                    self.completed_videos.remove(video)
                if video in self.paused_videos:
                    self.paused_videos.remove(video)
        elif state == "failed":
            self.failed_videos.append(video)
            if video in self.downloading_videos:
                self.downloading_videos.remove(video)
            if video in self.paused_videos:
                self.paused_videos.remove(video)
        elif state == "downloading":
            self.downloading_videos.append(video)
            if video in self.waiting_videos:
                self.waiting_videos.remove(video)
            if video in self.failed_videos:
                self.failed_videos.remove(video)
            if video in self.paused_videos:
                self.paused_videos.remove(video)
        elif state == "paused":
            self.paused_videos.append(video)
            if video in self.downloading_videos:
                self.downloading_videos.remove(video)
        elif state == "waiting":
            self.waiting_videos.append(video)
            if video in self.failed_videos:
                self.failed_videos.remove(video)
        elif state == "completed":
            self.completed_videos.append(video)
            self.downloading_videos.remove(video)

        if len(self.videos) != 0:
            self.videos_status_label.configure(
                text=f"Failed : {len(self.failed_videos)} |   "
                     f"Waiting : {len(self.waiting_videos)} |   "
                     f"Downloading : {len(self.downloading_videos)} |   "
                     f"Paused : {len(self.paused_videos)} |   "
                     f"Downloaded : {len(self.completed_videos)}",
                )
            self.playlist_video_count_label.configure(
                text=self.playlist_video_count
            )
            if len(self.failed_videos) != 0:
                self.indicate_downloading_failure()
            else:
                self.clear_downloading_failure()
            if len(self.downloading_videos) == 0 and len(self.waiting_videos) == 0 and \
                    len(self.failed_videos) == 0 and len(self.paused_videos) == 0:
                self.set_downloading_completed()

    def videos_progress_track(self):
        total_completion: float = 0
        for video in self.videos:
            if video.file_size != 0:
                total_completion += video.bytes_downloaded / video.file_size
        avg_completion = total_completion / self.playlist_video_count
        self.set_playlist_download_progress(avg_completion)

    def set_playlist_download_progress(self, progress):
        self.download_progress_bar.set(progress)
        self.download_percentage_label.configure(text=f"{round(progress * 100, 2)} %")

    def indicate_downloading_failure(self):
        self.re_download_btn.place(relx=1, y=32, x=-80)
        self.status_label.configure(text="Failed", text_color=ThemeManager.theme_settings["video_object"]["error_color"]["normal"])

    def clear_downloading_failure(self):
        self.re_download_btn.place_forget()
        self.status_label.configure(text="Downloading", text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"])

    def set_downloading_completed(self):
        self.status_label.configure(text="Downloaded", text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"])
        self.playlist_download_complete_callback(self)
        self.kill()

    def kill(self):
        for video in self.videos:
            video.video_download_status_callback = pass_command
            video.kill()
        super().kill()

    # create widgets
    def create_widgets(self):
        super().create_widgets()

        self.sub_frame = ctk.CTkFrame(
            self,
            height=self.height - 4,
        )

        self.download_progress_bar = ctk.CTkProgressBar(
            master=self.sub_frame,
            height=8
        )

        self.download_percentage_label = ctk.CTkLabel(
            master=self.sub_frame,
            text="",
            font=("arial", 12, "bold"),
        )

        self.status_label = ctk.CTkLabel(
            master=self.sub_frame,
            text="",
            font=("arial", 12, "bold"),
        )

        self.re_download_btn = ctk.CTkButton(
            self,
            text="⟳",
            width=15, height=15,
            font=("arial", 20, "normal"),
            command=self.re_download_videos,
            hover=False
        )

        self.videos_status_label = ctk.CTkLabel(
            master=self.sub_frame,
            text=f"Failed : {len(self.failed_videos)} |   "
                 f"Waiting : {len(self.waiting_videos)} |   "
                 f"Downloading : {len(self.downloading_videos)} |   "
                 f"Paused : {len(self.paused_videos)} |   "
                 f"Downloaded : {len(self.completed_videos)}",
            height=15,
            font=("arial", 11, "bold"),
        )

    # configure widgets colors depend on root width
    def set_accent_color(self):
        super().set_accent_color()
        self.re_download_btn.configure(text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"])

    def set_widgets_colors(self):
        super().set_widgets_colors()
        self.sub_frame.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]
        )
        self.download_percentage_label.configure(
            text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"]
        )
        self.status_label.configure(
            text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"]
        )
        self.re_download_btn.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]
        )

    def on_mouse_enter_self(self, _event):
        super().on_mouse_enter_self(_event)
        self.sub_frame.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])
        self.re_download_btn.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])

    def on_mouse_leave_self(self, _event):
        super().on_mouse_leave_self(_event)
        self.sub_frame.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])
        self.re_download_btn.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])

    def bind_widget_events(self):
        super().bind_widget_events()

        def on_mouse_enter_re_download_btn(_event):
            self.re_download_btn.configure(
                fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"],
                text_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"]
            )
            self.on_mouse_enter_self(_event)

        def on_mouse_leave_download_btn(_event):
            self.re_download_btn.configure(
                fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"],
                text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
            )
        self.re_download_btn.bind("<Enter>", on_mouse_enter_re_download_btn)
        self.re_download_btn.bind("<Leave>", on_mouse_leave_download_btn)

    # place widgets
    def place_widgets(self):
        super().place_widgets()
        self.title_label.place(x=50, y=10, height=20, width=-20, relwidth=0.5)
        self.channel_btn.place(x=50, y=34, height=20, width=-20, relwidth=0.5)
        self.url_label.place(x=50, y=54, height=20, width=-20, relwidth=0.5)

        self.sub_frame.place(relx=0.5, y=2, x=50)
        self.download_percentage_label.place(relx=0.5, anchor="n", y=4)
        self.download_percentage_label.configure(height=20)
        self.download_progress_bar.place(relwidth=1, y=28)
        self.status_label.place(relx=0.775, anchor="n", y=40)
        self.status_label.configure(height=20)
        self.videos_status_label.place(rely=1, y=-18, relx=0.5, anchor="n")

    # configure widgets sizes and place location depend on root width
    def configure_widget_sizes(self, e):
        self.sub_frame.configure(width=self.winfo_width() / 2 - 150)
