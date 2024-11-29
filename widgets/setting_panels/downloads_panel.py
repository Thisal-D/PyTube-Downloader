import customtkinter as ctk
from typing import Callable, Any
from tkinter import filedialog
from services import (
    ThemeManager,
    LanguageManager
)
from settings import (
    AppearanceSettings,
    GeneralSettings
)
from utils import SettingsValidateUtility
from utils import FileUtility


class DownloadsPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            general_settings_change_callback: Callable = None):

        super().__init__(
            master=master,
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )

        self.download_path_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.dash1_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.download_path_entry = ctk.CTkEntry(
            master=self,
            justify="left",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )

        self.download_path_choose_button = ctk.CTkButton(
            master=self,
            text="📂",
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            hover=False,
            command=self.select_download_path,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
            )

        # ---------------------------------------------------------------------------
        self.create_sep_path_for_videos_audios_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )

        self.dash2_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.create_sep_path_for_videos_audios_switch_state = ctk.BooleanVar(value=None)
        self.create_sep_path_for_videos_audios_switch = ctk.CTkSwitch(
            master=self,
            text="",
            command=self.change_create_sep_path_for_audios_videos,
            onvalue=True,
            offvalue=False,
            variable=self.create_sep_path_for_videos_audios_switch_state
        )
        self.create_sep_path_for_videos_audios_info_label = ctk.CTkLabel(
            master=self
        )

        # ---------------------------------------------------------------------------
        self.create_sep_path_for_qualities_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )

        self.dash3_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.create_sep_path_for_qualities_switch_state = ctk.BooleanVar(value=None)
        self.create_sep_path_for_qualities_switch = ctk.CTkSwitch(
            master=self,
            text="",
            command=self.change_create_sep_path_for_qualities,
            onvalue=True,
            offvalue=False,
            variable=self.create_sep_path_for_qualities_switch_state
        )
        self.create_sep_path_for_qualities_info_label = ctk.CTkLabel(
            master=self,
            text="",
        )
        
        # ---------------------------------------------------------------------------
        self.create_sep_path_for_playlists_label = ctk.CTkLabel(
            master=self,
            text="Playlist-Specific Directories",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.dash4_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        
        self.create_sep_path_for_playlists_switch_state = ctk.BooleanVar(value=None)
        self.create_sep_path_for_playlists_switch = ctk.CTkSwitch(
            master=self,
            text="",
            command=self.change_create_sep_path_for_playlists,
            onvalue=True,
            offvalue=False,
            variable=self.create_sep_path_for_playlists_switch_state
        ) 
        self.create_sep_path_for_playlists_info_label = ctk.CTkLabel(
            master=self,
            justify="left",
        )

        self.apply_changes_button = ctk.CTkButton(
            master=self,
            state="disabled",
            command=self.apply_downloads_settings,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        
        self.settings_reset_button = ctk.CTkButton(
            master=self, 
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            command=self.reset_settings
        )    
        
        self.download_path_changed: bool = False
        self.create_sep_path_for_qualities_state_changed: bool = False
        self.create_sep_path_for_videos_audios_state_changed: bool = False
        self.create_sep_path_for_playlists_state_changed: bool = False

        # track values validity
        self.download_path_valid: bool = True

        self.general_settings_change_callback = general_settings_change_callback
        self.configure_values()
        self.set_widgets_accent_color()
        self.set_widgets_texts()
        self.set_widgets_sizes()
        self.set_widgets_fonts()
        self.place_widgets()
        self.bind_widgets_events()

        ThemeManager.register_widget(self)
        LanguageManager.register_widget(self)

    def reset_settings(self):
        self.download_path_entry.delete(0, "end")
        self.download_path_entry.insert("end", GeneralSettings.default_download_dir)
        
        self.create_sep_path_for_videos_audios_switch.deselect()
        self.create_sep_path_for_qualities_switch.deselect()
        self.create_sep_path_for_playlists_switch.deselect()
        
        self.apply_downloads_settings()
        
    def apply_downloads_settings(self):
        GeneralSettings.settings["download_directory"] = FileUtility.format_path(self.download_path_entry.get())
        GeneralSettings.settings["create_sep_path_for_qualities"] = (
            self.create_sep_path_for_qualities_switch.get()
        )
        GeneralSettings.settings["create_sep_path_for_videos_audios"] = (
            self.create_sep_path_for_videos_audios_switch.get()
        )
        GeneralSettings.settings["create_sep_path_for_playlists"] = self.create_sep_path_for_playlists_switch.get()

        self.general_settings_change_callback()
        self.apply_changes_button.configure(state="disabled")
        
    def set_apply_button_state(self):
        if (any((self.download_path_changed, self.create_sep_path_for_videos_audios_state_changed,
                 self.create_sep_path_for_playlists_state_changed, self.create_sep_path_for_qualities_state_changed))
                and
                all((self.download_path_valid,))):
            self.apply_changes_button.configure(state="normal")
        else:
            self.apply_changes_button.configure(state="disabled")

    def download_path_validate(self, _event):
        path = FileUtility.format_path(self.download_path_entry.get())
        if path != GeneralSettings.settings["download_directory"]:
            self.download_path_changed = True
            if SettingsValidateUtility.validate_download_path(path):
                self.download_path_valid = True
            else:
                self.download_path_valid = False
        else:
            self.download_path_changed = False
        self.set_apply_button_state()

    def select_download_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.download_path_entry.delete(0, "end")
            self.download_path_entry.insert(0, directory)
            self.download_path_validate("event")
        else:
            self.download_path_valid = False
        self.set_apply_button_state()
            
    def change_create_sep_path_for_audios_videos(self):
        if (GeneralSettings.settings["create_sep_path_for_videos_audios"] !=
                self.create_sep_path_for_videos_audios_switch.get()):
            self.create_sep_path_for_videos_audios_state_changed = True
        else:
            self.create_sep_path_for_videos_audios_state_changed = False
        self.set_apply_button_state()
        
    def change_create_sep_path_for_playlists(self):
        if GeneralSettings.settings["create_sep_path_for_playlists"] != self.create_sep_path_for_playlists_switch.get():
            self.create_sep_path_for_playlists_state_changed = True
        else:
            self.create_sep_path_for_playlists_state_changed = False
        self.set_apply_button_state()
        
    def change_create_sep_path_for_qualities(self):
        if (GeneralSettings.settings["create_sep_path_for_qualities"] !=
                self.create_sep_path_for_qualities_switch.get()):
            self.create_sep_path_for_qualities_state_changed = True
        else:
            self.create_sep_path_for_qualities_state_changed = False
        self.set_apply_button_state()
        
    def configure_values(self):
        self.download_path_entry.insert(0, GeneralSettings.settings["download_directory"])
        
        if GeneralSettings.settings["create_sep_path_for_videos_audios"]:
            self.create_sep_path_for_videos_audios_switch.select()
            self.create_sep_path_for_videos_audios_switch_state.set(True)
        else:
            self.create_sep_path_for_videos_audios_switch_state.set(False)
            
        if GeneralSettings.settings["create_sep_path_for_qualities"]:
            self.create_sep_path_for_qualities_switch.select()
            self.create_sep_path_for_qualities_switch_state.set(True)
        else:
            self.create_sep_path_for_qualities_switch_state.set(False)
            
        if GeneralSettings.settings["create_sep_path_for_playlists"]:
            self.create_sep_path_for_playlists_switch.select()
            self.create_sep_path_for_playlists_switch_state.set(True)
        else:
            self.create_sep_path_for_playlists_switch_state.set(False)

    def bind_widgets_events(self):
        self.download_path_entry.bind("<KeyRelease>", self.download_path_validate)
        
        def on_mouse_enter_download_path_button(_event):
            self.download_path_choose_button.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )

        def on_mouse_leave_download_path_button(_event):
            self.download_path_choose_button.configure(
                text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
            )
        self.download_path_choose_button.bind("<Enter>", on_mouse_enter_download_path_button)
        self.download_path_choose_button.bind("<Leave>", on_mouse_leave_download_path_button)

    def set_widgets_accent_color(self):
        self.download_path_choose_button.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.apply_changes_button.configure(
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.download_path_entry.configure(
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )    
        self.create_sep_path_for_videos_audios_switch.configure(
            button_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            button_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            progress_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.create_sep_path_for_videos_audios_info_label.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.create_sep_path_for_qualities_switch.configure(
            button_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            button_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            progress_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.create_sep_path_for_qualities_info_label.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.create_sep_path_for_playlists_switch.configure(
            button_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            button_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            progress_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.create_sep_path_for_playlists_info_label.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.settings_reset_button.configure(
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        
    def update_widgets_accent_color(self):
        self.set_widgets_accent_color()

    def update_widgets_colors(self):
        """Update colors for the widgets."""

    def place_widgets(self):
        scale = AppearanceSettings.settings["scale_r"]
        pady = 16 * scale

        self.download_path_label.grid(row=0, column=0, padx=(100, 0), pady=(50, 0), sticky="w")
        self.dash1_label.grid(row=0, column=1, padx=(30, 30), pady=(50, 0), sticky="w")
        self.download_path_entry.grid(row=0, column=2, pady=(50, 0), sticky="w")
        self.download_path_choose_button.grid(row=0, column=3, pady=(50, 0), padx=(20, 0), sticky="w")
        
        self.create_sep_path_for_videos_audios_label.grid(row=1, column=0, padx=(100, 0), pady=(pady, 0), sticky="w")
        self.dash2_label.grid(row=1, column=1, padx=(30, 30), pady=(pady, 0), sticky="w")
        self.create_sep_path_for_videos_audios_switch.grid(row=1, column=2, padx=(0, 0), pady=(pady, 0), sticky="w")
        self.create_sep_path_for_videos_audios_info_label.grid(
            row=2, column=0, columnspan=4, padx=(100 + (20 * scale), 0), pady=(10, 0), sticky="w"
        )
        
        self.create_sep_path_for_qualities_label.grid(row=3, column=0, padx=(100, 0), pady=(pady, 0), sticky="w")
        self.dash3_label.grid(row=3, column=1, padx=(30, 30), pady=(pady, 0), sticky="w")
        self.create_sep_path_for_qualities_switch.grid(row=3, column=2, padx=(0, 0), pady=(pady, 0), sticky="w")
        self.create_sep_path_for_qualities_info_label.grid(
            row=4, column=0, columnspan=4, padx=(100 + (20 * scale), 0), pady=(10, 0), sticky="w"
        )
        
        self.create_sep_path_for_playlists_label.grid(row=5, column=0, padx=(100, 0), pady=(pady, 0), sticky="w")
        self.dash4_label.grid(row=5, column=1, padx=(30, 30), pady=(pady, 0), sticky="w")
        self.create_sep_path_for_playlists_switch.grid(row=5, column=2, padx=(0, 0), pady=(pady, 0), sticky="w")
        self.create_sep_path_for_playlists_info_label.grid(
            row=6, column=0, columnspan=4, padx=(100 + (20 * scale), 0), pady=(10, 0), sticky="w"
        )
        
        self.apply_changes_button.grid(
            row=7, column=2,
            columnspan=2,
            pady=(pady, 0), padx=(20 + 170 * scale, 0),
            sticky="w"
        )
        
        self.settings_reset_button.grid(
            row=8, column=2,
            columnspan=2,
            pady=(pady + 30*scale, 0), padx=(20 + 170 * scale, 0),
            sticky="w"
        )

    def set_widgets_sizes(self):
        scale = AppearanceSettings.settings["scale_r"]
        
        self.download_path_entry.configure(width=250 * scale, height=28 * scale)
        self.download_path_choose_button.configure(width=30 * scale, height=30 * scale)
        self.create_sep_path_for_videos_audios_switch.configure(switch_width=36 * scale, switch_height=18 * scale)
        self.create_sep_path_for_qualities_switch.configure(switch_width=36 * scale, switch_height=18 * scale)
        self.create_sep_path_for_playlists_switch.configure(switch_width=36 * scale, switch_height=18 * scale)
        self.apply_changes_button.configure(width=50 * scale, height=24 * scale)
        
        self.settings_reset_button.configure(width=80*scale, height=24 * scale)

    def set_widgets_texts(self):
        self.download_path_label.configure(
            text=LanguageManager.data["download_path"]
        )
        self.create_sep_path_for_videos_audios_label.configure(
            text=LanguageManager.data["separate_folders_for_audio_&_video"]
        )
        self.create_sep_path_for_videos_audios_info_label.configure(
            text=LanguageManager.data["separate_folders_for_audio_&_video_info"]
        )
        self.create_sep_path_for_qualities_label.configure(
            text=LanguageManager.data["quality-based_folder_organization"]
        )
        self.create_sep_path_for_qualities_info_label.configure(
            text=LanguageManager.data["quality-based_folder_organization_info"]
        )
        self.create_sep_path_for_playlists_label.configure(
            text=LanguageManager.data["playlist-specific_directories"]
        )
        self.create_sep_path_for_playlists_info_label.configure(
            text=LanguageManager.data["playlist-specific_directories_info"]
        )
        self.apply_changes_button.configure(
            text=LanguageManager.data["apply"]
        )
        self.settings_reset_button.configure(
            text=LanguageManager.data["reset"]
        )

    def update_widgets_text(self):
        self.set_widgets_texts()

    def set_widgets_fonts(self):
        scale = AppearanceSettings.settings["scale_r"]
        
        title_font = ("Segoe UI", 13 * scale, "bold")
        self.download_path_label.configure(font=title_font)
        self.dash1_label.configure(font=title_font)
        self.create_sep_path_for_videos_audios_label.configure(font=title_font)
        self.dash2_label.configure(font=title_font)
        self.create_sep_path_for_qualities_label.configure(font=title_font)
        self.dash3_label.configure(font=title_font)
        self.create_sep_path_for_playlists_label.configure(font=title_font)
        self.dash4_label.configure(font=title_font)

        value_font = ("Segoe UI", 13 * scale, "normal")
        self.download_path_entry.configure(font=value_font)
        self.create_sep_path_for_videos_audios_info_label.configure(font=value_font)
        self.create_sep_path_for_qualities_info_label.configure(font=value_font)
        self.create_sep_path_for_playlists_info_label.configure(font=value_font)

        button_font = ("Segoe UI", 13 * scale, "bold")
        self.apply_changes_button.configure(font=button_font)

        button_font2 = ("Segoe UI", 28 * scale, "bold")
        self.download_path_choose_button.configure(font=button_font2)
        
        self.settings_reset_button.configure(font=("Segoe UI", 11 * scale, "bold"))
