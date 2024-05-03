from app import App
import customtkinter as ctk
from widgets import AlertWindow
from settings import (
    ThemeSettings,
    GeneralSettings
)
from services import (
    DownloadManager,
    LoadManager,
    ThemeManager,
    LoadingIndicateManager
)
from utils import FileUtility
# configure settings
GeneralSettings.initialize("data\\general.json")
ThemeSettings.initialize("data\\theme.json")
# configure services
DownloadManager.initialize()
LoadManager.initialize()
ThemeManager.initialize()
LoadingIndicateManager.initialize()

# Initialize app.
app = App()

# Check directory accessibility during startup.
# If accessible, nothing happens if not, show an error message.
DIRECTORIES = ["temp", GeneralSettings.settings["download_directory"]]
for directory in DIRECTORIES:
    if not FileUtility.is_accessible(directory):
        AlertWindow(
            master=app,
            alert_msg="Please run this application as an administrator...!",
            ok_button_text="ok",
            ok_button_callback=app.on_app_closing,
            callback=app.on_app_closing
        )

# set the theme mode, dark or light or system, by getting from data
ctk.set_appearance_mode(ThemeSettings.settings["root"]["theme_mode"])
# deactivate the automatic scale
ctk.deactivate_automatic_dpi_awareness()
# place the app at the last placed geometry
app.geometry(GeneralSettings.settings["window_geometry"])
# set minimum window size to 900x500
app.minsize(900, 500)
# configure alpha
app.attributes("-alpha", ThemeSettings.settings["opacity"])
# set the title icon
app.iconbitmap("assets\\icon.ico")
# set the app title
app.title("PyTube Downloader")
# Create the main widgets of the application
app.create_widgets()
# place main widgets
app.place_widgets()
# configure colors for main widgets
app.set_widgets_colors()
# configure theme color
app.set_accent_color()
# configure fonts for main widgets
app.set_widgets_fonts()
# app event bind
app.bind_events()
# just rut the app
app.run()
