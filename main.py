from app import app
from widgets.addedVideo import addedVideo, Video
import customtkinter as ctk
import os


app = app(
    app_fg_color = ("#ffffff", "#101010"),
    app_btn_fg_color = ("#eeeeee","#202020"),
    app_btn_fg_hover_color = ("#cccccc","#252525"),
    app_frame_fg_color = ("#ffffff", "#101010"),
    app_widget_fg_color = ("#ffffff", "#101010"),
    app_widget_text_color = ("#404040", "#aaaaaa"),
    app_theme_color = ("#1f9bfd", "#1f9bfd"),
)


addedVideo.configure_loading_display()
app.geometry("900x500")
app.attributes("-alpha",0.97)
app.title("PyTube Downloader")
app.create_widgets()
app.place_widgets()
app.set_widgets_colors()
app.set_widgets_fonts()


#tests
urls = ["https://www.youtube.com/shorts/gunhFbIeakA?feature=share",
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

app.run()


[os.remove("temp\\"+file) for file in os.listdir("temp")]
[os.remove(file) for file in os.listdir() if file.split(".")[-1] == "mp4" or file.split(".")[-1] == "mp3"]
