import webbrowser
import customtkinter as ctk
from typing import Union, List
from services import ThemeManager, LanguageManager
from settings import AppearanceSettings


class PlayList(ctk.CTkFrame):
    """
    A custom Tkinter frame for displaying information about a playlist.

    Args:
        master (Optional): The parent widget.
        width (int): The width of the frame.
        height (int): The height of the frame.
        channel_url (str): The URL of the channel.
        playlist_url (str): The URL of the playlist.
        playlist_title (str): The title of the playlist.
        channel (str): The name of the channel.
        playlist_video_count (int): The number of videos in the playlist.
    """
    
    def __init__(
            self,
            root: ctk.CTk = None,
            master: ctk.CTkScrollableFrame = None,
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
        
        # Initialize attributes
        self.root = root
        self.master_frame = master
        self.height: int = height
        self.width: int = width
        
        # playlist info
        self.channel_url: str = channel_url
        self.channel: str = channel
        self.playlist_url: str = playlist_url
        self.playlist_title: str = playlist_title
        self.playlist_video_count = playlist_video_count

        # widgets
        self.view_btn: Union[ctk.CTkButton, None] = None

        self.info_frame: Union[ctk.CTkFrame, None] = None
        self.playlist_title_label: Union[ctk.CTkLabel, None] = None
        self.channel_btn: Union[ctk.CTkButton, None] = None
        self.url_label: Union[ctk.CTkLabel, None] = None

        self.playlist_main_frame: Union[ctk.CTkFrame, None] = None

        self.remove_btn: Union[ctk.CTkButton, None] = None
        self.playlist_video_count_label: Union[ctk.CTkLabel, None] = None
        self.playlist_item_frame: Union[ctk.CTkFrame, None] = None
        
        self.videos: List = []
        # Create and configure widgets
        self.create_widgets()
        self.set_widgets_texts()
        self.set_widgets_sizes()
        self.set_widgets_fonts()
        self.set_widgets_colors()
        self.set_tk_widgets_colors()
        self.set_widgets_accent_color()
        self.place_widgets()
        self.bind_widgets_events()

        # Register to Theme Manager for accent color updates & widgets colors updates
        ThemeManager.register_widget(self)
        LanguageManager.register_widget(self)

    def hide_videos(self):
        """Hide the videos in the playlist."""
        self.view_btn.configure(
            command=self.view_videos,
            text=">",
            font=('arial', 18 * AppearanceSettings.settings["scale_r"], 'bold')
        )
        self.playlist_item_frame.pack_forget()

    def view_videos(self):
        """View the videos in the playlist."""
        self.view_btn.configure(
            command=self.hide_videos,
            text="V",
            font=('arial', 13 * AppearanceSettings.settings["scale_r"], 'bold')
        )
        self.playlist_item_frame.pack(padx=10, fill="x", pady=2)

    def set_playlist_data(self):
        """Set the data of the playlist."""
        self.playlist_video_count_label.configure(text=f"{self.playlist_video_count}")
        self.playlist_title_label.configure(text=f"{LanguageManager.data['title']} : {self.playlist_title}")
        self.channel_btn.configure(text=f"{LanguageManager.data['channel']} : {self.channel}")
        self.url_label.configure(text=self.playlist_url)
        self.channel_btn.configure(state="normal")

    def create_widgets(self):
        """Create widgets for the playlist."""
        self.playlist_main_frame = ctk.CTkFrame(master=self)
        self.view_btn = ctk.CTkButton(
            master=self.playlist_main_frame,
            text=">",
            hover=False,
            command=self.view_videos,
            state="disabled",
            cursor="hand2",
        )
        self.info_frame = ctk.CTkFrame(master=self.playlist_main_frame)
        self.playlist_title_label = ctk.CTkLabel(
            master=self.info_frame, anchor="w"
        )
        self.channel_btn = ctk.CTkButton(
            master=self.info_frame,
            anchor="w",
            command=lambda: webbrowser.open(self.channel_url),
            state="disabled",
            hover=False,
        )
        self.url_label = ctk.CTkLabel(master=self.info_frame, anchor="w", text=self.playlist_url)

        self.remove_btn = ctk.CTkButton(master=self.playlist_main_frame, command=self.kill, text="X", hover=False)
        self.playlist_video_count_label = ctk.CTkLabel(
            master=self.playlist_main_frame,
            justify="right",
            text=f"{self.playlist_video_count}"
        )
        self.playlist_item_frame = ctk.CTkFrame(master=self)

    def set_widgets_texts(self):
        self.playlist_title_label.configure(text=f"{LanguageManager.data['title']} : {self.playlist_title}")
        self.channel_btn.configure(text=f"{LanguageManager.data['channel']} : {self.channel}")

    def update_widgets_text(self):
        self.set_widgets_texts()

    def set_widgets_fonts(self):
        """Set fonts for the widgets."""
        scale = AppearanceSettings.settings["scale_r"]

        self.view_btn.configure(font=('arial', 18 * scale, 'bold'),)
        self.playlist_title_label.configure(font=('arial', int(14 * scale), 'bold'))
        self.channel_btn.configure(font=('arial', int(14 * scale), 'bold'))
        font_style = ctk.CTkFont(family="arial", size=int(14 * scale), slant="italic", underline=True)
        self.url_label.configure(font=font_style)
        self.remove_btn.configure(font=("arial", 12 * scale, "bold"),)
        self.playlist_video_count_label.configure(font=("arial", 13 * scale, "bold"))

    def set_widgets_sizes(self):
        """Set sizes for the widgets."""
        scale = AppearanceSettings.settings["scale_r"]

        self.playlist_main_frame.configure(border_width=1, height=self.height, width=self.width)
        self.view_btn.configure(width=1, height=1)
        self.info_frame.configure(height=self.height-3)
        label_height = int((self.height - 2) / 3)
        self.playlist_title_label.configure(height=label_height)
        self.channel_btn.configure(height=label_height)
        self.url_label.configure(height=label_height)
        self.remove_btn.configure(width=22 * scale, height=22 * scale, border_spacing=0)
        self.playlist_video_count_label.configure(width=15 * scale, height=15 * scale)

    def set_widgets_accent_color(self):
        """Set accent color for the widgets."""
        self.playlist_main_frame.configure(
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.view_btn.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        self.url_label.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )

    def update_widgets_accent_color(self):
        """Update accent color for the widgets."""
        self.set_widgets_accent_color()

    def set_tk_widgets_colors(self):
        """Set colors for the Tk widgets."""
        self.playlist_title_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )
        self.channel_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"],
        )
        self.url_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )

    def update_widgets_colors(self):
        """Update colors for the widgets."""
        self.set_tk_widgets_colors()

    def set_widgets_colors(self):
        """Set colors for the widgets."""
        self.configure(
            fg_color=self.master_frame.cget("fg_color")
        )
        self.playlist_item_frame.configure(
            fg_color=self.master_frame.cget("fg_color")
        )
        self.playlist_main_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.info_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.view_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
        )
        self.playlist_main_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.view_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.remove_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["error_color"]["normal"],
            text_color=AppearanceSettings.settings["video_object"]["remove_btn_text_color"]["normal"]
        )
        self.playlist_video_count_label.configure(
            text_color=AppearanceSettings.settings["video_object"]["text_color"]["normal"]
        )

    def on_mouse_enter_self(self, event):
        """Handle mouse enter event for the widget."""
        """
        self.playlist_main_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"],
            border_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]
        )
        self.info_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"]
        )
        self.view_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["hover"],
        )
        self.channel_btn.configure(
            fg_color=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["fg_color"]["hover"]
            )
        )
        """
        # disable due to ui performance issue
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
        """Handle mouse leave event for the widget."""
        """
        self.playlist_main_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
            border_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]
        )
        self.info_frame.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
        )
        self.view_btn.configure(
            fg_color=AppearanceSettings.settings["video_object"]["fg_color"]["normal"],
        )
        self.channel_btn.configure(
            fg_color=ThemeManager.get_color_based_on_theme_mode(
                AppearanceSettings.settings["video_object"]["fg_color"]["normal"]
            )
        )
        """

        # disable due to ui performance down
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

    def bind_widgets_events(self):
        """Bind events for the widgets."""
        # self.playlist_main_frame.bind("<Enter>", self.on_mouse_enter_self)
        # self.playlist_main_frame.bind("<Leave>", self.on_mouse_leave_self)

        self.bind("<Configure>", self.configure_widget_sizes)

        """
        for child_widgets in self.playlist_main_frame.winfo_children() + self.playlist_item_frame.winfo_children():
            child_widgets.bind("<Enter>", self.on_mouse_enter_self)
            child_widgets.bind("<Leave>", self.on_mouse_leave_self)
            try:
                for sub_child_widgets in child_widgets.winfo_children():
                    sub_child_widgets.bind("<Enter>", self.on_mouse_enter_self)
                    sub_child_widgets.bind("<Leave>", self.on_mouse_leave_self)
            except Exception as error:
                print(f"1@PlayList.py > Err : {error}")
                pass
        """
        
        def on_mouse_enter_channel_btn(_event):
            self.channel_btn.configure(
                text_color=ThemeManager.get_color_based_on_theme_mode(
                    AppearanceSettings.settings["video_object"]["btn_text_color"]["hover"]
                ),
            )
            # self.on_mouse_enter_self(event)

        def on_mouse_leave_channel_btn(_event):
            self.channel_btn.configure(
                text_color=ThemeManager.get_color_based_on_theme_mode(
                    AppearanceSettings.settings["video_object"]["btn_text_color"]["normal"]
                ),
            )

        self.channel_btn.bind("<Enter>", on_mouse_enter_channel_btn)
        self.channel_btn.bind("<Leave>", on_mouse_leave_channel_btn)

        def on_mouse_enter_remove_btn(_event):
            self.remove_btn.configure(
                fg_color=AppearanceSettings.settings["video_object"]["error_color"]["hover"],
                text_color=AppearanceSettings.settings["video_object"]["remove_btn_text_color"]["hover"]
            )
            # self.on_mouse_enter_self(event)

        def on_mouse_leave_remove_btn(_event):
            self.remove_btn.configure(
                fg_color=AppearanceSettings.settings["video_object"]["error_color"]["normal"],
                text_color=AppearanceSettings.settings["video_object"]["remove_btn_text_color"]["normal"]
            )

        self.remove_btn.bind("<Enter>", on_mouse_enter_remove_btn)
        self.remove_btn.bind("<Leave>", on_mouse_leave_remove_btn)

    # place widgets
    def place_widgets(self):
        """Place the widgets."""
        scale = AppearanceSettings.settings["scale_r"]

        self.playlist_main_frame.pack(fill="x")
        self.view_btn.place(rely=0.7, x=15 * scale, anchor="w")

        self.info_frame.place(x=50*scale + 15 * scale, y=1)

        self.playlist_title_label.place(x=0, rely=0.2, anchor="w")
        self.channel_btn.place(x=0, rely=0.5, anchor="w")
        self.url_label.place(x=0, rely=0.8, anchor="w")

        self.playlist_video_count_label.place(relx=1, x=-40 * scale, rely=0.8, anchor="w")
        self.remove_btn.place(relx=1, x=-25 * scale, y=3 * scale)

    def configure_widget_sizes(self, _event):
        ...
        
    def __del__(self):
        """Clear the Memory."""
        self.root = None
        self.master_frame = None
        
        del self.height
        del self.width
        
        # playlist info
        del self.channel_url
        del self.channel
        del self.playlist_url
        del self.playlist_title
        del self.playlist_video_count

        # widgets
        del self.view_btn
        del self.info_frame
        del self.playlist_title_label
        del self.channel_btn
        del self.url_label
        del self.playlist_main_frame
        del self.remove_btn
        del self.playlist_video_count_label
        del self.playlist_item_frame
        
        del self.videos
        
        del self

    def destroy_widgets(self):
        """Destroy the child widget."""
        self.playlist_main_frame.destroy()
        self.view_btn.destroy()
        self.info_frame.destroy()
        self.playlist_title_label.destroy()
        self.channel_btn.destroy()
        self.url_label.destroy()
        self.remove_btn.destroy()
        self.playlist_video_count_label.destroy()
        self.playlist_item_frame.destroy()
                
        super().destroy()

    def kill(self):
        """Destroy the playlist widget."""
        ThemeManager.unregister_widget(self)
        LanguageManager.unregister_widget(self)
        self.destroy_widgets()
        self.__del__()