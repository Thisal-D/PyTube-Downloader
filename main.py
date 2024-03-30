from app import app
from functions.getThemeSettings import getThemeSettings
from functions.getGeneralSettings import getGeneralSettings
import customtkinter as ctk
import os


app_theme_settings = getThemeSettings()
app_general_settings = getGeneralSettings()


app = app(
    app_fg_color = app_theme_settings["app_fg_color"],
    app_btn_fg_color = app_theme_settings["app_btn_fg_color"],
    app_btn_fg_hover_color = app_theme_settings["app_btn_fg_hover_color"],
    app_frame_fg_color = app_theme_settings["app_frame_fg_color"],
    app_widget_fg_color = app_theme_settings["app_widget_fg_color"],
    app_widget_text_color = app_theme_settings["app_widget_text_color"],
    app_theme_color = app_theme_settings["app_theme_color"],
    app_theme_colors = app_theme_settings["default_theme_colors"]
)

ctk.deactivate_automatic_dpi_awareness()
app.geometry("900x500")
app.attributes("-alpha",0.97)
app.title("PyTube Downloader")
app.create_widgets()
app.place_widgets()
app.set_widgets_colors()
app.set_widgets_fonts()



"""#enable these line for test
urls = []
#tests
urls = ["https://www.youtube.com/shorts/gunhFbIeakA?feature=share",]
"https://www.youtube.com/watch?v=DM2vX8Ks93E",
"https://www.youtube.com/watch?v=WpnLehvOM6E",
"https://www.youtube.com/watch?v=iZW-5gpCC_Q",
"https://www.youtube.com/watch?v=R83W2XR3IC8",
"https://www.youtube.com/watch?v=q45jxjne3BU",
"https://www.youtube.com/watch?v=JTZU7FcAv-Y"]
for url in urls:
    app.link_entry.delete(0,"end")
    app.link_entry.insert(0, url)
    app.add_video()
"""

app.run()


[os.remove("temp\\"+file) for file in os.listdir("temp") if file != 'this directory is necessary']
