from app import app
from widgets.addedVideo import addedVideo
import os

app = app()
addedVideo.configure_loading_display()
app.geometry("700x325")
app.attributes("-alpha",0.97)
app.title("Youtube Downloader")
app.create_widgets()
app.place_widgets()
app.set_widgets_colors()
app.set_widgets_fonts()
app.run()


[os.remove("temp\\"+file) for file in os.listdir("temp")]