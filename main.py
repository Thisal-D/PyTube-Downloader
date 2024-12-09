from app import App
import customtkinter as ctk
from settings import (
    AppearanceSettings,
    GeneralSettings
)
from services import (
    DownloadManager,
    LoadManager,
    ThemeManager,
    LoadingIndicateManager,
    LanguageManager,
    VideoCountTracker
)


# Initialize app.
app = App()

# configure settings
GeneralSettings.initialize()
AppearanceSettings.initialize()
LanguageManager.initialize()

scale = AppearanceSettings.settings["scale_r"]

# Check directory accessibility during startup.
# If accessible, nothing happens if not, show an error message.
app.run_accessibility_check()

# configure services
LoadManager.initialize(app.update_active_videos_count_status)
DownloadManager.initialize(app.update_active_videos_count_status)
VideoCountTracker.initialize(app.update_total_videos_count_status)
ThemeManager.initialize()
LoadingIndicateManager.initialize()

# set the theme mode, dark or light or system, by getting from data
ctk.set_appearance_mode(AppearanceSettings.themes[AppearanceSettings.settings["root"]["theme_mode"]])
# deactivate the automatic scale
ctk.deactivate_automatic_dpi_awareness()
# place the app at the last placed geometry
app.geometry(GeneralSettings.settings["window_geometry"])
# set minimum window size to 900x500
app.minsize(int(900 * scale), int(500 * scale))
# configure alpha
app.attributes("-alpha", AppearanceSettings.settings["opacity_r"])
# set the title icon
app.iconbitmap("assets\\main icon\\512x512.ico")
# set the app title
app.title("PyTube Downloader")
# Create the main widgets of the application
app.create_widgets()
# set widgets sizes
app.set_widgets_sizes()
# set texts depend on language
app.set_widgets_texts()
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
# bind shortcut keys
app.bind_keyboard_shortcuts()
# Check app updates       
app.run_update_check()
# just run the app
app.run()

# Codes under here will only execute when the app is closed
 