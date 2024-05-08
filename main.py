from app import App
import customtkinter as ctk
from widgets import AlertWindow
from settings import (
    AppearanceSettings,
    GeneralSettings,
    WidgetPositionSettings
)
from services import (
    DownloadManager,
    LoadManager,
    ThemeManager,
    LoadingIndicateManager,
)
from utils import FileUtility


# configure settings
GeneralSettings.initialize("data\\general.json")
AppearanceSettings.initialize("data\\appearance.json")
WidgetPositionSettings.initialize("data\\widget_positions.json")

# Initialize app.
app = App()

# configure services
LoadManager.initialize(app.update_videos_count_status)
DownloadManager.initialize(app.update_videos_count_status)
ThemeManager.initialize()
LoadingIndicateManager.initialize()

# Check directory accessibility during startup.
# If accessible, nothing happens if not, show an error message.
scale = AppearanceSettings.settings["scale_r"]
DIRECTORIES = ["temp", GeneralSettings.settings["download_directory"]]
for directory in DIRECTORIES:
    if not FileUtility.is_accessible(directory):
        AlertWindow(
            master=app,
            alert_msg="Please run this application as an administrator...!",
            ok_button_text="ok",
            ok_button_callback=app.on_app_closing,
            callback=app.on_app_closing,
            width=int(450 * scale),
            height=int(130 * scale),
        )

# set the theme mode, dark or light or system, by getting from data
ctk.set_appearance_mode(AppearanceSettings.settings["root"]["theme_mode"])
# deactivate the automatic scale
ctk.deactivate_automatic_dpi_awareness()
# place the app at the last placed geometry
app.geometry(GeneralSettings.settings["window_geometry"])
# set minimum window size to 900x500
app.minsize(int(900 * scale), int(500 * scale))
# configure alpha
app.attributes("-alpha", AppearanceSettings.settings["opacity_r"])
# set the title icon
app.iconbitmap("assets\\main icon\\icon.ico")
# set the app title
app.title("PyTube Downloader")
# Create the main widgets of the application
app.create_widgets()
# set widgets sizes
app.set_widgets_sizes()
# place main widgets
app.place_widgets()
# configure colors for main widgets
app.set_widgets_colors()
# configure theme color
app.set_widgets_accent_color()
# configure fonts for main widgets
app.set_widgets_fonts()
# app event bind
app.bind_widgets_events()
# just rut the app
app.run()
