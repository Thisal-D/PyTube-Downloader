import tkinter as tk
import webbrowser
import customtkinter as ctk
from typing import Any, Union
from services import ThemeManager
from settings import ThemeSettings


class PlayList(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None,
            width: int = 0,
            height: int = 0,
            # playlist info
            channel_url: str = "-------",
            playlist_url: str = "-------",
            playlist_title: str = "-------",
            channel: str = "-------",
            playlist_video_count: int = 0):

        super().__init__(
            master=master,
            width=width,
        )

        self.height: int = height
        self.width: int = width
        # playlist info
        self.channel_url: str = channel_url
        self.channel: str = channel
        self.playlist_url: str = playlist_url
        self.playlist_title: str = playlist_title
        self.playlist_video_count = playlist_video_count
        # widgets
        self.playlist_info_widget: Union[ctk.CTkFrame, None] = None
        self.view_btn: Union[ctk.CTkButton, None] = None
        self.title_label: Union[tk.Label, None] = None
        self.channel_btn: Union[tk.Button, None] = None
        self.url_label: Union[ctk.CTkLabel, None] = None
        self.remove_btn: Union[ctk.CTkButton, None] = None
        self.playlist_video_count_label: Union[ctk.CTkLabel, None] = None
        self.playlist_item_frame: Union[ctk.CTkFrame, None] = None
        # self.on_mouse_state: Literal["enter", "leave"] = "leave"
        # initialize the object
        self.create_widgets()
        self.set_widgets_colors()
        self.reset_widgets_colors()
        self.set_accent_color()
        self.place_widgets()
        self.bind_widget_events()
        # self append to theme manger
        ThemeManager.register_widget(self)

    def hide_videos(self):
        self.view_btn.configure(
            command=self.view_videos,
            text=">",
            font=('arial', 18, 'bold')
        )
        self.playlist_item_frame.pack_forget()

    def view_videos(self):
        self.view_btn.configure(
            command=self.hide_videos,
            text="V",
            font=('arial', 13, 'bold')
        )
        self.playlist_item_frame.pack(padx=10, fill="x", pady=2)

    def set_playlist_data(self):
        self.playlist_video_count_label.configure(text=f"{self.playlist_video_count}")
        self.title_label.configure(text=f"Title : {self.playlist_title}")
        self.channel_btn.configure(text=f"Channel : {self.channel}")
        self.url_label.configure(text=self.playlist_url)
        self.channel_btn.configure(state="normal")

    def kill(self):
        ThemeManager.unregister_widget(self)
        self.pack_forget()
        self.destroy()

    def create_widgets(self):
        self.playlist_info_widget = ctk.CTkFrame(
            master=self,
            border_width=1,
            height=self.height,
            width=self.width
        )

        self.view_btn = ctk.CTkButton(
            master=self.playlist_info_widget,
            font=('arial', 18, 'bold'),
            text=">",
            width=1,
            height=1,
            hover=False,
            command=self.view_videos,
            state="disabled",
            cursor="hand2",
        )

        self.title_label = tk.Label(
            master=self.playlist_info_widget,
            anchor="w",
            font=('arial', 10, 'bold'),
            text=f"Title : {self.playlist_title}"
        )

        self.channel_btn = tk.Button(
            master=self.playlist_info_widget,
            font=('arial', 9, 'bold'),
            anchor="w",
            bd=0,
            command=lambda: webbrowser.open(self.channel_url),
            relief="sunken",
            state="disabled",
            cursor="hand2",
            text=f"Channel : {self.channel}"
        )

        self.url_label = tk.Label(
            master=self.playlist_info_widget, anchor="w",
            font=('arial', 11, "italic underline"),
            text=self.playlist_url,
        )

        self.remove_btn = ctk.CTkButton(
            master=self.playlist_info_widget,
            command=self.kill,
            text="X",
            font=("arial", 12, "bold"),
            width=12, height=20,
            border_spacing=0,
            hover=False,
        )

        self.playlist_video_count_label = ctk.CTkLabel(
            master=self.playlist_info_widget,
            width=15, height=15,
            font=("arial", 13, "bold"),
            justify="right",
            text=f"{self.playlist_video_count}"
        )

        self.playlist_item_frame = ctk.CTkFrame(
            master=self,
        )

        self.bind("<Configure>", self.configure_widget_sizes)

    # configure widgets colors
    def set_accent_color(self):
        self.playlist_info_widget.configure(
            border_color=ThemeSettings.settings["root"]["accent_color"]["normal"]
        )
        self.view_btn.configure(text_color=ThemeSettings.settings["root"]["accent_color"]["normal"])
        self.url_label.configure(
            fg=ThemeSettings.settings["root"]["accent_color"]["normal"]
        )

    def update_accent_color(self):
        self.set_accent_color()

    def reset_widgets_colors(self):
        self.title_label.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(ThemeSettings.settings["video_object"]["fg_color"]["normal"]),
            fg=ThemeManager.get_color_based_on_theme_mode(
                ThemeSettings.settings["video_object"]["text_color"]["normal"]
            )
        )
        self.channel_btn.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(ThemeSettings.settings["video_object"]["fg_color"]["normal"]),
            fg=ThemeManager.get_color_based_on_theme_mode(
                ThemeSettings.settings["video_object"]["text_color"]["normal"]
            ),
            activeforeground=ThemeManager.get_color_based_on_theme_mode(
                ThemeSettings.settings["video_object"]["text_color"]["hover"]),
        )
        self.url_label.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(ThemeSettings.settings["video_object"]["fg_color"]["normal"]),
            fg=ThemeManager.get_color_based_on_theme_mode(
                ThemeSettings.settings["video_object"]["text_color"]["normal"]
            )
        )

    def set_widgets_colors(self):
        self.configure(
            fg_color=self.master.cget("fg_color")
        )
        self.playlist_item_frame.configure(
            fg_color=self.master.cget("fg_color")
        )
        self.playlist_info_widget.configure(
            fg_color=ThemeSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.view_btn.configure(
            fg_color=ThemeSettings.settings["video_object"]["fg_color"]["normal"],
        )
        self.playlist_info_widget.configure(
            fg_color=ThemeSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.view_btn.configure(
            fg_color=ThemeSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.remove_btn.configure(
            fg_color=ThemeSettings.settings["video_object"]["error_color"]["normal"],
            text_color=ThemeSettings.settings["video_object"]["remove_btn_text_color"]["normal"]
        )
        self.playlist_video_count_label.configure(
            text_color=ThemeSettings.settings["video_object"]["text_color"]["normal"]
        )

    def on_mouse_enter_self(self, event):
        # self.on_mouse_state = "enter"
        self.playlist_info_widget.configure(
            fg_color=ThemeSettings.settings["video_object"]["fg_color"]["hover"],
            border_color=ThemeSettings.settings["root"]["accent_color"]["hover"]
        )
        self.view_btn.configure(
            fg_color=ThemeSettings.settings["video_object"]["fg_color"]["hover"],
        )
        self.title_label.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(ThemeSettings.settings["video_object"]["fg_color"]["hover"])
        )
        self.channel_btn.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(ThemeSettings.settings["video_object"]["fg_color"]["hover"])
        )
        self.url_label.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(ThemeSettings.settings["video_object"]["fg_color"]["hover"])
        )

        # disable due to ui performance
        """def on_mouse_enter_videos():
            video_object: AddedVideo
            for video_object in self.playlist_item_frame.winfo_children():
                if type(video_object) is AddedVideo or \
                        type(video_object) is DownloadingVideo or \
                        type(video_object) is DownloadedVideo:
                    if self.on_mouse_state == "enter":
                        video_object.on_mouse_enter_self(event)
                    else:
                        break
        threading.Thread(target=on_mouse_enter_videos).start()"""

    def on_mouse_leave_self(self, event):
        # self.on_mouse_state = "leave"
        self.playlist_info_widget.configure(
            fg_color=ThemeSettings.settings["video_object"]["fg_color"]["normal"],
            border_color=ThemeSettings.settings["root"]["accent_color"]["normal"]
        )
        self.view_btn.configure(
            fg_color=ThemeSettings.settings["video_object"]["fg_color"]["normal"],
        )
        self.title_label.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(ThemeSettings.settings["video_object"]["fg_color"]["normal"])
        )
        self.channel_btn.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(ThemeSettings.settings["video_object"]["fg_color"]["normal"])
        )
        self.url_label.configure(
            bg=ThemeManager.get_color_based_on_theme_mode(ThemeSettings.settings["video_object"]["fg_color"]["normal"])
        )

        # disable due to ui performance
        """def on_mouse_leave_videos():
            video_object: AddedVideo
            for video_object in self.playlist_item_frame.winfo_children():
                if type(video_object) is AddedVideo or \
                        type(video_object) is DownloadingVideo or \
                        type(video_object) is DownloadedVideo:
                    if self.on_mouse_state == "leave":
                        video_object.on_mouse_leave_self(event)
                    else:
                        break
        threading.Thread(target=on_mouse_leave_videos).start()"""

    def bind_widget_events(self):
        self.playlist_info_widget.bind("<Enter>", self.on_mouse_enter_self)
        self.playlist_info_widget.bind("<Leave>", self.on_mouse_leave_self)
        for child_widgets in self.playlist_info_widget.winfo_children() + self.playlist_item_frame.winfo_children():
            child_widgets.bind("<Enter>", self.on_mouse_enter_self)
            child_widgets.bind("<Leave>", self.on_mouse_leave_self)
            try:
                for sub_child_widgets in child_widgets.winfo_children():
                    sub_child_widgets.bind("<Enter>", self.on_mouse_enter_self)
                    sub_child_widgets.bind("<Leave>", self.on_mouse_leave_self)
            except Exception as error:
                print(f"1@PlayList.py > Err : {error}")
                pass

        def on_mouse_enter_channel_btn(event):
            self.channel_btn.configure(
                fg=ThemeManager.get_color_based_on_theme_mode(
                    ThemeSettings.settings["video_object"]["btn_text_color"]["hover"]
                ),
            )
            self.on_mouse_enter_self(event)

        def on_mouse_leave_channel_btn(_event):
            self.channel_btn.configure(
                fg=ThemeManager.get_color_based_on_theme_mode(
                    ThemeSettings.settings["video_object"]["btn_text_color"]["normal"]
                ),
            )

        self.channel_btn.bind("<Enter>", on_mouse_enter_channel_btn)
        self.channel_btn.bind("<Leave>", on_mouse_leave_channel_btn)

        def on_mouse_enter_remove_btn(event):
            self.remove_btn.configure(
                fg_color=ThemeSettings.settings["video_object"]["error_color"]["hover"],
                text_color=ThemeSettings.settings["video_object"]["remove_btn_text_color"]["hover"]
            )
            self.on_mouse_enter_self(event)

        def on_mouse_leave_remove_btn(_event):
            self.remove_btn.configure(
                fg_color=ThemeSettings.settings["video_object"]["error_color"]["normal"],
                text_color=ThemeSettings.settings["video_object"]["remove_btn_text_color"]["normal"]
            )

        self.remove_btn.bind("<Enter>", on_mouse_enter_remove_btn)
        self.remove_btn.bind("<Leave>", on_mouse_leave_remove_btn)

    # place widgets
    def place_widgets(self):
        self.playlist_info_widget.pack(fill="x")
        self.view_btn.place(y=55, x=10)
        self.title_label.place(x=50, y=10, height=20, width=-420, relwidth=1)
        self.channel_btn.place(x=50, y=34, height=20, width=-420, relwidth=1)
        self.url_label.place(x=50, y=54, height=20, width=-420, relwidth=1)
        self.playlist_video_count_label.place(relx=1, x=-40, rely=1, y=-25)
        self.remove_btn.place(relx=1, x=-25, y=3)

    # configure widgets sizes and place location depend on root width
    def configure_widget_sizes(self, e):
        ...
