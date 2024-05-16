import tkinter as tk
from widgets.video import Video
import customtkinter as ctk
import pytube
import threading
from typing import Literal, Union, List, Callable, Tuple, Dict
from PIL import Image
import time
from services import (
    LoadManager,
    ThemeManager,
)
from settings import (
    AppearanceSettings,
    GeneralSettings,
)
from utils import (
    ImageUtility,
    DownloadInfoUtility,
    FileUtility
)


class AddedVideo(Video):
    def __init__(
            self,
            root: ctk.CTk,
            master: Union[ctk.CTkFrame, ctk.CTkScrollableFrame],
            width: int = 0,
            height: int = 0,
            # video url
            video_url: str = "",
            # callback functions for buttons
            video_download_button_click_callback: Callable = None,
            # state callbacks only use if mode is play list
            mode: Literal["video", "playlist"] = "video",
            video_load_status_callback: callable = None):

        # video info
        self.video_stream_data: pytube.YouTube.streams = None
        self.support_download_types: Union[List[Dict[str, int]], None] = None
        # download info
        self.download_quality: Literal["128kbps", "360p", "720p"] = "720p"
        self.download_type: Literal["Audio", "Video"] = "Video"
        # callback utils
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
        # Track automatically reload count
        self.automatically_reload_count: int = 0

        super().__init__(
            root=root,
            master=master,
            width=width,
            height=height,
            video_url=video_url
        )

        self.set_waiting()
        LoadManager.register(self)

    def reload_video(self):
        self.load_state = None
        self.reload_btn.place_forget()
        self.thumbnail_btn.configure(
            disabledforeground=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["text_color"]["normal"]
            )
        )
        self.set_waiting()
        LoadManager.register(self)

    def load_video(self):
        self.load_state = "loading"
        if self.mode == "playlist":
            self.video_load_status_callback(self, self.load_state)
        self.status_label.configure(text="Loading")
        threading.Thread(target=self.retrieve_video_data, daemon=True).start()

    def get_video_thumbnails(self) -> Tuple[tk.PhotoImage, tk.PhotoImage]:
        thumbnail_size = (
            int(117 * AppearanceSettings.settings["scale_r"]),
            int(66 * AppearanceSettings.settings["scale_r"])
        )
        thumbnail_save_directory = "temp/thumbnails/"
        thumbnail_url = self.video.thumbnail_url
        # Generate download path to thumbnail based on url
        file_name = FileUtility.sanitize_filename(thumbnail_url)
        thumbnail_download_path = FileUtility.get_available_file_name(
            thumbnail_save_directory + file_name + "-og.png"
        )
        ImageUtility.download_image(image_url=thumbnail_url, output_image_path=thumbnail_download_path)
        # Open downloaded thumbnail as Image
        thumbnail = Image.open(thumbnail_download_path)

        # getting downloaded thumbnail width and height
        image_height = thumbnail.height
        image_width = thumbnail.width

        if round(image_width / 4 * 3) <= image_height:
            is_thumbnail_need_to_crop = True
        else:
            is_thumbnail_need_to_crop = False

        if is_thumbnail_need_to_crop:
            ignore_pos = int(image_height * 0.25 / 2)
            start_pos = (0, ignore_pos)
            end_pos = (image_width, image_height - ignore_pos)
            thumbnail = ImageUtility.crop_image(image=thumbnail, start_position=start_pos, end_position=end_pos)

        thumbnail_hover = ImageUtility.create_image_with_hover_effect(image=thumbnail, intensity_increase=50)

        corner_radius = int(image_width / 18)
        thumbnail = ImageUtility.create_image_with_rounded_corners(thumbnail, radius=corner_radius)
        thumbnail_hover = ImageUtility.create_image_with_rounded_corners(thumbnail_hover, radius=corner_radius)

        thumbnail = ImageUtility.resize_image(image=thumbnail, new_size=thumbnail_size)
        thumbnail_hover = ImageUtility.resize_image(image=thumbnail_hover, new_size=thumbnail_size)

        thumbnail_normal_save_path = FileUtility.get_available_file_name(
            thumbnail_save_directory + file_name + "-normal-changed.png"
        )
        thumbnail_hover_save_path = FileUtility.get_available_file_name(
            thumbnail_save_directory + file_name + "-hover-changed.png"
        )
        thumbnail.save(thumbnail_normal_save_path)
        thumbnail_hover.save(thumbnail_hover_save_path)

        thumbnail_normal = tk.PhotoImage(file=thumbnail_normal_save_path)
        thumbnail_hover = tk.PhotoImage(file=thumbnail_hover_save_path)

        return thumbnail_normal, thumbnail_hover

    @classmethod
    def get_default_thumbnails(self):
        if AddedVideo.default_thumbnails == (None, None):
            thumbnail_size = (
                int(117 * AppearanceSettings.settings["scale_r"]),
                int(66 * AppearanceSettings.settings["scale_r"])
            )
            thumbnail_save_directory = "temp/thumbnails/"
            file_name = "default-thumbnail"
            thumbnail = Image.open("assets/ui images/default thumbnail.png")
            corner_radius = int(thumbnail.width / 18)
            thumbnail_hover = ImageUtility.create_image_with_hover_effect(thumbnail, intensity_increase=50)
            thumbnail = ImageUtility.create_image_with_rounded_corners(thumbnail, radius=corner_radius)
            thumbnail_hover = ImageUtility.create_image_with_rounded_corners(thumbnail_hover, radius=corner_radius)
            thumbnail = ImageUtility.resize_image(image=thumbnail, new_size=thumbnail_size)
            thumbnail_hover = ImageUtility.resize_image(image=thumbnail_hover, new_size=thumbnail_size)

            thumbnail_normal_save_path = FileUtility.get_available_file_name(
                thumbnail_save_directory + file_name + "-normal-changed.png"
            )
            thumbnail_hover_save_path = FileUtility.get_available_file_name(
                thumbnail_save_directory + file_name + "-hover-changed.png"
            )
            thumbnail.save(thumbnail_normal_save_path)
            thumbnail_hover.save(thumbnail_hover_save_path)

            thumbnail_normal = tk.PhotoImage(file=thumbnail_normal_save_path)
            thumbnail_hover = tk.PhotoImage(file=thumbnail_hover_save_path)

            AddedVideo.default_thumbnails = (thumbnail_normal, thumbnail_hover)

        return AddedVideo.default_thumbnails

    def retrieve_video_data(self):
        try:
            self.video = pytube.YouTube(self.video_url)
            self.video_title = str(self.video.title)
            self.channel = str(self.video.author)
            self.length = int(self.video.length)
            self.video_stream_data = self.video.streams
            self.channel_url = str(self.video.channel_url)
            if GeneralSettings.settings["load_thumbnail"]:
                self.thumbnails = self.get_video_thumbnails()
            else:
                self.thumbnails = self.get_default_thumbnails()
            self.support_download_types = (
                DownloadInfoUtility.sort_download_qualities(
                    DownloadInfoUtility.get_supported_download_types(self.video_stream_data)
                )
            )
            self.set_loading_completed()
            self.set_video_data()
            self.download_automatically()
        except Exception as error:
            print(f"added_video.py L-198 : {error}")
            self.set_loading_failed()

    def choose_download_type(self, e: str):
        self.download_quality = e.replace(" ", "").split("|")[0]
        if "kbps" in self.download_quality:
            self.download_type = "Audio"
        elif "p" in self.download_quality:
            self.download_type = "Video"

    def set_waiting(self):
        self.thumbnail_btn.run_loading_animation()
        self.status_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.load_state = "waiting"
        if self.mode == "playlist":
            self.video_load_status_callback(self, self.load_state)
        self.status_label.configure(text="Waiting")

    def select_download_quality_automatic(self):
        index = None
        if GeneralSettings.settings["automatic_download"]["quality"] == "Audio Only":
            index = -1
        elif GeneralSettings.settings["automatic_download"]["quality"] == "Lowest Quality":
            index = -2
        elif GeneralSettings.settings["automatic_download"]["quality"] == "Highest Quality":
            index = 0
        self.resolution_select_menu.set(self.resolution_select_menu.cget("values")[index])

    def download_automatically(self):
        if self.mode == "video" and GeneralSettings.settings["automatic_download"]["status"] == "enable":
            self.select_download_quality_automatic()
            self.choose_download_type(self.resolution_select_menu.get())
            self.video_download_button_click_callback(self)

    def set_loading_completed(self):
        if self.load_state != "removed":
            self.load_state = "completed"
            if self.mode == "playlist":
                self.video_load_status_callback(self, self.load_state)
            self.status_label.configure(text="Loaded")
            LoadManager.unregister_from_active(self)

    def set_loading_failed(self):
        if self.load_state == "removed":
            return
        
        if GeneralSettings.settings["reload_automatically"] and self.automatically_reload_count < 5:
            time.sleep(1)
            self.automatically_reload_count += 1
            self.load_video()
        else:
            LoadManager.unregister_from_active(self)
            self.load_state = "failed"
            if self.mode == "playlist":
                self.video_load_status_callback(self, self.load_state)
            self.thumbnail_btn.show_failure_indicator(
                text_color=AppearanceSettings.settings["video_object"]["error_color"]["normal"]
            )
            self.status_label.configure(
                text_color=AppearanceSettings.settings["video_object"]["error_color"]["normal"],
                text="Failed"
            )
            self.reload_btn.place(
                relx=1,
                rely=0.5,
                anchor="w",
                x=-80 * AppearanceSettings.settings["scale_r"]
                )

    def set_video_data(self):
        if self.load_state != "removed":
            super().set_video_data()

            self.resolution_select_menu.configure(
                values=DownloadInfoUtility.generate_download_options(self.support_download_types)
            )
            self.resolution_select_menu.set(self.resolution_select_menu.cget("values")[0])
            self.choose_download_type(self.resolution_select_menu.get())
            self.resolution_select_menu.configure(command=self.choose_download_type)
            self.channel_btn.configure(state="normal")
            self.download_btn.configure(state="normal")

    def kill(self):
        self.load_state = "removed"
        LoadManager.unregister_from_active(self)
        LoadManager.unregister_from_queued(self)
        if self.mode == "playlist":
            self.video_load_status_callback(self, self.load_state)
        super().kill()

    # create widgets
    def create_widgets(self):
        super().create_widgets()

        self.sub_frame = ctk.CTkFrame(master=self)
        self.resolution_select_menu = ctk.CTkComboBox(
            master=self.sub_frame,
            values=["..........", "..........", ".........."],
            width=150 * AppearanceSettings.settings["scale_r"],
            height=28 * AppearanceSettings.settings["scale_r"],
        )
        self.download_btn = ctk.CTkButton(
            master=self.sub_frame,
            text="Download",
            state="disabled",
            hover=False,
            command=lambda: self.video_download_button_click_callback(self),
        )
        self.status_label = ctk.CTkLabel(master=self.sub_frame, text="")
        self.reload_btn = ctk.CTkButton(master=self, text="⟳", command=self.reload_video, hover=False)

    def set_widgets_fonts(self):
        super().set_widgets_fonts()

        scale = AppearanceSettings.settings["scale_r"]

        self.resolution_select_menu.configure(
            font=("Segoe UI", 13 * scale, "normal"),
            dropdown_font=("Segoe UI", 13 * scale, "normal")
        )
        self.download_btn.configure(font=("arial", 12 * scale, "bold"))
        self.status_label.configure(font=("arial", 12 * scale, "bold"))
        self.reload_btn.configure(font=("arial", 20 * scale, "normal"))

    def set_widgets_sizes(self):
        super().set_widgets_sizes()

        scale = AppearanceSettings.settings["scale_r"]

        self.sub_frame.configure(height=self.height - 3, width=270 * scale)
        self.download_btn.configure(width=80 * scale, height=25 * scale, border_width=2)
        self.resolution_select_menu.configure(width=150 * scale, height=28 * scale)
        self.status_label.configure(height=15 * scale, width=80 * scale)
        self.reload_btn.configure(width=15 * scale, height=15 * scale)

    # configure widgets colors
    def set_widgets_accent_color(self):
        super().set_widgets_accent_color()

        self.download_btn.configure(border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        self.reload_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        self.resolution_select_menu.configure(
            button_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            button_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            dropdown_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )

    def set_widgets_colors(self):
        super().set_widgets_colors()

        self.reload_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.download_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["btn_fg_color"]["normal"],
            text_color=AppearanceSettings.settings["video_object"]["btn_text_color"]["normal"]
        )
        self.sub_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.status_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.resolution_select_menu.configure(
            dropdown_fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"],
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
        )

    def on_mouse_enter_self(self, event):
        super().on_mouse_enter_self(event)

        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])
        self.reload_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])

    def on_mouse_leave_self(self, event):
        super().on_mouse_leave_self(event)

        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.reload_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])

    def bind_widgets_events(self):
        super().bind_widgets_events()

        def on_mouse_enter_download_btn(event):
            self.on_mouse_enter_self(event)
            if self.download_btn.cget("state") == "normal":
                self.download_btn.configure(
                    fg_color=AppearanceSettings.settings["video_object"]["btn_fg_color"]["hover"],
                    text_color=AppearanceSettings.settings["video_object"]["btn_text_color"]["hover"],
                    border_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
                )

        def on_mouse_leave_download_btn(event):
            self.on_mouse_leave_self(event)
            if self.download_btn.cget("state") == "normal":
                self.download_btn.configure(
                    fg_color=AppearanceSettings.settings["video_object"]["btn_fg_color"]["normal"],
                    text_color=AppearanceSettings.settings["video_object"]["btn_text_color"]["normal"],
                    border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
                )

        self.download_btn.bind("<Enter>", on_mouse_enter_download_btn)
        self.download_btn.bind("<Leave>", on_mouse_leave_download_btn)

        def on_mouse_enter_reload_btn(event):
            self.on_mouse_enter_self(event)
            self.reload_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"], )

        def on_mouse_leave_reload_btn(event):
            self.on_mouse_leave_self(event)
            self.reload_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

        self.reload_btn.bind("<Enter>", on_mouse_enter_reload_btn)
        self.reload_btn.bind("<Leave>", on_mouse_leave_reload_btn)

    # place widgets
    def place_widgets(self):
        super().place_widgets()

        scale = AppearanceSettings.settings["scale_r"]

        self.sub_frame.place(y=1, relx=1, x=-370 * scale)

        self.resolution_select_menu.place(rely=0.5, anchor="w")
        self.download_btn.place(x=190 * scale, rely=0.3, anchor="w")
        self.status_label.place(x=190 * scale, rely=0.75, anchor="w")

    def configure_widget_sizes(self, _event):
        scale = AppearanceSettings.settings["scale_r"]
        self.info_frame.configure(
            width=(
                self.master.winfo_width() - (370 * scale) -
                (self.thumbnail_btn.winfo_width() + 5) - (10 * scale) -
                (20 * scale)
            )
        )
