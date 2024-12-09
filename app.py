import os
import customtkinter as ctk
import tkinter as tk
import threading
import time
import webbrowser
from typing import Literal
import pyautogui
from widgets import (
    AddedVideo, 
    DownloadingVideo, 
    DownloadedVideo,
    AddedPlayList, 
    DownloadingPlayList, 
    DownloadedPlayList,
    SettingPanel, 
    TrayMenu, 
    AlertWindow
)
from widgets.core_widgets.context_menu import ContextMenu
from services import (
    ThemeManager,
    DownloadManager, 
    LoadManager, 
    LanguageManager
)
from settings import (
    AppearanceSettings,
    GeneralSettings,
)
from utils import (
    FileUtility,
    DataRetriveUtility
)


class App(ctk.CTk):
    """
    Initialize the application.

    This method sets up the initial state of the application by initializing attributes and widgets.

    Attributes:
        root_width (int): The initial width of the application window.
        root_height (int): The initial height of the application window.
        is_geometry_changes_tracker_running (bool): A flag indicating whether the geometry changes tracker is
                                                    running.
        selected_download_mode (str): The selected download mode, either "video" or "playlist".
        is_content_downloading (bool): A flag indicating whether content is currently being downloaded.
        is_content_downloaded (bool): A flag indicating whether content has been downloaded.
        is_content_added (bool): A flag indicating whether content has been added.
        added_video_count (int): The number of added videos.
        downloading_video_count (int): The number of videos currently being downloaded.
        downloaded_video_count (int): The number of videos that have been downloaded.
        # Add more attributes as needed...

    Widgets:
        url_entry (tk.Entry): Entry widget for entering URLs.
        add_url_btn (tk.Button): Button widget for adding URLs.
        # Add more widget descriptions as needed...
    """
    def __init__(self) -> None:
        super().__init__()

        # window width height save on these vars.
        # I will track window width, if it changed,app will call geometry tracker.
        self.root_width = self.winfo_width()
        self.root_height = self.winfo_height()

        # this var used to track status of geometry tracker. it's running or not
        # if it's running already running it's not be start again
        self.is_geometry_changes_tracker_running = False
        
        # Track app accessibility to all directories required
        self.is_accessible_to_required_dirs  = True
        self.is_app_running = True
        
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

        self.navigate_added_btn = None
        self.navigate_downloading_btn = None
        self.navigate_downloaded_btn = None

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

        self.is_settings_open = False
        self.is_in_full_screen_mode = False
        self.root_geometry = ""
        self.is_maximized = False
        
    def create_widgets(self) -> None:
        """
        Creates and initializes all the GUI widgets for the application.

        This method sets up various widgets such as entry fields, radio buttons, buttons, scrollable frames, labels,
        and context menus. It also creates the settings panel and logo frame for the application.
        """
        self.url_entry = ctk.CTkEntry(master=self, placeholder_text="Enter Youtube URL")

        self.video_radio_btn = ctk.CTkRadioButton(
            master=self,
            text="Video",
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

        self.navigate_added_btn = ctk.CTkButton(
            master=self,
            text="Added",
            command=lambda: self.place_frame(self.added_content_scroll_frame, "added")
        )

        self.navigate_downloading_btn = ctk.CTkButton(
            master=self,
            text="Downloading",
            command=lambda: self.place_frame(self.downloading_content_scroll_frame, "downloading")
        )

        self.navigate_downloaded_btn = ctk.CTkButton(
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
            theme_settings_change_callback=self.update_appearance_settings,
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
            options_texts=["select_all", "cut", "copy", "paste"],
            options_commands=[self.select_all_url, self.cut_url, self.copy_url, self.paste_url]
        )

        self.logo_frame = ctk.CTkFrame(master=self)
        self.logo_label = ctk.CTkLabel(master=self.logo_frame, text="⚡")

    def select_all_url(self) -> None:
        """
        Selects all text in the URL entry field.
        """
        self.url_entry.focus()
        pyautogui.hotkey("ctrl", "a")
        self.context_menu.place_forget()

    def cut_url(self) -> None:
        """
        Cuts text from the URL entry field.
        """
        self.url_entry.focus()
        pyautogui.hotkey("ctrl", "x")
        self.context_menu.place_forget()

    def copy_url(self) -> None:
        """
        Copies text from the URL entry field.
        """
        self.url_entry.focus()
        pyautogui.hotkey("ctrl", "c")
        self.context_menu.place_forget()

    def paste_url(self) -> None:
        """
        Pastes text into the URL entry field.
        """
        self.url_entry.focus()
        pyautogui.hotkey("ctrl", "v")
        self.context_menu.place_forget()

    def place_forget_nav_frames(self) -> None:
        """
        Hides the navigation frames for added, downloading, and downloaded content.
        """
        self.added_content_scroll_frame.place_forget()
        self.downloading_content_scroll_frame.place_forget()
        self.downloaded_content_scroll_frame.place_forget()

    def place_forget_nav_labels(self) -> None:
        """
        Hides the navigation labels for added, downloading, and downloaded content.
        """
        self.added_frame_info_label_placed = False
        self.downloading_frame_info_label_placed = False
        self.downloaded_frame_info_label_placed = False
        self.added_frame_info_label.place_forget()
        self.downloading_frame_info_label.place_forget()
        self.downloaded_frame_info_label.place_forget()

    def place_nav_label(self, frame_name: str) -> None:
        """
        Places the navigation label for the specified frame in the center of the main window.

        Args:
            frame_name (str): The name of the frame ('added', 'downloading', or 'downloaded').
        """
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

    def place_frame(self, frame: ctk.CTkScrollableFrame, frame_name: str) -> None:
        """
        Places the specified scrollable frame in the main window and updates the navigation label.

        Args:
            frame (ctk.CTkScrollableFrame): The scrollable frame to be placed.
            frame_name (str): The name of the frame ('added', 'downloading', or 'downloaded').
        """
        self.place_forget_nav_frames()
        frame.place(y=90 * AppearanceSettings.settings["scale_r"], x=10)
        self.place_nav_label(frame_name)

    def place_widgets(self) -> None:
        """
        Places all the GUI widgets in their respective positions within the main window.

        This method sets the position of various widgets such as buttons, entry fields, radio buttons, labels,
        and scrollable frames within the main window based on a predetermined layout.
        """
        scale = AppearanceSettings.settings["scale_r"]
        self.settings_btn.place(x=-5, y=4)
        self.url_entry.place(x=43 * scale, y=4)
        self.add_url_btn.place(y=4)
        self.video_radio_btn.place(y=5)
        self.playlist_radio_btn.place(y=25 * scale)
        self.navigate_added_btn.place(y=50 * scale, x=10)
        self.navigate_downloading_btn.place(y=50 * scale)
        self.navigate_downloaded_btn.place(y=50 * scale)
        self.place_frame(self.added_content_scroll_frame, "added")
        self.videos_status_count_label.place(x=10, rely=1, y=-20 * scale)
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")

    def set_widgets_fonts(self) -> None:
        """
        Sets the fonts for various GUI widgets.

        This method configures the font settings for different GUI widgets such as entry fields, buttons, labels, etc.,
        based on a predetermined font style and size.
        """
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
        self.navigate_added_btn.configure(font=font_style_2)
        self.navigate_downloading_btn.configure(font=font_style_2)
        self.navigate_downloaded_btn.configure(font=font_style_2)
        self.settings_btn.configure(font=("arial", 25 * scale, "normal"))
        self.context_menu.configure(font=("Segoe UI", 13 * scale, "bold"))
        self.videos_status_count_label.configure(font=("Segoe UI", 11 * scale, "normal"))
        self.logo_label.configure(font=("arial", 50 * scale, "normal"))

    def set_widgets_sizes(self) -> None:
        """
        Sets the sizes for various GUI widgets.

        This method configures the size settings for different GUI widgets such as entry fields, buttons,
        radio buttons, etc.,based on a predetermined scale value.
        """
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
        self.navigate_added_btn.configure(height=int(40 * scale))
        self.navigate_downloading_btn.configure(height=int(40 * scale))
        self.navigate_downloaded_btn.configure(height=int(40 * scale))
        self.settings_btn.configure(width=int(30 * scale), height=int(40 * scale))
        self.context_menu.configure(
            width=int(120 * AppearanceSettings.settings["scale_r"]),
            height=int(130 * AppearanceSettings.settings["scale_r"])
        )
        self.videos_status_count_label.configure(height=int(15 * scale))

    def configure_widgets_size(self) -> None:
        """
        Configures the size and placement of various GUI widgets based on the current size of the main window.

        This method adjusts the size and placement settings for different GUI widgets such as entry fields, buttons,
        scrollable frames, etc., based on the current size of the main window. It ensures that the widgets are
        appropriately sized and positioned to maintain a visually pleasing layout.
        """
        scale = AppearanceSettings.settings["scale_r"]
        root_width = self.winfo_width()
        root_height = self.winfo_height()
        self.url_entry.configure(width=root_width - 250 * scale)

        button_margin = int(3 * scale)
        nav_button_width = int((root_width - 20 - button_margin * 3) / 3)
        self.navigate_added_btn.configure(width=nav_button_width)
        self.navigate_downloading_btn.configure(width=nav_button_width)
        self.navigate_downloaded_btn.configure(width=nav_button_width)

        self.navigate_downloading_btn.place(x=nav_button_width + 10 + button_margin)
        self.navigate_downloaded_btn.place(x=nav_button_width * 2 + 10 + button_margin * 2)

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

    def set_widgets_texts(self):
        self.url_entry.configure(
            placeholder_text=LanguageManager.data["enter_youtube_url"]
        )
        self.video_radio_btn.configure(text=LanguageManager.data["video"])
        self.playlist_radio_btn.configure(text=LanguageManager.data["playlist"])
        self.add_url_btn.configure(text=LanguageManager.data["add +"])
        self.navigate_added_btn.configure(text=LanguageManager.data["added"] + " (0)")
        self.navigate_downloading_btn.configure(text=LanguageManager.data["downloading"] + " (0)")
        self.navigate_downloaded_btn.configure(text=LanguageManager.data["downloaded"] + " (0)")
        self.added_frame_info_label.configure(
            text=LanguageManager.data["added_videos_&_playlists_will_be_display_here"]
        )
        self.downloading_frame_info_label.configure(
            text=LanguageManager.data["downloading_videos_&_playlists_will_be_display_here"]
        )
        self.downloaded_frame_info_label.configure(
            text=LanguageManager.data["downloaded_videos_&_playlists_will_be_display_here"]
        )
        self.videos_status_count_label.configure(
            text=f"{LanguageManager.data['loading']} : {LoadManager.queued_load_count + LoadManager.active_load_count}"
                 f" | "
                 f"{LanguageManager.data['downloading']} : {DownloadManager.queued_download_count + 
                                                            DownloadManager.active_download_count}"
        )
        
    def update_widgets_text(self):
        self.set_widgets_texts()

    def set_widgets_accent_color(self) -> None:
        """
        Sets the accent color for various GUI widgets.

        This method configures the accent color for different GUI widgets such as buttons, radio buttons, labels, etc.,
        based on the current accent color setting in the application's appearance settings.
        """
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
        self.navigate_added_btn.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.navigate_downloading_btn.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.navigate_downloaded_btn.configure(
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

    def set_widgets_colors(self) -> None:
        """
        Sets the colors for various GUI widgets.

        This method configures the color settings for different GUI widgets such as buttons, entry fields, radio buttons
        ,labels, etc., based on the current color settings in the application's appearance settings.
        """
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

        self.navigate_added_btn.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"],
            hover=False
        )
        self.navigate_downloading_btn.configure(
            bg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"],
            hover=False
        )
        self.navigate_downloaded_btn.configure(
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

    def bind_widgets_events(self) -> None:
        """
        Binds events to various GUI widgets for handling user interactions.

        This method binds different event handlers to GUI widgets such as entry fields, buttons, radio buttons, labels,
        etc.,for handling user interactions such as mouse clicks, mouse hover, focus changes, etc. It ensures that
        appropriate actions are taken in response to user interactions to maintain the desired functionality and
        user experience.
        """
        self.url_entry.bind("<Button-3>", self.open_context_menu)
        self.url_entry.bind("<Button-2>", self.open_context_menu)
        self.bind("<Button-2>", self.close_context_menu)
        self.bind("<Button-3>", self.close_context_menu)

        self.url_entry.bind("<Button-1>", self.close_context_menu_directly)
        self.bind("<Button-1>", self.close_context_menu_directly)
        self.bind('<FocusOut>', self.close_context_menu_directly)
        self.bind("<Configure>", self.run_geometry_changes_tracker)

        def on_mouse_enter_url_entry(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the URL entry field.

            This function is called when the mouse enters the URL entry field. It changes the appearance settings of
            the URL entry field to reflect the hover state, such as modifying foreground color, border color, and
            text color, based on the current color settings in the application's appearance settings.
            """
            self.url_entry.configure(
                fg_color=AppearanceSettings.settings["url_entry"]["fg_color"]["hover"],
                border_color=AppearanceSettings.settings["url_entry"]["border_color"]["hover"],
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["hover"]
            )

        def on_mouse_leave_url_entry(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the URL entry field.

            This function is called when the mouse leaves the URL entry field. It reverts the appearance settings of the
            URL entry field back to the normal state after hover, restoring the original foreground color, border color,
            and text color based on the current  color settings in the application's appearance settings.
            """
            self.url_entry.configure(
                fg_color=AppearanceSettings.settings["url_entry"]["fg_color"]["normal"],
                border_color=AppearanceSettings.settings["url_entry"]["border_color"]["normal"],
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["normal"]
            )

        self.url_entry.bind("<Enter>", on_mouse_enter_url_entry)
        self.url_entry.bind("<Leave>", on_mouse_leave_url_entry)

        ######################################################################################

        def on_mouse_enter_settings_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the settings button.

            This function is called when the mouse enters the settings button. It adjusts the text color of the settings
            button to reflect the hover state, using the accent color defined in the application's appearance settings.
            """
            self.settings_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"])

        def on_mouse_leave_settings_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the settings button.

            This function is called when the mouse leaves the settings button. It resets the text color of the settings
            button to its normal state, using the accent color defined in the application's appearance settings.
            """
            self.settings_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

        self.settings_btn.bind("<Enter>", on_mouse_enter_settings_btn)
        self.settings_btn.bind("<Leave>", on_mouse_leave_settings_btn)

        ######################################################################################

        def on_mouse_enter_video_radio_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the video radio button.

            This function is called when the mouse enters the video radio button. It adjusts the text color and
            foreground color of the video radio button to reflect the hover state, using the colors defined in
            the application's appearance settings.
            """
            self.video_radio_btn.configure(
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["hover"],
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def on_mouse_leave_video_radio_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the video radio button.

            This function is called when the mouse leaves the video radio button. It resets the text color and
            foreground color of the video radio button to their normal states, using the colors defined in the
            application's appearance settings.
            """
            self.video_radio_btn.configure(
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["normal"],
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.video_radio_btn.bind("<Enter>", on_mouse_enter_video_radio_btn)
        self.video_radio_btn.bind("<Leave>", on_mouse_leave_video_radio_btn)

        ######################################################################################

        def on_mouse_enter_playlist_radio_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the playlist radio button.

            This function is called when the mouse enters the playlist radio button. It adjusts the text color and
            foreground color of the playlist radio button to reflect the hover state, using the colors defined in
            the application's appearance settings.
            """
            self.playlist_radio_btn.configure(
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["hover"],
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def on_mouse_leave_playlist_radio_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the playlist radio button.

            This function is called when the mouse leaves the playlist radio button. It resets the text color and
            foreground color of the playlist radio button to their normal states, using the colors defined in the
            application's appearance settings.
            """
            self.playlist_radio_btn.configure(
                text_color=AppearanceSettings.settings["url_entry"]["text_color"]["normal"],
                fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.playlist_radio_btn.bind("<Enter>", on_mouse_enter_playlist_radio_btn)
        self.playlist_radio_btn.bind("<Leave>", on_mouse_leave_playlist_radio_btn)

        ######################################################################################

        def on_mouse_enter_add_video_playlist_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the add video/playlist button.

            This function is called when the mouse enters the add video/playlist button. It adjusts the border color,
            text color, and foreground color of the button to reflect the hover state, using the colors defined in the
            application's appearance settings.
            """
            self.add_url_btn.configure(
                border_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                fg_color=AppearanceSettings.settings["url_adding_button"]["fg_color"]["hover"]
            )

        def on_mouse_leave_add_video_playlist_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the add video/playlist button.

            This function is called when the mouse leaves the add video/playlist button. It resets the border color,
            text color, and foreground color of the button to their normal states, using the colors defined in
            the application's appearance settings.
            """
            self.add_url_btn.configure(
                border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                fg_color=AppearanceSettings.settings["url_adding_button"]["fg_color"]["normal"]
            )

        self.add_url_btn.bind("<Enter>", on_mouse_enter_add_video_playlist_btn)
        self.add_url_btn.bind("<Leave>", on_mouse_leave_add_video_playlist_btn)

        ######################################################################################

        def on_mouse_enter_navigate_added_frame_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the navigate added frame button.

            This function is called when the mouse enters the navigate added frame button. It adjusts the text color and
            foreground color of the button to reflect the hover state, using the colors defined in the
            application's appearance settings.
            """
            self.navigate_added_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["hover"]
            )

        def on_mouse_leave_navigate_added_frame_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the navigate added frame button.

            This function is called when the mouse leaves the navigate added frame button. It resets the text color and
            foreground color of the button to their normal states, using the colors defined in the application's
            appearance settings.
            """
            self.navigate_added_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"]
            )

        self.navigate_added_btn.bind("<Enter>", on_mouse_enter_navigate_added_frame_btn)
        self.navigate_added_btn.bind("<Leave>", on_mouse_leave_navigate_added_frame_btn)

        ######################################################################################

        def on_mouse_enter_navigate_downloading_frame_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the navigate downloading frame button.

            This function adjusts the text color and foreground color of the navigate downloading frame button to
            reflect the hover state when the mouse enters the button.The colors are obtained from the application's
            appearance settings for the hover state.

            Parameters:
                _event (tk.Event): The event object.
            """
            self.navigate_downloading_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["hover"]
            )

        def on_mouse_leave_navigate_downloading_frame_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the navigate downloading frame button.

            This function resets the text color and foreground color of the navigate downloading frame button to their
            normal states when the mouse leaves the button.The colors are obtained from the application's appearance
            settings for the normal state.

            Parameters:
                _event (tk.Event): The event object.
            """
            self.navigate_downloading_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"]
            )

        self.navigate_downloading_btn.bind("<Enter>", on_mouse_enter_navigate_downloading_frame_btn)
        self.navigate_downloading_btn.bind("<Leave>", on_mouse_leave_navigate_downloading_frame_btn)

        ######################################################################################

        def on_mouse_enter_navigate_downloaded_frame_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the navigate downloaded frame button.

            This function adjusts the text color and foreground color of the navigate downloaded frame button to reflect
            the hover state when the mouse enters the button.The colors are obtained from the application's appearance
            settings for the hover state.

            Parameters:
                _event (tk.Event): The event object.
            """
            self.navigate_downloaded_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["hover"]
            )

        def on_mouse_leave_navigate_downloaded_frame_btn(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the navigate downloaded frame button.

            This function resets the text color and foreground color of the navigate downloaded frame button to their
            normal states when the mouse leaves the button. The colors are obtained from the application's appearance
            settings for the normal state.

            Parameters:
                _event (tk.Event): The event object.
            """
            self.navigate_downloaded_btn.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
                fg_color=AppearanceSettings.settings["navigation_button"]["fg_color"]["normal"]
            )

        self.navigate_downloaded_btn.bind("<Enter>", on_mouse_enter_navigate_downloaded_frame_btn)
        self.navigate_downloaded_btn.bind("<Leave>", on_mouse_leave_navigate_downloaded_frame_btn)

        #######################################################################################

        def on_mouse_enter_added_frame_info_label(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the added frame information label.

            This function adjusts the text color of the added frame information label to reflect the hover state when
            the mouse enters the label. The color is obtained from the application's appearance settings
            for the hover state.

            Parameters:
                _event (tk.Event): The event object.
            """
            self.added_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def on_mouse_leave_added_frame_info_label(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the added frame information label.

            This function resets the text color of the added frame information label to its normal state when the mouse
            leaves the label. The color is obtained from the application's appearance settings for the normal state.

            Parameters:
                _event (tk.Event): The event object.
            """
            self.added_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.added_frame_info_label.bind("<Enter>", on_mouse_enter_added_frame_info_label)
        self.added_frame_info_label.bind("<Leave>", on_mouse_leave_added_frame_info_label)

        #######################################################################################

        def on_mouse_enter_downloading_frame_info_label(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the downloading frame information label.

            This function adjusts the text color of the downloading frame information label to reflect the hover state
            when the mouse enters the label. The color is obtained from the application's appearance settings
            for the hover state.

            Parameters:
                _event (tk.Event): The event object.
            """
            self.downloading_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def on_mouse_leave_downloading_frame_info_label(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the downloading frame information label.

            This function resets the text color of the downloading frame information label to its normal state when the
            mouse leaves the label. The color is obtained from the application's appearance settings for
            the normal state.

            Parameters:
                _event (tk.Event): The event object.
            """
            self.downloading_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.downloading_frame_info_label.bind("<Enter>", on_mouse_enter_downloading_frame_info_label)
        self.downloading_frame_info_label.bind("<Leave>", on_mouse_leave_downloading_frame_info_label)

        #######################################################################################
        def on_mouse_enter_downloaded_frame_info_label(_event: tk.Event) -> None:
            """
            Event handler for mouse entering the downloaded frame information label.

            This function adjusts the text color of the downloaded frame information label to reflect the hover state
            when the mouse enters the label. The color is obtained from the application's appearance settings for
            the hover state.

            Parameters:
                _event (tk.Event): The event object.
            """
            self.downloaded_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def mouse_ot_downloaded_frame_info_label(_event: tk.Event) -> None:
            """
            Event handler for mouse leaving the downloaded frame information label.

            This function resets the text color of the downloaded frame information label to its normal state when the
            mouse leaves the label. The color is obtained from the application's appearance settings for the
            normal state.

            Parameters:
                _event (tk.Event): The event object.
            """
            self.downloaded_frame_info_label.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )

        self.downloaded_frame_info_label.bind("<Enter>", on_mouse_enter_downloaded_frame_info_label)
        self.downloaded_frame_info_label.bind("<Leave>", mouse_ot_downloaded_frame_info_label)
    
    def bind_keyboard_shortcuts(self):
        """
        Bind the keyboards shortcuts.
        """
        def toggle_settings(_event):
            if self.is_settings_open:
                self.close_settings()
            else:
                self.open_settings()
        
        def close_settings(_event):
            if self.is_settings_open:
                self.close_settings()
                
        self.bind("<Control-,>", toggle_settings)
        self.bind("<Escape>", close_settings)
        
        def choose_download_mode(_event):
            if self.selected_download_mode == "video":
                self.select_download_mode("playlist")
            else:
                self.select_download_mode("video")
                
        self.bind("<Control-d>", choose_download_mode)
        self.bind("<Control-D>", choose_download_mode)
        self.bind("<F6>", choose_download_mode)
        
        def add_video_playlist(_event):
            self.add_video_playlist()
        self.bind("<Return>", add_video_playlist)
        
        def toggle_full_screen(_event):
            if not self.is_in_full_screen_mode: 
                self.is_in_full_screen_mode = True
                self.attributes("-fullscreen", True)
                self.run_geometry_changes_tracker("_event")
            else:
                self.is_in_full_screen_mode = False
                self.attributes("-fullscreen", False)
                # Had to reset titlebar color because of customtkinter has some issue with when fullscreen toggle
                self._windows_set_titlebar_color(self._get_appearance_mode())
                self.run_geometry_changes_tracker("_event")
    
        self.bind("<F11>", toggle_full_screen)
        self.bind("<Alt-Return>", toggle_full_screen)
        
        def minimize(_event):
            self.iconify()
            
        self.bind("<Control-n>", minimize)
        self.bind("<Control-N>", minimize)
        self.bind("<F9>", minimize)
        self.bind("<Control-Down>", minimize)
        
        def toggle_maximize(_event):
            if not self.is_maximized:
                self.is_maximized = True
                self.root_geometry = self.geometry()
                self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+{0}+{0}")
                self.run_geometry_changes_tracker("_event")
            else:
                self.is_maximized = False
                self.geometry(self.root_geometry)
                self.run_geometry_changes_tracker("_event")
        
        self.bind("<Control-m>", toggle_maximize)
        self.bind("<Control-M>", toggle_maximize)
        self.bind("<F10>", toggle_maximize)
        self.bind("<Control-Up>", toggle_maximize)
        
        def terminate(_event):
            self.on_app_closing()
            
        self.bind("<Control-Alt-q>", terminate)
        self.bind("<Control-Alt-Q>", terminate)
        self.bind("<Control-Alt-F4>", terminate)
        
        def quick_exit(_event):
            self.show_close_confirmation_dialog()
            
        self.bind("<Control-q>", quick_exit)
        self.bind("<Control-Q>", quick_exit)
        
        def minimize_to_tray_icon(_event):
            self.minimize_to_tray()
            
        self.bind("<F12>", minimize_to_tray_icon)
        self.bind("<Control-Shift-m>", minimize_to_tray_icon)
        self.bind("<Control-Shift-M>", minimize_to_tray_icon)
        self.bind("<Control-Shift-n>", minimize_to_tray_icon)
        self.bind("<Control-Shift-N>", minimize_to_tray_icon)

    def show_app_logo(self) -> None:
        
        """
        Show the application logo.
        """
        self.logo_frame.place(relwidth=1, relheight=1)

    def hide_app_logo(self) -> None:
        """
        Hide the application logo.
        """
        self.logo_frame.place_forget()

    def update_widgets(self) -> None:
        """
        Update all the widgets in the application.
        """
        for widget in self.winfo_children():
            widget.update()
            try:
                for sub_widget in widget.winfo_children():
                    sub_widget.update()
                    sub_widget.focus_set()
                    try:
                        for sub_sub_widget in sub_widget.winfo_children():
                            sub_sub_widget.update()
                            sub_widget.focus_set()
                            try:
                                for sub_sub_sub_widget in sub_sub_widget.winfo_children():
                                    sub_sub_sub_widget.update()
                                    sub_widget.focus_set()
                            except Exception as error:
                                print(f"app.py L-657 : {error}")
                    except Exception as error:
                        print(f"app.py L-659 : {error}")
            except Exception as error:
                print(f"app.py L-661 : {error}")
        self.update()
        self.focus_set()

    def geometry_changes_tracker(self) -> None:
        """
        Track changes in the geometry of the window and adjust accordingly.
        """
        self.is_geometry_changes_tracker_running = True
        update_delay = 0.5
        # Check if the old window width or height is different from the current width or height
        if self.root_width != self.winfo_width() or self.root_height != self.winfo_height():
            # If the window size changed, show the logo on full screen
            self.show_app_logo()
            self.root_width = self.winfo_width()
            self.root_height = self.winfo_height()
            time.sleep(update_delay)
            # Wait until the user stops changing the window size
            while self.root_width != self.winfo_width() or self.root_height != self.winfo_height():
                # Keep updating the old window size to track if the user changed the window size or not
                self.root_width = self.winfo_width()
                self.root_height = self.winfo_height()
                # Set delay to 1 sec
                time.sleep(update_delay)
            self.configure_widgets_size()
            self.update_idletasks()
            self.update_widgets()
            self.hide_app_logo()
        self.is_geometry_changes_tracker_running = False

    def run_geometry_changes_tracker(self, _event: tk.Event | str) -> None:
        """
        Run the geometry changes tracker in a separate thread.
        """
        if not self.is_geometry_changes_tracker_running:
            threading.Thread(target=self.geometry_changes_tracker).start()

    def select_download_mode(self, download_mode: Literal["video", "playlist"]) -> None:
        """
        Select the download mode (either "video" or "playlist").
        """
        self.selected_download_mode = download_mode
        if download_mode == "playlist":
            self.playlist_radio_btn.select()
            self.video_radio_btn.deselect()
        else:
            self.video_radio_btn.select()
            self.playlist_radio_btn.deselect()

    def update_active_videos_count_status(self) -> None:
        """
        Update the status label with the count of active loading and active downloading videos.
        """
        self.videos_status_count_label.configure(
            text=f"{LanguageManager.data['loading']} : {LoadManager.queued_load_count + LoadManager.active_load_count}"
                 f" | "
                 f"{LanguageManager.data['downloading']} : {DownloadManager.queued_download_count + 
                                                            DownloadManager.active_download_count}"
        )
    
    def update_total_videos_count_status(self, added_video_count, downloading_video_count, downloaded_video_count) -> None:
        """
        Update the status label with the count of added loading and added downloading and downloaded videos.
        """
        self.navigate_added_btn.configure(text=LanguageManager.data["added"] + f" ({str(added_video_count)})")
        self.navigate_downloading_btn.configure(text=LanguageManager.data["downloading"] + f" ({str(downloading_video_count)})")
        self.navigate_downloaded_btn.configure(text=LanguageManager.data["downloaded"] + f" ({str(downloaded_video_count)})")

    def fade_effect(self) -> None:
        """
        Apply a fade effect to the application.
        """
        fade_out_to = AppearanceSettings.settings["opacity_r"] - 0.15
        
        def fade_out(alpha):
            print(alpha)
            if alpha > fade_out_to:
                self.attributes("-alpha", alpha)
                self.after(25, fade_out, alpha - 0.025)
            else:
                fade_in(fade_out_to)

        def fade_in(alpha):
            if AppearanceSettings.settings["opacity_r"] >= alpha:
                self.attributes("-alpha", alpha)
                self.after(25, fade_in, alpha + 0.025)
            else:
                self.attributes("-alpha", AppearanceSettings.settings["opacity_r"])
            
        fade_out(AppearanceSettings.settings["opacity_r"])
        
    def add_video_playlist(self) -> None:
        """
        Add a video or playlist to the content.
        """
        self.added_frame_info_label.place_forget()
        yt_url = self.url_entry.get()
        
        # if url entry is nothing just do nothing
        if yt_url.replace(" ", "") == "":
            return
        
        self.is_content_added = True
        
        # Show fade effect
        self.fade_effect()
        
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

    def download_video(self, video: AddedVideo) -> None:
        """
        Download a video.

        Args:
            video (AddedVideo): The video to be downloaded.
        """
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
            notification_thumbnail_image_path=video.notification_thumbnail_image_path,
            # download info
            download_quality=video.download_quality,
            download_type=video.download_type,
            video_download_complete_callback=self.downloaded_video,
        ).pack(fill="x", pady=2)

    def download_playlist(self, playlist: AddedPlayList) -> None:
        """
        Download a playlist.

        Args:
            playlist (AddedPlayList): The playlist to be downloaded.
        """
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
            playlist_video_count=len(playlist.loaded_videos),
            playlist_url=playlist.playlist_url,
            # play list videos
            videos=playlist.loaded_videos,
            # download directory
            # playlist download completed callback utils
            playlist_download_complete_callback=self.downloaded_playlist,
        ).pack(fill="x", pady=2)

    def downloaded_video(self, video: DownloadingVideo) -> None:
        """
        Handle downloaded video.

        Args:
            video (DownloadingVideo): The downloaded video.
        """
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

    def downloaded_playlist(self, playlist: DownloadingPlayList) -> None:
        """
        Handle downloaded playlist.

        Args:
            playlist (DownloadingPlayList): The downloaded playlist.
        """
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
            playlist_video_count=len(playlist.downloaded_videos),
            playlist_url=playlist.playlist_url,
            videos=playlist.downloaded_videos
        ).pack(fill="x", pady=2)

    def open_context_menu(self, _event: tk.Event) -> None:
        """
        Open the context menu at the current pointer position.

        Args:
            _event: The event triggering the context menu opening.
        """
        pointer_x = self.winfo_pointerx() - self.winfo_rootx()
        pointer_y = self.winfo_pointery() - self.winfo_rooty()

        self.context_menu.place(x=pointer_x, y=pointer_y)

    def close_context_menu(self, _event: tk.Event) -> None:
        """
        Close the context menu if the pointer is not over the entry widget.

        Args:
            _event: The event triggering the context menu closing.
        """
        pointer_x = self.winfo_pointerx() - self.winfo_rootx()
        pointer_y = self.winfo_pointery() - self.winfo_rooty()

        if (pointer_x < self.url_entry.winfo_x() or pointer_y < self.url_entry.winfo_y() or
                pointer_x > (self.url_entry.winfo_x() + self.url_entry.winfo_width()) or
                pointer_y > (self.url_entry.winfo_y() + self.url_entry.winfo_height())):
            self.context_menu.place_forget()

    def close_context_menu_directly(self, _event: tk.Event) -> None:
        """
        Close the context menu directly.

        Args:
            _event: The event triggering the context menu closing.
        """
        self.context_menu.place_forget()

    def update_general_settings(self, updated: Literal["language"] = None) -> None:
        """
        Update the general settings of the application and save them.
        """
        if updated == "language":
            LanguageManager.update_language()
            self.update_widgets_text()

        GeneralSettings.save_settings()

    def update_appearance_settings(
            self,
            updated: Literal["accent_color", "theme_mode", "opacity"] = None) -> None:
        """
        Update the theme settings based on the specified update.

        Args:
            updated (Literal["accent_color", "theme_mode", "opacity"], optional):
                The type of theme setting that was updated.
        """
        if updated == "accent_color":
            self.set_widgets_accent_color()
            ThemeManager.update_accent_color()
        if updated == "theme_mode":
            ctk.set_appearance_mode(AppearanceSettings.themes[AppearanceSettings.settings["root"]["theme_mode"]])
        if updated == "opacity":
            self.attributes("-alpha", AppearanceSettings.settings["opacity_r"])
        AppearanceSettings.save_settings()

    def open_settings(self) -> None:
        """
        Open the settings panel and configure the settings button to close the settings.

        """
        self.is_settings_open = True
        ContextMenu.close_all_menus()
        self.settings_panel.place(relwidth=1, relheight=1)
        self.settings_btn.configure(command=self.close_settings)

    def close_settings(self) -> None:
        """
        Close the settings panel and configure the settings button to open the settings.

        """
        self.is_settings_open = False
        self.settings_panel.place_forget()
        self.settings_btn.configure(command=self.open_settings)

    def on_app_closing(self, restart: bool = False) -> None:
        """
        Handle the application closing event.

        Args:
            restart (bool, optional): Whether to restart the application. Defaults to False.
        """
        if self.is_accessible_to_required_dirs :
            GeneralSettings.settings['window_geometry'] = self.geometry()
            GeneralSettings.save_settings()
            self.clear_temporally_saved_files()
        self.destroy()
        self.is_app_running = False
        if not restart:
            os._exit(0)

    def cancel_app_closing(self) -> None:
        """
        Cancel the application closing action.

        """
        self.bind_widgets_events()

    def restart(self) -> None:
        """
        Restart the application.

        """
        self.on_app_closing(restart=True)
        if os.path.exists("main.py"):
            os.startfile("main.py")
        if os.path.exists("PyTube Downloader.exe"):
            os.startfile("PyTube Downloader.exe")
        os._exit(0)
        
    def confirm_quit(self):
        self.restore_from_tray()
        self.show_close_confirmation_dialog()

    def show_close_confirmation_dialog(self) -> None:
        """
        Show a confirmation dialog before closing the application.

        """
        scale = AppearanceSettings.settings["scale_r"]
        AlertWindow(
            master=self,
            original_configure_callback=self.run_geometry_changes_tracker,
            alert_msg="exit_confirmation",
            ok_button_display=True,
            cancel_button_display=True,
            ok_button_callback=self.on_app_closing,
            cancel_button_callback=self.cancel_app_closing,
            callback=self.cancel_app_closing,
            wait_for_previous=True,
            width=int(450 * scale),
            height=int(130 * scale),
        )

    def restore_from_tray(self) -> None:
        """
        Restore the application window from the system tray.
        """
        self.tray_menu.stop()
        self.deiconify()

    def minimize_to_tray(self) -> None:
        """
        Minimize the application window to the system tray.
        """
        self.iconify()
        self.tray_menu = TrayMenu(
            open_command=self.restore_from_tray,
            quit_command=self.confirm_quit,
        )
        self.withdraw()
        threading.Thread(target=self.tray_menu.run, daemon=True).start()

    def run(self) -> None:
        """
        Run the application.
        """
        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.mainloop()

    @classmethod
    def clear_temporally_saved_files(self) -> None:
        """
        Clears temporarily saved files, such as thumbnails.
        """
        FileUtility.delete_files("temp\\thumbnails", ["this directory is necessary"])
    
    def open_update_download_page(self) -> None:
        """
        Open website for download latest version
        """
        webbrowser.open("https://sourceforge.net/projects/pytube-downloader/files/latest/download")
        
    def check_for_updates(self) -> None:
        """
        Update the version of the application.
        """
        # Check the app is updated or not
        latest_version = DataRetriveUtility.get_latest_version()
        current_version = DataRetriveUtility.get_current_version()
        scale = AppearanceSettings.settings["scale_r"]
        if latest_version is not None:
            if latest_version != current_version:
                AlertWindow(
                    master=self,
                    original_configure_callback=self.run_geometry_changes_tracker,
                    alert_msg="update_alert",
                    ok_button_display=True,
                    ok_button_callback=self.open_update_download_page,
                    cancel_button_display=True,
                    wait_for_previous=True,
                    width=int(450 * scale),
                    height=int(130 * scale)
                )
                
    def run_update_check(self):
        """
        Run the update check in a separate thread.
        """
        self.update_check_thread = threading.Thread(target=self.check_for_updates, daemon=True)
        self.update_check_thread.start()

    def check_accessibility(self):
        scale = AppearanceSettings.settings["scale_r"]
        DIRECTORIES = [GeneralSettings.backup_dir, GeneralSettings.settings["download_directory"], "data", "assets", "temp"]
        for directory in DIRECTORIES:
            # print("Checking Accesibility :", directory)
            if not FileUtility.is_accessible(directory):
                self.is_accessible_to_required_dirs  = False
                AlertWindow(
                    master=self,
                    original_configure_callback=self.run_geometry_changes_tracker,
                    alert_msg="run_as_admin_mode",
                    ok_button_display=True,
                    ok_button_callback=self.on_app_closing,
                    wait_for_previous=True,
                    callback=self.on_app_closing,
                    width=int(450 * scale),
                    height=int(130 * scale)
                )
                
    def run_accessibility_check(self):
        """
        Run the accessibilit check in a separate thread.
        """
        self.update_check_thread = threading.Thread(target=self.check_accessibility, daemon=True)
        self.update_check_thread.start()
        