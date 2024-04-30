from typing import Any, Callable, Literal
import customtkinter as ctk
from services import (
    ThemeManager,
    GeneralSettings
)
from functions import validate_simultaneous_count


# noinspection PyTypeChecker
class NetworkPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            general_settings_change_callback: Callable = None,
            width: int = 0):

        super().__init__(
            width=width,
            master=master,
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"]
        )

        self.load_label = ctk.CTkLabel(
            master=self,
            text="Maximum Simultaneous Loads",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )
        self.dash1_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )
        self.simultaneous_load_entry = ctk.CTkEntry(
            master=self,
            justify="right",
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"],
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )

        self.simultaneous_load_range_label = ctk.CTkLabel(
            master=self,
            text="(1-10)",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )

        self.download_label = ctk.CTkLabel(
            master=self,
            text="Maximum Simultaneous Downloads",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )
        self.dash2_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )
        self.simultaneous_download_entry = ctk.CTkEntry(
            master=self,
            justify="right",
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"],
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )

        self.simultaneous_download_range_label = ctk.CTkLabel(
            master=self,
            text="(1-10)",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )

        self.automatic_download_label = ctk.CTkLabel(
            master=self,
            text="Automatic Video Download",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )

        self.dash3_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )

        self.switch_state = ctk.StringVar(value=None)
        self.automatic_download_switch = ctk.CTkSwitch(
            master=self,
            width=150,
            height=30,
            text="",
            command=self.change_automatic_download,
            onvalue="enable",
            offvalue="disable",
            variable=self.switch_state
        )

        # noinspection PyTypeChecker
        self.automatic_download_quality_combo_box = ctk.CTkComboBox(
            master=self,
            values=["Highest Quality", "Lowest Quality", "Audio Only"],
            dropdown_fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"],
            command=self.change_automatic_download_quality,
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"],
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"]
        )

        self.automatic_download_info_label = ctk.CTkLabel(
            master=self,
            text="• Download videos automatically after complete loading",
        )

        self.apply_changes_btn = ctk.CTkButton(
            master=self,
            text="Apply",
            state="disabled",
            height=24,
            width=50,
            command=self.apply_general_settings,
            font=("arial", 12, "bold"),
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )

        # use to track anything is changed or not
        self.automatic_download_state_changed: bool = False
        self.automatic_download_quality_changed: bool = False
        self.simultaneous_download_count_changed: bool = False
        self.simultaneous_load_count_changed: bool = False

        self.general_settings_change_callback = general_settings_change_callback
        self.set_accent_color()
        self.place_widgets()
        self.bind_widgets()
        self.configure_values()
        ThemeManager.bind_widget(self)

    def apply_general_settings(self):
        GeneralSettings.general_settings["simultaneous_loads"] = int(self.simultaneous_load_entry.get())
        GeneralSettings.general_settings["simultaneous_downloads"] = int(self.simultaneous_download_entry.get())
        GeneralSettings.general_settings["automatic_download"]["state"] = self.switch_state.get()
        GeneralSettings.general_settings["automatic_download"]["quality"] = self.automatic_download_quality_combo_box.get()
        self.general_settings_change_callback()
        self.apply_changes_btn.configure(state="disabled")

    def change_automatic_download_quality(self, quality: Literal["Highest Quality", "Lowest Quality", "Audio Only"]):
        if GeneralSettings.general_settings["automatic_download"]["quality"] != quality:
            self.automatic_download_quality_changed = True
        else:
            self.automatic_download_quality_changed = False
        self.set_apply_button_state()

    def change_automatic_download(self):
        if GeneralSettings.general_settings["automatic_download"]["state"] != self.switch_state.get():
            self.automatic_download_state_changed = True
        else:
            self.automatic_download_state_changed = False
        self.set_apply_button_state()

    def simultaneous_load_count_check(self, _event):
        value = self.simultaneous_load_entry.get()
        if validate_simultaneous_count(value) and int(value) != GeneralSettings.general_settings["simultaneous_loads"]:
            self.simultaneous_load_count_changed = True
        else:
            self.simultaneous_load_count_changed = False
        self.set_apply_button_state()

    def simultaneous_download_count_check(self, _event):
        value = self.simultaneous_download_entry.get()
        if (validate_simultaneous_count(value) and
                int(value) != GeneralSettings.general_settings["simultaneous_downloads"]):
            self.simultaneous_download_count_changed = True
        else:
            self.simultaneous_download_count_changed = False
        self.set_apply_button_state()

    def set_apply_button_state(self):
        if any((self.simultaneous_download_count_changed,
                self.simultaneous_load_count_changed,
                self.automatic_download_state_changed,
                self.automatic_download_quality_changed)):
            self.apply_changes_btn.configure(state="normal")
        else:
            self.apply_changes_btn.configure(state="disabled")

    def bind_widgets(self):
        self.simultaneous_load_entry.bind("<KeyRelease>", self.simultaneous_load_count_check)
        self.simultaneous_download_entry.bind("<KeyRelease>", self.simultaneous_download_count_check)

    # set default values to widgets
    def configure_values(self):
        self.simultaneous_load_entry.insert(
            "end",
            GeneralSettings.general_settings["simultaneous_loads"]
        )
        self.simultaneous_download_entry.insert(
            "end",
            GeneralSettings.general_settings["simultaneous_downloads"]
        )
        if GeneralSettings.general_settings["automatic_download"]["state"] == "enable":
            self.automatic_download_switch.select()
            self.switch_state.set("enable")
        else:
            self.switch_state.set("disable")
        
        self.automatic_download_quality_combo_box.set(GeneralSettings.general_settings["automatic_download"]["quality"])

    def update_accent_color(self):
        self.set_accent_color()

    def set_accent_color(self):
        self.apply_changes_btn.configure(
            fg_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            hover_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"]
        )
        self.simultaneous_load_entry.configure(
            border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
        )
        self.simultaneous_download_entry.configure(
            border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
        )
        self.automatic_download_info_label.configure(
            text_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
        )
        self.automatic_download_switch.configure(
            button_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            button_hover_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"],
            progress_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"]
        )
        self.automatic_download_quality_combo_box.configure(
            button_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            button_hover_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"],
            border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            dropdown_hover_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"]
        )

    def place_widgets(self):
        self.load_label.place(y=50, x=50)
        self.dash1_label.place(y=50, x=270)
        self.simultaneous_load_entry.place(y=50, x=300)
        self.simultaneous_load_range_label.place(y=50, x=450)

        self.download_label.place(y=100, x=50)
        self.dash2_label.place(y=100, x=270)
        self.simultaneous_download_entry.place(y=100, x=300)
        self.simultaneous_download_range_label.place(y=100, x=450)

        self.automatic_download_label.place(y=150, x=50)
        self.dash3_label.place(y=150, x=270)
        self.automatic_download_switch.place(y=150, x=300)
        self.automatic_download_quality_combo_box.place(y=150, x=380)
        self.automatic_download_info_label.place(x=70, y=180)

        self.apply_changes_btn.place(y=220, x=380)

    def reset_widgets_colors(self):
        ...
