from widgets.Video import Video
import customtkinter as ctk
import threading
import time
import os
from tkinter import PhotoImage
from typing import Literal, List, Union, Any
from pytube import request as pytube_request
from services import DownloadManager
from functions import (
    pass_command,
    get_converted_size,
    get_valid_file_name,
    get_available_file_name,
    create_download_directory
)
from services import ThemeManager


class DownloadingVideo(Video):
    def __init__(
            self,
            master: Any,
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
            # video download callback functions @ only use if mode is video
            video_download_complete_callback: callable = None,
            # state callback functions @ only use if mode is video
            mode: Literal["video", "playlist"] = "video",
            video_download_status_callback: callable = None,
            video_download_progress_callback: callable = None,
            # download method and directory
            download_directory: str = ""):

        # download status track and callback
        self.download_state: Literal["waiting", "downloading", "failed", "completed", "removed"] = "waiting"
        self.pause_requested: bool = False
        self.pause_resume_btn_command: Literal["pause", "resume"] = "pause"
        # callback
        self.video_download_complete_callback: callable = video_download_complete_callback
        self.video_download_status_callback: callable = video_download_status_callback
        self.video_download_progress_callback: callable = video_download_progress_callback
        # selected download quality and type
        self.download_quality: Literal["128kbps", "360p", "720p"] = download_quality
        self.download_type: Literal["Video", "Audio"] = download_type
        self.video_stream_data: property = video_stream_data
        # playlist or video
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
        self.download_directory: str = download_directory
        self.bytes_downloaded: int = 0
        self.file_size: int = 0
        self.converted_file_size: str = "0 B"
        self.download_file_name: str = ""

        super().__init__(
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
        threading.Thread(target=self.start_download_video).start()

    def start_download_video(self):
        if DownloadManager.max_concurrent_downloads > DownloadManager.active_download_count:
            DownloadManager.active_download_count += 1
            DownloadManager.active_downloads.append(self)
            threading.Thread(target=self.download_video).start()
            self.set_pause_btn()
            self.pause_resume_btn.place(y=22, relx=1, x=-80)
            self.net_speed_label.configure(text="0.0 B/s")
            self.download_progress_bar.set(0)
            self.download_percentage_label.configure(text="0.0 %")
            self.download_state = "downloading"
            if self.mode == "playlist":
                self.video_download_status_callback(self, self.download_state)
            self.display_status()

        else:
            self.set_waiting()

    def re_download_video(self):
        self.re_download_btn.place_forget()
        self.start_download_video()

    def display_status(self):
        if self.download_state == "failed":
            self.status_label.configure(text_color=ThemeManager.theme_settings["video_object"]["error_color"]["normal"], text="Failed")
        elif self.download_state == "waiting":
            self.status_label.configure(text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"], text="Waiting")
        elif self.download_state == "paused":
            self.status_label.configure(text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"], text="Paused")
        elif self.download_state == "downloading":
            self.status_label.configure(text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"], text="Downloading")
        elif self.download_state == "pausing":
            self.status_label.configure(text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"], text="Pausing")
        elif self.download_state == "completed":
            self.status_label.configure(text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"], text="Downloaded")

    def download_video(self):
        if not os.path.exists(self.download_directory):
            try:
                create_download_directory(self.download_directory)
            except Exception as error:
                print("@2 : ", error)
                self.set_download_failed()
                return

        stream = None
        self.bytes_downloaded = 0
        self.download_file_name = (
                f"{self.download_directory}\\" + f"{get_valid_file_name(f"{self.channel} - {self.video_title}")}"
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
            self.converted_file_size = get_converted_size(self.file_size, 2)
            self.download_file_name = get_available_file_name(self.download_file_name)
            self.set_download_progress()
        except Exception as error:
            print("@1 : ", error)
            self.set_download_failed()

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
                                text=get_converted_size(
                                    ((self.bytes_downloaded + len(chunk)) - self.bytes_downloaded) / (time_e - time_s),
                                    1
                                ) + "/s"
                            )
                            self.bytes_downloaded += len(chunk)
                            self.set_download_progress()
                        else:
                            if self.bytes_downloaded == self.file_size:
                                self.set_download_completed()
                                break
                            else:
                                self.set_download_failed()
                                break
                    except Exception as error:
                        print("@3 DownloadingPlayList.py : ", error)
                        self.set_download_failed()
                        break
        except Exception as error:
            print("@4 DownloadingPlayList.py : ", error)
            self.set_download_failed()

    def set_resume_btn(self):
        self.pause_resume_btn.configure(text="▷")

    def set_pause_btn(self):
        self.pause_resume_btn.configure(text="⏸")

    def pause_downloading(self):
        self.pause_resume_btn.configure(command=pass_command)
        self.download_state = "pausing"
        self.display_status()
        self.pause_requested = True

    def resume_downloading(self):
        self.pause_requested = False
        self.set_pause_btn()
        while self.download_state == "paused":
            time.sleep(0.3)
        self.pause_resume_btn.configure(command=self.pause_downloading)
        self.download_state = "downloading"
        if self.mode == "playlist":
            self.video_download_status_callback(self, self.download_state)
        self.display_status()

    def set_download_progress(self):
        completed_percentage = self.bytes_downloaded / self.file_size
        self.download_progress_bar.set(completed_percentage)
        self.download_percentage_label.configure(text=f"{round(completed_percentage * 100, 2)} %")
        self.download_progress_label.configure(
            text=f"{get_converted_size(self.bytes_downloaded, 2)} / {self.converted_file_size}"
        )
        if self.mode == "playlist":
            self.video_download_progress_callback()

    def set_download_failed(self):
        print(self.download_state)
        if self.download_state != "removed":
            self.download_state = "failed"
            self.display_status()
            if self.mode == "playlist":
                self.video_download_status_callback(self, self.download_state)
            if self in DownloadManager.active_downloads:
                DownloadManager.active_downloads.remove(self)
                DownloadManager.active_download_count -= 1
            self.pause_resume_btn.place_forget()
            self.re_download_btn.place(y=22, relx=1, x=-80)

    def set_waiting(self):
        DownloadManager.queued_downloads.append(self)
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

    def set_download_completed(self):
        if self in DownloadManager.active_downloads:
            DownloadManager.active_downloads.remove(self)
            DownloadManager.active_download_count -= 1
        self.pause_resume_btn.place_forget()
        self.download_state = "completed"
        self.display_status()
        if self.mode == "playlist":
            self.video_download_status_callback(self, self.download_state)
        if self.mode == "video":
            self.video_download_complete_callback(self)
            self.kill()

    def kill(self):
        if self in DownloadManager.queued_downloads:
            DownloadManager.queued_downloads.remove(self)
        if self in DownloadManager.active_downloads:
            DownloadManager.active_downloads.remove(self)
            DownloadManager.active_download_count -= 1
        self.download_state = "removed"
        if self.mode == "playlist":
            self.video_download_status_callback(self, self.download_state)
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

        self.download_progress_label = ctk.CTkLabel(
            master=self.sub_frame,
            text="",
            font=("arial", 12, "bold"),
        )

        self.download_percentage_label = ctk.CTkLabel(
            master=self.sub_frame,
            text="",
            font=("arial", 12, "bold"),
        )

        self.download_type_label = ctk.CTkLabel(
            master=self.sub_frame,
            text="",
            font=("arial", 12, "normal"),
        )

        self.net_speed_label = ctk.CTkLabel(
            master=self.sub_frame,
            text="",
            font=("arial", 12, "normal"),
        )

        self.status_label = ctk.CTkLabel(
            master=self.sub_frame,
            text="",
            font=("arial", 12, "bold"),
        )

        self.re_download_btn = ctk.CTkButton(
            master=self,
            text="⟳",
            width=15,
            height=15,
            font=("arial", 20, "normal"),
            command=self.re_download_video,
            hover=False
        )

        self.pause_resume_btn = ctk.CTkButton(
            master=self,
            text="⏸",
            width=15,
            height=15,
            font=("arial", 20, "normal"),
            command=self.pause_downloading,
            hover=False
        )

    # configure widgets colors
    def on_mouse_enter_self(self, event):
        super().on_mouse_enter_self(event)
        self.sub_frame.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])
        self.re_download_btn.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])
        self.pause_resume_btn.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"])

    def on_mouse_leave_self(self, event):
        super().on_mouse_leave_self(event)
        self.sub_frame.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])
        self.re_download_btn.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])
        self.pause_resume_btn.configure(fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"])

    def set_accent_color(self):
        super().set_accent_color()
        self.download_progress_bar.configure(
            progress_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
        )
        self.re_download_btn.configure(
            text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
        )
        self.pause_resume_btn.configure(
            text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
        )

    def set_widgets_colors(self) -> None:
        super().set_widgets_colors()
        self.sub_frame.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"],
        )
        self.download_progress_label.configure(
            text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"]
        )
        self.download_percentage_label.configure(
            text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"]
        )
        self.download_type_label.configure(
            text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"]
        )
        self.net_speed_label.configure(
            text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"]
        )
        self.status_label.configure(
            text_color=ThemeManager.theme_settings["video_object"]["text_color"]["normal"]
        )
        self.re_download_btn.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]
        )
        self.pause_resume_btn.configure(
            fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"]
        )

    def bind_widget_events(self):
        super().bind_widget_events()

        def on_mouse_enter_re_download_btn(event):
            self.re_download_btn.configure(
                fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"],
                text_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"]
            )
            self.on_mouse_enter_self(event)

        def on_mouse_leave_download_btn(_event):
            self.re_download_btn.configure(
                fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"],
                text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
            )

        self.re_download_btn.bind("<Enter>", on_mouse_enter_re_download_btn)
        self.re_download_btn.bind("<Leave>", on_mouse_leave_download_btn)

        def on_mouse_enter_pause_resume_btn(event):
            self.pause_resume_btn.configure(
                fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["hover"],
                text_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"]
            )
            self.on_mouse_enter_self(event)

        def on_mouse_leave_pause_resume_btn(_event):
            self.pause_resume_btn.configure(
                fg_color=ThemeManager.theme_settings["video_object"]["fg_color"]["normal"],
                text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
            )

        self.pause_resume_btn.bind("<Enter>", on_mouse_enter_pause_resume_btn)
        self.pause_resume_btn.bind("<Leave>", on_mouse_leave_pause_resume_btn)

    # place widgets
    def place_widgets(self):
        self.remove_btn.place(relx=1, x=-24, y=4)
        self.thumbnail_btn.place(x=5, y=2, relheight=1, height=-4, width=int((self.height - 4) / 9 * 16))
        self.video_title_label.place(x=130, y=4, height=20, relwidth=0.5, width=-150)
        self.channel_btn.place(x=130, y=24, height=20, relwidth=0.5, width=-150)
        self.url_label.place(x=130, y=44, height=20, relwidth=0.5, width=-150)
        self.len_label.place(rely=1, y=-10, x=117, anchor="e")
        self.sub_frame.place(relx=0.5, y=2)
        self.download_progress_label.place(relx=0.25, anchor="n", y=4)
        self.download_progress_label.configure(height=20)
        self.download_percentage_label.place(relx=0.115, anchor="n", y=40)
        self.download_percentage_label.configure(height=20)
        self.download_progress_bar.place(relwidth=1, y=30)
        self.download_type_label.place(relx=0.75, anchor="n", y=4)
        self.download_type_label.configure(height=20)
        self.net_speed_label.place(relx=0.445, anchor="n", y=40)
        self.net_speed_label.configure(height=20)
        self.status_label.place(relx=0.775, anchor="n", y=40)
        self.status_label.configure(height=20)

    # configure widgets sizes and place location depend on root width
    def configure_widget_sizes(self, e):
        self.sub_frame.configure(width=self.master.winfo_width() / 2 - 100)
