from PIL import Image
import pystray
from typing import Callable


class TrayMenu:
    def __init__(
            self,
            open_command: Callable = None,
            quit_command: Callable = None):

        self.tray_image = Image.open("src/icon.ico")
        self.tray_menu = pystray.MenuItem("Open", open_command), pystray.MenuItem("Quit", quit_command)
        self.tray_icon = pystray.Icon("name", self.tray_image, "Network Info", self.tray_menu)

    def run(self):
        self.tray_icon.run()

    def stop(self):
        self.tray_icon.stop()
