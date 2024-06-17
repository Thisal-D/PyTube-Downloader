from widgets.play_list import PlayList
from widgets.video.downloaded_video import DownloadedVideo
from widgets.video.downloading_video import DownloadingVideo
import customtkinter as ctk
from typing import Literal, List
from utils import GuiUtils
import threading
from settings import AppearanceSettings


class DownloadedPlayList(PlayList):
    def __init__(
            self,
            root: ctk.CTk = None,
            master: ctk.CTkScrollableFrame = None,
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

        super().__init__(
            root=root,
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
                root=self.root,
                master=self.playlist_item_frame,
                height=70 * AppearanceSettings.settings["scale_r"],
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

    def configure_widget_sizes(self, _event):
        scale = AppearanceSettings.settings["scale_r"]
        self.info_frame.configure(
            width=self.master_frame.winfo_width() - (50 * scale + 15 * scale) - (60 * scale)
        )

    def __del__(self):
        """Clear the Memory."""
        del self.downloading_videos
        
        super().__del__()
        
    def destroy_widgets(self):
        """Destroy the child widget."""
            
        super().destroy_widgets()
    
    def kill(self):
        self.pack_forget()
        
        for video in self.videos:
            video.video_status_callback = GuiUtils.do_nothing
            video.kill()
            
        super().kill()