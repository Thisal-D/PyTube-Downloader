from typing import Any, List, Callable, Literal
import customtkinter as ctk
from widgets.components.accent_color_button import AccentColorButton
from services import ThemeManager, LanguageManager
from utils import SettingsValidateUtility
from settings import (
    AppearanceSettings
)


class AppearancePanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            theme_settings_change_callback: Callable = None,
            restart_callback: Callable = None):

        super().__init__(
            master=master,
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )

        self.theme_label = ctk.CTkLabel(
            master=self,
            text="Theme",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.dash1_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )

        self.theme_combo_box = ctk.CTkComboBox(
            master=self,
            values=[
                LanguageManager.data[AppearanceSettings.themes[0]],
                LanguageManager.data[AppearanceSettings.themes[1]]
            ],
            dropdown_fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            command=self.apply_theme_mode,
            width=140 * AppearanceSettings.settings["scale_r"],
            height=28 * AppearanceSettings.settings["scale_r"],
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )
        self.system_theme_check_box = ctk.CTkCheckBox(
            master=self,
            text="Sync with OS",
            command=self.sync_theme_with_os,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )

        self.accent_color_label = ctk.CTkLabel(
            master=self,
            text="Accent color",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.dash2_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.accent_color_frame = ctk.CTkFrame(
            master=self,
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )

        # add accent  color buttons
        self.accent_color_buttons: List[AccentColorButton] = []
        for accent_color in AppearanceSettings.settings["settings_panel"]["accent_colors"].values():
            button = AccentColorButton(
                master=self.accent_color_frame,
                text="",
                fg_color=accent_color["normal"],
                hover_color=accent_color["hover"],
                size_change=4,
                corner_radius=8,
            )
            button.configure(command=lambda btn=button: self.apply_accent_color(btn))
            self.accent_color_buttons.append(button)

        # add user custom accent color
        self.custom_accent_color_label = ctk.CTkLabel(
            master=self,
            text="Custom Accent color",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
        )
        self.dash3_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"]
        )
        self.custom_accent_color_entry = ctk.CTkEntry(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )

        self.custom_accent_color_display_btn = ctk.CTkButton(
            master=self,
            text="",
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            hover_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
        )

        self.custom_accent_color_apply_btn = ctk.CTkButton(
            master=self,
            text="Apply",
            state="disabled",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            command=self.apply_custom_accent_color
        )

        self.custom_accent_color_alert_text = ctk.CTkTextbox(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["warning_color"]["normal"],
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            activate_scrollbars=False,
        )

        self.scale_label = ctk.CTkLabel(
            master=self,
            text="Scale",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
        )

        self.dash4_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
        )

        self.scale_change_slider = ctk.CTkSlider(
            master=self,
            command=self.change_scale,
            number_of_steps=100,
            from_=100,
            to=200,
        )

        self.scale_apply_btn = ctk.CTkButton(
            master=self,
            text="Apply",
            state="disabled",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            command=self.ask_to_restart
        )

        self.scale_value_label = ctk.CTkLabel(
            master=self,
            text="",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
        )

        self.opacity_label = ctk.CTkLabel(
            master=self,
            text="Transparent",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
        )

        self.dash5_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
        )

        self.opacity_change_slider = ctk.CTkSlider(
            master=self,
            command=self.apply_opacity,
            from_=60,
            number_of_steps=320,
            to=100,
        )
        
        self.settings_reset_button = ctk.CTkButton(
            master=self, 
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"], 
            command=self.reset_settings
        )    

        # callbacks for settings changes
        self.restart_callback = restart_callback
        self.theme_settings_change_callback = theme_settings_change_callback

        self.set_widgets_fonts()
        self.set_widgets_texts()
        self.set_widgets_sizes()
        self.set_widgets_accent_color()
        self.place_widgets()
        self.bind_widgets_events()
        self.set_widgets_values()

        # Register widget with ThemeManager
        ThemeManager.register_widget(self)
        LanguageManager.register_widget(self)

    def cancel_scale_settings_resetting(self):
        self.scale_change_slider.set(AppearanceSettings.settings["scale"])
        self.scale_value_label.configure(text=f"{AppearanceSettings.settings["scale"]} %")
        
    def reset_settings(self):
        self.apply_theme_mode("Dark")
        self.theme_combo_box.set("Dark")
        
        if not self.accent_color_buttons[0].pressed:
            self.accent_color_buttons[0].on_mouse_enter_self('event')
            self.apply_accent_color(self.accent_color_buttons[0])
            
        self.scale_change_slider.set(100)
        self.apply_opacity(100)

        self.opacity_change_slider.set(100)
        self.scale_value_label.configure(text=f"{100.0} %")
        if AppearanceSettings.settings["scale"] != 100:
            from widgets import AlertWindow
            scale = AppearanceSettings.settings["scale_r"]
            AlertWindow(
                master=self.master.master,
                alert_msg="scale_settings_reset_confirmation",
                width=int(450 * scale),
                height=int(130 * scale),
                ok_button_display=True,
                cancel_button_display=True,
                ok_button_callback=self.apply_scale,
                cancel_button_callback=self.cancel_scale_settings_resetting
            )
        
    
    def release_all_accent_color_buttons(self):
        """
        Release all pressed accent color buttons.
        """
        for accent_button in self.accent_color_buttons:
            if accent_button.pressed:
                accent_button.set_unpressed()

    def apply_accent_color(self, button: AccentColorButton):
        """
        Apply selected accent color.
        """
        AppearanceSettings.settings["root"]["accent_color"] = {
            "normal": button.fg_color,
            "hover": button.hover_color,
            "default": True
        }
        self.theme_settings_change_callback("accent_color")
        self.release_all_accent_color_buttons()
        button.set_pressed()
        self.validate_custom_accent_color("event")

    def apply_custom_accent_color(self):
        """
        Apply custom accent color.
        """
        colors = self.custom_accent_color_entry.get().strip().replace(" ", "").split(",")
        AppearanceSettings.settings["root"]["accent_color"] = {
            "normal": colors[0],
            "hover": colors[1],
            "default": False
        }
        self.release_all_accent_color_buttons()
        self.theme_settings_change_callback("accent_color")
        self.custom_accent_color_apply_btn.configure(state="disabled")

    def apply_theme_mode(self, theme_mode: Literal["Dark", "Light", None]):
        """
        Apply selected theme mode. Dark / Light
        """
        AppearanceSettings.settings["root"]["theme_mode"] = self.theme_combo_box.cget("values").index(theme_mode)
        self.theme_settings_change_callback("theme_mode")

    def sync_theme_with_os(self):
        """
        Synchronize theme with the OS.
        """
        self.system_theme_check_box.configure(command=self.disable_sync_theme_with_os)
        self.theme_combo_box.configure(state="disabled")
        AppearanceSettings.settings["root"]["theme_mode"] = 2
        self.theme_settings_change_callback("theme_mode")

    def disable_sync_theme_with_os(self):
        """
        Disable synchronization with the OS.
        """
        self.system_theme_check_box.configure(command=self.sync_theme_with_os)
        self.theme_combo_box.configure(state="normal")
        AppearanceSettings.settings["root"]["theme_mode"] = (
            AppearanceSettings.themes.index(ctk.get_appearance_mode().lower())
        )
        self.theme_settings_change_callback("theme_mode")

    def apply_opacity(self, opacity_value: float):
        """
        Apply selected opacity value.
        """
        AppearanceSettings.settings["opacity"] = opacity_value
        AppearanceSettings.settings["opacity_r"] = opacity_value / 100
        self.theme_settings_change_callback("opacity")

    def change_scale(self, scale_value: int):
        """
        Change the scale value.
        """
        self.scale_value_label.configure(text=f"{scale_value} %")
        if scale_value != AppearanceSettings.settings["scale"]:
            self.scale_apply_btn.configure(state="normal")
        else:
            self.scale_apply_btn.configure(state="disabled")

    def ask_to_restart(self):
        from widgets import AlertWindow
        scale = AppearanceSettings.settings["scale_r"]
        AlertWindow(
            master=self.master.master,
            alert_msg="restart_confirmation",
            width=int(450 * scale),
            height=int(130 * scale),
            ok_button_display=True,
            cancel_button_display=True,
            ok_button_callback=self.apply_scale
        )

    def apply_scale(self):
        scale_value = self.scale_change_slider.get()
        AppearanceSettings.settings["scale"] = scale_value
        AppearanceSettings.settings["scale_r"] = scale_value / 100
        self.theme_settings_change_callback()
        self.restart_callback()

    def validate_custom_accent_color(self, _event):
        """
        Validate custom accent color entry.
        """
        text = self.custom_accent_color_entry.get()
        colors = text.strip().replace(" ", "")
        if SettingsValidateUtility.validate_accent_color(colors):
            fg_color = colors.split(",")[0]
            hover_color = colors.split(",")[1]
            self.custom_accent_color_display_btn.configure(
                fg_color=fg_color,
                hover_color=hover_color
            )
            self.custom_accent_color_entry.delete(0, "end")
            self.custom_accent_color_entry.insert("end", f"{fg_color}, {hover_color}")
            self.custom_accent_color_apply_btn.configure(state="normal")
        else:
            self.custom_accent_color_display_btn.configure(
                fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
                hover_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            )
            self.custom_accent_color_apply_btn.configure(state="disabled")

    def set_widgets_accent_color(self):
        """
        Set accent color for widgets.
        """
        self.theme_combo_box.configure(
            button_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            button_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            dropdown_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.custom_accent_color_entry.configure(
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.system_theme_check_box.configure(
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
        )
        self.custom_accent_color_apply_btn.configure(
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.opacity_change_slider.configure(
            button_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            progress_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            button_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
        )
        self.scale_change_slider.configure(
            button_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            progress_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
            button_hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"],
        )
        self.scale_apply_btn.configure(
            fg_color=AppearanceSettings.settings["root"]["accent_color"]["normal"],
            hover_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
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
        self.theme_label.grid(row=0, column=0, padx=(100, 0), pady=(50, 0), sticky="w")
        self.dash1_label.grid(row=0, column=1, padx=(30, 30), pady=(50, 0), sticky="w")
        self.theme_combo_box.grid(row=0, column=2, pady=(50, 0), sticky="w")
        self.system_theme_check_box.grid(row=0, column=3, padx=(20, 0), pady=(50, 0), sticky="w")

        self.accent_color_label.grid(row=1, column=0, padx=(100, 0), pady=(pady, 0), sticky="nw")
        self.dash2_label.grid(row=1, column=1, padx=(30, 30), pady=(pady, 0), sticky="nw")
        self.accent_color_frame.grid(row=1, column=2, pady=(pady, 0), sticky="w")
        
        # place accent color buttons
        max_columns = 3
        row = 0
        column = 0
        for button in self.accent_color_buttons:
            button.grid(row=row, column=column, padx=6, pady=6)
            column += 1
            if column > max_columns:
                column = 0
                row += 1
            button.bind_event()

        self.custom_accent_color_label.grid(row=2, column=0, padx=(100, 0), pady=(pady, 0), sticky="w")
        self.dash3_label.grid(row=2, column=1, padx=(30, 30), pady=(pady, 0), sticky="w")
        self.custom_accent_color_entry.grid(row=2, column=2, pady=(pady, 0), sticky="w")
        self.custom_accent_color_display_btn.grid(row=2, column=3, padx=(20, 0), pady=(pady, 0), sticky="w")
        self.custom_accent_color_apply_btn.grid(row=2, column=3, padx=(100 * scale, 0), pady=(pady, 0), sticky="w")
        self.custom_accent_color_alert_text.grid(row=3, column=0, columnspan=9, padx=(100, 0), pady=(10, 0), sticky="w")

        self.scale_label.grid(row=4, column=0, padx=(100, 0), pady=(pady, 0), sticky="w")
        self.dash4_label.grid(row=4, column=1, padx=(30, 30), pady=(pady, 0), sticky="w")
        self.scale_change_slider.grid(row=4, column=2, pady=(pady, 0), sticky="w")
        self.scale_value_label.grid(row=4, column=3, padx=(20, 0), pady=(pady, 0), sticky="w")
        self.scale_apply_btn.grid(row=4, column=3, padx=(100 * scale, 0), pady=(pady, 0), sticky="w")

        self.opacity_label.grid(row=5, column=0, padx=(100, 0), pady=(pady, 0), sticky="w")
        self.dash5_label.grid(row=5, column=1, padx=(30, 30), pady=(pady, 0), sticky="w")
        self.opacity_change_slider.grid(row=5, column=2, pady=(pady, 0), sticky="sw")
        
        self.settings_reset_button.grid(row=5, column=3, pady=(pady, 0), padx=(100, 0), sticky="w")
        

    def set_widgets_sizes(self):
        scale = AppearanceSettings.settings["scale_r"]
        self.theme_combo_box.configure(width=140 * scale, height=28 * scale)
        self.system_theme_check_box.configure(checkbox_width=24 * scale, checkbox_height=24 * scale)

        for accent_color_button in self.accent_color_buttons:
            accent_color_button.configure(width=30 * scale, height=30 * scale, corner_radius=6 * scale)
        self.custom_accent_color_display_btn.configure(width=30 * scale, height=30 * scale, corner_radius=6 * scale)
        self.custom_accent_color_entry.configure(width=140 * scale, height=28 * scale)
        self.custom_accent_color_apply_btn.configure(width=50 * scale, height=24 * scale)
        self.custom_accent_color_alert_text.configure(width=590 * scale, height=85 * scale)

        self.scale_change_slider.configure(width=180 * scale, height=18 * scale)
        self.scale_apply_btn.configure(width=50 * scale, height=24 * scale)
        self.opacity_change_slider.configure(width=180 * scale, height=18 * scale)
        
        self.settings_reset_button.configure(width=80*scale, height=24 * scale)

    def set_widgets_texts(self):
        self.theme_label.configure(text=LanguageManager.data["theme"])
        
        self.theme_combo_box.configure(
            values=[
                LanguageManager.data[AppearanceSettings.themes[0]],
                LanguageManager.data[AppearanceSettings.themes[1]]
            ]
        )
        
        if AppearanceSettings.settings["root"]["theme_mode"] != 2:
            self.theme_combo_box.set(
                self.theme_combo_box.cget("values")[AppearanceSettings.settings["root"]["theme_mode"]]
            )

        self.system_theme_check_box.configure(text=LanguageManager.data["sync_with_os"])
        self.accent_color_label.configure(text=LanguageManager.data["accent_color"])
        self.custom_accent_color_label.configure(
            text=LanguageManager.data["custom_accent_color"]
        )
        self.custom_accent_color_apply_btn.configure(text=LanguageManager.data["apply"])
        self.custom_accent_color_alert_text.delete(1.0, "end")
        self.custom_accent_color_alert_text.insert(
            "end",
            LanguageManager.data["custom_accent_color_alert_text"]
        )
        self.scale_label.configure(text=LanguageManager.data["scale"])
        self.scale_apply_btn.configure(text=LanguageManager.data["apply"])
        self.opacity_label.configure(text=LanguageManager.data["transparent"])
        self.settings_reset_button.configure(
            text=LanguageManager.data["reset"]
        )

    def update_widgets_text(self):
        self.set_widgets_texts()

    def set_widgets_fonts(self):
        # Segoe UI, Open Sans
        scale = AppearanceSettings.settings["scale_r"]
        title_font = ("Segoe UI", 13 * scale, "bold")
        self.theme_label.configure(font=title_font)
        self.dash1_label.configure(font=title_font)
        self.accent_color_label.configure(font=title_font)
        self.dash2_label.configure(font=title_font)
        self.custom_accent_color_label.configure(font=title_font)
        self.dash3_label.configure(font=title_font)
        self.scale_label.configure(font=title_font)
        self.dash4_label.configure(font=title_font)
        self.opacity_label.configure(font=title_font)
        self.dash5_label.configure(font=title_font)

        value_font = ("Segoe UI", 13 * scale, "normal")
        self.theme_combo_box.configure(font=value_font, dropdown_font=value_font)
        self.system_theme_check_box.configure(font=value_font)
        self.custom_accent_color_entry.configure(font=value_font)
        self.custom_accent_color_alert_text.configure(font=value_font)
        self.scale_value_label.configure(font=value_font)

        button_font = ("Segoe UI", 13 * scale, "bold")
        self.custom_accent_color_apply_btn.configure(font=button_font)
        self.scale_apply_btn.configure(font=button_font)
        
        self.settings_reset_button.configure(font=("Segoe UI", 11 * scale, "bold"))

    # set default values to widgets
    def set_widgets_values(self):
        """
        set values for widgets using saved settings.
        """
        self.custom_accent_color_alert_text.bind("<Key>", lambda e: "break")

        if AppearanceSettings.settings["root"]["accent_color"]["default"]:
            for button in self.accent_color_buttons:
                if button.fg_color == AppearanceSettings.settings["root"]["accent_color"]["normal"] and \
                        button.hover_color == AppearanceSettings.settings["root"]["accent_color"]["hover"]:
                    button.on_mouse_enter_self("event")
                    button.set_pressed()
        else:
            # add default value to entry using data
            self.custom_accent_color_entry.insert(
                "end",
                AppearanceSettings.settings["root"]["accent_color"]["normal"] +
                ", " + AppearanceSettings.settings["root"]["accent_color"]["hover"]
            )
            self.validate_custom_accent_color("event")
            self.custom_accent_color_apply_btn.configure(state="disabled")

        if AppearanceSettings.settings["root"]["theme_mode"] == 2:
            self.sync_theme_with_os()
            self.system_theme_check_box.select()
        elif AppearanceSettings.settings["root"]["theme_mode"] == 0:
            self.theme_combo_box.set(self.theme_combo_box.cget("values")[0])
        if AppearanceSettings.settings["root"]["theme_mode"] == 1:
            self.theme_combo_box.set(self.theme_combo_box.cget("values")[1])

        self.opacity_change_slider.set(AppearanceSettings.settings["opacity"])

        self.scale_change_slider.set(AppearanceSettings.settings["scale"])
        self.scale_value_label.configure(text=f"{AppearanceSettings.settings["scale"]} %")

    def bind_widgets_events(self):
        """
        Bind events to widgets.
        """
        self.custom_accent_color_entry.bind("<KeyRelease>", self.validate_custom_accent_color)
        self.validate_custom_accent_color("event")
