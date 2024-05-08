from PIL import Image
import pystray
from typing import Callable


class TrayMenu:
    """
    A class to manage a system tray menu for the application.

    Attributes:
        tray_image (PIL.Image): The image used for the tray icon.
        tray_menu (tuple): A tuple containing menu items for the tray menu.
        tray_icon (pystray.Icon): The system tray icon object.
    """

    def __init__(
            self,
            open_command: Callable = None,
            quit_command: Callable = None):
        """
        Initialize the TrayMenu object.

        Args:
            open_command (Callable, optional): The function to execute when "Open" menu item is clicked.
            quit_command (Callable, optional): The function to execute when "Quit" menu item is clicked.
        """
        self.tray_image = Image.open("assets/main icon/icon.ico")
        self.tray_menu = (
            pystray.MenuItem("Open", open_command),
            pystray.MenuItem("Quit", quit_command)
        )
        self.tray_icon = pystray.Icon("name", self.tray_image, "PyTube Downloader", self.tray_menu)

    def run(self):
        """
        Run the system tray icon.
        """
        self.tray_icon.run()

    def stop(self):
        """
        Stop the system tray icon.
        """
        self.tray_icon.stop()
