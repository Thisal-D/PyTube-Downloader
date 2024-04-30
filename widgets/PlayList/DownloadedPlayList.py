from widgets.PlayList import PlayList
from widgets.Video.DownloadedVideo import DownloadedVideo
from widgets.Video.DownloadingVideo import DownloadingVideo
from typing import Literal, List, Any
from functions import pass_command
import threading


class DownloadedPlayList(PlayList):
    def __init__(
            self,
            master: Any = None,
            width: int = 0,
            height: int = 0,
            # playlist info
            channel_url: str = "",
            playlist_url: str = "",
            playlist_title: str = "---------",
            channel: str = "---------",
            playlist_video_count: int = 0,
            # videos of playlist
            videos: List[DownloadingVideo] = None):

        # playlist videos
        self.downloading_videos: List[DownloadingVideo] = videos
        self.videos: List[DownloadedVideo] = []

        super().__init__(
            master=master,
            width=width,
            height=height,
            # playlist info
            channel_url=channel_url,
            playlist_url=playlist_url,
            playlist_title=playlist_title,
            channel=channel,
            playlist_video_count=playlist_video_count,
        )

        threading.Thread(target=self.display_downloaded_widgets, daemon=True).start()

    def display_downloaded_widgets(self):
        for downloading_video in self.downloading_videos:
            video = DownloadedVideo(
                master=self.playlist_item_frame,
                height=70,
                width=self.playlist_item_frame.winfo_width() - 20,
                # video info
                thumbnails=downloading_video.thumbnails,
                video_title=downloading_video.video_title,
                channel=downloading_video.channel,
                channel_url=downloading_video.channel_url,
                video_url=downloading_video.video_url,
                file_size=downloading_video.file_size,
                length=downloading_video.length,
                # download info
                download_path=downloading_video.download_file_name,
                download_quality=downloading_video.download_quality,
                download_type=downloading_video.download_type,
                # state callbacks
                mode=downloading_video.mode,
                video_status_callback=self.videos_status_track,
            )
            video.pack(fill="x", padx=(20, 0), pady=1)
            self.videos.append(video)
        self.view_btn.configure(state="normal")

    # status tracker
    def videos_status_track(
            self,
            video: DownloadedVideo,
            state: Literal["removed"]):
        if state == "removed":
            self.videos.remove(video)
            self.playlist_video_count -= 1
            if self.playlist_video_count == 0:
                self.kill()
            else:
                self.playlist_video_count_label.configure(
                    text=self.playlist_video_count
                )

    # configure widgets colors
    def set_accent_color(self):
        super().set_accent_color()

    def kill(self):
        for video in self.videos:
            video.video_status_callback = pass_command
            video.kill()
        super().kill()
