from typing import Any, List, Callable, Literal, Union
import customtkinter as ctk
from functions import validate_color
from .AccentColorButton import AccentColorButton
from services import ThemeManager


class AppearancePanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            theme_settings_change_callback: Callable = None,
            width: int = 0):

        super().__init__(
            width=width,
            master=master,
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"]
        )

        self.theme_label = ctk.CTkLabel(
            master=self,
            text="Theme",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )
        self.dash1_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )
        self.theme_combo_box = ctk.CTkComboBox(
            master=self,
            values=["Dark", "Light"],
            dropdown_fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"],
            command=self.apply_theme_mode,
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"],
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"]
        )
        self.system_theme_check_box = ctk.CTkCheckBox(
            master=self,
            text="Sync with OS",
            command=self.sync_theme_with_os,
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )

        self.accent_color_label = ctk.CTkLabel(
            master=self,
            text="Accent color",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )
        self.dash2_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )
        self.accent_color_frame = ctk.CTkFrame(
            master=self,
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"]
        )

        # add accent  color buttons
        self.accent_color_buttons: List[AccentColorButton] = []
        for accent_color in ThemeManager.theme_settings["settings_panel"]["accent_colors"].values():
            button = AccentColorButton(
                master=self.accent_color_frame,
                text="",
                fg_color=accent_color["normal"],
                hover_color=accent_color["hover"],
                size_change=4,
                height=30,
                width=30,
                corner_radius=8,
            )
            button.configure(command=lambda btn=button: self.apply_accent_color(btn))
            self.accent_color_buttons.append(button)

        # add user custom accent color
        self.custom_accent_color_label = ctk.CTkLabel(
            master=self,
            text="Custom Accent color",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"],
        )
        self.dash3_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"]
        )
        self.custom_accent_color_entry = ctk.CTkEntry(
            master=self,
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"],
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"]
        )

        self.custom_accent_color_display_btn = ctk.CTkButton(
            master=self,
            text="",
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"],
            hover_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"],
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"],
            height=30,
            width=30,
            corner_radius=8
        )

        self.custom_accent_color_apply_btn = ctk.CTkButton(
            master=self,
            text="Apply",
            state="disabled",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"],
            height=24,
            width=50,
            font=("arial", 12, "bold"),
            command=self.apply_custom_accent_color
        )

        self.custom_accent_color_warning_text = ctk.CTkTextbox(
            master=self,
            text_color=ThemeManager.theme_settings["settings_panel"]["warning_color"]["normal"],
            width=560,
            fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"],
        )
        
        self.opacity_label = ctk.CTkLabel(
            master=self,
            text="Transparent",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"],
        )
        
        self.dash4_label = ctk.CTkLabel(
            master=self,
            text=":",
            text_color=ThemeManager.theme_settings["settings_panel"]["text_color"],
        )
        
        self.opacity_change_slider = ctk.CTkSlider(
            master=self,
            command=self.apply_opacity,
            from_=0.6,
            to=1,
        )

        self.custom_accent_color = ""
        ThemeManager.theme_settings = ThemeManager.theme_settings
        self.theme_settings_change_callback = theme_settings_change_callback
        self.place_widgets()
        self.configure_values()
        self.bind_events()
        self.set_accent_color()
        ThemeManager.bind_widget(self)

    def release_all_accent_color_buttons(self):
        for accent_button in self.accent_color_buttons:
            if accent_button.pressed:
                accent_button.set_unpressed()

    def apply_accent_color(self, button: AccentColorButton):
        ThemeManager.theme_settings["root"]["accent_color"] = {
            "normal": button.fg_color,
            "hover": button.hover_color,
            "default": True
        }
        self.theme_settings_change_callback(ThemeManager.theme_settings, "accent_color")
        self.release_all_accent_color_buttons()
        button.set_pressed()
        self.custom_accent_color_apply_btn.configure(state="normal")

    def apply_custom_accent_color(self):
        colors = self.custom_accent_color_entry.get().strip().replace(" ", "").split(",")
        ThemeManager.theme_settings["root"]["accent_color"] = {
            "normal": colors[0],
            "hover": colors[1],
            "default": False
        }
        self.release_all_accent_color_buttons()
        self.theme_settings_change_callback(ThemeManager.theme_settings, "accent_color")
        self.custom_accent_color_apply_btn.configure(state="disabled")

    def apply_theme_mode(self, theme_mode: Union[Literal["Dark", "Light"], Any]):
        ThemeManager.theme_settings["root"]["theme_mode"] = theme_mode.lower()
        self.theme_settings_change_callback(ThemeManager.theme_settings, "theme_mode")

    def sync_theme_with_os(self):
        self.system_theme_check_box.configure(command=self.disable_sync_theme_with_os)
        self.theme_combo_box.configure(state="disabled")
        ThemeManager.theme_settings["root"]["theme_mode"] = "system"
        self.theme_settings_change_callback(ThemeManager.theme_settings, "theme_mode")

    def disable_sync_theme_with_os(self):
        self.system_theme_check_box.configure(command=self.sync_theme_with_os)
        self.theme_combo_box.configure(state="normal")
        ThemeManager.theme_settings["root"]["theme_mode"] = ctk.get_appearance_mode().lower()
        self.theme_settings_change_callback(ThemeManager.theme_settings, "theme_mode")
        
    def apply_opacity(self, opacity_value: float):
        ThemeManager.theme_settings["opacity"] = opacity_value
        self.theme_settings_change_callback(ThemeManager.theme_settings, "opacity")

    def validate_custom_accent_color(self, _event):
        text = self.custom_accent_color_entry.get()
        if self.custom_accent_color != text:
            self.custom_accent_color = text
            colors = text.strip().replace(" ", "")
            if validate_color(colors):
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
                    fg_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"],
                    hover_color=ThemeManager.theme_settings["root"]["fg_color"]["normal"],
                )
                self.custom_accent_color_apply_btn.configure(state="disabled")

    def set_accent_color(self):
        self.theme_combo_box.configure(
            button_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            button_hover_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"],
            border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            dropdown_hover_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"]
        )
        self.custom_accent_color_entry.configure(
            border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"]
        )
        self.system_theme_check_box.configure(
            fg_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            hover_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"],
            border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
        )
        self.custom_accent_color_apply_btn.configure(
            fg_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            hover_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"]
        )
        self.opacity_change_slider.configure(
            button_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            fg_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            progress_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"],
            button_hover_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"],
        )

    def update_accent_color(self):
        self.set_accent_color()

    def reset_widgets_colors(self):
        self.custom_accent_color_warning_text.tag_config(
            "normal", 
            foreground=ThemeManager.get_color_based_on_theme(ThemeManager.theme_settings["settings_panel"]["text_color"])
        )

    def place_widgets(self):
        self.theme_label.place(y=50, x=100)
        self.dash1_label.place(y=50, x=240)
        self.theme_combo_box.place(y=50, x=270)
        self.system_theme_check_box.place(y=50, x=440)

        self.accent_color_label.place(y=90, x=100)
        self.dash2_label.place(y=90, x=240)
        self.accent_color_frame.place(y=90, x=270)

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

        self.custom_accent_color_label.place(y=270, x=100)
        self.dash3_label.place(y=270, x=240)
        self.custom_accent_color_entry.place(y=270, x=270)
        self.custom_accent_color_display_btn.place(y=270, x=420)
        self.custom_accent_color_apply_btn.place(y=272, x=470)
        self.custom_accent_color_warning_text.place(y=300, x=50)
        
        self.opacity_label.place(y=430, x=100)
        self.dash4_label.place(y=430, x=240)
        self.opacity_change_slider.place(y=435, x=270)

    # set default values to widgets
    def configure_values(self):
        self.custom_accent_color_warning_text.bind("<Key>", lambda e: "break")
        self.custom_accent_color_warning_text.insert(
            "end",
            """*Please enter custom accent colors for normal and hover states in one of the following formats:
        - Hexadecimal format: #RRGGBB or #RGB (e.g., #0f0f0f, #0f0f0ff or #fff, #f0f ) 
        - Color names: Supported color names such as red, green, blue
        - Separate the two colors with a comma (,)
                :- Example:
                        : #0f0f0f, #0f0f0ff
                        : green, lightgreen"""
        )
        self.custom_accent_color_warning_text.tag_add("red", "2.31", "2.33")
        self.custom_accent_color_warning_text.tag_add("green", "2.33", "2.35")
        self.custom_accent_color_warning_text.tag_add("blue", "2.35", "2.37")
        self.custom_accent_color_warning_text.tag_add("red", "2.42", "2.43")
        self.custom_accent_color_warning_text.tag_add("green", "2.43", "2.44")
        self.custom_accent_color_warning_text.tag_add("blue", "2.44", "2.45")
        self.custom_accent_color_warning_text.tag_add("normal", "5.0", "7.43")

        self.custom_accent_color_warning_text.tag_config("red", foreground="#ff0000")
        self.custom_accent_color_warning_text.tag_config("green", foreground="#00ff00")
        self.custom_accent_color_warning_text.tag_config("blue", foreground="#0000ff")

        if ThemeManager.theme_settings["root"]["accent_color"]["default"]:
            for button in self.accent_color_buttons:
                if button.fg_color == ThemeManager.theme_settings["root"]["accent_color"]["normal"] and \
                        button.hover_color == ThemeManager.theme_settings["root"]["accent_color"]["hover"]:
                    button.on_mouse_enter_self("event")
                    button.set_pressed()
        else:
            # add default value to entry using settings
            self.custom_accent_color_entry.insert(
                "end",
                ThemeManager.theme_settings["root"]["accent_color"]["normal"] +
                ", " + ThemeManager.theme_settings["root"]["accent_color"]["hover"]
            )

        if ThemeManager.theme_settings["root"]["theme_mode"] == "system":
            self.sync_theme_with_os()
            self.system_theme_check_box.select()
        elif ThemeManager.theme_settings["root"]["theme_mode"] == "dark":
            self.theme_combo_box.set("Dark")
        if ThemeManager.theme_settings["root"]["theme_mode"] == "light":
            self.theme_combo_box.set("Light")
            
        self.opacity_change_slider.set(ThemeManager.theme_settings["opacity"])

    def bind_events(self):
        self.custom_accent_color_entry.bind("<KeyRelease>", self.validate_custom_accent_color)
        self.validate_custom_accent_color("event")