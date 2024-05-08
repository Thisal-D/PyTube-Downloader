from widgets.video import Video
import customtkinter as ctk
import threading
import time
import os
from tkinter import PhotoImage
from typing import Literal, List, Union
from pytube import request as pytube_request
from settings import (
    GeneralSettings,
    AppearanceSettings,
    WidgetPositionSettings
)
from services import (
    DownloadManager
)
from utils import (
    GuiUtils,
    ValueConvertUtility,
    FileUtility
)


class DownloadingVideo(Video):
    """A class representing a downloading video widget."""

    def __init__(
            self,
            root: ctk.CTk,
            master: Union[ctk.CTkFrame, ctk.CTkScrollableFrame],
            width: int = 0,
            height: int = 0,
            # download quality & type
            download_quality: Literal["128kbps", "360p", "720p"] = "720p",
            download_type: Literal["Video", "Audio"] = "Video",
            # video details
            video_title: str = "-------",
            channel: str = "-------",
            video_url: str = "-------",
            channel_url: str = "-------",
            length: int = 0,
            thumbnails: List[PhotoImage] = (None, None),
            # video stream data
            video_stream_data: property = None,
            # video download callback utils @ only use if mode is video
            video_download_complete_callback: callable = None,
            # state callbacks only use if mode is playlist
            mode: Literal["video", "playlist"] = "video",
            video_download_status_callback: callable = None,
            video_download_progress_callback: callable = None):

        # download status track and callback
        self.download_state: Literal["waiting", "downloading", "failed", "completed", "removed"] = "waiting"
        self.pause_requested: bool = False
        self.pause_resume_btn_command: Literal["pause", "resume"] = "pause"
        # status and progress callbacks
        self.video_download_complete_callback: callable = video_download_complete_callback
        self.video_download_status_callback: callable = video_download_status_callback
        self.video_download_progress_callback: callable = video_download_progress_callback
        # download info
        self.download_quality: Literal["128kbps", "360p", "720p"] = download_quality
        self.download_type: Literal["Video", "Audio"] = download_type
        self.video_stream_data: property = video_stream_data
        # download mode
        self.mode: Literal["video", "playlist"] = mode
        # widgets
        self.sub_frame: Union[ctk.CTkFrame, None] = None
        self.download_progress_bar: Union[ctk.CTkProgressBar, None] = None
        self.download_progress_label: Union[ctk.CTkLabel, None] = None
        self.download_percentage_label: Union[ctk.CTkLabel, None] = None
        self.download_type_label: Union[ctk.CTkLabel, None] = None
        self.net_speed_label: Union[ctk.CTkLabel, None] = None
        self.status_label: Union[ctk.CTkLabel, None] = None
        self.re_download_btn: Union[ctk.CTkButton, None] = None
        self.pause_resume_btn: Union[ctk.CTkButton, None] = None
        # download file info
        self.bytes_downloaded: int = 0
        self.file_size: int = 0
        self.converted_file_size: str = "0 B"
        self.download_file_name: str = ""

        super().__init__(
            root=root,
            master=master,
            height=height,
            width=width,
            video_url=video_url,
            channel_url=channel_url,
            thumbnails=thumbnails,
            video_title=video_title,
            channel=channel,
            length=length
        )

        self.set_video_data()
        self.set_waiting()
        DownloadManager.register(self)

    def download_video(self):
        """
        Start the video download process.
        """
        threading.Thread(target=self.retrieve_file, daemon=True).start()
        self.set_pause_btn()
        self.pause_resume_btn.place(
            y=WidgetPositionSettings.settings["DownloadingVideo"][str(AppearanceSettings.settings["scale_r"])][6],
            relx=1,
            x=-80 * AppearanceSettings.settings["scale_r"])
        self.net_speed_label.configure(text="0.0 B/s")
        self.download_progress_bar.set(0)
        self.download_percentage_label.configure(text="0.0 %")
        self.download_state = "downloading"
        if self.mode == "playlist":
            self.video_download_status_callback(self, self.download_state)
        self.display_status()

    def re_download_video(self):
        """
        Re-download the video.
        """
        self.re_download_btn.place_forget()
        self.set_waiting()
        DownloadManager.register(self)

    def display_status(self):
        """
        Display the status of the download.
        """
        
        if self.download_state == "failed":
            self.status_label.configure(
                text_color=AppearanceSettings.settings["video_object"]["error_color"]["normal"],
                text="Failed"
            )
        elif self.download_state == "waiting":
            self.status_label.configure(
                text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"],
                text="Waiting"
            )
        elif self.download_state == "paused":
            self.status_label.configure(
                text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"],
                text="Paused"
            )
        elif self.download_state == "downloading":
            self.status_label.configure(
                text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"],
                text="Downloading"
            )
        elif self.download_state == "pausing":
            self.status_label.configure(
                text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"],
                text="Pausing"
            )
        elif self.download_state == "completed":
            self.status_label.configure(
                text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"],
                text="Downloaded"
            )

    def retrieve_file(self):
        """
        Download the video.
        """
        
        if not os.path.exists(GeneralSettings.settings["download_directory"]):
            try:
                FileUtility.create_directory(GeneralSettings.settings["download_directory"])
            except Exception as error:
                print("@2 : ", error)
                self.set_downloading_failed()
                return

        stream = None
        self.bytes_downloaded = 0
        self.download_file_name = (
                f"{GeneralSettings.settings["download_directory"]}\\" +
                f"{FileUtility.sanitize_filename(f"{self.channel} - {self.video_title}")}"
            )
        try:
            self.download_type_label.configure(text=f"{self.download_type} : {self.download_quality}")
            if self.download_type == "Video":
                stream = self.video_stream_data.get_by_resolution(self.download_quality)
                self.download_file_name += ".mp4"
            else:
                stream = self.video_stream_data.get_audio_only()
                self.download_file_name += ".mp3"
            self.file_size = stream.filesize
            self.converted_file_size = ValueConvertUtility.convert_size(self.file_size, 2)
            self.download_file_name = FileUtility.get_available_file_name(self.download_file_name)
            self.set_downloading_progress()
        except Exception as error:
            print("@1 : ", error)
            self.set_downloading_failed()

        try:
            with open(self.download_file_name, "wb") as self.video_file:
                stream = pytube_request.stream(stream.url)
                while 1:
                    try:
                        time_s = time.time()
                        if self.pause_requested:
                            if self.pause_resume_btn_command != "resume":
                                self.pause_resume_btn.configure(command=self.resume_downloading)
                                self.download_state = "paused"
                                if self.mode == "playlist":
                                    self.video_download_status_callback(self, self.download_state)
                                self.display_status()
                                self.set_resume_btn()
                                self.pause_resume_btn_command = "resume"
                            time.sleep(0.3)
                            continue
                        self.download_state = "downloading"
                        self.pause_resume_btn_command = "pause"
                        chunk = next(stream, None)
                        time_e = time.time()
                        if chunk:
                            self.video_file.write(chunk)
                            self.net_speed_label.configure(
                                text=ValueConvertUtility.convert_size(
                                    ((self.bytes_downloaded + len(chunk)) - self.bytes_downloaded) / (time_e - time_s),
                                    1
                                ) + "/s"
                            )
                            self.bytes_downloaded += len(chunk)
                            self.set_downloading_progress()
                        else:
                            if self.bytes_downloaded == self.file_size:
                                self.set_downloading_completed()
                                break
                            else:
                                self.set_downloading_failed()
                                break
                    except Exception as error:
                        print("@3 downloading_play_list.py : ", error)
                        self.set_downloading_failed()
                        break
        except Exception as error:
            print("@4 downloading_play_list.py : ", error)
            self.set_downloading_failed()

    def set_resume_btn(self):
        """
        Set the resume button.
        """
        
        self.pause_resume_btn.configure(text="▷")

    def set_pause_btn(self):
        """
        Set the pause button.
        """
        
        self.pause_resume_btn.configure(text="⏸")

    def pause_downloading(self):
        """
        Pause the downloading process.
        """

        self.pause_resume_btn.configure(command=GuiUtils.do_nothing)
        self.download_state = "pausing"
        self.display_status()
        self.pause_requested = True

    def resume_downloading(self):
        """
        Resume the downloading process.
        """
        
        self.pause_requested = False
        self.set_pause_btn()
        while self.download_state == "paused":
            time.sleep(0.3)
        self.pause_resume_btn.configure(command=self.pause_downloading)
        self.download_state = "downloading"
        if self.mode == "playlist":
            self.video_download_status_callback(self, self.download_state)
        self.display_status()

    def set_downloading_progress(self):
        """
        Set the progress of the downloading process.
        """
        
        completed_percentage = self.bytes_downloaded / self.file_size
        self.download_progress_bar.set(completed_percentage)
        self.download_percentage_label.configure(text=f"{round(completed_percentage * 100, 2)} %")
        self.download_progress_label.configure(
            text=f"{ValueConvertUtility.convert_size(self.bytes_downloaded, 2)} / {self.converted_file_size}"
        )
        if self.mode == "playlist":
            self.video_download_progress_callback()

    def set_downloading_failed(self):
        """
        Set the status to 'failed' if downloading fails.
        """

        if self.download_state != "removed":
            self.download_state = "failed"
            self.display_status()
            if self.mode == "playlist":
                self.video_download_status_callback(self, self.download_state)
            DownloadManager.unregister_from_active(self)
            self.pause_resume_btn.place_forget()
            self.re_download_btn.place(
                y=WidgetPositionSettings.settings["DownloadingVideo"][str(AppearanceSettings.settings["scale_r"])][7],
                relx=1,
                x=-80 * AppearanceSettings.settings["scale_r"])

    def set_waiting(self):
        """
        Set the status to 'waiting' if the download is queued.
        """
        
        DownloadManager.unregister_from_queued(self)
        self.download_state = "waiting"
        if self.mode == "playlist":
            self.video_download_status_callback(self, self.download_state)
        self.display_status()
        self.pause_resume_btn.place_forget()
        self.download_progress_bar.set(0.5)
        self.download_percentage_label.configure(text="")
        self.net_speed_label.configure(text="")
        self.download_progress_label.configure(text="")
        self.download_type_label.configure(text="")

    def set_downloading_completed(self):
        """
        Set the status to 'completed' if the download is completed.
        """

        DownloadManager.unregister_from_active(self)
        self.pause_resume_btn.place_forget()
        self.download_state = "completed"
        self.display_status()
        if self.mode == "playlist":
            self.video_download_status_callback(self, self.download_state)
        if self.mode == "video":
            self.video_download_complete_callback(self)
            self.kill()

    def kill(self):
        """
        Kill the downloading process.
        """
        
        DownloadManager.unregister_from_active(self)
        DownloadManager.unregister_from_queued(self)
        self.download_state = "removed"
        if self.mode == "playlist":
            self.video_download_status_callback(self, self.download_state)

        super().kill()

    # create widgets
    def create_widgets(self):
        """
        Create all required widgets.
        """
        
        super().create_widgets()

        self.sub_frame = ctk.CTkFrame(self)
        self.download_progress_bar = ctk.CTkProgressBar(master=self.sub_frame)
        self.download_progress_label = ctk.CTkLabel(master=self.sub_frame, text="")
        self.download_percentage_label = ctk.CTkLabel(master=self.sub_frame, text="")
        self.download_type_label = ctk.CTkLabel(master=self.sub_frame, text="")
        self.net_speed_label = ctk.CTkLabel(master=self.sub_frame, text="")
        self.status_label = ctk.CTkLabel(master=self.sub_frame, text="")
        self.re_download_btn = ctk.CTkButton(
            master=self,
            text="⟳",
            command=self.re_download_video,
            hover=False
        )
        self.pause_resume_btn = ctk.CTkButton(
            master=self,
            text="⏸",
            command=self.pause_downloading,
            hover=False
        )

    def set_widgets_fonts(self):
        """
        Set fonts for all widgets.
        """
        
        super().set_widgets_fonts()

        scale = AppearanceSettings.settings["scale_r"]

        self.download_progress_label.configure(font=("arial", 12 * scale, "bold"))
        self.download_percentage_label.configure(font=("arial", 12 * scale, "bold"))
        self.download_type_label.configure(font=("arial", 12 * scale, "normal"))
        self.net_speed_label.configure(font=("arial", 12 * scale, "normal"), )
        self.status_label.configure(font=("arial", 12 * scale, "bold"))
        self.re_download_btn.configure(font=("arial", 20 * scale, "normal"))
        self.pause_resume_btn.configure(font=("arial", 20 * scale, "normal"))

    def set_widgets_sizes(self):
        """
        Set sizes for all widgets.
        """
        
        super().set_widgets_sizes()

        scale = AppearanceSettings.settings["scale_r"]

        self.sub_frame.configure(height=self.height - 4)
        self.download_progress_bar.configure(height=8 * scale, width=self.sub_frame.winfo_width())
        self.download_progress_label.configure(height=20 * scale)
        self.download_percentage_label.configure(height=20 * scale)
        self.download_type_label.configure(height=20 * scale)
        self.net_speed_label.configure(height=20 * scale)
        self.status_label.configure(height=20 * scale)
        self.re_download_btn.configure(width=15 * scale, height=15 * scale)
        self.pause_resume_btn.configure(width=15 * scale, height=15 * scale)

    def set_widgets_accent_color(self):
        """
        Set accent colors for widgets.
        """
        
        super().set_widgets_accent_color()

        self.download_progress_bar.configure(
            progress_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.re_download_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        self.pause_resume_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

    def set_widgets_colors(self) -> None:
        """
        Set colors for all widgets.
        """
        
        super().set_widgets_colors()

        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.download_progress_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.download_percentage_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.download_type_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.net_speed_label.configure(text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"])
        self.status_label.configure(text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"])
        self.re_download_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.pause_resume_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])

    def on_mouse_enter_self(self, event):
        """
        Handle mouse entering the widget area.
        """
        
        super().on_mouse_enter_self(event)

        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])
        self.re_download_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])
        self.pause_resume_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])

    def on_mouse_leave_self(self, event):
        """
        Handle mouse leaving the widget area.
        """

        super().on_mouse_leave_self(event)

        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.re_download_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.pause_resume_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])

    def bind_widgets_events(self):
        """
        Bind events to all widgets.
        """
        
        super().bind_widgets_events()

        self.bind("<Configure>", self.configure_widget_sizes)

        def on_mouse_enter_re_download_btn(event):
            self.re_download_btn.configure(
                fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"],
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )
            self.on_mouse_enter_self(event)

        def on_mouse_leave_download_btn(_event):
            self.re_download_btn.configure(
                fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.re_download_btn.bind("<Enter>", on_mouse_enter_re_download_btn)
        self.re_download_btn.bind("<Leave>", on_mouse_leave_download_btn)

        def on_mouse_enter_pause_resume_btn(event):
            self.pause_resume_btn.configure(
                fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"],
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )
            self.on_mouse_enter_self(event)

        def on_mouse_leave_pause_resume_btn(_event):
            self.pause_resume_btn.configure(
                fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.pause_resume_btn.bind("<Enter>", on_mouse_enter_pause_resume_btn)
        self.pause_resume_btn.bind("<Leave>", on_mouse_leave_pause_resume_btn)

    def place_widgets(self):
        """
        Place all widgets using a grid layout.
        """
        
        super().place_widgets()

        scale = AppearanceSettings.settings["scale_r"]
        y = WidgetPositionSettings.settings["DownloadingVideo"][str(scale)]

        self.video_title_label.place(relwidth=0.5, width=-150 * scale)
        self.channel_btn.place(relwidth=0.5, width=-150 * scale)
        self.url_label.place(relwidth=0.5, width=-150 * scale)
        self.sub_frame.place(relx=0.5, y=2)
        self.download_progress_label.place(relx=0.25, anchor="n", y=y[0])
        self.download_type_label.place(relx=0.75, anchor="n", y=y[1])
        self.download_progress_bar.place(relwidth=1, y=y[2] * scale)
        self.download_percentage_label.place(relx=0.115, anchor="n", y=y[3])
        self.net_speed_label.place(relx=0.445, anchor="n", y=y[4])
        self.status_label.place(relx=0.775, anchor="n", y=y[5])

    def configure_widget_sizes(self, _event):
        """
        Configure widget sizes based on the parent widget's size.
        """
        
        self.sub_frame.configure(width=self.master.winfo_width() / 2 - 100 * AppearanceSettings.settings["scale_r"])
