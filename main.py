from app import App
import customtkinter as ctk
import sys
from widgets import AlertWindow
from functions import (
    get_theme_settings,
    get_general_settings,
    accessible
)

# get the theme settings
# get the general settings
app_theme_settings = get_theme_settings()
app_general_settings = get_general_settings()

# Check directory access during startup.
# If accessible, nothing happens if not, show an error message.
DIRECTORIES = ["temp", app_general_settings["download_directory"]]
for directory in DIRECTORIES:
    if not accessible(directory):
        error_message = AlertWindow(
            error_msg="Please run this application as an administrator...!",
            button_text="ok",
            theme_settings=app_theme_settings,
        )
        error_message.show()
        sys.exit()

# Initialize app.
app = App(
    # settings
    general_settings=app_general_settings,
    theme_settings=app_theme_settings,
)

# set the theme mode, dark or light or system, by getting from settings
ctk.set_appearance_mode(app_theme_settings["root"]["theme_mode"])
# deactivate the automatic scale
ctk.deactivate_automatic_dpi_awareness()
# place the app at the last placed geometry
app.geometry(app_general_settings["geometry"])
# set minimum window size to 900x500
app.minsize(900, 500)
# set the title icon
app.iconbitmap("src\\icon.ico")
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
# configure alpha
app.attributes("-alpha", app_theme_settings["opacity"])
# initiate services
app.initiate_services()
app.configure_services_values()
# just rut the app
app.run()
