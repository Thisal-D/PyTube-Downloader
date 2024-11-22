import customtkinter as ctk
from typing import Callable, Any
from settings import AppearanceSettings, GeneralSettings
from services import LanguageManager, ThemeManager
from utils import JsonUtility


class GeneralPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            general_settings_change_callback: Callable = None):

        super().__init__(
            master=master,
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )

        self.language_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.dash1_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )

        self.language_data = JsonUtility.read_from_file("data\\languages.json")
        self.language_names = [language_name for language_name in self.language_data.keys()]
        self.languages_combo_box = ctk.CTkComboBox(
            master=self,
            values=self.language_names,
            dropdown_fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            command=self.apply_language,
            width=140 * AppearanceSettings.settings["scale_r"],
            height=28 * AppearanceSettings.settings["scale_r"],
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )
        
        self.shortcut_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.dash2_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.shortcut_frame = ctk.CTkScrollableFrame(
            master=self,
            scrollbar_fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )
        self.shortcut_keys_data = [
            {"desc": "toggle_settings", "key_strokes": [("Ctrl", ",")]},
            {"desc": "exit_settings", "key_strokes": [("Esc", )]},
            {"desc": "change_download_mode", "key_strokes": [("F6", ), ("Ctrl", "d")]},
            {"desc": "add_video_/_playlist", "key_strokes": [("Enter", )]},
            {"desc": "toggle_fullscreen", "key_strokes": [("F11", ), ("Alt", "Enter")]},
            {"desc": "minimize", "key_strokes": [("F9",), ("Ctrl", "n"), ("Ctrl", "↓")]},
            {"desc": "toggle_maximize", "key_strokes": [("F10",), ("Ctrl", "m"), ("Ctrl", "↑")]},
            {"desc": "quick_exit", "key_strokes": [("Ctrl", "q")]},
            {"desc": "force_exit", "key_strokes": [("Ctrl", "Alt", "q"), ("Ctrl", "Alt", "F4")]},
            {"desc": "minimize_to_tray", "key_strokes": [("F12", ), ("Ctrl", "Shift", "m"), ("Ctrl", "Shift", "n")]},
        ]
        
        self.shortcut_keys_widgets_info = []
        for skd in self.shortcut_keys_data:
            shortcut_keys_widgets_info_dict = {"label": ctk.CTkLabel(
                master=self.shortcut_frame,
                text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            ), "dash": ctk.CTkLabel(
                master=self.shortcut_frame,
                text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
                text=":"
            ), "key_frame": ctk.CTkFrame(
                master=self.shortcut_frame,
                fg_color="transparent"
            ), "buttons": []}
            for key_stroke in skd["key_strokes"]:
                shortcut_keys_widgets_info_dict["buttons"].append(
                    ctk.CTkButton(
                        master=shortcut_keys_widgets_info_dict["key_frame"],
                        text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
                        fg_color="transparent",
                        border_width=1,
                        hover=False,
                        border_color=("#505050", "#808080"),
                        text=" + ".join(key_stroke),
                        corner_radius=8
                    )
                )
            self.shortcut_keys_widgets_info.append(shortcut_keys_widgets_info_dict)
        
        self.settings_reset_button = ctk.CTkButton(master=self, text_color=AppearanceSettings.settings["settings_panel"]["text_color"], command=self.reset_settings)    
        
        # callbacks for settings changes
        self.general_settings_change_callback = general_settings_change_callback
        
        self.set_widgets_fonts()
        self.set_widgets_texts()
        self.set_widgets_sizes()
        self.set_widgets_accent_color()
        self.place_widgets()
        self.set_widgets_values()

        # Register widget with ThemeManager
        ThemeManager.register_widget(self)
        LanguageManager.register_widget(self)
    
    def reset_settings(self):
        # Reset language to english and apply it
        self.languages_combo_box.set("English")
        self.apply_language("English")
        
    def apply_language(self, language: str) -> None:
        lang_code = self.language_data[language]
        if lang_code != GeneralSettings.settings["lang_code"]:
            GeneralSettings.settings["lang_code"] = lang_code
            GeneralSettings.settings["language"] = language
            self.general_settings_change_callback(updated="language")

    def set_widgets_accent_color(self):
        """
        Set accent color for widgets.
        """
        self.languages_combo_box.configure(
            button_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            button_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            dropdown_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.settings_reset_button.configure(
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )

    def update_widgets_accent_color(self):
        """
        Update accent color.
        """
        self.set_widgets_accent_color()

    def update_widgets_colors(self):
        """Update colors for the widgets."""

    def place_widgets(self):
        """
        Place widgets on the frame.
        """
        scale = AppearanceSettings.settings["scale_r"]
        pady = 16 * scale
        
        self.language_label.grid(row=0, column=0, padx=(100, 0), pady=(50, 0), sticky="w")
        self.dash1_label.grid(row=0, column=1, padx=(30, 30), pady=(50, 0), sticky="w")
        self.languages_combo_box.grid(row=0, column=2, pady=(50, 0), sticky="w")

        self.shortcut_label.grid(row=1, column=0, padx=(100, 0), pady=(pady, 0), sticky="nw")
        self.dash2_label.grid(row=1, column=1, padx=(30, 30), pady=(pady, 0), sticky="nw")
        self.shortcut_frame.grid(row=1, column=2, pady=(2, 0), sticky="w")
        
        for i, shortcut_widget_info in enumerate(self.shortcut_keys_widgets_info):
            shortcut_widget_info["label"].grid(row=i, column=0, pady=(4 * scale, 0), sticky="e")
            shortcut_widget_info["dash"].grid(
                row=i, column=1,
                padx=(15 * scale, 15 * scale), pady=(4 * scale, 0), sticky="w"
            )
            shortcut_widget_info["key_frame"].grid(row=i, column=2, pady=(4 * scale, 0), sticky="w")
            for button in shortcut_widget_info["buttons"]:
                button.pack(side="left", padx=(2 * scale, 0))
                
        self.settings_reset_button.grid(row=2, column=2, padx=(100, 0), pady=(pady, 0), sticky="e")
        
    def set_widgets_sizes(self):
        scale = AppearanceSettings.settings["scale_r"]
        self.languages_combo_box.configure(width=140 * scale, height=28 * scale)
        self.shortcut_frame.configure(width=450 * scale, height=252 * scale)
        self.shortcut_frame._scrollbar.grid_forget()
        
        for shortcut_widget_info in self.shortcut_keys_widgets_info:
            for button in shortcut_widget_info["buttons"]:
                button.configure(width=1, height=24 * scale)

        self.settings_reset_button.configure(width=80*scale, height=24 * scale)
        
    def set_widgets_texts(self):
        self.language_label.configure(text=LanguageManager.data["language"])
        self.shortcut_label.configure(text=LanguageManager.data["shortcuts"])

        for i, shortcut_widget_info in enumerate(self.shortcut_keys_widgets_info):
            shortcut_widget_info["label"].configure(text=LanguageManager.data[self.shortcut_keys_data[i]["desc"]])
            
        self.settings_reset_button.configure(
            text=LanguageManager.data["reset"]
        )
        
    def update_widgets_text(self):
        self.set_widgets_texts()

    def set_widgets_fonts(self):
        # Segoe UI, Open Sans
        scale = AppearanceSettings.settings["scale_r"]
        title_font = ("Segoe UI", 13 * scale, "bold")
        self.language_label.configure(font=title_font)
        self.dash1_label.configure(font=title_font)
        self.shortcut_label.configure(font=title_font)
        self.dash2_label.configure(font=title_font)

        value_font = ("Segoe UI", 13 * scale, "normal")
        self.languages_combo_box.configure(font=value_font, dropdown_font=value_font)
        
        value_font = ("Segoe UI", 11 * scale, "bold")
        for shortcut_widget_info in self.shortcut_keys_widgets_info:
            shortcut_widget_info["label"].configure(font=value_font)
            shortcut_widget_info["dash"].configure(font=value_font)
                
        value_font = ("Segoe UI", 11 * scale, "normal")
        for shortcut_widget_info in self.shortcut_keys_widgets_info:
            for button in shortcut_widget_info["buttons"]:
                button.configure(font=value_font)
                
        self.settings_reset_button.configure(font=("Segoe UI", 11 * scale, "bold"))
        

    # set default values to widgets
    def set_widgets_values(self):
        """
        set values for widgets using saved settings.
        """
        self.languages_combo_box.set(GeneralSettings.settings["language"])
