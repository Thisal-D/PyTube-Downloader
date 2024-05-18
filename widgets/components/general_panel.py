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
            text="Language",
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
        self.language_label.grid(row=0, column=0, padx=(100, 0), pady=(50, 0), sticky="w")
        self.dash1_label.grid(row=0, column=1, padx=(30, 30), pady=(50, 0), sticky="w")
        self.languages_combo_box.grid(row=0, column=2, pady=(50, 0), sticky="w")

    def set_widgets_sizes(self):
        scale = AppearanceSettings.settings["scale_r"]
        self.languages_combo_box.configure(width=140 * scale, height=28 * scale)

    def set_widgets_texts(self):
        self.language_label.configure(text=LanguageManager.data["language"])

    def update_widgets_text(self):
        self.set_widgets_texts()

    def set_widgets_fonts(self):
        # Segoe UI, Open Sans
        scale = AppearanceSettings.settings["scale_r"]
        title_font = ("Segoe UI", 13 * scale, "bold")
        self.language_label.configure(font=title_font)
        self.dash1_label.configure(font=title_font)

        value_font = ("Segoe UI", 13 * scale, "normal")
        self.languages_combo_box.configure(font=value_font, dropdown_font=value_font)

    # set default values to widgets
    def set_widgets_values(self):
        """
        set values for widgets using saved settings.
        """
        self.languages_combo_box.set(GeneralSettings.settings["language"])
