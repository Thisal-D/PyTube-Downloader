import tkinter
import webbrowser
import customtkinter as ctk
from typing import List, Union, Tuple
from tkinter import PhotoImage
import pyperclip
from utils import (
    ValueConvertUtility,
)
from widgets.components.thumbnail_button import (
    ThumbnailButton,
)
from services import (
    ThemeManager, LanguageManager
)
from settings import (
    AppearanceSettings
)


class Video(ctk.CTkFrame):
    """A class representing a video widget."""

    default_thumbnails: Tuple[tkinter.PhotoImage, tkinter.PhotoImage] = (None, None)

    def __init__(
            self,
            root: ctk.CTk,
            master: Union[ctk.CTkFrame, ctk.CTkScrollableFrame],
            width: int = 0,
            height: int = 0,
            # video info
            video_url: str = "",
            video_title: str = "-------",
            channel: str = "-------",
            thumbnails: List[PhotoImage] = (None, None),
            channel_url: str = "-------",
            length: int = 0):

        super().__init__(
            master=master,
            height=height,
            width=width,
            border_width=1,
            corner_radius=8,
        )
        self.root = root
        self.master = master
        self.height: int = height
        self.width: int = width
        # video details
        self.video_url: str = video_url
        self.video_title: str = video_title
        self.channel: str = channel
        self.channel_url: str = channel_url
        self.length: int = length
        self.thumbnails: List[PhotoImage] = thumbnails
        # widgets
        self.info_frame: Union[ctk.CTkFrame, None] = None
        self.url_label: Union[ctk.CTkLabel, None] = None
        self.video_title_label: Union[ctk.CTkLabel, None] = None
        self.channel_btn: Union[ctk.CTkButton, None] = None
        self.video_length_label: Union[ctk.CTkLabel, None] = None
        self.thumbnail_btn: Union[ThumbnailButton, None] = None
        self.remove_btn: Union[ctk.CTkButton, None] = None

        from widgets import ContextMenu
        self.context_menu: Union['ContextMenu', None] = None
        # initialize the object
        self.create_widgets()
        self.set_widgets_texts()
        self.set_widgets_sizes()
        self.set_widgets_fonts()
        self.set_widgets_colors()
        self.set_tk_widgets_colors()
        self.set_widgets_accent_color()
        self.place_widgets()
        self.bind_widgets_events()

        # register to Theme Manger for accent color updates & widgets colors updates
        ThemeManager.register_widget(self)
        LanguageManager.register_widget(self)

    def set_video_data(self):
        """Display video data on widgets."""
        self.video_title_label.configure(text=f"{LanguageManager.data['title']} : {self.video_title}")
        self.channel_btn.configure(text=f"{LanguageManager.data['channel']} : {self.channel}", state="normal")
        self.url_label.configure(text=self.video_url)
        
        self.video_length_label.configure(text=ValueConvertUtility.convert_time(self.length))

        self.thumbnail_btn.stop_loading_animation()
        self.thumbnail_btn.configure_thumbnail(thumbnails=self.thumbnails)
        self.thumbnail_btn.configure(state="normal")

        def on_mouse_enter_thumbnail_btn(event):
            self.on_mouse_enter_self(event)
            self.thumbnail_btn.on_mouse_enter(event)

        def on_mouse_leave_thumbnail_btn(event):
            self.on_mouse_leave_self(event)
            self.thumbnail_btn.on_mouse_leave(event)

        self.thumbnail_btn.bind("<Enter>", on_mouse_enter_thumbnail_btn)
        self.thumbnail_btn.bind("<Leave>", on_mouse_leave_thumbnail_btn)
        self.video_length_label.bind("<Enter>", on_mouse_enter_thumbnail_btn)
        self.video_length_label.bind("<Leave>", on_mouse_leave_thumbnail_btn)

    def kill(self):
        """Destroy the widget."""
        ThemeManager.unregister_widget(self)
        self.pack_forget()
        self.destroy()

    def copy_url(self):
        pyperclip.copy(self.video_url)
        self.close_context_menu_directly("event")

    def open_in_web_browser(self):
        webbrowser.open(self.video_url)
        self.close_context_menu_directly("event")

    def remove(self):
        self.kill()
        self.close_context_menu_directly("event")

    def create_widgets(self):
        """Create widgets."""
        from widgets import ContextMenu

        self.thumbnail_btn = ThumbnailButton(
            master=self,
            state="disabled",
            command=lambda: webbrowser.open(self.video_url),
        )
        self.video_length_label = ctk.CTkLabel(master=self, text=ValueConvertUtility.convert_time(self.length))

        self.info_frame = ctk.CTkFrame(master=self)
        self.video_title_label = ctk.CTkLabel(master=self.info_frame, anchor="w")
        self.channel_btn = ctk.CTkButton(
            master=self.info_frame,
            anchor="w",
            command=lambda: webbrowser.open(self.channel_url),
            state="disabled",
            hover=False
        )
        self.url_label = ctk.CTkLabel(master=self.info_frame, anchor="w", text=self.video_url)
        self.remove_btn = ctk.CTkButton(master=self, command=self.kill, text="X", hover=False)

        self.context_menu = ContextMenu(
            master=self.root,
            options_texts=["copy_url", "open_in_browser", "remove"],
            options_commands=[
                self.copy_url,
                self.open_in_web_browser,
                self.remove
            ]
        )

    def set_widgets_texts(self):
        self.video_title_label.configure(
            text=f"{LanguageManager.data['title']} : {self.video_title}"
        )
        self.channel_btn.configure(
            text=f"{LanguageManager.data['channel']} : {self.channel}"
        )

    def update_widgets_text(self):
        self.set_widgets_texts()

    def set_widgets_fonts(self):
        """Set fonts for widgets."""
        scale = AppearanceSettings.settings["scale_r"]

        self.thumbnail_btn.configure(font=("arial", int(14 * scale), "bold"))
        self.video_length_label.configure(font=("arial", int(11 * scale), "bold"))

        self.video_title_label.configure(font=('arial', int(13 * scale), 'bold'))
        self.channel_btn.configure(font=('arial', int(13 * scale), 'bold'))
        font_style = ctk.CTkFont(family="arial", size=int(13 * scale), slant="italic", underline=True)
        self.url_label.configure(font=font_style)

        self.remove_btn.configure(font=("arial", 12 * scale, "bold"))
        self.context_menu.configure(font=("Segoe UI", 12 * scale, "bold"))

    def set_widgets_sizes(self):
        """Set sizes for widgets."""
        scale = AppearanceSettings.settings["scale_r"]

        self.video_length_label.configure(height=1, width=1)
        self.info_frame.configure(height=self.height-3)
        label_height = int((self.height - 2) / 3)
        self.video_title_label.configure(height=label_height, width=2)
        self.channel_btn.configure(height=label_height, width=2)
        self.url_label.configure(height=label_height, width=2)

        self.remove_btn.configure(width=22 * scale, height=22 * scale, border_spacing=0)
        self.context_menu.configure(
            width=int(120 * AppearanceSettings.settings["scale_r"]),
            height=int(80 * AppearanceSettings.settings["scale_r"]),
        )

    def set_widgets_accent_color(self):
        """Set accent color for widgets."""
        self.configure(border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        self.thumbnail_btn.configure(
            fg=(AppearanceSettings.settings["root"]["accent_color"]["normal"]),
        )
        self.url_label.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

    def update_widgets_accent_color(self):
        """Update accent color for widgets."""
        self.set_widgets_accent_color()

    def set_tk_widgets_colors(self):
        """Set colors for the Tk widgets."""
        self.thumbnail_btn.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
            ),
            disabledforeground=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["text_color"]["normal"]
            ),
            activebackground=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
            )
        )

    def update_widgets_colors(self):
        """Update colors for widgets."""
        self.set_tk_widgets_colors()

    def set_widgets_colors(self):
        """Set colors for widgets."""
        self.configure(fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"])
        self.info_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.video_length_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.video_title_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.channel_btn.configure(
            text_color=AppearanceSettings.settings["video_object"]["btn_text_color"]["normal"],
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.remove_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["error_color"]["normal"],
            text_color=AppearanceSettings.settings["video_object"]["remove_btn_text_color"]["normal"]
        )

    def on_mouse_enter_self(self, event):
        """Handle mouse enter event for self."""
        self.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"],
            border_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.thumbnail_btn.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["fg_color"]["hover"]
            )
        )
        self.info_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"],
        )
        self.channel_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"]
        )

    def on_mouse_leave_self(self, event):
        """Handle mouse leave event for self."""
        self.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.thumbnail_btn.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
            )
        )
        self.info_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
        )
        self.channel_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )

    def open_context_menu(self, _event):
        from widgets import ContextMenu
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        ContextMenu.close_all_menus()
        self.context_menu.set_open()
        self.context_menu.place(x=x-10, y=y-10)

    def close_context_menu_directly(self, _event):
        self.context_menu.set_closed()
        self.context_menu.place_forget()

    def close_context_menu(self, _event):
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        if (x <= self.context_menu.winfo_x() + 10 or
                x >= (self.context_menu.winfo_x() + self.context_menu.winfo_width() - 10) or
                y <= self.context_menu.winfo_y() + 10 or
                y >= (self.context_menu.winfo_y() + self.context_menu.winfo_height() - 10)):
            self.close_context_menu_directly("event")

    def bind_widgets_events(self):
        """Bind events for widgets."""

        self.bind("<Configure>", self.configure_widget_sizes)

        self.thumbnail_btn.bind("<Button-3>", self.open_context_menu)
        self.thumbnail_btn.bind("<Button-2>", self.open_context_menu)

        self.thumbnail_btn.bind("<Button-1>", self.close_context_menu_directly)
        self.context_menu.bind_widgets_events("<Leave>", self.close_context_menu)

        self.bind("<Enter>", self.on_mouse_enter_self)
        self.bind("<Leave>", self.on_mouse_leave_self)

        for child_widgets in self.winfo_children():
            child_widgets.bind("<Enter>", self.on_mouse_enter_self)
            child_widgets.bind("<Leave>", self.on_mouse_leave_self)

            try:
                sub_child_widget = None
                for sub_child_widget in child_widgets.winfo_children():
                    sub_child_widget.bind("<Enter>", self.on_mouse_enter_self)
                    sub_child_widget.bind("<Leave>", self.on_mouse_leave_self)
                try:
                    for sub_sub_child_widget in sub_child_widget.winfo_children():
                        sub_sub_child_widget.bind("<Enter>", self.on_mouse_enter_self)
                        sub_sub_child_widget.bind("<Leave>", self.on_mouse_leave_self)
                except Exception as error:
                    print(f"Video.py : {error}")
            except Exception as error:
                print(f"Video.py : {error}")

        def on_mouse_enter_channel_btn(event):
            self.channel_btn.configure(
                text_color=AppearanceSettings.settings["video_object"]["btn_text_color"]["hover"]
            )
            self.on_mouse_enter_self(event)

        def on_mouse_leave_channel_btn(_event):
            self.channel_btn.configure(
                text_color=AppearanceSettings.settings["video_object"]["btn_text_color"]["normal"]
            )

        self.channel_btn.bind("<Enter>", on_mouse_enter_channel_btn)
        self.channel_btn.bind("<Leave>", on_mouse_leave_channel_btn)

        def on_mouse_enter_remove_btn(event):
            self.remove_btn.configure(
                fg_color=AppearanceSettings.settings["video_object"]["error_color"]["hover"],
                text_color=AppearanceSettings.settings["video_object"]["remove_btn_text_color"]["hover"]
            )
            self.on_mouse_enter_self(event)

        def on_mouse_leave_remove_btn(event):
            self.remove_btn.configure(
                fg_color=AppearanceSettings.settings["video_object"]["error_color"]["normal"],
                text_color=AppearanceSettings.settings["video_object"]["remove_btn_text_color"]["normal"]
            )
            self.on_mouse_leave_self(event)

        self.remove_btn.bind("<Enter>", on_mouse_enter_remove_btn)
        self.remove_btn.bind("<Leave>", on_mouse_leave_remove_btn)

    def place_widgets(self):
        """Place widgets."""
        scale = AppearanceSettings.settings["scale_r"]

        thumbnail_width = int((self.height - 4) / 9 * 16)
        self.thumbnail_btn.place(x=5, y=1, width=thumbnail_width, height=self.height - 4)
        self.video_length_label.place(rely=1, x=thumbnail_width + 5, anchor="se", y=-2)

        self.info_frame.place(x=thumbnail_width + 10 * scale, y=1)

        self.video_title_label.place(x=0, rely=0.2, anchor="w")
        self.channel_btn.place(x=0, rely=0.5, anchor="w")
        self.url_label.place(x=0, rely=0.8, anchor="w")
        self.remove_btn.place(relx=1, x=-25 * scale, y=3 * scale)

    def configure_widget_sizes(self, _event):
        ...
