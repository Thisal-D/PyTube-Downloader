import threading
import customtkinter as ctk
import pytube
from typing import Literal, Union, List
from .play_list import PlayList
from widgets import AddedVideo
from utils import GuiUtils
from settings import AppearanceSettings, GeneralSettings
from services import LanguageManager


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
        # state
        self.load_state: Literal[None, "waiting", "loading", "failed", "loaded"] = "loading"
        # vars for state track
        self.waiting_videos: List[AddedVideo] = []
        self.loading_videos: List[AddedVideo] = []
        self.failed_videos: List[AddedVideo] = []
        self.loaded_videos: List[AddedVideo] = []
        self.automatic_downloaded: bool = False
        
        self.qualities: List[str] = ['highest_quality', 'lowest_quality', 'audio_only']
        
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
            self.channel_btn.configure(state="normal")
            self.set_playlist_data()
            self.load_videos()
        except Exception as error:
            print(f"added_play_list.py L-74 : {error}")
            self.indicate_loading_failure()

    def load_videos(self):
        for video_url in self.playlist.video_urls:
            video = AddedVideo(
                root=self.root,
                master=self.playlist_videos_frame,
                width=self.playlist_videos_frame.winfo_width() - 20,
                height=70 * AppearanceSettings.settings["scale_r"],
                video_url=video_url,
                video_download_button_click_callback=self.video_download_button_click_callback,
                mode="playlist",
                # videos state track
                video_load_status_callback=self.videos_status_track,
            )
            if self.last_viewed_index < PlayList.max_videos_per_page:
                video.pack(fill="x", padx=(20, 0), pady=(1, 0))
                self.last_viewed_index += 1
            self.videos.append(video)
            
        self.configure_videos_tab_view()
        self.view_btn.configure(state="normal")

    def videos_status_track(
            self,
            video: AddedVideo,
            state: Literal["waiting", "loading", "loaded", "failed", "removed"]):
        if state == "removed":
            self.videos.remove(video)
            self.configure_videos_tab_view()
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
                if video in self.loaded_videos:
                    self.loaded_videos.remove(video)
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
        elif state == "loaded":
            self.loaded_videos.append(video)
            self.loading_videos.remove(video)

        if len(self.videos) != 0:
            self.videos_status_counts_label.configure(
                text=f"{LanguageManager.data['failed']} : {len(self.failed_videos)} |   "
                     f"{LanguageManager.data['waiting']} : {len(self.waiting_videos)} |   "
                     f"{LanguageManager.data['loading']} : {len(self.loading_videos)} |   "
                     f"{LanguageManager.data['loaded']} : {len(self.loaded_videos)}"
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
                
            self.handle_automatic_download()
            
    def handle_automatic_download(self):
        if (GeneralSettings.settings["automatic_download"]["status"] == "enable" and
                len(self.waiting_videos) == 0 and len(self.loading_videos) == 0 and
                len(self.loaded_videos) != 0) and self.automatic_downloaded is not True:
            self.automatic_downloaded = True
            auto_download_quality_index = GeneralSettings.settings["automatic_download"]["quality"]
            if len(self.failed_videos) == 0:
                self.resolution_select_menu.set(
                    LanguageManager.data[self.qualities[auto_download_quality_index]]
                )
            self.select_download_option(
                [LanguageManager.data[quality] for quality in self.qualities][auto_download_quality_index]
            )
            self.playlist_download_button_click_callback(self)

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
        self.load_state = "waiting"
        self.status_label.configure(
            text=LanguageManager.data['waiting'],
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.reload_btn.place_forget()

    def indicate_loading_failure(self):
        self.load_state = "failed"
        self.status_label.configure(
            text=LanguageManager.data['failed'],
            text_color=AppearanceSettings.settings["video_object"]["error_color"]["normal"]
        )
        self.reload_btn.place(
            relx=1,
            rely=0.5,
            anchor="w",
            x=-80 * AppearanceSettings.settings["scale_r"])

    def indicate_loading(self):
        self.load_state = "loading"
        self.status_label.configure(
            text=LanguageManager.data['loading'],
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.reload_btn.place_forget()

    def set_loading_completed(self):
        self.load_state = "loaded"
        self.status_label.configure(text=LanguageManager.data['loaded'])
        self.download_btn.configure(state="normal")
        self.resolution_select_menu.configure(
            values=[LanguageManager.data[quality] for quality in self.qualities]
        )
        if GeneralSettings.settings["automatic_download"]["status"] == "enable":
            default_index = GeneralSettings.settings["automatic_download"]["quality"]
        else:
            default_index = 0
        self.resolution_select_menu.set(
            LanguageManager.data[self.qualities[default_index]]
        )
            
        self.resolution_select_menu.configure(command=self.select_download_option)

    def download_playlist(self):
        self.root.fade_effect()
        self.playlist_download_button_click_callback(self)
        
    def select_download_option(self, e):
        selected_index = self.resolution_select_menu.cget("values").index(e)
        if selected_index != 0:
            selected_index -= len(self.qualities)
        for video in self.loaded_videos:
            video.resolution_select_menu.set(video.resolution_select_menu.cget("values")[selected_index])
            video.choose_download_type(video.resolution_select_menu.get())

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
            state="disabled",
            hover=False,
            command=self.download_playlist
        )
        self.status_label = ctk.CTkLabel(master=self.sub_frame)
        self.reload_btn = ctk.CTkButton(
            self.playlist_main_frame,
            text="⟳",
            command=self.reload_playlist,
            hover=False,
        )
        self.videos_status_counts_label = ctk.CTkLabel(
            master=self.sub_frame,
        )

    def set_widgets_texts(self):
        super().set_widgets_texts()
        self.status_label.configure(text=LanguageManager.data[self.load_state])
        self.download_btn.configure(text=LanguageManager.data["download"])
        self.videos_status_counts_label.configure(
            text=f"{LanguageManager.data['failed']} : {len(self.failed_videos)} |   "
                 f"{LanguageManager.data['waiting']} : {len(self.waiting_videos)} |   "
                 f"{LanguageManager.data['loading']} : {len(self.loading_videos)} |   "
                 f"{LanguageManager.data['loaded']} : {len(self.loaded_videos)}"
        )
        if self.load_state == "loaded":
            current_selected_quality = self.resolution_select_menu.cget("values").index(
                self.resolution_select_menu.get()
            )
            self.resolution_select_menu.configure(
                values=[LanguageManager.data[quality] for quality in self.qualities]
            )
            self.resolution_select_menu.set(
                self.resolution_select_menu.cget("values")[current_selected_quality]
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
        # super().on_mouse_enter_self(_event)
        
        """
        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])
        self.reload_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"])
        """
        
    def on_mouse_leave_self(self, _event):
        # super().on_mouse_leave_self(_event)
        
        """
        self.sub_frame.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.reload_btn.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        """
        
    def bind_widgets_events(self):
        super().bind_widgets_events()

        def on_mouse_enter_download_btn(_event):
            if self.download_btn.cget("state") == "normal":
                self.download_btn.configure(
                    fg_color=AppearanceSettings.settings["video_object"]["btn_fg_color"]["hover"],
                    text_color=AppearanceSettings.settings["video_object"]["btn_text_color"]["hover"],
                    border_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
                )
            # self.on_mouse_enter_self(_event)

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
            # self.on_mouse_enter_self(_event)

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
            width=self.master_frame.winfo_width() - (390*scale) - (50*scale + 15 * scale) - (20 * scale)
        )
        
    def __del__(self):
        """Clear the Memory."""
        del self.sub_frame
        del self.resolution_select_menu
        del self.download_btn
        del self.status_label
        del self.reload_btn
        del self.videos_status_counts_label

        del self.playlist
        del self.playlist_download_button_click_callback
        del self.video_download_button_click_callback
        del self.load_state
        
        del self.waiting_videos
        del self.loading_videos
        del self.failed_videos
        del self.loaded_videos
        
        del self.automatic_downloaded
        del self.qualities

        super().__del__()
        
    def destroy_widgets(self):
        """Destroy the child widget."""
        self.sub_frame.destroy()
        self.resolution_select_menu.destroy()
        self.download_btn.destroy()
        self.status_label.destroy()
        self.reload_btn.destroy()
        self.videos_status_counts_label.destroy()
        
        super().destroy_widgets()
        
    def kill(self):
        self.pack_forget()
        
        for video in self.videos:
            video.video_load_status_callback = GuiUtils.do_nothing
            video.kill()
        
        super().kill()
        