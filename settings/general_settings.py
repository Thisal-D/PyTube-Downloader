from typing import Dict
from utils import JsonUtility
import os


class GeneralSettings:
    """
    A class to manage general settings for the application.
    """
    settings: Dict = {}
    file_path: str = ""

    @staticmethod
    def initialize(file_path: str) -> None:
        """
        Initialize settings from a JSON file.

        Args:
            file_path (str): The file path to the JSON settings file.

        Returns:
            GeneralSettings: An instance of GeneralSettings initialized with the settings from the JSON file.
        """
        settings = JsonUtility.read_from_file(file_path)

        if settings.get("download_directory") is False:
            settings["download_directory"] = f"C:\\users\\{os.getlogin()}\\downloads\\PyTube Downloader\\"

        GeneralSettings.settings = settings
        GeneralSettings.file_path = file_path

    @staticmethod
    def save_settings() -> None:
        """
        Save the current settings to a file.

        """
        JsonUtility.write_to_file(GeneralSettings.file_path, GeneralSettings.settings)
