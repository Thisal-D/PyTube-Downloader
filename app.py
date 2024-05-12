import os
import customtkinter as ctk
import threading
import time
from typing import Literal
import pyautogui
from widgets import (
    AddedVideo, DownloadingVideo, DownloadedVideo,
    AddedPlayList, DownloadingPlayList, DownloadedPlayList,
    SettingPanel, TrayMenu, AlertWindow
)
from widgets.core_widgets.context_menu import ContextMenu
from services import (
    ThemeManager, DownloadManager, LoadManager
)
from settings import (
    AppearanceSettings,
    GeneralSettings,
)
from utils import (
    FileUtility
)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # root width height
        self.root_width = self.winfo_width()
        self.root_height = self.winfo_height()

        # widgets size resetting check
        self.is_geometry_changes_tracker_running = False

        # download method
        self.selected_download_mode = "video"

        # check if any video added or downloading or downloaded
        self.is_content_downloading = False
        self.is_content_downloaded = False
        self.is_content_added = False

        self.added_video_count = 0
        self.downloading_video_count = 0
        self.downloaded_video_count = 0

        # widgets
        self.url_entry = None
        self.add_url_btn = None

        self.video_radio_btn = None
        self.playlist_radio_btn = None

        self.navigate_added_frame_btn = None
        self.navigate_downloading_frame_btn = None
        self.navigate_downloaded_frame_btn = None

        self.added_content_scroll_frame = None
        self.downloading_content_scroll_frame = None
        self.downloaded_content_scroll_frame = None

        self.added_frame_info_label = None
        self.downloading_frame_info_label = None
        self.downloaded_frame_info_label = None

        self.added_frame_info_label_placed = False
        self.downloading_frame_info_label_placed = False
        self.downloaded_frame_info_label_placed = False

        self.videos_status_count_label = None

        self.context_menu = None
        self.settings_panel = None
        self.settings_btn = None

        self.logo_frame = None
        self.logo_label = None

        self.tray_menu = None

    def create_widgets(self):
        self.url_entry = ctk.CTkEntry(master=self, placeholder_text="Enter Youtube URL")

        self.video_radio_btn = ctk.CTkRadioButton(
            master=self, text="Video",
            height=18,
            command=lambda: self.select_download_mode("video")
        )
        self.video_radio_btn.select()

        self.playlist_radio_btn = ctk.CTkRadioButton(
            master=self,
            text="Playlist",
            command=lambda: self.select_download_mode("playlist")
        )

        self.add_url_btn = ctk.CTkButton(
            master=self,
            text="Add +",
            border_width=2,
            command=self.add_video_playlist
        )

        self.added_content_scroll_frame = ctk.CTkScrollableFrame(master=self)
        self.downloading_content_scroll_frame = ctk.CTkScrollableFrame(master=self)
        self.downloaded_content_scroll_frame = ctk.CTkScrollableFrame(master=self)

        self.settings_btn = ctk.CTkButton(master=self, text="Setting")

        self.navigate_added_frame_btn = ctk.CTkButton(
            master=self,
            text="Added",
            command=lambda: self.place_frame(self.added_content_scroll_frame, "added")
        )

        self.navigate_downloading_frame_btn = ctk.CTkButton(
            master=self,
            text="Downloading",
            command=lambda: self.place_frame(self.downloading_content_scroll_frame, "downloading")
        )

        self.navigate_downloaded_frame_btn = ctk.CTkButton(
            master=self,
            text="Downloaded",
            command=lambda: self.place_frame(self.downloaded_content_scroll_frame, "downloaded")
        )

        self.added_frame_info_label = ctk.CTkLabel(
            master=self,
            text="Added videos & playlists will be display here.",
        )

        self.downloading_frame_info_label = ctk.CTkLabel(
            master=self,
            text="Downloading videos & playlists will be display here.",
        )

        self.downloaded_frame_info_label = ctk.CTkLabel(
            master=self,
            text="Downloaded videos & playlists will be display here.",
        )

        self.videos_status_count_label = ctk.CTkLabel(
            text="Loading : 0 | Downloading : 0",
            master=self
        )

        self.settings_panel = SettingPanel(
            master=self,
            theme_settings_change_callback=self.update_theme_settings,
            general_settings_change_callback=self.update_general_settings,
            restart_callback=self.restart
        )

        self.settings_btn = ctk.CTkButton(
            master=self,
            text="⚡",
            border_spacing=0,
            hover=False,
            command=self.open_settings
        )

        self.context_menu = ContextMenu(
            master=self,
            options_texts=["Select All", "Cut", "Copy", "Paste"],
            options_commands=[self.select_all_url, self.cut_url, self.copy_url, self.paste_url]
        )

        self.logo_frame = ctk.CTkFrame(master=self)
        self.logo_label = ctk.CTkLabel(master=self.logo_frame, text="⚡")

    def select_all_url(self):
        self.url_entry.focus()
        pyautogui.hotkey("ctrl", "a")
        self.context_menu.place_forget()

    def cut_url(self):
        self.url_entry.focus()
        pyautogui.hotkey("ctrl", "x")
        self.context_menu.place_forget()

    def copy_url(self):
        self.url_entry.focus()
        pyautogui.hotkey("ctrl", "c")
        self.context_menu.place_forget()

    def paste_url(self):
        self.url_entry.focus()
        pyautogui.hotkey("ctrl", "v")
        self.context_menu.place_forget()

    def place_forget_nav_frames(self):
        self.added_content_scroll_frame.place_forget()
        self.downloading_content_scroll_frame.place_forget()
        self.downloaded_content_scroll_frame.place_forget()

    def place_forget_nav_labels(self):
        self.added_frame_info_label_placed = False
        self.downloading_frame_info_label_placed = False
        self.downloaded_frame_info_label_placed = False
        self.added_frame_info_label.place_forget()
        self.downloading_frame_info_label.place_forget()
        self.downloaded_frame_info_label.place_forget()

    def place_nav_label(self, frame_name: str):
        self.place_forget_nav_labels()
        if frame_name == "added" and self.is_content_added is not True:
            self.added_frame_info_label_placed = True
            self.added_frame_info_label.place(y=self.winfo_height() / 2 + 45, x=self.winfo_width() / 2, anchor="center")
        elif frame_name == "downloading" and self.is_content_downloading is not True:
            self.downloading_frame_info_label_placed = True
            self.downloading_frame_info_label.place(
                y=self.winfo_height() / 2 + 45,
                x=self.winfo_width() / 2,
                anchor="center"
            )
        elif frame_name == "downloaded" and self.is_content_downloaded is not True:
            self.downloaded_frame_info_label_placed = True
            self.downloaded_frame_info_label.place(
                y=self.winfo_height() / 2 + 45,
                x=self.winfo_width() / 2,
                anchor="center"
            )

    def place_frame(self, frame: ctk.CTkScrollableFrame, frame_name: str):
        self.place_forget_nav_frames()
        frame.place(y=90 * AppearanceSettings.settings["scale_r"], x=10)
        self.place_nav_label(frame_name)

    def place_widgets(self):
        scale = AppearanceSettings.settings["scale_r"]
        self.settings_btn.place(x=-5, y=4)
        self.url_entry.place(x=43 * scale, y=4)
        self.add_url_btn.place(y=4)
        self.video_radio_btn.place(y=5)
        self.playlist_radio_btn.place(y=25 * scale)
        self.navigate_added_frame_btn.place(y=50 * scale, x=10)
        self.navigate_downloading_frame_btn.place(y=50 * scale)
        self.navigate_downloaded_frame_btn.place(y=50 * scale)
        self.place_frame(self.added_content_scroll_frame, "added")
        self.videos_status_count_label.place(x=10, rely=1, y=-20 * scale)
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")

    def set_widgets_fonts(self):
        scale = AppearanceSettings.settings["scale_r"]
        self.url_entry.configure(
            font=ctk.CTkFont(
                family="Segoe UI",
                size=int(16 * scale),
                weight="normal",
                slant="italic",
                underline=True
            )
        )

        self.video_radio_btn.configure(font=("Segoe UI", 12 * scale, "bold"))
        self.playlist_radio_btn.configure(font=("Segoe UI", 12 * scale, "bold"))
        self.add_url_btn.configure(font=("Segoe UI", 15 * scale, "bold"))

        font_style_1 = ctk.CTkFont(
            family="Comic Sans MS",
            size=int(16 * scale),
            weight="bold",
            slant="italic"
        )
        self.added_frame_info_label.configure(font=font_style_1)
        self.downloading_frame_info_label.configure(font=font_style_1)
        self.downloaded_frame_info_label.configure(font=font_style_1)

        font_style_2 = ("Segoe UI", 15 * scale, "bold")
        self.navigate_added_frame_btn.configure(font=font_style_2)
        self.navigate_downloading_frame_btn.configure(font=font_style_2)
        self.navigate_downloaded_frame_btn.configure(font=font_style_2)
        self.settings_btn.configure(font=("arial", 25 * scale, "normal"))
        self.context_menu.configure(font=("Segoe UI", 13 * scale, "bold"))
        self.videos_status_count_label.configure(font=("Segoe UI", 11 * scale, "normal"))
        self.logo_label.configure(font=("arial", 50 * scale, "normal"))

    def set_widgets_sizes(self):
        scale = AppearanceSettings.settings["scale_r"]
        self.url_entry.configure(height=int(40 * scale))
        self.video_radio_btn.configure(
            radiobutton_width=int(16 * scale),
            radiobutton_height=int(16 * scale),
            width=int(60 * scale),
            height=int(18 * scale)
        )
        self.playlist_radio_btn.configure(
            radiobutton_width=int(16 * scale),
            radiobutton_height=int(16 * scale),
            width=int(60 * scale),
            height=int(18 * scale)
        )
        self.add_url_btn.configure(height=int(40 * scale), width=int(100 * scale))
        self.navigate_added_frame_btn.configure(height=int(40 * scale))
        self.navigate_downloading_frame_btn.configure(height=int(40 * scale))
        self.navigate_downloaded_frame_btn.configure(height=int(40 * scale))
        self.settings_btn.configure(width=int(30 * scale), height=int(40 * scale))
        self.context_menu.configure(
            width=int(100 * AppearanceSettings.settings["scale_r"]),
            height=int(120 * AppearanceSettings.settings["scale_r"])
        )
        self.videos_status_count_label.configure(height=int(15 * scale))

    def configure_widgets_size(self):
        scale = AppearanceSettings.settings["scale_r"]
        root_width = self.winfo_width()
        root_height = self.winfo_height()
        self.url_entry.configure(width=root_width - 250 * scale)

        button_margin = int(3 * scale)
        nav_button_width = int((root_width - 20 - button_margin * 3) / 3)
        self.navigate_added_frame_btn.configure(width=nav_button_width)
        self.navigate_downloading_frame_btn.configure(width=nav_button_width)
        self.navigate_downloaded_frame_btn.configure(width=nav_button_width)

        self.navigate_downloading_frame_btn.place(x=nav_button_width + 10 + button_margin)
        self.navigate_downloaded_frame_btn.place(x=nav_button_width * 2 + 10 + button_margin * 2)

        self.video_radio_btn.place(x=root_width - 190 * scale)
        self.playlist_radio_btn.place(x=root_width - 190 * scale)
        self.add_url_btn.place(x=root_width - 110 * scale)

        if self.added_frame_info_label_placed:
            self.place_nav_label("added")
        elif self.downloading_frame_info_label_placed:
            self.place_nav_label("downloading")
        elif self.downloaded_frame_info_label_placed:
            self.place_nav_label("downloaded")

        frame_height = root_height - (100 + 15) * scale
        frame_width = root_width - 40
        self.added_content_scroll_frame.configure(height=frame_height, width=frame_width)
        self.downloading_content_scroll_frame.configure(height=frame_height, width=frame_width)
        self.downloaded_content_scroll_frame.configure(height=frame_height, width=frame_width)

    def set_widgets_accent_color(self):
        self.settings_btn.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.video_radio_btn.configure(
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.playlist_radio_btn.configure(
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.add_url_btn.configure(
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.navigate_added_frame_btn.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.navigate_downloading_frame_btn.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.navigate_downloaded_frame_btn.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.added_frame_info_label.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.downloading_frame_info_label.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.downloaded_frame_info_label.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.logo_label.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )

    def set_widgets_colors(self):
        self.configure(fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"])

        self.settings_btn.configure(
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            hover=False
        )

        self.url_entry.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["url_entry"]["fg_color"]["normal"],
            border_color=AppearanceSettings.settings["url_entry"]["border_color"]["normal"],
            text_color=AppearanceSettings.settings["url_entry"]["text_color"]["normal"]
        )

        self.video_radio_btn.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            text_color=AppearanceSettings.settings["url_entry"]["text_color"]["normal"]
        )
        self.playlist_radio_btn.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            text_color=AppearanceSettings.settings["url_entry"]["text_color"]["normal"]
        )

        self.add_url_btn.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["url_adding_button"]["fg_color"]["normal"],
            hover=False
        )

        self.navigate_added_frame_btn.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"],
            hover=False
        )
        self.navigate_downloading_frame_btn.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"],
            hover=False
        )
        self.navigate_downloaded_frame_btn.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"],
            hover=False
        )

        self.added_content_scroll_frame.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["navigation_frame"]["fg_color"]["normal"]
        )
        self.downloading_content_scroll_frame.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["navigation_frame"]["fg_color"]["normal"]
        )
        self.downloaded_content_scroll_frame.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["navigation_frame"]["fg_color"]["normal"]
        )
        self.added_frame_info_label.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )
        self.downloading_frame_info_label.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.downloaded_frame_info_label.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.videos_status_count_label.configure(
            text_color=AppearanceSettings.settings["root"]["text_color"]["normal"]
        )
        self.logo_frame.configure(
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )

    def bind_widgets_events(self):
        self.url_entry.bind("<Button-3>", self.open_context_menu)
        self.url_entry.bind("<Button-2>", self.open_context_menu)
        self.bind("<Button-2>", self.close_context_menu)
        self.bind("<Button-3>", self.close_context_menu)

        self.url_entry.bind("<Button-1>", self.close_context_menu_directly)
        self.bind("<Button-1>", self.close_context_menu_directly)
        self.bind('<FocusOut>', self.close_context_menu_directly)
        self.bind("<Configure>", self.run_geometry_changes_tracker)

        def on_mouse_enter_url_entry(_event):
            self.url_entry.configure(
                fg_color=AppearanceSettings.settings["url_entry"]["fg_color"]["hover"],
                border_color=AppearanceSettings.settings["url_entry"]["border_color"]["hover"],
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["hover"]
            )

        def on_mouse_leave_url_entry(_event):
            self.url_entry.configure(
                fg_color=AppearanceSettings.settings["url_entry"]["fg_color"]["normal"],
                border_color=AppearanceSettings.settings["url_entry"]["border_color"]["normal"],
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["normal"]
            )

        self.url_entry.bind("<Enter>", on_mouse_enter_url_entry)
        self.url_entry.bind("<Leave>", on_mouse_leave_url_entry)

        ######################################################################################

        def on_mouse_enter_settings_btn(_event):
            self.settings_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"])

        def on_mouse_leave_settings_btn(_event):
            self.settings_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

        self.settings_btn.bind("<Enter>", on_mouse_enter_settings_btn)
        self.settings_btn.bind("<Leave>", on_mouse_leave_settings_btn)

        ######################################################################################

        def on_mouse_enter_video_radio_btn(_event):
            self.video_radio_btn.configure(
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["hover"],
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def on_mouse_leave_video_radio_btn(_event):
            self.video_radio_btn.configure(
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["normal"],
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.video_radio_btn.bind("<Enter>", on_mouse_enter_video_radio_btn)
        self.video_radio_btn.bind("<Leave>", on_mouse_leave_video_radio_btn)

        ######################################################################################

        def on_mouse_enter_playlist_radio_btn(_event):
            self.playlist_radio_btn.configure(
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["hover"],
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def on_mouse_leave_playlist_radio_btn(_event):
            self.playlist_radio_btn.configure(
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["normal"],
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.playlist_radio_btn.bind("<Enter>", on_mouse_enter_playlist_radio_btn)
        self.playlist_radio_btn.bind("<Leave>", on_mouse_leave_playlist_radio_btn)

        ######################################################################################

        def on_mouse_enter_add_video_playlist_btn(_event):
            self.add_url_btn.configure(
                border_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                fg_color=AppearanceSettings.settings["url_adding_button"]["fg_color"]["hover"]
            )

        def on_mouse_leave_add_video_playlist_btn(_event):
            self.add_url_btn.configure(
                border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                fg_color=AppearanceSettings.settings["url_adding_button"]["fg_color"]["normal"]
            )

        self.add_url_btn.bind("<Enter>", on_mouse_enter_add_video_playlist_btn)
        self.add_url_btn.bind("<Leave>", on_mouse_leave_add_video_playlist_btn)

        ######################################################################################

        def on_mouse_enter_navigate_added_frame_btn(_event):
            self.navigate_added_frame_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["hover"]
            )

        def on_mouse_leave_navigate_added_frame_btn(_event):
            self.navigate_added_frame_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"]
            )

        self.navigate_added_frame_btn.bind("<Enter>", on_mouse_enter_navigate_added_frame_btn)
        self.navigate_added_frame_btn.bind("<Leave>", on_mouse_leave_navigate_added_frame_btn)

        ######################################################################################

        def on_mouse_enter_navigate_downloading_frame_btn(_event):
            self.navigate_downloading_frame_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["hover"]
            )

        def on_mouse_leave_navigate_downloading_frame_btn(_event):
            self.navigate_downloading_frame_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"]
            )

        self.navigate_downloading_frame_btn.bind("<Enter>", on_mouse_enter_navigate_downloading_frame_btn)
        self.navigate_downloading_frame_btn.bind("<Leave>", on_mouse_leave_navigate_downloading_frame_btn)

        ######################################################################################

        def on_mouse_enter_navigate_downloaded_frame_btn(_event):
            self.navigate_downloaded_frame_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["hover"]
            )

        def on_mouse_leave_navigate_downloaded_frame_btn(_event):
            self.navigate_downloaded_frame_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"]
            )

        self.navigate_downloaded_frame_btn.bind("<Enter>", on_mouse_enter_navigate_downloaded_frame_btn)
        self.navigate_downloaded_frame_btn.bind("<Leave>", on_mouse_leave_navigate_downloaded_frame_btn)

        #######################################################################################

        def on_mouse_enter_added_frame_info_label(_event):
            self.added_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def on_mouse_leave_added_frame_info_label(_event):
            self.added_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.added_frame_info_label.bind("<Enter>", on_mouse_enter_added_frame_info_label)
        self.added_frame_info_label.bind("<Leave>", on_mouse_leave_added_frame_info_label)

        #######################################################################################

        def on_mouse_enter_downloading_frame_info_label(_event):
            self.downloading_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def on_mouse_leave_downloading_frame_info_label(_event):
            self.downloading_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.downloading_frame_info_label.bind("<Enter>", on_mouse_enter_downloading_frame_info_label)
        self.downloading_frame_info_label.bind("<Leave>", on_mouse_leave_downloading_frame_info_label)

        #######################################################################################
        def on_mouse_enter_downloaded_frame_info_label(_event):
            self.downloaded_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def mouse_ot_downloaded_frame_info_label(_event):
            self.downloaded_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.downloaded_frame_info_label.bind("<Enter>", on_mouse_enter_downloaded_frame_info_label)
        self.downloaded_frame_info_label.bind("<Leave>", mouse_ot_downloaded_frame_info_label)

    def show_app_logo(self):
        self.logo_frame.place(relwidth=1, relheight=1)

    def hide_app_logo(self):
        self.logo_frame.place_forget()

    def geometry_changes_tracker(self):
        self.is_geometry_changes_tracker_running = True
        update_delay = 1
        # if old window width or height not same to current width or height that meas window size changed
        if self.root_width != self.winfo_width() or self.root_height != self.winfo_height():
            # if window size changed, show the logo on full screen
            self.show_app_logo()
            self.root_width = self.winfo_width()
            self.root_height = self.winfo_height()
            time.sleep(update_delay)
            # wait till user stop window size changing
            while self.root_width != self.winfo_width() or self.root_height != self.winfo_height():
                # keep update old window size to track i fuser change windows size or not
                self.root_width = self.winfo_width()
                self.root_height = self.winfo_height()
                # set delay to 1 sec
                time.sleep(update_delay)
            # after user stop changing windows size check if window size changed or not
            self.configure_widgets_size()
            self.update()
            self.update_idletasks()
            self.hide_app_logo()
        self.is_geometry_changes_tracker_running = False

    def run_geometry_changes_tracker(self, _event):
        if not self.is_geometry_changes_tracker_running:
            threading.Thread(target=self.geometry_changes_tracker).start()

    def select_download_mode(self, download_mode):
        self.selected_download_mode = download_mode
        if download_mode == "playlist":
            self.video_radio_btn.deselect()
        else:
            self.playlist_radio_btn.deselect()

    def update_videos_count_status(self):
        print(DownloadManager.queued_download_count, DownloadManager.active_download_count)
        self.videos_status_count_label.configure(
            text=f"Loading : {LoadManager.queued_load_count + LoadManager.active_load_count} | "
                 f"Downloading : {DownloadManager.queued_download_count + DownloadManager.active_download_count}"
        )

    def add_video_playlist(self):
        self.is_content_added = True
        self.added_frame_info_label.place_forget()
        yt_url = self.url_entry.get()
        if self.selected_download_mode == "video":
            AddedVideo(
                root=self,
                master=self.added_content_scroll_frame,
                height=int(70 * AppearanceSettings.settings["scale_r"]),
                width=self.added_content_scroll_frame.winfo_width(),
                # video url
                video_url=yt_url,
                # download btn callback
                video_download_button_click_callback=self.download_video,
            ).pack(fill="x", pady=2)

        else:
            AddedPlayList(
                root=self,
                master=self.added_content_scroll_frame,
                height=int(86 * AppearanceSettings.settings["scale_r"]),
                width=self.added_content_scroll_frame.winfo_width(),

                playlist_download_button_click_callback=self.download_playlist,
                video_download_button_click_callback=self.download_video,
                playlist_url=yt_url
            ).pack(fill="x", pady=2)

    def download_video(self, video: AddedVideo):
        self.is_content_downloading = True
        self.downloading_frame_info_label.place_forget()
        DownloadingVideo(
            root=self,
            master=self.downloading_content_scroll_frame,
            height=int(70 * AppearanceSettings.settings["scale_r"]),
            width=self.downloading_content_scroll_frame.winfo_width(),
            # video info
            channel_url=video.channel_url,
            video_url=video.video_url,
            channel=video.channel,
            video_title=video.video_title,
            video_stream_data=video.video_stream_data,
            length=video.length,
            thumbnails=video.thumbnails,
            # download info
            download_quality=video.download_quality,
            download_type=video.download_type,
            video_download_complete_callback=self.downloaded_video,
        ).pack(fill="x", pady=2)

    def download_playlist(self, playlist: AddedPlayList):
        self.is_content_downloading = True
        self.downloading_frame_info_label.place_forget()
        DownloadingPlayList(
            root=self,
            master=self.downloading_content_scroll_frame,
            height=int(86 * AppearanceSettings.settings["scale_r"]),
            width=self.downloading_content_scroll_frame.winfo_width(),
            # video info
            channel_url=playlist.channel_url,
            channel=playlist.channel,
            playlist_title=playlist.playlist_title,
            playlist_video_count=playlist.playlist_video_count,
            playlist_url=playlist.playlist_url,
            # play list videos
            videos=playlist.videos,
            # download directory
            # playlist download completed callback utils
            playlist_download_complete_callback=self.downloaded_playlist,
        ).pack(fill="x", pady=2)

    def downloaded_video(self, video: DownloadingVideo):
        self.is_content_downloaded = True
        self.downloaded_frame_info_label.place_forget()
        DownloadedVideo(
            root=self,
            master=self.downloaded_content_scroll_frame,
            height=int(70 * AppearanceSettings.settings["scale_r"]),
            width=self.downloaded_content_scroll_frame.winfo_width(),

            thumbnails=video.thumbnails,
            video_title=video.video_title,
            channel=video.channel,
            channel_url=video.channel_url,
            video_url=video.video_url,
            file_size=video.file_size,
            length=video.length,

            download_path=video.download_file_name,
            download_quality=video.download_quality,
            download_type=video.download_type
        ).pack(fill="x", pady=2)

    def downloaded_playlist(self, playlist: DownloadingPlayList):
        self.is_content_downloaded = True
        self.downloaded_frame_info_label.place_forget()
        DownloadedPlayList(
            root=self,
            master=self.downloaded_content_scroll_frame,
            height=86 * AppearanceSettings.settings["scale_r"],
            width=self.downloaded_content_scroll_frame.winfo_width(),
            # playlist url
            channel_url=playlist.channel_url,
            channel=playlist.channel,
            playlist_title=playlist.playlist_title,
            playlist_video_count=playlist.playlist_video_count,
            playlist_url=playlist.playlist_url,
            videos=playlist.videos
        ).pack(fill="x", pady=2)

    def open_context_menu(self, _event):
        pointer_x = self.winfo_pointerx() - self.winfo_rootx()
        pointer_y = self.winfo_pointery() - self.winfo_rooty()

        self.context_menu.place(x=pointer_x, y=pointer_y)

    def close_context_menu(self, _event):
        pointer_x = self.winfo_pointerx() - self.winfo_rootx()
        pointer_y = self.winfo_pointery() - self.winfo_rooty()

        if (pointer_x < self.url_entry.winfo_x() or pointer_y < self.url_entry.winfo_y() or
                pointer_x > (self.url_entry.winfo_x() + self.url_entry.winfo_width()) or
                pointer_y > (self.url_entry.winfo_y() + self.url_entry.winfo_height())):
            self.context_menu.place_forget()

    def close_context_menu_directly(self, _event):
        self.context_menu.place_forget()

    def update_theme_settings(
            self,
            updated: Literal["accent_color", "theme_mode", "opacity"] = None):
        if updated == "accent_color":
            self.set_widgets_accent_color()
            ThemeManager.update_accent_color()
        if updated == "theme_mode":
            ctk.set_appearance_mode(AppearanceSettings.settings["root"]["theme_mode"])
        if updated == "opacity":
            self.attributes("-alpha", AppearanceSettings.settings["opacity_r"])
        AppearanceSettings.save_settings()

    def open_settings(self):
        ContextMenu.close_all_menus()
        self.settings_panel.place(relwidth=1, relheight=1)
        self.settings_btn.configure(command=self.close_settings)

    def close_settings(self):
        self.settings_panel.place_forget()
        self.settings_btn.configure(command=self.open_settings)

    def on_app_closing(self, restart: bool = False):
        GeneralSettings.settings['window_geometry'] = self.geometry()
        GeneralSettings.save_settings()
        self.clear_temporally_saved_files()
        self.destroy()
        if not restart:
            os._exit(0)

    def cancel_app_closing(self):
        self.bind_widgets_events()

    def restart(self):
        self.on_app_closing(restart=True)
        if os.path.exists("main.py"):
            os.startfile("main.py")
        if os.path.exists("PyTube Downloader.exe"):
            os.startfile("PyTube Downloader.exe")
        os._exit(0)

    def show_close_confirmation_dialog(self):
        scale = AppearanceSettings.settings["scale_r"]
        self.restore_from_tray()
        AlertWindow(
            master=self,
            alert_msg="Are you sure you want to exit the application?",
            ok_button_text="ok",
            cancel_button_text="cancel",
            ok_button_callback=self.on_app_closing,
            cancel_button_callback=self.cancel_app_closing,
            callback=self.cancel_app_closing,
            width=int(450 * scale),
            height=int(130 * scale),
        )

    def restore_from_tray(self):
        self.tray_menu.stop()
        self.deiconify()

    def minimize_to_tray(self):
        self.iconify()
        self.tray_menu = TrayMenu(
            open_command=self.restore_from_tray,
            quit_command=self.show_close_confirmation_dialog,
        )
        self.withdraw()
        threading.Thread(target=self.tray_menu.run, daemon=True).start()

    def run(self):
        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.mainloop()

    @staticmethod
    def update_general_settings():
        GeneralSettings.save_settings()

    @classmethod
    def clear_temporally_saved_files(self):
        FileUtility.delete_files("temp\\thumbnails", ["this directory is necessary"])
