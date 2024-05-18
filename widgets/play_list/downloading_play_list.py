import customtkinter as ctk
import threading
from typing import List, Literal, Union, Callable
from widgets.play_list import PlayList
from widgets.video.downloading_video import DownloadingVideo
from widgets.video.added_video import AddedVideo
from utils import GuiUtils
from settings import AppearanceSettings
from services import LanguageManager


class DownloadingPlayList(PlayList):
    def __init__(
            self,
            root: ctk.CTk = None,
            master: ctk.CTkScrollableFrame = None,
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
            # playlist download completed callback utils
            playlist_download_complete_callback: Callable = None):

        # widgets
        self.sub_frame: Union[ctk.CTkFrame, None] = None
        self.download_progress_bar: Union[ctk.CTkProgressBar, None] = None
        self.download_percentage_label: Union[ctk.CTkLabel, None] = None
        self.status_label: Union[ctk.CTkLabel, None] = None
        self.re_download_btn: Union[ctk.CTkButton, None] = None
        self.videos_status_counts_label: Union[ctk.CTkLabel, None] = None
        # callback utils
        self.playlist_download_complete_callback = playlist_download_complete_callback
        self.added_videos: List[AddedVideo] = videos
        self.videos: List[DownloadingVideo] = []
        # vars for state track
        self.waiting_videos: List[DownloadingVideo] = []
        self.downloading_videos: List[DownloadingVideo] = []
        self.paused_videos: List[DownloadingVideo] = []
        self.failed_videos: List[DownloadingVideo] = []
        self.downloaded_videos: List[DownloadingVideo] = []
        self.download_state: Literal["waiting", "downloading", "downloaded", "failed"] = "waiting"

        super().__init__(
            root=root,
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
        self.indicate_waiting()
        threading.Thread(target=self.download_videos, daemon=True).start()

    def download_videos(self):
        for added_video in self.added_videos:
            video = DownloadingVideo(
                root=self.root,
                master=self.playlist_item_frame,
                height=70 * AppearanceSettings.settings["scale_r"],
                width=self.playlist_item_frame.winfo_width() - 20,
                channel_url=added_video.channel_url,
                video_url=added_video.video_url,
                # download info
                download_type=added_video.download_type,
                download_quality=added_video.download_quality,
                # video info
                video_title=added_video.video_title,
                channel=added_video.channel,
                thumbnails=added_video.thumbnails,
                video_stream_data=added_video.video_stream_data,
                length=added_video.length,
                # download mode
                playlist_title=self.playlist_title,
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
            state: Literal["waiting", "downloading", "paused", "downloaded", "failed", "removed"]):
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
                if video in self.downloaded_videos:
                    self.downloaded_videos.remove(video)
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
        elif state == "downloaded":
            self.downloaded_videos.append(video)
            self.downloading_videos.remove(video)

        # if len is 0 that means all videos are remove :D
        if len(self.videos) != 0:
            self.videos_status_counts_label.configure(
                text=f"{LanguageManager.data['failed']} : {len(self.failed_videos)} |   "
                     f"{LanguageManager.data['waiting']} : {len(self.waiting_videos)} |   "
                     f"{LanguageManager.data['downloading']} : {len(self.downloading_videos)} |   "
                     f"{LanguageManager.data['paused']} : {len(self.paused_videos)} |   "
                     f"{LanguageManager.data['downloaded']} : {len(self.downloaded_videos)}",
                )
            self.playlist_video_count_label.configure(
                text=self.playlist_video_count
            )

            if len(self.failed_videos) != 0:
                self.indicate_downloading_failure()
            else:
                # if all videos waiting
                if len(self.waiting_videos) == self.playlist_video_count:
                    self.indicate_waiting()
                else:
                    self.indicate_downloading()
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

    def re_download_videos(self):
        if len(self.downloading_videos) == 0:
            self.indicate_waiting()
        else:
            self.indicate_downloading()
        for video in self.videos:
            if video.download_state == "failed":
                video.re_download_video()

    def indicate_waiting(self):
        self.download_state = "waiting"
        self.re_download_btn.place_forget()
        self.status_label.configure(
            text=LanguageManager.data['waiting'],
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )

    def indicate_downloading_failure(self):
        self.download_state = "failed"
        self.re_download_btn.place(
            relx=1,
            rely=0.5,
            anchor="w",
            x=-80 * AppearanceSettings.settings["scale_r"])
        self.status_label.configure(
            text=LanguageManager.data['failed'],
            text_color=AppearanceSettings.settings["video_object"]["error_color"]["normal"]
        )

    def indicate_downloading(self):
        self.download_state = "downloading"
        self.re_download_btn.place_forget()
        self.status_label.configure(
            text=LanguageManager.data['downloading'],
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )

    def set_downloading_completed(self):
        self.download_state = "downloaded"
        self.status_label.configure(
            text=LanguageManager.data['downloaded'],
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.playlist_download_complete_callback(self)
        self.kill()

    def kill(self):
        for video in self.videos:
            video.video_download_status_callback = GuiUtils.do_nothing
            video.kill()
        super().kill()

    # create widgets
    def create_widgets(self):
        super().create_widgets()

        self.sub_frame = ctk.CTkFrame(self)
        self.download_progress_bar = ctk.CTkProgressBar(master=self.sub_frame)
        self.download_percentage_label = ctk.CTkLabel(master=self.sub_frame, text="")
        self.status_label = ctk.CTkLabel(master=self.sub_frame)
        self.re_download_btn = ctk.CTkButton(
            self.playlist_main_frame,
            text="⟳",
            command=self.re_download_videos, hover=False
        )
        self.videos_status_counts_label = ctk.CTkLabel(master=self.sub_frame)

    def set_widgets_texts(self):
        super().set_widgets_texts()
        self.status_label.configure(text=LanguageManager.data[self.download_state])
        self.videos_status_counts_label.configure(
            text=f"{LanguageManager.data['failed']} : {len(self.failed_videos)} |   "
                 f"{LanguageManager.data['waiting']} : {len(self.waiting_videos)} |   "
                 f"{LanguageManager.data['downloading']} : {len(self.downloading_videos)} |   "
                 f"{LanguageManager.data['paused']} : {len(self.paused_videos)} |   "
                 f"{LanguageManager.data['downloaded']} : {len(self.downloaded_videos)}",
        )

    def set_widgets_fonts(self):
        super().set_widgets_fonts()

        scale = AppearanceSettings.settings["scale_r"]

        self.download_percentage_label.configure(font=("arial", 12 * scale, "bold"))
        self.status_label.configure(font=("arial", 12 * scale, "bold"))
        self.re_download_btn.configure(font=("arial", 20 * scale, "normal"))
        self.videos_status_counts_label.configure(font=("Segoe UI", 11 * scale, "normal"))

    def set_widgets_sizes(self):
        super().set_widgets_sizes()

        scale = AppearanceSettings.settings["scale_r"]

        self.sub_frame.configure(height=self.height - 3)
        self.download_progress_bar.configure(height=8 * scale)
        self.download_percentage_label.configure(height=15 * scale)
        self.status_label.configure(height=15 * scale)
        self.re_download_btn.configure(width=15 * scale, height=15 * scale)
        self.videos_status_counts_label.configure(height=15 * scale)

    # configure widgets colors depend on root width
    def set_widgets_accent_color(self):
        super().set_widgets_accent_color()
        self.download_progress_bar.configure(
            progress_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.re_download_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

    def set_widgets_colors(self):
        super().set_widgets_colors()

        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.download_percentage_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.status_label.configure(text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"])
        self.re_download_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])

    def on_mouse_enter_self(self, _event):
        super().on_mouse_enter_self(_event)

        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])
        self.re_download_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])

    def on_mouse_leave_self(self, _event):
        super().on_mouse_leave_self(_event)

        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.re_download_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])

    def bind_widgets_events(self):
        super().bind_widgets_events()

        def on_mouse_enter_re_download_btn(_event):
            self.re_download_btn.configure(
                fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"],
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )
            self.on_mouse_enter_self(_event)

        def on_mouse_leave_download_btn(_event):
            self.re_download_btn.configure(
                fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )
        self.re_download_btn.bind("<Enter>", on_mouse_enter_re_download_btn)
        self.re_download_btn.bind("<Leave>", on_mouse_leave_download_btn)

    # place widgets
    def place_widgets(self):
        super().place_widgets()

        self.sub_frame.place(relx=0.5, y=1)
        self.download_percentage_label.place(relx=0.15, anchor="center", rely=0.2)
        self.download_progress_bar.place(relwidth=1, rely=0.4, anchor="w")
        self.status_label.place(relx=0.775, anchor="n", rely=0.55)
        self.videos_status_counts_label.place(rely=0.875, relx=0.5, anchor="center")

    # configure widgets sizes and place location depend on root width
    def configure_widget_sizes(self, _event):
        scale = AppearanceSettings.settings["scale_r"]
        self.info_frame.configure(
            width=self.master.winfo_width() / 2 - (50 * scale + 15 * scale) - (20 * scale)
        )
        self.sub_frame.configure(width=(self.winfo_width() / 2) - (110 * scale))
